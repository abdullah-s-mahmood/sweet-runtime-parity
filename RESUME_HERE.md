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

A single user "اكمل" may perform up to **20 tool operations**, but they must be **strictly sequential**. Do not run tools in parallel. For a long-running workflow: check up to five times at ~20-second intervals; if still running, switch to ~1-minute checks. Do not stop merely because it is still running; stop only when it completes or when evidence shows it is genuinely stalled/problematic. Keep all checks strictly sequential. If a step fails, identify the exact cause before changing architecture.

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

> Read `RESUME_HERE.md` from branch `phase2-arabic-eval` in `abdullah-s-mahmood/sweet-runtime-parity`. Treat it as canonical. Inspect current branch HEAD and continue only from the exact next step. Do not restart closed phases. Use checkpoint execution with up to 20 strictly sequential tool operations and no parallel tool calls. Keep Arabic responses RTL-friendly and isolate English technical terms in backticks.



## 20. CALIBRATION ARETA enrichment — COMPLETE

Workflow:
- `Phase 2 M2-H CALIBRATION ARETA Enrichment`
- run: `36658916857`
- head: `87a150f237850ef395458123cd41b105fbe84133`
- conclusion: **SUCCESS**

Scope validation:
- `CALIBRATION` cases reconstructed: **6,888**
- sentence groups processed by ARETA: **6,888**
- `CALIBRATION_RECONSTRUCTION_OK`: PASS
- `ARETA_CALIBRATION_SCOPE_OK`: PASS

Case-level diagnostic strata:
- orthographic: **6,363 / 6,888 = 92.38%**
- morphology primary (`MI` or `MT`): **1,544 / 6,888 = 22.42%**
- syntax: **3,640 / 6,888 = 52.85%**
- boundary (`MG` or `SP`): **2,997 / 6,888 = 43.51%**
- contains `UNK`: **706 / 6,888 = 10.25%**

Selected token/code counts:
- `OH`: 34,188
- `OT`: 5,917
- `OR`: 3,577
- `OA`: 2,923
- `OM`: 2,698
- `OD`: 2,583
- `MI`: 2,558
- `MT`: 39
- `MG`: 2,626
- `SP`: 3,093
- `UNK`: 992
- `UC`: 264,067

Important interpretation:
- these are **ARETA diagnostic strata**, not independent gold;
- H2 can now be calibrated on a large orthographic stratum;
- H3 has a non-trivial `MI/MT` development-proxy stratum;
- `UNK` remains material at ~10.25% of cases and must be handled explicitly rather than silently treated as clean;
- boundary ARETA labels are only diagnostic and do not replace the stricter pure-whitespace H4 gold contract already frozen.

Artifact:
- id: `11074295904`
- name: `m2h-calibration-areta-enrichment-v1`
- ZIP SHA256: `e29cd674e8606eff4d685ef59fa3e11b51b6a769425a29dcb4042884100dde1c`

Integrity:
- `INTERNAL_EVALUATION`: unopened
- `STRESS_DIAGNOSTIC`: unopened
- Confirmation: unopened
- Holdout: unopened
- A7'ta reserve: unopened
- reserved Nahw IDs: unopened
- QALB15 TEST: unopened

Scientific classification versus the prior checkpoint:
**IMPROVED**

Magnitude:
- moved from software-feasible ARETA smoke test to full diagnostic enrichment of all 6,888 CALIBRATION cases;
- no M2-H verifier quality metric has been measured yet, so scientific performance remains **UNCHANGED / NOT YET EVALUATED**.

Exact next authorized step:
1. validate the enrichment artifact structure and UID alignment;
2. define/freeze H2 deterministic orthographic rule families using CALIBRATION only;
3. define/freeze H3 morphology development-proxy protocol on `MI/MT`;
4. run H4 deterministic calibration against the previously frozen pure-whitespace boundary gold;
5. only after component rules/thresholds are frozen may `INTERNAL_EVALUATION` be opened.


## 21. ARETA artifact validation + component calibration freeze — COMPLETE

Artifact `11074295904` was downloaded and validated directly.

Validation:
- rows: **6,888**
- unique UIDs: **6,888**
- unique case IDs: **6,888**
- case IDs: `M2H-CAL-00001` through `M2H-CAL-06888`
- case ID sequence: PASS
- structural errors: **0**
- UID SHA256:
  `3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9`
- frozen UID SHA256 match: PASS
- pip-freeze SHA256:
  `56b9a3964f149eeab9db64ff118287b23a63bf05eb52c6599e9b4af859a12704`
- recorded pip-freeze hash match: PASS
- reserved/internal dataset markers in enrichment artifact: none found

Result:
**ARTIFACT VALIDATION PASS**

Component search space is now frozen in:
`phase2/redesign/M2H_COMPONENT_CALIBRATION_FREEZE_V1.md`

Key consequences:
- H2 may calibrate only the preregistered conservative surface families.
- H3 remains an MI/MT DEVELOPMENT PROXY and requires compatible morphology evidence; analyzability alone is insufficient.
- H4 still uses exact character preservation with whitespace-only boundary change; ARETA MG/SP is diagnostic only.
- H4 automatic approval requires at least two distinct frozen non-H1 evidence families.
- `UNK` is an explicit uncertainty state, never silently treated as clean or erroneous.

Scientific classification:
**IMPROVED METHODOLOGICALLY / PERFORMANCE NOT YET EVALUATED**

Exact next authorized step:
run H2 → H3 → H4 component calibration on `CALIBRATION` only, then freeze enabled/disabled families before opening `INTERNAL_EVALUATION`.


## 22. H1 candidate generation + H2 orthographic calibration + ALIF_VARIANT blind packet — CURRENT CHECKPOINT

### H1 CALIBRATION candidate generation — COMPLETE

Frozen H1 candidate contract:
`phase2/redesign/M2H_H1_CANDIDATE_CONTRACT_V1.md`

Workflow:
- run: `36691616010`
- job: `h1-calibration-candidates`
- conclusion: **SUCCESS**
- started: `2026-09-30T08:44:42Z`
- completed: `2026-09-30T09:19:00Z`

Artifact:
- id: `11088155733`
- name: `m2h-h1-calibration-candidates-v1`
- SHA256: `907065fd1a3e156456cec7a31f86facff689896b4d8d39b50cbc852ffd7cc8d3`

H1 results:
- CALIBRATION cases: **6,888**
- structured H1 candidates: **46,811**
- exact QALB-reference-supported: **32,502**
- reference-unsupported: **14,309**
- overall strict-reference support rate: **69.4324%**
- truncated cases: **0**
- non-applicable H1 edits: **18**

Important:
- H1 remains a candidate generator only.
- H1 confidence is diagnostic only and is not safety evidence.
- `REFERENCE_UNSUPPORTED` is not automatically linguistically wrong because QALB is single-reference.

### H2 deterministic orthographic calibration — COMPLETE

Frozen predicates:
`phase2/redesign/M2H_H2_ORTHOGRAPHIC_RULES_V1.md`

Calibration scorer:
`phase2/redesign/m2h_h2_calibrate.py`

Frozen result:
`phase2/redesign/M2H_H2_CALIBRATION_RESULT_V1.md`

Results:
- `HAMZA_ALIF_SEAT`: **85.57%** strict-reference lower bound
- `ALIF_MAQSURA_YA`: **90.34%**
- `TA_MARBUTA_HA`: **94.01%**
- `ALIF_VARIANT`: **95.85%**
- `SINGLE_ARABIC_LETTER_ORTHOGRAPHIC`: **93.90%**
- `DIACRITIC_ONLY`: no candidates, diagnostic-only
- `TATWEEL_ONLY`: no candidates, diagnostic-only

Frozen promotion gate remains:
`strict-reference precision lower bound >= 98%`

Result:
**0 / 5 non-diagnostic H2 families auto-promoted.**

The 98% gate was not lowered.

Scientific classification:
**MIXED**
- improved methodologically because H1→H2 is now measured reproducibly;
- worsened performance outlook for direct family-wide H2 auto-approval.

### ALIF_VARIANT blind adjudication — PROTOCOL AND PACKET FROZEN

Reason:
`ALIF_VARIANT` is closest to the 98% gate and QALB single-reference may undercount valid mandatory corrections.

Frozen protocol:
`phase2/redesign/M2H_H2_ALIF_VARIANT_BLIND_ADJUDICATION_PROTOCOL_V1.md`

Population:
- family total: **19,338**
- exact-supported: **18,536**
- reference-unsupported: **802**

To reach 98% overall:
- at least **416 / 802** unsupported candidates must truly be safe mandatory corrections.

Frozen sample:
- unsupported: **200**
- hidden exact-supported controls: **50**
- packet total: **250**

Frozen sampling salt:
`M2H-H2-ALIF-VARIANT-BLIND-V1-20260930-A`

Frozen statistical decision:
- exact one-sided 95% hypergeometric lower bound;
- need at least **115 / 200** unsupported sampled rows adjudicated exactly `SUPPORTED_MANDATORY`;
- this gives `K_lower_95 >= 419`;
- combined lower-bound family precision >= **98.019%**.

Anything below 115/200 fails to establish the 98% gate in this v1 protocol.

Controls:
- 50 exact-supported rows are hidden in the packet;
- any confirmed `UNNECESSARY_EDIT` or `WRONG_CORRECTION` control is a critical contradiction and prevents auto-promotion under v1.

