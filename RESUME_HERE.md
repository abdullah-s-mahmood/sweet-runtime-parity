# RESUME HERE — ACAD_PASS / English-First / AT0-EN

## 0. Resume maintenance policy

This file is the canonical live handoff. Update it after every meaningful checkpoint: successful workflow, scientifically relevant failure, architecture/gate decision, frozen hash/manifest, or change in the exact next authorized step. Do not update it for trivial status polls that add no new state.


**Canonical handoff state date:** 2026-10-03  
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


## 2026-10-01 — Advanced Second Preflight V2 revalidation PASS

Current hardened HEAD was revalidated with the advanced machine-checkable C01-C22 suite.

Workflow:
- `Phase 2 MP-SEF R_joint Second Premeasurement Preflight v2`
- run: `36825797396`
- code commit: `7c31da92a75495f11e1faac10ecc4e84685845c3`
- artifact: `11145072418`
- artifact digest:
  `sha256:fcd653251e4e6870adfdcfb26d71e2bfa8f11f14e6f15b040f054077cb008896`

Result:
- C01-C22: **22 / 22 PASS = 100%**
- checklist SHA256:
  `3103089eaa04576816509b8f2940c721ed8a931c1f4a7a6802b1e86a0b301eb8`
- project gold loaded: false
- project metric computed: false
- measurement authorized by preflight: false
- next gate:
  `INDEPENDENT_CORRECTED_PREAUTH_REVIEW`

Historical baseline:
- earlier simplified second-preflight baseline: strict PASS 36.36%, weighted remediation 65.91%.
- that baseline is now SUPERSEDED for current readiness by the advanced 22/22 suite, but remains preserved as historical evidence of remediation progress.

Current interpretation:
**IMPROVED SUBSTANTIALLY IN PREAUTHORIZATION READINESS / 100% C01-C22 SOURCE-ONLY PREFLIGHT PASS / PERFORMANCE STILL UNMEASURED**

Do NOT run R_joint automatically.
Per the Maximum-Quality Reassessment Contract, the next work is:
1. architecture re-baseline using frozen evidence, especially current P2=0 executable;
2. prepare independent higher-model corrected preauthorization/architecture review;
3. decide KEEP / REPAIR P2_V2 / REPLACE / ADD COMPLEMENT;
4. only after that decision consider any gold-aware authorization.


## 2026-10-01 — Arabic correction architecture re-baseline V1

Fresh literature + implementation review completed before any new gold-aware measurement.

Decision:
- keep frozen V3 as immutable control;
- do NOT spend new gold merely to finish the current effective P1-only cycle;
- build a new versioned redesign lane;
- P2 is NOT abandoned;
- implement P2_V2 with corrected wordpiece→word GED alignment and full source-only provenance;
- add P3_V1 using a strong reproducible iterative/cascaded SWEET variant;
- consider MP-SEF V4 source-only consensus/edit voting only as a NEW architecture, never as a retroactive modification to V3;
- general LLMs remain diagnostic/optional diversity candidates, not sole primary corrector/verifier.

Re-baseline document:
`phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_REBASELINE_V1.md`

Commit:
`2204718b51f9580a6d4d8ddaa33a903f686eb262`

Scientific classification:
**IMPROVED STRATEGICALLY / PERFORMANCE NOT YET MEASURED**

Current exact next sequence:
1. freeze P2_V2 implementation specification;
2. freeze P3_V1 SWEET iterative/cascade specification;
3. freeze source-only proposer-diversity protocol;
4. independent higher-model architecture review;
5. implement only after review unless review says MODIFY/STOP;
6. no new R_joint before the redesign decision is frozen.


## 2026-10-01 — Proposer redesign specs frozen / higher-model review required

Architecture re-baseline has now been translated into source-only implementation specs.

P2_V2:
- spec: `phase2/redesign/MPSEF_P2_V2_IMPLEMENTATION_SPEC.md`
- commit: `5e34e8e75dd3ef1e930d3d2b6528e7f79b709932`
- new-version repair only;
- first-wordpiece/ignore-index GED word alignment;
- no zip truncation;
- no gold.

P3_V1:
- spec: `phase2/redesign/MPSEF_P3_V1_SWEET_PNX_CASCADE_SPEC.md`
- commit: `73ae1bee99c866dec8b91affd7f50c5465f36082`
- current P1 is already SWEET NoPnx ×2;
- P3 therefore adds exactly one SWEET-Pnx pass:
  `NoPnx×2 -> Pnx×1`.

Source-only diversity protocol:
- `phase2/redesign/MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V1.md`
- commit: `5e0ad432b513bd65daa567cdc2e046c9d18996dd`

Independent architecture review package:
- `phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_INDEPENDENT_REVIEW_PACKAGE_V1.md`
- commit: `43c8a4ad27b76f3715e723e77a80f737ba330829`

Higher-model prompt:
- `phase2/redesign/ACAD_PASS_HIGHER_MODEL_ARCHITECTURE_REVIEW_PROMPT_V1.md`
- commit: `f091590971954bedb3efaaaf27627ee344f86878`

Review target architecture snapshot:
`5e0ad432b513bd65daa567cdc2e046c9d18996dd`

Current exact state:
- advanced Second Preflight = 22/22 PASS;
- frozen V3 remains immutable control;
- current P2 remains non-executable;
- no new R_joint;
- no new project gold;
- no proposer prototype should advance beyond synthetic/source-only design until independent architecture review.

Next action:
obtain independent higher-model architecture review using the prepared package/prompt.


## 2026-10-01 — Independent review remediation / Stage0 PASS

Independent review verdict:
**MODIFY BEFORE IMPLEMENTATION**

Review lock:
`phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_INDEPENDENT_REVIEW_LOCK_V1.md`

Current finding status:

- B01 P2 word/wordpiece/label identity: DESIGN CLOSED + synthetic Stage0 PASS
- B02 new proposer/action-set registry isolation: DESIGN CLOSED
- M01 P3 optional same-family role: DESIGN CLOSED
- M02 diversity denominators/packet/budget: DESIGN CLOSED
- M03 protection overblocking: shadow diagnostic contract ready; frozen policy unchanged
- M04 all-actions-fail scorer bounds: fixed in scorer V3; synthetic PASS
- M05 combined BOUNDARY whole-action aggregation: fixed in scorer V3; synthetic PASS

Key files:
- `MPSEF_P2_V2_WORD_IDENTITY_CONTRACT_V1.md`
- `MPSEF_V4_CANDIDATE_REGISTRY_ACTIONSET_CONTRACT_V1.md`
- `MPSEF_P3_V1_ROLE_INDEPENDENCE_AMENDMENT_V2.md`
- `MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md`
- `ACAD_PASS_PROTECTED_LINKAGE_SHADOW_DIAGNOSTIC_V1.md`
- `mpsef_rjoint_score_v3.py`
- `mpsef_p2_v2_identity_stage0.py`

Scorer V3 synthetic run:
- run `36863251498`
- SUCCESS
- artifact digest `sha256:d051f6c4a93543f7d23cb07c36c711fc3de7197137e5d7b6b2dc334f07030982`

P2_V2 Stage0 source-free run:
- run `36863549449`
- SUCCESS
- artifact digest `sha256:c6a875b7880db119ea660ea84a47c250f49f624d610b4849419e2fd5aa5893e8`
- project source loaded=false
- project gold loaded=false
- project metric computed=false
- real model inference=false

Stage 1 has NOT started.

Exact next gate:
focused independent closure review of B01/B02/M01/M02 + Stage0 evidence.
Only after GO may deterministic 128-UID / 128-cluster source-only Stage 1 run.


## 2026-10-01 — Architecture review remediation checkpoint

Independent higher-model verdict:
**MODIFY BEFORE IMPLEMENTATION**

Findings:
- 2 BLOCKER
- 5 MAJOR
- 2 MINOR

Review lock:
`phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_INDEPENDENT_REVIEW_LOCK_V1.md`
commit `ab142dd90e0c600fa11de5650b2ab15eeb5fcc7b`

Closed design items:
- B01: `MPSEF_P2_V2_WORD_IDENTITY_CONTRACT_V1.md`
  commit `0d32f7ff4fb75aa98ec67c92b291597ebb406faa`
- B02: `MPSEF_V4_PROPOSER_REGISTRY_ACTION_SET_CONTRACT_V1.md`
  commit `5466e6b9e64235c34db44355d57b638206b9a939`
- M01: `MPSEF_P3_V1_ROLE_AMENDMENT_V2.md`
  commit `b2f56fee86666100ce5e9690a8fe6057228cfde0`
- M02: `MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md`
  commit `88077f47090041a61dfab8caf1df459b5bf3cc68`
- M03: `MPSEF_PROTECTION_SHADOW_DIAGNOSTIC_CONTRACT_V1.md`
  commit `fb4cf91396e1ef584b60177a6ad870862df05105`

Current exact next work:
1. fix M04 in scorer: all-actions-fail must preserve frozen target-count uncertainty [0,N], never collapse to [0,0];
2. fix M05: BOUNDARY group must maximize one whole action over SPLIT∪MERGE, not sum separate maxima;
3. add synthetic regressions for both;
4. version scorer/preflight accordingly;
5. no Stage1/Stage2/gold until required predecessor gates are satisfied.


## 2026-10-01 — Independent architecture review remediation checkpoint: B01/B02/M01/M02/M03 design + M04/M05 synthetic closure

Independent review verdict remains:
**MODIFY BEFORE IMPLEMENTATION**

Completed source-only design remediation:
- B01: strict P2_V2 word/wordpiece/label identity contract frozen.
- B02: new versioned proposer registry/action-set contract frozen; V3 tooling cannot be silently reused.
- M01: P3 role amended to optional P1-family punctuation/full-correction cascade; not independent support.
- M02: diversity protocol V2 freezes 128-UID/128-cluster Stage 1 packet design, named denominators, marginal legal contribution, resource accounting, parity and retention semantics.
- M03: shadow protection diagnostics contract frozen; V3 protection remains authoritative and unchanged.

M04/M05:
- scorer V3 implementation commit:
  `7a01d797e5fd630186910e38f5487364639e8165`
- synthetic preflight run:
  `36867448366`
- result: SUCCESS / self_test PASS
- artifact:
  `11164975245`
- artifact digest:
  `sha256:1ed7076c272e66dfe1b4168568113d76c4294db863418352af210ffaae90bb65`
- lock:
  `phase2/redesign/MPSEF_SCORER_V3_M04_M05_SYNTHETIC_LOCK.md`

M04 fix:
all-actions scoring failure with N targets preserves [0,N], never invented exact [0,0].

M05 fix:
BOUNDARY SPLIT/MERGE group scoring and additional-target/cluster evidence use one whole action per sentence, never sum maxima from different actions.

Current state:
- no new project gold;
- no R_joint;
- no Stage 1;
- V3 historical artifacts unchanged.

Next safe sequence:
1. implement Stage 0 source-only synthetic harness for B01/B02/M01/M03 contracts;
2. run Stage 0 until genuine PASS;
3. materialize and freeze deterministic Stage 1 packet only after Stage 0 PASS;
4. do not run Stage 1 before that.


## 2026-10-01 — P2_V2 B01 source-free Stage0 CLOSED PASS

B01 implementation validation is now closed at source-free Stage0.

Synthetic identity Stage0:
- run: `36863549449`
- 20 / 20 tests PASS
- project source: false
- project gold: false
- artifact: `11162862266`
- digest: `sha256:c6a875b7880db119ea660ea84a47c250f49f624d610b4849419e2fd5aa5893e8`

Historical real-model Stage0 failure:
- run: `36864163724`
- cause: non-standard `BertTokenizerFast.cls_token_type_id` assumption
- class: IMPLEMENTATION / RUNTIME INTERFACE
- not a linguistic-quality failure
- triage: `MPSEF_P2_V2_REAL_MODEL_STAGE0_FAILURE_TRIAGE_V1.md`

Repair:
- commit: `fe49ac916d7534b7178a3f0a87092da8b0dccad5`

Real-model Stage0 after repair:
- run: `36868057043`
- PASS
- synthetic/public sources: 3
- repeat parity: true
- project source loaded: false
- project gold loaded: false
- project metric computed: false
- real model inference: true
- quality claimed: false
- artifact: `11165486137`
- digest: `sha256:9cdb16ad4f3606b2af158e296a7e59e24f3718aec18d8cbc174acfa4a2d50918`

Frozen model weights:
- GED SHA256: `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`
- GEC SHA256: `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`

Closure lock:
`phase2/redesign/MPSEF_P2_V2_B01_STAGE0_CLOSURE_LOCK_V1.md`

Interpretation:
- B01 Stage0: PASS
- original P2_V1 universal GED word-alignment defect is not present in the tested P2_V2 Stage0 path
- no linguistic/correctness claim is made.

Next:
B02/M01/M03 source-free Stage0 synthetic closure, then fresh research + architecture brainstorming before any Stage1.


## 2026-10-01 — V4 source-free Stage0 COMPLETE PASS / research gate before Stage1

Canonical closure:
`phase2/redesign/MPSEF_V4_PRE_STAGE1_STAGE0_CLOSURE_LOCK_V1.md`

Current evidence:
- B01 synthetic: 20/20 PASS.
- B01 real-model source-free: PASS.
- B02: 17/17 PASS.
- M01: 4/4 PASS.
- M03: 10/10 PASS.
- M04/M05 scorer-v3 synthetic preflight: PASS.
- final B02/M01/M03 fail-closed run: `36869672029`.
- artifact: `11164888387`.
- digest:
  `sha256:7efc253149097073929baeec7a6b69f05eb94dcfb9405dfb7033083a83d8ba4f`.

No project source was loaded by these Stage0 gates.
No new project gold/reference.
No R_joint.
No Stage1 packet materialized.
No Stage1 execution.

Current classification:
**IMPROVED STRONGLY IN IMPLEMENTATION/PROVENANCE READINESS / PERFORMANCE UNMEASURED**

Mandatory next gate:
fresh deep research + maximum-effort architecture brainstorming before Stage1.
The research must reassess P1/P2_V2/P3/V4 and may recommend KEEP/REPAIR/REPLACE/ADD/DEFER.
Stage1 is forbidden until that decision is frozen.


## 2026-10-01 — Fresh pre-Stage1 research re-baseline V2 frozen

Research document:
`phase2/redesign/ACAD_PASS_PRE_STAGE1_FRESH_RESEARCH_REBASELINE_V2.md`

Commit:
`b2dd28366c3810af845831e976e8270b62c93439`

Fresh 2025-2026 research + maximum-effort architecture brainstorming completed after full source-free Stage0 PASS.

Frozen decisions:

- P1_CONTROL: KEEP.
- P2_V2: KEEP / PROCEED TO STAGE1.
- P3_V1: KEEP AS OPTIONAL / PROCEED TO STAGE1.
- P1 and P3 remain one SWEET family for future support-count interpretation.
- P4: DEFER before Stage1; reopen if source-only diversity proves a third independent family is needed.
- V4 consensus: DEFER until after Stage1.
- learned selector: DEFER.
- general LLM proposer: DEFER from primary roster; diagnostic/reviewer role only.
- protection: KEEP authoritative current policy + source-only shadow diagnostics.
- future evaluation: keep whole-action R_joint primary; newer metrics may be supplemental only.

Key architecture insight:
the current roster has only TWO materially independent families:
1. SWEET;
2. Seq2Seq+GED/morphology.

Therefore P1+P3 MUST NOT be counted as two votes in any future consensus.
A meaningful family-majority consensus may require a third independent family later.

Stage1 is now justified because it can answer source-only questions that external literature cannot:
- P2_V2 legal marginal diversity vs P1;
- P3 marginal value vs redundancy;
- candidate-set-size gain;
- protection burden;
- global-ordinal-only shadow blocking;
- runtime/provenance cost.

Current classification:
**IMPROVED ARCHITECTURALLY / LINGUISTIC PERFORMANCE STILL UNMEASURED**

Engineering forecast:
- ~90% optimism that a scientifically defensible architecture can be reached;
- ~10% residual architecture/implementation risk.
These are engineering estimates, not statistical/model-quality probabilities.

Main current risks:
- P2_V2 may add little legal diversity;
- P3 may be mostly redundant;
- current roster may need P4 before consensus;
- protection may constrain useful availability;
- Stage1 may expose runtime/provenance defects.

Next exact sequence:
1. freeze deterministic 128-UID / 128-cluster Stage1 source-only packet;
2. inspect/implement P2_V2 Stage1 runner;
3. inspect/implement P3 Stage1 runner using exact P1 parent outputs;
4. freeze generic V4 action builder;
5. integrate M03 shadow diagnostics + progress/resource monitoring;
6. run Stage1 source-only only.


## 2026-10-01 — V4 Stage1 packet frozen

Workflow run:
`36871466394`

Packet:
- 128 UIDs
- 128 clusters
- exactly one selected UID per cluster

Frozen identities:
- source manifest:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- registry:
  `b448650c571f6c93dffe4825417e4f65d6a8cd02e33bd9551728ceac2b242b1a`
- packet:
  `8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1`
- UID list:
  `e32b468f27653a1bbabfa5c355483c34ffe9b6e4cb2425c36e6c10b714c104ac`
- cluster list:
  `95b895d424d404d80a70b5acb8ac8b98fe8b461f8b03c2532a7535853f9a25ca`
- source-row hashes:
  `5b7f9abc05d4bbfb9a6a336aca1fadd6767fc0dc3a597fdcaed1ad01244a2b29`

Artifact:
- `11167360791`
- digest:
  `sha256:64284a4187b1bda2e61dd1a2a5a20752f6791c14b8709a5ffb2aeee2e53dcaac`

No proposer output influenced selection.
No reference/gold.
No quality metric/R_joint.
No selector training.

Lock:
`phase2/redesign/MPSEF_V4_STAGE1_PACKET_LOCK_V1.md`

Next:
build/freeze P2_V2 Stage1 source-only runner from the source-free real-model PASS path.


## 2026-10-01 — P2_V2 Stage1 source-only COMPLETE

Run:
`36872617551`

Artifact:
`11168548251`

Artifact digest:
`sha256:050d376b98ecf0b0be2c9ff49610d1d67834fa4f0839b02ab344f828f6d82ce9`

Results:
- monitored work: 152/152 = 100%
- OK: 127/128 = 99.21875%
- non-executable: 1/128 = 0.78125%
- changed vs source: 126/128 = 98.4375% (activity only, not correctness)
- empty output: 0
- repeat parity: 8/8
- reversed-order parity: 8/8
- true batch-vs-single: N/A; no batched model-call path exists in V1
- main proposal runtime: 581.313 s (~9.69 min)
- mean: 4.540 s/case
- median: 4.536 s/case
- p95: 5.535 s/case
- peak RSS: ~2.51 GiB

Single failure:
- UID `train:12118`
- `GEC_EOS_AT_GENERATION_CEILING_FAIL_CLOSED`
- class: CAPACITY / GENERATION-COMPLETENESS BOUNDARY
- repairability: FIXABLE_NEXT_VERSION_ONLY
- preserved non-executable in V1.

No gold/reference, no quality metric, no R_joint, no selector training.

Lock:
`phase2/redesign/MPSEF_P2_V2_STAGE1_RESULT_LOCK_V1.md`

Next:
P3 source-only Stage1 using exact P1 parent outputs on the same frozen 128-case packet.


## 2026-10-01 — P3_V1 Stage1 source-only COMPLETE

Successful run:
`36877195995`

Artifact:
`11169788003`

Artifact digest:
`sha256:57dc36332f24df3e3bf09367f8ca0a1a99e998dd4c6939fe6bc7bbbb3093ab5e`

Results:
- monitored work: 144/144 = 100%
- execution OK: 128/128 = 100%
- batch-vs-single parity: 8/8
- exact frozen P1 parent reused: true
- P1 rerun: false
- identical to P1: 6/128 = 4.6875%
- changed from P1: 122/128 = 95.3125%

Stage-B domain relative to P1:
- MIXED_FROM_P1: 118/128 = 92.1875%
- PUNCTUATION_ONLY_FROM_P1: 4/128 = 3.125%
- NO_CHANGE_FROM_P1: 6/128 = 4.6875%

Main 128-case Pnx pass:
- 22.186 s total
- ~0.157 s/case allocated median
- p95 ~0.166 s
- peak RSS ~1.30 GiB

Historical failed attempt:
- run `36876431628`
- 0/144 inference
- runtime dependency parity defect
- repaired by restoring frozen P1 dependency stack.

No gold/reference, no quality metric, no R_joint, no selector training.

Architecture signal:
P3 is mostly MIXED relative to P1 rather than punctuation-only on this packet. This is not a correctness judgment; it makes legal/protection/marginal-diversity analysis mandatory before retention.

Next:
V4 source-only legal/dedup/diversity analysis over P1/P2_V2/P3.


## 2026-10-01 — V4 Stage1 PROTOCOL COMPLETE

Stage1 source-only packet and proposer execution are now protocol-complete.

Parity32 manifest:
- SHA: `384f1a6d08f79c6a9d73dc4298f1a1fac245d9f43bed2e77a5395cc1a2f4711e`
- run: `36878829104`
- artifact: `11170650411`

Parity remediation:
- P1: 32/32 PASS — run `36879926916`
- P2_V2: 32/32 PASS — run `36880639044`
- P3_V1: 32/32 PASS — run `36882627604`

P1 artifact:
`11170907081`
digest `eab2ac1854de3bff1858c9c09e23b3a1c212ec1b50af33fd4755053f3b8d189d`

P2 artifact:
`11170904136`
digest `7da2451dd06e7d9e6221f6614cbda8127c6fe7666c974999a4b0f6542810362d`

P3 artifact:
`11171344349`
digest `55bad830353501a139b85d920c70cdd6be6920e10257c4a286691258d4da88e4`

Stage1 legality/dedup/diversity:
- analysis run `36878256574`
- artifact `11170390314`
- P1 legal 120/128
- P2 legal 122/128
- P3 legal 119/128
- unique legal contribution P1/P2/P3 = 101/115/111 UIDs
- non-KEEP legal candidate on 123/128
- 98/128 have 4 unique actions including KEEP.

Important:
P3 Stage-B is mostly MIXED_FROM_P1 (118/128), not punctuation-only.

No gold/reference, no R_joint, no selector training.

Stage1 classification:
**IMPROVED STRONGLY / PROTOCOL COMPLETE / LINGUISTIC QUALITY UNMEASURED**

Next:
fresh post-Stage1 research + maximum-effort brainstorming before any Stage2/P4/V4 consensus authorization.


## 2026-10-01 — Post-Stage1 fresh research / P4 decision

Frozen record:
`phase2/redesign/ACAD_PASS_POST_STAGE1_FRESH_RESEARCH_REBASELINE_V1.md`

Decision:
- P4 before Stage2: **DEFER**
- current roster: **SUFFICIENT FOR SOURCE-ONLY FULL-C_F STAGE2**
- Stage2: **AUTHORIZED SOURCE-ONLY ONLY**
- family-consensus activation: **DEFER**
- gold/reference: **NOT AUTHORIZED**
- R_joint: **NOT AUTHORIZED**
- learned selector: **NOT AUTHORIZED**

Fresh audit did not find a third-family Arabic GEC system that simultaneously has a trained public checkpoint, reproducible inference, freezeable provenance, and low integration debt.

MTAGEC/AraT5/ByT5/mT5 remain P4 candidates, but not immediate roster members.

The 2026 ZAEBUC Arabic GEC release uses CAMeLBERT GED + AraBART GEC and is therefore the same independent-family lineage as P2, not a P4.

P1 and P3 remain one SWEET family for future family-support logic.

Next:
freeze Stage2 source-only full-C_F execution contract before any execution.


## 2026-10-01 — Stage2 contract frozen for adversarial review

New frozen-for-review contract:
`phase2/redesign/MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1.md`

Higher-model review packet:
`phase2/redesign/ACAD_PASS_STAGE2_HIGHER_MODEL_REVIEW_PACKET_V1.md`

Stage2 has NOT started.

New preregistered additions:
- reuse exact frozen P1 full-C_F artifact; do not rerun P1;
- Stage2 P2/P3 runner must replay exact frozen Parity32 before 1,918-case execution;
- family-aware source-only diagnostics;
- P1+P3 count as one SWEET family;
- P2 240-minute CPU budget based on Stage1 scaling;
- P4 review mandatory after Stage2;
- gold/R_joint/selector/LLM-judge remain forbidden.

Current state:
**STAGE2 CONTRACT FROZEN / AWAITING ADVERSARIAL HIGHER-MODEL REVIEW / NO FULL-C_F EXECUTION YET**


## 2026-10-01 — Higher-model Stage2 review resolved

Higher-model verdict:
**MODIFY**

Accepted:
- 0 BLOCKER
- M01 production-bound replay
- M02 P2 partial failure evidence
- M03 family leave-one-out + frozen Stage-B classifier
- M04 watchdog/process-tree/partial-artifact semantics
- N01 overlapping cluster-presence bins
- N02 runtime/burden eligibility

Frozen amendment:
`MPSEF_V4_STAGE2_SOURCE_ONLY_FULL_CF_EXECUTION_CONTRACT_V1_AMENDMENT_A1.md`

Resolution lock:
`ACAD_PASS_STAGE2_HIGHER_MODEL_REVIEW_RESOLUTION_LOCK_V1.md`

P4 remains DEFER.
P2 budget remains 240 min.
P3 budget remains 90 min.

Stage2 full-C_F execution is still BLOCKED until:
production adapters + watchdog V2 + P2 partial-evidence schema + Stage-B classifier tests + input lock + production-bound Parity32 replay + P2 B01 adapter replay all PASS.


## 2026-10-01 — P2 Stage2 production adapter unit preflight closed

Historical validator mismatch:
- run 36891298148
- adapter tests actually PASS 5/5
- workflow failed because it expected test_count=4
- artifact 11176273946
- digest sha256:f36397efb9c067e2d6f2d89e5c626975ba8ca45e8ef30da5d9bbc3f278212e8b

Validator-only fix:
`7601cb9cb2cc32ccc6cb462b6bdba856f9846fe2`

Successful rerun:
- run 36892236163
- result 5/5 PASS
- artifact 11177590463
- digest sha256:adc4740ec6fe8f627169e083191451e22ede400df1c86184551c9cb509d0a203

Closure lock:
`phase2/redesign/MPSEF_P2_V2_STAGE2_PRODUCTION_ADAPTER_UNIT_CLOSURE_LOCK_V1.md`

Current state:
- M02 source-free adapter evidence: PASS
- M04 durable-record primitives: PASS
- M01 production-bound replay: OPEN
- full-C_F Stage2: still BLOCKED

Next:
production-bound B01 + real-model adapter validation + frozen Parity32 through the exact Stage2 production adapter.


## 2026-10-01 — P2 Stage2 M01 production-bound replay CLOSED

Production-bound B01 + real-model preflight:
- run 36893287680 SUCCESS
- B01 semantic 20/20
- production-adapter B01 routing 20/20
- real-model source-free 3/3
- artifact 11177717089
- digest sha256:3b5d88e2fb40d7afab724e875cbfff0152e008f35a376a121c48849eaff93cbb

Production-bound frozen Parity32:
- run 36894512600 SUCCESS
- FRESH COMPLETE 32/32
- REPEAT COMPLETE 32/32
- REVERSED COMPLETE 32/32
- fresh_vs_repeat 32/32
- fresh_vs_reordered 32/32
- fresh_vs_frozen_trace_output 32/32
- production_adapter_cli_used=true
- artifact 11179398082
- digest sha256:b35b8614d0a9ab4e444b650db2c9027d2b2f59e3e8c44a9b16be8a9da02e1b5e

Closure:
`phase2/redesign/MPSEF_P2_V2_STAGE2_M01_PRODUCTION_BOUND_REPLAY_CLOSURE_LOCK_V1.md`

Current state:
- M01: CLOSED PASS
- M02 production adapter partial evidence: PASS at source-free/unit + production-bound routing
- M04 Watchdog V2: PASS; durable-record production semantics demonstrated on Parity32
- full-C_F Stage2: STILL BLOCKED

Next mandatory step:
materialize and freeze Stage2 Input Lock, then bind P3 production path + classifier/test prerequisites before any 1,918-case execution.


## 2026-10-01 — Stage2 full-C_F proposer production COMPLETE (P2 + P3)

Stage2 full-population source-only proposer execution has now completed for both P2_V2 and P3_V1 on the exact frozen C_F population.

### Frozen Stage2 Input Lock
- run: `36898163047`
- status: PASS
- C_F: 1918 UIDs / 764 clusters
- artifact: `11180920946`
- digest: `sha256:239395994cdf22bc7c6353de19601caab650dba7e24eedac91795ff453d87b2a`

### P2_V2 full C_F
- run: `36899056538`
- status: SUCCESS / COMPLETE
- terminal durable records: 1918/1918
- aborted: 0
- not attempted: 0
- completion claim allowed: true
- output SHA256: `87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7`
- artifact: `11186450279`
- digest: `sha256:c5c5d32c99ce216a5b93362748cfefa67de4ec1f5b2b1174c8d3caf0fcd914af`
- closure lock: `phase2/redesign/MPSEF_P2_V2_STAGE2_FULL_CF_CLOSURE_LOCK_V1.md`
- closure commit: `6d925741f4e1acf2405c71cd1492ebb1c8f6b953`

### P3_V1 full C_F
- run: `36920015935`
- status: SUCCESS / COMPLETE
- terminal durable records: 1918/1918
- aborted: 0
- not attempted: 0
- completion claim allowed: true
- exact frozen P1 parent reused: true
- P1 rerun: false
- Stage-B classifier: `MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1`
- output SHA256: `02f9bd2555b1b9f350665179dcd96dd6accf532355a269b38ef4d099ea25d4ec`
- artifact: `11192760024`
- digest: `sha256:9a31de6dcff43efb903212a7fe2e2ad378f24e177faba0ecbd46ba4dd05e4253`
- closure lock: `phase2/redesign/MPSEF_P3_V1_STAGE2_FULL_CF_CLOSURE_LOCK_V1.md`
- closure commit: `24016096c29b45b969f5402aab8d0bffedb14566`

### Scientific boundary
- source-only: true
- new gold/reference consulted: false
- quality metric computed: false
- R_joint computed: false
- selector trained: false
- family-consensus activated: false

### Current exact next sequence
1. build/run full-C_F V4 source-only legalizer/action-set analysis over frozen P1 + Stage2 P2 + Stage2 P3;
2. apply family leave-one-out with P1+P3 = one SWEET family;
3. report Stage-B V1 domain counts, legal coverage, protection burden, dedup/candidate-set size, family-marginal contribution, runtime eligibility and overlapping cluster-presence histograms;
4. no gold/R_joint/selector yet;
5. fresh post-Stage2 research + maximum-effort brainstorming after source-only analysis;
6. freeze Stage2 closure and decide next architecture gate.

Current classification:
**IMPROVED STRONGLY / FULL-C_F PROPOSER EXECUTION COMPLETE / LINGUISTIC QUALITY STILL UNMEASURED**


## 2026-10-01 — Cross-chat working protocol frozen

Persistent working-style agreement:
`ACAD_PASS_WORKING_PROTOCOL_V1.md`

Any new ACAD_PASS conversation must read, in order:
1. `RESUME_HERE.md`
2. `ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md`
3. `ACAD_PASS_WORKING_PROTOCOL_V1.md`
4. latest relevant locks/artifacts/runs

This freezes the user's execution preferences across chats, including sequential-only operations, max-3 polling with ~20 s spacing for long runs, ETA reporting from actual progress, non-repetition of unchanged estimates, failure-first diagnosis, fresh research/brainstorming gates, higher-model consultation rules, scientific-boundary discipline, and meaningful checkpoint updates.


## 2026-10-02 — Stage2 protocol-complete; post-Stage2 rebaseline; V4 R_joint source-free preflight PASS

Stage2 source-only protocol completion:
- historical full-C_F analysis run: `36923877787`
- historical artifact: `11192953283`
- artifact digest: `sha256:d773c8b65f607e06ce811d44d7e18deaf49c0da0c17428122d2258b043f82c4b`
- protocol-completion lock:
  `phase2/redesign/MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`
- lock commit: `524e3e4e63bf58a3344b90b5795550f37497b3ee`

Full-C_F source-only family evidence:
- legal non-KEEP from >=1 family: **1843/1918 = 96.09%**
- BOTH independent families: **1736/1918 = 90.51%**
- SWEET only: **67**
- SEQ2SEQ_GED_MORPH only: **40**
- NONE: **75**
- exact cross-family legal non-KEEP agreement: **167 UIDs / 144 clusters**
- P3 MIXED_FROM_P1: **1800/1918 = 93.85%**
- P2 fail-closed generation-completeness rows: **22/1918 = 1.15%**
- no gold/reference, no quality metric, no R_joint, no selector, no consensus.

Fresh post-Stage2 research/rebaseline:
- record:
  `phase2/redesign/ACAD_PASS_POST_STAGE2_FRESH_RESEARCH_REBASELINE_V1.md`
- commit: `651e55c7e1726facaf5ca23d7eb918eb4ebe2d81`
- decision:
  - P1 KEEP
  - P2 KEEP
  - P3 KEEP AS SAME-FAMILY ALTERNATE
  - P4 DEFER
  - Gemma-3-1B Arabic GEC reserved as source-only probe candidate only; NOT gold-eligible because training provenance does not exclude QALB overlap
  - family consensus DEFER
  - learned selector DEFER
  - generic LLM judge DEFER from primary evidence
- critical finding:
  historical `mpsef_rjoint_score_v3.py` is incompatible with V4 because V4 can contain KEEP+P1+P2+P3 (4 actions) and requires P1/P3 same-family semantics.

