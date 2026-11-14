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


ELEMENT_STYLE_JS = """(selector) => {
  const el = document.querySelector(selector);
  if (!el) return null;
  const parse = (c) => {
    const m = /rgba?\\(([^)]+)\\)/.exec(c || "");
    if (!m) return { r: 0, g: 0, b: 0, a: 0 };
    const [r, g, b, a = 1] = m[1].split(",").map((x) => parseFloat(x.trim()));
    return { r, g, b, a };
  };
  const over = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a),
    a: 1,
  });
  const lin = (v) => {
    const x = v / 255;
    return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
  };
  const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const layers = [];
  for (let a = el; a; a = a.parentElement) {
    const bg = parse(getComputedStyle(a).backgroundColor);
    if (bg.a > 0) {
      layers.push(bg);
      if (bg.a >= 0.99) break;
    }
  }
  const bodyToken = getComputedStyle(document.body).getPropertyValue("--md-default-bg-color").trim();
  let bg = layers.length && layers[layers.length - 1].a >= 0.99 ? layers.pop() : parse(bodyToken || "#fff");
  while (layers.length) bg = over(layers.pop(), bg);
  const s = getComputedStyle(el);
  let fg = parse(s.color);
  if (fg.a < 1) fg = over(fg, bg);
  const l1 = lum(fg);
  const l2 = lum(bg);
  return {
    scheme: document.body.getAttribute("data-md-color-scheme"),
    contrast: (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05),
    focusVisible: el.matches(":focus-visible"),
    outlineStyle: s.outlineStyle,
    outlineWidth: parseFloat(s.outlineWidth || "0"),
    fg: s.color,
    bg: s.backgroundColor,
  };
}"""


