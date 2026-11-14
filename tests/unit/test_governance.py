"""Testes unitários das verificações de governança do repositório."""

from __future__ import annotations

from pathlib import Path

from scripts.check_governance import (
    REQUIRED_GOVERNANCE_FILES,
    check_freeze_guard,
    check_github_configs,
    check_pr_metadata,
    check_required_files,
    run_checks,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_real_repository_governance_passes() -> None:
    """O próprio repositório deve atender todas as regras base de governança."""
    errors, warnings = run_checks(REPO_ROOT)
    assert errors == []
    assert warnings == []


def test_detects_missing_or_empty_governance_file(tmp_path: Path) -> None:
    """Arquivos obrigatórios ausentes ou vazios devem gerar falha explícita."""
    for rel in REQUIRED_GOVERNANCE_FILES:
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("ok\n", encoding="utf-8")

    (tmp_path / "SECURITY.md").write_text("", encoding="utf-8")
    (tmp_path / "LICENSE").unlink()

    errors = check_required_files(tmp_path)
    assert any("LICENSE" in err for err in errors)
    assert any("SECURITY.md" in err for err in errors)


def test_rejects_unpinned_action_and_empty_workflow(tmp_path: Path) -> None:
    """Workflows com 0 bytes ou Actions sem SHA de 40 dígitos devem falhar."""
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "empty.yml").write_text("", encoding="utf-8")
    (wf_dir / "bad.yml").write_text(
        "jobs:\n  build:\n    steps:\n      - uses: actions/checkout@v4\n",
        encoding="utf-8",
    )
    (wf_dir / "good.yml").write_text(
        "jobs:\n"
        "  build:\n"
        "    steps:\n"
        "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1\n"
        "      - uses: ./.github/actions/local-helper\n",
        encoding="utf-8",
    )

    errors = check_github_configs(tmp_path)
    assert any("empty.yml" in err for err in errors)
    assert any("actions/checkout@v4" in err for err in errors)
    assert not any("good.yml" in err for err in errors)


def test_pr_metadata_validation() -> None:
    """Valida Conventional Commits no título e convenção de branch do Auditor 12.002."""
    assert check_pr_metadata("feat(rules): implementa regra R1@1.0", "feat/12-regra-R1") == []
    assert (
        check_pr_metadata("ci(deps): bump actions/checkout", "dependabot/github_actions/v7") == []
    )

    bad_title = check_pr_metadata("ajusta coisas", "feat/12-regra-R1")
    assert len(bad_title) == 1

    wip_title = check_pr_metadata("WIP: testando parser", "feat/12-regra-R1")
    assert len(wip_title) == 1

    bad_branch = check_pr_metadata("fix(parser): corrige encoding", "minha-branch-solta")
    assert len(bad_branch) == 1


def test_freeze_guard_behavior() -> None:
    """Pré-congelamento emite aviso; pós-congelamento bloqueia alteração em corpus/gold."""
    pre_errors, pre_warnings = check_freeze_guard(
        ["PREREGISTRO.md", "data/manifesto.csv"],
        manifest_hash_nonempty=False,
    )
    assert pre_errors == []
    assert len(pre_warnings) == 1

    post_errors, post_warnings = check_freeze_guard(
        ["data/gold/gold-v1.csv"],
        manifest_hash_nonempty=True,
    )
    assert len(post_errors) == 1
    assert "TM-06" in post_errors[0]
    assert len(post_warnings) == 1