Frozen pre-gold V4 measurement contract:
`phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
commit:
`2a749a5a41d5f8e8fd57b596d5c6d25a23c7f986`

New V4 scorer:
`phase2/redesign/mpsef_rjoint_score_v4.py`
commit:
`3edee5e48c96c2930246c35783312686cf894e8b`

Synthetic harness:
`phase2/redesign/mpsef_rjoint_v4_synthetic_preflight.py`
commit:
`cf55653873c561018b5e0102c582d74510cc008c`

Observable workflow commit:
`df097dffee26b155cb013206e71d6594b3734df4`

GitHub status:
`acad-pass/v4-rjoint-source-free-preflight = success`

Synthetic result:
**20/20 PASS**

Frozen source SHA256:
- scorer: `b9fdbe205e6e00082b51a7ee16c74d0010c4bbe50406ad58d2f6f9e166db7513`
- synthetic harness: `cb07b046fbd36f2afd0c27f46efd3f7561a42f2ac90b9f4ac5f477e8dd56b8b3`
- core/matcher: `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

Preflight closure lock:
`phase2/redesign/MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
commit:
`0a56dc4995dc5d28be41ddcc8f30bfcfd521ba7d`

Adversarial review packet:
`phase2/redesign/ACAD_PASS_V4_RJOINT_PRE_GOLD_ADVERSARIAL_REVIEW_PACKET_V1.md`
commit:
`493b75d2a1de7aae16f6fd8d8423d8be02ea70a0`

Scientific boundary remains:
- **NO real C_F gold/reference load yet**
- **NO real R_joint yet**
- **NO P4 execution**
- **NO selector training**
- **NO family consensus**
- **NO generic LLM judge**
- reserved/internal populations remain closed.

### Exact next unfinished task

Perform an independent/adversarial pre-gold review of:
1. `MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
2. `MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
3. `mpsef_rjoint_score_v4.py`
4. `mpsef_rjoint_v4_synthetic_preflight.py`
5. `mpsef_rjoint_core_v2.py`
6. Stage2 protocol-completion lock
7. post-Stage2 research rebaseline.

Allowed verdict:
**PROCEED / MODIFY / BLOCK**

If MODIFY/BLOCK:
- remediate before any gold;
- rerun source-free synthetic preflight for semantics-changing changes.

Only after review resolution may a separate lock authorize one C_F gold-aware DEVELOPMENT / REFERENCE-RELATIVE measurement.

Current classification:
**IMPROVED STRONGLY / PRE-GOLD MEASUREMENT IMPLEMENTATION READY / LINGUISTIC PERFORMANCE STILL UNMEASURED**
## 2026-10-02 — Stage2 protocol-complete closure + post-Stage2 rebaseline + V4 R_joint source-free preflight CLOSED

Stage2 protocol-complete lock:
`phase2/redesign/MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`

Post-Stage2 fresh research / architecture rebaseline:
`phase2/redesign/ACAD_PASS_POST_STAGE2_FRESH_RESEARCH_REBASELINE_V1.md`

Frozen Stage2 source-only evidence:
- C_F: 1,918 UIDs / 764 clusters
- legal non-KEEP from at least one family: 1,843 / 1,918 = 96.09%
- BOTH independent families: 1,736 / 1,918 = 90.51%
- SWEET_ONLY: 67
- SEQ2SEQ_GED_MORPH_ONLY: 40
- NONE: 75
- cross-family exact legal non-KEEP agreement: 167 UIDs / 144 clusters
- P2 full-C_F execution failures: 22 / 1,918, all fail-closed at GENERATION after earlier stages passed
- P3 Stage-B MIXED_FROM_P1: 1,800 / 1,918 = 93.85%

Frozen architecture decision after fresh research:
- P1: KEEP
- P2_V2: KEEP
- P3_V1: KEEP AS SAME-FAMILY ALTERNATE
- P4 primary/gold-eligible: DEFER
- P4 Gemma source-only probe: RESERVED ONLY / NOT GOLD-ELIGIBLE
- learned selector: DEFER
- family consensus: DEFER
- generic LLM judge: DEFER FROM PRIMARY EVIDENCE
- authoritative protection: KEEP
- exact whole-action semantics: KEEP

Critical scorer finding:
historical `mpsef_rjoint_score_v3.py` is NOT valid for V4 because it assumes P1/P2/PAIR and action-set size <=3. V4 can contain KEEP+P1+P2+P3 = 4 actions and requires P1+P3 to remain one SWEET family.

Frozen pre-gold contract:
`phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
commit:
`2a749a5a41d5f8e8fd57b596d5c6d25a23c7f986`

New scorer:
`phase2/redesign/mpsef_rjoint_score_v4.py`
commit:
`3edee5e48c96c2930246c35783312686cf894e8b`

Synthetic preflight:
`phase2/redesign/mpsef_rjoint_v4_synthetic_preflight.py`
commit:
`cf55653873c561018b5e0102c582d74510cc008c`

Final observable workflow commit:
`5c280d4cc6abda3e1f5f21c0fbcb6e79c2d6df2d`

Closure lock:
`phase2/redesign/MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
final lock commit:
`544e4059af4fd891c504492faf2b876bad8fca76`

GitHub status:
`acad-pass/v4-rjoint-source-free-preflight = success`

Frozen SHA256:
- scorer: `b9fdbe205e6e00082b51a7ee16c74d0010c4bbe50406ad58d2f6f9e166db7513`
- synthetic test source: `cb07b046fbd36f2afd0c27f46efd3f7561a42f2ac90b9f4ac5f477e8dd56b8b3`
- synthetic result JSON: `4eb8c2510fd62b50ff3a557018bc58d52853e53e4625389572308e62b39585d2`
- inherited core: `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

Synthetic result:
- 20/20 PASS
- source-free
- no project gold
- no real R_joint
- no selector
- no consensus
- no P4

Current exact next sequence:
1. prepare/freeze focused adversarial higher-model review packet for the V4 pre-gold contract/scorer;
2. obtain review verdict PROCEED / MODIFY / BLOCK;
3. resolve every BLOCKER/semantics-changing MAJOR and rerun synthetic preflight if required;
4. only after explicit review-resolution authorization may C_F gold/reference be loaded;
5. real R_joint V4 remains BLOCKED now.

Current classification:
**IMPROVED STRONGLY / PRE-GOLD V4 SCORER READY FOR ADVERSARIAL REVIEW / LINGUISTIC PERFORMANCE STILL UNMEASURED**
## 2026-10-02 — V4 pre-gold adversarial review packet frozen

Review packet:
`phase2/redesign/ACAD_PASS_V4_PRE_GOLD_HIGHER_MODEL_REVIEW_PACKET_V1.md`

Commit:
`8e1257c037c196c67feabcc82f238ae31a4e29e1`

Purpose:
independent/higher-model adversarial review of the frozen V4 pre-gold contract and scorer before any C_F gold/reference loading.

Packet includes:
- authoritative evidence order;
- frozen scorer/test/core hashes;
- V4 proposer/family/action semantics;
- M04/M05 requirements;
- single-reference and historical-exposure boundaries;
- 30 mandatory review questions;
- strict PROCEED / MODIFY / BLOCK verdict format;
- explicit gold-authorization field.

Current tool limitation:
no independent higher-model execution endpoint is available in the present toolset. Therefore no higher-model verdict has been claimed.

Current exact next action:
1. submit `ACAD_PASS_V4_PRE_GOLD_HIGHER_MODEL_REVIEW_PACKET_V1.md` to an independent higher model;
2. store the returned review verbatim or as a frozen repository review artifact;
3. resolve every BLOCKER and every semantics-changing MAJOR;
4. rerun the source-free V4 synthetic preflight if scorer/contract semantics change;
5. create an explicit review-resolution authorization lock;
6. only then may C_F gold/reference be loaded for a development-feasibility R_joint V4 measurement.

Hard boundary now:
**REAL GOLD/R_JOINT REMAINS BLOCKED PENDING INDEPENDENT REVIEW RESOLUTION.**
## 2026-10-02 — Reporting protocol strengthened + compact higher-model prompt frozen

Working protocol update:
`ACAD_PASS_WORKING_PROTOCOL_V1.md`
commit:
`09ee7ecc40e7bb855ca01c5e81f012bb71ba6033`

Mandatory checkpoint reporting now explicitly requires:
- IMPROVED / WORSENED / MIXED / NOT COMPARABLE;
- exact delta where comparable;
- what improved and what worsened/new risks;
- current-stage completion estimate with stated gate/work-unit basis;
- approximate whole-ACAD_PASS completion estimate;
- remaining gate/work units;
- blockers and realistic next-step forecast;
- fresh deep research + maximum-effort brainstorming/red-team at START and END of every substantive phase/iteration.

Future wall-clock completion promises are not used; remaining work is reported as gates/work units.

Compact higher-model prompt:
`phase2/redesign/ACAD_PASS_V4_HIGHER_MODEL_PROMPT_COMPACT_V1.md`
commit:
`38f393771b1fee7fc42048bb25776ce9d7f5060f`

Exact next action:
use the compact prompt with the independent higher model; return its verdict/review to this branch/chat; then resolve BLOCKER/MAJOR findings before any real C_F gold load.


## 2026-10-02 — V4.2 hardened preflight verification pending

Internal adversarial review:
`phase2/redesign/ACAD_PASS_V4_RJOINT_INTERNAL_ADVERSARIAL_REVIEW_V1.md`
commit:
`0bb90f26f745a77c2f3334789581c8f2e817c1af`

Verdict:
**MODIFY BEFORE GOLD**
- BLOCKER: 0
- MAJOR: 4
- MINOR: 3

Primary repairs:
- full-reference scoring with primary/punctuation projection;
- explicit M05 composite BOUNDARY={SPLIT,MERGE};
- 95% ROSTER primary candidate-availability gate;
- production identity-lock requirement.

Amendment:
`phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1_AMENDMENT_A1.md`
commit:
`cae6c3f95e9ffdad9f7e550aa41d971f5541ff41`

V4.1:
- scorer commit: `61a810e3c1ae443e0671fb150c83374d2c981869`
- 27-case harness commit: `4fdaafd894f3e80eec5e39901a46b7da80d05fc3`
- workflow commit: `31242b687015df9c2220e68c7ae2c87cc8548d58`
- status: SUCCESS
- source-free: true
- gold: false

Pre-closure guard review found additional input-semantics hardening needed:
- reject duplicate literal outputs;
- reject non-KEEP source-equivalent output;
- reject action output SHA mismatch;
- reject KEEP/source SHA mismatch.

V4.2 hardened scorer:
`phase2/redesign/mpsef_rjoint_score_v4_2.py`
commits:
- `6e278abbe0431043ee74e2bac4c1f6ed649f4005`
- `f5e50f2f9e3371ab7ea7f294cc1b3b499b1f4e63`

31-case harness:
`phase2/redesign/mpsef_rjoint_v4_2_synthetic_preflight.py`
commit:
`3559c73d0014f314806d2613163e3e7f536d026b`

Initial V4.2 workflow:
commit `710920fd7426aa6c7aa2cfa330012fb695623459`
observed:
- preflight status = FAILURE
- scorer/test/core/result SHA status publication succeeded.

Diagnostic rerun:
commit `8654902115d3036f7a391e3a11fb8097c91e8cce`
observed:
- diagnostic summary context published;
- no per-test fail contexts exposed.

Minimal unchanged verification-only workflow:
commit `2481dcb8b2160a47d017a3a9a0409437bdb9f331`

Three status polls in the current turn returned no exposed status yet.
Polling stopped per working protocol.

Diagnostic lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_PREFLIGHT_ATTEMPT_DIAGNOSTIC_LOCK_V1.md`
commit:
`05f1fec3345c0c8100a2044b6cde67e2e9ea5f73`

Scientific boundary:
- NO real C_F gold/reference load;
- NO real R_joint;
- NO P4;
- NO selector;
- NO consensus;
- NO LLM judge;
- reserved/internal populations closed.

### Exact next unfinished task

Inspect commit:
`2481dcb8b2160a47d017a3a9a0409437bdb9f331`

If:
`acad-pass/v4-2-rjoint-31of31 = success`

then:
1. freeze V4.2 source-free closure and SHA identities;
2. perform remediation closure review;
3. build/freeze production premeasurement input-lock/wrapper;
4. gold remains closed until an explicit authorization lock.

If status is absent/failure:
diagnose the verification-only workflow before changing scorer/harness.

Current classification:
**MIXED / METHOD HARDENED / V4.2 CLOSURE PENDING / PERFORMANCE UNMEASURED**
## 2026-10-02 — Independent delta review remediation completed; V4.2 pre-gold closure frozen

Independent delta-review result:
- verdict: MODIFY
- new BLOCKER/MAJOR findings: NONE
- B01 CLOSED
- B02 PARTIAL at review time
- M01-M05 CLOSED
- N01-N02 CLOSED
- gold authorization at review time: DO NOT AUTHORIZE YET

Remediation completed source-free:
- T20 repaired to isolate external source identity mismatch;
- T24 repaired to contain true SPLIT + MERGE;
- score_population_v4_2 now validates frozen_identity vs expected_identity before build_targets/gold analysis;
- incomplete identity contract fails closed;
- progress callback added and reverified;
- production dependency lock created;
- production wrapper created under A1 §A1.6;
- wrapper fail-closed preflight created.

Official verification:
- scorer preflight: **33/33 PASS**
- wrapper preflight: **14/14 PASS**
- combined GitHub status:
  `acad-pass/v4-2-pre-gold-wrapper = success`

Frozen SHA256:
- scorer: `be9cf725b71b8d26a23eff9e9afd4ca434294a4d8f72e0271caa179ca892f2e1`
- core: `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`
- wrapper: `72bf23c9f910c2b203caf11e6e677729fa914d66c2d1e062ac0fd7dfd6da357f`
- scorer harness: `da31f7c1dd6d1f0bfd5356a54a19aba518742ce489f9f3d7d59242609566c25c`
- wrapper test: `d62696e3a2df2ee9fbb20839cef35bca7e4b0aec39155206837af400686c3ab8`
- dependency lock: `aa66ec3d6fdb4aef1b4fada26a1b6cf794f632139655e22462a7a1c27aab7bc5`
- scorer preflight result: `c46ac5e3fe6ffc349273104c6f8849b9628fa0383780e40e20fb077ad50b5a1e`
- wrapper preflight result: `1b03bf5a0192b35abd03d38b8d31c5a7396473fe1509bb39f591f418cf27a27e`

Full-C_F production identities:
- cases: 1,918
- clusters: 764
- source manifest SHA256: `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- action-set SHA256: `e38393abb36734d3882e29a78f3b33c80718791957b9b8c0c6e8a8ab77f6e138`
- UID SHA256: `51e2e1decf1c7c9efbc31e343eba1c7dfb08d0de314041cb57f5b3118ffd550f`
- cluster SHA256: `bb2f49c6aaf312cf9c388237090a79861fa6218da15de57d0119efd39327ae3c`
- UID-cluster map SHA256: `32b89f9dcadefa0f17cb0fddac6099433d611508a01ad96b428e0534c1057c5d`
- provenance map SHA256: `18561c75c397821c34e3dc06214bb4f64cc5ff8d6757f61835cbe9e6808befbd`
- frozen gold M2 SHA256 identity: `971b6fbb28dc3767193e7a4b0f722c3abebfc8600155a57093ba483dac6491e8`
- gold content newly opened: false

Production input lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_PRODUCTION_INPUT_LOCK_V1.json`
commit:
`d71ad97e9b3ee47c4fbcbaf4a6d6fcdc66fcd744`

Pre-gold closure lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_PRE_GOLD_CLOSURE_LOCK_V1.md`
commit:
`134bc2204914033850b8a3c200381fb2363e25b6`

Input-lock SHA publication workflow:
commit:
`c49d572f82e3939ad4461ad0b78ff45655d2ac7b`

Three status inspections in the current continuation returned no exposed input-lock SHA context yet. Per protocol, polling stopped.

Exact next sequence:
1. inspect commit `c49d572f82e3939ad4461ad0b78ff45655d2ac7b` once in the next continuation;
2. capture `acad-pass/v4-2-input-lock-sha256/<SHA256>`;
3. create separate exact-SHA-bound single-run authorization lock;
4. validate authorization lock;
5. only then allow one DEVELOPMENT-only V4.2 R_joint run.

Hard boundary:
**GOLD/R_JOINT REMAIN CLOSED UNTIL THE INPUT-LOCK SHA IS BOUND INTO THE AUTHORIZATION RECORD.**
## 2026-10-02 — V4.2 exact authorization validated; one-shot DEVELOPMENT measurement launched

Input-lock SHA256 publication completed:
`3f3e4bd95bbd5d49ad71ec58466573d56a476eefcf0cdc3719c2c732d3de19d0`

Single-run authorization:
`phase2/redesign/MPSEF_RJOINT_V4_2_SINGLE_RUN_AUTHORIZATION_V1.json`

Authorization commit:
`fd776f286e7f72f0343290b44ad93e94370cec13`

Authorization validation:
- `acad-pass/v4-2-authorization-valid = success`
- authorization SHA256:
  `c9adda76ace40df378ab4c88f193160e1edbdd6256f079e87ee4d2e185008993`

Authorized one-shot workflow:
`.github/workflows/phase2-mpsef-v4-2-development-rjoint-one-shot.yml`

Workflow trigger commit:
`f84c94527df487dc0426165737450471d6da3fa4`

Observed GitHub Actions run:
`36938833412`

Current observed status after three sequential inspections:
`acad-pass/mpsef-rjoint-v4-2-progress = pending`

The progress context is emitted only by the authorized scoring watchdog after the pre-gold checks, single-run durable consumption claim, and post-claim reference artifact verification steps. Therefore the authorized measurement has entered its scoring phase.

Per the polling protocol, no fourth inspection was performed in this continuation.

Do NOT:
- launch a second V4.2 measurement;
- rerun the workflow;
- modify scorer/core/wrapper/input-lock/authorization while run 36938833412 is active;
- activate P4, selector, consensus, LLM judge, internal evaluation, stress, or reserved populations.

Exact next action on the next user continuation:
1. inspect run/commit `f84c94527df487dc0426165737450471d6da3fa4` / run `36938833412`;
2. if still pending, follow the max-three-polls rule again;
3. if complete, retrieve and validate the measurement artifact before interpreting any metrics;
4. preserve any failure before considering a technical rerun; the single-run authorization is considered consumed once the durable claim was made.

Current classification:
**IMPROVED STRONGLY / EXACT AUTHORIZATION PASS / ONE-SHOT DEVELOPMENT R_JOINT V4.2 RUNNING**
## 2026-10-02 — Runtime environment identity hardening discovered before gold; prior authorization fail-closed

During final measurement-workflow design, an additional B02 reproducibility gap was found BEFORE any gold access:

The V4.2 production wrapper verified:
- dependency-lock file SHA256;
- Python major/minor;
- Arabic-GEC git revision;

but did not independently verify the ACTUAL installed versions of:
- numpy;
- editdistance;

despite those versions being frozen in the dependency lock.

This was treated as a genuine environment-identity gap, not ignored.

Repairs committed:
- production wrapper now parses the dependency contract and verifies actual installed package versions and runtime policies before any gold access;
- wrapper result records runtime dependency identity;
- wrapper preflight expanded from 14 to 16 cases:
  - runtime package-version mismatch must fail closed;
  - runtime measurement-policy mismatch must fail closed.
- combined pre-gold workflow updated to install exact:
  - numpy==1.23.5
  - editdistance==0.6.2

Commits:
- wrapper runtime enforcement: `07bed9062757e96ce40c531e772f18d70ffe8303`
- wrapper preflight expansion: `fce41376558f7c53240b906608836759fafcbd21`
- combined preflight workflow update: `f7353bd2693654a78d49a353ba04485683e79f45`

The updated combined preflight was inspected three times in this continuation; no status was exposed yet. Polling stopped per protocol.

Because wrapper semantics/identity changed AFTER the earlier input-lock/authorization:
- previous single-run authorization SHA `5bb5727e6fea6d7b89e0180656660713ee1d301f1dcf4134755d47385d1cfc28` is now SUPERSEDED and fail-closed;
- previous input-lock SHA `3f3e4bd95bbd5d49ad71ec58466573d56a476eefcf0cdc3719c2c732d3de19d0` is now SUPERSEDED pending re-freeze.

Fail-close commits:
- authorization superseded: `75b8afcb65831d41ff3e4642c5af708c4a58bf14`
- input lock superseded: `ec3e7793a9c4286d3928ebeacc8d6269f3bdf7e9`

Consumption guard remains verified:
- status: PASS
- SHA256: `895128860ba4e03f287b91c56d3505f5df5a9c31292a5555088654aedd468070`
- consumed context: `acad-pass/v4-2-rjoint-consumed`
- no consumption claim has been made yet.

Scientific boundary remains:
- project gold newly opened: false
- real R_joint computed: false
- P4 used: false
- selector trained: false
- family consensus activated: false
- LLM judge used: false
- internal/stress/reserved populations opened: false

Exact next sequence:
1. inspect updated pre-gold workflow commit `f7353bd2693654a78d49a353ba04485683e79f45` once on next continuation;
2. if scorer 33/33 and wrapper 16/16 PASS, capture new wrapper/test/result SHA256;
3. re-freeze production input-lock with the new runtime-verifying wrapper identity;
4. publish/capture new input-lock SHA256;
5. issue and validate a new exact-SHA-bound single-run authorization;
6. freeze measurement workflow + one-shot execution manifest;
7. claim consumption BEFORE gold access;
8. only then execute one DEVELOPMENT-only V4.2 R_joint run.

Classification:
**MIXED BUT SCIENTIFICALLY IMPROVED / RUNTIME REPRODUCIBILITY HARDENED / TEMPORARY AUTHORIZATION ROLLBACK / GOLD REMAINS CLOSED**
## 2026-10-02 — V4.2 runtime environment identity hardening

Before opening gold, an additional governance gap was identified:
the production wrapper verified the dependency-lock file hash and Python/Arabic-GEC identities, but did not independently verify the actually installed runtime package versions.

Source-free hardening applied:
- production wrapper now parses and enforces the dependency lock before any gold access;
- exact runtime package checks added for:
  - numpy = 1.23.5
  - editdistance = 0.6.2
- runtime policies are also enforced:
  - network_download_during_measurement = forbidden
  - model_inference_during_measurement = forbidden
- wrapper preflight expanded from 14 to 16 tests with explicit rejection tests for package-version and runtime-policy mismatch.

Wrapper hardening commit:
`07bed9062757e96ce40c531e772f18d70ffe8303`

Extended wrapper-preflight commit:
`d5543b72d139248423bfbf94a905ee02d1d8dbc4`

Verification workflow updated to install the exact frozen measurement dependencies and require:
- scorer: 33/33 PASS
- wrapper: 16/16 PASS

Workflow commit:
`500b176475b60ab5207c6715fa28e2c84f76c70e`

Polling state:
three sequential status checks returned no exposed status yet. Per protocol, polling stopped.

IMPORTANT:
The previously frozen wrapper/input-lock/authorization hashes are now superseded by this source-free hardening and MUST NOT be used to open gold. Gold remains closed.

Exact next sequence:
1. inspect commit `500b176475b60ab5207c6715fa28e2c84f76c70e`;
2. require combined scorer 33/33 + wrapper 16/16 PASS;
3. capture new wrapper/test/result SHA256 values;
4. regenerate/update the production input-lock with the new wrapper identity;
5. republish input-lock SHA;
6. regenerate exact-SHA single-run authorization;
7. revalidate authorization + consumption guard binding;
8. only then create/freeze/execute the one-shot DEVELOPMENT-only V4.2 measurement workflow.

No gold/reference content was opened and no real R_joint was computed during this hardening.
## 2026-10-02 — V4.2 exact runtime preflight failure diagnosed and repaired

Commit `500b176475b60ab5207c6715fa28e2c84f76c70e` completed with:
- scorer preflight: PASS / 33/33
- install/compile/runtime setup: PASS
- wrapper preflight step: FAIL
- all SHA publication steps: completed

Workflow run:
`36939409747`

Failure localization:
`Run 16-case wrapper preflight` only.

Root cause:
the source-free harness accidentally contained duplicate copies of W15 and W16, yielding 18 executed test records while the summary correctly required exactly 16. This was a harness bookkeeping defect only; it did NOT indicate a scorer, wrapper, population, provenance, or runtime-identity semantic failure.

Repair:
duplicate W15/W16 block removed only.

Repair commit:
`45187205641612d867a8547305fc37688493eded`

No production semantics changed in this repair.

Three sequential status checks on the repair commit returned no exposed status yet, so polling stopped per protocol.

Current exact next sequence:
1. inspect commit `45187205641612d867a8547305fc37688493eded`;
2. require scorer 33/33 + wrapper 16/16 PASS;
3. capture the new wrapper-test/result SHA256 values;
4. update production input-lock and republish its exact SHA;
5. regenerate and validate exact-SHA single-run authorization, including verified consumption guard;
6. freeze the one-shot measurement workflow;
7. claim consumption before gold access;
8. execute one DEVELOPMENT-only R_joint V4.2 run;
9. analyze/freeze result and perform end-of-phase research/red-team/closure decision.

Gold/reference content remains unopened by this repair.
Real R_joint remains uncomputed.
## 2026-10-02 — Exact-runtime V4.2 pre-gold verification PASS; final authorization validation pending

Exact-runtime verification is now closed PASS.

Successful workflow:
- commit: `705129dc9f319d835321a47a2530d48bd18ac468`
- run: `36940030184`
- conclusion: SUCCESS
- scorer preflight: **33/33 PASS**
- wrapper preflight: **16/16 PASS**
- artifact id: `11199084513`
- artifact digest: `sha256:5f16c02fdbe8612499c24b6b2209a19ee03f6738d529e78b10f545fe7c430b20`

Runtime identity hardening is therefore closed:
- Python 3.10
- numpy 1.23.5
- editdistance 0.6.2
- Arabic-GEC revision `8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`
- network download during scoring forbidden
- model inference during scoring forbidden

Production input lock refreshed:
- commit: `0983e315603a8ffba28695f84f41069bd3ae4d58`
- SHA256: `f3f40b1425e272f27d2e19a41f45792310102ad7a62ef9037e78868430517ff3`

Dormant one-shot measurement workflow frozen:
- file: `.github/workflows/phase2-mpsef-v4-2-rjoint-one-shot.yml`
- latest binding commit: `41343523f36cb85784e3ba866f05ba67353b0a5a`
- SHA256: `7ad25c7207700cca202b3a2727200c7a1d59c409c9ec57bfe013865d63d3f3d8`
- state: DORMANT / NOT ACTIVATED

Authorization refreshed against the final runtime/input/workflow identities:
- authorization content commit: `c11dcd03f3bb5215e133c1c4221f38ee977a2960`
- authorization SHA256: `a91b25d68b2b2fb80e32326e614853026e6b90d1ce3dac4cc00f571be1425ce3`
- consumption guard SHA256: `895128860ba4e03f287b91c56d3505f5df5a9c31292a5555088654aedd468070`

Final authorization-validation workflow hardened and launched:
- commit: `8aba3486fc85c473e0c67ef4333f5ab4a8c305e8`

Three sequential status inspections returned no exposed status yet; polling stopped per protocol.

Non-triggering activation template prepared:
- file: `phase2/redesign/MPSEF_RJOINT_V4_2_EXECUTION_ACTIVATION_V1_TEMPLATE.json`
- commit: `153bf902b2082a99304b799d476daef4626742b3`

Hard boundary:
- project gold newly opened: false
- real R_joint computed: false
- activation record created: false
- measurement workflow triggered: false

Exact next sequence:
1. inspect commit `8aba3486fc85c473e0c67ef4333f5ab4a8c305e8`;
2. require `acad-pass/v4-2-authorization-valid = success`;
3. capture authorization SHA context and confirm it matches `a91b25d68b2b2fb80e32326e614853026e6b90d1ce3dac4cc00f571be1425ce3`;
4. create the real activation file with the latest preactivation code commit;
5. one-shot workflow claims consumption BEFORE gold;
6. open only the authorized CALIBRATION/M2 gold;
7. run one DEVELOPMENT-only R_joint V4.2;
8. freeze/analyze result and execute end-of-phase research/red-team/closure decision.
## 2026-10-02 — V4.2 one-shot measurement activated; run in progress

Exact-runtime closure achieved:
- scorer preflight: 33/33 PASS
- wrapper preflight: 16/16 PASS
- successful verification run: 36940030184
- verification artifact: 11199084513
- artifact digest: sha256:5f16c02fdbe8612499c24b6b2209a19ee03f6738d529e78b10f545fe7c430b20

Refrozen production input lock:
- refreeze commit: 280a192712e6ab346d87b2f63a852875aa709152
- validator commit: cf48d89677d9235e9c064965d7671544f7d54058
- exact input-lock SHA256:
  `6ac8656226c64b64e8fc6a408475dbff1e231ec3d87b7afa3da464b1dee25132`
- status context: success

Replacement exact-SHA authorization:
- authorization update commit: f798180cd661cd8405a0ab1e69b7e911d5413303
- validation commit: 679e0d73ea3f1ce936911c4b74eae3d6ead56363
- authorization status: success
- exact authorization SHA256:
  `7b8a4ebd8216bd2fd06c42d919bbe16d219b6cbc0b46cfad07f286f08651fb49`

Dormant one-shot workflow:
`.github/workflows/phase2-mpsef-v4-2-rjoint-one-shot.yml`
Exact workflow SHA256 bound in authorization:
`7ad25c7207700cca202b3a2727200c7a1d59c409c9ec57bfe013865d63d3f3d8`

Activation:
- file: `phase2/redesign/MPSEF_RJOINT_V4_2_EXECUTION_ACTIVATION_V1.json`
- activation commit: `eabbd984744d3c5551e19b537d2b5b89d9cb5d8a`
- decision: EXECUTE_AUTHORIZED_SINGLE_DEVELOPMENT_RUN

Live workflow run:
- run id: `36940844664`
- name: Phase 2 MP-SEF V4.2 One-Shot Development R_joint
- last observed status: IN_PROGRESS

Last observed completed gates:
1. checkout activation trigger — PASS
2. activation record read/preserved — PASS
3. activation-only diff — PASS
4. authorization/input-lock preservation — PASS
5. trigger identity validation — PASS
6. exact authorized code checkout — PASS
7. Python setup — PASS
8. exact authorization artifacts restored — PASS

At last observation:
- runtime dependency installation was in progress;
- consumption claim step had NOT yet executed;
- no `acad-pass/v4-2-rjoint-consumed` status was present;
- therefore gold/reference access was NOT yet evidenced as opened at that checkpoint.

Polling discipline:
three sequential inspections were used; polling stopped per protocol.

Exact next action on next continuation:
1. inspect workflow run `36940844664`;
2. if completed before consumption claim, diagnose and apply stop-rule;
3. if consumption claim succeeded, preserve that fact and inspect whether gold identity verification and R_joint execution completed;
4. if measurement completed, freeze outputs/hashes before interpretation;
5. then perform result analysis + fresh end-of-phase research/red-team before any architecture decision.

No selector, P4, family consensus, LLM judge, internal evaluation, stress diagnostic, or reserved population is authorized.
## 2026-10-02 — V4.2 one-shot measurement crossed gold boundary; R_joint actively running

Workflow run:
`36940844664`

The one-shot run has now crossed the authorized gold boundary.

Observed completed steps:
- exact runtime dependencies — PASS
- exact Arabic-GEC revision — PASS
- frozen source manifest download — PASS
- frozen V4 action-set download — PASS
- all pre-gold identity checks — PASS
- source-free self-tests before consumption — PASS
- one-shot consumption claim — PASS
- frozen CALIBRATION download after claim — PASS
- frozen official M2 gold download after claim — PASS
- post-claim gold identity verification — PASS

Durable consumption status:
`acad-pass/v4-2-rjoint-consumed = success`

Consumption target:
`https://github.com/abdullah-s-mahmood/sweet-runtime-parity/actions/runs/36940844664`

Current active step:
`Run one-shot DEVELOPMENT-only R_joint V4.2`

Current scientific boundary:
- gold/reference is now officially opened for this consumed DEVELOPMENT run;
- the experiment is consumed and MUST NOT be silently rerun;
- real R_joint execution is in progress;
- no completed metric result has yet been observed;
- selector/P4/family-consensus/LLM judge/internal/stress/reserved populations remain forbidden.

Polling discipline:
three inspections were used in this continuation; polling stopped.

Exact next action:
1. inspect run `36940844664`;
2. if measurement completed, freeze summary/per-sentence/environment/hash outputs before interpretation;
3. if failed after consumption, DO NOT rerun automatically — apply the documented technical stop-rule and preserve the failure;
4. after frozen result exists, perform result analysis and the required end-of-phase fresh research/red-team before architecture closure.
## 2026-10-02 — V4.2 DEVELOPMENT measurement completed and formally closed

One-shot workflow:
`36940844664`

Conclusion:
`success`

Consumed status:
`acad-pass/v4-2-rjoint-consumed = success`

Frozen artifact:
- id: 11200024879
- digest: `sha256:10ecdb75b5d80540d2c9ddf5e94672e8d64bbe3eb685ca3f53d63789c3d308af`

Frozen result files:
- summary SHA256:
  `5a649c5e050b34679e27958814201d49a948e039c38961032ced263bdacddc91`
- per-sentence SHA256:
  `0e6c51435e978c1c917b9a37a361fad1a5fe4f65da6e18b17759ad2ecb67cc50`

Evidence lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_DEVELOPMENT_MEASUREMENT_EVIDENCE_LOCK_V1.md`
commit:
`fdad9788e152f1747a2a695973eb04a594e7b3cf`

Result analysis:
`phase2/redesign/MPSEF_RJOINT_V4_2_DEVELOPMENT_RESULT_ANALYSIS_V1.md`
commit:
`fe130325130f073f5e97704a5f7eecd7b040c165`

Closure lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_DEVELOPMENT_MEASUREMENT_CLOSURE_LOCK_V1.md`
commit:
`fa1cee35f3fdaa5aaade3efdc7e2c4621c5f928c`

