#!/usr/bin/env python3
"""Install both skills and their shared runtime without breaking relative paths."""

import argparse
import pathlib
import shutil
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_NAMES = ("sow-intake", "scope-sentinel")
RUNTIME_NAME = ".delivery-guardrails"
RUNTIME_DIRS = ("config", "schemas", "scripts", "templates")


def copy_tree(source: pathlib.Path, destination: pathlib.Path):
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=pathlib.Path, help="Skills directory, for example ~/.codex/skills")
    parser.add_argument("--force", action="store_true", help="Replace a previous installation")
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    destinations = [target / name for name in SKILL_NAMES]
    runtime = target / RUNTIME_NAME
    existing = [path for path in [*destinations, runtime] if path.exists()]
    if existing and not args.force:
        names = ", ".join(str(path) for path in existing)
        sys.exit(f"Refusing to overwrite existing paths: {names}. Re-run with --force.")

    for path in existing:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

    for name, destination in zip(SKILL_NAMES, destinations):
        copy_tree(REPO_ROOT / "skills" / name, destination)

    runtime.mkdir()
    for directory in RUNTIME_DIRS:
        copy_tree(REPO_ROOT / directory, runtime / directory)
    shutil.copy2(REPO_ROOT / "requirements.txt", runtime / "requirements.txt")

    required = [
        *(destination / "SKILL.md" for destination in destinations),
        runtime / "scripts" / "validate_citations.py",
        runtime / "schemas" / "baseline.schema.json",
        runtime / "templates" / "change-request.md",
    ]
    missing = [path for path in required if not path.is_file()]
    if missing:
        sys.exit(f"Installation is incomplete; missing: {missing}")

    print(f"Installed {len(SKILL_NAMES)} skills in {target}")
    print(f"Shared runtime: {runtime}")
    print(f"Install dependencies: python -m pip install -r {runtime / 'requirements.txt'}")


if __name__ == "__main__":
    main()
