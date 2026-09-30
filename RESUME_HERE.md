# RESUME HERE — ACAD_PASS / Phase 2 Arabic / M2-H

## 0. Resume maintenance policy

This file is the canonical live handoff. Update it after every meaningful checkpoint: successful workflow, scientifically relevant failure, architecture/gate decision, frozen hash/manifest, or change in the exact next authorized step. Do not update it for trivial status polls that add no new state.


**Canonical handoff state date:** 2026-09-30  
**Repository:** `abdullah-s-mahmood/sweet-runtime-parity`  
**Branch:** `phase2-arabic-eval`  
**State before this handoff commit:** `90eb4e3dd0b36106493376efc7221422aa91a067`

> **Instruction to any new ChatGPT conversation:** Read this file first. Treat it as the current canonical handoff. Older handoff files are historical context only. Do not restart closed work. Inspect the branch HEAD and the exact runs/commits listed here before changing anything.

---

## 1. Permanent execution rule

Use **checkpoint execution**.

A single user "اكمل" may perform 2–4 tool operations, but they must be **strictly sequential**. Do not run tools in parallel. If a workflow is still running, inspect once and stop. If a step fails, identify the exact cause before changing architecture.

Arabic responses should be RTL-friendly. Keep English technical terms isolated in backticks such as `CALIBRATION`, `H3`, `ARETA`.

---

## 2. Permanent research rule

At the START and END of every substantive phase/iteration:
- perform fresh rigorous research;
- perform maximum-effort brainstorming;
- challenge current assumptions and alternatives;
- report **IMPROVED / WORSENED / MIXED** versus the previous comparable state;
- report magnitude only with comparable metrics;
- report grounded forecast and blockers.

Do not suppress negative evidence or weaken gates post hoc.

---

## 3. Product identity

ACAD_PASS is a bilingual **Academic Document Intelligence & Transformation Platform**.

Architecture:

`UNDERSTAND → PROTECT → TRANSFORM/PROOFREAD → INDEPENDENTLY VERIFY → DETECT RISK → REPAIR → RE-VERIFY → ESCALATE/REVIEW → PRESERVE DOCUMENT → DELIVER`

Arabic GEC is one bounded subsystem. Scientific/semantic fidelity, facts/numbers/units/citations, mixed language, DOCX/OOXML/OMML preservation remain first-class.

---

## 4. Independent audit that triggered redesign

The earlier claim `88.73% → 96.55%` was invalid as a causal improvement claim because populations differed.

Correct same-population GED comparison:
- 34/36 = 94.44%
- 28/29 = 96.55%
- +2.1073 percentage points precision
- supported retention 28/34 = 82.35%

Audit conclusion:
- **YES — STRONG REDESIGN OPPORTUNITY**
- current construct validity was partly wrong;
- correct edit ≠ complete repair ≠ safe scientific transformation;
- Arabic remains **REVIEW-first**.

Atomic unit is now a **reversible, evidence-bearing edit transaction on a structured document**.

---

## 5. M1 — CLOSED

M1 established the edit contract and label schema.

Core axes:
- necessity
- local correctness
- contextual correctness
- edit-group completeness
- residual-error relation
- semantic fidelity
- scientific fidelity
- protected invariants
- surface/document integrity
- ambiguity/author intent
- severity

24-case pilot:
- 8 SUPPORTED_CORRECTION
- 5 SUPPORTED_ALTERNATIVE
- 7 WRONG_CORRECTION
- 2 PARTIAL_CORRECTION
- 2 UNNECESSARY_EDIT

M1-A expert-evidence pool is complete and data-ready.

Key M1-A counts:
- QALB14 TRAIN source/corrected: 19,411
- QALB14 DEV source/corrected: 1,017
- reconstructable TRAIN: 18,884
- reconstructable DEV: 1,003
- total failures: 493
- safe persisted calibration sample: 3,829 hashed cases
- A7'ta parseable: 463
- A7'ta bootstrap: 375
- **A7'ta reserve: 88 — keep closed**

M1-A classification:
**IMPROVED / DATA_READY**

---

## 6. M2 monolithic frontier verifier — CLOSED FAIL

P0:
- unsafe acceptance rate: 4.17%
- safe acceptance coverage: 22.22%
- review burden: 37.5%

P1:
- unsafe acceptance rate: 18.75%
- safe acceptance coverage: 56.94%
- review burden: 20.83%

P1 improved coverage but violated unsafe acceptance.

No P2. A7'ta reserve remained unopened. M3 was not authorized.

Conclusion:
monolithic verifier path closed.

---

## 7. M2-R residual span hunter — CLOSED

ArabiGEE was rejected as a sentence-completeness gold because annotations are selective, not exhaustive.

M2-R v2 switched to QALB complete-gold.

P0:
- CRR 82.22%
- GELR 29.14%
- CFPR 60%
- strict residual recall 63.33%
- claim precision 63.47%

P1:
- CRR 86.67%
- GELR 48.88%
- CFPR 33.33%
- strict residual recall 76.67%
- claim precision 65.50%