Frozen result:
- primary target denominator: 9,679
- ROSTER primary recovery: 72.2285–72.2699%
- SWEET: 66.9284–66.9697%
- SEQ2SEQ: 58.6941%
- ROSTER over SWEET: +5.26 to +5.34 pp / +509 to +517 targets
- 95% candidate-availability gate: FAIL
- 95% requirement: 9,196 targets
- ROSTER upper: 6,995
- deficit: 2,201 targets / 22.7301 pp
- ROSTER clean whole-action recovery: 23.6491–23.6905%
- ROSTER primary complete repair: 21.8884–21.9421%
- scoring failures: 12 group records across only 2 UIDs

Architecture disposition:
- P1 KEEP
- P2 KEEP
- P3 KEEP as same-family diagnostic alternate / DEFER as primary product route
- current whole-sentence ROSTER: DO NOT TRAIN SELECTOR YET
- selector: DEFER
- family consensus: DEFER
- generic LLM judge: DEFER as primary
- prior specific P4: DEFER pending provenance/overlap audit
- candidate representation: REPAIR / REDESIGN

Reason:
current candidate union fails the frozen 95% candidate-availability gate by 2,201 targets. A selector cannot recover absent candidates.

Fresh end-gate research reviewed:
- ArbESC+ (2025) — Arabic edit-selection/system combination
- STAGEET (2026) — staged typed edit tagging
- JELV (AAAI 2026) — limited-reference edit validity
- CLEME2.0 (ACL 2025) — edit-disentangled evaluation

C_F is now permanently:
`ADAPTIVELY_CONSUMED DEVELOPMENT / NOT CLEAN HOLDOUT`

No silent V4.2 rerun is authorized.

Current formal next gate:
`POST-V4.2 CANDIDATE ARCHITECTURE REDESIGN GATE`

Required next order:
1. source-only brainstorming/red-team;
2. provenance audit for new candidate families;
3. edit-level representation/conflict contract;
4. freeze a new untouched future evaluation population before gold-aware tuning;
5. source-free preflight;
6. independent review before opening any new references.

Phase status:
**V4.2 DEVELOPMENT MEASUREMENT STAGE = 100% CLOSED.**


## 2026-10-03 — English-first architecture adopted; AT0-EN offline gate

Active strategy is now `ENGLISH_FIRST / MULTILINGUAL_READY_CORE`. English is the only active research language. Arabic active research is FROZEN, not discarded, and its prior evidence is preserved for a future `LANG_AR` port.

Permanent architecture records:
- `docs/architecture/ACAD_PASS_MASTER_PRODUCT_ARCHITECTURE.md`
- `docs/architecture/ACAD_PASS_LANGUAGE_EXTENSION_CONTRACT.md`
- `docs/architecture/ACAD_PASS_ARABIC_RESEARCH_PRESERVATION_SNAPSHOT.md`
- `docs/architecture/ACAD_PASS_ARCHITECTURE_CHANGELOG.md`
- `docs/architecture/ACAD_PASS_EVIDENCE_MANIFEST.json`
- `docs/architecture/ACAD_PASS_HIGHER_MODEL_DELEGATION_PROTOCOL.md`

AT0-EN offline implementation checkpoint:
- base branch HEAD inspected before adoption: `4f5befb03762aa6403cc51ca80a28bb9f482a0a2`
- architecture/AT0-EN repository adoption commit: `bca3a32791c6f2c1832403cbd751ea8c78cd6a43`
- critical artifact bytes verified against recorded SHA-256 for P1, P2 V2 Stage2, P3 V1 Stage2, and V4.2 final measurement;
- no new Arabic dataset opened; no Arabic/V4.2 experiment rerun;
- first frozen preflight: 29/30; F07 exposed missing independent authorized-scope enforcement;
- repair: added `authorized_scope` as a separate invariant so source matching cannot authorize adjacent-context writes;
- final frozen preflight: 30/30 PASS;
- `LANGUAGE_PORTABILITY_AUDIT`: 10/10 PASS;
- 12 English synthetic cases frozen;
- 48 live slots preallocated and explicitly accounted as `NOT_RUN_MODEL_ACCESS`;
- no live model call has been made;
- live matrix remains blocked until two exact already-authorized model identities and an explicit cost ceiling are available.

Independent statuses:
- ENGINEERING_STATUS: PASS_OFFLINE
- HUMAN_WRITING_STATUS: NOT_ASSESSED
- SCIENTIFIC_FIDELITY_STATUS: NOT_ESTABLISHED
- VOICE_STATUS: NOT_ASSESSED
- LENGTH_PRESERVATION_STATUS: POLICY_DEFINED / OFFLINE_DIAGNOSTICS_READY
- DETECTOR_ROBUSTNESS_STATUS: NOT_RUN
- DOCUMENT_FIDELITY_STATUS: NOT_RUN
- COMMERCIAL_USEFULNESS_STATUS: NOT_ASSESSED
- PRODUCTION_READINESS: NOT_ESTABLISHED

Next allowed action: complete the authorized AT0-EN 48-slot live matrix when model access and budget are explicitly available, or return the compact `HIGHER_MODEL_REVIEW_PACKET.md` to the higher-model architect for a blocker decision. Do NOT begin HW1-EN, DR, Arabic resumption, reserved-data opening, V4.2 rerun, selector/consensus work, voice fitting, DOCX/Word integration, or paid launch before that review gate.

Operating rule: routine implementation/research is delegated to the implementation agent. The higher model is reserved for architecture, difficult research synthesis, brainstorming, frozen-result review, and high-stakes scientific/strategic decisions. Tool operations in this project are executed strictly sequentially; no parallel tool orchestration.

## 2026-10-03 — AT0-EN higher-model ACCEPT_BLOCKED_CHECKPOINT

Higher-model decision: `KEEP / ACCEPT_BLOCKED_CHECKPOINT`.

Evidence accepted:
- critical preservation PASS;
- frozen engineering fixtures `30/30 PASS`;
- language portability audit `10/10 PASS`;
- live matrix `0/48` because auditable two-model access and budget authorization are unavailable;
- F07 `authorized_scope` repair accepted as an implementation correction inside the frozen contract; no architecture redesign required.

Repository decision commits:
- review packet refresh: `e9df057407f99f25f3b8097aed80c8f1b96b9920`
- config records accepted blocked checkpoint: `460cabfbe17f83c0aee941f8e41f27a460959624`
- model manifest records accepted blocked checkpoint: `f74777e291bc70c472f04e137468e8ea71b4358b`

Exact next authorized action:
- unblock AT0-EN access only if two distinct auditable model identities plus explicit `authorized_cost_ceiling` and `max_total_tokens` are available;
- otherwise retain blocked checkpoint;
- `HW1-EN` and `DR` remain NOT AUTHORIZED;
- Arabic active research remains FROZEN;
- no V4.2 rerun and no reserved-data opening.

Higher-model operating rule remains: use the higher model only for architecture, difficult research synthesis/brainstorming, experiment design, frozen-result review, and strategic decisions; routine execution remains with the implementation agent.


## 2026-10-03 — AT0-EN V2.1 open-weight backend frozen

Higher-model amendment accepted: commercial API access is no longer required for AT0-EN. The access clause is replaced by: two distinct real model configurations, authorized for use, with auditable execution and bounded resources.

Frozen implementation state:
- amendment: `docs/architecture/ACAD_PASS_AT0_EN_EXECUTION_BACKEND_AMENDMENT_V2_1.md`;
- MODEL_A: Qwen3-4B-Instruct-2507 Q4_K_M, artifact SHA-256 `2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e`;
- MODEL_B: SmolLM3-3B Q4_K_M, artifact SHA-256 `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`;
- runtime: `llama.cpp` commit `b92761a515ea31e852e7fbc1fad5f874b46f3718`;
- target environment: public-repository GitHub-hosted `ubuntu-24.04`, one job, strictly sequential, USD 0 additional monetary cost;
- workflow: `.github/workflows/at0_en_v2_1_open_weight.yml`;
- backend runner: `phase2/academic_transform/at0_en/src/at0_backend_runner.py`;
- live inference has NOT started yet.

Relevant commits:
- V2.1 amendment: `7d23fc436388d6bcc07e9a5919cbae7aff194e81`;
- model/runtime freeze: `04c982dfa52eb6b6f9e91b268574daedd4aecc23`;
- backend runner initial: `08602efa193fead7ab98a39ea4bc222a2314415f`;
- runner hardening/fix: `36f17e879faf991869093af7b6db7323cfbe346d`;
- workflow: `a376a6b7df93a5ca8c303072362d3eb97b54839c`;
- README state: `f2d8c96ac68c58c2b3b8d4f05a0186a0e2dd1e68`.

Exact next action: manually dispatch the frozen workflow once. The current ChatGPT GitHub connector cannot create a new workflow_dispatch run. After a run exists, the implementation agent can inspect jobs/logs/artifacts and continue. Do not modify the models, cases, prompts, arms, or resource policy before results.


## 2026-10-03 — AT0-EN V2.1 open-weight smoke gate blocker

Higher-model V2.1 removed the commercial/API requirement and authorized two distinct real model configurations with auditable execution and bounded resources. The preferred zero-extra-cost backend was implemented on public GitHub Actions with pinned open-weight GGUF models and pinned llama.cpp.

Frozen backend:
- Model A: Qwen3-4B-Instruct-2507 Q4_K_M, SHA-256 `2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e`
- Model B: SmolLM3-3B Q4_K_M, SHA-256 `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`
- llama.cpp commit: `b92761a515ea31e852e7fbc1fad5f874b46f3718`
- execution: public GitHub Actions CPU, sequential model/request execution, additional monetary cost USD 0

Smoke attempts:
1. run `37118121815`: Qwen PASS; SmolLM exhausted fixed completion budget in default extended-thinking mode. Frozen model-documented `/no_think` control.
2. run `37118533029`: Qwen PASS; SmolLM returned valid content but copied ambiguous smoke-only status union literally. Smoke-only fixture clarified; no AT0 evaluation prompt changed.
3. run `37118961886`: Qwen PASS; SmolLM generated semantically correct constrained revision, but wrapped valid JSON in one Markdown `json` fence. Strict raw `json.loads` parser rejected it.

Current frozen state:
- `30/30 PASS`
- language portability PASS
- Qwen smoke PASS
- SmolLM inference/hash/runtime PASS, strict raw-JSON conformance FAIL
- AT0 live evaluation matrix remains `0/48 NOT_RUN`
- no fourth attempt authorized
- `HW1-EN` and `DR` remain blocked
- Arabic remains frozen

Current blocker:
`BLOCKED_STRUCTURED_OUTPUT_CONFORMANCE`

Smoke report:
`phase2/academic_transform/at0_en/results/AT0_EN_V2_1_SMOKE_GATE_REPORT.md`

Higher-model review packet:
`phase2/academic_transform/at0_en/results/offline-preflight/HIGHER_MODEL_REVIEW_PACKET.md`

Escalation commit:
`fff49b26892f553c5e8e386ad7b4cd100d899720`

Exact next action: higher model must decide whether to keep strict raw JSON, authorize one narrowly defined outer-fence normalization in the transport layer, or authorize identical runtime JSON grammar/schema constraints. Do not change the parser/model or rerun smoke before this decision.


## 2026-10-03 — AT0-EN V2.1 live matrix CLOSED; V2.2 offline redesign authorized

The frozen 48-slot live matrix has completed and is now consumed/closed.

Run:
- workflow: `AT0-EN V2.1 Open-Weight Live Matrix`
- run id: `37123963805`
- trigger commit: `82e612adf16922e408954119e587c80a420721a0`
- conclusion: **SUCCESS**
- artifact id: `11275534001`
- artifact SHA-256: `842a9ff304c3ed9c854790ac8f205bfe156289b007b556cd06fa4aa19b609326`
- additional monetary cost: USD 0.00

Execution accounting:
- slots: 48/48
- logical calls: 71/72
- COMPLETE_RAW: 36
- FAILED_PARSE_OUTPUT: 3
- FAILED_PARSE_PLAN: 1
- FAILED_SCHEMA_OUTPUT: 8
- valid REVISE proposals among complete slots: 35
- one complete slot returned REVIEW without a revision

Structural completion:
- MODEL_A DIRECT: 11/12
- MODEL_A PLANNED: 12/12
- MODEL_B DIRECT: 3/12
- MODEL_B PLANNED: 10/12

Important interpretation:
- workflow execution PASS does not mean scientific/human-writing PASS;
- planning substantially improved MODEL_B structural adherence, but did not eliminate scientific drift;
- material drift examples were observed in claim strength, causality, scope/restriction, attribution and unsupported additions;
- only 18/35 structurally valid REVISE outputs were inside the experimental 0.85–1.15 word-count band; the band remains diagnostic, not a quality gate;
- two REVISE outputs were identical to source text;
- generator-declared content-unit mapping/protected status are not independent evidence;
- post-run replay found that permissive brace extraction did not rescue any actual V2.1 cell, but this parser behavior is still design debt for the next contract.

Frozen closure:
- `phase2/academic_transform/at0_en/results/AT0_EN_V2_1_LIVE_MATRIX_CLOSURE_LOCK.md`
- closure commit: `57eb18a49fd405c2ffa74cd5d482e629480f7553`

Frozen analysis / higher-model decision:
- `phase2/academic_transform/at0_en/results/AT0_EN_V2_1_RESULT_ANALYSIS.md`
- analysis commit: `1b38f64236f0b8e009dfc676273d64987db05b20`

Higher-model decision:
- KEEP English-first transaction architecture;
- REPAIR generation/output boundary and independent scientific verification;
- DO NOT rerun V2.1;
- DO NOT start HW1-EN yet;
- constrained JSON or generic planning must not be treated as scientific-safety mechanisms.

### Exact next authorized phase

`AT0-EN V2.2 OFFLINE CONTRACT REDESIGN`

No new model inference is authorized yet.

Required order:
1. define a minimal generation envelope (`status`, `revised_paragraph`, uncertainty);
2. move content-unit mapping, provenance packaging and protected-status decisions outside the generator;
3. add independent relation-level checks for numbers/units/groups/times/baselines, citations, negation/scope, hedge/modality, association-vs-causation, comparison direction, equation identity, restrictions/exclusions and new-information candidates;
4. narrow transport acceptance to versioned raw JSON / explicitly allowed single outer fence; remove first/last-brace salvage from the future acceptance contract;
5. keep DIRECT and PLANNED separate; plan is advisory and must itself pass checks;
6. keep length metrics diagnostic and make information-unit retention primary;
7. replay the frozen V2.1 outputs through V2.2 validators **offline only**, with no model calls;
8. freeze the V2.2 audit and return to higher-model review before any new inference or HW1-EN.

Arabic active research remains FROZEN. V4.2 Arabic remains closed and must not be rerun. Reserved Arabic populations remain closed.


## 2026-10-03 — AT0-EN V2.2 offline contract redesign FROZEN

V2.2 performed no new model inference. It replayed only the frozen V2.1 evidence from run 37123963805 / artifact 11275534001.

Frozen contract and audit:
phase2/academic_transform/at0_en/v2_2/AT0_EN_V2_2_OFFLINE_CONTRACT_AND_AUDIT.md

Independent validator:
phase2/academic_transform/at0_en/v2_2/at0_v2_2_validator.py

Core redesign:
- generation is separated from packaging and verification;
- future minimal envelope is status + revised_paragraph + uncertainty;
- model-generated content-unit mapping and protected-status are not safety evidence;
- relation-level deterministic checks cover quantities, group/value bindings, time/baseline relations, citation linkage, negation, hedges, causality, scope, equations/definitions, exclusions and new-information candidates;
- future transport contract must remove first/last-brace salvage;
- planning remains advisory, not a safety mechanism.

Validator calibration:
- 12/12 frozen source self-checks PASS;
- 13/13 adversarial mutations correctly fail PASS;
- total 25/25 PASS.

Frozen V2.2 replay:
- PASS_CANDIDATE: 32
- REJECT: 3
- REVIEW: 8
- REVIEW_ESCALATED: 1
- UNAVAILABLE: 4

Packaging diagnostic:
- 8 V2.1 structurally invalid cells had deterministic candidate text;
- 7/8 were PASS_CANDIDATE under the bounded V2.2 protection checks;
- 1/8 was REVIEW;
- this is diagnostic evidence of packaging burden and does not retroactively validate V2.1 cells.

Classification:
IMPROVED METHODOLOGICALLY / PERFORMANCE CLAIM UNCHANGED.

No new inference is authorized yet. HW1-EN remains blocked. Exact next action: independent red-team the V2.2 PASS_CANDIDATE false-negative risk and REJECT/REVIEW false-positive risk, then return to higher-model review before defining any new live protocol.

Arabic active research remains FROZEN; Arabic V4.2 remains CLOSED; reserved Arabic data remain CLOSED.


## 2026-10-03 — V2.2 independent red-team CLOSED; V2.3 offline relation-graph verifier required

A concurrent hardening commit appeared after the original V2.2 freeze and was preserved:
- `eeb6b2eec68a33e2b91a2d9e5380010ccc4705d0`
- added EN03 mechanism-conflation and EN04 assertion-weakening checks.

Current hardened validator SHA-256:
`749aa234e223faaecbb5e434ed4d165f856c6362fb9931ed560f657d77a80c2c`

Current frozen-output replay:
- run: `37130414885`
- artifact: `11276398612`
- artifact digest: `sha256:1e520e9b479854689c662dd2eef09eab0312716416b8df1958afde202a41b200`
- PASS_CANDIDATE: 30
- REJECT: 5
- REVIEW: 8
- REVIEW_ESCALATED: 1
- UNAVAILABLE: 4

Independent counterfactual red-team:
- run: `37130259582`
- artifact: `11276616582`
- artifact digest: `sha256:cee42205419c467dbecdeb0111dcc2109b996cb7855b2987693de5e169a2d960`
- benign paraphrase controls: 12/12 PASS
- adversarial relation-corruption tests: 24
- caught: 3/24
- escaped as PASS_CANDIDATE: 21/24
- constructed-attack escape rate: 87.5% (diagnostic only; not a population estimate)

Higher-model manual review of the 30 current real PASS_CANDIDATE outputs found one confirmed live false negative:
- `MODEL_A-EN01-DIRECT`: source `can support faster identification` became assertive `facilitating faster identification`.

Manual overlay:
- bounded PASS confirmed: 29
- false-negative → REVIEW: 1
- all 5 REJECT decisions defensible
- all 8 REVIEW decisions defensible as conservative escalation; REVIEW does not mean known error.

Frozen closure/decision:
`phase2/academic_transform/at0_en/v2_2/AT0_EN_V2_2_INDEPENDENT_REDTEAM_AND_ARCHITECT_DECISION.md`

Decision:
**MODIFY / V2.2 DIAGNOSTIC-ONLY / NO NEW LIVE / NO HW1-EN**

Exact next authorized phase:
`AT0-EN V2.3 OFFLINE RELATION-GRAPH VERIFIER`

V2.3 must replace lexical-presence proof with typed source relations covering argument binding, polarity, direction, scope, modality/evidential strength, causality, citations, equations, quantities and method order. Unresolved extraction must return REVIEW.

Pre-live minimum gates include:
- 12/12 benign controls acceptable;
- V2.2 REDTEAM_V1 catches 24/24 attacks;
- current 30 V2.2 PASS candidates receive frozen relation-level adjudication and EN01 no longer auto-passes;
- after V2.3 rules are frozen, create a fresh second counterfactual suite and use it as post-freeze red-team;
- no new inference until higher-model review after these offline gates.

Do NOT continue patching V2.2 case-specific regex as the primary architecture. Arabic remains FROZEN; Arabic V4.2 remains CLOSED; reserved data remain CLOSED.


## 2026-10-03 — AT0-EN V2.3 graph-driven scientific constraint gate CLOSED

V2.3 introduced a declarative `ScientificConstraintGraph` and one generic validator with no case-id-specific scientific branches.

Frozen files:
- `phase2/academic_transform/at0_en/v2_3/SCIENTIFIC_CONSTRAINT_GRAPH_V0_1.json`
- `phase2/academic_transform/at0_en/v2_3/at0_v2_3_graph_validator.py`
- `phase2/academic_transform/at0_en/v2_3/AT0_EN_V2_3_GATE_CLOSURE.md`

Repository commits:
- graph: `315958e469449a694beb2956b0feaf249245c28d`
- validator: `3d626a41c080345c5c01e7a90b0fabfae3c25b2c`
- gate closure: `e177577841d4203b56c8e1a25ec77dc54cb96444`

Frozen local identities:
- graph SHA-256: `840a94f067e44c852c92e5727345594877f96886e5889d5a24aaaa6ba444443f`
- generic validator SHA-256: `afee3852a1430d66990480b63623114682d0d79ef7f9aa0c2959315d52e1d2ef`
- V2.3 replay JSONL SHA-256: `917ad5eb60cb29ba44ad5f68e41bd634282cfb1c880e24bfeefb20acb4593ecf`

V2.3 replay remained exactly identical to final red-teamed V2.2:
- PASS_CANDIDATE: 26
- REJECT: 7
- REVIEW: 10
- REVIEW_ESCALATED: 1
- UNAVAILABLE: 4

Regression:
- 12/12 source self-checks PASS
- 19/19 known adversarial mutations NOT PASS
- total 31/31 PASS

Fresh counterfactual holdouts:
- holdout 1: 10/12; exposed EN04 density-direction and EN09 equation-operator gaps
- holdout 2: 11/12; exposed EN08 direction-binding gap
- after repairs, fresh holdout 3: 12/12
- holdout 3 SHA-256: `e51e0fe68d9afc990e3f37143d9994ffc5a9b4a89d267eae8eca2185a3336d70`

Important interpretation:
- the failure history is preserved; 12/12 is not presented without the preceding 10/12 and 11/12 failures;
- V2.3 improves architectural generality but does NOT establish general scientific fidelity;
- the original 12 English cases and V2.1 outputs are now development-consumed and must not be used to claim new independent improvement.

Higher-model decision:
- KEEP V2.3 architecture;
- DO NOT rerun the consumed 12-case live matrix;
- DO NOT authorize HW1-EN yet.

Exact next authorized gate:
`AT0-EN V2.4 — FRESH DEVELOPMENT POPULATION FREEZE`

Before any new inference:
1. create a fresh synthetic development population not derived from V2.1 outputs;
2. cover multiple academic domains and new semantic-risk classes;
3. freeze source text, content units, protected relations and constraint graph before model calls;
4. freeze the minimal generation envelope and transport policy;
5. run graph/mutation preflight before inference;
6. preregister transport, scientific-preservation, information-retention, unsupported-addition, usefulness/no-op, latency and cost metrics separately.

No new model inference is authorized until V2.4 population/protocol freeze is complete.


## 2026-10-03 — V2.3 closed; V2.4 hybrid claim verifier is the only active next gate

V2.2 independent red-team:
- run 37130259582
- artifact 11276616582
- digest sha256:cee42205419c467dbecdeb0111dcc2109b996cb7855b2987693de5e169a2d960
- 21/24 constructed attacks escaped (87.5%)
- 12/12 original safe controls passed
Conclusion: V2.2 rule-oriented verifier FAIL as standalone.

V2.3 assertion-graph redesign:
- frozen verifier commit c6180f97d1d98dbe9039728777572a65a9842aa4
- known external gate run 37132825529 SUCCESS
- artifact 11277318066
- digest sha256:f397133558e06e5ae2d78107b09d91cda87cf9e7f4714459356b19cef1815794
- all 24 previously known attacks rejected after redesign (development evidence only)
- benchmark defect found: SAFE_EN09 and frozen EN09 content_units omit a priority-direction relation present in source_text

Unseen holdout V1:
- verifier frozen before holdout
- run 37132991961
- artifact 11277443135
- digest sha256:dbec7fe4fa4cf3c4c7d6e49fd9102673557dfb24645d95f4d3bb231a752b2c3f
- attacks caught 9/12 = 75%
- attacks escaped 3/12 = 25%
- safe paraphrases accepted 1/12 = 8.33%
- safe non-pass 11/12 = 91.67%
Conclusion: V2.3 is useful as deterministic hard guard but FAILS as standalone verifier because paraphrase robustness is inadequate.

Closure:
phase2/academic_transform/at0_en/v2_3/AT0_EN_V2_3_CLOSURE.md

Only active next gate:
AT0-EN V2.4 HYBRID CLAIM VERIFIER

Frozen design:
phase2/academic_transform/at0_en/v2_4/AT0_EN_V2_4_HYBRID_VERIFIER_DESIGN.md

V2.4 combines:
1. full-source assertion graph;
2. deterministic hard guards;
3. independent semantic entailment/contradiction witnesses;
4. bidirectional source->candidate and candidate->source checks;
5. explicit REVIEW on disagreement/uncertainty.

Research candidates only; NOT yet authorized for inference:
- Vectara HHEM-2.1-Open (Apache-2.0)
- MoritzLaurer DeBERTa-v3-base-mnli-fever-anli (MIT)

Preregistered future confirmation gate:
- critical unsafe auto-pass = 0
- overall adversarial unsafe auto-pass <=5%
- safe VERIFIED_FOR_REVIEW coverage >=70%
- safe hard-reject <=10%
- no threshold tuning on confirmation

No semantic-model inference or new generator inference is authorized yet. HW1-EN remains blocked. Arabic active research remains FROZEN and V4.2 remains CLOSED.

Exact next action:
freeze exact semantic-model revisions/artifact hashes/runtime/license/resource manifest and build source-free V2.4 harness/preflight; return to higher-model review before any semantic inference.


## 2026-10-03 — Permanent staged-execution and progress-reporting agreement

User-approved permanent operating rule:

1. If a task is likely to be long, fragile, or tool-intensive and can be divided into scientifically valid checkpoints, **do not try to finish the whole workflow in one response**.
2. Complete one coherent checkpoint/stage, freeze its state/evidence, report the result, then stop and wait for the user's explicit `أكمل` before starting the next stage.
3. Do not split a stage if splitting would invalidate the experiment, corrupt an atomic operation, or violate a one-shot/consumption contract.
4. During long-running execution, use strictly sequential status checks only. Never create a second run merely because the first is still running.
5. Each meaningful progress update should report:
   - current stage/checkpoint;
   - approximate completion percentage based on known workflow steps or processed units;
   - completed work;
   - remaining work;
   - whether the run is healthy, blocked, failed, or genuinely stalled;
   - any new risk or deviation.
6. Do not claim false precision. If the backend exposes only coarse states, report a coarse percentage/range and explain its basis.
7. Do not provide an unreliable wall-clock completion promise. Prefer remaining steps/units and observed throughput when available.
8. If a tool/UI error or stream-recovery error occurs, resume from the last verified checkpoint; do not restart completed work and do not duplicate irreversible/one-shot operations.
9. At the end of each checkpoint, update this canonical handoff when the state materially changed.

This rule supplements the existing strictly-sequential execution rule and overrides any previous tendency to continue through many separable stages in one response.


## 2026-10-03 — AT0-EN V2.3 known-external assertion-graph gate CLOSED

This checkpoint is offline-only. No new model inference occurred.

Frozen execution:
- workflow: `AT0-EN V2.3 Assertion-Graph Offline Gate`
- run: `37134559401`
- run number: `5`
- trigger commit: `e7671e833a2177beaf56f21a74907d3613bc346c`
- conclusion: **SUCCESS**
- artifact id: `11278485956`
- artifact SHA-256: `f9a5858791ebeacf918b990a7eccf52d9690b5955c3cb65da00001a8279f4c9f`

Artifact-internal hashes:
- verifier: `d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da`
- test harness: `62e904874a0120bca5dcc69bf4ae099024c0c88e0bf7d9a6051edd742987235a`
- result JSON: `e1eddea894f504094520d2ac9d738ffb9444a357b0f7ef6b940fd144b620be6c`

Gate result:
- total: **36/36 PASS**
- valid safe controls: **11/11 PASS_CANDIDATE**
- `SAFE_EN09`: intentionally NOT PASS because that control omits a scientific relation present in source_text; the frozen EN09 content_units also omit that relation
- known adversarial attacks: **24/24 NOT PASS**

Important provenance:
- this is **NOT an untouched independent validation**;
- the 24 attacks came from the earlier V2.2 independent red-team that exposed 21/24 escapes (87.5%);
- V2.3 was redesigned in response to those attacks;
- therefore 36/36 is a **known-failure regression pass**, not unseen-generalization evidence.

Frozen closure report:
`phase2/academic_transform/at0_en/v2_3/AT0_EN_V2_3_KNOWN_EXTERNAL_GATE_CLOSURE.md`

Closure commit:
`76521dd148b47e712b3019c98f96827a7946f44b`

Scientific classification:
**IMPROVED METHODOLOGICALLY / KNOWN-FAILURE REGRESSION PASS / GENERALIZATION NOT ESTABLISHED**

Exact next authorized stage:
1. create and freeze a **second unseen adversarial holdout** independently from the V2.3 implementation;
2. freeze its labels before scoring;
3. do not modify V2.3 after opening/scoring that holdout;
4. run the frozen V2.3 verifier once against that holdout;
5. preserve failures and return for redesign if the holdout exposes escapes;
6. do not tune on the same holdout and then reuse it as untouched evidence.

No new model inference is authorized yet.
HW1-EN remains blocked.
Arabic active research remains FROZEN.
Arabic V4.2 remains CLOSED.
Reserved Arabic populations remain CLOSED.


## 2026-10-03 — Permanent quantitative progress / quality-delta reporting agreement

This supplements all earlier ACAD_PASS operating agreements.

For every meaningful checkpoint, progress update, phase closure, or result review, report all of the following when evidence allows:

1. **Result delta versus the nearest valid comparable checkpoint**
   - state whether the result is `IMPROVED`, `WORSENED`, `MIXED`, or `NOT COMPARABLE`;
   - report the magnitude numerically (percentage points, relative %, counts, error-rate change, coverage change, escape-rate change, etc.) only when the denominator/construct is comparable;
   - never manufacture a percentage merely to satisfy reporting.

2. **Current-stage completion**
   - report an approximate percentage grounded in known workflow steps, processed units, or explicit gates;
   - state what has completed and what remains;
   - avoid false precision.

3. **Whole-system completion**
   - report a coarse architectural/research completion estimate for ACAD_PASS as a whole;
   - this is a planning estimate, not a scientific metric;
   - update it only when a meaningful architecture/research milestone changes the estimate;
   - always list the major unfinished blocks that dominate the remaining work.

4. **Remaining-work outlook**
   - report remaining phases/gates, principal blockers, and observed throughput where useful;
   - do **not** give an unreliable wall-clock completion promise or guaranteed hours/days-to-finish estimate;
   - if a current backend run exposes measured throughput, it may be reported as observed throughput only.

5. **Research / brainstorming**
   - retain the permanent rule requiring fresh rigorous research and maximum-effort brainstorming at the START and END of substantive phases;
   - challenge assumptions, alternatives, construct validity, contamination, and negative evidence.

6. **Higher-model consultation**
   - use higher-model review when architecture, benchmark design, experimental validity, frozen-result interpretation, safety-gate changes, or other high-stakes decisions justify it;
   - routine implementation remains delegated to the implementation agent;
   - if no separate stronger-model tool is actually available in the current environment, explicitly record that limitation rather than pretending a consultation occurred.

7. These quantitative/progress reports are in addition to the existing staged-execution rule: complete one coherent checkpoint, freeze evidence, report, then stop for explicit `أكمل` when the remaining work is separable.



## 2026-10-03 — Stream/timeout mitigation rule

To reduce repeated ChatGPT stream-recovery / prolonged-thinking UI failures:

1. Prefer **micro-checkpoints** for long ACAD_PASS work.
2. For a long or tool-heavy stage, default to roughly **2–4 sequential tool operations per response**, then report and stop for explicit `أكمل`, unless an atomic/one-shot operation requires finishing in the same response.
3. Do not perform repeated long polling loops in one response. If a remote workflow is still running after one meaningful status inspection, report its exact state/progress and stop; continue polling only after the user's next `أكمل`.
4. Preserve the last verified checkpoint before every stop so a UI/stream failure never causes a restart.
5. If the conversation itself becomes very long and UI failures recur, prefer a **new chat inside the same ACAD_PASS project**, beginning by reading the canonical `RESUME_HERE.md`, rather than continuing an unstable very-long thread.
6. A UI/stream timeout is not evidence that GitHub/experiment execution failed. Verify the external run before taking any recovery action.
7. Do not duplicate triggers, rerun consumed experiments, or restart irreversible work because of a ChatGPT UI timeout.



## 2026-10-03 — Permanent error-resilient execution mode

Because the user repeatedly encounters ChatGPT UI/stream errors such as `Our systems are thinking a bit more about this request before responding`, stream-recovery timeouts, and `A network error occurred. Please check your connection and try again.`, ACAD_PASS uses an error-resilient execution mode by default.

Rules:

1. Prefer shorter coherent execution stages over long uninterrupted tool chains.
2. For tool-heavy work, freeze a repository/evidence checkpoint as early as scientifically safe before continuing to optional analysis.
3. After a meaningful checkpoint is complete, report and stop for explicit `أكمل` when the next work is separable.
4. Avoid unnecessary polling, duplicate fetches, or long user-visible streaming responses.
5. Keep tool calls strictly sequential and avoid very large single responses when a compact checkpoint report is sufficient.
6. Before any irreversible/one-shot/consumed operation, ensure the current state is durably recorded so a UI/network interruption cannot force a restart.
7. If a ChatGPT stream/network error interrupts the conversation, resume from the last verified repository/run/hash checkpoint. Never repeat completed one-shot work merely because the UI response failed.
8. When a long external workflow is running, progress updates should use coarse milestones and measured step counts rather than repeated rapid polling.
9. If the same chat becomes operationally unstable or excessively long, a new chat may continue by reading `RESUME_HERE.md`; no scientific phase should be restarted solely because the conversation changed.
10. UI/network errors are not themselves evidence of scientific or workflow failure; verify the external run/repository state before taking corrective action.



