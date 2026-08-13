#!/usr/bin/env python3
"""Verify exact quotes, source locations, and section markers in a JSON artifact."""

import argparse
import json
import pathlib
import re
import sys

MIN_QUOTE_LENGTH = 20
MAX_CITATION_SPAN_LINES = 20


def find_citations(node, path="$"):
    """Collect (JSON path, citation) pairs recursively."""
    found = []
    if isinstance(node, dict):
        if {"section", "quote", "source_line_start", "source_line_end"} <= node.keys():
            found.append((path, node))
            return found
        for key, value in node.items():
            found.extend(find_citations(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(find_citations(value, f"{path}[{index}]"))
    return found


def validate_citation(citation, source_lines):
    quote = citation.get("quote", "")
    section = str(citation.get("section", "")).strip()
    start = citation.get("source_line_start")
    end = citation.get("source_line_end")
    errors = []

    if len(quote.strip()) < MIN_QUOTE_LENGTH:
        errors.append(f"quote is shorter than {MIN_QUOTE_LENGTH} characters")
    if not isinstance(start, int) or not isinstance(end, int):
        errors.append("source line range must contain integers")
        return errors
    if start < 1 or end < start or end > len(source_lines):
        errors.append(f"invalid source line range {start}-{end}; source has {len(source_lines)} lines")
        return errors
    if end - start + 1 > MAX_CITATION_SPAN_LINES:
        errors.append(f"source line range exceeds {MAX_CITATION_SPAN_LINES} lines")

    cited_text = "\n".join(source_lines[start - 1:end])
    if quote not in cited_text:
        errors.append("quote is not an exact match inside the declared source lines")

    section_pattern = re.compile(
        rf"(?<![A-Za-z0-9]){re.escape(section)}(?![A-Za-z0-9])",
        re.IGNORECASE,
    )
    nearby_lines = source_lines[max(0, start - 10):end]
    heading_lines = [
        line
        for line in nearby_lines
        if re.match(r"^\s*(?:#{1,6}\s+|(?:section|clause)\s+|\d+(?:\.\d+)*[.):]?\s+)", line, re.IGNORECASE)
    ]
    if not section or not any(section_pattern.search(line) for line in heading_lines):
        errors.append("section marker is not present in a nearby source heading")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=pathlib.Path, help="JSON containing citation objects")
    parser.add_argument("source", type=pathlib.Path, help="Canonical UTF-8 Markdown or text source")
    parser.add_argument(
        "--allow-none",
        action="store_true",
        help="Allow an artifact with no citations. Use only for an ambiguous decision with NOT_FOUND evidence.",
    )
    args = parser.parse_args()

    with args.artifact.open(encoding="utf-8") as handle:
        artifact = json.load(handle)
    with args.source.open(encoding="utf-8") as handle:
        source_lines = handle.read().splitlines()

    citations = find_citations(artifact)
    if not citations:
        if args.allow_none:
            print("PASS  no citation objects present; caller explicitly allowed none")
            return
        sys.exit("FAIL  no citation objects found")

    failures = []
    for path, citation in citations:
        errors = validate_citation(citation, source_lines)
        print(f"{'FAIL' if errors else 'PASS'}  {path}")
        failures.extend((path, error) for error in errors)

    print(f"\n{len(citations) - len({path for path, _ in failures})}/{len(citations)} citations verified exactly.")
    if failures:
        print("\nCitation failures:")
        for path, error in failures:
            print(f"  {path}: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
