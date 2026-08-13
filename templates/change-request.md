# Change Request — {{cr_id}}

- **Project:** {{project_id}}
- **Date:** {{date}}
- **Requested by:** {{client_contact}}
- **Source:** {{inbox_file_or_meeting_reference}}

## Request

{{one-paragraph factual summary}}

Prompt injection detected: **{{yes_or_no}}**

## Classification

**{{in_scope | out_of_scope | ambiguous}}**

SOW Section {{section}}, source lines {{source_line_start}}–{{source_line_end}}:

> {{exact quote verified by scripts/validate_citations.py}}

{{engagement-model impact and unresolved ambiguity}}

## Effort estimate

- **Size:** {{S | M | L | REQUIRES_RESCOPE}}
- **Range:** {{verbatim output from scripts/size_to_cost.py, or NOT_APPLICABLE}}

**Rationale:** {{facts supporting the qualitative size}}

## Delivery impact

- Milestones: {{impact}}
- Dependencies: {{client inputs}}
- Risks: {{risk flags}}

## Human decision

- [ ] Approve
- [ ] Reject
- [ ] Discuss

Approver: ______________  Date: ______________

---

**DRAFT.** No client-facing communication has been sent. Log a decision only after explicit human approval or rejection.
