#!/usr/bin/env python3
"""Evaluate baseline artifacts and scope classifications against synthetic gold labels."""

import argparse
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_BASELINE_GOLD = REPO_ROOT / "eval" / "gold" / "baselines"
DEFAULT_CASES = REPO_ROOT / "eval" / "cases" / "classifications.json"
DEFAULT_PREDICTIONS = REPO_ROOT / "eval" / "predictions" / "classifications.example.json"
DEFAULT_PROJECTS = REPO_ROOT / "examples" / "projects"


def unwrap(value):
    return value.get("value") if isinstance(value, dict) and "value" in value else value


def get_path(data, dotted):
    node = data
    for key in dotted.split("."):
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def compare(label, expected, actual):
    ok = expected == actual
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: expected {expected!r}, got {actual!r}")
    return int(ok), 1


def evaluate_baselines(gold_dir, projects_dir):
    passed = total = 0
    gold_files = sorted(gold_dir.glob("*.json"))
    if not gold_files:
        raise SystemExit(f"No baseline gold files found in {gold_dir}")

    for gold_path in gold_files:
        gold = json.loads(gold_path.read_text(encoding="utf-8"))
        project_id = gold["project_id"]
        baseline_path = projects_dir / project_id / "baseline.json"
        print(f"\n=== Baseline: {project_id} ===")
        if not baseline_path.is_file():
            print(f"  FAIL  missing baseline: {baseline_path}")
            total += 1
            continue
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))

        for field, expected in gold.get("scalar_fields", {}).items():
            result = compare(field, expected, unwrap(get_path(baseline, field)))
            passed += result[0]
            total += result[1]
        for field, expected in gold.get("counts", {}).items():
            value = get_path(baseline, field)
            result = compare(f"count {field}", expected, len(value) if isinstance(value, list) else None)
            passed += result[0]
            total += result[1]

        actual_not_found = set(get_path(baseline, "extraction_meta.fields_not_found") or [])
        for field in gold.get("expected_not_found", []):
            result = compare(f"NOT_FOUND {field}", True, field in actual_not_found)
            passed += result[0]
            total += result[1]

        actual_flags = {flag.get("type") for flag in baseline.get("risk_flags", [])}
        for flag in gold.get("expected_risk_flags", []):
            result = compare(f"risk flag {flag}", True, flag in actual_flags)
            passed += result[0]
            total += result[1]

        if "expected_cap_values" in gold:
            caps = get_path(baseline, "commercials.monthly_hours_cap") or []
            actual_caps = sorted(unwrap(cap) for cap in caps)
            result = compare("all conflicting cap values", sorted(gold["expected_cap_values"]), actual_caps)
            passed += result[0]
            total += result[1]
    return passed, total


def evaluate_classifications(cases_path, predictions_path):
    cases = json.loads(cases_path.read_text(encoding="utf-8"))["cases"]
    predictions = json.loads(predictions_path.read_text(encoding="utf-8"))["predictions"]
    by_id = {prediction["case_id"]: prediction for prediction in predictions}
    passed = total = 0

    for case in cases:
        case_id = case["case_id"]
        print(f"\n=== Classification: {case_id} ===")
        prediction = by_id.get(case_id)
        if prediction is None:
            print("  FAIL  prediction missing")
            total += 1
            continue
        for field, expected in case["expected"].items():
            actual = prediction.get(field)
            if field == "risk_flags":
                expected = sorted(expected)
                actual = sorted(actual or [])
            result = compare(field, expected, actual)
            passed += result[0]
            total += result[1]

    unexpected = sorted(set(by_id) - {case["case_id"] for case in cases})
    if unexpected:
        print(f"\nFAIL  unexpected prediction IDs: {unexpected}")
        total += 1
    return passed, total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projects-dir", type=pathlib.Path, default=DEFAULT_PROJECTS)
    parser.add_argument("--baseline-gold", type=pathlib.Path, default=DEFAULT_BASELINE_GOLD)
    parser.add_argument("--cases", type=pathlib.Path, default=DEFAULT_CASES)
    parser.add_argument("--predictions", type=pathlib.Path, default=DEFAULT_PREDICTIONS)
    args = parser.parse_args()

    baseline_passed, baseline_total = evaluate_baselines(args.baseline_gold, args.projects_dir)
    class_passed, class_total = evaluate_classifications(args.cases, args.predictions)
    passed = baseline_passed + class_passed
    total = baseline_total + class_total
    percentage = 100 * passed / total if total else 0
    print(f"\n=== OVERALL: {passed}/{total} ({percentage:.0f}%) ===")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