Reviewer instructions:
`phase2/redesign/M2H_H2_ALIF_VARIANT_REVIEWER_INSTRUCTIONS_V1.md`

Primary-review validator:
`phase2/redesign/m2h_h2_validate_primary_review.py`

Blind-packet workflow:
- run: `36699684143`
- job: `build-blind-packet`
- conclusion: **SUCCESS**
- started: `2026-09-30T10:00:13Z`
- completed: `2026-09-30T10:00:21Z`

Review artifact:
- id: `11088429825`
- name: `m2h-h2-alif-variant-blind-review-v1`
- artifact SHA256: `4f25f69bc1d8b46b37629ab490273024dc032cd4ef40a57f3351e33f014b6d55`

Key artifact:
- id: `11088684206`
- name: `m2h-h2-alif-variant-blind-key-v1`
- artifact SHA256: `7edbdbee65627c85b9ad03a5f7081430f8b42bd8eb002c5cb94e069366299c82`

Blind packet content SHA256:
`e8e7dd687267cb4a53ea30c8f089114358b24123d9a0b4f3fbc9f061a404d9de`

Blind key content SHA256:
`f82c8a92cfdeeddef0a1a87b52f7e72a8e26e1c9d1ace959d8aa9805f0b315ae`

Packet integrity:
- unsupported population: **802**
- exact-supported population: **18,536**
- sample: **200 unsupported + 50 hidden controls**
- packet contains no gold-support label
- packet contains no QALB reference
- packet contains no H1 identity/confidence
- key is separate
- unique packet IDs: PASS
- unique candidate IDs in key: PASS
- local packet SHA verification: PASS

Still unopened:
- `INTERNAL_EVALUATION`
- `STRESS_DIAGNOSTIC`
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

### Promotion-standard reviewer requirement

Two independent qualified Arabic reviewers are required for the primary blinded Stage-A pass.

AI may prepare packets, validate structure, and perform explicitly labeled developmental diagnostics, but AI-only judgments do **not** satisfy the promotion-standard human-evidence requirement.

A higher-capability ChatGPT/model may be used only for a small focused ambiguous-case review packet when genuinely needed; do not send the whole project/system.

### Exact next authorized step

1. Do NOT open the blind key.
2. Do NOT reveal QALB reference or support status to primary reviewers.
3. Obtain two independent blinded primary reviews of the 250-row review packet.
4. Validate each review with `m2h_h2_validate_primary_review.py`.
5. Freeze/hash Reviewer A and Reviewer B outputs.
6. Compute pre-adjudication raw agreement / Cohen's kappa and disposition confusion matrix.
7. Resolve disagreements with a third qualified Arabic adjudicator or documented qualified consensus.
8. Only after final adjudication is frozen may the blind key be opened and the 115/200 hypergeometric decision computed.
9. If ALIF_VARIANT fails, do not lower the 98% gate. Proceed with H3/H4 with H2 ALIF_VARIANT disabled unless a separately versioned development iteration is justified.
10. Keep all reserved/internal splits closed until component activation decisions are frozen.


## 23. Reviewer-bottleneck resolution + H2-v2 closure — COMPLETE

### Reviewer bottleneck resolution

The 250-row blinded ALIF_VARIANT human-review packet remains frozen and valid, but **human review is no longer on the critical execution path** because qualified independent Arabic reviewers are not practically available.

Do not misrepresent AI review as human validation.

If qualified human reviewers become available later, the packet may be used as optional external validation.

A higher-capability ChatGPT/model may be used only for small focused ambiguity packets when genuinely needed; it does not substitute for independent human validation.

### H2 evidence-constrained development iteration v2

Frozen protocol:
`phase2/redesign/M2H_H2_EVIDENCE_CONSTRAINED_ITERATION_V2.md`

Purpose:
test a narrower automatic `ALIF_VARIANT` subset using independent CALIMA-MSA evidence, without lowering the 98% gate.

Frozen predicate:
- H2-v1 ALIF_VARIANT surface predicate passes;
- clean one-token Arabic source and candidate;
- source has zero CALIMA-MSA analyses;
- candidate has >=1 analysis;
- candidate analyses agree on one lexical identity;
- no proper-name risk;
- no analyzer/invariant failure.

Frozen activation gate:
- n >= 50
- strict-reference precision lower bound >= 98%
- zero invariant failures
- zero analyzer failures among accepted rows

Workflow:
- run: `36702245858`
- job: `h2-v2-calibration`
- conclusion: **SUCCESS**
- started: `2026-09-30T10:24:42Z`
- completed: `2026-09-30T10:26:54Z`

Artifact:
- id: `11090183156`
- name: `m2h-h2-v2-calibration-v1`
- SHA256: `769bcd52f897868ebcb5b64b46f217d0b0ee63b047d1815174ca2c7d3ab38d2b`

Results:
- ALIF_VARIANT family candidates: **19,338**
- accepted candidates: **0**
- exact-supported accepted: **0**
- reference-unsupported accepted: **0**
- accepted case coverage: **0**
- invariant failures among accepted: **0**
- analyzer failures: **0**

Reason counts:
- `SOURCE_ANALYZABLE`: **18,998**
- `CANDIDATE_UNANALYZABLE`: **339**
- `SURFACE_HYGIENE_FAIL`: **1**

Automatic activation:
**DISABLED**

Interpretation:
the hypothesis that erroneous ALIF_VARIANT source forms would often be absent from CALIMA-MSA while the corrected form is attested was falsified on CALIBRATION. Modern Arabic morphological analyzers have broad coverage, so analyzability alone is too permissive to act as a spelling-error discriminator.

Frozen result:
`phase2/redesign/M2H_H2_V2_RESULT.md`

Decision:
- H2-v2 CLOSED;
- do not lower the 98% gate;
- do not create another narrower ALIF_VARIANT rule from the same observed v2 failures;
- do not block progress waiting for human reviewers;
- current automatic H2 activation remains **none**.

Scientific classification versus H2-v1:
**WORSENED FOR H2 COVERAGE / IMPROVED SCIENTIFICALLY**

Magnitude:
- H2-v1 best family lower bound: ALIF_VARIANT **95.85%**, not activatable;
- H2-v2 accepted coverage: **0 / 19,338 = 0%**;
- automatic H2 families enabled: remains **0**.

Still unopened:
- `INTERNAL_EVALUATION`
- `STRESS_DIAGNOSTIC`
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

### Exact next authorized step

Proceed directly to:
1. H3 morphology-aware CALIBRATION development proxy using the already frozen MI/MT protocol;
2. H4 structural boundary calibration;
3. freeze final component activation decisions;
4. only then consider opening INTERNAL_EVALUATION.

Do not reopen H2 tuning in the current development iteration.


## 24. H3 + H4 closure and H1-H4 activation freeze — COMPLETE

### H3 morphology-aware CALIBRATION — CLOSED FAIL

Protocol:
`phase2/redesign/M2H_H3_MORPHOLOGY_CALIBRATION_PROTOCOL_V1.md`

Workflow:
- run: `36703934748`
- job: `h3-calibration`
- conclusion: **SUCCESS**

Artifact:
- id: `11091545756`
- SHA256: `82372c564d0f05dd16b3f7cc6d141c5eb77647a2c3a4277560ab6c6dc71d7f27`

Results:
- MI/MT annotations: **2,597**
- mapped annotations: **2,529**
- exact-span H1 candidates: **169**
- exact-reference-supported nominated: **85**
- H3-supported: **3**
- exact-reference-supported H3-supported: **1**
- candidate recall: **1.18%**
- target recall: **>=70%**
- supported-candidate precision proxy: **33.33%**
- false-positive case proxy: **66.67%** on only 3 supported cases

H3 activation:
**DISABLED**

Result file:
`phase2/redesign/M2H_H3_CALIBRATION_RESULT_V1.md`

### H4 structural boundary CALIBRATION — CLOSED / NOT ACTIVATED

Frozen protocol:
`phase2/redesign/M2H_H4_BOUNDARY_CALIBRATION_PROTOCOL_V1.md`

Initial workflow run:
`36704936665`
failed before H4 execution because the workflow validator referenced an old-summary integrity key that did not exist. This was an operational validation bug only.

Fix commit:
`7a962e124321d4ba993bd8fc9165c667b4f78b87`

Successful workflow:
- run: `36705698086`
- job: `h4-calibration`
- conclusion: **SUCCESS**
- started: `2026-09-30T10:58:55Z`
- completed: `2026-09-30T11:00:59Z`

Artifact:
- id: `11092051414`
- name: `m2h-h4-calibration-v1`
- SHA256: `060b5ee437feefae2031108c102ee408ffe61178a813b54396599b199970994e`

SPLIT:
- pure gold total: **2,633**
- accepted: **0**
- recall: **0.00%**
- H1 PURE_SPLIT stream: **1,920**
- H1 accepted: **0**
- non-pure adversarial accepted: **0 / 1,143**
- general diagnostic accepted: **0 / 1,000**
- activation: **DISABLED**

MERGE:
- pure gold total: **5,505**
- accepted: **2,612**
- recall: **47.45%**
- frozen recall target: **>=70%**
- H1 PURE_MERGE stream: **3,792**
- H1 accepted: **1,853**
- accepted exact-reference-supported: **1,779**
- accepted reference-unsupported: **74**
- strict-reference precision lower bound: **96.01%**
- frozen precision target: **>=90%**
- non-pure adversarial accepted: **0 / 1,124**
- general diagnostic accepted: **0 / 1,000**
- activation: **DISABLED** because recall failed by **22.55 pp**

