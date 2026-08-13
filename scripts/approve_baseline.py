#!/usr/bin/env python3
"""Record an explicit human decision on an intake baseline.

Does not invent approval. The caller must pass approve or reject.
"""

import argparse
import datetime
import json
import pathlib
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=pathlib.Path)
    parser.add_argument("--status", required=True, choices=("approved", "rejected"))
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()

    if not args.baseline.is_file():
        sys.exit(f"STOP: no baseline at {args.baseline}")

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    pending = baseline.get("extraction_meta", {}).get("fields_pending_review") or []
    if args.status == "approved" and pending:
        sys.exit(
            "STOP: cannot approve a baseline while fields_pending_review is non-empty: "
            + ", ".join(pending)
        )

    baseline["human_review"] = {
        "status": args.status,
        "reviewed_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "reviewer": args.reviewer,
    }
    args.baseline.write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote human_review.status={args.status} to {args.baseline}")


if __name__ == "__main__":
    main()
