#!/usr/bin/env python3
"""Remove generated artifacts under projects/. Keep hand-authored sources."""

import argparse
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATED_NAMES = {
    "baseline.json",
    "baseline.draft.json",
    "delivery-brief.md",
    "scope-changelog.jsonl",
    "scope-decision.json",
    "pending-decision.json",
}


def is_generated(path: pathlib.Path) -> bool:
    if path.name in GENERATED_NAMES:
        return True
    if path.name.startswith("cr-") and path.suffix == ".md":
        return True
    if path.name.endswith(".extracted.txt"):
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--projects-dir",
        type=pathlib.Path,
        default=REPO_ROOT / "projects",
        help="Live project directory. Synthetic examples/ are never deleted.",
    )
    args = parser.parse_args()
    projects_dir = args.projects_dir

    if not projects_dir.is_dir():
        print(f"No projects directory at {projects_dir}. Nothing to reset.")
        return

    removed = []
    for path in sorted(projects_dir.rglob("*")):
        if path.is_file() and is_generated(path):
            path.unlink()
            removed.append(path)

    print("Removed generated artifacts:" if removed else "No generated artifacts found.")
    for path in removed:
        print(f"  {path}")

    remaining = [path for path in sorted(projects_dir.rglob("*")) if path.is_file()]
    print("\nHand-authored files:")
    for path in remaining:
        print(f"  {path}")


if __name__ == "__main__":
    main()
