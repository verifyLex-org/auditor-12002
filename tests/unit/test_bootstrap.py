import sys


def test_python_version_matches_project_contract() -> None:
    assert sys.version_info[:2] == (3, 12)
