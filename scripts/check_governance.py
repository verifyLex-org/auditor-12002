"""Verificador determinístico de governança e cadeia de suprimentos do repositório."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REQUIRED_GOVERNANCE_FILES: tuple[str, ...] = (
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "PREREGISTRO.md",
    "pyproject.toml",
    "uv.lock",
    ".pre-commit-config.yaml",
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/tarefa_sprint.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/proposta_adr.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/docs.yml",
)

GOVERNED_FREEZE_FILES: frozenset[str] = frozenset(
    {
        "PREREGISTRO.md",
        "data/manifesto.csv",
        "data/MANIFEST.sha256",
        "data/gold/gold-v1.csv",
    }
)

FROZEN_CORPUS_FILES: frozenset[str] = frozenset(
    {
        "data/manifesto.csv",
        "data/MANIFEST.sha256",
        "data/gold/gold-v1.csv",
    }
)

CONVENTIONAL_PR_RE = re.compile(
    r"^(feat|fix|docs|test|refactor|chore|ci|perf|sec|build|revert)"
    r"(?:\([A-Za-z0-9._/-]+\))?(?:!)?:\s+\S.{2,}$"
)

ALLOWED_BRANCH_RE = re.compile(
    r"^(?:feat|fix|docs|sec|ci|chore|refactor|test|hotfix|release)/[A-Za-z0-9._/-]+$"
)

BOT_BRANCH_PREFIXES: tuple[str, ...] = ("dependabot/", "renovate/")
ACTION_USES_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)")
PINNED_SHA_ACTION_RE = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._/-]+@[0-9a-f]{40}$")


def check_required_files(root: Path) -> list[str]:
    """Garante existência e conteúdo não-vazio dos arquivos essenciais de governança."""
    errors: list[str] = []
    for rel_path in REQUIRED_GOVERNANCE_FILES:
        target = root / rel_path
        if not target.is_file():
            errors.append(f"Arquivo de governança obrigatório ausente: {rel_path}")
        elif target.stat().st_size == 0:
            errors.append(f"Arquivo de governança vazio (0 bytes): {rel_path}")
    return errors


def check_github_configs(root: Path) -> list[str]:
    """Verifica ausência de YAML vazio em `.github/` e pinning por SHA nos workflows."""
    errors: list[str] = []
    github_dir = root / ".github"
    if not github_dir.is_dir():
        return ["Diretório .github/ ausente."]

    for path in sorted(github_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix in {".yml", ".yaml"} and path.stat().st_size == 0:
            errors.append(f"Arquivo YAML vazio (0 bytes) em .github/: {rel}")
            continue

        if path.parent.name == "workflows" and path.suffix in {".yml", ".yaml"}:
            lines = path.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, start=1):
                match = ACTION_USES_RE.match(line)
                if not match:
                    continue
                target = match.group(1)
                if target.startswith("./"):
                    continue
                if not PINNED_SHA_ACTION_RE.match(target):
                    errors.append(
                        f"{rel}:{lineno}: Action externa deve estar pinada por SHA de 40 hex "
                        f"(encontrado: {target})"
                    )
    return errors


def check_pr_metadata(pr_title: str, head_ref: str) -> list[str]:
    """Valida título em Conventional Commits e padrão de branch do projeto em PRs."""
    errors: list[str] = []
    normalized_title = pr_title.strip()
    if normalized_title.upper().startswith(("WIP", "[WIP]")):
        errors.append(f"Título de PR com marcador WIP não pode ser integrado: {normalized_title!r}")
    elif not CONVENTIONAL_PR_RE.match(normalized_title):
        errors.append(
            "Título de PR fora do padrão Conventional Commits "
            f"('tipo(escopo): descrição'): {normalized_title!r}"
        )

    normalized_branch = head_ref.strip()
    is_bot_branch = normalized_branch.startswith(BOT_BRANCH_PREFIXES)
    if not is_bot_branch and not ALLOWED_BRANCH_RE.match(normalized_branch):
        errors.append(
            "Nome de branch fora da convenção do projeto "
            "(feat|fix|docs|sec|ci|chore|refactor|test|hotfix|release/<id>-<tema>): "
            f"{normalized_branch!r}"
        )
    return errors


def check_freeze_guard(
    changed_files: list[str],
    *,
    manifest_hash_nonempty: bool,
) -> tuple[list[str], list[str]]:
    """Detecta alterações em artefatos de pré-registro e corpus congelado."""
    normalized = {item.replace("\\", "/").strip() for item in changed_files if item.strip()}
    touched_governed = sorted(normalized & GOVERNED_FREEZE_FILES)
    if not touched_governed:
        return [], []

    warnings = [
        "Artefatos experimentais governados tocados neste PR: " + ", ".join(touched_governed)
    ]
    errors: list[str] = []
    touched_frozen = sorted(normalized & FROZEN_CORPUS_FILES)
    if manifest_hash_nonempty and touched_frozen:
        errors.append(
            "Alteração bloqueada pela regra de congelamento (TM-06): "
            "data/MANIFEST.sha256 já está preenchido na base, portanto alterações em "
            + ", ".join(touched_frozen)
            + " exigem nova versão de marco/gabarito."
        )
    return errors, warnings


def run_checks(
    root: Path,
    *,
    pr_title: str | None = None,
    pr_head_ref: str | None = None,
    changed_files: list[str] | None = None,
    manifest_hash_nonempty: bool = False,
) -> tuple[list[str], list[str]]:
    """Executa toda a bateria de verificações de governança do repositório."""
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(check_required_files(root))
    errors.extend(check_github_configs(root))

    if pr_title is not None or pr_head_ref is not None:
        errors.extend(check_pr_metadata(pr_title or "", pr_head_ref or ""))

    if changed_files:
        freeze_errors, freeze_warnings = check_freeze_guard(
            changed_files,
            manifest_hash_nonempty=manifest_hash_nonempty,
        )
        errors.extend(freeze_errors)
        warnings.extend(freeze_warnings)

    return errors, warnings


def _write_step_summary(summary_path: Path, errors: list[str], warnings: list[str]) -> None:
    lines = ["## Governança de Repositório — Auditor 12.002", ""]
    if warnings:
        lines.append("### Avisos")
        lines.extend(f"- {item}" for item in warnings)
        lines.append("")
    if errors:
        lines.append("### Falhas")
        lines.extend(f"- {item}" for item in errors)
    else:
        lines.append("- Todas as verificações determinísticas de governança passaram.")
    lines.append("")
    with summary_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada CLI do verificador de governança."""
    parser = argparse.ArgumentParser(
        description="Valida regras de governança e supply-chain do Auditor 12.002."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Raiz do repositório a ser inspecionada.",
    )
    parser.add_argument(
        "--pr-title",
        default=os.environ.get("PR_TITLE"),
        help="Título do Pull Request para validar Conventional Commits.",
    )
    parser.add_argument(
        "--pr-head-ref",
        default=os.environ.get("PR_HEAD_REF"),
        help="Nome da branch de origem do Pull Request.",
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        dest="changed_files",
        default=None,
        help="Arquivo alterado no PR (pode ser repetido; fallback em CHANGED_FILES).",
    )
    parser.add_argument(
        "--manifest-nonempty",
        action="store_true",
        default=os.environ.get("BASE_MANIFEST_NONEMPTY", "").lower() == "true",
        help="Indica que data/MANIFEST.sha256 já está preenchido na branch base.",
    )
    args = parser.parse_args(argv)

    changed_files = args.changed_files
    if changed_files is None:
        raw_env = os.environ.get("CHANGED_FILES", "")
        changed_files = [line for line in raw_env.splitlines() if line.strip()]

    errors, warnings = run_checks(
        args.root.resolve(),
        pr_title=args.pr_title,
        pr_head_ref=args.pr_head_ref,
        changed_files=changed_files,
        manifest_hash_nonempty=args.manifest_nonempty,
    )

    for warning in warnings:
        print(f"AVISO: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERRO: {error}", file=sys.stderr)

    summary_target = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_target:
        _write_step_summary(Path(summary_target), errors, warnings)

    if errors:
        return 1
    print("Governança verificada: todos os artefatos obrigatórios e workflows conformes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