Comparable P1 vs P0:
- CRR +4.44 pp
- GELR +19.74 pp
- CFPR improved by 26.67 pp
- strict recall +13.33 pp
- claim precision +2.03 pp

Final classification:
**IMPROVED SCIENTIFICALLY / PARTIALLY SUPPORTED TECHNICALLY / FAIL AS STANDALONE SAFETY VERIFIER**

No P2. Confirmation/Holdout/A7'ta reserve remained closed. M3 not authorized.

M2-R final closure commit:
`54129a5111d8d58a49e5e5f85a7a3c48bfd11251`

---

## 8. M2-H — CURRENT ACTIVE STAGE

Goal:
build a **heterogeneous specialized/hybrid verifier**, not another generic LLM gate.

Architecture:
1. structured edit candidate generator
2. high-precision deterministic orthographic validator
3. morphology-aware validator
4. structural word-boundary Split/Merge validator
5. contextual/semantic ambiguity handling
6. calibrated risk fusion
7. independent sentence-completeness decision
8. REVIEW escalation

Dispositions:
- SUPPORTED_MANDATORY
- SUPPORTED_OPTIONAL_OR_ALTERNATIVE
- UNCERTAIN
- REJECTED
- REVIEW

Preregistered overall success requires:
1. unsafe-clean <= 5%
2. CFPR <= 10%
3. CRR >= 90%
4. strict recall >= 90%
5. mandatory precision >= 90%
6. edit localization >= 70%
7. zero protected-invariant failure
8. hybrid beats M2-R P1 by >=10 pp CFPR and >=10 pp GELR on comparable definitions

Do not weaken these gates after seeing internal evaluation.

---

## 9. M2-H component choices

### H1
Official CAMeL-Lab text-editing:
`CAMeL-Lab/text-editing-qalb14-nopnx`

Published reproduction environment:
- Python 3.10
- PyTorch 1.12.1
- Transformers 4.30.0

### H2
Deterministic high-precision orthographic rules plus morphology/lexicon evidence.

### H3
CAMeL morphology / CALIMA MSA evidence.

### H4
Local deterministic high-precision word-boundary validator.

H4 must not approve based only on a hand-written rule; it requires structural legality plus at least two independent non-H1 evidence families and no contradiction.

---

## 10. M2-H environment architecture — FROZEN

Initial single-environment preflight failed because current CAMeL Tools requires dependencies incompatible with H1's Python 3.10 stack.

Decision:
**dual-environment isolation**

H1 environment:
- Python 3.10
- PyTorch 1.12.1
- Transformers 4.30.0

H3/H4 environment:
- Python 3.11+
- current frozen CAMeL Tools

Components communicate only via serialized JSON/JSONL artifacts.

Environment decision commit:
`1f6c36d104d5d8e3d0a9746bbca2c7ec07783c97`

Preflight v2 run:
`36653526757`

Result:
**SUCCESS**

Reproducibility lock commit:
`228d37d8ff525a9c597a716dbc44a1a4b063f2a7`

Frozen H1:
- model revision: `21286e56ce98a86362db540863f91c083b8970f9`
- model weight SHA256:
  `9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`

Frozen H3:
- camel_tools git SHA:
  `be79ca9fc493f0df795375a7255bafef246a802d`
- morphology.db SHA256:
  `195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70`

---

## 11. Remaining DEVELOPMENT split — FROZEN

QALB14 TRAIN+DEV existing M2-R DEVELOPMENT only.

Development reconstructable:
**14,017 UIDs**

Excluded:
- M2-R P0: 120
- M2-R P1: 120
- overlap: 0

Remaining:
**13,777 UIDs**

Frozen split:
- `CALIBRATION`: 6,888
- `INTERNAL_EVALUATION`: 5,510
- `STRESS_DIAGNOSTIC`: 1,379

UID hashes:

CALIBRATION:
`3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9`

INTERNAL_EVALUATION:
`55a07608bd4ffd88f9d443aa877cae0830a20f4e797621853fb5bd096c276255`

STRESS_DIAGNOSTIC:
`aa0c341451adca4bf861a0758c36f6b6629e3c3af65b5f8c9f73da2997752587`

ALL_REMAINING:
`0a03e6f5a5a7c46ef917630a9fd8fc69fea1d651141c163ed55751564c6b375c`

Split lock commit:
`40545c5150a0831ee5d0d320da6049047693ff68`

Keep `INTERNAL_EVALUATION` and `STRESS_DIAGNOSTIC` text closed until component rules/thresholds are frozen.

---

## 12. CALIBRATION — MATERIALIZED

Run:
`36654588477`

Artifact:
- id `11070819539`
- ZIP SHA256:
  `ab5f303b4405162684d9a8ece23c0ed378b25e7863129a284f3e65ca0844058a`

Cases:
- total: 6,888
- changed source/reference: 6,867
- unchanged: 21

Operation counts:
- Edit: 59,875
- Add_before: 34,816
- Split: 3,776
- Merge: 6,629
- Delete: 2,427
- Move: 132
- Add_after: 12
- Other: 599

---

## 13. Critical H4 construct correction

Not every QALB `Split`/`Merge` is a whitespace-only boundary change.

Within CALIBRATION:

