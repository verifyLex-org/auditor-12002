from pathlib import Path

import pytest

from verify import manifest


@pytest.fixture
def corpus_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    manifest.git("init", "--quiet")
    manifest.git("config", "user.name", "Teste")
    manifest.git("config", "user.email", "teste@example.com")
    for name in (
        manifest.CSV,
        manifest.SUMS,
        manifest.GOLD,
        manifest.SPLIT,
        "data/raw/{ato_id}/original.html",
        "data/raw/{ato_id}/conferencia.pdf",
        "data/raw/{ato_id}/original.xml",
    ):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"")
    manifest.git("add", ".")
    manifest.git("commit", "--quiet", "-m", "Scaffold inicial")
    return tmp_path


@pytest.mark.parametrize("staged", [False, True])
def test_empty_scaffold_is_valid(corpus_repo: Path, staged: bool) -> None:
    manifest.check(None, staged, False)


def test_scaffold_rejects_raw_content(corpus_repo: Path) -> None:
    (corpus_repo / "data/raw/{ato_id}/original.html").write_bytes(b"documento")
    manifest.git("add", ".")
    with pytest.raises(ValueError, match="scaffold inicial"):
        manifest.check(None, True, False)


@pytest.mark.parametrize("tag", ["corpus-v1", "gold-v1"])
def test_scaffold_rejects_frozen_tags(corpus_repo: Path, tag: str) -> None:
    manifest.git("tag", tag)
    with pytest.raises(ValueError, match="scaffold inicial"):
        manifest.check(None, True, False)


def test_scaffold_rejects_erasing_populated_base(corpus_repo: Path) -> None:
    (corpus_repo / manifest.GOLD).write_bytes(b"gold congelado\n")
    manifest.git("add", ".")
    manifest.git("commit", "--quiet", "-m", "Gold preenchido")
    (corpus_repo / manifest.GOLD).write_bytes(b"")
    manifest.git("add", ".")
    with pytest.raises(ValueError, match="scaffold inicial"):
        manifest.check("HEAD", True, False)


def test_populated_manifest_still_requires_header(corpus_repo: Path) -> None:
    (corpus_repo / manifest.CSV).write_bytes(b"cabecalho,invalido\n")
    manifest.git("add", ".")
    with pytest.raises(ValueError, match="Cabeçalho esperado"):
        manifest.check(None, True, False)


@pytest.mark.parametrize("corrupt_hashes", [False, True])
def test_collected_corpus_requires_matching_hashes(corpus_repo: Path, corrupt_hashes: bool) -> None:
    manifest.git("rm", "-r", "--quiet", "data/raw")
    raw_path = "data/raw/ato-1/original.html"
    document = corpus_repo / raw_path
    document.parent.mkdir(parents=True)
    document.write_bytes(b"ato normativo\n")
    (corpus_repo / manifest.CSV).write_bytes(
        f"ato_id,path,source_url\nato-1,{raw_path},https://example.com/ato-1\n".encode()
    )
    manifest.git("add", ".")
    sums = b"hash incorreto\n" if corrupt_hashes else manifest.hashes({manifest.CSV, raw_path}, "")
    (corpus_repo / manifest.SUMS).write_bytes(sums)
    manifest.git("add", ".")
    if corrupt_hashes:
        with pytest.raises(ValueError, match="diverge do manifesto"):
            manifest.check(None, True, False)
    else:
        manifest.check(None, True, False)