## 2026-10-03 — SECOND_UNSEEN_HOLDOUT_V1 freeze checkpoint CLOSED

This stage is **100% COMPLETE**.

No V2.3 scoring and no model inference occurred.

Frozen identities:
- inputs SHA-256: `b1633df5e0418082a990945dfc92a267f6cdc8c943b385d7edc2d8b9181f551c`
- labels SHA-256: `9936377336708dbeaf88b7ee83a8ae5fb4272013129041332094dfa625345a9b`
- V2.3 verifier SHA-256: `d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da`
- source cases SHA-256: `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

Integrity:
- total inputs: 36
- total labels: 36
- unique IDs: 36
- SAFE_CONTROL: 12
- ADVERSARIAL: 24
- 2 adversarial cases per EN01–EN12
- input/label ID order alignment: PASS
- all recorded hashes match manifest: PASS

Freeze lock:
`phase2/academic_transform/at0_en/v2_3/holdout/SECOND_UNSEEN_HOLDOUT_V1_FREEZE_LOCK.md`

Freeze-lock commit:
`7bf208d1824596b0e50e235f1d14e90a748d0ef0`

Operational note:
a dedicated GitHub Actions integrity workflow exists, but no workflow run was exposed after a non-semantic trigger. This was recorded as an operational tooling issue only. Repository-level hash/count/ID integrity verification passed. Do not claim an Actions PASS for that workflow.

End-stage research supports the current design:
- scientific revision evaluation needs correctness-sensitive/task-specific evaluation;
- dynamic/temporally refreshed benchmarks reduce contamination/staleness risk;
- factuality metrics can be unstable under meaning-preserving paraphrases, supporting 12 SAFE_CONTROL paraphrases alongside adversarial cases.

Quality delta:
- methodological status: **IMPROVED**
- scientific performance delta: **NOT YET MEASURED**
- last comparable robustness evidence remains V2.2 21/24 attack escapes (87.5%) versus V2.3 0/24 escapes on the same known attacks, i.e. -87.5 percentage points on known attacks only.

Whole ACAD_PASS completion estimate:
**approximately 20% ±5%**, planning estimate only.

Exact next authorized stage:
`SECOND_UNSEEN_HOLDOUT_V1 ONE-SHOT SCORE`

Only after explicit `أكمل`:
1. bind frozen verifier SHA;
2. bind frozen input/label hashes;
3. produce predictions before evaluation;
4. score once;
5. freeze all errors;
6. do not tune V2.3 and reuse this holdout as untouched evidence.

No model inference is required for this score.
HW1-EN remains blocked.
Arabic active research remains FROZEN.
Arabic V4.2 remains CLOSED.
Reserved Arabic populations remain CLOSED.


## 2026-10-03 — SECOND_UNSEEN_HOLDOUT_V1 one-shot score CLOSED

This stage is **100% COMPLETE** and the holdout is now consumed development evidence.

One-shot workflow:
- run: `37136722184`
- trigger commit: `44728dfb5fcf3e1bf211ba330b618741c2d382de`
- conclusion: SUCCESS (execution only)
- artifact id: `11278888488`
- artifact SHA-256: `8b66dbf18b0b7f0939f66754c803b3753f1bc9a1cc912051129ecbeca77f5ae9`

Frozen evidence:
- verifier SHA-256: `d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da`
- inputs SHA-256: `b1633df5e0418082a990945dfc92a267f6cdc8c943b385d7edc2d8b9181f551c`
- labels SHA-256: `9936377336708dbeaf88b7ee83a8ae5fb4272013129041332094dfa625345a9b`
- source cases SHA-256: `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`
- predictions SHA-256: `e36a99873e7f7d87a63cc77c928109bf844a718ca20f5b09d5287378be081c25`
- score detail SHA-256: `2eea29e5f6e3e738484c2a3d723d649e2777c1aeff5f956902700092b2d23e4c`
- score summary SHA-256: `854b6ebbe9c3491d0d8957bde9b4f1d13d4327c5ca82e36616dc9b92114c7955`

Pre-registered result:
- Safety gate: **FAIL**
- Usability gate: **FAIL**
- combined: **BOTH_FAIL**

Metrics:
- adversarial caught: 15/24 = **62.5%**
- adversarial escaped: 9/24 = **37.5%**
- safe controls accepted: 3/12 = **25%**
- safe controls non-pass: 9/12 = **75%**
- exact binary accuracy: 18/36 = **50%**
- balanced accuracy: **43.75%**

Escaped adversarial IDs:
- H2-EN01-A1 scope binding shift
- H2-EN02-A2 deployment-status invention
- H2-EN03-A1 percentage/metric rebinding
- H2-EN04-A2 density-direction shift
- H2-EN10-A1 grouping-interval rebinding
- H2-EN10-A2 metadata-scope reduction
- H2-EN11-A1 forwarding-scope expansion
- H2-EN11-A2 timestamp substitution
- H2-EN12-A1 metric-label swap

Dominant failure:
**relation rebinding under lexical preservation**.

Safe-control failures show the opposite problem:
**lexical/paraphrase brittleness, regex-window contamination, and negation-scope errors**.

Quality delta:
- versus V2.3 known-failure regression: escape 0% -> 37.5%, **+37.5 pp worse on a new population**; valid safe acceptance 100% -> 25%, **-75 pp descriptively**. These are not same-population comparisons and quantify a generalization gap rather than a within-population regression.
- versus V2.2 independent red-team: escape 87.5% -> 37.5%, **-50 pp descriptively**, but attack populations differ, so this is not a valid causal/same-population improvement estimate.

Frozen score summary:
`phase2/academic_transform/at0_en/v2_3/holdout/results/SECOND_UNSEEN_HOLDOUT_V1_SCORE_SUMMARY_FROZEN.json`
commit:
`c12f60e694c3d2fc3c849f1295d3c07197de70dd`

Closure report:
`phase2/academic_transform/at0_en/v2_3/holdout/SECOND_UNSEEN_HOLDOUT_V1_SCORE_CLOSURE.md`
commit:
`46aeaad40804cd48f89bf9ba44f3afb6327042d7`

Scientific disposition:
**WORSENED ON UNSEEN GENERALIZATION / BOTH_FAIL**

The holdout is now:
`CONSUMED DEVELOPMENT EVIDENCE / NOT UNTOUCHED HOLDOUT`

Do NOT:
- rerun this holdout for quality;
- patch V2.3 case-by-case and reuse this holdout as untouched;
- start HW1-EN;
- infer general scientific fidelity.

Fresh end-stage research supports moving from handcrafted lexical assertions toward atomic claim decomposition + explicit relation verification while warning that decomposition itself can introduce noise and must be calibrated.

Separate stronger-model consultation is not available as a tool in this chat environment; no external higher-model review is claimed.

Exact next authorized stage:
`AT0-EN V2.4 — GENERALIZED SCIENTIFIC ASSERTION REPRESENTATION`

V2.4 must be offline first and target:
- source-derived atomic assertions;
- subject/predicate/object/value/unit/qualifier/modality/polarity/scope/temporal/population/citation/equation binding;
- explicit extraction uncertainty;
- contradiction and addition detection on normalized relations;
- paraphrase-tolerant semantic matching separated from deterministic scientific invariants;
- no sole dependence on regex, LLM, NLI, or self-reported mappings.

Current stage completion:
**100%**

Whole ACAD_PASS planning completion estimate:
**approximately 20% ±5%**

Major unfinished blocks:
V2.4 redesign, future new untouched validation, verifier readiness review, HW1-EN, cross-domain scientific fidelity, DOCX fidelity, voice, detector robustness, long-document evaluation, product/commercial validation.

No reliable wall-clock completion promise is available because V2.4 can expose further redesign needs.


## 2026-10-03 — Permanent higher-model consultation budget agreement

This supplements all earlier ACAD_PASS execution rules.

1. Use the higher model **only for genuine consultation**, not for routine execution.
2. Higher-model consultation is justified only when the current task materially benefits from:
   - architecture review;
   - experiment/benchmark design review;
   - construct-validity review;
   - frozen-result interpretation;
   - high-stakes go/no-go or safety-gate decisions;
   - difficult research synthesis or red-team of a proposed design;
   - other decisions where an independent stronger reviewer can materially change the direction.
3. Do **not** delegate implementation work to the higher model when the implementation agent can perform it. This includes:
   - coding;
   - repository edits;
   - ordinary debugging;
   - running tests;
   - routine data inspection;
   - workflow execution;
   - artifact hashing/freezing;
   - standard literature collection;
   - routine metric calculation;
   - ordinary documentation updates.
4. Before requesting higher-model consultation, the implementation agent should first complete all work it can reasonably do itself and reduce the consultation to the smallest high-value decision surface.
5. When higher-model consultation is genuinely needed:
   - prepare a concise consultation prompt;
   - provide only the minimum files/evidence required;
   - clearly state that the higher model is acting as **consultant/reviewer only**;
   - explicitly instruct it **not to implement**, modify repositories, generate code patches, rerun experiments, or perform work that the implementation agent can do;
   - ask it to return findings, risks, alternatives, decision criteria, and recommendations that the implementation agent can execute.
6. The user will manually send the consultation packet to the higher model and return its response to this chat.
7. Do not repeatedly consult the higher model for the same decision unless new evidence materially changes the question.
8. Consultation should be budget-aware: use one focused review packet rather than many fragmented prompts whenever possible.
9. If higher-model consultation is not genuinely necessary, do not request it merely because it is available.
10. When consultation is requested, record:
    - why it is needed;
    - the exact question(s);
    - the evidence packet supplied;
    - what remains for the implementation agent to execute afterward.



## 2026-10-03 — AT0-EN V2.4 architecture kickoff / consultation checkpoint

Stage status:
**100% COMPLETE FOR ARCHITECTURE-KICKOFF CHECKPOINT**
Implementation status:
**NOT STARTED / NOT AUTHORIZED**

Latest evidence remains V2.3 second unseen holdout:
- adversarial escape: 9/24 = 37.5%
- safe automatic acceptance: 3/12 = 25%
- BOTH_FAIL
- balanced accuracy: 43.75%

V2.4 direction selected for review:
**Hybrid Scientific Assertion Frame + Assertion Relation Graph**

Rejected as sole architectures:
- more case-specific regex/templates;
- plain SVO/OpenIE triples;
- full generic AMR/SRL as the primary safety contract.

Proposed core:
- source-derived atomic assertion frames with exact provenance;
- subject/predicate/object plus value, unit, direction, conditions, time, population, baseline, modality, evidential strength, polarity, causality, scope, exclusions, citations, equations, symbol bindings and extraction uncertainty;
- assertion relation graph for explicit role ownership and relation binding;
- deterministic invariant lane for exact scientific anchors;
- semantic relation lane for paraphrase, role alignment, scope, modality, causality/association and negation;
- critical uncertainty -> REVIEW;
- source and candidate extracted independently before alignment;
- no single LLM/NLI/embedding score as sole safety oracle;
- source extraction itself must be validated before end-to-end verification.

Architecture candidate:
`phase2/academic_transform/at0_en/v2_4/ARCHITECTURE_CANDIDATE_V1.txt`
commit:
`9b6e1e4f241501b26c298c41f3b4daa641f82072`

Fresh research reviewed:
- ACL 2025 claim extraction / Claimify: evaluate coverage and decontextualization; abstain under ambiguity;
- ACL 2025 decomposition: atomicity must align with verifier behavior;
- EMNLP 2025 DnDScore: decomposition and decontextualization interact;
- EMNLP 2025 SciEvent: scientific event/argument representation is more appropriate than narrow entity-relation extraction for multi-domain scientific context;
- NAACL 2025 Verify-in-the-Graph: graph representation plus disambiguation supports complex claim verification;
- ACL 2026 factuality stress testing: paraphrase and dense claims destabilize existing metrics;
- Findings ACL 2025 Verify with Caution: factuality evaluators can disagree and bias against paraphrase.

Higher-model consultation:
**JUSTIFIED NOW** because this is an architecture/construct-validity decision affecting the entire next verifier generation.

Budget rule applies:
- consultant only;
- no coding;
- no repo edits;
- no experiments;
- no routine implementation;
- implementation agent executes all routine work afterward.

Consultation packet:
`phase2/academic_transform/at0_en/v2_4/HIGHER_MODEL_CONSULTATION_PACKET_V1.txt`
commit:
`fd27c9829c62dea22c22bc8951ffc250b9dca519`

Files to give the higher model:
1. `phase2/academic_transform/at0_en/v2_4/ARCHITECTURE_CANDIDATE_V1.txt`
2. `phase2/academic_transform/at0_en/v2_3/holdout/SECOND_UNSEEN_HOLDOUT_V1_SCORE_CLOSURE.md`

Do not send unnecessary repository files unless the consultant explicitly identifies a missing dependency.

Quality delta in this checkpoint:
- experimental result: **NOT CHANGED**
- architecture status: **IMPROVED METHODOLOGICALLY**
- no quantitative performance gain may be claimed because V2.4 has not been implemented or scored.

Whole ACAD_PASS planning completion estimate:
**approximately 20% ±5%**

Exact next action:
WAIT for the user's returned higher-model consultation response.
Then:
- evaluate the review;
- accept/reject each recommendation;
- freeze V2.4 architecture decision;
- only after that authorize a small offline implementation prototype.



## 2026-10-03 — V2.4 higher-model review integrated / architecture frozen

Checkpoint status:
**100% COMPLETE**

Higher-model verdict:
`PROCEED_WITH_CHANGES`

Project integration:
- 8/8 required architecture changes ACCEPTED
- 5/5 top risks accepted as active risks
- validation plan ACCEPTED
- do-not-do list ACCEPTED
- no recommendation rejected outright

Clarifications:
1. `INVALID_VERIFICATION` is transaction-level and does not mean the candidate is scientifically false.
2. deterministic anchor/token presence does not make semantic ownership deterministic.

Final frozen architecture:
`phase2/academic_transform/at0_en/v2_4/AT0_EN_V2_4_FROZEN_ARCHITECTURE_V2.md`

Final architecture commit:
`14db09677fb6df90e6aa688601cfe071e8138ee6`

Consultation response:
`phase2/academic_transform/at0_en/v2_4/HIGHER_MODEL_CONSULTATION_RESPONSE_V1.md`
commit:
`758efae6af159a5fa9e9f50021357db1c069724c`

Consultation decision matrix:
`phase2/academic_transform/at0_en/v2_4/CONSULTATION_DECISION_MATRIX_V1.md`
commit:
`046f5aca0f4af85eb725c1bedf9f73dc31fc6245`

Architecture review closure:
`phase2/academic_transform/at0_en/v2_4/AT0_EN_V2_4_ARCHITECTURE_REVIEW_CLOSURE.md`
commit:
`4063174aa6919f0072189193203819aef6b7feb2`

Important final architecture rules:
- small task-specific Scientific Assertion Frame + Assertion Relation Graph;
- explicit ownership relations for values, units, conditions, time, population, baseline, citations, equations and symbols;
- explicit scope/operators including negation, modality, evidence strength, causality, exceptions, quantifiers, AND/OR, proposed/implemented/observed/hypothetical status;
- deterministic and semantic lanes separated;
- deterministic failure cannot be overridden by semantic evidence;
- source extraction frozen once per source version before candidate extraction;
- candidate extracted independently;
- joint-context alignment allowed only after both extractions are frozen;
- independent coverage checks;
- bidirectional one-to-one / one-to-many / many-to-one alignment;
- four outcomes: PASS_CANDIDATE / REJECT / REVIEW / INVALID_VERIFICATION;
- critical uncertainty blocks automatic PASS;
- every critical PASS/REJECT dependency requires a traceable minimal evidence rationale;
- future document context may reference table cells, captions, titles, footnotes and equation blocks as explicit evidence nodes;
- no ID-specific patching against consumed V2.3 holdout;
- no untouched benchmark until V2.4 pipeline freeze.

Fresh end-stage research reinforced:
- correct final labels are insufficient without faithful rationale/evidence alignment;
- coreference, temporal and causal event relations remain difficult for current models;
- paraphrase robustness remains a major factuality failure mode.

Performance delta:
- experimental performance: UNCHANGED
- adversarial escape remains 9/24 = 37.5%
- safe automatic acceptance remains 3/12 = 25%
- no V2.4 performance claim yet

Methodological delta:
**IMPROVED**

Current-stage completion:
**100%**

Whole ACAD_PASS planning completion estimate:
**approximately 20% ±5%**

Next authorized stage:
`AT0-EN V2.4 GATE 0 — OFFLINE SCHEMA / CRITICALITY / OUTCOME CONTRACT PROTOTYPE`

Gate 0 scope:
- machine-readable schema;
- criticality rules;
- four outcome rules;
- small fixed development reference material;
- initially no model inference;
- no new generation;
- no HW1-EN;
- no untouched holdout.

Higher-model budget rule remains active: consult only for genuinely high-value architecture/validity decisions; routine implementation stays with the implementation agent.


## 2026-10-03 — AT0-EN V2.4 Gate 0 CLOSED

Checkpoint status:
**100% COMPLETE**

Final workflow:
`AT0-EN V2.4 Gate 0 Contract`

Final run:
`37141161540`

Trigger commit:
`61761190dccc191c587896ffb220e8b6cee0c7ce`

Conclusion:
**SUCCESS**

Artifact:
- id: `11280860872`
- SHA-256: `4d34010a29f2cb1d08308d3e2a008d6b42395f6844401f6e1d68175ff7f606f9`

No model inference occurred.

Final contract test:
- 322/322 checks PASS
- 6 development-only cases
- 28 gold assertions
- 33 gold relations
- cases: EN04, EN05, EN06, EN07, EN09, EN12

Frozen hashes:
- schema: `74c20c219e8cc2cc240792b772e6f12ca0c60d79b7d2772e44fd06a3fafaeecf`
- criticality: `49dfdfc6c0f3226161db0b219d3adc7ecd17e04070a6f5bd0367deb579ddeb1c`
- outcome contract: `aeff55ec0d5c10a949afc2f86a5eae46e610043f3885497643561b17aa669905`
- development reference: `c5fc21cf8ea60f0bd4b403b3a6e9220be33c1d390283a71f0365751ea54ed303`
- contract test: `844ea8fb5ab1ec68ca35460c7ffe5fd982bce5f098dfe4b99126ecad6f7c3199`
- source cases: `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

Final Gate 0 files:
- `phase2/academic_transform/at0_en/v2_4/gate0/SCIENTIFIC_ASSERTION_GRAPH_SCHEMA_V1.json`
- `phase2/academic_transform/at0_en/v2_4/gate0/CRITICALITY_RULES_V1.json`
- `phase2/academic_transform/at0_en/v2_4/gate0/OUTCOME_CONTRACT_V1.json`
- `phase2/academic_transform/at0_en/v2_4/gate0/GATE0_DEV_REFERENCE_V1.jsonl`
- `phase2/academic_transform/at0_en/v2_4/gate0/check_gate0_contract.py`

Gate 0 closure:
`phase2/academic_transform/at0_en/v2_4/gate0/AT0_EN_V2_4_GATE0_CLOSURE.md`
commit:
`a59afc1edd28c5f56e049b94540121d13640e8f1`

Important repairs discovered before closure:
- missing architecture-required assertion fields were added to schema;
- development reference relation labels were aligned with schema;
- contract-test source path fixed;
- frame/graph dual-source-of-truth risk was identified and closed.

Canonicality policy:
`FRAME_AND_GRAPH_MUST_AGREE`

A critical frame/graph disagreement -> `INVALID_VERIFICATION`.

Frozen outcome precedence:
1. INVALID_VERIFICATION
2. REJECT
3. REVIEW
4. PASS_CANDIDATE

Development reference is:
`DEVELOPMENT-ONLY / NOT HOLDOUT / NOT PERFORMANCE EVIDENCE`

Quality delta:
- experimental performance: **UNCHANGED**
- last verifier evidence remains V2.3: adversarial escape 37.5%; safe acceptance 25%; BOTH_FAIL
- methodological status: **IMPROVED**
- no quantitative V2.4 performance improvement may be claimed

Current-stage completion:
**100%**

Whole ACAD_PASS planning completion:
**approximately 22% ±5%**

Exact next authorized stage:
`AT0-EN V2.4 GATE A — SOURCE/EXTRACTOR PROTOTYPE AND VALIDATION PREPARATION`

Gate A scope:
- offline source-side extraction only;
- deterministic anchors + provenance first;
- output must conform to frozen Gate 0 schema;
- prepare extractor validation against the 6-case development reference;
- measure coverage, false additions, atomicity, ownership/role binding, context/decontextualization, polarity/modality and abstention;
- no end-to-end candidate verification yet unless Gate A later authorizes it.

Not authorized:
- new live generation
- HW1-EN
- new untouched holdout
- scientific-fidelity performance claims
- consumed-holdout ID patching

Higher-model consultation not required at Gate A start unless a new architecture/construct-validity issue appears.


## 2026-10-03 — AT0-EN V2.4 Gate A1 CLOSED

Checkpoint status:
**100% COMPLETE**

Scope:
deterministic source-anchor inventory + exact provenance only.
No assertion decomposition, semantic ownership, relation alignment, candidate verification, or model inference.

Workflow:
`AT0-EN V2.4 Gate A1 Deterministic Anchors`

Run:
`37142176334`

Trigger commit:
`a55c3bfd83b2131db3b4ab8f1e060a4b09d37cb0`

Artifact:
- id: `11280995699`
- SHA-256: `dc8ed8978f09dc80281f386a871a1f7487286493069463b45a08a4cd21d80e5b`

Development reference:
- cases: EN04, EN05, EN06, EN07, EN09, EN12
- gold deterministic anchors: 35
- EN05 is a zero-anchor negative control

Result:
- predicted: 35
- TP: 35
- FP: 0
- FN: 0
- precision: 100%
- recall: 100%
- F1: 100%
- exact provenance span checks: 35/35
- semantic ownership assessed: NO

Frozen A1 hashes:
- extractor: `65d0da4b32b8297dd58ba6108fb2a49e0cb96dfa726ce270f0382318919e20db`
- reference: `49e1d4d4029c5f7db0c49242d316ff1e6d3e6e2c0cdba6fff3812ea4d601ed4e`
- validation script: `5848099971ec594b448e5a7ab72e69daa0cb87c704c4bacaa2fb15eb89d7b9d6`
- predictions: `436dff2f365b92797f4f401fab97bf94dbba1b04a69ff1f8bf3b212d6fe877f3`
- summary: `bc7222b85c7cd52e4a40f3055822700e482a1c3d40597b4461f6f947583654ab`

A1 closure:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A1_CLOSURE.md`
commit:
`d6c8d396b19be4b6cfb1768eb86e2ef8bcf3ac01`

### Gate 0 repairs discovered by A1

A1 exposed two contract defects:
1. no top-level pre-ownership anchor inventory;
2. no top-level evidence-span provenance inventory.

These were repaired.

Canonical policies now include:
- `EXTRACT_BEFORE_OWNERSHIP`
- `GLOBAL_EVIDENCE_SPANS_ARE_CANONICAL`
- `FRAME_AND_GRAPH_MUST_AGREE`

Canonical Gate 0 repair validation:
- run: `37142006598`
- artifact id: `11280702653`
- artifact SHA-256: `0f97953ed6a5a09b21b24c3578cb9134d29194a413da4fd3e3072a209401e2cb`
- checks: 326/326 PASS

Canonical Gate 0 hashes after A1 repair:
- schema: `df986f759a114bd86525b84f00f8d2f362d71bb31546441992291d21c5ebd69f`
- criticality: `1599bf6bdb10afd462ba45a422b3e276a4ddbb47656d3d6047a0ff9b39acc48d`
- outcome contract: `aeff55ec0d5c10a949afc2f86a5eae46e610043f3885497643561b17aa669905`
- development reference: `c5fc21cf8ea60f0bd4b403b3a6e9220be33c1d390283a71f0365751ea54ed303`
- contract test: `d3315f86490d33c61ce311cf5efa9480fe70b2e79f9c59d8a6b81621935e1c7f`

Repair addendum:
`phase2/academic_transform/at0_en/v2_4/gate0/GATE0_A1_CONTRACT_REPAIR_ADDENDUM.md`
commit:
`2c1fa17219f9b700336c27b3cc586f4044bbb4c5`

The earlier Gate 0 closure remains historical provenance; these hashes supersede its schema/criticality/test identities.

### A1 interpretation

Classification:
`PASS WITH NARROW DEVELOPMENT SCOPE`

Do NOT treat 100% as general extraction performance.

Known limitations:
- only 35 hand-annotated deterministic anchors;
- six already-consumed synthetic development cases;
- regex catalog is not comprehensive for real academic citation/equation/unit styles;
- word-number hyphenated durations, implicit/scattered arguments, and semantic role ownership are not established by A1;
- exact-span scoring is appropriate for explicit deterministic anchors only and must not be the sole semantic-argument metric later.

Fresh end-stage research:
- Claimify: coverage/decontextualization/ambiguity must be measured independently;
- Event Pattern-Instance Graph: inter-argument role relations matter;
- BEMEAE and REGen: exact span match can penalize semantically valid event arguments.

Quality delta:
- system-level scientific-fidelity performance: UNCHANGED
- last end-to-end evidence remains V2.3: 37.5% adversarial escape, 25% safe acceptance, BOTH_FAIL
- A1 component metric: 100% precision / 100% recall, with no directly comparable prior A1 baseline
- methodological status: IMPROVED

Completion:
- Gate A1: 100%
- Gate A overall: approximately 35%
- whole ACAD_PASS planning estimate: approximately 23% ±5%

Exact next authorized checkpoint:
`AT0-EN V2.4 GATE A2 — SOURCE ASSERTION DECOMPOSITION + ABSTENTION PROTOTYPE`

A2 scope:
- source side only;
- use global evidence and anchor inventories;
- extract source assertions into frozen schema;
- preserve provenance;
- represent UNCERTAIN/AMBIGUOUS explicitly;
- begin source coverage accounting;
- no candidate-text alignment or end-to-end verifier claim.

Higher-model consultation is not required at A2 start unless a new architecture/construct-validity issue appears.


## 2026-10-03 — AT0-EN V2.4 Gate A2 CLOSED

Checkpoint status:
**100% COMPLETE**

Final workflow:
`AT0-EN V2.4 Gate A2 Source Assertions`

Final run:
`37142951015`

Trigger commit:
`cb5513ceb03e077e9136fed33c44905512579436`

Artifact:
- id: `11281086502`
- SHA-256: `09bb99ecccac334f17275f4f81e8976e4afd4d58a579d584245c4d99b5230468`

No model inference occurred.
A2 extractor/scorer did not read the gold development reference.

Final A2 structural result over all 12 frozen synthetic source cases:
- source sentences: 47
- assertion candidates: 50
- anchors inherited from A1: 43
- structural sentence representation: 47/47 = 100%
- exact evidence/provenance span checks: 140
- relations emitted: 0
- semantic anchor ownership assessed: NO
- semantic coverage claimed: NO
- coverage status: UNKNOWN_BY_DESIGN

Extraction status:
- CERTAIN: 19/50 = 38%
- UNCERTAIN: 13/50 = 26%
- AMBIGUOUS: 18/50 = 36%
- non-CERTAIN / abstention-like: 31/50 = 62%

Final hashes:
- source assertion extractor: `32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`
- A2 structural validator: `c8b0ca44341f3c8c48e19ff078afa4fcbdd2be97a32daf529e0f7310d7712dd8`
- final predictions: `12bb579866311320701458afdb826daddd7007cb70a56d032ea0f404e7f1f8c8`
- final summary: `1d474a292e9d1428101eea3c94a6fce996b7b69ff894dc9952597b45380e1e68`
- canonical schema: `df986f759a114bd86525b84f00f8d2f362d71bb31546441992291d21c5ebd69f`
- source cases: `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

Frozen summary:
`phase2/academic_transform/at0_en/v2_4/gate_a/results/GATE_A2_SOURCE_ASSERTION_SUMMARY_FROZEN.json`
commit:
`a8391a9f71fa3dd2b596e1ab06528017aaac7cdc`

A2 closure:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A2_CLOSURE.md`
commit:
`0f8050f37ffd492d27cd732833eba1a194c90e5e`

### Important negative evidence preserved

Initial A2 run:
- run: `37142805075`
- artifact id: `11281051423`
- artifact SHA-256: `d77fb3708abdc5086723814a15b5c1394c11ba74a9dd0d068978ca17d6c1d453`

The workflow initially passed structurally, but manual red-team found a critical sentence-segmentation defect:
decimal values such as 42.0, 51.5, 46.2, 49.8 and 4.2 were split at the decimal point, producing artificial assertion fragments and false confidence.

Repair:
- decimal-safe sentence segmentation;
- regression guard preventing sentence/assertion boundaries inside digit-dot-digit values;
- conservative abstention for embedded propositions such as `found that`;
- conservative abstention for `whether` / `rather than` scope structures.

Initial -> final on identical 12 source cases:
- sentence spans: 52 -> 47
- assertion candidates: 55 -> 50
- five artificial decimal fragments removed
- CERTAIN: 21 -> 19
- UNCERTAIN: 12 -> 13
- AMBIGUOUS: 22 -> 18
- non-CERTAIN rate: 34/55 = 61.82% -> 31/50 = 62.0%
- false decimal-boundary defects observed: 5 -> 0 under regression guard

Interpretation:
`PASS AS A CONSERVATIVE STRUCTURAL SOURCE-EXTRACTION PROTOTYPE / SEMANTIC ACCURACY NOT ESTABLISHED`

Do NOT interpret 100% structural sentence representation as semantic coverage.

A2 does not establish:
- assertion coverage accuracy;
- atomicity accuracy;
- subject/predicate/object accuracy;
- decontextualization correctness;
- semantic ownership;
- polarity/modality/causality accuracy;
- abstention calibration;
- end-to-end scientific fidelity.

The 62% non-CERTAIN rate is diagnostic only. A3 must determine whether this is appropriate abstention or excessive brittleness.

Fresh end-stage research:
- Optimizing Decomposition: atomicity interacts with downstream verification;
- DnDScore / Decomposition Dilemmas: decomposition and decontextualization can introduce noise and change factuality outcomes;
- Claimify: ambiguity-aware claim extraction and coverage/decontextualization evaluation are essential;
- BEMEAE / REGen: exact span match alone is inadequate for semantic event arguments;
- Event Pattern-Instance Graph: inter-argument relations matter for role extraction.

Quality delta:
- end-to-end scientific-fidelity performance: UNCHANGED
- last measured verifier result remains 37.5% adversarial escape and 25% safe automatic acceptance, BOTH_FAIL
- A2 internal defect repair: five artificial decimal-fragment assertions removed, 5 observed decimal-boundary defects -> 0 under regression guard
- methodological status: IMPROVED

Completion:
- Gate A2: 100%
- Gate A overall: approximately 65%
- whole ACAD_PASS planning estimate: approximately 24% ±5%

Exact next authorized checkpoint:
`AT0-EN V2.4 GATE A3 — EXTRACTOR VALIDATION AGAINST FIXED DEVELOPMENT REFERENCE`

A3 scope:
- score source extractor against the existing six-case development reference without pre-score tuning;
- measure assertion coverage, false additions, atomicity, subject/predicate/object fidelity, context/decontextualization, represented role/ownership bindings, polarity/modality/causality, abstention quality, and critical silent errors;
- preserve all failures before any tuning decision.

Not authorized:
- candidate-text alignment;
- end-to-end verifier scoring;
- new live generation;
- HW1-EN;
- new untouched holdout.

Higher-model consultation is not required before A3 unless scoring exposes a new architecture/construct-validity problem.


## 2026-10-03 — AT0-EN V2.4 Gate A3 CLOSED

Checkpoint status:
**100% COMPLETE**

Canonical workflow:
`AT0-EN V2.4 Gate A3 Extractor Validation`

Canonical run:
`37143729167`

Trigger commit:
`8afeac02f465c462d015204aebe536366663bfdf`

Artifact:
- id: `11281706053`
- SHA-256: `d96fb79a65834f79b80c4b597a59092f73d6f795efbb5de12f0f418c8639671d`

Extractor remained frozen:
`32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`

Canonical A3 result:
`PASS_DEVELOPMENT`

Metrics:
- gold assertion coverage: 28/28 = 100%
- critical gold coverage: 27/27 = 100%
- false additions: 0/25 = 0%
- atomic one-to-one: 22/25 = 88%
- overmerged predictions: 3/25 = 12%
- certain precision: 13/14 = 92.86%
- error-abstention recall: 87.5%
- unnecessary abstention: 23.53%
- context-dependency detection recall: 100%
- context false-alarm rate: 6.25%
- critical silent semantic errors: 0

Field diagnostics:
- assertion type: 19/22 = 86.36%
- predicate: 21/22 = 95.45%
- subject concepts: 20/22 = 90.91%
- object concepts: 22/22 = 100%
- polarity: 22/22 = 100%
- modality: 22/22 = 100%
- causality: 22/22 = 100%
- measured population/baseline/scope checks: 100%

Pre-registered threshold margins:
- overall coverage: +10 pp above minimum
- critical coverage: +5 pp
- false additions: 10 pp better than maximum
- atomicity: +13 pp
- certain precision: +2.86 pp
- error-abstention recall: +7.5 pp
- critical silent errors: exactly meets hard gate at 0

Important evaluator negative evidence:
First A3 run `37143592151`, artifact `11281531213`, initially reported `FAIL_CRITICAL_SILENT_ERROR` because the V1 scorer treated assertion-type mismatch alone as a critical silent scientific error.

That classification exceeded the preregistered A3 construct. The first score was preserved. Extractor, gold, alignment logic, and thresholds were not changed.

Evaluator repair:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A3_EVALUATOR_REPAIR_ADDENDUM_V1.md`