def _rects_separation(a: dict[str, float], b: dict[str, float]) -> float:
    """Distância mínima (px) entre dois retângulos; negativa indica sobreposição."""
    dx = max(b["left"] - a["right"], a["left"] - b["right"], 0.0)
    dy = max(b["top"] - a["bottom"], a["top"] - b["bottom"], 0.0)
    if dx > 0.0 or dy > 0.0:
        return float(max(dx, dy))
    overlap_x = min(a["right"], b["right"]) - max(a["left"], b["left"])
    overlap_y = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
    return -float(min(overlap_x, overlap_y))


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("selector", [".vlx-btn-primary", ".vlx-btn-secondary"])
def test_hero_cta_states_contrast(open_page: OpenPage, scheme: str, selector: str) -> None:
    """Botões CTA preservam contraste AA (>= 4,5:1) em repouso, hover e foco."""
    loaded = open_page("", viewport="desktop", scheme=scheme, reduced_motion=False)
    page = loaded.page
    expected_scheme = "slate" if scheme == "dark" else "default"

    rest = page.evaluate(ELEMENT_STYLE_JS, selector)
    assert rest is not None
    assert rest["scheme"] == expected_scheme
    assert rest["contrast"] >= 4.5, f"{selector} repouso {scheme}: {rest}"

    btn = page.locator(selector)
    btn.hover()
    page.wait_for_timeout(260)
    hovered = page.evaluate(ELEMENT_STYLE_JS, selector)
    assert hovered is not None
    assert hovered["contrast"] >= 4.5, f"{selector} hover {scheme}: {hovered}"

    # Garante modalidade de teclado para acionar :focus-visible real.
    page.mouse.move(0, 0)
    page.keyboard.press("Tab")
    page.evaluate("(sel) => document.querySelector(sel).focus()", selector)
    focused = page.evaluate(ELEMENT_STYLE_JS, selector)
    assert focused is not None
    assert focused["focusVisible"] is True
    assert focused["outlineStyle"] != "none"
    assert focused["outlineWidth"] >= 2.0
    assert focused["contrast"] >= 4.5, f"{selector} focus-visible {scheme}: {focused}"
    assert loaded.errors == []


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("viewport", ["tablet", "desktop"])
def test_navigation_cards_hover_no_overlap(open_page: OpenPage, scheme: str, viewport: str) -> None:
    """Cards de 'Escolha seu caminho' formam grade 2x2 e não se sobrepõem no hover."""
    loaded = open_page("", viewport=viewport, scheme=scheme, reduced_motion=False)
    page = loaded.page
    cards = page.locator(".grid.cards > ul > li")
    assert cards.count() == 4
    cards.first.scroll_into_view_if_needed()

    card_rects_js = """() => [...document.querySelectorAll('.grid.cards > ul > li')].map((el) => {
      const r = el.getBoundingClientRect();
      return { left: r.left, right: r.right, top: r.top, bottom: r.bottom };
    })"""
    rest_rects: list[dict[str, float]] = page.evaluate(card_rects_js)
    assert abs(rest_rects[0]["top"] - rest_rects[1]["top"]) < 2.0
    assert abs(rest_rects[2]["top"] - rest_rects[3]["top"]) < 2.0

    for idx in range(4):
        cards.nth(idx).hover()
        page.wait_for_timeout(280)
        rects: list[dict[str, float]] = page.evaluate(card_rects_js)
        hovered = rects[idx]
        for other_idx, other in enumerate(rects):
            if other_idx == idx:
                continue
            sep = _rects_separation(hovered, other)
            assert sep >= 12.0, f"card {idx} colidiu com card {other_idx} ({sep:.1f}px)"
    assert loaded.errors == []


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("viewport", ["mobile", "tablet", "desktop"])
def test_status_board_layout_and_contrast(open_page: OpenPage, scheme: str, viewport: str) -> None:
    """Painel de estado exibe 2 colunas no desktop/tablet, empilha no mobile e mantém AA."""
    loaded = open_page("", viewport=viewport, scheme=scheme, reduced_motion=True)
    page = loaded.page
    panels: list[dict[str, float]] = page.evaluate(
        """() => [...document.querySelectorAll('.vlx-status-panel')].map((el) => {
          const r = el.getBoundingClientRect();
          return { left: r.left, right: r.right, top: r.top, bottom: r.bottom };
        })"""
    )
    assert len(panels) == 2
    if viewport == "mobile":
        assert panels[1]["top"] >= panels[0]["bottom"] + 10.0
    else:
        assert abs(panels[0]["top"] - panels[1]["top"]) < 2.0
        assert panels[1]["left"] >= panels[0]["right"] + 12.0

    for pill in (".vlx-status-pill--ready", ".vlx-status-pill--roadmap"):
        res = page.evaluate(ELEMENT_STYLE_JS, pill)
        assert res is not None
        assert res["contrast"] >= 4.5, f"{pill} {scheme}: {res}"
    assert loaded.errors == []


def test_mobile_verdict_alignment_and_subpage_admonitions(open_page: OpenPage) -> None:
    """Bloco de veredito alinha colunas no mobile e subpáginas usam admonitions."""
    home = open_page("", viewport="mobile", scheme="dark", reduced_motion=True)
    rows: list[dict[str, float]] = home.page.evaluate(
        """() => [...document.querySelectorAll('.vlx-verdict-body > div')].map((row) => {
          const k = row.querySelector('.vlx-k').getBoundingClientRect();
          const v = row.querySelector('.vlx-v').getBoundingClientRect();
          return { kRight: k.right, vLeft: v.left };
        })"""
    )
    assert len(rows) == 5
    assert all(r["vLeft"] >= r["kRight"] for r in rows)

    for route in ("operacao/como-rodar/", "seguranca/threat-model/", "dominio/"):
        sub = open_page(route, viewport="desktop", scheme="light", reduced_motion=True)
        assert sub.page.locator(".md-typeset .admonition").count() >= 1
        assert sub.page.locator(".md-typeset blockquote").count() == 0
        assert sub.errors == []