H4 result:
`phase2/redesign/M2H_H4_CALIBRATION_RESULT_V1.md`

Scientific interpretation:
- structural invariance is highly safe;
- current two-of-three evidence requirement is too sparse for required recall;
- do not tune H4-v1 post hoc;
- any future contextual boundary verifier must be separately versioned.

### H1-H4 activation freeze

Frozen in:
`phase2/redesign/M2H_COMPONENT_ACTIVATION_FREEZE_V1.md`

Commit:
`50794b34b224ac867f0cadde0d2c8facc2d83fa9`

Current component state:
- H1: **ACTIVE AS CANDIDATE GENERATOR ONLY**
- H2: **NO AUTOMATIC FAMILY ACTIVATED**
- H3: **NOT ACTIVATED**
- H4: **NO OPERATION ACTIVATED**

Standalone automatic validators after CALIBRATION:
**NONE**

This negative result does not authorize gate weakening.

### H5/H6 remain authorized by the original protocol

The original frozen `M2H_HYBRID_VERIFIER_PROTOCOL_V1.md` explicitly preregistered:
- H5 Risk Fusion
- H6 Sentence Completeness

Therefore H5/H6 are not a post-hoc invention.

One-attempt rule now applies:
- one preregistered H5/H6 CALIBRATION implementation only;
- no iterative tuning loop;
- freeze features/model/thresholds before INTERNAL_EVALUATION;
- if H5/H6 cannot meet the preregistered feasibility logic without changing definitions/gates, record failure and stop the M2-H path.

H5 may consume frozen raw H1-H4 evidence features, but failed H2/H3/H4 components may not be reinterpreted as standalone safe validators.

### INTERNAL_EVALUATION remains unopened

Still unopened:
- INTERNAL_EVALUATION text
- STRESS_DIAGNOSTIC text
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

### Exact next authorized step

Start the single H5/H6 iteration:
1. fresh rigorous research and adversarial brainstorming;
2. freeze H5 target labels, feature set, calibration model, thresholds, and H6 sentence-completeness derivation;
3. calibrate on CALIBRATION only;
4. freeze H5/H6 result;
5. only after that freeze, open INTERNAL_EVALUATION once.


## 25. Critical pre-H5 H1 recall audit — PROVISIONAL BLOCKER

Before freezing H5/H6, the original H1 feasibility gate in `M2H_HYBRID_VERIFIER_PROTOCOL_V1.md` was rechecked.

Frozen H1 target:
- candidate edit-instance recall >= **80%**

Direct strict-reference audit on CALIBRATION, using current H1 candidate exact-support matching:

- total QALB gold edit instances: **108,266**
- exact gold edit identities covered by at least one current H1 candidate: **32,502**
- provisional strict edit-instance recall: **30.0205%**

By QALB operation:
- Edit: 26,662 / 59,875 = **44.53%**
- Add_before: 0 / 34,816 = **0.00%**
- Split: 1,782 / 3,776 = **47.19%**
- Merge: 3,806 / 6,629 = **57.41%**
- Delete: 189 / 2,427 = **7.79%**
- Move: 1 / 132 = **0.76%**
- Other: 62 / 599 = **10.35%**
- Add_after: 0 / 12 = **0.00%**

Case-level diagnostic:
- cases with at least one gold edit: **6,867**
- at least one gold edit covered: **6,478 / 6,867 = 94.34%**
- all gold edits covered: **53 / 6,867 = 0.77%**

### IMPORTANT: this is not yet a final H1 scientific failure

The zero coverage for all 34,816 `Add_before` edits is suspicious.

Possible causes that must be falsified before interpreting the 30.02% value:
1. source-span convention mismatch for insertion edits between QALB reconstructed gold and H1/difflib candidate transactions;
2. candidate extraction alignment semantics may fail to map H1 insertions to zero-width QALB spans;
3. current H1 runner uses Hugging Face `BertForTokenClassification` and direct tokenization rather than the official repository's custom `gec.model.BertForTokenClassification` + official preprocessing pipeline;
4. one-pass candidate transaction alignment may undercount exact gold even when the rewritten sentence contains the correct insertion.

Therefore:

**H5/H6 is temporarily BLOCKED pending H1 feasibility audit.**

Do NOT:
- declare H1 failed solely from the provisional 30.02% figure;
- open INTERNAL_EVALUATION;
- change H5 architecture;
- tune H1 model;
- change the frozen 80% gate.

### Exact next authorized step

Audit H1 reproducibility and gold-span matching on CALIBRATION only:

1. inspect H1 candidate operation counts, especially INSERT / Add_before mapping;
2. inspect a deterministic small sample of current H1 insertion candidates versus QALB Add_before span semantics;
3. compare the current runner against official `CAMeL-Lab/text-editing` inference/preprocessing code at frozen revision `4d552ca3ae98029550f27fc52aa1b22883e16e61`;
4. determine whether the provisional recall deficit is a measurement/extraction bug or genuine model coverage;
5. only after that determination decide whether H5/H6 remains scientifically viable.

INTERNAL_EVALUATION and every reserved dataset remain unopened.


## 26. H1 official-alignment recall audit — FINAL / H1-v1 GATE FAIL

The provisional exact-transaction figure in Section 25 is superseded for the H1 feasibility decision by the representation-invariant official-alignment audit below.

### Inference parity — PASS

Frozen H1:
- model: `CAMeL-Lab/text-editing-qalb14-nopnx`
- model revision: `21286e56ce98a86362db540863f91c083b8970f9`
- implementation revision: `4d552ca3ae98029550f27fc52aa1b22883e16e61`
- decode: one-pass, top-1, NoPnx

Deterministic CALIBRATION parity sample:
- sample: **256**
- subwords match: **256 / 256**
- labels match: **256 / 256**
- normalized rewrite match: **256 / 256**
- all-field parity: **256 / 256**
- mismatches: **0**

Conclusion:
the frozen H1 inference stream is validated against the public/official inference path. The recall deficit is not explained by an H1 runner parity bug.

### Tatweel alignment edge case — resolved without dropping cases

Upstream `char_level_alignment` fails on QALB rows containing U+0640 tatweel because the upstream normalization removes kashida before exact surface reconstruction.

Frozen amendments:
- `phase2/redesign/M2H_H1_OFFICIAL_ALIGNMENT_TATWEEL_AMENDMENT_V1.md`
- `phase2/redesign/M2H_H1_OFFICIAL_ALIGNMENT_TATWEEL_CHARALIGN_AMENDMENT_V1.md`

Final CALIBRATION gold-construction loop:
- cases processed: **6,888 / 6,888**
- elapsed: **1,279.8 s**
- final rate: **5.382 cases/s**
- construction failures: **0**
- char-alignment cross mismatches: **0**
- word/subword NoPnx cross-path mismatches: **0**

Source run:
`36716848223`

Source artifact:
- id: `11098030966`
- SHA256: `ad476c7dfb8e194320a1a5d4b0a05ea016be5e4b012403854290fc86ca455fb1`

### Scoring-only continuation — SUCCESS

To avoid rerunning the completed 6,888-case gold-construction loop after an operational M2 import-context failure, a frozen scoring-only continuation was created:

`phase2/redesign/M2H_H1_SCORING_CONTINUATION_CHECKPOINT_V1.md`

Workflow:
- run: `36720612925`
- job: `h1-scoring-continuation`
- conclusion: **SUCCESS**

Artifact:
- id: `11101562193`
- name: `m2h-h1-official-alignment-scoring-continuation-v1`
- SHA256: `5f3478162cb54034cb89a58a47db32f70e50573186b7df980215e56b3259e420`

### Official-alignment one-pass NoPnx M2 result

- Precision: **71.53%**
- Recall: **69.39%**
- F1: **70.44%**
- F0.5: **71.09%**
- frozen H1 recall gate: **>=80%**
- recall deficit: **-10.61 pp**
- gate: **FAIL**

Secondary:
- derived gold M2 edit lines: **35,559**
- exact NoPnx reference sentences: **1,540 / 6,888 = 22.36%**
- source-copy sentences: **283 / 6,888 = 4.11%**

This is **not borderline**. The miss exceeds 10 percentage points.

### Fresh external sanity check

The public SWEET model card/repository example uses iterative NoPnx decoding (`decode_iter=2`) before one Pnx pass.

This does not retroactively rescue H1-v1 because H1-v1 was frozen as one-pass before metrics were observed.

A separately versioned iterative diagnostic may be considered only after focused methodological review, with:
- H1-v1 permanently retained as FAIL;
- no change to the 80% gate;
- no INTERNAL_EVALUATION access;
- a preregistered one-attempt stopping rule;
- no iterative tuning loop.

### Downstream validity

Because H1 inference parity passed 256/256 and the H1 candidate stream did not change:
- H2 does **not** require candidate regeneration; remains closed with no automatic family activated.
- H3 does **not** require rerun; remains CLOSED FAIL.
- H4 does **not** require rerun; remains not activated.
- M1 / M2 / M2-R remain closed and unaffected.

H5/H6:
**BLOCKED pending focused methodological decision.**

Do NOT open:
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC
- Confirmation
- Holdout
- A7'ta reserve
- reserved Nahw IDs
- QALB15 TEST

Focused review packet:
`phase2/redesign/FOCUSED_REVIEW_PACKET_H1_PARITY_AND_DOWNSTREAM_VALIDITY.md`

### Scientific classification