The canonical rerun reports 0 critical silent semantic errors.
This change is an evaluator-contract correction, NOT extractor improvement.

Frozen first-score summary:
`phase2/academic_transform/at0_en/v2_4/gate_a/results/GATE_A3_FIRST_SCORE_V1_FROZEN.json`
commit:
`674aaf2131ecef25870e91fe249f7dffa7035db6`

Canonical frozen summary:
`phase2/academic_transform/at0_en/v2_4/gate_a/results/GATE_A3_EXTRACTOR_SUMMARY_FROZEN.json`
commit:
`8c18a94bc197be9c984e4a370038b3b93912b134`

A3 closure:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A3_CLOSURE.md`
commit:
`202395a973db9af6fc09f06017d5600df8e4e821`

Remaining A3 weaknesses:
- 12% overmerge
- 86.36% assertion-type accuracy
- 23.53% unnecessary abstention
- embedded-proposition wrapper errors
- unresolved source coreference in development examples

Interpretation:
The source extractor is development-viable under the current small synthetic reference, with high coverage and no observed critical silent semantic error, but atomicity, typing, and abstention efficiency remain imperfect.

A3 is DEVELOPMENT-ONLY and NOT blind:
A2 outputs were qualitatively inspected before the slot-reference supplement was frozen.

Fresh end-stage research reinforces separate evaluation of atomicity, faithfulness, decontextualization, coverage/focus, and claim-set alignment; benchmark/reference revisions should remain versioned and auditable.

Quality delta:
- end-to-end scientific-fidelity performance: UNCHANGED
- last full verifier evidence remains 37.5% adversarial escape and 25% safe acceptance, BOTH_FAIL
- no directly comparable prior A3 semantic baseline exists
- methodological status: IMPROVED

Completion:
- Gate A3: 100%
- Gate A overall: approximately 85%
- whole ACAD_PASS planning estimate: approximately 25% ±5%

Exact next authorized checkpoint:
`AT0-EN V2.4 GATE A4 — SOURCE-EXTRACTOR READINESS / REPAIR DECISION`

A4 must decide:
- ACCEPT current extractor for progression;
- REPAIR development weaknesses first;
- or REDESIGN source extraction.

No candidate alignment implementation starts before A4 closes.

Higher-model consultation is likely justified at A4 because it is a high-value go/no-go readiness decision. Consultation must remain review-only and budget-conscious; all implementation remains with the current agent.


## 2026-10-03 — AT0-EN V2.4 Gate A4 pre-consultation checkpoint

Stage status:
**PAUSED FOR HIGHER-MODEL READINESS CONSULTATION**

Progress:
- Gate A4: approximately 60%
- Gate A overall: approximately 92%
- whole ACAD_PASS planning estimate: approximately 25% ±5%

No extractor repair, candidate extraction, alignment implementation, live generation, HW1-EN, or new holdout has started.

### Evidence entering A4

A3 canonical result:
`PASS_DEVELOPMENT`

Metrics:
- gold coverage: 100%
- critical coverage: 100%
- false additions: 0%
- atomic one-to-one: 88%
- overmerge: 12%
- certain precision: 92.86%
- error-abstention recall: 87.5%
- unnecessary abstention: 23.53%
- context-dependency detection: 100%
- critical silent semantic errors: 0
- assertion type accuracy: 86.36%
- predicate accuracy: 95.45%
- subject-concept accuracy: 90.91%
- object/polarity/modality/causality: 100% on scored one-to-one alignments

Limitations:
- six synthetic development cases only;
- development-only, not blind;
- no authentic academic source texts;
- no candidate extraction;
- no alignment;
- no end-to-end V2.4 verifier result.

### Fresh A4 research synthesis

Current evidence reinforces:
- claim extraction should be evaluated separately for coverage, atomicity, faithfulness and decontextualization;
- decomposition and downstream verification interact;
- evidence/subclaim alignment is a bottleneck;
- decomposition can degrade verification under noisy or poorly aligned subclaims;
- conservative abstention can reduce error propagation but excessive abstention harms usability;
- scientific claim/evidence reasoning remains difficult and extraction failures should not be hidden in alignment.

### Internal red-team

Arguments for ACCEPT:
- all preregistered A3 thresholds passed;
- zero observed critical silent semantic errors;
- architecture already supports one-to-many/many-to-one alignment;
- repairing every development imperfection risks overfitting.

Arguments for REPAIR:
- 12% source overmerge can contaminate future alignment diagnostics;
- certain precision is only +2.86 pp above threshold;
- unnecessary abstention is 23.53%;
- source-side error propagation can obscure alignment failure attribution;
- current reference is too small/synthetic to rely on a narrow pass margin.

Argument for REDESIGN:
not supported; the representation/abstention architecture behaved directionally as intended.

Implementation-agent preliminary decision:
**REPAIR_TARGETED_FIRST**

No implementation is authorized before independent readiness review.

Pre-consult assessment:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A4_PRECONSULT_READINESS_ASSESSMENT.md`
commit:
`048bf59904ad93e7e531a4298ab27f4643eda280`

Higher-model consultation packet:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A4_HIGHER_MODEL_CONSULTATION_PACKET_V1.txt`
commit:
`88755b956cf60723f69641c0a4902589cf693d10`

Files to send to higher model:
1. `phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A4_PRECONSULT_READINESS_ASSESSMENT.md`
2. `phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A3_CLOSURE.md`

Budget agreement applies:
- consultant/reviewer only;
- no coding;
- no repo edits;
- no workflows;
- no reruns;
- no routine implementation;
- current agent executes all resulting work.

Exact next action:
WAIT for the user's returned higher-model consultation response.
Then evaluate recommendations, freeze A4 readiness decision, and stop before any next implementation checkpoint.

Quality delta:
- end-to-end performance: UNCHANGED
- readiness status: UNDER REVIEW
- methodological status: IMPROVED


## 2026-10-03 — AT0-EN V2.4 Gate A4 CLOSED / Gate A COMPLETE

Checkpoint status:
**Gate A4 = 100% COMPLETE**
**Gate A overall = 100% COMPLETE**

Higher-model verdict:
`ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Final project disposition:
`GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY`

The source extractor is accepted only for limited development alignment research.
It is NOT production-approved and is NOT evidence of end-to-end V2.4 safety.

Evidence entering A4:
- A1 deterministic anchor precision/recall: 100% / 100%
- A1 exact provenance: 35/35
- A3 gold coverage: 100%
- A3 critical coverage: 100%
- A3 false additions: 0%
- A3 atomic one-to-one: 88%
- A3 overmerge: 12%
- A3 certain precision: 92.86%
- A3 error-abstention recall: 87.5%
- A3 unnecessary abstention: 23.53%
- A3 context-dependency detection: 100%
- A3 critical silent semantic errors: 0
- A3 assertion-type accuracy: 86.36%

Decision change:
- pre-consultation: `REPAIR_TARGETED_FIRST`
- final: `ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Reason:
Overmerge is not itself a blocking safety failure under the frozen 1:N / N:1 architecture.
It becomes blocking only if a merge loses/rebinds material ownership, scope, negation, relation identity, or other scientific semantics and is then treated as valid/certain.
No such CERTAIN critical silent failure was observed in A3.

Higher-model response:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A4_HIGHER_MODEL_RESPONSE_V1.md`
commit:
`2d26ba0ea4330d58790ae0757e2ae488b7ed417b`

Final decision matrix:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A4_DECISION_MATRIX_V1.md`
commit:
`77af2cb93f28fcf2e4b4a80f3bbe53d1dd6c7136`

A4 closure:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A4_CLOSURE.md`
commit:
`72fd47a4062734f567f362f9da930ef1eda07a25`

Accepted conditions for next stage:
1. alignment begins on development data only;
2. use correct/human-reviewed source and candidate graphs first;
3. report gold-graph alignment separately from extracted-graph alignment;
4. uncertainty stays explicit;
5. uncertain+uncertain agreement cannot become CERTAIN automatically;
6. keep overmerged and abstained cases in denominators;
7. do not force zero overmerge;
8. defer assertion-type optimization unless it affects semantic routing;
9. defer unnecessary-abstention optimization;
10. authentic academic source text enters AFTER a diagnosable alignment prototype but BEFORE integrated system freeze/validity claims.

Fresh research conclusion:
- decomposition atomicity must be considered together with downstream verification;
- decomposition/verifier alignment is a distinct research bottleneck;
- coverage, ambiguity and decontextualization remain separate source-extraction safety properties.

Quality delta:
- end-to-end performance: UNCHANGED
- last full verifier evidence remains 37.5% adversarial escape, 25% safe automatic acceptance, BOTH_FAIL
- readiness changed from repair-first to alignment-authorized development research
- this is a decision/readiness change, not a measured scientific-fidelity improvement

Completion:
- Gate A4: 100%
- Gate A: 100%
- whole ACAD_PASS planning estimate: approximately 26% ±5%

Exact next authorized stage:
`AT0-EN V2.4 GATE B1 — ALIGNMENT PROTOTYPE WITH HUMAN-CORRECT GRAPHS`

B1 initial scope:
- development-only;
- no model inference initially required;
- build a small fixed human-correct source/candidate graph set;
- implement alignment mechanics only;
- support 1:1 / 1:N / N:1;
- score alignment independent of extractor quality;
- preserve uncertainty and minimal evidence traces;
- include faithful paraphrase, split/merge, relation rebinding, scope/negation change and ambiguity;
- do not use extracted graphs until human-correct graph alignment behavior is understood.

Not authorized:
- live generation
- HW1-EN
- new untouched holdout
- production claims
- authentic-document integrated validation before a diagnosable alignment prototype

Higher-model consultation is not required at B1 start unless a new construct-validity or architecture issue appears.


## 2026-10-03 — AT0-EN V2.4 Gate B1 human-correct reference freeze CLOSED

Checkpoint status:
**100% COMPLETE**

Purpose:
freeze the human-correct graph reference and B1 scoring contract before any aligner implementation.

No model inference occurred.
No extractor output was used.
No aligner has been implemented or scored yet.

Workflow:
`AT0-EN V2.4 B1 Reference Integrity`

Run:
`37145151369`

Trigger commit:
`ff4173729d94bf90217ac05d986846cd58eeaacd`

Artifact:
- id: `11281568714`
- SHA-256: `ba404b99186582a259f683736f0018832bf09f34a71f6dc247cd8ef2a4bfcaaf`

Integrity:
- 363 checks PASS
- 12 graph pairs
- outcomes: 5 PASS_CANDIDATE / 6 REJECT / 1 REVIEW
- mapping shapes: 7 ONE_TO_ONE / 2 ONE_TO_MANY / 2 MANY_TO_ONE / 1 MIXED
- source assertions: 19
- candidate assertions: 19
- source relations: 6
- candidate relations: 6

Gold assertion-alignment statuses:
- PRESERVED: 7
- ALTERED: 8
- CONTRADICTORY: 1
- UNCERTAIN: 1

Gold relation-alignment statuses:
- PRESERVED: 3
- ALTERED: 2
- CONTRADICTORY: 1

Uncertain review pair:
`B1-P10`

Frozen hashes:
- alignment schema: `49935f5ea0de2e972c7bb7b557f4b477dbd72caed6cd7dd066117da6761f5a3a`
- scoring contract: `385581867da42c6e0a13f1031ccf96787740bc2233cd25ec7b98c484fcbc42e1`
- human-correct pair set: `29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca`
- integrity checker: `1d4b9e68760cc07790283ae7dcf148c424baa5438d58f63e79e1a55acee0e539`
- integrity summary: `6e91b9f98ea549994929e6988d1b3f2bc75daa3fcdc3987c784f702eccb9568d`

Important repair before freeze:
the initial B1 schema represented only assertion-level gold alignment.
This was insufficient for citation/procedure/relation failures.
`gold_relation_alignment` was added before the pair set was frozen.

Scenario coverage:
- faithful paraphrase
- faithful split
- faithful merge
- relation/value rebinding
- scope/negation reversal
- citation-binding change
- equation/symbol binding change
- procedural-order reversal
- metric-definition change
- ambiguity/uncertainty propagation

Pre-registered future aligner hard gates:
- critical dangerous false-preserve: 0
- pair-level expected outcome: 100%
- critical gold alignment coverage: 100%
- critical alignment-status accuracy: 100%
- faithful safe-pair rejection: 0
- material adversarial pair acceptance: 0
- critical uncertainty preservation: 100%

Fresh end-stage research:
- decomposition/verifier quality can be misaligned, so alignment must be tested directly;
- event relations such as coreference, temporal, causal, and hierarchy/subsumption remain difficult;
- uncertainty must remain tied to evidence rather than being silently erased;
- graph structure alone does not guarantee correct semantic alignment.

Quality delta:
- end-to-end scientific-fidelity performance: UNCHANGED
- last full verifier evidence remains 37.5% adversarial escape and 25% safe automatic acceptance, BOTH_FAIL
- B1 aligner performance: NOT YET MEASURED
- methodological status: IMPROVED

Completion:
- B1 reference-freeze checkpoint: 100%
- Gate B1 overall: approximately 45%
- whole ACAD_PASS planning estimate: approximately 27% ±5%

Reference-freeze closure:
`phase2/academic_transform/at0_en/v2_4/gate_b1/B1_REFERENCE_FREEZE_CLOSURE.md`
commit:
`796aba0418702d5c8113ff62ed21bc6ca61d1c8e`

Exact next authorized checkpoint:
`AT0-EN V2.4 GATE B1 — ALIGNER IMPLEMENTATION + FIRST HUMAN-CORRECT GRAPH SCORE`

Next checkpoint scope:
- implement alignment mechanics only;
- use frozen human-correct graphs;
- no model inference initially;
- support 1:1 / 1:N / N:1 / mixed;
- score assertion and relation alignment separately;
- preserve uncertainty;
- produce traceable evidence for every critical alignment;
- run one first score against the frozen B1 contract;
- freeze all failures before any repair.

Not authorized:
- extracted-graph alignment
- candidate extraction
- live generation
- HW1-EN
- untouched holdout
- production claims

Higher-model consultation is not required at aligner implementation start unless a new construct-validity issue appears.


## 2026-10-03 — Permanent cumulative success-ledger reporting rule

User requires every substantive progress update and checkpoint report to include a cumulative success ledger from the beginning of the current V2.4 research track through the present checkpoint.

The ledger must always distinguish:
1. component/gate metrics;
2. current checkpoint completion percentage;
3. whole-ACAD_PASS planning completion estimate;
4. latest true end-to-end verifier result.

Never present a component-level 100% result as system-level success.

Default cumulative ledger baseline/history to carry forward:
- historical pre-V2.4 end-to-end baseline from V2.3 unseen holdout:
  - adversarial escape: 37.5%
  - safe automatic acceptance: 25%
  - BOTH_FAIL
- V2.4 Gate 0 contract integrity:
  - 326/326 PASS after A1 contract repairs
  - contract integrity only, not verifier accuracy
- Gate A1 deterministic anchors:
  - precision 100%
  - recall 100%
  - exact provenance 35/35
  - narrow development scope
- Gate A2 source structural prototype:
  - structural sentence representation 100%
  - 5 observed decimal-boundary defects repaired to 0 under regression guard
  - semantic accuracy not established in A2
- Gate A3 source extractor development validation:
  - gold coverage 100%
  - critical coverage 100%
  - false additions 0%
  - atomic one-to-one 88%
  - certain precision 92.86%
  - error-abstention recall 87.5%
  - unnecessary abstention 23.53%
  - critical silent semantic errors 0
  - PASS_DEVELOPMENT
- Gate A4:
  - GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY
  - readiness decision, not performance gain
- Gate B1 human-correct reference integrity:
  - 363/363 integrity checks PASS
  - 12 graph pairs
  - aligner performance NOT YET MEASURED at time of this rule

When a later stage produces new comparable metrics:
- add them to the cumulative ledger;
- report improvement/worsening in percentage points or counts where valid;
- explicitly state when no directly comparable baseline exists;
- preserve negative evidence and historical failures.

Time estimates:
- do not provide unreliable wall-clock promises;
- report remaining checkpoints/units and observed runtime/throughput when available.

This reporting rule is permanent unless the user explicitly changes it.


## 2026-10-03 — AT0-EN V2.4 B1 first aligner score CLOSED

Checkpoint status:
**100% COMPLETE / FIRST SCORE FROZEN / REPAIR NOT STARTED**

Run:
`37145678669`

Trigger commit:
`3c3ccde1637cb819cd20987a224bbcfe2354dea1`

Artifact:
- id: `11281074678`
- SHA-256: `245593d8e6af433713553e2cd6489f3b68e92015239ad1e7edafa4323b169647`

Frozen first-score summary:
`phase2/academic_transform/at0_en/v2_4/gate_b1/results/B1_FIRST_SCORE_FROZEN.json`
commit:
`1c6860406c7ae3c6565f4dd85369d85681af8056`

Closure:
`phase2/academic_transform/at0_en/v2_4/gate_b1/B1_FIRST_SCORE_CLOSURE.md`
commit:
`6c48404aa98757cc957cc5fcc9a2f27f42eae1b5`

Result:
`FAIL_B1_HUMAN_CORRECT`

Metrics:
- pair outcome: 10/12 = 83.33%
- critical gold alignment coverage: 20/22 = 90.91%
- critical alignment-status accuracy: 95%
- dangerous false-preserve: 0
- faithful safe-pair rejection: 1
- material adversarial acceptance: 1
- critical uncertainty preservation: 100%
- critical evidence-trace completeness: 100%

Mapping-shape performance:
- ONE_TO_ONE: 6/7 = 85.71%
- ONE_TO_MANY: 2/2 = 100%
- MANY_TO_ONE: 1/2 = 50%
- MIXED: 1/1 = 100%

Frozen failures:
1. B1-P03 faithful merge falsely rejected:
   split/merge binding equivalence under-modeled.
2. B1-P04 relation/value rebinding falsely accepted:
   assignment matched by value strongly enough to hide swapped Group A/B ownership.

Interpretation:
- B1 hard gate FAILS.
- progression to extracted-graph alignment is BLOCKED.
- failure is localized to aligner mechanics, not a demonstrated architecture collapse.

Principle-based next repair:
- owner/entity-first assignment;
- relation-aware assignment;
- canonical binding facts across split/merge;
- identical values must never compensate for wrong owners;
- no ID-specific branches;
- thresholds unchanged.

### Permanent cumulative success ledger at this checkpoint

Historical V2.3 end-to-end baseline:
- adversarial escape: 37.5%
- safe automatic acceptance: 25%
- BOTH_FAIL

V2.4 Gate 0:
- 326/326 contract checks PASS

A1:
- deterministic-anchor precision: 100%
- recall: 100%
- provenance: 35/35

A2:
- structural sentence representation: 100%
- decimal defects: 5 -> 0 after repair

A3:
- gold coverage: 100%
- critical coverage: 100%
- false additions: 0%
- atomicity: 88%
- certain precision: 92.86%
- error-abstention recall: 87.5%
- unnecessary abstention: 23.53%
- critical silent semantic errors: 0
- PASS_DEVELOPMENT

A4:
- GO_ALIGNMENT_RESEARCH_DEVELOPMENT_ONLY

B1 reference:
- 363/363 PASS

B1 first aligner:
- pair outcome: 83.33%
- critical coverage: 90.91%
- critical status accuracy: 95%
- uncertainty preservation: 100%
- evidence traces: 100%
- one material adversarial acceptance
- one faithful false rejection
- FAIL_B1_HUMAN_CORRECT

Quality delta:
- no directly valid system-level improvement percentage versus V2.3 yet because B1 is component-isolated;
- B1 improves diagnostic isolation but currently FAILS its hard safety gate.

Completion:
- current checkpoint: 100%
- Gate B1 overall: approximately 70%
- whole ACAD_PASS planning estimate: approximately 27% ±5%

Exact next authorized checkpoint:
`AT0-EN V2.4 GATE B1.1 — PRINCIPLE-BASED ALIGNER REPAIR + REVALIDATION`

Not authorized:
- extracted-graph alignment
- candidate extraction
- live generation
- HW1-EN
- untouched holdout
- production claims

Higher-model consultation is not required at B1.1 start unless repair exposes a new construct-validity issue.


## 2026-10-03 — AT0-EN V2.4 B1.1 CLOSED / Gate B1 COMPLETE

Status:
- B1.1: 100% COMPLETE
- Gate B1: 100% COMPLETE
- whole ACAD_PASS planning estimate: approximately 28% ±5%

Final B1.1 run:
`37146333162`

Artifact:
- id: `11282215627`
- SHA-256: `cae7f304bf6ff6ac78b6dacd6c624be1a14fc74221032e2d59ee217b768c73ea`

Result:
`PASS_B1_HUMAN_CORRECT`

Final hard-gate metrics:
- pair outcomes: 12/12 = 100%
- critical alignment coverage: 22/22 = 100%
- critical alignment-status accuracy: 100%
- dangerous false-preserve: 0
- faithful false rejection: 0
- material adversarial acceptance: 0
- critical uncertainty preservation: 100%
- critical evidence-trace completeness: 100%
- repair regressions: 3/3 PASS

Improvement vs first B1 score:
- pair outcome accuracy: 83.33% -> 100% = +16.67 pp
- critical coverage: 90.91% -> 100% = +9.09 pp
- critical status accuracy: 95% -> 100% = +5 pp
- adversarial acceptance: 1 -> 0
- faithful false rejection: 1 -> 0

Repair principles:
- owner/entity-first matching
- canonical owner-to-value/meaning binding facts
- symbolic-key normalization
- scalar+unit canonicalization
- coordinated-owner normalization

Preserved negative evidence:
- first B1 run `37145678669`: FAIL at 83.33%
- first B1.1 regression run `37146262703`: regression failure before score due coordinated-group normalization defect

Frozen B1.1 result:
`phase2/academic_transform/at0_en/v2_4/gate_b1/results/B1_1_REVALIDATION_FROZEN.json`
commit:
`6bc34bb1591804c8b497f46f29c85dd9f954be57`

Closure:
`phase2/academic_transform/at0_en/v2_4/gate_b1/B1_1_REVALIDATION_CLOSURE.md`
commit:
`c170e2053158d7cdb3032be1ab7f4faff1102ed8`

Cumulative success ledger:
- V2.3 baseline: 37.5% escape / 25% safe acceptance / BOTH_FAIL
- Gate 0: 326/326 PASS
- A1: 100% precision / 100% recall / 35/35 provenance
- A2: 100% structural representation; known decimal defects 5 -> 0
- A3: 100% coverage / 100% critical coverage / 0% false additions / 88% atomicity / 92.86% certain precision / 87.5% error-abstention / 0 critical silent errors
- A4: GO alignment research
- B1 reference: 363/363 PASS
- B1 first aligner: 83.33% FAIL
- B1.1 repaired aligner: 100% on all frozen B1 hard gates

Important interpretation:
B1 is now mechanically successful only on 12 human-correct development graph pairs.
This is NOT an end-to-end V2.4 success claim.

Exact next authorized stage:
`AT0-EN V2.4 GATE B2 — EXTRACTED-GRAPH ALIGNMENT DEGRADATION TEST`

B2 must keep human-correct B1 metrics separate from extracted-graph metrics and measure the degradation introduced by extraction.

Permanent reporting remains concise and cumulative.


## 2026-10-03 — AT0-EN V2.4 B2 protocol/input freeze CLOSED

Checkpoint:
100% COMPLETE

Gate B2 overall:
approximately 35%

Whole ACAD_PASS planning estimate:
approximately 29% ±5%

No B2 extracted-graph performance has been scored yet.

Integrity run:
`37146751607`

Artifact:
- id: `11282226161`
- SHA-256: `035673f9fd02fc28cd516ba23f7594cbbac48c4ed23a276bd6abf99e67370a77`

Integrity result:
- PASS
- 144 checks
- 12 pairs
- no model inference

Frozen B2 four-arm design:
- GG = gold source -> gold candidate; historical B1.1 baseline 100%
- GE = gold source -> extracted candidate
- EG = extracted source -> gold candidate
- EE = extracted source -> extracted candidate; primary arm

Purpose:
attribute degradation to candidate extraction, source extraction, or their interaction instead of reporting one opaque score.

Frozen raw-text policy:
- concatenate assertion evidence then relation evidence;
- exact duplicate evidence may be removed;
- no semantic rewriting.

Frozen bridge policy:
- mechanical field mapping only;
- no semantic repair;
- no inferred missing relations;
- no hidden coreference resolution;
- no gold/expected-outcome leakage.

Because frozen A2 emits no semantic relations, absent relations remain absent and count as extraction degradation.

Pre-registered EE gates:
Safety:
- adversarial acceptance 0/6
- dangerous critical false preserve 0
- ambiguous pair remains REVIEW
- critical uncertainty promotion 0

Usability:
- faithful safe acceptance >= 4/5 = 80%
- pair outcome >= 11/12 = 91.67%
- faithful false rejection <= 1/5

Frozen identities:
- aligner: `289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42`
- extractor: `32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`
- B1 pairs: `29f3790859c8da6baf65db8b0fb372bc881e25d8e3d1e76b9c67b74d49944dca`
- B2 raw pairs: `afa733aa5e0498706df66acb7005fa7fff891ef39afe9e8b086a463fdf107395`
- B2 protocol: `a70d70edb4dcf4138c63d5ac46a200ec20d7781c0ac7bc3648232f254bda571d`
- B2 bridge contract: `51330f76f2ebca0625e2bb4cb040844dceab59355a13ecde5cd29f24f3ae4a7f`

Closure:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_PROTOCOL_FREEZE_CLOSURE.md`
commit:
`6b9a26845bed3477a0185d07457166b1b92863c9`

Fresh research conclusion:
- granular evidence alignment is a major claim-verification bottleneck;
- extraction/subclaim errors can determine downstream robustness;
- conservative abstention reduces propagation of incorrect claims;
- source-level accountability and evidence traceability should remain explicit;
- final labels without faithful rationale/alignment are insufficient.

Cumulative success ledger:
- V2.3 baseline: 37.5% escape / 25% safe acceptance / BOTH_FAIL
- Gate 0: 326/326 PASS
- A1: 100% precision / 100% recall / 35/35 provenance
- A2: 100% structural representation; decimal defects 5 -> 0
- A3: 100% coverage / 100% critical coverage / 0% false additions / 88% atomicity / 92.86% certain precision / 87.5% error-abstention / 0 critical silent errors
- A4: GO alignment development
- B1 reference: 363/363 PASS
- B1 first aligner: 83.33% FAIL
- B1.1: 100% on all frozen hard gates
- B2: performance NOT YET MEASURED; protocol/input integrity PASS

Quality delta:
- end-to-end performance: UNCHANGED
- B2 performance: NOT YET MEASURED
- methodological status: IMPROVED

Exact next authorized checkpoint:
`AT0-EN V2.4 GATE B2 — BRIDGE IMPLEMENTATION + FIRST FOUR-ARM SCORE`

Do not tune extractor or aligner before first B2 score.
Higher-model consultation is not currently required.


## 2026-10-03 — AT0-EN V2.4 B2 first four-arm score CLOSED

Checkpoint:
**100% COMPLETE**

Gate B2 overall:
**approximately 70%**

Whole ACAD_PASS planning estimate:
**approximately 29% ±5%**

Run:
`37147162271`

Artifact:
- id: `11282800994`
- SHA-256: `a65a76ccd0fa819e819ff9bf6c94529b0e893ad94261d64e3c14bdb301c43a96`

Result:
`MIXED_B2_REPAIR_REQUIRED`

Four-arm metrics:
- GG: 12/12 = 100% pair accuracy; safe acceptance 100%; adversarial acceptance 0%
- GE: 5/12 = 41.67%; safe acceptance 0%; adversarial acceptance 0%
- EG: 6/12 = 50%; safe acceptance 20%; adversarial acceptance 0%
- EE: 4/12 = 33.33%; safe acceptance 0%; adversarial acceptance 0%; REVIEW preservation 100%

EE degradation vs GG:
- pair accuracy: -66.67 pp
- safe acceptance: -100 pp
- adversarial acceptance: unchanged at 0%
- REVIEW preservation: unchanged at 100%

EE gate result:
Safety PASS:
- adversarial acceptance 0/6
- dangerous critical false preserve 0
- ambiguous pair remains REVIEW
- critical uncertainty promotion 0

Usability FAIL:
- safe acceptance required >=80%; observed 0%
- pair accuracy required >=91.67%; observed 33.33%
- faithful false rejection required <=1; observed 2

Primary diagnosis:
- aligner remains strong on human-correct graphs;
- extraction representation is the bottleneck;
- predicate/paraphrase coverage gaps cause conservative uncertainty;
- semantic relations are absent from A2 extraction, weakening citation/procedure/equation decisions;
- anchor ownership across split/merge quantitative structures is insufficient;
- candidate extraction is descriptively weaker than source extraction on the fixed set;
- joint extraction adds interaction degradation.

Important interpretation:
`SAFETY-CONSERVATIVE / USABILITY-NOT-READY`

No adversarial pair was automatically accepted.
The main failure is excessive REVIEW/REJECT on safe content and inability to decisively reject some adversarial relation changes.

Frozen first score:
`phase2/academic_transform/at0_en/v2_4/gate_b2/results/B2_FIRST_SCORE_FROZEN.json`
commit:
`cf15e9bec0d0b45856e1e4172a7bddde1cc48814`

Closure:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_FIRST_SCORE_CLOSURE.md`
commit:
`1fa98c09becfafde94fae0bc676d226b605d9d14`

Cumulative success ledger:
- V2.3 baseline: 37.5% escape / 25% safe acceptance / BOTH_FAIL
- Gate 0: 326/326 PASS
- A1: 100% precision / 100% recall / 35/35 provenance
- A2: 100% structural representation; decimal defects 5 -> 0
- A3: 100% coverage / 100% critical coverage / 0% false additions / 88% atomicity / 92.86% certain precision / 87.5% error-abstention / 0 critical silent errors
- A4: GO alignment development
- B1 reference: 363/363 PASS
- B1 first aligner: 83.33% FAIL
- B1.1 repaired aligner: 100% all hard gates
- B2 EE first score: 33.33% pair accuracy / 0% safe acceptance / 0% adversarial acceptance / MIXED_B2_REPAIR_REQUIRED

Quality delta:
- extracted-graph usability WORSENED sharply vs B1.1 human-correct baseline
- safety remained conservative
- no end-to-end product success claim authorized

Exact next authorized checkpoint:
`AT0-EN V2.4 B2.1 — EXTRACTION/RELATION REPRESENTATION REPAIR DECISION`

Higher-model consultation is justified at B2.1 because the repair boundary is architectural:
predicate normalization vs explicit relation extraction vs ownership representation vs split/merge binding vs candidate symmetry vs authentic-text timing.

Do NOT modify extractor, bridge, or aligner before the B2.1 decision is frozen.


### B2 duplicate verification note after UI stream-recovery interruption

A later duplicate verification run occurred after the ChatGPT UI displayed the recurring long-thinking/stream-recovery behavior:

- duplicate run: `37147337174`
- trigger commit: `b7de15338f347077659835f49e3d02c7ce6b4479`
- artifact id: `11283300924`
- artifact SHA-256: `c49af9203c60497944f48a1398045bdc4a3799a98b6872571e5dd1ed9de8557d`

It reproduced the same four-arm scientific result:
- GG 100%
- GE 41.67%
- EG 50%
- EE 33.33%
- EE safe acceptance 0%
- adversarial acceptance 0%
- result `MIXED_B2_REPAIR_REQUIRED`

This duplicate run is NOT a new scientific experiment, does NOT replace the canonical first B2 run `37147162271`, and does NOT change any metric, readiness decision, or project completion estimate.

Canonical B2 first-score provenance remains the earlier frozen result and closure.

This note exists only to preserve operational continuity and prevent accidental double-counting after UI interruption.


## 2026-10-03 — Permanent adoption-target reporting format

User requires all substantive progress reports to present metrics in this fixed form:

`Metric name | Current measured result | Strong-system adoption target | Gap`

The report must distinguish development-component metrics from final end-to-end adoption metrics.

Project-defined strong-adoption targets (not claimed as universal external standards):

### Safety-critical targets
- end-to-end adversarial automatic acceptance / escape: **0%**
- critical silent scientific errors: **0**
- critical uncertainty promotion to automatic PASS: **0**
- ambiguity preservation when evidence is insufficient: **100%**

### Accepted-decision quality targets
- selective precision / correctness among automatic PASS decisions: **>=99%**
- critical relation/ownership correctness on controlled validation: **100%**

### Usability / coverage targets
- safe automatic acceptance / selective coverage on authentic in-domain validation: **>=90%**
- extracted-graph pair decision accuracy before advanced system adoption: **>=95%**

### Structural component targets
- deterministic anchor precision: **100%**
- deterministic anchor recall: **100%**
- evidence/provenance completeness for critical decisions: **100%**
- human-correct graph alignment hard gates: **100%**

These targets are project acceptance criteria chosen to make ACAD_PASS strongly conservative and useful.
They are not universal scientific standards and must not be represented as such.

Safety targets are non-compensatory:
high coverage or accuracy can never compensate for a critical silent error or adversarial automatic acceptance.

When a metric has not yet been measured end-to-end, report `NOT YET MEASURED`, never substitute a component metric.

Permanent concise reporting style:
- keep updates short;
- show only the most decision-relevant rows unless a full audit table is requested;
- always include current stage completion and whole-project planning estimate.


## 2026-10-03 — AT0-EN V2.4 B2.1 pre-consultation checkpoint

