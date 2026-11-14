"""Testes E2E do portal MkDocs: erros, layout responsivo, contraste AA e conteúdo visível.

Cada página pública é aberta num Chromium real servido localmente. Requisições para fora
do servidor local são bloqueadas para manter os testes determinísticos e offline; as que
apontam para o `site_url` de produção (o plugin `privacy` reescreve recursos carregados por
JavaScript, como o Mermaid, com URL absoluta) são servidas pelo site local.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Browser, ConsoleMessage, Page, Response, Route, ViewportSize

pytestmark = pytest.mark.e2e

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs"
EXCLUDED_DOC_DIRS = frozenset({"_templates"})


def expected_page_paths() -> list[str]:
    """Rotas públicas esperadas, derivadas de `docs/` (use_directory_urls do MkDocs)."""
    routes: list[str] = []
    for md in sorted(DOCS_DIR.rglob("*.md")):
        rel = md.relative_to(DOCS_DIR)
        if rel.parts[0] in EXCLUDED_DOC_DIRS:
            continue
        parent = rel.parent.as_posix()
        prefix = "" if parent == "." else f"{parent}/"
        routes.append(prefix if rel.stem == "index" else f"{prefix}{rel.stem}/")
    return routes


def production_site_url() -> str:
    """`site_url` do mkdocs.yml, com barra final."""
    text = (REPO_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    match = re.search(r"^site_url:\s*(\S+)\s*$", text, flags=re.MULTILINE)
    if match is None:
        raise RuntimeError("site_url ausente em mkdocs.yml")
    return match.group(1).strip("\"'").rstrip("/") + "/"


PAGES = expected_page_paths()
SITE_URL = production_site_url()
INSPECT_JS = (Path(__file__).with_name("inspect_page.js")).read_text(encoding="utf-8")

VIEWPORTS: dict[str, ViewportSize] = {
    "mobile": {"width": 375, "height": 812},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1440, "height": 900},
}

# Percorre a página para disparar as animações de revelação ligadas à rolagem.
SCROLL_THROUGH_JS = """async () => {
  for (let y = 0; y < document.body.scrollHeight; y += 400) {
    window.scrollTo(0, y);
    await new Promise((r) => setTimeout(r, 20));
  }
  window.scrollTo(0, 0);
}"""

# Leva cada bloco animado ao centro da tela e mede a opacidade final lá.
INVISIBLE_AFTER_SCROLL_JS = """async () => {
  const bad = [];
  const blocks = document.querySelectorAll(
    ".md-content__inner > :nth-child(-n+3), [class*='-reveal'], [class*='-rv']");
  for (const el of blocks) {
    if (!el.getBoundingClientRect().height) continue;
    el.scrollIntoView({ block: "center" });
    await new Promise((r) => setTimeout(r, 120));
    const opacity = Number(getComputedStyle(el).opacity);
    if (opacity < 0.9) bad.push(`${el.tagName.toLowerCase()}.${[...el.classList].join(".")}`);
  }
  window.scrollTo(0, 0);
  return [...new Set(bad)];
}"""


@dataclass
class LoadedPage:
    page: Page
    errors: list[str] = field(default_factory=list)


OpenPage = Callable[..., LoadedPage]


@pytest.fixture
def open_page(browser: Browser, base_url: str) -> Iterator[OpenPage]:
    """Abre uma rota com viewport, esquema de cor e preferência de movimento definidos."""
    contexts = []

    def _open(route: str, *, viewport: str, scheme: str, reduced_motion: bool) -> LoadedPage:
        mobile = viewport == "mobile"
        context = browser.new_context(
            viewport=VIEWPORTS[viewport],
            color_scheme="dark" if scheme == "dark" else "light",
            reduced_motion="reduce" if reduced_motion else "no-preference",
            is_mobile=mobile,
            has_touch=mobile,
        )
        contexts.append(context)

        def _gate(request_route: Route) -> None:
            url = request_route.request.url
            if url.startswith(base_url):
                request_route.continue_()
            elif url.startswith(SITE_URL):
                local = request_route.fetch(url=base_url + url.removeprefix(SITE_URL))
                request_route.fulfill(response=local)
            else:
                request_route.abort()

        context.route("**/*", _gate)
        page = context.new_page()
        loaded = LoadedPage(page=page)

        def _on_console(msg: ConsoleMessage) -> None:
            origin = msg.location.get("url", "")
            if msg.type == "error" and (not origin or origin.startswith((base_url, SITE_URL))):
                loaded.errors.append(f"console: {msg.text[:200]}")

        def _on_response(response: Response) -> None:
            own = response.url.startswith((base_url, SITE_URL))
            if own and response.status >= 400:
                loaded.errors.append(f"HTTP {response.status}: {response.url}")

        page.on("console", _on_console)
        page.on("pageerror", lambda exc: loaded.errors.append(f"pageerror: {exc}"))
        page.on("response", _on_response)
        page.goto(base_url + route, wait_until="networkidle", timeout=30_000)
        return loaded

    yield _open
    for context in contexts:
        context.close()


def test_every_doc_page_was_built(site_dir: Path) -> None:
    """Toda página de `docs/` deve existir no site compilado."""
    missing = [route for route in PAGES if not (site_dir / route / "index.html").is_file()]
    assert missing == []


@pytest.mark.parametrize("route", PAGES, ids=lambda r: r or "home")
@pytest.mark.parametrize("viewport", list(VIEWPORTS))
def test_layout(open_page: OpenPage, route: str, viewport: str) -> None:
    """Sem erros, um único H1, sem rolagem horizontal, imagens com alt e conteúdo visível."""
    loaded = open_page(route, viewport=viewport, scheme="light", reduced_motion=False)
    loaded.page.evaluate(SCROLL_THROUGH_JS)
    data: dict[str, Any] = loaded.page.evaluate(INSPECT_JS, False)
    invisible: list[str] = loaded.page.evaluate(INVISIBLE_AFTER_SCROLL_JS)

    assert loaded.errors == []
    assert data["h1"] == 1, f"esperado 1 <h1>, encontrado {data['h1']}"
    assert data["overflowPx"] <= 1, f"rolagem horizontal de {data['overflowPx']}px: {data}"
    assert data["imgNoAlt"] == []
    assert invisible == []


@pytest.mark.parametrize("route", PAGES, ids=lambda r: r or "home")
@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_contrast_aa(open_page: OpenPage, route: str, scheme: str) -> None:
    """Texto com contraste WCAG AA (4,5:1; 3:1 para texto grande) nos modos claro e escuro."""
    loaded = open_page(route, viewport="desktop", scheme=scheme, reduced_motion=True)
    data: dict[str, Any] = loaded.page.evaluate(INSPECT_JS, True)

    assert loaded.errors == []
    assert data["lowContrast"] == []