**WORSENED FOR M2-H VIABILITY / IMPROVED SCIENTIFIC CERTAINTY**

Magnitude:
- frozen target: **80.00% recall**
- observed official-alignment one-pass recall: **69.39%**
- deficit: **10.61 pp**
- parity uncertainty reduced to **0 / 256 mismatches**
- gold-construction failures reduced from the tatweel blocker to **0 / 6,888**

### Exact next authorized step

Do **not** start H5/H6 and do **not** open INTERNAL_EVALUATION yet.

Perform a focused methodological review of:
1. whether official-alignment M2 recall is the defensible realization of the frozen H1 candidate-recall gate;
2. whether H1-v1 should be formally CLOSED FAIL;
3. whether exactly one separately versioned iterative-decoding diagnostic is scientifically justified by the published SWEET usage pattern;
4. whether such a diagnostic would have a preregistered no-tuning stopping rule.

If no defensible exception is established, close H1-v1 and the current M2-H path before H5/H6.


## 27. H1-v1 formal closure — CURRENT AUTHORIZED STATE

Final decision file:
`phase2/redesign/M2H_H1_FINAL_DECISION_V1.md`

Decision:
**H1-v1 = CLOSED FAIL**

Basis:
- frozen operational gate realization: official-alignment one-pass NoPnx M2 recall;
- observed Recall: **69.39%**;
- frozen gate: **>=80%**;
- deficit: **-10.61 pp**;
- classification: not borderline.

Supporting reproducibility:
- inference parity: **256 / 256**, mismatches **0**;
- CALIBRATION gold construction: **6,888 / 6,888**;
- gold-construction failures: **0**;
- char-alignment cross mismatches: **0**;
- word/subword cross-path mismatches: **0**.

Current M2-H path:
**CLOSED BEFORE H5/H6**

Do NOT start:
- H5 Risk Fusion
- H6 Sentence Completeness
- INTERNAL_EVALUATION
- STRESS_DIAGNOSTIC

Public SWEET usage does show iterative NoPnx decoding (`decode_iter=2`), but H1-v1 was frozen as one-pass and cannot be retroactively changed.

Any future iterative SWEET study must be a separately versioned architectural diagnostic with a new frozen protocol. It cannot overwrite H1-v1 and is not currently authorized as part of the closed M2-H path.

Reserved datasets remain closed.

### Scientific classification

**WORSENED FOR CURRENT M2-H VIABILITY / IMPROVED SCIENTIFIC CERTAINTY**

### Exact next authorized direction

Do not continue M2-H tuning.

The next substantive Arabic correction step must be a **new architecture decision phase** with fresh research, explicit alternatives, and frozen gates before any new evaluation.


## 28. Arabic correction architecture v2 — MP-SEF STARTED

The closed M2-H path remains closed.

New architecture decision:
`phase2/redesign/ARABIC_CORRECTION_ARCHITECTURE_V2_MPSEF.md`

Commit:
`730b9bb944a1967180e33401fa3836fed72cbc8a`

Architecture:
**Multi-Proposer Selective Edit Fusion (MP-SEF)**

Core principle:
separate proposal generation from edit authorization.

Initial reproducible proposers:
- P1: SWEET QALB14 NoPnx, same frozen weights as H1-v1 but separately versioned with documented iterative decoding `decode_iter=2`;
- P2: AraBART+Morph+GED QALB14 with paired CAMeLBERT GED and official arabic-gec preprocessing/inference path.

Proposer identity freeze:
`phase2/redesign/MPSEF_PROPOSER_IDENTITY_FREEZE_V1.md`

Commit:
`b453236cf5d80c0916a0c23fd167af14edaefc85`

P2 frozen identities:
- AraBART GEC revision:
  `410588a318d988cdcfdbf64cf5745ed4adea0f6a`
- CAMeLBERT GED revision:
  `447179dc63d186e4bff09a993e90e73ad622d571`
- official arabic-gec repo revision:
  `8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`
- modified Transformers dependency:
  `bc21aaca789f1a366c05e8b5e111632944886393`

Initial feasibility gate:
- candidate-union recall >=95% before any selector is built;
- 90% to <95% = borderline methodological review;
- <90% = proposer architecture must be revisited;
- no selector tuning before proposal gate passes.

Conditional components MTAGEC and STAGEET are research-track only until reproducible checkpoints/code are established.

### P1 iterative parity — RUNNING

Runner:
`phase2/redesign/mpsef_p1_iterative_parity.py`

Workflow:
`.github/workflows/phase2-mpsef-p1-iterative-parity-v1.yml`

Workflow commit:
`a514e99159c4e87b9fdca83225224618dc2e7d6b`

Current run:
`36748281679`

Job:
`109999992046`

Last observed state:
**in_progress**

Parity sample:
- 64 deterministic CALIBRATION source-only cases;
- no gold/reference consulted;
- two-pass NoPnx trace comparison;
- required pass1/pass2/all-field match: 100%.

Do not start P2 parity until P1 parity is resolved.

Reserved/internal datasets remain closed.

### Scientific classification

**IMPROVED ARCHITECTURALLY / PERFORMANCE NOT YET MEASURED**

The new design directly addresses the demonstrated single-proposer recall bottleneck while preserving REVIEW-first operation and protected-invariant safeguards.

### Exact next authorized step

1. Resolve P1 parity run `36748281679`.
2. If P1 parity passes, freeze its runtime artifact/hash.
3. Only then run P2 runtime parity.
4. Only after both parity checks pass, implement canonical edit extraction and the P1+P2 candidate-union feasibility experiment.
5. Do not build an authorization selector until candidate-union recall is frozen.


## 29. MP-SEF P1 runtime parity — PASS; P2 parity started

P1 runtime lock:
`phase2/redesign/MPSEF_P1_RUNTIME_LOCK_V1.md`

Lock commit:
`e3e878db3736fe1b7aab5afc88fb68caa34ff0de`

P1 parity run:
`36749690421`

P1 artifact:
- id: `11113469233`
- digest: `sha256:994c98dbe965883f9097a1845dc3240105b3fb11de709aeb11f454b6a34dfbb0`

P1 result:
- sample: **64 source-only CALIBRATION cases**
- pass 1 exact trace match: **64 / 64**
- pass 2 exact trace match: **64 / 64**
- all-field match: **64 / 64**
- mismatches: **0**
- gold/reference consulted: **false**
- INTERNAL_EVALUATION opened: **false**
- STRESS_DIAGNOSTIC opened: **false**

P1 runner SHA256:
`31b0d7728b2d74e9848601653fd91017e54d83867861c287479bbe1c847fe1f1`

P1 pip-freeze SHA256:
`aa9c31581f733395b1da19244c9971818499dd1d5bd1d3da0b2057b91fe66df4`

Decision:
**P1 activated as proposer only.**
No automatic correction is authorized.

### P2 parity — RUNNING

Runner:
`phase2/redesign/mpsef_p2_arabart_ged_parity.py`

Workflow:
`.github/workflows/phase2-mpsef-p2-arabart-ged-parity-v1.yml`

Workflow commit:
`cbba8356faf662104f14849f9c9e89a33826d813`

Current run:
`36750725611`

Current job:
`110008353484`

Last observed state:
- run: queued/in progress transition;
- clone frozen official arabic-gec implementation: in progress;
- P2 inference not started yet.

P2 parity gate:
- deterministic 64 source-only CALIBRATION cases;
- exact morphology-preprocessed text match: 64/64;
- GED labels match: 64/64;
- GEC subword tokens/input ids/GED label ids match: 64/64;
- exact generated output match: 64/64;
- all-field match: 64/64;
- no gold/reference consultation.

Do not compute candidate-union recall until P2 parity is frozen PASS.

Reserved/internal datasets remain closed.


## 30. MP-SEF P2 runtime parity — PASS; independent review checkpoint

P2 runtime lock:
`phase2/redesign/MPSEF_P2_RUNTIME_LOCK_V1.md`

Lock commit:
`a49bc394033edfdd8552cff163e92d163f26318d`

P2 parity run:
`36751445734`

P2 job:
`110010823722`

P2 artifact:
- id: `11114738715`
- digest:
  `sha256:c8d2ea2b378a03b3e6ca5f81b53a0527f0f796d8610a6d615027eedce06cbaf3`

P2 deterministic source-only parity:
- sample: **64**
- morphology-preprocessed text: **64 / 64**
- GED labels: **64 / 64**
- AraBART subword tokens: **64 / 64**
- input IDs: **64 / 64**
- GED label IDs: **64 / 64**
- generated exact output: **64 / 64**
- generated normalized output: **64 / 64**
- all-field match: **64 / 64**
- mismatches: **0**

P2 sample UID SHA256:
`f787df9c7acabbb5b6cb02a04c12e5d505e7590b94b19deca9064d321223c6f6`

P2 runner SHA256:
`746274e34cc73f0a6f99994f25d5f7e23dd064f54d1b86a2eddc716da7a15f75`

P2 pip-freeze SHA256:
`cbd42c8a3296eb59e933b04f83c70f34d78b98160f09a069fea32fcfc142fe38`

P2 model hashes:
- GED pytorch_model.bin:
  `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`
- GEC pytorch_model.bin:
  `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`

Integrity:
- gold/reference consulted: **false**
- INTERNAL_EVALUATION opened: **false**
- STRESS_DIAGNOSTIC opened: **false**

Current proposer status:
- P1 iterative SWEET: **PASS / proposer only**
- P2 AraBART+Morph+GED: **PASS / proposer only**

