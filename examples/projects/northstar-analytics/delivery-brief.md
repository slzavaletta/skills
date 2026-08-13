# Delivery Brief — Analytics Enablement

> Generated from `sow.md` on 2026-08-13. Every source-derived fact has a verified quote and line range. Human review remains required.

## Snapshot

| Field | Value | Source |
|---|---|---|
| Client | Northstar Retail | Section 1, lines 4-4 |
| Engagement model | time_and_materials | Section 2, lines 9-9 |
| Contract value | Indicative only - see commercial summary | `scripts/compute_revenue.py` |
| Start date | 2026-10-01 | Section 3, lines 16-16 |
| End date | NOT_FOUND | Human review required |
| Language | English | Section 1, lines 6-6 |

## Commercial summary

```
Project: northstar-analytics
Engagement type: time_and_materials
Rate card: config/rate-card.json

Hourly rates (as stated in SOW):
  integration_engineer: USD 110/h
Monthly run-rate at 120 h cap (blended USD 105/h): USD 12,600
Monthly run-rate at 160 h cap (blended USD 105/h): USD 16,800
Indicative engagement value over 8-12 weeks: USD 23,279 - USD 46,559

FLAGS (copy into the brief's risk section - human resolution required):
  - SOW states CONFLICTING monthly hour caps: [120, 160] - human resolution required before any commitment; scenarios below are illustrative only
```

## Scope

1. S1. Build dashboard variants using the existing warehouse tables. (Section 4, lines 19-19)
2. S2. Configure scheduled email delivery for approved dashboards. (Section 4, lines 20-20)

## Deliverables

| ID | Deliverable | Source |
|---|---|---|
| D1 | Configured dashboard variants using existing data. | Section 5, lines 23-23 |

## Milestones

| ID | Name | Date | Source |
|---|---|---|---|
| M1 | Discovery begins | 2026-10-01 | Section 6, lines 26-26 |

## Assumptions

- A1. The client maintains the existing warehouse tables and grants read access. (Section 7, lines 29-29)

## Exclusions

- E1. New external data sources and new ingestion pipelines are excluded. (Section 8, lines 32-32)

## Service levels

- SLA1. Delivery questions receive an initial response within two business days. (Section 10, lines 38-38)

## Risk flags

| Type | Severity | Description | Source |
|---|---|---|---|
| missing_end_date | high | The SOW does not define a contractual completion date. | NOT_FOUND |
| hours_cap_contradiction | high | The SOW states monthly caps of 120 and 160 hours. | Section 9, lines 35-35 |
| client_controlled_prioritization | medium | Completion depends on client prioritization. | Section 3, lines 16-16 |

## Human review required

- `dates.end_date` is `NOT_FOUND`. This blocks kickoff sign-off.

## Kickoff checklist

- [ ] Confirm client obligation A1: warehouse tables remain available with read access.
- [ ] Schedule milestone M1: discovery begins on 2026-10-01.
- [ ] Resolve `NOT_FOUND` field `dates.end_date` with the account executive.
- [ ] Resolve conflicting monthly caps of 120 and 160 hours before any commitment.
