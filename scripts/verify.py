#!/usr/bin/env python3
"""Run the complete deterministic verification suite from a clean clone."""

import ast
import json
import os
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(label, *arguments):
    print(f"\n--- {label} ---", flush=True)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(arguments, cwd=REPO_ROOT, env=environment, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)


def static_checks():
    print("\n--- static files ---")
    python_files = sorted(
        path for path in REPO_ROOT.rglob("*.py")
        if not {".git", ".venv", "__pycache__"}.intersection(path.parts)
    )
    for path in python_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    json_files = sorted(
        path for path in REPO_ROOT.rglob("*.json")
        if not {".git", ".venv", "__pycache__"}.intersection(path.parts)
    )
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))
    print(f"PASS  parsed {len(python_files)} Python files and {len(json_files)} JSON files")


def main():
    static_checks()
    run("skill metadata", PYTHON, "scripts/validate_skills.py")

    projects = REPO_ROOT / "examples" / "projects"
    for project in ("acme-support-automation", "northstar-analytics"):
        project_dir = projects / project
        run(
            f"baseline schema: {project}",
            PYTHON,
            "scripts/validate_schema.py",
            str(project_dir / "baseline.json"),
            "schemas/baseline.schema.json",
        )
        run(
            f"baseline citations: {project}",
            PYTHON,
            "scripts/validate_citations.py",
            str(project_dir / "baseline.json"),
            str(project_dir / "sow.md"),
        )
        run(
            f"scope decision schema: {project}",
            PYTHON,
            "scripts/validate_schema.py",
            str(project_dir / "scope-decision.json"),
            "schemas/scope-decision.schema.json",
        )
        run(
            f"scope decision citation: {project}",
            PYTHON,
            "scripts/validate_citations.py",
            str(project_dir / "scope-decision.json"),
            str(project_dir / "sow.md"),
        )
        run(f"commercial calculation: {project}", PYTHON, "scripts/compute_revenue.py", str(project_dir))

    run("evaluation harness", PYTHON, "eval/run_eval.py")
    run("portfolio view", PYTHON, "scripts/portfolio_status.py")
    run("unit tests", PYTHON, "-m", "unittest", "discover", "-s", "tests", "-v")
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