No candidate-union metric has been observed.

### Independent review gate

Candidate-union evaluation is now:
**BLOCKED PENDING INDEPENDENT HIGHER-MODEL METHODOLOGICAL REVIEW**

Final review packet:
`phase2/redesign/FOCUSED_REVIEW_PACKET_MPSEF_ARCHITECTURE_V2.md`

Final packet commit:
`3313b592120368ad7a11569ad0b1079e7bcdc1c7`

Higher-model prompt:
`phase2/redesign/PROMPT_HIGHER_MODEL_MPSEF_ARCHITECTURE_REVIEW_V1.txt`

Prompt commit:
`dc23dd7d3dfb0dc58176a34830692c2d0d94b845`

The higher-model review must occur before candidate-union measurement to avoid post-hoc protocol adaptation after seeing union performance.

Fresh literature challenge before consultation supports investigating heterogeneous system combination, edit-level selection, and generator+scorer designs, but also highlights:
- system diversity as a prerequisite for useful combination;
- seq2seq over-correction risk;
- candidate/edit decomposition construct risk;
- development-data reuse/double-dipping risk.

### Scientific classification

Relative to the closed M2-H path:

**IMPROVED ARCHITECTURALLY AND REPRODUCIBLY / PERFORMANCE NOT YET MEASURED**

Magnitude of reproducibility improvement:
- P1 runtime parity: **64/64 all-field**
- P2 runtime parity: **64/64 all-field**
- both source-only; no gold/reference consultation.

Performance forecast:
candidate-union coverage is expected to be at least as high as the best constituent proposer under a valid union definition, but the magnitude of unique gain is intentionally unknown and must not be estimated from the unseen CALIBRATION result.

Main unresolved risks before union:
1. seq2seq coupled-edit decomposition;
2. definition of the primary candidate-stage endpoint;
3. whether CALIBRATION must be subdivided before union/selector work;
4. proposer diversity sufficiency;
5. anti-loop stop rules;
6. whether a learned selector should be permitted at all.

### Exact next authorized step

Obtain independent higher-model review using the frozen packet and prompt.

Do NOT:
- run candidate-union evaluation;
- add a third proposer;
- train/calibrate a selector;
- change the >=95% proposed union gate;
- repartition CALIBRATION;
until the review is returned and adjudicated.

Reserved/internal datasets remain closed.


## 31. MP-SEF independent review adjudicated — V3 pre-union methodology frozen

Independent review supplied by user:
- MPSEF_INDEPENDENT_REVIEW_AR.md
- decision: **MODIFY PROTOCOL BEFORE UNION MEASUREMENT**
- no union measurement, simulation, selector training, or reserved-data access occurred in that review.

Core review requirements adopted:
- replace raw union recall with jointly realizable `R_joint`;
- represent proposer output as source-anchored bundles with dependencies/conflicts;
- preserve original-source provenance through P1 iterative passes and P2 morphology/GED/generation;
- maintain explicit exposure ledger;
- freeze stop rules before any metric;
- keep the >=95% candidate-availability floor, but apply it to `R_joint`;
- do not authorize selector training or AUTO_SAFE merely because proposal availability passes.

Frozen protocol:
`phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3.md`

Protocol commit:
`a666ec4da15a552b347d5907b87f58ae496526b5`

Frozen contracts:
- `MPSEF_BUNDLE_CONTRACT_V1.md`
  commit `642c39bc7b14af1ba0525da4416c2cf723d5c04e`
- `MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md`
  commit `1780842256ddb9833054df3a8ff7f685a85f47c0`
- `MPSEF_PROTECTED_INVARIANTS_CONTRACT_V1.md`
  commit `1a9b4f536d031f4278e995e2cc4aad73c64fdac1`

No candidate metric was computed while creating these documents.

## 32. New training-overlap discovery — protocol amended BEFORE measurement

A required provenance audit found that the frozen 6,888-record CALIBRATION artifact contains:
- **6,571 QALB-2014 train-origin records**
- **317 QALB-2014 dev-origin records**

Public provenance confirms:
- P1 SWEET-QALB14 was fine-tuned on QALB-2014 and the paper trains QALB-2014 taggers on the QALB-2014 training setup;
- P2 AraBART-QALB14 was fine-tuned on QALB-2014 with the standard Train-L1 / Dev-L1 / Test-L1 organization.

Therefore a generic random 30/40/30 split across all CALIBRATION would put direct proposer-training-origin records into the primary feasibility population.

This confound was discovered before any P1+P2 feasibility metric.

Frozen audit:
`phase2/redesign/MPSEF_TRAINING_OVERLAP_AUDIT_V1.md`

Audit commit:
`e8389cdbaa3804df396e337d1e195671b74d737d`

Frozen amendment:
`phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3_TRAINING_OVERLAP_AMENDMENT_V1.md`

Amendment commit:
`1f2827083b599325017e69d8852e9584a9a1e694`

Revised primary feasibility population:
**D_DEV_FEAS_V1**

Definition:
- all 317 CALIBRATION records with original QALB-2014 split == dev;
- no QALB-2014 train-origin record;
- developmental / dev-origin / not independent.

Train-origin population:
**D_TRAIN_INTERNAL_V1**
- 6,571 records;
- development only;
- excluded from primary candidate-availability gate.

The higher-model 30/40/30 concept is deferred for any future selector role separation; it is not used to define the first proposer-feasibility population.

## 33. Pre-union manifests and exposure ledger — PASS / FROZEN

Source-only manifest generator:
`phase2/redesign/mpsef_prepare_preunion_manifests_v1.py`

Generator commit:
`549406b2151727280db57fe077ce6e6e885a1c54`

Generator SHA256:
`a79e0bfc0c73a9cf92ea342103cc4d4b357363ba61da049e212ba576be1f0d5d`

Workflow:
`.github/workflows/phase2-mpsef-preunion-manifests-v1.yml`

Workflow commit:
`c5dfd4db8da6e84f36988cd3bd14ba596344c79a`

Run:
`36761718922`

Job:
`110045678462`

Conclusion:
**SUCCESS**

Artifact:
- id: `11119695370`
- name: `mpsef-preunion-manifests-v1`
- digest:
  `sha256:1163b37d2c0b50f8a1f6f804e3c012928f1bc3a894c7cb0d87cbffd66196b712`

Manifest lock:
`phase2/redesign/MPSEF_PREUNION_MANIFEST_LOCK_V1.md`

Lock commit:
`bfc08addb199808e311d21820a7e1ee2cdd03a30`

Preflight:
**PASS**

Reproduced counts:
- total CALIBRATION records: **6,888**
- train-origin: **6,571**
- dev-origin: **317**
- total duplicate/near-duplicate clusters: **6,871**
- non-singleton clusters: **15**
- max cluster size: **4**
- near-duplicate edges: **20**
- dev clusters: **317**
- train/dev crossing clusters: **0**
- D_DEV_FEAS_V1 records: **317**
- D_DEV_FEAS_V1 clusters: **317**
- D_TRAIN_INTERNAL_V1 records: **6,571**
- D_TRAIN_INTERNAL_V1 clusters: **6,554**
- cluster overlap between the two populations: **0**

Exposure ledger:
- all 6,888 records gold_exposed=true;
- all 6,888 aggregate_result_exposed=true;
- all 6,888 independence_claim_allowed=false;
- 6,571 marked KNOWN_OR_HIGHLY_EXPECTED_DIRECT_TRAIN_OVERLAP;
- 317 marked MODEL_DEVELOPMENT_EVALUATION_EXPOSURE;
- fine-grained historical error-analysis exposure conservatively unknown for all records.

Integrity:
- candidate_metric_computed=false
- reference_content_used_for_manifest_generation=false
- gold_edit_content_used_for_manifest_generation=false
- INTERNAL_EVALUATION opened=false
- STRESS_DIAGNOSTIC opened=false
- reserved_data_opened=false

### Scientific classification

Relative to the initial MP-SEF v2 proposal:

**IMPROVED METHODOLOGICALLY / PERFORMANCE STILL NOT MEASURED**

Specific improvement:
the primary feasibility population is no longer dominated by direct proposer-training-origin records.

Remaining limitation:
D_DEV_FEAS_V1 is still development-exposed and cannot be treated as independent generalization evidence.

### Current authorization state

P1:
PASS / proposer only.

P2:
PASS / proposer only.

Pre-union methodology:
FROZEN WITH TRAINING-OVERLAP AMENDMENT.

Pre-union manifests:
PASS / FROZEN.

Candidate feasibility / R_joint:
**NOT RUN**

Selector:
**NOT AUTHORIZED**

AUTO_SAFE:
**NOT AUTHORIZED**

Reserved/internal datasets:
**CLOSED**

### Exact next decision point

Before running the single P1+P2 feasibility measurement on D_DEV_FEAS_V1, adjudicate whether the training-overlap amendment should receive a focused independent delta review because it changes the higher-model review's originally proposed generic 30/40/30 role split.

Do not silently revert to 30/40/30 across train+dev.

Do not run feasibility until this decision is explicitly resolved.


## 34. Focused higher-model delta review prepared — current stop point

Reason:
the first higher-model review recommended a generic 30/40/30 future role split before candidate measurement, but it did not have the newly established CALIBRATION composition and proposer-training-overlap evidence.

New fact established before any candidate metric:
- CALIBRATION train-origin: 6,571
- CALIBRATION dev-origin: 317
- P1: QALB-2014 fine-tuned system
- P2: QALB-2014 fine-tuned system
- train/dev crossing duplicate clusters under frozen rule: 0

