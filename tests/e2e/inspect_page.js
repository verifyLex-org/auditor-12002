// Executado dentro da página pelo Playwright (page.evaluate). Devolve medições de layout e
// acessibilidade do portal; os limites (o que é falha) ficam no teste Python.
(checkContrast) => {
  const vw = document.documentElement.clientWidth;
  const out = { h1: 0, overflowPx: 0, overflowing: [], imgNoAlt: [], lowContrast: [] };
  out.h1 = document.querySelectorAll("article h1, .md-content h1").length;

  out.overflowPx = document.documentElement.scrollWidth - vw;
  if (out.overflowPx > 1) {
    const insideScroller = (el) => {
      for (let a = el; a; a = a.parentElement) {
        const s = getComputedStyle(a);
        if (/(auto|scroll|hidden)/.test(s.overflowX) && a.scrollWidth > a.clientWidth) return true;
      }
      return false;
    };
    for (const el of document.querySelectorAll("body *")) {
      const r = el.getBoundingClientRect();
      if (r.width && r.right > vw + 1 && !insideScroller(el.parentElement)) {
        out.overflowing.push(`${el.tagName.toLowerCase()}.${[...el.classList].join(".")}`);
        if (out.overflowing.length >= 5) break;
      }
    }
  }

  out.imgNoAlt = [...document.querySelectorAll("img:not([alt])")].map((i) => i.src).slice(0, 5);

  if (!checkContrast) return out;

  // Um canvas 1x1 normaliza rgb(), rgba() e color(srgb ...) (resultado de color-mix).
  // getImageData devolve valores já não pré-multiplicados.
  const cv = document.createElement("canvas");
  cv.width = cv.height = 1;
  const cx = cv.getContext("2d", { willReadFrequently: true });
  const parse = (c) => {
    if (!c || c === "transparent") return { r: 0, g: 0, b: 0, a: 0 };
    cx.clearRect(0, 0, 1, 1);
    cx.fillStyle = "rgba(0,0,0,0)";
    cx.fillStyle = c;
    cx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = cx.getImageData(0, 0, 1, 1).data;
    return { r, g, b, a: a / 255 };
  };
  const over = (top, under) => ({
    r: top.r * top.a + under.r * (1 - top.a),
    g: top.g * top.a + under.g * (1 - top.a),
    b: top.b * top.a + under.b * (1 - top.a),
    a: 1,
  });
  const lum = ({ r, g, b }) => {
    const f = (x) => {
      x = Math.min(255, Math.max(0, x)) / 255;
      return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  // Empilha as camadas de fundo até achar uma opaca e compõe de baixo para cima.
  // Fundo com gradiente ou imagem não é estimável: o elemento é ignorado.
  const bgOf = (el) => {
    const layers = [];
    for (let a = el; a; a = a.parentElement) {
      const s = getComputedStyle(a);
      if (s.backgroundImage && s.backgroundImage !== "none") return null;
      const c = parse(s.backgroundColor);
      if (c.a > 0) {
        layers.push(c);
        if (c.a >= 0.99) break;
      }
    }
    let acc =
      layers.length && layers[layers.length - 1].a >= 0.99
        ? layers.pop()
        : parse(getComputedStyle(document.documentElement).backgroundColor);
    if (acc.a < 0.99) {
      const token = getComputedStyle(document.body).getPropertyValue("--md-default-bg-color").trim();
      acc = parse(token || "#fff");
    }
    if (acc.a < 0.99) acc = { r: 255, g: 255, b: 255, a: 1 };
    while (layers.length) acc = over(layers.pop(), acc);
    return acc;
  };

  const selector = [
    ".md-content p", ".md-content li", ".md-content td", ".md-content th", ".md-content a",
    ".md-content span", ".md-content h1", ".md-content h2", ".md-content h3", ".md-content code",
    ".md-tabs__link", ".md-nav__link", ".md-banner", ".md-footer a",
  ].join(", ");
  const seen = new Set();
  for (const el of document.querySelectorAll(selector)) {
    if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const s = getComputedStyle(el);
    if (s.visibility === "hidden" || s.display === "none" || Number(s.opacity) < 0.2) continue;
    const rect = el.getBoundingClientRect();
    if (!rect.width || !rect.height) continue;
    const bg = bgOf(el);
    let fg = parse(s.color);
    if (!bg || fg.a === 0) continue;
    if (fg.a < 1) fg = over(fg, bg);
    const l1 = lum(fg);
    const l2 = lum(bg);
    const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    const size = parseFloat(s.fontSize);
    const large = size >= 24 || (Number(s.fontWeight) >= 700 && size >= 18.66);
    const need = large ? 3 : 4.5;
    if (ratio < need) {
      const cls = el.className ? "." + String(el.className).split(" ")[0] : "";
      const text = el.textContent.trim().slice(0, 40);
      const item = `${el.tagName.toLowerCase()}${cls} "${text}" ${ratio.toFixed(2)} < ${need}`;
      if (!seen.has(item)) {
        seen.add(item);
        out.lowContrast.push(item);
      }
    }
  }
  return out;
}
