#!/usr/bin/env python3
"""Validate a JSON artifact against a JSON Schema Draft 7 contract."""

import argparse
import json
import pathlib
import sys

try:
    from jsonschema import Draft7Validator, FormatChecker
except ImportError:
    sys.exit("Missing dependency 'jsonschema'. Run: python -m pip install -r requirements.txt")


def format_path(parts):
    if not parts:
        return "$"
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=pathlib.Path)
    parser.add_argument("schema", type=pathlib.Path)
    args = parser.parse_args()

    with args.artifact.open(encoding="utf-8") as handle:
        artifact = json.load(handle)
    with args.schema.open(encoding="utf-8") as handle:
        schema = json.load(handle)

    Draft7Validator.check_schema(schema)
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(artifact), key=lambda error: list(error.absolute_path))

    if errors:
        print(f"FAIL  {args.artifact} against {args.schema}")
        for error in errors:
            print(f"  {format_path(error.absolute_path)}: {error.message}")
        sys.exit(1)

    print(f"PASS  {args.artifact} against {args.schema}")


if __name__ == "__main__":
    main()
