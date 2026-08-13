# Delivery Guardrails for Agentic AI

Two portable AI skills for delivery management. They turn a Statement of Work (SOW) into a cited project baseline, then classify incoming requests against that baseline without letting the model invent evidence or commercial estimates.

The repository demonstrates a practical division of responsibility:

- The AI extracts, classifies, explains, and drafts.
- Deterministic scripts validate structure, evidence, and arithmetic.
- A human approves every consequential result.

## Skills

### `sow-intake`

Creates two project artifacts:

- `baseline.json`: structured project memory validated against a JSON Schema.
- `delivery-brief.md`: a readable summary for kickoff and delivery governance.

Every source-derived value contains an exact quote, section identifier, and source line range. Missing facts remain `NOT_FOUND`. Contradictions remain visible.

### `scope-sentinel`

Classifies a client request as `in_scope`, `out_of_scope`, or `ambiguous`. It changes its reasoning for fixed-price, time-and-materials, and staff-augmentation engagements.

The skill creates a structured decision before it drafts a change request. A script converts only approved qualitative sizes into hours and cost ranges.

## Safety model

| Risk | Control |
|---|---|
| Invented SOW claim | Exact quote, line-range, and nearby-section validation |
| Missing citations | JSON Schema requires cited wrappers for source-derived values |
| Conflicting numbers | Preserve every cited value and raise a risk flag |
| Model-generated arithmetic | Run deterministic commercial and sizing scripts |
| Prompt injection in a SOW or request | Treat all source content as untrusted data |
| Premature client commitment | Require explicit human approval |
| Accidental client-data commit | Ignore `projects/`; track only synthetic `examples/` |

## Pipeline

```text
SOW (.md/.txt/.pdf)
  -> canonical UTF-8 source
  -> AI extraction
  -> baseline schema gate
  -> exact citation gate
  -> deterministic commercial check
  -> human-reviewed delivery brief

Client request
  -> prompt-injection check
  -> engagement-aware classification
  -> scope-decision schema gate
  -> exact citation gate
  -> deterministic size-to-cost conversion
  -> human approval
```

## Quick start

Requires Python 3.10 or later.

```bash
git clone git@github.com:slopez-z/skills.git
cd skills
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\verify.py
```

On macOS or Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify.py
```

`verify.py` validates both skills, every JSON artifact, both schemas, all citations, both commercial models, the eval harness, installer behavior, and unit tests.

## Synthetic demo projects

The repository contains no client data. Two fictional projects under `examples/projects/` make the demo reproducible:

- `acme-support-automation`: fixed-price intake plus an out-of-scope request containing prompt injection.
- `northstar-analytics`: time-and-materials intake with conflicting monthly caps and a new-data-source request.

Run the individual surfaces:

```bash
python eval/run_eval.py
python scripts/portfolio_status.py
python scripts/compute_revenue.py examples/projects/acme-support-automation
python scripts/compute_revenue.py examples/projects/northstar-analytics
```

The included classification predictions exercise the evaluator. They are labeled examples, not claimed live model results. Replace `eval/predictions/classifications.example.json` with fresh outputs to evaluate another model or prompt revision.

## Installation

Install both skills and their shared runtime into a skills directory:

```bash
python scripts/install_skills.py ~/.codex/skills
```

Use `--force` only when you intend to replace an earlier installation. The installer places both skills at the target root and preserves shared scripts, schemas, templates, and configuration under `.delivery-guardrails/`.

Each skill also includes `agents/openai.yaml` metadata for Codex-compatible discovery. The `SKILL.md` instructions remain tool-neutral enough to use from other agent environments that support repository skills.

## PDF input

`prepare_sow.py` accepts Markdown, UTF-8 text, and PDFs with extractable text. PDF extraction uses `pypdf` and writes a canonical `.extracted.txt` source for stable line citations.

Image-only PDFs require OCR before intake. The workflow stops instead of pretending an empty extraction is valid.

## Repository structure

```text
skills/                  Skill instructions and OpenAI interface metadata
scripts/                 Deterministic gates, calculations, installer, and verification
schemas/                 Baseline and scope-decision JSON Schemas
templates/               Delivery Brief and Change Request templates
config/                  Synthetic sizing policy and rate card
examples/projects/       Fictional end-to-end fixtures
eval/                    Gold labels, classification cases, and example predictions
tests/                   Negative and portability tests
```

## Design limits

- Citation validation proves that quoted text exists at the declared location. It does not prove that the model interpreted the clause correctly.
- PDF text order depends on the source file. Complex layouts may require manual review or OCR.
- The repository includes an evaluation harness, not a hosted model runner. Model invocation remains environment-specific.
- The default rate card is synthetic. Real rates belong only in ignored project folders.

These controls make AI output inspectable and fail-closed. They do not replace delivery judgment, legal review, or client approval.