Primary feasibility population was therefore prospectively changed to:
**D_DEV_FEAS_V1 = 317 dev-origin records**

This is labeled:
**DEVELOPMENTAL / DEV-ORIGIN / NOT INDEPENDENT**

A focused delta review packet now exists:

`phase2/redesign/FOCUSED_REVIEW_PACKET_MPSEF_V3_TRAINING_OVERLAP_DELTA.md`

Packet commit:
`18672b4a28d21fd8494743cddbf913d3a6bde148`

Higher-model delta prompt:

`phase2/redesign/PROMPT_HIGHER_MODEL_MPSEF_V3_TRAINING_OVERLAP_DELTA_REVIEW_V1.txt`

Prompt commit:
`66c4e62e13e9bfc1417c6b167b388ebf6091df07`

The delta review asks only whether:
- D_DEV_FEAS_V1 is a defensible first developmental feasibility population;
- it is preferable to train-dominated generic 30/40/30;
- 317 dev-origin cases are sufficient for the limited primary R_joint question;
- the >=95% floor should remain;
- external non-QALB evidence is required now or only for later generalization/AUTO_SAFE claims.

No experiment is requested in the delta review.

### Exact current stop rule

Do NOT run P1+P2 R_joint yet.

Obtain/adjudicate the focused delta review first because the training-overlap discovery changes one material recommendation from the first independent review.

No files/data are currently missing from the project side.

Reserved/internal datasets remain closed.


## 31. MP-SEF V3 foundational pre-measurement artifacts — PASS

Independent higher-model review decision:
**MODIFY PROTOCOL BEFORE UNION MEASUREMENT**

The requested V3 methodology has now been materialized and frozen.

### V3 protocol

File:
`phase2/redesign/MPSEF_PRE_UNION_PROTOCOL_V3.md`

Commit:
`a666ec4da15a552b347d5907b87f58ae496526b5`

Primary methodological changes:
- raw union recall replaced by jointly realizable `R_joint`;
- original-source anchoring required;
- gold-guided atomic decomposition forbidden;
- bundle/dependency semantics frozen;
- CALIBRATION explicitly treated as historically consumed development evidence;
- future role split cannot restore historical independence;
- strict stop rules frozen.

### Exposure ledger — PASS

Workflow run:
`36762360756`

Artifact:
- id: `11119212690`
- digest:
  `sha256:556946d798e58ea507ec73f45d9de2192d873465c684c1a170820af100e58a47`

Ledger SHA256:
`a58fd47ff8a85969eb740ed669d71e98fff10369779c7e8cef152a001135b1b3`

Evidence:
- cases: **6,888**
- train origin: **6,571**
- dev origin: **317**
- document IDs recovered: **2,563**
- author IDs available: **0**
- exact duplicate groups: **7**
- exact duplicate records: **15**
- all records historically independent: **false**
- all records gold/reference exposed: **true**
- all records aggregate-result exposed: **true**
- exact record-level manual/error-analysis exposure: **unknown**

Training-overlap claim:
- P1 dataset scope: QALB-2014 confirmed
- P2 dataset scope: QALB-2014 confirmed
- record-level training overlap: unresolved
- permitted scientific claim: **DEVELOPMENT FEASIBILITY ONLY**

No internal/reserved set was opened.

### Future role split — PASS

Workflow run:
`36762615920`

Artifact:
- id: `11119351957`
- digest:
  `sha256:bb5aaca9505c0d6dd026cfeba14bbf9abc1eac555d0bf6b03cfd200f50007a23`

Role manifest SHA256:
`6912dac4405c5f2456c24a4268869c167beba4480c9d3d3cd193574f7cab4c12`

UID/role/cluster digest:
`85a5dcb1b26a9773ea0ef7e04bb42e8e56dde5d44f1e63fcbe54141dbcb47dfc`

Clustering:
- total clusters: **2,552**
- same-document union edges: **4,325**
- exact-duplicate union edges: **8**
- near-duplicate pairs with Jaccard >=0.90: **20**
- cluster role overlap: **0**

Role allocation:
- C_F: **1,918 records / 764 clusters**
- C_T: **2,898 records / 1,020 clusters**
- C_R: **2,072 records / 768 clusters**

Cluster fractions:
- C_F: **29.94%**
- C_T: **39.97%**
- C_R: **30.09%**

Record fractions differ because document/duplicate clusters are kept intact.

Interpretation:
**FUTURE ROLE SEPARATION ONLY / HISTORICAL INDEPENDENCE NOT RESTORED**

No feasibility metric was computed.

### Bundle contract tightened

File:
`phase2/redesign/MPSEF_BUNDLE_CONTRACT_V1.md`

Commit:
`be18311b29fd7c4c9b72739f78b52d15fdde5e80`

Primary V3 executable action space is deliberately conservative:
- KEEP
- whole P1 final pass-2 sentence
- whole P2 final sentence

No edit-level hybrid fusion in the primary measurement.

Diagnostic component edits may be used for `R_raw`, but are not executable.

This prevents gold-guided/cherry-picked decomposition from inflating primary coverage.

### Target/matching contract aligned to V3

File:
`phase2/redesign/MPSEF_TARGET_AND_MATCHING_CONTRACT_V1.md`

Commit:
`21660b6ab4a468d52789893e76ac5578df3d40de`

Primary population:
**C_F only**

Primary endpoint:
`R_joint(P1,P2)`

Primary gate:
**>=95%**

Secondary mandatory:
- R_P1
- R_P2
- R_raw
- R_raw - R_joint
- R_clean
- complete-sentence repair
- four-way reachability
- leave-one-out gains
- family metrics
- clean-sentence proposal rate
- conflicts
- candidate volume
- protected-touch accounting
- failure accounting

Claim scope:
**DEVELOPMENT FEASIBILITY / NOT INDEPENDENT GENERALIZATION EVIDENCE**

### Foundational preflight — PASS

Workflow run:
`36763150865`

Artifact:
- id: `11119532160`
- digest:
  `sha256:9e8f0ad13838a334830553fdd2b0de41cdc02849b68f0cefc7d7e20030a5a13a`

Preflight status:
**PASS**

Verified:
- all 6,888 records assigned once;
- 2,552 clusters;
- zero cluster-role overlap;
- no feasibility metric computed;
- no selector trained;
- all reserved/internal sets closed;
- protocol/contract hashes frozen.

Important:
the preflight explicitly states:
`measurement_authorized_by_preflight=false`

### Remaining blocker before any R_joint measurement

The exact MEASUREMENT runner/workflow do not yet exist and therefore cannot yet
have frozen hashes.

V3 requires the scientific measurement implementation itself to be frozen
before any metric is observed.

Therefore current state is:

**FOUNDATIONAL PREFLIGHT PASS / MEASUREMENT STILL BLOCKED**

Exact next authorized work:
1. implement source-only C_F P1 proposal runner/workflow;
2. freeze and preflight it without gold scoring;
3. implement source-only C_F P2 proposal runner/workflow;
4. freeze and preflight it without gold scoring;
5. implement the scorer/R_joint runner against the already frozen proposal artifacts;
6. freeze measurement runner/workflow hashes;
7. run a SECOND pre-measurement preflight;
8. only then make the explicit measurement authorization decision.

Do not compute R_joint before step 8.

No parallel execution.
Reserved/internal datasets remain closed.


## 36. MP-SEF P1/P2 C_F premeasurement proposal freeze

Date: 2026-09-30

### P1 C_F — FROZEN PASS

- run: `36765798233`
- artifact: `11123050529`
- artifact ZIP SHA256: `e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46`
- source manifest: **1918 records / 764 clusters**
- source manifest SHA256: `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- batch-vs-single parity: **64/64**
- changed source-only: **1838/1918 = 95.83%**
- protected touch: **19/1918 = 0.99%**
- empty outputs: **0**
- proposal SHA256: `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- lock: `phase2/redesign/MPSEF_P1_CF_PROPOSAL_LOCK_V1.md`
- R_joint: **NOT COMPUTED**

### P2 C_F — FROZEN PASS

- run: `36768378938`
- artifact: `11124303107`
- artifact ZIP SHA256: `5209633d389db02054456a42710a96a1d6e573cefca308254747897969c7d41c`
- consumed the exact same P1 C_F source manifest
- batch-vs-single parity: **32/32 all fields**
- changed source-only: **1906/1918 = 99.37%**
- protected touch: **21/1918 = 1.10%**
- empty outputs: **0**
- proposal SHA256: `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`
- lock: `phase2/redesign/MPSEF_P2_CF_PROPOSAL_LOCK_V1.md`
- R_joint: **NOT COMPUTED**

P2 step 10 ran approximately 35 minutes. The runner did emit
`P2_CF_BATCH_PROGRESS` through 1918/1918; active-log `BlobNotFound`
through the ChatGPT GitHub connector caused the apparent observability gap,
not a stalled model process.

### Current classification

**IMPROVED IMPLEMENTATION COMPLETENESS / QUALITY PERFORMANCE STILL UNMEASURED**

Both primary proposers are now frozen, source-only, parity-validated, and
anchored to the same C_F population.

### Next authorized sequence

1. prepare independent higher-model premeasurement review packet;
2. implement the frozen-artifact R_joint scorer;
3. freeze scorer/workflow hashes;
4. run second pre-measurement preflight;
5. make explicit measurement-authorization decision;
6. only then compute R_joint once.