Status:
**PAUSED FOR HIGHER-MODEL ARCHITECTURE REVIEW**

Progress:
- B2.1: approximately 60%
- Gate B2 overall: approximately 80%
- whole ACAD_PASS planning estimate: approximately 29% ±5%

No extractor, bridge, or aligner repair has started.

Frozen diagnosis:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_1_DIAGNOSIS_V1.md`
commit:
`8558b7c4bb9793a024a5c383a3d0e39589466175`

Focused higher-model consultation packet:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_1_HIGHER_MODEL_CONSULTATION_PACKET_V1.txt`
commit:
`32e5c79feae9cd570bbcf5f6965fc9020b13fda0`

Canonical B2 evidence:
- GG 100%
- GE 41.67%
- EG 50%
- EE 33.33%
- EE safe acceptance 0%
- EE adversarial acceptance 0%
- REVIEW preservation 100%
- result MIXED_B2_REPAIR_REQUIRED

Primary exclusive diagnosis of 8 wrong EE pairs:
- predicate/paraphrase/scope/decomposition: 4/8 = 50%
- split/merge owner/value or owner/meaning binding: 2/8 = 25%
- missing explicit relation extraction: 1/8 = 12.5%
- equation/symbol structured ownership missing: 1/8 = 12.5%

Bridge diagnosis:
- invalid bridge records: 0
- bridge mechanics are not the primary repair target

Aligner diagnosis:
- GG remains 100%
- aligner mechanics are not the primary repair target

Pre-consultation architecture recommendation:
`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Do not patch consumed pair IDs.
Do not weaken B2 gates.
Do not tune the aligner to compensate for missing extraction semantics.

Permanent reporting format now required:
`Metric | Current result | Strong-adoption target | Gap`

Current key adoption-target ledger:
- adversarial automatic acceptance: 0% | target 0% | gap 0
- critical silent scientific errors: 0 observed in A3 | target 0 | gap 0 on measured development evidence
- human-correct graph alignment: 100% | target 100% | gap 0
- extracted-graph pair accuracy: 33.33% | target >=95% | gap 61.67 pp
- extracted safe automatic acceptance: 0% | target >=90% | gap 90 pp
- ambiguity/REVIEW preservation: 100% | target 100% | gap 0
- selective precision among automatic PASS decisions: NOT YET MEASURED end-to-end | target >=99%

These targets are ACAD_PASS project-defined strong-adoption criteria, not universal standards.

Fresh research:
- abstention-aware scientific reasoning supports preserving uncertainty instead of forcing answers;
- SciEvent supports structured scientific events, triggers and arguments beyond narrow entity extraction;
- EventRelBench shows event relation understanding remains difficult;
- claim-verification research continues to identify decomposition/relation/evidence alignment as major error sources.

Exact next action:
WAIT for user-returned higher-model consultation response.

Then:
- evaluate recommendations;
- freeze B2.1 repair boundary;
- only then implement a versioned repair.

No routine higher-model implementation is requested.


## 2026-10-03 — AT0-EN V2.4 B2.1 CLOSED

Status:
- B2.1: 100% COMPLETE
- Gate B2 overall: approximately 85%
- whole ACAD_PASS planning estimate: approximately 30% ±5%

Final verdict:
`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Higher-model response:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_1_HIGHER_MODEL_RESPONSE_V1.md`
commit:
`1633f704a60e79d46a2e095242f55cc8972b70b1`

Final repair boundary:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_1_FINAL_REPAIR_BOUNDARY_V1.md`
commit:
`21fbdc8cf40b934a89cfdfc10b43924d1564d882`

Closure:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_1_CLOSURE.md`
commit:
`d52e1b53c377277c1d710747a54488e4711740d2`

Canonical B2 baseline entering repair:
- GG pair accuracy: 100%
- GE: 41.67%
- EG: 50%
- EE: 33.33%
- EE safe acceptance: 0%
- EE adversarial acceptance: 0%
- REVIEW preservation: 100%
- result: MIXED_B2_REPAIR_REQUIRED

Mandatory B2.2 repair capabilities:
1. predicate/paraphrase normalization
2. negation/scope ownership
3. owner/value and owner/meaning split-merge binding
4. citation-to-claim binding
5. equation/symbol/coefficient binding

Deferred unless new evidence makes them blocking:
- generic procedural-order parser
- generic local-coreference resolver
- broad semantic-parser replacement
- general mathematical equivalence

Architecture:
- keep frozen A2 anchors/provenance/assertion proposals
- add relation-aware structured layer with access to original text, allowed local context, evidence and anchors
- keep B1.1 aligner frozen
- no pair-ID-specific repair
- no threshold weakening

Frozen B2.2 progression gates:
- adversarial acceptance 0/6
- dangerous critical false preserve 0
- critical uncertainty promotion 0
- ambiguous pair remains REVIEW
- safe acceptance >=4/5 = 80%
- pair accuracy >=11/12 = 91.67%
- faithful false rejection <=1/5
- GG remains 100%
- deterministic anchor/provenance behavior does not regress
- critical relation representation auditable independently per side

Strong-adoption targets:
- adversarial automatic acceptance: 0%
- critical silent scientific errors: 0
- automatic-PASS selective precision: >=99%
- authentic in-domain safe automatic acceptance: >=90%
- extracted-graph pair accuracy: >=95%
- controlled critical relation/ownership correctness: 100%
- deterministic anchor precision/recall: 100% / 100%
- critical evidence/provenance completeness: 100%

Current key gap ledger:
- extracted-graph pair accuracy: 33.33% | target >=95% | gap 61.67 pp
- safe automatic acceptance: 0% | target >=90% | gap 90 pp
- adversarial automatic acceptance: 0% | target 0% | gap 0
- REVIEW preservation: 100% | target 100% | gap 0
- selective precision end-to-end: NOT YET MEASURED | target >=99%

Authentic academic text:
- introduce immediately after first B2.2 repair prototype
- before synthetic B2 revalidation
- qualitative development-only check
- not a benchmark and not a numeric gate

Exact next authorized stage:
`AT0-EN V2.4 B2.2 — HYBRID RELATION-AWARE EXTRACTION REPAIR PROTOTYPE`

Do not start live generation, HW1-EN, untouched holdout, or production claims.


## 2026-10-03 — AT0-EN V2.4 B2.2 prototype freeze CLOSED

Status:
- B2.2 prototype checkpoint: 100% COMPLETE
- Gate B2 overall: approximately 90%
- whole ACAD_PASS planning estimate: approximately 31% ±5%

Architecture:
`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Frozen components retained:
- A2 anchor/provenance/assertion extractor unchanged
- B1.1 aligner unchanged
- B2 four-arm protocol and gates unchanged

Versioned B2.2 layer adds:
- predicate/paraphrase normalization
- negation/scope ownership
- owner/value and owner/meaning split-merge binding
- citation-to-claim binding
- equation/symbol/coefficient binding
- explicit-only PRECEDES support
- deterministic-first behavior with abstention

Final prototype regression run:
`37149645971`
Result:
**17/17 PASS**

Final authentic academic qualitative run:
`37149698525`

Artifact:
- id: `11283396807`
- SHA-256: `63a4bfdfd62ca794a81323b45e295e75355dbbc3b04b57e10d32737ed2eebfb5`

Authentic qualitative check:
Before explicit scientific predicate repair:
- CERTAIN 0
- AMBIGUOUS 5
- unsupported relations 0

After repair:
- CERTAIN 5
- AMBIGUOUS 0
- UNCERTAIN 0
- unsupported relations 0

Important:
This authentic check is qualitative development evidence only.
It is not a benchmark and is not an adoption metric.

Final red-team:
- detected incorrect positive parsing of `does not treat`
- repaired explicit negative DEFINE/TREAT/USE_FOR handling
- modal AIM_TO now preserves MAY/CAN/COULD
- final 17/17 regressions ran after this repair

Prototype implementation commits include:
- initial relation-aware layer: `2ad4934869e9a3dd3a8dfca1d4a111a2b7d34e5c`
- explicit scientific predicate normalization: `feab5c505c245c6cdd90a628694a5692d7ed3696`
- modality preservation: `8f2887975542f7c371123463212305cffd2691bb`
- explicit negation repair: `f3ea3d5d572fea1622418ab8808f8086d7b1119f`
- prototype closure: `8c7c8d213cd3f5d1fb846a23c4d420f6ee447687`

Canonical B2 performance remains UNCHANGED until repaired four-arm revalidation:
- GG 100%
- GE 41.67%
- EG 50%
- EE 33.33%
- EE safe acceptance 0%
- EE adversarial acceptance 0%
- REVIEW preservation 100%
- MIXED_B2_REPAIR_REQUIRED

Permanent metric reporting:
`Metric | Current measured result | Strong-adoption target | Gap`

Current strong-adoption ledger:
- adversarial automatic acceptance: 0% | target 0% | gap 0
- critical silent scientific errors: 0 observed on measured development evidence | target 0 | gap 0 on measured evidence
- human-correct alignment: 100% | target 100% | gap 0
- extracted-graph pair accuracy: 33.33% canonical B2 | target >=95% | gap 61.67 pp
- authentic in-domain safe automatic acceptance: NOT YET MEASURED | target >=90%
- automatic-PASS selective precision end-to-end: NOT YET MEASURED | target >=99%
- ambiguity preservation: 100% canonical B2 | target 100% | gap 0

Research conclusion:
- scientific IE benefits from structured event/argument representations;
- relation-aware information helps argument-role disambiguation;
- high-precision syntactic relation constraints reduce false relation candidates;
- decomposition quality must remain aligned with downstream verifier needs;
- mathematical-symbol reasoning should remain explicitly structured where possible.

Exact next authorized checkpoint:
`AT0-EN V2.4 B2.2 — FROZEN FOUR-ARM REVALIDATION WITH RELATION-AWARE PROTOTYPE`

Next checkpoint must:
- use same frozen B2 raw pairs
- preserve GG/GE/EG/EE separation
- keep gates unchanged
- check A1 anchor/provenance non-regression
- audit critical relation support per side
- freeze first repaired B2 result before any further repair

Not authorized:
- live generation
- HW1-EN
- untouched holdout
- production claims


## 2026-10-03 — AT0-EN V2.4 Gate B2 CLOSED / PASS

Status:
- Gate B2: 100% COMPLETE
- Gate B overall: 100% COMPLETE
- whole ACAD_PASS planning estimate: approximately 33% ±5%

Canonical repaired revalidation:
- run: `37150199075`
- trigger commit: `6d8a38c9befb8729c093efaeca1feb7a67e47942`
- artifact id: `11283159352`
- artifact SHA-256: `08b9d7a31a611b4fe0d6e8cd25deaffc8f254950c7173cc68666164ed0c23aec`

Result:
`PASS_B2_EXTRACTED_DEVELOPMENT`

Frozen result:
`phase2/academic_transform/at0_en/v2_4/gate_b2/results/B2_2_REVALIDATION_FROZEN.json`
commit:
`d39108f7f375124ef7b6fa03d18c2a8e496de91c`

Final closure:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_FINAL_CLOSURE.md`
commit:
`ff56323d1c9a75211eaf33dc753d2a6a642166f9`

Four-arm repaired result:
- GG: pair accuracy 100%; safe acceptance 100%; adversarial acceptance 0%
- GE: pair accuracy 91.67%; safe acceptance 80%; adversarial acceptance 0%
- EG: pair accuracy 91.67%; safe acceptance 80%; adversarial acceptance 0%
- EE: pair accuracy 100%; safe acceptance 100%; adversarial acceptance 0%; REVIEW preservation 100%

Representation audit:
- 24 sides
- 102 checks
- 0 failures

Improvement vs canonical first B2:
- EE pair accuracy: 33.33% -> 100% = +66.67 pp
- EE safe acceptance: 0% -> 100% = +100 pp
- GE pair accuracy: 41.67% -> 91.67% = +50 pp
- EG pair accuracy: 50% -> 91.67% = +41.67 pp
- no adversarial-acceptance regression

Shared-error safeguard:
EE=100% while GE/EG=91.67% triggered mandatory review.

Review:
`phase2/academic_transform/at0_en/v2_4/gate_b2/B2_2_SHARED_ERROR_REVIEW_P01.md`
commit:
`4e0ec1001487dbf7375429e562b793f7d78ea9c3`

Finding:
`CANONICALIZATION_FIXTURE_MISMATCH / NOT_SHARED_SEMANTIC_ERROR`

Reason:
B2 raw fixture appends relation evidence as standalone text. For B1-P01, the extractor legitimately emits an additional MATERIAL assertion from the supported relation-evidence sentence. Gold represents the same material only as relation evidence. EE therefore uses the same redundant-but-supported representation on both sides; GE/EG compare gold-vs-extracted representation shapes and miss the pair.

No repair was made after this review.
GE/EG remain visibly reported at 91.67%.

Strong-adoption reporting:
- extracted-graph pair accuracy: current synthetic development EE 100% | target >=95% | target exceeded on this development set only
- authentic in-domain safe automatic acceptance: NOT YET MEASURED as benchmark | target >=90%
- automatic-PASS selective precision end-to-end: NOT YET MEASURED | target >=99%
- adversarial automatic acceptance: current B2 0% | target 0%
- critical silent scientific errors: 0 observed on measured development evidence | target 0
- human-correct alignment: 100% | target 100%
- ambiguity preservation: 100% | target 100%

Important interpretation:
B2 is a DEVELOPMENT PASS only.
Do not convert synthetic-development 100% into a generalization or production claim.

Recent research review at B2 close:
- scientific full-text relation extraction remains difficult;
- high intra-dataset scores do not guarantee cross-dataset transfer;
- correct final labels without aligned evidence/rationales can hide unfaithful reasoning.

Exact next authorized checkpoint:
`AT0-EN V2.4 PRE-GATE-C — PIPELINE FREEZE + END-TO-END HOLDOUT PROTOCOL`

Purpose:
- freeze complete verifier pipeline identity
- freeze Gate C denominators/outcomes/metrics/audit rules
- design authentic end-to-end untouched evaluation without opening it before pipeline freeze
- preserve predictions-first / labels-second
- perform focused higher-model consultation because Gate C benchmark design is high-stakes construct-validity work

Not authorized yet:
- opening/running a new untouched holdout
- live transformation generation
- HW1-EN
- production readiness claims


## 2026-10-03 — AT0-EN V2.4 PRE-GATE-C pre-consultation checkpoint CLOSED

Status:
- PRE-GATE-C: approximately 65% complete
- whole ACAD_PASS planning estimate: approximately 34% ±5%

Pipeline freeze:
- canonical run: `37150864483`
- trigger commit: `c0193aa3f578cc32b454a031ead73ff7e56c8918`
- artifact id: `11284520199`
- artifact SHA-256: `74f765f614b616da2eb101c30d669de0c0931b304a377944be2a4039fe5a844c`
- result: PASS

Frozen core runtime identities:
- schema: `df986f759a114bd86525b84f00f8d2f362d71bb31546441992291d21c5ebd69f`
- criticality rules: `1599bf6bdb10afd462ba45a422b3e276a4ddbb47656d3d6047a0ff9b39acc48d`
- outcome contract: `aeff55ec0d5c10a949afc2f86a5eae46e610043f3885497643561b17aa669905`
- A1 anchor/provenance: `65d0da4b32b8297dd58ba6108fb2a49e0cb96dfa726ce270f0382318919e20db`
- A2 assertion extractor: `32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`
- B2.2 relation-aware layer: `f44a4de5536dae62b8a65a4370d186c8f0087a6bf24e5e4f2d37d25ca3600478`
- B1.1 aligner: `289d2898c89850f691d52313a1d2a2b12b37cef6b674549215579caedf84cd42`

Freeze rule:
any runtime modification after Gate C protocol freeze creates a new pipeline version and invalidates direct comparison with old Gate C predictions.

Operational negative evidence:
- first freeze run `37150815799` failed because checker repository-root path was one directory too high
- checker path only was repaired
- runtime components did not change
- canonical second run passed

Holdout status:
- no Gate C source sampled
- no Gate C candidate constructed
- no Gate C gold created/opened
- no Gate C predictions generated

Pre-consultation protocol:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_PROTOCOL_PRECONSULT_V1.md`
commit:
`d3d57fd45741b8d20114ced9a865b1d705f46057`

Proposed Gate C design pending consultation:
- 80 independent authentic source clusters
- 5 domains x 16 sources
- 80 faithful PASS transactions
- 80 material-drift REJECT transactions
- 40 ambiguity REVIEW transactions
- total 200 transactions
- primary statistical independence unit = source cluster

Proposed gold:
- two independent qualified reviewers
- blind to verifier prediction and each other
- third-reviewer disagreement adjudication
- critical source/candidate evidence spans recorded
- without this, Gate C can only be provisional

Proposed sealed execution:
1. freeze unlabeled inputs
2. freeze/seal gold
3. hash both
4. run predictions
5. hash predictions
6. reveal frozen gold
7. score once
8. preserve failures

Frozen-architecture Gate C minimum:
- dangerous adversarial automatic PASS = 0
- safe automatic acceptance >=75%

Pre-consultation proposed additional gates:
- REJECT -> auto PASS = 0/80
- REVIEW -> auto PASS = 0/40
- critical silent errors = 0
- unsupported critical evidence for auto decision = 0
- safe acceptance >=60/80
- decisive REJECT >=60/80 (pending consultation)
- exact REVIEW preservation >=36/40 (pending consultation)
- critical evidence-trace completeness =100%

Strong-adoption targets remain:
- adversarial automatic acceptance 0%
- critical silent scientific errors 0
- automatic-PASS selective precision >=99%
- authentic safe automatic acceptance >=90%
- end-to-end decision accuracy >=95%
- critical relation/ownership correctness 100%
- critical evidence/provenance completeness 100%

Statistical boundary:
Gate C with 80 independent source clusters is not sufficient by itself to establish <1% true error.
Under a simple independent one-sided 95% binomial calculation, about 299 zero-error independent decisions are needed for an upper error bound below 1%.
Transactions clustered under one source cannot be naively treated as independent.

Fresh research at PRE-GATE-C:
- benchmark leakage/contamination can inflate evaluation results
- recent/dynamic/decontaminated evaluation improves credibility
- abstention must be evaluated separately from correctness
- final labels without faithful evidence/rationale alignment can hide unfaithful reasoning

Higher-model consultation packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/PRE_GATE_C_HIGHER_MODEL_CONSULTATION_PACKET_V1.txt`
commit:
`28450f6d2c81e2c71a7edd5ccd4b8bcfe1ba4836`

Pre-consult closure:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/PRE_GATE_C_PRECONSULT_CLOSURE.md`
commit:
`ebffda51c87878a067f833717273b590cf7eb830`

Permanent metric reporting format:
`Metric | Current measured result | Strong-adoption target | Gap`

Current key metric ledger:
- development EE extracted-graph accuracy: 100% | strong target >=95% | exceeded on synthetic development only
- authentic safe auto acceptance: NOT YET MEASURED | strong target >=90%
- end-to-end automatic-PASS selective precision: NOT YET MEASURED | strong target >=99%
- adversarial automatic acceptance: 0% development | strong target 0%
- critical silent scientific errors: 0 observed development | strong target 0
- ambiguity preservation: 100% development | strong target 100%

Exact next action:
WAIT for user-mediated higher-model consultation response.

No untouched holdout may be opened before final protocol freeze.


## 2026-10-03 — PRE-GATE-C final protocol freeze CLOSED

Status:
- final-protocol freeze checkpoint: 100% COMPLETE
- PRE-GATE-C overall: approximately 85%
- whole ACAD_PASS planning estimate: approximately 35% ±5%

Higher-model verdict:
`ACCEPT_WITH_ESSENTIAL_PROTOCOL_AMENDMENTS`

Final Gate C protocol:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_PROTOCOL_FINAL_V1.md`
commit:
`2f9286614741c8168c6e45b8f9fb7a7366e4a18a`
SHA-256:
`f41fdc9aa6c574447779858cdbd5a2dec83a9851c81408cc415be58c8eda1d1e`

Higher-model response record:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/PRE_GATE_C_HIGHER_MODEL_RESPONSE_V1.md`
commit:
`dfe4b76ebd48ec73ef9321226f91653748cbad3b`

Final protocol integrity:
- run: `37153113766`
- trigger commit: `830d53d6a7fe6fc04df032c432c6244c60b5b67e`
- artifact id: `11284443202`
- artifact digest: `7a1bfbdd09cf51c5d8ad0e71bff7db0853d26eff47b6742558005ca3e70b5a3f`
- status: PASS
- protocol checks: 19
- pipeline component checks: 9
- holdout opened: false
- source sampling authorized: false

Final Gate C design:
- 80 independent original studies
- five domains x 16 studies
- target temporal mix per domain: 8 first publicly available in 2026 + 8 older unseen
- PASS transactions: 80
- REJECT transactions: 80
- REVIEW transactions: 40
- total transactions: 200
- primary inferential independence unit: original source study/paper

Final progression gates:
Safety:
- REJECT -> automatic PASS = 0/80
- REVIEW -> automatic PASS = 0/40
- critical silent scientific errors = 0
- unsupported critical evidence used for auto PASS/REJECT = 0

Usability:
- faithful safe automatic acceptance >=60/80 =75%
- decisive material-drift REJECT >=60/80 =75%
- REVIEW preservation >=36/40 =90%

Evidence:
- critical evidence reference completeness =100%
- critical evidence semantic support =100%
- decision-path linkage =100% where runtime records it

INVALID_VERIFICATION:
- separate outcome
- never success
- remains in denominators/reporting

Human gold:
- two qualified independent initial reviewers
- third qualified reviewer only for unresolved material disagreement
- blind to prediction, construction class, constructor rationale and each other's initial judgments
- without qualified independent human adjudication Gate C is PROVISIONAL only

Statistical plan:
- source study is primary independence unit
- cluster bootstrap whole source clusters within domain for non-boundary metrics
- exact one-sided binomial bounds for zero-event safety
- 0/80 zero events ~3.68% one-sided 95% upper bound under simple independent Bernoulli assumptions
- Gate C does not establish <1% error or >=99% reliability
- later simple zero-error <1% claim needs >=299 appropriately independent decisions for the relevant claim

Strong-adoption targets unchanged:
- adversarial automatic acceptance 0%
- critical silent scientific errors 0
- automatic-PASS selective precision >=99%
- authentic in-domain safe automatic acceptance >=90%
- end-to-end decision accuracy >=95%
- critical relation/ownership correctness 100%
- critical evidence/provenance completeness 100%

Eight holdout-opening conditions:
1. scope/context freeze
2. sampling/temporal/de-duplication/exposure freeze
3. family/REVIEW/replacement policy freeze
4. qualified adjudicators + guide
5. role/access separation + neutral IDs
6. full pipeline/runtime/settings verification
7. metrics/statistics/evidence audit/report weights freeze
8. one-shot failure/exclusion/gold-correction/full-reporting policy freeze

Current opening readiness:
- conditions 1,2,3,6,7,8 substantially specified in final protocol
- still require operational confirmation:
  4. qualified independent adjudicators
  5. actual role/access separation and sealed-gold mechanism

Therefore:
`SOURCE_SAMPLING_NOT_YET_AUTHORIZED`

Final-protocol closure:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/PRE_GATE_C_FINAL_PROTOCOL_FREEZE_CLOSURE.md`
commit:
`f8d81e4618a6e30203084a44f7c290c6ac9875c1`

Permanent metric-reporting format:
`Metric | Current measured result | Strong-adoption target | Gap`

Current key metric ledger:
- development EE extracted-graph accuracy: 100% | target >=95% | exceeded development-only
- authentic safe auto acceptance: NOT YET MEASURED | target >=90%
- end-to-end automatic-PASS selective precision: NOT YET MEASURED | target >=99%
- adversarial automatic acceptance: 0% development | target 0%
- critical silent scientific errors: 0 observed development | target 0
- ambiguity preservation: 100% development | target 100%

Exact next authorized checkpoint:
`AT0-EN V2.4 PRE-GATE-C — HOLDOUT-OPENING READINESS SETUP`

Do not select/open Gate C sources until this checkpoint verifies all eight opening conditions.


## 2026-10-03 — Canonical cross-conversation continuity + reviewer acquisition solution

New canonical continuity file:
`ACAD_PASS_MASTER_CONTINUITY.md`

Commit:
`e83bdd99cfa3046a1e66c90b2c35f6d45f20e3ce`

Permanent continuity rule:
- new conversations must read `ACAD_PASS_MASTER_CONTINUITY.md` first;
- then read the latest end of `RESUME_HERE.md`;
- verify branch HEAD;
- continue only the exact authorized next checkpoint;
- never restart completed stages or consumed one-shot experiments;
- update both files after every material result, failure, decision, agreement, or exact-next-step change.

User output preference:
- concise responses;
- concise output likely reduces context consumption and may help extend conversation longevity, though no exact conversation-length guarantee is possible.

Human reviewer problem:
- user has no pre-existing human reviewers.

Preferred solution:
`INTERNET_RECRUITED_QUALIFIED_HUMAN_ADJUDICATION`

Plan:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_INTERNET_EXPERT_ADJUDICATION_PLAN_V1.md`

Plan commit:
`710367d45b5cb2b8b2138da29ad1118230e851d1`

Primary reviewer-acquisition routes:
1. Kolabtree — domain-specific scientists/peer-review consultants.
2. Prolific Domain Experts — verified specialist recruitment.

Reviewer design:
- 2 independent primary reviewers/domain
- reserve/adjudicator for unresolved material disagreement
- target 10 primary reviewers total + up to 5 reserve/adjudicators

Reviewer qualification:
- frozen qualification pack
- domain credentials
- scientific-fidelity task
- evidence-span task
- ambiguity-vs-difficulty task
- critical-relation task
- public expert-annotated scientific datasets such as SciFact may be used only for qualification/calibration

SciFact does NOT replace Gate C because its construct is scientific claim verification, not full source-candidate academic transformation fidelity.

Low-budget fallback:
- Gate C may proceed only as `PROVISIONAL_RESEARCH_EVIDENCE`
- multiple independent model judges + deterministic checks + expert-labeled public calibration
- never call this independent human gold
- never use it for non-provisional Gate C / Strong-Adoption claims

Current Gate C opening state:
`SOURCE_SAMPLING_NOT_YET_AUTHORIZED`

Exact next authorized checkpoint remains:
`AT0-EN V2.4 PRE-GATE-C — HOLDOUT-OPENING READINESS SETUP`

Immediate scope:
- freeze reviewer qualification pack and thresholds
- freeze recruitment briefs
- determine Kolabtree/Prolific/hybrid operational route
- define neutral reviewer IDs and assignments
- define gold access separation
- verify all 8 holdout-opening conditions


## 2026-10-03 — Deep research: no-new-human Gate C alternative

User explicitly requested a serious attempt to eliminate the need for newly recruited human reviewers.

New researched direction:
`EXTERNAL_HUMAN_GOLD_COMPOSITE_VALIDATION`

Plan:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_NO_NEW_HUMAN_ALTERNATIVE_RESEARCH_V1.md`
commit:
`a8a613f28988046ccd37411760cbf8aa4c66a0cb`

Research found multiple independent published human/expert-labeled resources suitable for triangulated validation:
- SciFact
- SciFact-Open
- QASPER
- DeFacto
- TRUE
- SummaC
- AGGREFACT
- FRANK
- FENICE long-form annotations
- QASemConsistency 2026
- clinical-study summarization factuality annotations
- PlainFact / PlainQAFact
- USB

Complement with deterministic ACAD_PASS-specific metamorphic tests.

Important scientific boundary:
- no single dataset fully matches ACAD_PASS transformation fidelity;
- a frozen composite suite can yield non-provisional external-benchmark validation for the represented constructs;
- this must not be mislabeled as fresh bespoke human-adjudicated Gate C;
- dataset-specific label-to-ACAD_PASS mapping contracts must be frozen before execution.

Potential revised Gate C:
- `Gate C-EXT` = external published human-gold validation
- `Gate C-META` = deterministic metamorphic relation validation

Immediate decision:
- do NOT recruit reviewers yet;
- do NOT open custom 80-study holdout yet;
- current frozen custom Gate C protocol remains preserved, not deleted.

Exact next recommended checkpoint:
`PRE-GATE-C — EXTERNAL HUMAN-GOLD COMPOSITE FEASIBILITY AUDIT`

Scope:
1. dataset inventory;
2. licenses/downloadability;
3. label schemas;
4. usable labeled counts;
5. overlap/deduplication;
6. adapter contracts;
7. construct-coverage map;
8. decide whether fresh human adjudication can be eliminated entirely or reduced to a small residual study.

Master continuity updated:
`ACAD_PASS_MASTER_CONTINUITY.md`
commit:
`1a30755f0ef2c8af43367ad0142eaa9d4ceb5e0e`


## 2026-10-04 — External Human-Gold Composite feasibility audit CLOSED

Audit:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/EXTERNAL_HUMAN_GOLD_COMPOSITE_FEASIBILITY_AUDIT_V1.md`
commit:
`609d9ca39d5fbb333887c6f09b85a36b8d554b9d`

Verdict:
`FEASIBLE_WITHOUT_NEW_HUMAN_ADJUDICATORS_FOR_RESEARCH_PROGRESSION`

Core external tracks:
- DeFacto
- PLABA
- CLEF SimpleText 2025 human-annotated real scientific simplifications if accessible
- SciFact
- QASemConsistency
- USB
- PlainFact positive biomedical track

Secondary/diagnostic:
- QASPER
- TRUE
- AggreFact
- FENICE
- optional non-overlapping SciFact-Open
- Cochrane-auto
- 2026 expert-edited scientific simplification corpus

Proposed replacement:
- `Gate C-EXT` = multiple independent published human/expert-gold tracks
- `Gate C-META` = deterministic ACAD_PASS-specific metamorphic relation tests

Critical mapping rule:
never force every external dataset into PASS/REJECT/REVIEW.
Use native labels unless an exact adapter is frozen.

Key overlap risks:
- SciFact/SciFact-Open
- TRUE/components
- AggreFact/components
- QASemConsistency underlying datasets
- DeFacto derivatives
- PLABA/TREC shared sources

High-stakes protocol replacement has NOT been approved yet.
Current custom 80-study Gate C protocol remains preserved and unopened.

Higher-model consultation packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/NO_NEW_HUMAN_HIGHER_MODEL_CONSULTATION_PACKET_V1.txt`
commit:
`9d015241f52244448f7ccb9800e0a473f8a7f213`

Master continuity updated:
`ACAD_PASS_MASTER_CONTINUITY.md`
commit:
`180ba1e2c141d2346b6156e78564bfa4962c7385`

Exact next action:
user-mediated higher-model construct-validity consultation.

Until consultation response:
- do not recruit reviewers
- do not open custom Gate C
- do not execute external suite
- do not modify frozen V2.4 runtime


## 2026-10-04 — No-new-human higher-model consultation received and EXT/META protocol amendment frozen

Independent higher-model verdict:
`B — YES_WITH_ESSENTIAL_CHANGES`

Meaning:
- `Gate C-EXT + Gate C-META` may replace the custom newly-human-adjudicated 80-study Gate C for the next research-progression decision.
- do not recruit new human reviewers now.
- original custom Gate C remains frozen, preserved and unopened.
- residual human study status:
  `DEFERRED — CONDITIONALLY REQUIRED FOR UNCOVERED CLAIMS`.

Important consultation corrections accepted:
- PLABA is not automatically PASS gold.
- PlainFact remains secondary unless exact human validation supports the measured label.
- CLEF SimpleText hard evidence must use actual human-annotated real-system material, not synthetic distortion training records.
- QASemConsistency is relation-level evidence, not full-source completeness evidence.
- metamorphic testing requires formal oracle validity + matched controls; it cannot prove absolute correctness by itself.
- “all output content is supported” and “all required source content is preserved” are separate constructs.
- retain native dataset semantics unless an exact ACAD_PASS adapter mapping is justified.
- no weighted aggregate may compensate a safety failure.

Fresh implementation-agent web verification after consultation confirmed:
- FactPICO (ACL 2024): 345 RCT plain-language summaries with fine-grained expert judgments/rationales on PICO and findings.
- FaReBio (EMNLP Findings 2024): expert-annotated biomedical summary faithfulness + supporting evidence.
- LongSciVerify (LREC-COLING 2024): human fine-grained factual consistency for long scientific-document summaries.
- CLEF SimpleText 2026 official docs explicitly reuse manual annotations from 2025 submissions as ground truth for distortion classification.

New prioritized H1 audit candidates:
- FactPICO
- FaReBio
- LongSciVerify

Decision record:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/NO_NEW_HUMAN_HIGHER_MODEL_CONSULTATION_DECISION_V1.md`
commit:
`d6dbb95053a2d95a1d273eeff9a71e00afbfa988`

Protocol amendment:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PROTOCOL_AMENDMENT_V1.md`
commit:
`7ad010a95373ecb7626bf1bea5a3b68979a08385`

Readiness contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_READINESS_V1.md`
commit:
`99803dee149e8c5f8ba6d30e830d27556f4766b9`

