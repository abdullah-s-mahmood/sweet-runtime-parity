# AT0-EN V2.4 — Higher-Model Pre-Inference Review

Date: 2026-10-03
Decision: **ACCEPT PRE-INFERENCE IDENTITY PACKAGE / AUTHORIZE LOAD-ONLY COMPATIBILITY + CALIBRATION FREEZE / SEMANTIC SCORING STILL BLOCKED**

## Evidence accepted

Source-free contract preflight:
- 17/17 PASS
- no model inference

Hash-only workflow:
- run: 37133900590
- trigger commit: d1db30b5d30560f96b80c1ac5844acea981a98bb
- conclusion: SUCCESS
- artifact: 11277806000
- artifact digest: sha256:789388dfd4305933741895162e708bf9cc6501a2756297eae64a9216cf1381a1
- 16 files hashed
- semantic inference: false
- model import: false
- forward pass: false
- threshold calibration: false
- generator inference: false
- additional monetary cost: USD 0

Hash lock:
phase2/academic_transform/at0_en/v2_4/SEMANTIC_MODEL_FILE_HASH_LOCK_V1.json

## Frozen witnesses

### HHEM-2.1-Open
- repo: vectara/hallucination_evaluation_model
- revision: c9ccea35f0e37e02422eb49b798e09ed82be5a20
- license: Apache-2.0
- model SHA-256: 634de18a38cf1e991c1acd0f7a9e0d30f7ea187fba42bb4798f862d3edd31e72
- custom code is pinned and hashed
- transitive runtime config/tokenizer dependency google/flan-t5-base is pinned at 7bcac572ce56db69c1ea7c8af255c5d7c9672fc2 and hashed
- role: support/factual-consistency witness, not contradiction oracle
- pair order is semantically significant

### DeBERTa NLI
- repo: MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli
- revision: 6f5cf0a2b59cabb106aca4c287eed12e357e90eb
- license: MIT
- model SHA-256: 06d6fd89edd4f97816831626daafbdb0b029cf63bae8edc0bccab1d64e2e7707
- label mapping: 0 entailment, 1 neutral, 2 contradiction
- role: independent NLI witness, not scientific oracle

## Review findings

1. V2.3 demonstrated that deterministic rules are valuable for hard invariants but fail semantic paraphrase coverage.
2. HHEM and DeBERTa are architecturally/task-wise distinct enough to serve as heterogeneous semantic witnesses, but neither has project-specific scientific-revision validation yet.
3. HHEM's custom remote code and FLAN tokenizer/config are part of the executable identity and must remain local/hash-verified before loading.
4. Paragraph-level factuality alone is insufficient. V2.4 must preserve the preregistered claim-by-claim bidirectional design.
5. No semantic threshold may be selected using future confirmation evidence.
6. The existing consumed V2.2/V2.3 safe/adversarial examples may be used as DEVELOPMENT calibration material after label audit. They are not confirmation.
7. V2.1 generated outputs may be diagnostic only unless a specific claim-level label is independently adjudicated.

## Authorization from this review

Authorized next, strictly sequential:
1. freeze a clean DEVELOPMENT semantic-calibration population from already-consumed evidence;
2. freeze source assertions and calibration labels before any score is observed;
3. build a local-only model loader that verifies hashes before import and forbids network after acquisition;
4. run a **load-only compatibility smoke** for both models: instantiate tokenizer/model, confirm class/label/config identity and memory viability, but do not score any semantic text pair;
5. return the load-only evidence and calibration manifest for final pre-scoring review.

Still NOT authorized:
- HHEM or NLI scoring on calibration/holdout text
- threshold tuning
- confirmation opening
- new generator inference
- HW1-EN
- detector robustness
- Arabic restart or reserved Arabic access

## Calibration population rule

Use only already-consumed constructed examples with labels auditable from source text:
- safe paraphrases from the V2.2/V2.3 development/red-team materials after excluding defective labels;
- adversarial variants from the consumed V2.2 independent red-team and V2.3 unseen holdout.

Do not include an example merely to increase N. Record exclusions and reasons. The source text is authoritative over legacy content_units.

## Next return gate

Return after:
- calibration population/hash frozen;
- load-only compatibility smoke PASS or hard blocker;
- no semantic pair has been scored.
