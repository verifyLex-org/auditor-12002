"""Hook do MkDocs que valida o HTML final gerado em `site/` (on_post_build).

O `mkdocs build --strict` verifica links escritos em Markdown, mas não valida
links escritos em HTML bruto nem scripts carregados por extensões/tema.
Este hook inspeciona o site compilado e interrompe o build quando encontra:

- link interno que não resolve para um arquivo dentro de `site_dir`;
- link com esquema `javascript:`;
- tag `<script src="...">` apontando para domínio externo (garante execução offline);
- página de conteúdo sem exatamente um `<h1>`;
- grade de cartões (`.grid.cards`) com texto ou elemento solto fora da lista.
"""

from __future__ import annotations

import posixpath
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from mkdocs.exceptions import PluginError

NON_CONTENT_PAGES = {"404.html", "search.html"}

VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}


class _PageScanner(HTMLParser):
    """Coleta scripts da página, links/títulos de `<article>` e desvios em `.grid.cards`."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.h1_count = 0
        self.grid_strays: list[str] = []
        self._article_depth = 0
        self._open: list[tuple[str, bool]] = []

    def _inside_grid(self) -> bool:
        return bool(self._open) and self._open[-1][1]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if self._inside_grid() and tag not in ("ul", "ol"):
            self.grid_strays.append(f"<{tag}>")
        if tag not in VOID_TAGS:
            classes = set((values.get("class") or "").split())
            self._open.append((tag, tag == "div" and {"grid", "cards"} <= classes))

        src = values.get("src")
        if tag == "script" and src:
            self.scripts.append(src)
        if tag == "article":
            self._article_depth += 1
        if not self._article_depth:
            return
        href = values.get("href")
        if tag == "a" and href:
            self.links.append(href)
        elif tag == "h1":
            self.h1_count += 1

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._open) - 1, -1, -1):
            if self._open[index][0] == tag:
                del self._open[index:]
                break
        if tag == "article" and self._article_depth:
            self._article_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._inside_grid() and data.strip():
            self.grid_strays.append(data.strip()[:40])


def _resolve(site_dir: Path, page: Path, href: str) -> Path | None:
    """Resolve um `href` interno relativo para o arquivo esperado dentro de `site_dir`."""
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or not parts.path:
        return None
    if parts.path.startswith("/"):
        # Links absolutos gerados pelo tema carregam o prefixo de site_url (/auditor-12002/).
        return None
    page_dir = page.parent.relative_to(site_dir).as_posix()
    target = posixpath.normpath(posixpath.join(page_dir, unquote(parts.path)))
    resolved = site_dir / target
    if parts.path.endswith("/") or resolved.is_dir():
        resolved = resolved / "index.html"
    return resolved


def on_post_build(config: Any, **kwargs: Any) -> None:
    """Valida todas as páginas HTML geradas após a compilação do MkDocs."""
    site_dir = Path(config["site_dir"]).resolve()
    problems: list[str] = []

    for page in sorted(site_dir.rglob("*.html")):
        relative = page.relative_to(site_dir).as_posix()
        scanner = _PageScanner()
        scanner.feed(page.read_text(encoding="utf-8"))

        for href in scanner.links:
            if href.strip().lower().startswith("javascript:"):
                problems.append(f"{relative}: link javascript: proibido ({href})")
                continue
            target = _resolve(site_dir, page, href)
            if target is not None and (
                not target.resolve().is_relative_to(site_dir) or not target.is_file()
            ):
                problems.append(f"{relative}: link interno quebrado -> {href}")

        for src in scanner.scripts:
            if urlsplit(src).netloc:
                problems.append(f"{relative}: script de domínio externo proibido -> {src}")

        for stray in scanner.grid_strays:
            problems.append(f"{relative}: conteúdo fora dos cartões da grade -> {stray}")

        if relative not in NON_CONTENT_PAGES and scanner.h1_count != 1:
            problems.append(
                f"{relative}: esperado exatamente 1 <h1>, encontrados {scanner.h1_count}"
            )

    if problems:
        detail = "\n  ".join(problems)
        raise PluginError(f"Verificação do site falhou ({len(problems)} problemas):\n  {detail}")