Pre-execution independent-review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PREEXECUTION_REVIEW_PACKET_V1.txt`
commit:
`5e18d6e71e7a4d2720d81c4d53d117a4bdb11b8f`

Hard-gate functional design frozen for review:
- H1 = scientific transformation fidelity
- H2 = scientific claim/evidence fidelity
- H3 = fine-grained relation fidelity
- H4 = deterministic ACAD_PASS metamorphic validation

Diagnostic by default:
- DeFacto
- USB
- PlainFact
- QASPER
- FENICE
- TRUE or AggreFact
- expert-edited 2026 simplification corpus
- other long-document resources unless promoted before results

Current readiness:
`NOT_READY_GATE_C_EXT_META`

No external benchmark executed.
No V2.4 prediction run on external evaluation cases.
No custom 80-study source opened.
No reviewer recruited.
No runtime change.

Quality delta:
`IMPROVED`
- independent construct-validity review now supports the no-new-human direction;
- claim boundaries tightened;
- stronger expert scientific benchmarks added;
- public-gold exposure limitation explicitly recognized;
- non-compensatory multi-track protocol frozen for review.

Current exact next checkpoint:
`USER-MEDIATED HIGHER-MODEL PRE-EXECUTION REVIEW`

User should provide the higher model:
`GATE_C_EXT_META_PREEXECUTION_REVIEW_PACKET_V1.txt`

Until that response:
- do not freeze/execute final external dataset suite;
- do not run verifier on external evaluation cases;
- do not open original custom Gate C;
- do not recruit new humans;
- do not modify V2.4.


## 2026-10-04 — Second EXT/META pre-execution review accepted; V2 protocol frozen

Independent review verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

The review explicitly authorizes the next non-execution stage:
`dataset / version / split / adapter / metric / overlap freezing`

with:
`ZERO NEW-HUMAN RECRUITMENT AT THIS STAGE`

No external benchmark execution is authorized yet.

Key required changes accepted:
1. H1 must prove two separate functions:
   - output-content support/factuality;
   - preservation/completeness of required source content.
2. H2/H3 must be measurable from actual frozen V2.4 outputs without semantic helper inference.
3. evidence location/reference correctness != semantic support correctness.
4. META oracle must be independent from verifier output AND extractor semantic assumptions/rules.
5. denominators, sample/source-cluster targets, thresholds, missing/invalid handling and success rules must be frozen before prediction.

H1 resource status:
- FactPICO = CONDITIONAL SUBSTITUTE
- FaReBio = CONDITIONAL SUBSTITUTE
- LongSciVerify = DIAGNOSTIC ONLY

Preferred minimum H1 candidates:
- CLEF SimpleText human-annotated real-system outputs
- eligible PLABA/TREC human judgments

Additional H1 resource only if exact frozen labels reveal a construct gap.

H2:
SciFact remains claim/evidence only.
Gold evidence cannot be used to claim full retrieval evaluation.

H3:
QASemConsistency remains relation-level only.
Gold QA decomposition cannot assist inference.
Unmatched relations cannot be dropped from the frozen denominator.

META/REVIEW:
controlled REVIEW testing can proceed without new human labels if the oracle proves unresolvedness independently and matched anti-degenerate controls are included.
This does NOT establish natural-world ambiguity performance.

Adapter boundary strengthened:
deterministic or rule-based semantic inference is still an invalid adapter if it adds capability necessary for success.

Statistical rule:
no universal N.
Each hard track must freeze a source-cluster/sample target justified by CI width, error bound, power/effect target, or controlled-family coverage as appropriate.

Public-gold claim:
procedurally frozen prospective evaluation against previously published external human/expert labels.
Do NOT call it secret/unseen holdout validation.

No diagnostic dataset promoted to hard now.

Decision file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PREEXECUTION_REVIEW_DECISION_V2.md`
commit:
`41f518392a6aab3af4e1c0f0d2834a5736e02377`

Protocol V2:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`
commit:
`a8cd52bb731a53e1a72de6984a2eb3308fad7966`

Readiness V2:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_READINESS_V2.md`
commit:
`73c7e5673b4bbcc708e2eb69eb745c91d3e713e6`

Master continuity update:
commit:
`fc21d6d7b834170ed73ca43463cf605a2ab0ecec`

Readiness now:
- condition 1/10 = PASS
- conditions 2-10 = NOT YET PASS
- overall = `NOT_READY_GATE_C_EXT_META`

Quality delta:
`IMPROVED`

No V2.4 runtime change.
No external evaluation prediction.
No original custom Gate C source opened.
No human reviewer recruited.

Exact next checkpoint:
`PRE-GATE-C EXT/META — DATASET / VERSION / SPLIT / ADAPTER / METRIC / OVERLAP FREEZE`

Stop here until user says:
`أكمل`


## 2026-10-04 — H1 dataset/version/access/label audit V1 frozen

Checkpoint:
`PRE-GATE-C EXT/META — H1 DATASET / VERSION / ACCESS / LABEL AUDIT`

Audit file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_DATASET_VERSION_ACCESS_LABEL_AUDIT_V1.md`

Audit commit:
`87485c350c148668fcba85fc6d6bca802b1c5001`

Readiness V2 updated:
commit:
`4025a5a295228e47ba7509d3acbb03027638daba`

Master continuity updated:
commit:
`897fed6ce816fd16d1f10045cd9259bb07e655ec`

### CLEF SimpleText 2025
Verified:
- official Task 2 identity and paper;
- official 2026 page explicitly states that manual CLEF 2025 Task 1 annotations are reused as ground truth for 2026 information-distortion classification;
- 2025 data are made available to registered participants;
- CLEF 2025 Task 2 Codabench remains operational;
- site repository main HEAD observed:
  `14cb2f19a5eb7e8d7d3382b241578c5affc5bbac`;
- repository-level license metadata is absent.

Not frozen:
- official human annotation artifact bytes;
- exact eligible IDs;
- exact dataset license/reuse terms;
- artifact hashes.

Construct:
- H1-S = strong candidate;
- H1-C = unresolved until exact annotation coverage/artifact inspection.

### PLABA original
Verified:
- DOI `10.1038/s41597-022-01920-3`;
- 750 abstracts;
- 7,643 sentence pairs;
- manual adaptation;
- OSF project identity `rnpmf`;
- official artifact name `data.json`;
- data keyed using question identity and PMID.

Access issue:
direct OSF download failed through current tools.

License boundary:
article = CC BY 4.0;
dataset-specific license = NOT SEPARATELY VERIFIED.

Permanent:
PLABA human reference is NOT automatic full-preservation PASS because omission is permitted.

### TREC PLABA 2023
Manual completeness/faithfulness is evaluated only on up to 3 question-relevant sentences per abstract.
Therefore:
`H1-C = PARTIAL / SAMPLED-SCOPE`

### TREC PLABA 2024
Task 2 = complete abstract adaptation.
Expert manual evaluation includes:
- simplicity;
- accuracy;
- completeness;
- brevity.

Completeness explicitly targets minimizing information lost from the original.

2025 retrospective paper confirms:
- 2023 + 2024 PLABA tracks;
- four professionally written references;
- extensive biomedical-expert manual evaluation;
- factual accuracy + completeness judgments.

Current classification:
`STRONGEST PLABA-FAMILY H1-C CANDIDATE`

But:
TREC 2024 reusable record-level judgment artifact + reuse/license terms remain NOT FROZEN.

### Readiness after checkpoint

Condition 1:
`PASS`

Condition 2:
`PARTIAL / NOT PASS`

Condition 3:
`PARTIAL / NOT PASS`

Condition 8:
`PARTIAL`

Condition 10:
`PARTIAL`

Other conditions:
`NOT READY`

Overall:
`NOT_READY_GATE_C_EXT_META`

Quality delta:
`IMPROVED / ACCESS-BLOCKED`

No V2.4 prediction.
No scoring.
No custom Gate C opening.
No human recruitment.
No runtime change.

Exact next checkpoint:
`H1 ACCESS + ARTIFACT RESOLUTION`

Next scope:
- SimpleText 2025 annotation artifact/access/license;
- PLABA OSF artifact/license metadata;
- TREC 2024 expert judgment artifact/reuse path;
- then exact H1 IDs/hashes/adapters.

Stop here until user says:
`أكمل`


## 2026-10-04 — H1 access + artifact resolution substantially improved

Resolution file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_ACCESS_ARTIFACT_RESOLUTION_V1.md`

Commit:
`f88fe5b599ade9b85e6a301b350bc33c2163e331`

Readiness update:
`451c4a19b8b825d5de2df026152b19bff79fbe16`

Master continuity update:
`12b3cdf8ec791e5efcf056dd323d6c10f422e588`

Quality delta:
`IMPROVED`

Key resolution:
public Zenodo dataset `10.5281/zenodo.18637045` exposes raw TREC PLABA manual judgments.

Relevant artifacts:
- `manual-judgments-task1-2023.csv`
  MD5 `0f320090ce516d799b4e970ebb3194a4`
- `manual-judgments-task1-2024.zip`
  MD5 `589ad66e0b9324592f0151cc67974015`
- `manual-judgments-task2-2024.zip`
  MD5 `c23fe9c96addedb9c8ad4a8901734996`

Critical task-numbering issue resolved:
- original TREC 2024 naming: Task 2 = Complete Abstract Adaptation
- retrospective publication / Zenodo normalization: Task 1 = Rewriting Abstracts

Therefore H1 complete-rewrite manual judgment archive is:
`manual-judgments-task1-2024.zip`

2024 retrospective manual axes:
- ACC = accuracy relative to source
- COM = completeness / information preservation
- SIM = simplicity
- BRV = brevity
- FIN = mean of axes

Paper states:
- 19 2024 complete-rewrite submissions;
- sentence-level outputs across all 400 test abstracts were manually evaluated;
- manual evaluation is treated as gold standard.

Preferred H1 conceptual core:
- H1-S <- ACC
- H1-C <- COM

No outcome mapping frozen yet.

TREC corpus public route identified:
`https://trec.nist.gov/data/plaba/PLABA_2024-Task_2.zip`

Rights:
- TREC research-use/data-sharing path identified;
- Zenodo record publicly Open;
- explicit license value not shown in Zenodo metadata;
- exact applicable reuse agreement remains to be frozen.

FaReBio:
- expert faithfulness/evidence benchmark;
- 25 articles / 175 summaries / 1,445 sentences;
- public for research only;
- conditional H1-S support, not H1-C.

SimpleText:
optional/access-gated; no longer blocks H1.

Current readiness:
- condition 1 PASS
- condition 2 SUBSTANTIAL PARTIAL / NOT PASS
- condition 3 SUBSTANTIAL PARTIAL / NOT PASS
- condition 4 NOT READY
- overall NOT_READY_GATE_C_EXT_META

No V2.4 prediction.
No benchmark score.
No custom 80-study holdout opened.
No human recruitment.
No Arabic-track work.

Exact next checkpoint:
`H1 RAW ARTIFACT + SCHEMA + TERMS FREEZE`

Stop until user says:
`أكمل`


## 2026-10-04 — H1 raw artifact + schema + terms freeze V1

Freeze file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_RAW_ARTIFACT_SCHEMA_TERMS_FREEZE_V1.md`

Commit:
`a4e4d01a6f3b0ff2dba6360327c523e587e1c282`

Readiness update:
`3cb83a562fe96705c0c7b84de3a07e5089f26d31`

Master continuity update:
`ab946b94c00b3757e00622df07520f5d2757c860`

Quality delta:
`IMPROVED / TOOLING-MATERIALIZATION BLOCKED`

Frozen:
- H1 core artifact identity:
  `manual-judgments-task1-2024.zip`
- Zenodo DOI:
  `10.5281/zenodo.18637045`
- publisher MD5:
  `589ad66e0b9324592f0151cc67974015`
- public NIST/TREC complete-adaptation source URL:
  `https://trec.nist.gov/data/plaba/PLABA_2024-Task_2.zip`

Directly verified 2023 manual-judgment physical schema:
`Source, Output, Answer, Simp. sent, Simp. term, Simp. term acc., Simp. fluency, Acc. comp., Acc. faith., Team, Sent, Abst`

2024 logical manual schema frozen:
- ACC = accuracy relative to source
- COM = completeness / minimize information loss
- SIM = simplicity
- BRV = brevity
- FIN = aggregate

Preferred conceptual H1:
- H1-S <- ACC
- H1-C <- COM

No binary outcome threshold frozen.

TREC handling policy frozen conservatively:
- research use only
- scientific reporting allowed subject to TREC/copyright terms
- do not redistribute raw TREC/PLABA source text in public ACAD_PASS repo
- public repo may contain IDs/hashes/protocol metadata/derived metrics

Zenodo record:
- Open public access verified
- explicit license value not shown
- unrestricted redistribution NOT assumed

Independence:
`original biomedical abstract / PMID = source cluster`

Potential pool:
400 TREC 2024 test abstracts.

Still blocked:
- local ZIP byte copy
- local SHA-256
- exact 2024 TSV physical headers
- exact PMID/source-cluster manifest
- explicit Zenodo license/reuse record
- H1 adapter/native metric contract

Tooling result:
web can resolve the public ZIP URL but cannot ingest the binary due size/content type;
local runtime has no external DNS, so direct byte materialization failed.

If manual upload is needed, request exactly:
1. `manual-judgments-task1-2024.zip`
2. `PLABA_2024-Task_2.zip`

Current readiness:
- condition 1 PASS
- condition 2 substantial partial / not pass
- condition 3 substantial partial / not pass
- condition 4 NOT READY
- overall `NOT_READY_GATE_C_EXT_META`

No V2.4 prediction.
No scoring.
No original custom Gate C opening.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`H1 PHYSICAL SCHEMA + SOURCE-CLUSTER FREEZE`

Stop here until user says `أكمل` and/or provides the two public ZIPs.


## 2026-10-04 — H1 physical schema + source-cluster freeze complete

Freeze file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_PHYSICAL_SCHEMA_SOURCE_CLUSTER_FREEZE_V1.md`

Commit:
`1cb73aa79658462d105be0de02f2e2acb6f16023`

Readiness update:
`4ed5de1969a889e88c0e8f25ca30305017c3ae7c`

Master continuity update:
`f412d0b17dd2d233f305becb46cb06db70071d45`

User supplied:
- `manual-judgments-task1-2024.zip`
- `PLABA_2024-Task_2.zip`

Raw integrity:
- manual judgments SHA-256:
  `8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce`
- manual judgments MD5:
  `589ad66e0b9324592f0151cc67974015`
  publisher MD5 match = YES
- source ZIP SHA-256:
  `f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e`
- source ZIP MD5:
  `daa454a5234161489fef52eab1ebec26`
- test.json SHA-256:
  `2d53f485082ea16571ac54d9f3bcbd56c1c199130d4b8542e93b678ed561e9a7`

Exact judgment TSV schema:
`Abstract, Sentence, Source, Target, Accuracy, Completeness, Simplicity, Brevity`

Source corpus:
- 40 questions
- 400 abstract slots
- 4,060 source sentences
- 399 unique PMIDs

Duplicate:
PMID `15857353`
appears in:
- Q14_A3
- Q37_A5
with exact same seven source sentences.

Therefore:
`PMID = H1 source-cluster unit`
and max independent clusters = 399.

Judgment archive:
- 19 runs
- 76,790 rows
- 14 complete 4,060-row runs
- 5 incomplete runs
- 350 missing run×sentence rows
- 315 unique source-sentence pairs missing in >=1 run
- 0 extra rows
- 0 empty target fields

All retained rows match test.json exactly by:
- Abstract
- Sentence
- Source text

Score alphabet:
`-1, 0, 1`

Gold-only descriptive distributions:
Accuracy:
- -1 2,084
- 0 10,296
- 1 64,410

Completeness:
- -1 3,151
- 0 16,992
- 1 56,647

No ACAD_PASS predictions were run.

Quality delta:
`IMPROVED`

Current readiness:
- Condition 1 PASS
- Condition 2 substantial partial / rights terms remain
- Condition 3 substantial partial / final eligible subset not frozen
- Condition 5 H1 internal clustering frozen
- Conditions 4 and 6 NOT READY
- overall `NOT_READY_GATE_C_EXT_META`

Exact next checkpoint:
`H1 ADAPTER + NATIVE METRIC CONTRACT FREEZE`

Next work:
- decide native ACC/COM handling vs exact ACAD_PASS mapping;
- freeze eligible records/runs;
- freeze denominator and incomplete-run handling;
- freeze PMID-clustered statistics;
- freeze thresholds/sample-size rationale;
- prove no semantic helper inference is needed.

No V2.4 prediction.
No scoring.
No original custom Gate C opening.
No human recruitment.
No Arabic work.

Stop here until user says:
`أكمل`


## 2026-10-04 — H1 adapter/native-metric contract V2 frozen for independent review

Preferred contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_ADAPTER_NATIVE_METRIC_CONTRACT_V2.md`

Commit:
`23a613da183157c14ef5c1c82051a5014dbca18e`

Review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTRACT_V2_HIGHER_MODEL_REVIEW_PACKET.txt`

Review packet commit:
`0f583d601f8d195797e597308887465864dd3c94`

Readiness update:
`5cc7f8c3339d4db3d67fdc51d1f19652c19f5e1b`

Master continuity update:
`f6af52f70f6a0a6a351628ec0f4ce04f656bd6f5`

Quality delta:
`IMPROVED`

Key V2 changes:
1. utility confirmatory subset = 14 complete PLABA runs only;
2. safety population = all observed qualified-negative gold across all 19 runs;
3. exact Source==Target positive rows removed from primary transformed-positive utility and kept as identity controls.

Gold strata:
- QUALIFIED_POSITIVE = ACC==1 AND COM==1
- QUALIFIED_NEGATIVE = ACC==-1 OR COM==-1
- other ACC/COM cells diagnostic only
- human score 0 is NOT ACAD_PASS REVIEW

Safety:
- 4,275 negative rows
- 396 PMID clusters
- any PASS_CANDIDATE = hard safety failure

Positive utility:
- 33,660 non-identical qualified-positive rows
- 399 PMIDs
- PMID-macro PASS_CANDIDATE >=75%

Negative utility:
- 3,677 qualified-negative rows
- 394 PMIDs
- PMID-macro REJECT >=75%
- REVIEW = safe abstention, not decisive rejection
- INVALID = non-success

Statistics:
- PMID cluster unit
- 10,000 cluster bootstrap resamples
- seed 20261004
- percentile 95% CI
- exact one-sided zero-event upper bound

Current state:
`H1 CONTRACT V2 FROZEN FOR INDEPENDENT REVIEW`

No V2.4 external prediction.
No scoring.
No threshold tuning.
No original custom Gate C opening.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`USER-MEDIATED HIGHER-MODEL REVIEW OF H1 CONTRACT V2`

Stop until user returns the complete higher-model review.


## 2026-10-04 — H1 contract V3 frozen; V2 superseded before execution

Preferred contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_ADAPTER_NATIVE_METRIC_CONTRACT_V3.md`

Commit:
`672bbc119eaa174e22365f5c4907bb47f9474a7d`

Review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTRACT_V3_HIGHER_MODEL_REVIEW_PACKET.txt`

Packet commit:
`78e5562cba86b99655acc5c54cec277e1196cbc4`

Readiness update:
`e20ea2544032fdc8c44eed6cc0c187d5ba2503fb`

Master continuity update:
`615bd9c2b6a169e71aaa187abf91f796a4ed5e94`

Quality delta:
`IMPROVED`

Why V3 was necessary:
- row-level gold = 76,790;
- unique Abstract+Sentence+Source+Target = 62,382;
- canonical PMID+Source+Target = 62,315;
- repeated identical inputs across runs must not be repeated V2.4 predictions;
- human ratings disagree across some repeated identical inputs;
- hard gold therefore requires canonical consolidation before prediction.

Frozen canonical gold:
- SAFE_STRICT = 40,609 pairs / 399 PMIDs
- ERROR_STRICT = 3,566 pairs / 396 PMIDs
- INTERMEDIATE = 16,800 pairs / 399 PMIDs
- HUMAN_CONFLICT = 1,340 pairs / 320 PMIDs

Multi-rated sensitivity:
10,554 canonical pairs:
- SAFE_STRICT 7,159
- ERROR_STRICT 455
- INTERMEDIATE 1,600
- HUMAN_CONFLICT 1,340

Frozen eligibility-manifest SHA-256:
`f0371da56290999d4786ce86ea319be15f994c8cc8075a8fddaaa81c12cf5dc9`

V3 hard rules:
- ERROR_STRICT PASS_CANDIDATE = 0
- SAFE_STRICT pair-micro PASS >=75%
- SAFE_STRICT PMID-macro PASS >=75%
- ERROR_STRICT pair-micro REJECT >=75%
- ERROR_STRICT PMID-macro REJECT >=75%

No mapping:
- 0 -> REVIEW
- human disagreement -> REVIEW

Exact-copy positive pairs remain in primary gold with prespecified subgroup reporting; they are not silently removed.

Statistics:
- PMID primary independence unit
- 10,000 whole-PMID cluster bootstrap
- seed 20261004
- 95% percentile CI
- zero-event source-cluster upper bound

Important negative evidence:
V1 and V2 are preserved.
Neither was executed.
V2 is superseded because its repeated-row/run-completeness design could inflate evidence and create incompatible hard expectations under human disagreement.

No V2.4 external prediction.
No H1 scoring.
No adapter implementation.
No custom Gate C opening.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`USER-MEDIATED HIGHER-MODEL REVIEW OF H1 CONTRACT V3`

Stop until user returns the full higher-model review.


## 2026-10-04 — H1 Contract V3 independent review accepted with essential changes

Decision file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTRACT_V3_INDEPENDENT_REVIEW_DECISION_V1.md`

Commit:
`5488022080f2d55265f1e12e168c5efef5e6c59f`

Readiness update:
`1742ba46bd82b9a006aa1d05c85d7bf15b0c0ad8`

Master continuity update:
`f2ff6d51241e1b753ef0190332ea269e5f60fba7`

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Higher-model review source:
user uploaded full review.

Core accepted:
- canonical PMID+Source+Target deduplication
- score 0 != REVIEW
- HUMAN_CONFLICT != REVIEW
- single published expert judgment acceptable under narrow claims
- multi-rated subset is sensitivity only
- pair-micro + PMID-macro framework
- PMID cluster bootstrap
- zero unsafe PASS after eligibility freeze
- no new humans now

Core blocker independently verified:
PLABA sentence-level evaluation accounts for whole-abstract context, while official guidelines allow context-dependent rewriting and task-permitted information omission.

Primary-source verification:
- entire rewritten abstract expected to read fluently as one document
- sentence-level evaluation accounts for entire-abstract context
- anaphora may be resolved from previous source sentence
- some source sentences may be ignored
- confidence intervals / p-values / similar measurements may be omitted
- context may be used to make named entities/pronouns explicit

V2.4 frozen runtime audit:
- source extractor takes one raw text string
- no separate non-protected context field
- blindly prepending prior/whole abstract context would create false preservation obligations against a single target sentence

Therefore:
`H1_NOT_READY_CONTEXT_GOLD_ALIGNMENT`

Important interpretation:
`PLABA SAFE_STRICT` is not automatically equivalent to ACAD_PASS strict protected-detail preservation.

Exact-copy policy correction:
Source==Target SAFE cases must be excluded from primary transformed-positive acceptance and kept as identity controls.

Current authorization:
`H1 CONTEXT + GOLD-SEMANTICS RESOLUTION`

Still forbidden:
- H1 adapter implementation
- V2.4 PLABA prediction
- H1 scoring
- V2.4 modification
- original custom 80-study Gate C opening
- new human recruitment
- Arabic work

Quality delta:
`MIXED / METHODOLOGICALLY IMPROVED`

Reason:
we found a genuine construct mismatch before contaminating the external evaluation.

Exact next checkpoint:
`H1 CONTEXT + GOLD-SEMANTICS RESOLUTION`

Stop until user says:
`أكمل`


## 2026-10-04 — H1 context + gold-semantics resolution complete at design level

Resolution:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTEXT_GOLD_SEMANTICS_RESOLUTION_V1.md`

Commit:
`0db47c57fc012dd95cc7a147b27745e5d8356314`

Readiness update:
`7c948cc7704bbe27dbd95b11c19a0036921e45d8`

Master continuity update:
`21bada9cadb6b490588080f8df0228cd051e9691`

Quality delta:
`IMPROVED`

PLABA conclusion:
- sentence-level alignment is not equivalent to context-free judging;
- PLABA task/guidelines permit context-dependent rewriting and omission of some details;
- PLABA cannot by itself serve as strict ACAD_PASS preservation PASS gold.

Therefore:
`PLABA-ONLY HARD H1 = REJECTED`

No post-hoc surface/semantic hard subset will be created.

PLABA remains:
`DIAGNOSTIC / AUTHENTIC TRANSFORMATION UTILITY`

Minimum hard-H1 companion selected:
`FactPICO`

FactPICO source:
ACL 2024
DOI:
`10.18653/v1/2024.acl-long.459`

Official repo:
`lilywchen/FactPICO`

Observed repo HEAD:
`2e16993a000aedb15cb348b7bcd61070d26bab14`

Repo license:
`MIT`

FactPICO hard-H1 rationale:
- whole abstract -> whole plain-language summary
- 115 RCT abstracts
- 345 generated summaries
- expert ratings for Population / Intervention / Comparator / Outcome
- rating 2 includes severe inaccuracies and/or missing critical descriptors
- rating 1 = missing
- evidence-inference ratings cover findings/results
- added-information spans and correctness are expert annotated
- full-source/full-candidate context fits frozen V2.4 interface without separate hidden context channel

Construct coverage:
- H1-S: critical factuality/support + correctness of added information
- H1-C: missing PICO descriptors/elements + missing evidence inference

Claim boundary:
`CRITICAL RCT-ELEMENT FIDELITY/PRESERVATION`
not exhaustive document preservation.

FactPICO raw data:
hosted separately via UT Austin Box.
Exact bytes + separate dataset license/reuse terms:
`NOT YET FROZEN`

InfoLossQA:
`DIAGNOSTIC ONLY`
because its QA representation is not an exact frozen V2.4 oracle without semantic adapter logic.

Current authorization:
`FACTPICO ARTIFACT + SCHEMA + LICENSE FREEZE`

Still forbidden:
- V2.4 external prediction
- H1 scoring
- runtime modification
- new human recruitment
- original custom Gate C opening
- Arabic work

Stop until user says:
`أكمل`


## 2026-10-04 — FactPICO artifact/schema/license audit partial freeze

Audit file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_ARTIFACT_SCHEMA_LICENSE_AUDIT_V1.md`

Commit:
`4c55af156df1e0f67fd8ebe4f3a06f70b5c6a813`

Readiness update:
`b842e27001e26870ed7e9125c821692d50203f48`

Master continuity update:
`10f15640b49efe562c681e54084500a50b414d59`

Quality delta:
`IMPROVED / RAW-ARTIFACT BLOCKED`

Verified:
- FactPICO ACL 2024
- 115 RCT abstracts
- 345 summaries
- three generating models
- PICO expert ratings 4/3/2/1
- Evidence Inference expert ratings
- Added Information factuality annotations
- exhaustive-outcome annotation
- FactPICO annotations CC BY 4.0
- source abstracts from PubMed Open Access reuse-compatible sources
- repository code MIT
- official repo HEAD `2e16993a000aedb15cb348b7bcd61070d26bab14`

Official data route:
`https://utexas.box.com/s/mpe5idxrqrzs1wcakphng7xfi7h4g83j`

Current tooling cannot materialize Box.

Needed:
download complete FactPICO shared folder/archive and upload unchanged.

After upload:
- compute SHA-256
- inspect exact physical schema
- reconcile 115/345
- freeze PMIDs/source clusters
- audit missing/duplicate/annotator fields
- freeze hard-gold eligibility
- draft H1 Contract V4

Current state:
`FACTPICO PARTIAL / NOT EXECUTION-READY`

No V2.4 prediction.
No H1 scoring.
No runtime modification.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`FACTPICO PHYSICAL ARTIFACT + SCHEMA FREEZE`

Stop until user uploads the Box archive or asks for download instructions.


## 2026-10-04 — FactPICO physical artifact + schema freeze complete

Freeze:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_PHYSICAL_ARTIFACT_SCHEMA_FREEZE_V1.md`

Commit:
`117cd7c4b414aa77dab22db22423d2ce6bb319e1`

Readiness update:
`58bb72ed2e9da9b11c7aec771d3a55f1d03c4bba`

Master continuity:
`130c5ba1fd060579b6d58f78f6d9e81d5e24c320`

Quality delta:
`IMPROVED`

FactPICO.zip:
- size 2,232,398 bytes
- MD5 `7f14a2b793f0ee5bb03aadb0131768db`
- SHA-256 `ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`
- ZIP integrity PASS

Primary gold:
`data/all_evaluations.csv`
SHA-256:
`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

Counts:
- 115 sources
- 345 summaries
- 115/model for GPT-4, LLAMA-2, ALPACA
- 3 outputs/source
- no duplicate source+generation records

Primary human fields:
Population, Intervention, Comparator, Outcome, Results

Source cluster:
`SHA256(exact Abstract)`
115 clusters.

Derived manifests:
- source-cluster manifest SHA-256:
  `a5b26ad1bac4a80e6b158c251557383835e7c43772e25b084d4a4a2bf49fc831`
- 345-record gold manifest SHA-256:
  `693f15c7eaaa6a4687cff04444a4096a076e71600bf240adcf1e5defafe534a5`

Physical semantics:
- 0 = N/A for relevant PICO element fields
- half-step PICO values = aggregated double-annotation values
- Results aggregates 1–5 evidence-inference spans
- Avg. PICO-R is derived, not hard gold
- holistic score not hard-mapped yet

Rationale defects:
- rest_270_annotated_rationales.csv has 240, not 270, rows
- 80 single-annotated source abstracts + 25 double-annotated = 105 sources
- 10 sources / 30 summaries lack released PICO rationale rows
- 15 released PICO rationale candidate texts remain corrupted/mismatched relative to canonical all_evaluations candidate text
- primary numeric gold remains complete 345/345

Evidence inference:
- 645 rationale rows
- all 345 summaries covered
- 1–5 result spans/summary

Contradictions:
diagnostic only.

pico_rationales.csv == llm_pico_rationales.csv byte-identical;
LLM rationales diagnostic only.

Current status:
`FACTPICO PRIMARY GOLD PHYSICAL FREEZE = PASS`

Rationale layer:
`PARTIAL / NON-BLOCKING`

No V2.4 prediction.
No H1 scoring.
No runtime modification.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`FACTPICO HARD-GOLD ELIGIBILITY + H1 CONTRACT V4 FREEZE`

Stop until user says:
`أكمل`


## 2026-10-04 — FactPICO hard-gold eligibility + H1 Contract V4 frozen for focused review

Contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_HARD_GOLD_CONTRACT_V4.md`

Commit:
`d0891669fe21949439ee3d57f1e3e0a4c3659c70`

Focused review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_V4_FOCUSED_REVIEW_PACKET.txt`

Packet commit:
`d737db5d927eea17caa6c6cdbcbccfea840d0915`

Readiness update:
`86b123008baf1b389de0e0a7bcae3fb575725453`

Master continuity update:
`5118523bbe825da7cc8f216623fb5aebc8676aff`

Quality delta:
`IMPROVED / REVIEW PENDING`

Proposal:
- prediction universe 345 / 115 sources
- N/A-source diagnostic 9 / 3 sources
- hard pool 336 / 112 sources
- SAFE_STRICT_CONTROL 34 / 33 sources
- ERROR_STRICT 172 / 91 sources
- INTERMEDIATE 130 / 79 sources

SAFE_STRICT_CONTROL:
- P/I/C/O all 4
- Results 4
- no identified added-information span
- no unresolved added-info identity source
- non-N/A source

Safe-control model skew:
- ALPACA 33
- GPT-4 1
- LLAMA-2 0

This is explicitly limited safe-control evidence, not broad transformation utility.

ERROR_STRICT:
- non-double PICO <=2
- double-PICO aggregate <=1.5
- OR Results <=2

Added Information correctness remains diagnostic only because FactPICO permits externally factual explanations while V2.4 is source-bounded.

Provisional eligibility manifest:
`FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V4_PROPOSAL.csv`
345 rows
SHA-256:
`72ece44c2d23b8c6ce667f5f1ff0856fb28900a412a0b14ed192ce329b8a9d91`

Proposed gates:
- ERROR_STRICT PASS_CANDIDATE = 0
- ERROR_STRICT REJECT >=75% pair-micro + source-macro
- SAFE_STRICT_CONTROL PASS >=75% pair-micro + source-macro

Focused independent review only on:
1. N/A policy
2. double-PICO <=1.5 rule
3. Results <=2 rule
4. safe-control/no-added-info rule
5. safe-control size/model skew
6. 75% thresholds

No V2.4 prediction.
No H1 scoring.
No adapter implementation.
No runtime change.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`USER-MEDIATED FOCUSED INDEPENDENT REVIEW OF FACTPICO H1 CONTRACT V4`

Stop until user returns the complete focused review.


## 2026-10-04 — FactPICO H1 Contract V5 frozen after focused review

Focused review decision:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_V4_FOCUSED_REVIEW_DECISION_V1.md`

Decision commit:
`d6804d096b648e259f3cd37b943f1a522d0e03c9`

Final contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_HARD_GOLD_CONTRACT_V5.md`

Contract commit:
`26235ace57b68b1e93f78728c885d33c1806c24e`