No selector training. No INTERNAL_EVALUATION or STRESS_DIAGNOSTIC opening.
No reserved-set use.


## CHECKPOINT 2026-09-30 — MP-SEF P1/P2 C_F FROZEN; INDEPENDENT PREMEASUREMENT REVIEW READY

P1 C_F:
- run: `36765798233`
- artifact: `11123050529`
- conclusion: SUCCESS
- cases: 1,918 / 1,918
- clusters: 764
- batch/single parity: 64/64
- changed-vs-source activity: 1,838 / 1,918 = 95.83%
- protected-touch: 19 / 1,918 = 0.99%
- empty outputs: 0
- proposal SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- lock:
  `phase2/redesign/MPSEF_P1_CF_PROPOSAL_LOCK_V1.md`

P2 C_F:
- run: `36768378938`
- artifact: `11124303107`
- conclusion: SUCCESS
- cases: 1,918 / 1,918
- clusters: 764
- batch/single all-field parity: 32/32
- changed-vs-source activity: 1,906 / 1,918 = 99.37%
- protected-touch: 21 / 1,918 = 1.10%
- empty outputs: 0
- proposal SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`
- lock:
  `phase2/redesign/MPSEF_P2_CF_PROPOSAL_LOCK_V1.md`

Shared exact C_F source manifest:
`051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

P2 runtime observation:
- heavy proposal step ran approximately 35 minutes;
- emitted progress through 1,918/1,918;
- ChatGPT GitHub connector could not read active-step logs and returned `BlobNotFound`;
- this was an observability limitation, not a stalled process.

Independent review package:
`phase2/redesign/MPSEF_PREMEASUREMENT_INDEPENDENT_REVIEW_PACKAGE_V1.md`
commit:
`c18902bfb9b2a7c0c5c9ac32ce1ac2e6bf8399fb`

Higher-model review prompt:
`phase2/redesign/MPSEF_HIGHER_MODEL_REVIEW_PROMPT_V1.md`
updated after P2 freeze.

Current classification versus prior checkpoint:
**IMPROVED IMPLEMENTATION COMPLETENESS / QUALITY PERFORMANCE STILL UNMEASURED**

Important:
- `R_joint` has NOT been computed.
- selector has NOT been trained.
- reserved/internal sets remain closed.
- source-change percentages are activity only, not quality.

Exact next authorized sequence:
1. obtain independent higher-model premeasurement review;
2. resolve any BLOCKER/MAJOR findings before measurement;
3. implement gold-blind executable-action legalizer + R_joint scorer;
4. freeze legalizer/scorer/workflow hashes;
5. run second premeasurement preflight;
6. make explicit measurement authorization decision;
7. only then compute R_joint once.


## CHECKPOINT — mandatory long-process monitoring instrumentation

From this checkpoint onward, every NEW long-running ACAD_PASS process must use:

- `phase2/redesign/process_progress_v1.py`
- `phase2/redesign/run_with_progress_watchdog_v1.py`
- `phase2/redesign/ACAD_PASS_LONG_PROCESS_MONITORING_CONTRACT_V1.md`

Required live fields:
- child alive/dead;
- processed;
- total;
- percent;
- last_progress_at;
- stale_seconds;
- rate_per_min;
- ETA where meaningful;
- stage;
- final return code.

Recommended cadence:
- progress update every batch or <=60 s;
- watchdog poll every 20 s;
- external GitHub status publication every 60 s;
- default stale threshold 600 s unless process-specific evidence justifies another threshold.

For GitHub Actions long processes, prefer a narrowly scoped `statuses: write` permission and publish progress to a dedicated commit-status context so progress can be inspected while a job is running even if live job logs are unavailable.

Do not rerun already completed P1/P2 artifacts solely to add monitoring.

Classification:
**IMPROVED OPERATIONAL OBSERVABILITY / SCIENTIFIC PERFORMANCE UNCHANGED**


## CHECKPOINT 2026-10-01 — SOURCE-ONLY LEGALIZER FROZEN

Independent-review remediation status:
- F01 exposure: machine audit frozen; partial technical scorer execution occurred to 500/1918 in cancelled run; no valid final result; human recollection = UNKNOWN.
- F09 population precedence: current cycle frozen to C_F=1918/764; historical 317-record amendment does not govern this cycle.
- P2 GED provenance audit: **1,918/1,918 cases mismatch word-level morphology count vs GED-label count**; P2 frozen hypotheses are therefore source-only `EXECUTION_FAILED` for this cycle.
- source-only legalizer run: `36807189754` SUCCESS.
- artifact: `11137763396`, ZIP digest `sha256:a6d265295dfacd623057c6a4c9d5e111145c90e2670eae1c5bf8ee6bfef34152`.
- P1_OK: 1,806 / 1,918 = 94.16%.
- P1_PROTECTED_BLOCKED: 112 / 1,918 = 5.84%.
- P2_EXECUTION_FAILED: 1,918 / 1,918 = 100%.
- legal action-set SHA256:
  `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`.
- hypotheses SHA256:
  `c91195a66a687ba8acf12d1b1e51741183b28992f89681c8510cdac8fddf9e14`.
- lock:
  `phase2/redesign/MPSEF_SOURCE_ONLY_LEGALIZER_LOCK_V1.md`.
- monitoring contract proved operational: watchdog reported live progress and completed 1918/1918.

Scientific classification:
**IMPROVED METHODOLOGICAL VALIDITY / WORSENED P2 EXECUTABILITY / QUALITY PERFORMANCE STILL UNMEASURED**

Do NOT compute R_joint yet.

Exact next work:
1. fix scorer F06/F07/F10;
2. scorer must read frozen legal action sets and never call legality with gold;
3. freeze target-scope/family rules and evaluation-vs-execution alignment boundary;
4. strengthen run guards/hashes (F08);
5. execute synthetic-only second preflight;
6. explicit authorization review only after all mandatory checks pass.


## CHECKPOINT 2026-10-01 — DIAGNOSTIC EVIDENCE FROZEN / SCORER V2 STARTED

Corrected target/evaluation core:
- `phase2/redesign/mpsef_rjoint_core_v2.py`
- fixes punctuation set bug (`a/m/p` no longer punctuation);
- preserves mixed punctuation+linguistic targets;
- classifies `ياولد -> يا ولد،` as mixed + SPLIT;
- explicitly labels gold-aware M2 alignment as evaluation-only.

Source-only diagnostic evidence:
- run: `36807629220` SUCCESS
- artifact: `11138426729`
- ZIP digest: `sha256:e27bee3c9690fb1794b413d8a9ab5d5134f4f3d0cd8da5bc3350e525a9c6e33b`
- records: 3,836
- components: 43,207
- diagnostic JSONL SHA256:
  `2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e`
- gold/reference: false
- executable actions created: false
- R_raw/R_joint: not computed
- lock:
  `phase2/redesign/MPSEF_DIAGNOSTIC_COMPONENTS_LOCK_V1.md`

Current frozen source-only inputs for corrected scorer:
1. C_F source manifest;
2. P1/P2 proposal artifacts;
3. executable action sets SHA256
   `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`;
4. hypothesis-state artifact SHA256
   `c91195a66a687ba8acf12d1b1e51741183b28992f89681c8510cdac8fddf9e14`;
5. diagnostic components SHA256
   `2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e`.

R_joint remains BLOCKED.

Exact next step:
implement `mpsef_rjoint_score_v2.py` so it consumes frozen action sets and never recomputes legality; implement denominator-safe target construction, scoring-failure INVALID semantics, R_clean/complete-repair accounting, and a diagnostic-only R_raw matcher against the frozen diagnostic artifact; then synthetic-only preflight before any project gold measurement.


## CHECKPOINT 2026-10-01 — CORRECTED MP-SEF PRE-AUTHORIZATION STACK READY

Independent review remediation has progressed from `MODIFY BEFORE SECOND PREFLIGHT` to a corrected stack ready for the actual Second Premeasurement Preflight V2.

### Exposure / population

- V1 measurement attempt history is frozen in:
  `phase2/redesign/MPSEF_MEASUREMENT_EXPOSURE_AUDIT_V1.md`
- cancelled technical attempt reached scorer progress 500/1918; no valid final result exists.
- operator exposure recollection is explicitly UNKNOWN:
  `phase2/redesign/MPSEF_OPERATOR_EXPOSURE_ATTESTATION_V1.md`
- governing population remains C_F=1918/764:
  `phase2/redesign/MPSEF_POPULATION_PRECEDENCE_DECISION_V1.md`

### P2 provenance

Frozen P2 is non-executable in the corrected cycle:
- 1918/1918 rows have morphology-word / GED-label count mismatch;
- all P2 hypotheses are source-only `EXECUTION_FAILED:GED_WORD_ALIGNMENT_MISMATCH`;
- P2 frozen output text is retained historically and is NOT regenerated/rescued.

Audit:
`phase2/redesign/MPSEF_P2_GED_WORD_ALIGNMENT_PROVENANCE_AUDIT_V1.md`

### Final source-only executable actions

Legalizer V1R1:
- run: `36808497947`
- artifact: `11138269108`
- digest: `sha256:97f60f7d8147dd8cc5378df94a2b506d790086146395720e631c771d0db4fee1`
- P1_OK=1806
- P1_PROTECTED_BLOCKED=112
- P2_EXECUTION_FAILED=1918
- executable action-set SHA256:
  `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`
