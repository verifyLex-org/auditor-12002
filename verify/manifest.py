import argparse
import csv
import hashlib
import io
import re
import shutil
import subprocess
from pathlib import PurePosixPath

CSV = "data/manifesto.csv"
SUMS = "data/MANIFEST.sha256"
GOLD = "data/gold/gold-v1.csv"
SPLIT = "data/splits/split-v1.csv"
RAW = re.compile(r"data/raw/([A-Za-z0-9_-]+)/(original\.html|conferencia\.pdf|original\.xml)")
HEADER = ("ato_id", "path", "source_url")
git_path = shutil.which("git")
if git_path is None:
    raise RuntimeError("Git não encontrado no PATH")
GIT: str = git_path


def git(*args: str) -> bytes:
    # Argumentos internos em lista, sem interpretação por shell.
    return subprocess.check_output([GIT, *args])  # noqa: S603


def exists(spec: str) -> bool:
    # A referência é um argumento de cat-file, sem interpretação por shell.
    result = subprocess.run(  # noqa: S603
        [GIT, "cat-file", "-e", spec],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def blob(spec: str) -> bytes:
    return git("cat-file", "blob", spec)


def hashes(paths: set[str], ref: str) -> bytes:
    return "".join(
        f"{hashlib.sha256(blob(f'{ref}:{path}')).hexdigest()}  {path}\n" for path in sorted(paths)
    ).encode("ascii")


def check(base: str | None, stage: bool, print_hashes: bool) -> None:
    ref = "" if stage else "HEAD"
    files = (
        set(git("ls-files", "-z" if stage else "--cached").decode().split("\0"))
        if stage
        else (set(git("ls-tree", "-r", "--name-only", "-z", ref).decode().split("\0")))
    )
    raw_files = {path for path in files if path.startswith("data/raw/")}

    if not blob(f"{ref}:{CSV}"):
        placeholders = {
            f"data/raw/{{ato_id}}/{name}"
            for name in ("original.html", "conferencia.pdf", "original.xml")
        }
        scaffold_files = {CSV, SUMS, GOLD, SPLIT, *placeholders}
        anchors = ("refs/tags/corpus-v1", "refs/tags/gold-v1", base)
        if (
            raw_files != placeholders
            or any(blob(f"{ref}:{path}") for path in scaffold_files)
            or any(
                anchor
                and any(
                    exists(f"{anchor}:{path}") and blob(f"{anchor}:{path}")
                    for path in (CSV, SUMS, GOLD, SPLIT)
                )
                for anchor in anchors
            )
            or exists("refs/tags/corpus-v1")
            or exists("refs/tags/gold-v1")
        ):
            raise ValueError("Manifesto vazio permitido apenas no scaffold inicial do corpus")
        if not print_hashes:
            print("Corpus ainda não coletado: scaffold vazio verificado.")
        return

    with io.StringIO(blob(f"{ref}:{CSV}").decode("utf-8"), newline="") as stream:
        rows = csv.DictReader(stream, strict=True)
        if tuple(rows.fieldnames or ()) != HEADER:
            raise ValueError(f"Cabeçalho esperado: {','.join(HEADER)}")
        registered: set[str] = set()
        for row in rows:
            path = row.get("path") or ""
            match = RAW.fullmatch(path)
            if (
                None in row
                or not match
                or PurePosixPath(path).as_posix() != path
                or row.get("ato_id") != match[1]
                or not (row.get("source_url") or "").startswith("https://")
                or path in registered
            ):
                raise ValueError(f"Linha incorreta ou duplicada no manifesto: {row}")
            registered.add(path)

    if raw_files != registered:
        raise ValueError(f"Arquivos brutos divergentes: {sorted(raw_files ^ registered)}")
    expected = hashes({CSV, *registered}, ref)
    if print_hashes:
        print(expected.decode("ascii"), end="")
        return
    if blob(f"{ref}:{SUMS}") != expected:
        raise ValueError(f"{SUMS} diverge do manifesto ou de seus documentos")

    for anchor in ("refs/tags/gold-v1", base):
        if anchor and exists(f"{anchor}:{GOLD}"):
            if not exists(f"{ref}:{GOLD}") or blob(f"{ref}:{GOLD}") != blob(f"{anchor}:{GOLD}"):
                raise ValueError(f"Gold congelado diverge de {anchor}")

    corpus_tag = "refs/tags/corpus-v1"
    if exists(f"{corpus_tag}:{SUMS}"):
        for path in (CSV, SUMS, SPLIT):
            if blob(f"{ref}:{path}") != blob(f"{corpus_tag}:{path}"):
                raise ValueError(f"Corpus congelado diverge da tag: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base")
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--print-hashes", action="store_true")
    args = parser.parse_args()
    try:
        check(args.base, args.staged, args.print_hashes)
    except (ValueError, csv.Error, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Falha de integridade: {error}") from error


if __name__ == "__main__":
    main()