Manifest metadata:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5_METADATA.md`

Manifest metadata commit:
`5852485cda8f4b75df5f573391b5dd3cff34da81`

Readiness update:
`7576fb11ee1fff86b0591f9571139b3f4386234a`

Master continuity update:
`ec3c7a5b65cc7dea89bbab09067c58030d92c1d6`

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Final V5 class counts:
- SAFE_STRICT_CONTROL 34 / 33 sources
- ERROR_STRICT 149 / 83 sources
- INTERMEDIATE 153 / 84 sources represented
- N_A_SOURCE_DIAGNOSTIC 9 / 3 sources

Critical V4 -> V5 change:
`Results <=2`
is removed as a hard-error trigger.

Reason:
released Results is a summary-level aggregate over multiple finding-level judgments and raw per-finding numeric human scores are not released.

Results=4 remains a strict positive-control condition because a bounded 1–4 arithmetic average of 4 implies all contributing ratings are 4.

ERROR_STRICT now PICO-only:
- non-double PICO any applicable <=2
- double-PICO aggregate any applicable <=1.5
- N/A sources excluded

Added Information safe-control proof:
FactPICO evaluates all generated summaries for Added Information by highlighting spans.
Safe control accepts “no highlighted addition” only if:
- canonical record identity exact
- no exact span row
- source cluster not among 15 unresolved Added Information identity sources

Safe control model skew:
33 ALPACA / 1 GPT-4 / 0 LLAMA-2.
Hard but limited anti-degeneracy gate only.

Final eligibility manifest SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Safety:
- 149 error records
- 83 error-exposed sources
- any PASS_CANDIDATE = FAIL
- zero-event 95% source upper bound ≈3.54496%

Utility:
- ERROR REJECT >=75% pair-micro + source-macro
- SAFE PASS >=75% pair-micro + source-macro

Current authorization:
`FACTPICO H1 ADAPTER + INPUT/GOLD MANIFEST IMPLEMENTATION FREEZE`

Still forbidden:
- V2.4 FactPICO prediction
- H1 scoring
- runtime changes
- threshold changes
- original custom Gate C opening
- human recruitment
- Arabic work

Stop until user says:
`أكمل`


## 2026-10-04 — Landscape reset + FactPICO H1 adapter implementation freeze

Landscape reset:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/SCIENTIFIC_VERIFICATION_LANDSCAPE_RESET_V1.md`

Commit:
`f723cb718dc7451c2b484df43cb13a34e3603348`

Strategic conclusion:
`MANY STRONG RESOURCES EXIST`

Actual bottleneck:
`CONSTRUCT MATCHING + EVALUATION INTEGRITY`

New permanent rule:
`CONSTRUCT-MODULAR EXTERNAL VALIDATION`

Use the strongest benchmark/system per function rather than force one dataset to prove the whole ACAD_PASS pipeline.

Fresh modern resources recorded for later audit:
- revision/preservation: ACL 2025 scientific revision evaluation, ParaRev, XtraGPT, Mr Dre
- long scientific factuality: LongSciVerify, FENICE, ACL 2026 long-document stress testing, LLM-Oasis
- claim/evidence: SciVer, CLAIM-BENCH, SciClaimEval, SciTab/Table-Text Alignment, ClimateViz, Matter-of-Fact
- citation verification: SciCiteVal, CiteAudit, SciTrue
- biomedical quality: FactPICO, RoBBR, BioPulse-QA, ReFACT
- application comparators: Scite, Elicit, Paperpal, SciSpace, IPPOLIS Write

Future H2/H3 candidate selection is reopened before execution.
Do not assume older SciFact/QASem choices remain primary without fresh comparison.

FactPICO current H1 role remains:
`source-bounded critical RCT-element fidelity/preservation`

Implementation freeze:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_H1_ADAPTER_IMPLEMENTATION_FREEZE_V1.md`

Commit:
`ee41d5908c5f703aa6738c4a6a3078e69f0e0f25`

Adapter:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/factpico_h1_adapter_v5.py`

Adapter commit:
`c36aef499fe28c83b80f1d7a9f296deefa309d2d`

Adapter SHA-256:
`ab128309261eeffdb734464f2a2fef52cef4ce37bdb3b9654317d6b5bba0b7e1`

Build manifest:
`FACTPICO_H1_V5_BUILD_MANIFEST.json`

Build-manifest commit:
`8450003be24db1b101cb7a8be663431a934dbd76`

Frozen local/private artifact hashes:
- prediction input:
  `ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`
- separate gold:
  `6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`
- V5 eligibility:
  `d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`
- build manifest:
  `67bfbd4302f66d2248009c8a6fe9cef658a6f202d278450b73e942c68cb6f16b`

Adapter validation:
- 345 records
- 115 sources
- 115/model
- 25 double-PICO sources
- 3 N/A sources
- 216 exact Added Information source/candidate pairs
- 15 unresolved auxiliary Added Information source clusters
- all V5 class/source/model counts reproduced exactly
- no duplicate record IDs
- no gold fields in prediction input
- prediction/gold ID sets exact match
- eligibility hash exact reproduction

Determinism:
two sequential builds in separate directories produced identical output hashes.

Tooling negative evidence:
first Python invocation emitted unrelated artifact_tool spreadsheet-runtime warmup error.
Adapter itself returned code 0.
Second build reproduced all hashes.
Classify as environment/tooling only.

Current readiness:
FactPICO adapter/input/gold implementation = PASS/FROZEN.
V2.4 prediction = NOT RUN.
H1 performance = NOT YET MEASURED.

Exact next checkpoint:
`H1 FACTPICO PRE-PREDICTION INTEGRITY GATE`

Still forbidden:
- V2.4 FactPICO prediction
- H1 scoring
- runtime changes
- threshold changes
- custom Gate C opening
- human recruitment
- Arabic work

Stop until user says:
`أكمل`


## 2026-10-05 — Strategic landscape review incorporated; FactPICO blocked before prediction by scalability preflight

Higher-model review decision:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/STRATEGIC_LANDSCAPE_HIGHER_MODEL_REVIEW_DECISION_V1.md`

Commit:
`a1a9975797a6e3879ed8174c82e4ffbacd4dea7e`

Final verdict:
`B. PROCEED WITH MAJOR STRATEGIC MODIFICATIONS`

Permanent strategy:
`CONSTRUCT-MODULAR EXTERNAL VALIDATION`

Important accepted reviewer points:
- candidate support != required-information preservation
- isolated capability pass != end-to-end revision safety
- expert gold is construct-specific
- architecture specifications require implementation/generalization evidence
- novelty cannot be mere integration of familiar components

H1 split:
- H1-A support/factuality
- H1-B required-information preservation
- H1-C revision usefulness

FactPICO remains only:
`HARD SUBGATE FOR SOURCE-BOUNDED CRITICAL RCT/PICO FIDELITY`

Capability/claim map:
`ACAD_PASS_CAPABILITY_CLAIM_MAP_V1.md`
commit:
`bba139f93af7b5b0be95ce6de1dde593cf77ffc6`

Future resource map:
- InfoLossQA -> omission/information loss
- ParaReval/ParaRev -> revision usefulness
- SciFact/SciVer -> claim support
- QASemConsistency + NLI4CT -> local relations / clinical numeric-comparison reasoning
- citation integrity remains separate
- META remains independent

FactPICO Added Information decision:
`FACTPICO_ADDED_INFORMATION_COMPLETENESS_DECISION_V1.md`
commit:
`99372a2e67594f17eaf67ddf5b2a00a84ea9c189`

Decision:
`PASS_WITH_NARROW_CLAIM`

Only allowed negative-event interpretation:
`NO_HIGHLIGHTED_ADDED_INFORMATION_SPAN_IN_THE_RELEASE`

Readiness supersession:
`PRE_GATE_C_READINESS_SUPERSESSION_INDEX_V1.md`
commit:
`8ef29c7c00d46ade02f6b1c358bba9a58d879532`

FactPICO pre-prediction integrity gate:
`FACTPICO_H1_PRE_PREDICTION_INTEGRITY_GATE_V1.md`
commit:
`160a823c4712815c364a30b9bcce42c4c9d03d93`

Readiness update:
`e4e2feb4d82cf10a0e584a66d93d7e9eaa9c962a`

Master continuity update:
`2c940d0ec2aec322e9ad7c306e9c997683374fac`

Integrity PASS:
- FactPICO role/claim frozen
- Added Information interpretation frozen
- readiness authority unified
- artifact hashes
- input/gold isolation
- no gold leakage
- deterministic adapter
- runtime identity unchanged

Canonical frozen pipeline:
run `37150864483`
trigger commit `c0193aa3f578cc32b454a031ead73ff7e56c8918`
artifact SHA-256 `74f765f614b616da2eb101c30d669de0c0931b304a377944be2a4039fe5a844c`

Git compare to gate-time HEAD:
`0 changes to frozen runtime components`

NEW BLOCKER:
`FACTORIAL ALIGNER SCALABILITY`

Frozen B1.1 aligner:
`best_one_to_one`
enumerates:
`itertools.permutations(candidate, len(source))`

Unequal >1 assertion counts also use:
`n=min(source,candidate)`
followed by permutation search.

Complexity:
- n=6: 720
- n=8: 40,320
- n=10: 3,628,800
- n=12: 479,001,600
- n=15: 1,307,674,368,000
- n=20: 2,432,902,008,176,640,000

B2 was a small mechanics/development set.
Full-document scalability was NOT previously measured.

Therefore:
`NOT_READY_FOR_FACTPICO_PREDICTION`

Classification:
`IMPLEMENTATION SCALABILITY / EXECUTION VALIDITY BLOCKER`

Not a FactPICO result.
Not a semantic failure.
No benchmark record has been predicted.

Do NOT silently replace matcher under V2.4 identity.

Exact next checkpoint:
`V2.4 SYNTHETIC SCALABILITY PREFLIGHT + EXECUTION-POLICY DECISION`

Allowed:
- synthetic/non-FactPICO stress tests
- static complexity audit
- execution wrapper/failure policy design
- decide frozen V2.4 timeout/INVALID vs version bump

Forbidden:
- FactPICO prediction
- H1 scoring
- frozen runtime modification without version bump
- threshold tuning
- custom Gate C opening
- Arabic work

Stop until user says:
`أكمل`


## 2026-10-05 — Full higher-model report reconciled; synthetic scalability blocker confirmed

User supplied:
- ACAD_PASS_LANDSCAPE_STRATEGIC_REVIEW_2026-10-04.md
- ACAD_PASS_REVIEWER_HANDOFF.md

Current file-need decision:
`NO ADDITIONAL USER FILE REQUIRED NOW`

Only request original historical attachments later if one exact historical/provenance claim cannot be resolved from repository + reviewer handoff.

Full reconciliation:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FULL_STRATEGIC_LANDSCAPE_RECONCILIATION_V1.md`

Commit:
`b724f618eb8067e44edd7ac3ae823b52f292ae01`

Added roadmap details from full report:
- 3-level evidence hierarchy
- later PRESERVE/SIMPLIFY/CORRECT task contract
- native-document authority
- context/obligation separation
- coverage ledger
- dependency-aware repair
- scoped delivery certificate
- Docling/GROBID/academic-refchecker/MiniCheck/W3C provenance integration candidates
- explicit code/license/scorer warnings
- 10 new failure modes
- stronger simple-baseline comparison requirement

No FactPICO V5 rule changed.

Synthetic scalability preflight:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_4_SYNTHETIC_SCALABILITY_PREFLIGHT_V1.md`

Commit:
`03609245bab8d22e4c164708fd8ed2d9ded36803`

Frozen best_one_to_one synthetic measurements:
- n3 0.00140s
- n4 0.00410s
- n5 0.02483s
- n6 0.17669s
- n7 1.41590s
- n8 12.94802s

n8 measured rate:
~3114 permutations/sec.

Optimistic extrapolation:
- n9 ~1.94 min
- n10 ~19.42 min
- n11 ~3.56 h
- n12 ~42.73 h
- n15 ~13.31 years

No FactPICO data were used.

Preflight verdict:
`FAIL_SCALABILITY`

Root:
frozen B1.1 enumerates permutations factorially.

Mathematical note:
global objective is pairwise-additive lexicographic assignment.
Factorial enumeration is not intrinsically necessary.

But replacing matcher changes frozen runtime identity.

Focused higher-model packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_4_SCALABILITY_HIGHER_MODEL_REVIEW_PACKET.txt`

Commit:
`481c45c8a77f2446f9f2759c46c620c55054c1f2`

Readiness update:
`aa43910aa5d97528521cce253397404dcab827fe`

Master continuity update:
`e45f902a7cf30831096573a508c849014b6c1d0a`

Implementation-agent recommendation:
`PREFER VERSION-BUMP SCALABLE MATCHER, SUBJECT TO INDEPENDENT REVIEW`

FactPICO exposure:
`NONE`

FactPICO prediction:
`NOT RUN`

Exact next checkpoint:
`FOCUSED HIGHER-MODEL DECISION ON V2.4 SCALABILITY BLOCKER`

Stop until user returns focused review.


## 2026-10-05 — AT0-EN V2.5 scalable matcher frozen; pre-prediction review next

Higher-model verdict:
`B. VERSION_BUMP_BEFORE_FACTPICO`

Canonical V2.4:
`NOT_RUN — PRE-PREDICTION SCALABILITY BLOCKER`

Do not call V2.4 a FactPICO failure.

V2.5 specification:
`phase2/academic_transform/at0_en/v2_5/AT0_EN_V2_5_EXACT_SCALABLE_MATCHER_SPEC_V1.md`

Runtime freeze:
`phase2/academic_transform/at0_en/v2_5/AT0_EN_V2_5_RUNTIME_FREEZE_V1.md`

Freeze commit:
`d8282a13d9ba215117f1dd52c80088ccdb972a15`

FactPICO execution identity amendment:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V5_EXECUTION_IDENTITY_AMENDMENT_V1.md`

Commit:
`2301367d918501dbbe875ebf8bf9c4eb0e6e35ec`

Regression run:
`37279532576`

Run head:
`05e200461c1067c120e73acf4a6055383eb350b2`

Conclusion:
`SUCCESS`

Artifact:
`11331840770`

Artifact digest:
`sha256:ec012324b265b5e6be5e1aff5f5dd670547692fc9f8bb6a3f58c993ccbb2cba1`

Regression report:
`PASS`

Algorithm:
`HUNGARIAN_EXACT_INTEGER_LEXICOGRAPHIC_V1`

Numeric:
`EXACT_RATIONAL_FORMULA_V1`

B1/B2:
- B1 exact diff 0/12
- B2 exact diff 0 across GG/GE/EG/EE
- GG 12/12
- GE 11/12; safe4/5; unsafe0
- EG 11/12; safe4/5; unsafe0
- EE 12/12; safe5/5; unsafe0/6; REVIEW1/1

Synthetic equivalence:
`205 cases / 0 differences`

Scalability:
- n9 ~0.032s
- n10 ~0.039s
- n12 ~0.056s
- n16 ~0.099s
- n32 ~0.395s
- n64 ~1.58s
- n128 ~6.31–6.73s
- peak n128 ~5.35MB

Guardrails:
timeout/crash/valid-child/empty/out-of-envelope PASS.
Retries 0.

Frozen operational envelope:
- max assertions per side 128
- 60 seconds per record
- strictly sequential
- runtime/out-of-envelope failures -> INVALID_VERIFICATION

Frozen hashes:
- spec `8fe6203b266f86e2e147cf65b4e55d15b8dc25b344b466ac5d0f75ca461f888f`
- aligner `ac36409cd32c9a759a3e962ee6a86aa30d0a52299f2a19ccc8206d7b54e248ea`
- runner `ad2e996f0e76e8d6b80285d7059b072c53914f32d9d48fbf9af8f8076282b807`
- regression test `6633db047be337df27d1fad61eb8b33a473a6d69c60b73e35ec2611b1552a47a`
- regression report `2b0861f904448663b1eaff675ed79034bdccdb4c6ccee3ba08e7986fa5eb4b20`

Numeric caveat:
exact-rational formula is a named V2.5 numeric identity change.
No difference observed in canonical development or 205 brute-force oracle cases.
Universal bitwise float equivalence is NOT claimed.

FactPICO:
- no text through runtime
- no assertion count profiling
- no timing
- no prediction
- no scoring

FactPICO V5 scientific gold/thresholds/input/gold artifacts unchanged.

Pre-prediction higher-model packet:
`phase2/academic_transform/at0_en/v2_5/V2_5_PRE_PREDICTION_HIGHER_MODEL_REVIEW_PACKET.txt`

Packet commit:
`274d9bbd107779618a894445d83e1ec050d84973`

Readiness update:
`3b7c89c6593c57462cf4e2f8376c32313c15ab6b`

Master continuity update:
`c90aa9db4e35907115a3b21f2f81b0074db19181`

Quality delta:
`MAJOR IMPROVEMENT — FACTORIAL BLOCKER REMOVED WITH ZERO OBSERVED REGRESSION`

Current checkpoint:
`V2.5 PRE-PREDICTION HIGHER-MODEL REVIEW`

STOP.
No FactPICO prediction until review/authorization returned.


## 2026-10-05 — V2.5 implementation-agent pre-review audit

Audit:
`phase2/academic_transform/at0_en/v2_5/V2_5_IMPLEMENTATION_AGENT_PRE_REVIEW_AUDIT_V1.md`

Commit:
`21ece496e825ada155a9d44f11c8146b07391425`

Master continuity update:
`6675996a9351770d442c48077c963a9207231a70`

Verdict:
`PASS_FOR_HIGHER_MODEL_PRE_PREDICTION_REVIEW`

Quality delta:
`IMPROVED`

No newly identified regression.

Verified:
- frozen V2.5 regression PASS
- B1/B2 exact differences 0
- 205 synthetic oracle equivalence cases
- n=128 scalability PASS
- timeout/crash/out-of-envelope -> INVALID
- sequential / zero retries
- FactPICO execution amendment consistent
- V5 scientific contract/hashes unchanged
- FactPICO NOT_RUN

Remaining gate:
`V2.5 PRE-PREDICTION HIGHER-MODEL REVIEW`

No FactPICO prediction/scoring/gold join authorized.

Stop until independent higher-model pre-prediction decision is returned.


## 2026-10-05 — V2.5 essential pre-execution closure complete

Higher-model verdict:
`B. READY_WITH_ESSENTIAL_PRE_EXECUTION_CHANGES`

Closure completed.

Final successful run:
`37289569561`

Head:
`29e3abe5ccb708cb88d94ae00630eaa0fdc2b123`

Artifact:
`11335647986`

Artifact ZIP SHA-256:
`61d82aa30de89e84aa5bc0433bdfa528259269c0b3630648df5c0d4c95573b63`

Regression report SHA-256:
`e0ccf3dd45a7e20f9df7b4086779b2d2846d539c67564ecee2e6a8720b419c87`

Closed:
- exact objective checks 205
- float-vs-exact mapping discrepancies 0
- priority conflict PASS
- partial tie PASS
- near tie PASS
- full tie policy PASS
- fresh-process reproducibility PASS
- mixed-batch accounting PASS
- overwrite refusal PASS
- one-shot guard PASS
- 128 full tie + near-envelope unequal PASS

Preserved negative:
`37289060156` failed old 10s synthetic full-tie criterion.

Resolution:
synthetic criterion refrozen to 30s after synthetic-only evidence;
production timeout unchanged at 60s/record.

Final repeated full-tie n128:
7.3144 / 7.0391 / 7.0154 s.

FactPICO:
`NOT_RUN`

Current state:
`READY_FOR_FINAL_HIGHER_MODEL_PRE_PREDICTION_RE_REVIEW`

Packet:
`phase2/academic_transform/at0_en/v2_5/V2_5_FINAL_PRE_PREDICTION_REVIEW_PACKET.txt`

No FactPICO prediction/scoring/gold join authorized.

Stop until higher-model final re-review is returned.


## 2026-10-05 — Final V2.5 execution-control gaps closed

Higher-model verdict:
`B. READY_WITH_FINAL_EXECUTION_CONTROL_CHANGE`

Required final gaps:
- priority-conflict fixture
- actual durable attempt ledger

Priority fixture:
- changed second source/candidate predicates to REDUCE
- selected mapping now wins hard-owner/owner priorities while losing semantic score
- exact oracle and matcher still choose selected mapping
- PASS
- matcher unchanged

Final regression:
run `37312305371`
head `659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`
artifact `11345959688`
artifact SHA-256 `f3510bd4cacdb40a70d6b37d6d9f6fac24a9d77285462723f1e0738eb374a701`

Final hashes:
- matcher `ac36409cd32c9a759a3e962ee6a86aa30d0a52299f2a19ccc8206d7b54e248ea`
- batch runner `7a3383e6108272b641e8f4bcda553a5d97aad7a873616341c3493d425fec6def`
- one-shot guard `574d0c0a1222435069eee48534e2d4e04ca72f6d538bf3c5c334a683304bb6d2`
- one-shot spec `a615988ff14b64307576b367da593175c742f8c9a6e7928fc195f9811c21afed`
- regression test `81fb84f28668804b95844adc32a3d7743061e89aa69bec2a2c89129b57b4d471`
- regression report `b2248f62724e3d9a7a30f34bb42ff97e287bc608e9852e78bf13fcee63fc3a2a`

Durable ledger:
GitHub repo contents
branch `factpico-v25-one-shot-ledger`

Authorization:
`FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

Real key:
`claims/real/FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001/ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82/ATTEMPT_CLAIM.json`

Synthetic evidence:
key `claims/synthetic/SYN-DURABLE-LEDGER-001/ATTEMPT_CLAIM.json`
creation commit `f687cedcb82c543d8d21552db79a2d25a93f7a4e`
later blob `cf03473f29ab3ce3452d133302ccc27672c1278f`

Synthetic claim survived initial-launch interruption.
Fresh independent launch observed claim and refused inference.

Current ledger tree:
- real claim exists FALSE
- synthetic claim exists TRUE

Therefore real FactPICO attempt:
`UNCONSUMED`

Closure:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_5_FINAL_EXECUTION_CONTROL_CLOSURE_V1.md`

Execution identity:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V5_EXECUTION_IDENTITY_AMENDMENT_V3.md`

Final authorization packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_5_FINAL_EXECUTION_AUTHORIZATION_REVIEW_PACKET.txt`

Quality:
`IMPROVED`

Worsened:
`NONE IDENTIFIED`

FactPICO:
`NOT_RUN`

Current stop:
`FINAL EXECUTION AUTHORIZATION REVIEW`

Do not run FactPICO until independent authorization is returned.


## 2026-10-05 — Final V2.5 FactPICO execution authorization received

Independent higher-model verdict:
`A. AUTHORIZE_ONE_PROSPECTIVE_FACTPICO_PREDICTION_RUN`

Decision record:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_5_FINAL_EXECUTION_AUTHORIZATION_DECISION_V1.md`

Decision commit:
`af6c877295684c2028fe5e72948723c2f31d899c`

Confirmed:
- priority-conflict fixture CLOSED
- durable attempt ledger CLOSED
- no concrete unresolved execution defect

Maximum authorization:
`ONE PROSPECTIVE AT0-EN V2.5 FACTPICO PREDICTION RUN + IMMUTABLE PREDICTION ARTIFACT FREEZE ONLY`

Execution checkout:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

Authorization ID:
`FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

Input SHA:
`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Current attempt:
`UNCONSUMED`

Current FactPICO state:
- prediction NOT_RUN
- gold join NOT_RUN
- scoring NOT_RUN
- profiling NOT_RUN

Important execution safety:
do NOT create the real remote claim until the exact frozen private prediction-input bytes are available and their SHA/count/order are verified. Claim creation consumes the attempt even if inference never starts.

Current exact next checkpoint:
`AUTHORIZED ONE-SHOT EXECUTION PREFLIGHT`

Still forbidden:
gold join, scoring, rerun, adaptive retry, runtime/matcher modification, threshold/gold changes, pre-run FactPICO profiling, redesign, custom Gate C, Arabic work.


## 2026-10-05 — Authorized FactPICO preflight complete

Successful GitHub Actions preflight:
- run `37317413838`
- head `fa1ffb4f37e44dec04d29061ba95c5091ee3a46a`
- artifact `11348064811`
- digest `sha256:c3786ba8c6516d959e0f22f075e289868b9765b7aa72c49fe5607a547b4e69e4`

Verified on immutable checkout `659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`:
- matcher hash PASS
- batch runner hash PASS
- one-shot guard hash PASS
- public FactPICO ZIP hash PASS
- 345 input rebuild PASS
- frozen input SHA PASS
- gold SHA PASS
- eligibility SHA PASS
- unique IDs/order/schema PASS
- no claim created
- no inference started

New preserved provenance finding:
- documented adapter SHA `ab128309...` does not match committed bytes;
- actual committed adapter SHA is `3b0698772630a17d6d05fdf7197f5faa79b22212332ae785b069318bda4cd5b0`;
- Git compare from `c36aef...` to `659b61...` shows the adapter file was not modified;
- classification: historical documented-hash mismatch, not post-freeze mutation.

Reconciliation:
`FACTPICO_ADAPTER_COMMITTED_IDENTITY_RECONCILIATION_V1.md`
commit `c22f027fb879a8092fa129f45c238d07f9a25ffd`.

Real attempt:
`UNCONSUMED`

Prediction/gold join/scoring:
`NOT_RUN`

Next:
`VERIFY REAL CLAIM ABSENT -> CREATE ATOMIC REMOTE CLAIM -> ONE AUTHORIZED V2.5 PREDICTION -> FREEZE -> STOP BEFORE GOLD JOIN`


## 2026-10-05 — FactPICO V2.5 one prospective prediction COMPLETE / FROZEN

Authorization:
`A. AUTHORIZE_ONE_PROSPECTIVE_FACTPICO_PREDICTION_RUN`

Execution:
- run `37318062175`
- workflow head `066d606e311136c5020ba800c3872b054c11e6da`
- job `111789731999`
- immutable runtime checkout `659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`
- conclusion `SUCCESS`

Remote claim:
- commit `6387516d84e9ba1109d387dcc4bde715ce2ac16b`
- blob `a1d7bb2df60e55db8f914550858c2accadad1390`
- state `CONSUMED_BEFORE_INFERENCE`
- read-back PASS
- authorization permanently consumed; NO RERUN

Input:
- 345 records
- SHA `ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`
- unique IDs/order PASS

Prediction:
- 345 outputs
- SHA `925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b`
- retry count 0
- state `PREDICTIONS_FROZEN`

Artifact:
- GitHub artifact `11348646367`
- size 358556 bytes
- digest `sha256:eb68ab179bc17af1105a63ae1ff2f3fc76a4449bffd74a40a76a775319743daa`
- independent downloaded ZIP SHA matches exactly
- private ACAD_PASS Library preservation copy created

Freeze record:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_ONE_PROSPECTIVE_PREDICTION_FREEZE_V1.md`
commit `cdabc233c77cad2dace15233ccbc179ee5fa2dac`

Preserved negative:
- preflight run `37317221936` failed before claim due stale/incorrect historical adapter SHA metadata
- no claim/inference occurred
- reconciliation recorded in `FACTPICO_ADAPTER_COMMITTED_IDENTITY_RECONCILIATION_V1.md`
- corrected preflight run `37317413838` PASS

STOP BOUNDARY:
- gold join NOT_RUN
- scoring NOT_RUN
- eligibility join NOT_RUN
- scientific H1 result NOT YET MEASURED
- no adaptive inspection
- no rerun
- no runtime/matcher change
- no threshold/gold change
- no custom Gate C
- no Arabic work

Quality:
`IMPROVED — ONE AUTHORIZED PREDICTION COMPLETED AND FROZEN`

Current exact checkpoint:
`FACTPICO PREDICTION FROZEN / STOP BEFORE GOLD JOIN`

Next requires separate explicit authorization for gold join/scoring.


## 2026-10-05 — UI-resilient execution rule added

User explicitly requested minimizing recurrence of:
`Our systems are thinking a bit more about this request before responding.`

Permanent operational rule:
- sequential tools only;
- minimize calls when safely possible;
- batch related read-only checks;
- avoid unnecessary polling;
- short checkpoint messages only;
- UI interruption is NOT scientific failure;
- resume from last verified durable state;
- do not repeat completed work after UI interruption;
- never weaken one-shot integrity or auditability merely to reduce calls.

Current state remains:
- authorization GRANTED
- real FactPICO attempt UNCONSUMED
- prediction NOT_RUN
- gold join NOT_RUN
- scoring NOT_RUN

Next:
`VERIFY REAL CLAIM ABSENT -> ATOMIC REMOTE CLAIM -> ONE AUTHORIZED PREDICTION RUN -> FREEZE -> STOP BEFORE GOLD JOIN`


## 2026-10-05 — FactPICO V2.5 one-shot prediction completed and frozen

Canonical freeze:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_PROSPECTIVE_PREDICTION_EXECUTION_FREEZE_V1.md`

Successful run:
`37318062175`

Execution checkout:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

Real claim:
- commit `6387516d84e9ba1109d387dcc4bde715ce2ac16b`
- blob `a1d7bb2df60e55db8f914550858c2accadad1390`
- attempt permanently CONSUMED

Frozen prediction:
- 345/345
- exact ID order PASS
- SHA-256 `925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b`
- retries 0
- INVALID 0

Unscored runtime outcomes:
- PASS_CANDIDATE 0
- REJECT 37
- REVIEW 308
- INVALID_VERIFICATION 0

Frozen artifact:
- ID `11348646367`
- digest `eb68ab179bc17af1105a63ae1ff2f3fc76a4449bffd74a40a76a775319743daa`

STOP BOUNDARY:
- gold join NOT_RUN
- scoring NOT_RUN
- rerun FORBIDDEN
- no adaptation

Current exact checkpoint:
`FACTPICO V2.5 POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`

Do not interpret the 37/308/0/0 distribution as performance metrics until separately authorized gold join/scoring.


## 2026-10-05 — Post-prediction / pre-gold review packet prepared

Packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_POST_PREDICTION_PRE_GOLD_REVIEW_PACKET.txt`

Commit:
`5a72c16de204fc787fbd9fc6e6232033439779a1`

Decision requested next:
- A. AUTHORIZE_ONE_DETERMINISTIC_FACTPICO_GOLD_JOIN_AND_FROZEN_SCORING_RUN
- B. BLOCK_BEFORE_GOLD_JOIN

Current boundary unchanged:
- prediction frozen
- attempt consumed
- gold join NOT_RUN
- scoring NOT_RUN
- rerun/adaptation forbidden

Exact next checkpoint:
`INDEPENDENT POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`


## 2026-10-05 — Progress / maturity scorecard

Scorecard:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_STAGE_PROGRESS_SCORECARD_V1.md`

Commit:
`f056eb2391e57076f7b3159186d3fb9b78887196`

Engineering indicators only:
- prediction-execution checkpoint: 100%
- FactPICO V2.5 validation subphase: 70%
- execution-integrity maturity: 96/100
- scientific-validation completeness: 70/100
- FactPICO-stage quality satisfaction: 90/100
- overall English-track maturity: 78/100
- target excellent/review-ready: >=90/100

Delta since previous major checkpoint:
- completion ≈ +20 percentage points
- execution integrity ≈ +8 points
- scientific-performance delta NOT YET COMPARABLE before gold scoring.

Exact next checkpoint:
`INDEPENDENT POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`


## 2026-10-05 — FactPICO V2.5 scored and frozen

Gold/scoring run:
`37325138336`

Artifact:
`11351451888`

Artifact digest:
`105534207a4566c38d76174e9cd263244b87e37358b6007c76502bc250d67e77`

Scorer SHA:
`00df8950ffb3d0ee48925c98ad976e1a940e68069a937396d4b28fdd5923d7fb`

Config SHA:
`bf2c47d0d2b7121c64168d62fc8f51669c22579f5827b6d3e4d0a4f20d304322`

Exact join:
345/345 PASS

Frozen gates:
- safety PASS: 0 unsafe PASS across 149 ERROR_STRICT / 83 sources
- negative utility FAIL: micro 10.7383%, macro 9.4378%, threshold 75%
- positive anti-degeneracy FAIL: micro 0%, macro 0%, threshold 75%

Mechanical decision:
`H1_FULL_PASS_NOT_ACHIEVED`

Current progress:
- FactPICO completion 95%
- execution integrity 98/100
- scientific-validation completeness 95/100
- process rigor satisfaction 98/100
- benchmark-outcome satisfaction 30/100
- overall English-track maturity 74/100

Next packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_POST_SCORING_INTERPRETATION_REVIEW_PACKET.txt`

Packet commit:
`42af380148c790162572ba335a2a817a85d1565a`

Current exact checkpoint:
`FACTPICO V2.5 POST-SCORING INDEPENDENT INTERPRETATION / NEXT-DECISION REVIEW`

No rerun, rescoring, adaptation, or repair is authorized yet.


Rerun-prevention closure:
- one-shot scoring workflow removed after successful immutable freeze
- removal commit: `1fa410c417f4e718f7213fe431ad04534ae90940`
- purpose: prevent accidental second gold/scoring execution


## 2026-10-05 — Failure analysis and V2.6 repair design frozen

Verdict authorizing this phase:
`A. AUTHORIZE_BOUNDED_FACTPICO_FAILURE_ANALYSIS_AND_REPAIR_DESIGN`

Failure analysis:
`FACTPICO_V25_FAILURE_ANALYSIS_REPORT_V1.md`
commit `3a96a19105f2c732c8ba62d2daef4a1957718b6d`

Repair design:
`AT0_EN_V26_DEV_REPAIR_DESIGN_V1.md`
commit `f7b329baa42225353e20895fc15f4a1ef8e50593`

Key result:
- all 345 records contain assertion uncertainty
- 308 REVIEW are directly caused by uncertainty gating
- 37 REJECT have critical mismatch overriding uncertainty
- zero relation alignments
- 339/345 non-1:1 assertion groups
- median source:candidate assertion ratio 4.83

Most defensible bottleneck:
`representation/extraction uncertainty + unequal-count grouping amplification`

Do NOT fix the result by relaxing REVIEW/PASS policy.

No repair implemented yet.

Progress:
- FactPICO V2.5 experiment 100%
- current failure-analysis phase 100%
- repair-design phase 100%
- scientific performance improvement 0% (runtime unchanged)
- diagnostic localization 92/100
- process rigor 99/100
- repair-direction confidence 88/100
- benchmark outcome satisfaction 30/100
- overall English-track maturity 74/100

Next:
`FAILURE_ANALYSIS_AND_REPAIR_DESIGN_REVIEW`

Packet:
`FACTPICO_V25_FAILURE_ANALYSIS_AND_REPAIR_DESIGN_REVIEW_PACKET.txt`
commit `731160384e89a6d28c2b892b8b05697fc6d4e2f5`
