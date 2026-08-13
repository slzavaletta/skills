#!/usr/bin/env python3
"""Print the shared runtime root for these skills.

Looks for this repository layout or an installed `.delivery-guardrails`
directory next to the skill folders. Skills should call this instead of
guessing parent directories.
"""

import argparse
import pathlib
import sys

SCRIPT_PATH = pathlib.Path(__file__).resolve()


def candidate_roots():
    yield SCRIPT_PATH.parents[1]
    installed = SCRIPT_PATH.parents[1]
    if installed.name == ".delivery-guardrails":
        yield installed
    # Installed copy: ~/.codex/skills/.delivery-guardrails/scripts/resolve_runtime.py
    # Already covered by parents[1]. Also accept a sibling runtime from a skill dir.
    for parent in SCRIPT_PATH.parents:
        sibling = parent / ".delivery-guardrails"
        if sibling.is_dir():
            yield sibling


def resolve_runtime():
    seen = set()
    for candidate in candidate_roots():
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        marker = resolved / "scripts" / "validate_schema.py"
        if marker.is_file():
            return resolved
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        metavar="SCRIPT",
        help="Also require this script to exist under the runtime, for example validate_schema.py",
    )
    args = parser.parse_args()

    runtime = resolve_runtime()
    if runtime is None:
        sys.exit(
            "STOP: shared runtime not found. Run this repository, or install with "
            "scripts/install_skills.py so `.delivery-guardrails/scripts/validate_schema.py` exists."
        )
    if args.check:
        required = runtime / "scripts" / args.check
        if not required.is_file():
            sys.exit(f"STOP: missing {required}")
    print(runtime)


if __name__ == "__main__":
    main()
