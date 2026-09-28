# Phase 2 Arabic Evaluation Handoff

This branch receives the text-only inputs and runner from the partial Work package for **Phase 2 — Real Arabic Correction Evaluation**.

## Established constraints

- Do not start Phase 3.
- Do not rerun model-acquisition or runtime-parity work.
- Use only the official runtime already proven on `main`.
- NoPnx SHA-256:
  `584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6`
- Pnx SHA-256:
  `195696eaf09a5b92d8141f473e0e3a0d5a710649114b3180afb25cf76cdaa4f3`
- CAMeL-Lab/text-editing pinned commit:
  `4d552ca3ae98029550f27fc52aa1b22883e16e61`
- Python 3.10 + PyTorch 1.12.1 CPU + Transformers 4.30.0 is the proven reference environment.

## Required upload from the partial package

Copy the package's **text/code files only** into this branch. Do not upload model weights.

At minimum preserve:
- the 150-case development dataset exactly as generated;
- case IDs and the exclusion record for the 59 previously sealed IDs;
- source/provenance/license ledger;
- the 12 project-authored scientific stress cases, clearly marked non-human-gold;
- the official-development runner;
- any config/schema files the runner requires;
- the start/end research and brainstorming notes already produced.

Do not regenerate or silently alter the selected 150 cases.

## Output contract for GitHub Actions

The official runner must produce at least:

- `artifacts/OFFICIAL_DEVELOPMENT_RAW.jsonl`
- `artifacts/OFFICIAL_DEVELOPMENT_RUN_LOG.txt`
- `artifacts/OFFICIAL_DEVELOPMENT_MANIFEST.json`

For every development case, retain:
- case_id
- source
- reference
- provenance/category metadata
- NoPnx iteration 1 output
- NoPnx iteration 2 output
- Pnx output
- final SWEET output
- raw edit labels for each stage where available
- runtime/model/hash provenance

The run must verify both pinned model SHA-256 values before scoring.

## Important evaluation semantics

Nahw references in this development slice are **single-location human corrections**, not fully corrected paragraphs. Therefore:
- do not score sentence/paragraph exact-match as if the entire passage were gold;
- score whether the targeted published correction was recovered;
- separately record collateral edits outside the targeted location;
- treat collateral edits as candidates for precision/safety adjudication, not automatically as errors.

The 12 project-authored scientific cases are stress tests, not human-gold benchmark items.

## After official inference

Do not freeze or run a sealed set automatically.

First perform:
1. targeted-correction recovery analysis;
2. collateral-edit analysis;
3. NoPnx/Pnx ablation;
4. scientific invariant checks;
5. review-burden analysis with the existing frozen safety stack;
6. failure taxonomy;
7. mid-phase research + brainstorming.

Then decide whether bounded development changes are justified.
