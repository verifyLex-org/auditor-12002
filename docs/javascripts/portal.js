/* Revelação suave ao rolar para as páginas internas do portal.
 *
 * Aprimoramento progressivo: sem JS (ou com movimento reduzido) o conteúdo
 * aparece normalmente. As classes `vlx-io` só são aplicadas por este script,
 * portanto uma falha aqui nunca deixa conteúdo oculto.
 */
(function () {
  "use strict";

  var TARGETS = [
    ".md-typeset h2",
    ".md-typeset .md-typeset__table",
    ".md-typeset .admonition",
    ".md-typeset details",
    ".md-typeset .mermaid",
    ".md-typeset .highlight",
    ".md-typeset .tabbed-set",
    ".md-typeset .vlx-card",
    ".md-typeset .vlx-step",
    ".md-typeset .vlx-tl-item",
    ".md-typeset .vlx-meter"
  ].join(",");

  var SAFETY_MS = 2500;
  var observer = null;
  var safetyTimer = 0;

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function reveal(el) {
    el.classList.add("is-in");
    if (observer) {
      observer.unobserve(el);
    }
  }

  function teardown() {
    if (observer) {
      observer.disconnect();
      observer = null;
    }
    window.clearTimeout(safetyTimer);
  }

  function init() {
    teardown();
    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
      return;
    }

    var nodes = Array.prototype.filter.call(document.querySelectorAll(TARGETS), function (el) {
      return !el.closest(".vlx-landing-wrap") && !el.classList.contains("vlx-rv");
    });
    if (!nodes.length) {
      return;
    }

    observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            reveal(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );

    nodes.forEach(function (el) {
      var parent = el.parentElement;
      var siblings = parent ? parent.children : [];
      el.style.setProperty("--i", String(Array.prototype.indexOf.call(siblings, el)));
      el.classList.add("vlx-io");
      observer.observe(el);
    });

    safetyTimer = window.setTimeout(function () {
      document.querySelectorAll(".vlx-io:not(.is-in)").forEach(function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight) {
          el.classList.add("is-in");
        }
      });
    }, SAFETY_MS);
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