- hypothesis audit SHA256:
  `b4736383019d017780a8bfe4b076a0cd742e71bccfbb50350da8fa59b7c9ac75`
- legalizer code SHA256:
  `f17af03343490f6edba59693babed9ec65c992309eec5a3b32dd68d9b9969686`

Lock:
`phase2/redesign/MPSEF_SOURCE_ONLY_LEGALIZER_LOCK_V1R1.md`

### Frozen diagnostic evidence

- diagnostic components SHA256:
  `2490a6f924d06cbc8240c1396763151d9cbbc4ed172a1de7f4876e56842f491e`
- records: 3836
- components: 43207
- executable=false
- gold=false

Lock:
`phase2/redesign/MPSEF_DIAGNOSTIC_COMPONENTS_LOCK_V1.md`

### Corrected scorer stack

Final synthetic preflight:
- run: `36809271706`
- artifact: `11138601773`
- digest: `sha256:245cab3d87e2f2960fcc4ce72b1a3575b31687b6397b3046558a79c7939c388c`

Final hashes:
- `mpsef_rjoint_core_v2.py`:
  `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`
- `mpsef_rjoint_score_v2.py`:
  `948e7db182237b2af93b08f31ba9677b2c7cff83f284072d0ed2697039e41ead`

Scorer V2:
- rejects punctuation-classifier bug;
- rejects no-op and multiple-reference targets;
- rejects duplicate target credit;
- uses whole-action oracle only;
- scoring failures produce [L,U], not known zero;
- reports R_clean, complete repair, family/macro intervals, weak-family routes, per-sentence audit, candidate-size stats;
- R_raw remains diagnostic-only;
- project measurement CLI is disabled.

Lock:
`phase2/redesign/MPSEF_SCORER_V2_FINAL_SYNTHETIC_PREFLIGHT_LOCK.md`

### One-shot measurement guard architecture

Frozen experiment ID:
`MPSEF-RJOINT-V2-CF1918-20261001-A`

Files:
- `phase2/redesign/MPSEF_RJOINT_EXPERIMENT_ID_V2.json`
- `phase2/redesign/mpsef_measurement_guard_v2.py`
- `phase2/redesign/mpsef_cf_gold_projection_v2.py`
- `phase2/redesign/mpsef_rjoint_measurement_v2.py`
- `.github/workflows/phase2-mpsef-rjoint-measurement-v2.yml`

One-shot sequence:
1. read authorization + independent review from trigger commit;
2. require diff from frozen code commit to contain exactly corrected review + authorization;
3. checkout exact second-preflight code commit;
4. validate second-preflight summary SHA;
5. validate implementation/contract hashes;
6. verify source-only artifacts;
7. rerun all non-gold smoke tests;
8. write durable `acad-pass/mpsef-rjoint-v2-consumed` status;
9. only then permit project gold download;
10. cancelled/failed after claim = permanently consumed; no rerun.

Measurement runner has a frozen 60-second per-action scorer timeout.
A timeout becomes scoring uncertainty and [L,U], not known-zero.
Long-process progress is published without metric values.

### Corrected independent review gate

Prepared BEFORE second preflight:
- `phase2/redesign/MPSEF_CORRECTED_PREAUTH_REVIEW_PACKAGE_V2.md`
- `phase2/redesign/MPSEF_HIGHER_MODEL_CORRECTED_REVIEW_PROMPT_V2.md`
- `phase2/redesign/MPSEF_RJOINT_MEASUREMENT_AUTHORIZATION_V2_TEMPLATE.json`

Required independent-review GO line:
`DECISION: GO TO MEASUREMENT AUTHORIZATION`

Actual authorization remains nonexistent and measurement remains unauthorized.

### C01-C22

Machine-checkable implementation:
`phase2/redesign/mpsef_second_preflight_checks_v2.py`

The next and only authorized execution is:
**Second Premeasurement Preflight V2, synthetic/source-only, with no project gold and no metric.**

After a PASS:
- make NO repository code/doc changes;
- give exact code commit + run ID to the higher model;
- if verdict is MODIFY/STOP, do not authorize;
- if and only if verdict is GO, commit the exact review report, then create the active authorization as the only other diff;
- measurement still occurs only through the one-shot guarded workflow.

Current classification:
**IMPROVED METHODOLOGICAL VALIDITY / P2 EXECUTABILITY WORSENED TO ZERO / CORRECTED QUALITY PERFORMANCE STILL UNMEASURED**


### Corrected matching contracts added before Second Preflight

Governing corrected-cycle files:
- `phase2/redesign/MPSEF_TARGET_FAMILY_MAP_V2.md`
- `phase2/redesign/MPSEF_TARGET_AND_MATCHING_CONTRACT_V2_AMENDMENT.md`

Key freeze:
- punctuation-only classification preserves lexical token-boundary changes;
- `m -> a!` and `ياولد -> يا ولد،` cannot disappear from the linguistic denominator;
- execution/legalization alignment is source-only;
- diagnostic decomposition is source-only;
- official M2 gold-aware path selection is permitted only inside evaluation of an already frozen whole action;
- evaluation matching cannot mutate legality, actions, diagnostic evidence, protection, or denominator;
- scoring failure yields [L,U], not known zero.

These files must be included in Second Preflight contract hashes.


## 2026-10-01 — MP-SEF source-only legality checkpoint

Independent premeasurement review remediation progressed without running R_joint.

Frozen evidence:
- operator exposure status: UNKNOWN / insufficient recollection
- C_F precedence remains 1918 cases / 764 clusters
- P2 generation trace reproduced 1918/1918 frozen outputs exactly
- P2 GED word-label alignment mismatch: 1918/1918 cases
- P2 total dropped GED predictions from zip behavior: 30,341
- P2 generation-ceiling cases: 24
- P2 missing terminal EOS cases: 0

Gold-blind executable-action legalizer run:
- workflow run: 36818173661
- P1_OK = 1806
- P1_PROTECTED_BLOCKED = 112
- P2_EXECUTION_FAILED = 1918
- hypotheses = 3836
- action sets = 1918
- hypotheses SHA256 = a54c1bcd38c9d34d389054cb125878be92bc9e603f062621e6d44a627037dc4f
- action sets SHA256 = 6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a

Legalizer lock:
- phase2/redesign/MPSEF_EXECUTABLE_ACTIONS_LOCK_V1.md
- commit 1127968ee97693d3bdc188378ed4e8fb3ff92970

Current scientific status:
IMPROVED SUBSTANTIALLY IN METHODOLOGICAL SAFETY / WORSENED IN AVAILABLE P2 COVERAGE.

Do NOT run R_joint yet.
Next sequence:
1. Correct scorer according to S01-S12.
2. Rebuild second preflight C01-C22 around immutable executable-action artifacts.
3. Independent re-review / explicit authorization.
4. Only then allow any gold-aware measurement.

Long-process monitoring now includes adaptive ETA, predicted finish timestamp, EWMA rate, confidence, and stale detection for future runs.


## 2026-10-01 — Maximum-quality reassessment rule

Permanent governance rule frozen in:
`phase2/redesign/ACAD_PASS_MAXIMUM_QUALITY_REASSESSMENT_CONTRACT_V1.md`
commit:
`06637217759810726adead618bf5b199743913dd`

Project objective is the strongest scientifically defensible ACAD_PASS system, not preservation of the current architecture.

Earlier phases/processes/models may be revisited, repaired, replaced, removed, or redesigned whenever new evidence justifies it, but frozen evidence must remain immutable and redesign must occur in a new explicit versioned lane.

Current strategic implication:
- frozen P2 remains blocked in the current cycle;
- P2 failure is implementation/provenance, not proven linguistic-quality failure;
- P2_V2 or a replacement/complementary proposer is allowed and should be evaluated before spending additional gold-aware measurement exposure if it can materially strengthen candidate coverage;
- completing Second Preflight remains useful as a clean baseline and engineering proof;
- SECOND_PREFLIGHT_PASS must NOT automatically authorize R_joint;
- before any new gold-aware measurement, perform an architecture re-baseline decision using the frozen evidence and P2 repair/replacement alternatives.

Higher-model independent review is recommended:
1. after Second Preflight remediation is stable and before gold-aware authorization;
2. before committing to major P2_V2/replacement architecture;
3. after any future material metric failure before patch-vs-rebaseline decision.

All future FAIL/BLOCKED/PARTIAL outcomes require root-cause and repairability analysis rather than result-only interpretation.


## 2026-10-01 — Canonical system-evolution ledger created

A permanent historical/scientific ledger now exists:

`ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md`

Creation commit:
`3826bd27f4a22716330e981334bffa2ae023393c`

Purpose:
- preserve the full ACAD_PASS evolution, including successful and failed paths, quantitative metrics, decision rationales, root causes, repairability, superseded conclusions, architecture pivots, and frozen evidence;
- support future system-wide re-baselining when stronger methods/models become available;
- preserve a research-grade history that can later support paper/thesis/dissertation assessment.

Permanent maintenance rule:
- after every meaningful checkpoint, update BOTH:
  1. `RESUME_HERE.md` for current operational truth and exact next step;
  2. `ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md` for historical/scientific chronology.
- never erase historical negative evidence; supersede it explicitly.
- record percentages only when measured/computable; otherwise write NOT QUANTIFIED.
- include WHY a path was chosen, WHY it failed/succeeded, and whether it is repairable/current-cycle-safe.

The ledger also contains a dedicated Research / Doctoral-Dissertation Conversion Map.
