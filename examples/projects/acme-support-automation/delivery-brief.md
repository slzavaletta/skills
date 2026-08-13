# Delivery Brief — Support Automation

> Generated from `sow.md` on 2026-08-13. Every source-derived fact has a verified quote and line range. Human review remains required.

## Snapshot

| Field | Value | Source |
|---|---|---|
| Client | Acme Services | Section 1, lines 4-4 |
| Engagement model | fixed_price | Section 2, lines 9-9 |
| Contract value | USD 48,000 | `scripts/compute_revenue.py` |
| Start date | 2026-09-01 | Section 3, lines 13-13 |
| End date | 2026-11-30 | Section 3, lines 13-13 |
| Language | English | Section 1, lines 6-6 |

## Commercial summary

```
Project: acme-support-automation
Engagement type: fixed_price
Rate card: config/rate-card.json

Total fixed price: USD 48,000
Payment schedule:
  50% on kickoff: USD 24,000
  50% on production launch: USD 24,000
Schedule check: OK - milestones sum to USD 48,000

No commercial discrepancies detected.
```

## Scope

1. S1. Configure an English-language support assistant for the existing web channel. (Section 4, lines 16-16)
2. S2. Integrate the assistant with the client's existing Zendesk instance. (Section 4, lines 17-17)

## Deliverables

| ID | Deliverable | Source |
|---|---|---|
| D1 | One configured support assistant for the existing web channel. | Section 5, lines 20-20 |
| D2 | One production integration with the existing Zendesk instance. | Section 5, lines 21-21 |

## Milestones

| ID | Name | Date | Source |
|---|---|---|---|
| M1 | Discovery and content inventory complete | 2026-09-15 | Section 6, lines 24-24 |
| M2 | Production launch complete | 2026-11-30 | Section 6, lines 25-25 |

## Assumptions

- A1. The client provides approved support content by 2026-09-08. (Section 7, lines 28-28)
- A2. The client provides Zendesk sandbox access before integration starts. (Section 7, lines 29-29)

## Exclusions

- E1. Voice, WhatsApp, and social messaging channels are excluded. (Section 8, lines 32-32)

## Service levels

- SLA1. Critical production incidents receive an initial response within four business hours. (Section 10, lines 38-38)

## Risk flags

No structural risks detected.

## Human review required

No fields were marked `NOT_FOUND` or pending review.

## Kickoff checklist

- [ ] Confirm client obligation A1: approved support content by 2026-09-08.
- [ ] Confirm client obligation A2: Zendesk sandbox access before integration starts.
- [ ] Schedule milestone M1: discovery and content inventory complete on 2026-09-15.
- [ ] Schedule milestone M2: production launch complete on 2026-11-30.
