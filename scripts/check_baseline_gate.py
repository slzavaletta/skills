#!/usr/bin/env python3
"""Refuse scope classification unless the baseline is approved and complete enough."""

import argparse
import json
import pathlib
import sys


def unwrap(value):
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=pathlib.Path)
    args = parser.parse_args()

    if not args.baseline.is_file():
        sys.exit(f"STOP: no baseline at {args.baseline}. Run sow-intake first.")

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    review = baseline.get("human_review") or {}
    status = review.get("status")
    pending = baseline.get("extraction_meta", {}).get("fields_pending_review") or []
    engagement = unwrap(baseline.get("engagement_type", "NOT_FOUND"))

    blockers = []
    if status != "approved":
        blockers.append(
            f"baseline human_review.status is {status!r}; a human must approve intake before classification"
        )
    if pending:
        blockers.append(f"fields still pending review: {', '.join(pending)}")
    if engagement not in {"fixed_price", "time_and_materials", "staff_augmentation"}:
        blockers.append(f"engagement_type is {engagement!r}")

    if blockers:
        print("STOP: scope-sentinel cannot classify this project yet.")
        for blocker in blockers:
            print(f"  - {blocker}")
        sys.exit(1)

    reviewer = review.get("reviewer") or "unknown reviewer"
    reviewed_at = review.get("reviewed_at") or "unknown time"
    print(f"PASS  baseline approved by {reviewer} at {reviewed_at}")


if __name__ == "__main__":
    main()