Split:
- total 3,776
- pure-space eligible: 2,633
- non-pure: 1,143

Merge:
- total 6,629
- pure-space eligible: 5,505
- non-pure: 1,124

Sentence availability:
- pure Split: 1,732 sentences
- pure Merge: 1,936
- either: 3,347
- both: 321
- neither: 3,049

H4 gold definition:
removing whitespace from source and replacement must leave the exact same character sequence.

The 2,267 non-pure Split/Merge edits are adversarial negatives, not positives.

Calibration protocol commit:
`f920d93ea90ef1364476cceb62aa9112baeab6f4`

---

## 14. ARETA role — FROZEN

Enhanced ARETA is used only for:
- stratification
- candidate selection
- diagnostic taxonomy
- coverage/error analysis

ARETA is **NOT independent human gold** and is not an approval oracle.

Use enhanced ARETA from:
- repo `CAMeL-Lab/arabic-gec`
- revision `8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`

H2 orthographic nomination can use ARETA orthographic codes.

H3 primary development-proxy nomination:
- MI
- MT

H3 results on this subset must be labeled:
**DEVELOPMENT PROXY**

---

## 15. ARETA diagnostic environment — FAILURES AND FINAL SUCCESS

Purpose:
validate an isolated historical environment for diagnostic enrichment only.

### Failure 1

Run:
`36656461533`

Result:
FAIL during dependency installation.

Cause:
`scikit-learn==0.23.2` under Python 3.9 attempted a source build, pulling `numpy==1.17.3`, which failed during metadata generation with:

`NameError: CCompiler is not defined`

Scientific interpretation:
software compatibility failure only.

### Fix 1

Changed Python only:
- 3.9 → 3.8

Kept historical pins unchanged.

Commit:
`3fccd966016a832c34f7cbdae1732adb0e7664da`

### Failure 2

Run:
`36657211515`

Result:
FAIL after environment installation succeeded.

Cause:
missing morphology data:

`~/.camel_tools/data/morphology_db/calima-msa-r13/morphology.db`

### Fix 2

Checked official CAMeL Tools v1.2.0 documentation.

For v1.2.0 the correct data command is:
`camel_data light`

The `light` package includes morphology and MLE data, including `calima-msa-r13`.

Commit:
`90eb4e3dd0b36106493376efc7221422aa91a067`

### Final successful preflight

Run:
`36657724871`

Result:
**SUCCESS**

Confirmed:
- `COALIGN_CONTRACT_OK`
- `ARETA_SYNTHETIC_DIAGNOSTIC_OK`

Synthetic labels:
`UC, UC, UC, OH, UC, UC`

The Hamza synthetic error was correctly surfaced as `OH`.

pip-freeze SHA256:
`56b9a3964f149eeab9db64ff118287b23a63bf05eb52c6599e9b4af859a12704`

Artifact:
- id `11073405357`
- ZIP SHA256:
  `9623141a4fb21ffaa8ff893ea6fb187610611ef854d055870c157ec86e4acfed`

Preflight opened no CALIBRATION/Internal/Stress text.

ARETA environment now considered:
**SOFTWARE FEASIBLE / DIAGNOSTIC-ONLY**

---

## 16. Current scientific status

M1:
CLOSED / DATA_READY

M2 monolithic verifier:
CLOSED FAIL

M2-R:
CLOSED; useful residual-risk signal but not standalone safety verifier

M2-H:
ACTIVE

Arabic deployment posture:
**REVIEW-first**

Measured M2-H verifier performance:
**not yet available**

Do not interpret software preflights as scientific success.

---

## 17. CLOSED / FORBIDDEN unless explicitly reopened

Do NOT:
- restart Phase 0 / 0B / 1
- regenerate the frozen 150 Nahw targets
- change the 41 Nahw passages
- consume the 59 reserved Nahw IDs
- read QALB15 TEST
- open A7'ta reserve (88)
- open Confirmation
- open Holdout
- open INTERNAL_EVALUATION text before calibration freeze
- open STRESS_DIAGNOSTIC text before calibration freeze
- start Phase 3
- tune SWEET or weaken safety gates merely to improve metrics
- run M2-R P2
- authorize M3 unless a later explicit decision does so

---

## 18. Exact next step

The next authorized work is:

1. freeze the successful ARETA preflight result in the repo;
2. run **ARETA enrichment on CALIBRATION only**;
3. extract H2/H3 diagnostic strata and counts;
4. do not run any verifier yet unless the enrichment output is validated;
5. keep INTERNAL_EVALUATION and STRESS_DIAGNOSTIC closed;
6. after H2/H3 strata are characterized, run H4 deterministic calibration and freeze component rules/thresholds before any internal evaluation.

---

## 19. How a new conversation should start

Recommended instruction:

> Read `RESUME_HERE.md` from branch `phase2-arabic-eval` in `abdullah-s-mahmood/sweet-runtime-parity`. Treat it as canonical. Inspect current branch HEAD and continue only from the exact next step. Do not restart closed phases. Use checkpoint execution with 2–4 strictly sequential tool operations and no parallel tool calls. Keep Arabic responses RTL-friendly and isolate English technical terms in backticks.

