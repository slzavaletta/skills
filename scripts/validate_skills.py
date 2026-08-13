#!/usr/bin/env python3
"""Validate local skill frontmatter and required OpenAI interface metadata."""

import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"


def parse_frontmatter(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, ["frontmatter must start on line 1"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["frontmatter has no closing delimiter"]
    data = {}
    errors = []
    for line in lines[1:end]:
        match = re.fullmatch(r"([a-z_]+):\s*(.+)", line)
        if not match:
            errors.append(f"invalid frontmatter line: {line!r}")
            continue
        data[match.group(1)] = match.group(2).strip()
    return data, errors


def validate_skill(skill_dir):
    errors = []
    skill_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "agents" / "openai.yaml"
    if not skill_path.is_file():
        return ["missing SKILL.md"]
    frontmatter, frontmatter_errors = parse_frontmatter(skill_path)
    errors.extend(frontmatter_errors)
    if set(frontmatter) != {"name", "description"}:
        errors.append("frontmatter must contain only name and description")
    if frontmatter.get("name") != skill_dir.name:
        errors.append("frontmatter name must equal the skill directory name")
    if len(frontmatter.get("description", "")) < 40:
        errors.append("description must explain both capability and trigger context")
    if not metadata_path.is_file():
        errors.append("missing agents/openai.yaml")
    else:
        metadata = metadata_path.read_text(encoding="utf-8")
        for field in ("display_name", "short_description", "default_prompt"):
            if not re.search(rf"^\s{{2}}{field}:\s+\".+\"$", metadata, re.MULTILINE):
                errors.append(f"openai.yaml missing quoted {field}")
        if f"${skill_dir.name}" not in metadata:
            errors.append("default_prompt must mention the skill with $skill-name")
    return errors


def main():
    failed = False
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        errors = validate_skill(skill_dir)
        print(f"{'FAIL' if errors else 'PASS'}  {skill_dir.name}")
        for error in errors:
            print(f"  {error}")
        failed |= bool(errors)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
