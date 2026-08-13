#!/usr/bin/env python3
"""Append an approved or rejected scope decision to scope-changelog.jsonl.

Accept a JSON file payload. Do not log discuss or pending decisions.
"""

import argparse
import datetime
import json
import pathlib
import sys

REQUIRED_FIELDS = ["request_source", "classification", "decision", "approver"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=pathlib.Path)
    payload = parser.add_mutually_exclusive_group(required=True)
    payload.add_argument("--json-file", type=pathlib.Path, help="Path to a JSON event payload")
    payload.add_argument("--json", help="Event payload as a JSON string. Prefer --json-file on Windows.")
    args = parser.parse_args()

    if args.json_file:
        try:
            event = json.loads(args.json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"Invalid JSON payload: {exc}")
    else:
        try:
            event = json.loads(args.json)
        except json.JSONDecodeError as exc:
            sys.exit(f"Invalid JSON payload: {exc}")

    missing = [field for field in REQUIRED_FIELDS if field not in event]
    if missing:
        sys.exit(f"Missing required fields: {missing}")

    if event["decision"] not in ("approved", "rejected"):
        sys.exit("decision must be 'approved' or 'rejected' — pending items are not logged")

    project_dir = args.project_dir
    event["project_id"] = project_dir.name
    event["ts"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    changelog = project_dir / "scope-changelog.jsonl"
    with changelog.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f"Logged to {changelog}")


if __name__ == "__main__":
    main()
