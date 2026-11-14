"""Infraestrutura dos testes E2E do portal: servidor estático local e navegador Chromium."""

from __future__ import annotations

import os
import threading
from collections.abc import Iterator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Browser, Playwright, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


class _LocalServer(ThreadingHTTPServer):
    # Backlog padrão (5) do stdlib pode recusar rajadas simultâneas do Chromium no Windows.
    request_queue_size = 128


@pytest.fixture(scope="session")
def site_dir() -> Path:
    """Site já compilado por `mkdocs build --strict` (ou `AUDITOR_SITE_DIR`)."""
    target = Path(os.environ.get("AUDITOR_SITE_DIR", REPO_ROOT / "site")).resolve()
    if not (target / "index.html").is_file():
        pytest.fail(
            f"Site compilado não encontrado em {target}. "
            "Rode `uv run --frozen mkdocs build --strict` antes dos testes E2E."
        )
    return target


@pytest.fixture(scope="session")
def base_url(site_dir: Path) -> Iterator[str]:
    """Serve o site em 127.0.0.1 numa porta livre durante a sessão de testes."""
    handler = partial(_QuietHandler, directory=str(site_dir))
    server = _LocalServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture(scope="session")
def playwright_instance() -> Iterator[Playwright]:
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Iterator[Browser]:
    instance = playwright_instance.chromium.launch(headless=True)
    try:
        yield instance
    finally:
        instance.close()
