# ACAD_PASS SYSTEM EVOLUTION LEDGER

**Status:** CANONICAL LIVING HISTORY  
**Project:** ACAD_PASS — Academic Document Intelligence & Transformation Platform  
**Repository:** `abdullah-s-mahmood/sweet-runtime-parity`  
**Primary active branch at creation:** `phase2-arabic-eval`  
**Initial ledger date:** 2026-10-01

---

## 0. Purpose

This file is the long-term chronological and scientific record of ACAD_PASS.

It exists for two equally important purposes:

1. **System engineering and re-baselining**
   - preserve every material success, failure, metric, architectural decision, root cause, and repair;
   - make it possible to revisit an earlier assumption when stronger models, methods, datasets, or tooling become available;
   - prevent repeated mistakes or accidental loss of negative evidence;
   - distinguish frozen evidence from later redesigns.

2. **Future academic conversion**
   - preserve the experimental history needed to later assess whether ACAD_PASS can support one or more peer-reviewed papers, a doctoral dissertation, or another formal research program;
   - retain failed hypotheses, negative results, design pivots, preregistered gates, reproducibility evidence, and methodological corrections;
   - make future research claims traceable to actual evidence rather than reconstructed memory.

This ledger is not a marketing document. It must preserve negative evidence with the same priority as positive evidence.

---

## 1. Permanent maintenance rule

Update this ledger after every **meaningful checkpoint**, including:

- a successful or failed scientific workflow;
- a major infrastructure failure that changes reproducibility understanding;
- a frozen dataset/model/artifact/hash;
- a new quantitative result;
- a root-cause diagnosis;
- a change in architecture, model, proposer, evaluator, legalizer, or policy;
- an independent review;
- a gate decision;
- a re-baseline decision;
- a higher-model review;
- a discovery that an earlier conclusion was invalid, incomplete, or superseded.

Do **not** rewrite historical entries merely because later evidence changes interpretation.

When later evidence supersedes an earlier result:

1. preserve the original entry;
2. mark it `SUPERSEDED`, `INVALIDATED`, or `REINTERPRETED`;
3. state the new evidence;
4. link the new decision/version.

Every material entry should record, when available:

- date;
- stage/version;
- objective;
- why the path was chosen;
- population/data;
- method;
- success/failure status;
- quantitative metrics;
- root cause for failures;
- repairability;
- scientific interpretation;
- engineering consequence;
- next decision;
- evidence/commit/run/artifact/hash.

If an exact percentage is not available, write **NOT QUANTIFIED**. Never invent a percentage.

---

## 2. Project objective and architectural vision

ACAD_PASS evolved from an Arabic correction/evaluation effort into a broader bilingual academic-document platform.

Current long-term product vision:

`Transform → Protect → Verify → Drift → Repair/Escalate → Review → Preserve → Deliver`

Equivalent system concerns include:

- understanding structured academic documents;
- Arabic/English/mixed-language transformation;
- source-preserving correction;
- protected invariants for numbers, units, citations, equations, technical tokens, URLs, and document structure;
- independent verification;
- uncertainty and risk detection;
- repair or escalation;
- document-format preservation;
- final delivery.

Permanent product capabilities also include:

- direct pasted-text/editor input;
- whole-text, paragraph, and adaptive processing;
- DOCX/Word preservation;
- long-term DOCX→LaTeX conversion;
- preservation/validation of structure, mathematics, citations, tables, figures, references, and Arabic/English mixed content.

The objective is the **strongest scientifically defensible system**, not preservation of any current architecture.

---

## 3. Historical chronology

### 3.1 Early Arabic evaluation / NoPnx baseline

**Status:** HISTORICAL DEVELOPMENT EVIDENCE

Known frozen evidence:

- NoPnx ZIP: **500,903,197 bytes**
- NoPnx binary: **539,450,353 bytes**
- SHA-256: matched
- model layers: **12**
- labels: **315**

Arabic development evaluation:

- targets: **150**
- passages: **41**
- RECOVERED: **29 / 150 = 19.33%**
- PRESERVED_ERROR: **65 / 150 = 43.33%**
- CHANGED_OTHER: **56 / 150 = 37.33%**

Interpretation:

The result was not sufficient to justify a strong automatic-correction claim. It motivated deeper auditing and a more explicit safety/evidence architecture.

A later audit of **21 sections / 64 experiments** exposed redesign opportunities and construct-validity problems.

**Reason for moving forward:** raw correction activity was not equivalent to safe, complete, scientifically valid correction.

---

### 3.2 Early claimed improvement audit

An earlier comparison suggested:

`88.73% → 96.55%`

This was later determined to be invalid as a causal improvement claim because the populations were not comparable.

Correct same-population GED comparison:

- baseline: **34 / 36 = 94.44%**
- later: **28 / 29 = 96.55%**
- comparable precision change: **+2.1073 percentage points**
- supported retention: **28 / 34 = 82.35%**

**Status:** EARLIER CLAIM INVALIDATED / CONSTRUCT CORRECTED

**Scientific lesson:** cross-population percentages cannot be treated as causal improvement.

This audit triggered the stronger redesign principle:

> correct edit ≠ complete repair ≠ safe scientific transformation.

---

### 3.3 M1 — edit-contract and evidence model

**Status:** CLOSED / DATA_READY

Objective:

Define the unit of correction and evidence rather than treating sentence correction as an opaque pass/fail event.

Core axes introduced:

- necessity;
- local correctness;
- contextual correctness;
- edit-group completeness;
- residual-error relation;
- semantic fidelity;
- scientific fidelity;
- protected invariants;
- surface/document integrity;
- ambiguity/author intent;
- severity.

24-case pilot:

- SUPPORTED_CORRECTION: **8 / 24 = 33.33%**
- SUPPORTED_ALTERNATIVE: **5 / 24 = 20.83%**
- WRONG_CORRECTION: **7 / 24 = 29.17%**
- PARTIAL_CORRECTION: **2 / 24 = 8.33%**
- UNNECESSARY_EDIT: **2 / 24 = 8.33%**

M1-A evidence pool:

- QALB14 TRAIN source/corrected: **19,411**
- QALB14 DEV source/corrected: **1,017**
- reconstructable TRAIN: **18,884**
- reconstructable DEV: **1,003**
- reconstruction failures: **493**
- safe persisted calibration sample: **3,829**
- A7'ta parseable: **463**
- A7'ta bootstrap: **375**
- A7'ta reserve: **88**, kept closed

**Why this route was chosen:** correction needed a reversible, auditable edit transaction rather than a sentence-level opaque decision.

**Classification:** IMPROVED / DATA_READY

---

### 3.4 M2 monolithic frontier verifier

**Status:** CLOSED FAIL

Purpose:

Test whether one general verifier could safely approve/reject correction outcomes.

P0:

- unsafe acceptance: **4.17%**
- safe acceptance coverage: **22.22%**
- review burden: **37.50%**

P1:

- unsafe acceptance: **18.75%**
- safe acceptance coverage: **56.94%**
- review burden: **20.83%**

Change P1 vs P0:

- coverage: **+34.72 pp**
- review burden: **−16.67 pp**
- unsafe acceptance: **+14.58 pp worse**

**Why it failed:** improved coverage came at an unacceptable increase in unsafe acceptance.

**Decision:** close the monolithic verifier path.

**Scientific lesson:** higher automation coverage without independent safety evidence can worsen the system.

No P2 was authorized. Reserved evaluation pools remained closed.

---

### 3.5 M2-R — residual span hunter

**Status:** CLOSED / USEFUL DIAGNOSTIC / FAIL AS STANDALONE SAFETY VERIFIER

ArabiGEE was first considered but rejected as sentence-completeness gold because its annotations were selective rather than exhaustive.

The design switched to QALB complete-gold.

P0:

- CRR: **82.22%**
- GELR: **29.14%**
- CFPR: **60.00%**
- strict residual recall: **63.33%**
- claim precision: **63.47%**

P1:

- CRR: **86.67%**
- GELR: **48.88%**
- CFPR: **33.33%**
- strict residual recall: **76.67%**
- claim precision: **65.50%**

P1 vs P0:

- CRR: **+4.44 pp**
- GELR: **+19.74 pp**
- CFPR: **−26.67 pp improvement**
- strict recall: **+13.33 pp**
- claim precision: **+2.03 pp**

**Why it was retained conceptually:** it produced useful residual-risk evidence.

**Why it was not accepted as the final verifier:** residual evidence did not provide sufficiently strong standalone safety assurance.

**Classification:** IMPROVED SCIENTIFICALLY / PARTIALLY SUPPORTED TECHNICALLY / FAIL AS STANDALONE SAFETY VERIFIER

---

### 3.6 M2-H — heterogeneous verifier architecture

**Status:** MAJOR REDESIGN PATH

Reason for selection:

The evidence from M2 and M2-R suggested that one generic gate was insufficient. The design therefore moved to specialized heterogeneous evidence.

Planned architecture:

1. structured edit candidate generator;
2. deterministic orthographic validator;
3. morphology-aware validator;
4. deterministic word-boundary validator;
5. contextual/semantic ambiguity handling;
6. calibrated risk fusion;
7. independent sentence-completeness decision;
8. REVIEW escalation.

Frozen success gates:

- unsafe-clean ≤ **5%**
- CFPR ≤ **10%**
- CRR ≥ **90%**
- strict recall ≥ **90%**
- mandatory precision ≥ **90%**
- edit localization ≥ **70%**
- protected invariant failures = **0**
- hybrid must improve over M2-R P1 by at least **10 pp CFPR** and **10 pp GELR** on comparable definitions

**Scientific rule:** these gates were not to be weakened after seeing results.

---

### 3.7 Dual-environment architecture

Initial single-environment preflight failed because H1's historical Python/PyTorch/Transformers requirements conflicted with current CAMeL Tools dependencies.

Decision:

Use isolated environments communicating only through serialized artifacts.

H1:

- Python 3.10
- PyTorch 1.12.1
- Transformers 4.30.0

H3/H4:

- Python 3.11+
- current frozen CAMeL Tools

Frozen H1 model revision:

`21286e56ce98a86362db540863f91c083b8970f9`

H1 weight SHA-256:

`9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`

Frozen CAMeL Tools SHA:

`be79ca9fc493f0df795375a7255bafef246a802d`

morphology.db SHA-256:

`195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70`

Preflight v2:

- run `36653526757`
- **SUCCESS**

**Lesson:** environment isolation was necessary for reproducibility; software compatibility failure was not scientific failure.

---

### 3.8 Development split freeze

Reconstructable development population:

- total: **14,017 UIDs**
- M2-R P0 excluded: **120**
- M2-R P1 excluded: **120**
- overlap: **0**
- remaining: **13,777**

Frozen split:

- CALIBRATION: **6,888 / 13,777 = 50.00% approximately**
- INTERNAL_EVALUATION: **5,510 / 13,777 = 39.99% approximately**
- STRESS_DIAGNOSTIC: **1,379 / 13,777 = 10.01% approximately**

Reserved/internal populations remained closed until rules were frozen.

**Reason:** prevent adaptive leakage and preserve later evaluation value.

---

### 3.9 CALIBRATION materialization

Population:

- cases: **6,888**
- changed source/reference: **6,867 = 99.70%**
- unchanged: **21 = 0.30%**

Operation counts:

- Edit: **59,875**
- Add_before: **34,816**
- Split: **3,776**
- Merge: **6,629**
- Delete: **2,427**
- Move: **132**
- Add_after: **12**
- Other: **599**

Artifact ID: `11070819539`

---

### 3.10 H4 construct correction

A critical construct-validity error was identified:

Not every QALB Split/Merge is a pure whitespace boundary correction.

Split:

- total: **3,776**
- pure-space eligible: **2,633 = 69.73%**
- non-pure: **1,143 = 30.27%**

Merge:

- total: **6,629**
- pure-space eligible: **5,505 = 83.04%**
- non-pure: **1,124 = 16.96%**

Combined non-pure adversarial negatives:

- **2,267**

Sentence availability:

- pure Split: **1,732**
- pure Merge: **1,936**
- either: **3,347**
- both: **321**
- neither: **3,049**

Revised H4 gold rule:

Removing whitespace from source and correction must preserve the exact character sequence.

**Why the process changed:** the original label name alone was insufficient to define a true boundary-only correction.

---

### 3.11 ARETA diagnostic environment

ARETA was frozen as **diagnostic only**, not independent human gold.

#### Failure 1

Run: `36656461533`

Cause:

Historical `scikit-learn==0.23.2` under Python 3.9 pulled an old NumPy source build and failed with `CCompiler` metadata error.

Repair:

Python 3.9 → Python 3.8 while preserving historical pins.

#### Failure 2

Run: `36657211515`

Cause:

missing CAMeL morphology database.

Repair:

use historical CAMeL Tools command:

`camel_data light`

#### Final success

Run: `36657724871`

Result:

**SUCCESS**

Synthetic labels included:

`UC, UC, UC, OH, UC, UC`

Artifact ID: `11073405357`

**Failure classification:** infrastructure/runtime compatibility only; no scientific metric implication.

---

### 3.12 ARETA CALIBRATION enrichment

Run: `36658916857`

Result: **SUCCESS**

Processed:

- **6,888 / 6,888 = 100%**

Diagnostic strata:

- orthographic: **6,363 / 6,888 = 92.38%**
- morphology MI/MT: **1,544 / 6,888 = 22.42%**
- syntax: **3,640 / 6,888 = 52.85%**
- boundary MG/SP: **2,997 / 6,888 = 43.51%**
- contains UNK: **706 / 6,888 = 10.25%**

Important:

ARETA remained diagnostic and was not promoted to approval gold.

**Classification:** IMPROVED diagnostic observability / verifier performance still unmeasured.

---

### 3.13 H1 candidate generation

Run: `36691616010`

Result: **SUCCESS**

Population:

- CALIBRATION: **6,888**
- candidates: **46,811**
- exact QALB-supported: **32,502 = 69.4324%**
- reference-unsupported: **14,309 = 30.5676%**
- truncated cases: **0**
- non-applicable edits: **18**

Interpretation:

H1 is a candidate generator, not independent safety evidence.

Single-reference QALB means unsupported does not automatically mean linguistically wrong.

---

### 3.14 H2 deterministic orthographic calibration

Frozen promotion gate:

**strict-reference precision lower bound ≥98%**

Measured families:

- HAMZA_ALIF_SEAT: **85.57%**
- ALIF_MAQSURA_YA: **90.34%**
- TA_MARBUTA_HA: **94.01%**
- ALIF_VARIANT: **95.85%**
- SINGLE_ARABIC_LETTER_ORTHOGRAPHIC: **93.90%**

Promoted families:

- **0 / 5 = 0%**

**Decision:** do not lower the 98% gate.

**Classification:** MIXED

Methodology improved because the families were measured reproducibly; automatic-approval outlook worsened.

---

### 3.15 H4 calibration outcome

Frozen H4 automatic-approval gate required structural legality and multiple independent non-H1 evidence families.

Known outcomes:

- split recall: **0% — FAIL**
- merge recall: **47.45%**
- required recall: **≥70%**
- merge gap to gate: **−22.55 pp**
- merge precision lower bound: **96.01%**
- adversarial accepted: **0**
- no-boundary accepted: **0**

**Decision:** H4 was not activated.

**Interpretation:** strong conservatism was insufficient if recall could not meet the preregistered gate.

---

### 3.16 MP-SEF redesign

The project moved from component-level approval toward **whole-source-anchored proposal feasibility**.

Primary executable action space was frozen to:

- KEEP
- P1_FINAL
- P2_FINAL

No edit-level hybrid fusion was permitted in the primary measurement.

Diagnostic components remained separate for `R_raw`.

Primary development population:

- C_F: **1,918 records**
- clusters: **764**

Other roles:

- C_T: **2,898 / 1,020 clusters**
- C_R: **2,072 / 768 clusters**
- cluster overlap: **0**

The claim scope was explicitly restricted to:

**DEVELOPMENT FEASIBILITY / NOT INDEPENDENT GENERALIZATION EVIDENCE**

---

### 3.17 Foundational MP-SEF preflight

Run: `36763150865`

Result: **PASS**

Verified:

- all **6,888** records assigned once;
- **2,552** clusters;
- role overlap: **0**;
- no feasibility metric computed;
- no selector trained;
- reserved/internal data remained closed.

Important:

`measurement_authorized_by_preflight=false`

**Reason:** a successful preflight proves protocol integrity, not performance.

---

### 3.18 P1 C_F source-only proposal freeze

Run: `36765798233`

Result: **SUCCESS / FROZEN**

- cases: **1,918 / 1,918 = 100%**
- clusters: **764**
- batch/single parity: **64 / 64 = 100%**
- changed vs source: **1,838 / 1,918 = 95.83%**
- protected touch: **19 / 1,918 = 0.99%**
- empty output: **0**
- proposal SHA-256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`

The 95.83% value is activity, not quality.

---

### 3.19 P2 C_F source-only proposal freeze

Run: `36768378938`

Initial source-only result:

- cases: **1,918 / 1,918 = 100%**
- batch/single parity: **32 / 32 = 100%**
- changed vs source: **1,906 / 1,918 = 99.37%**
- protected touch: **21 / 1,918 = 1.10%**
- empty output: **0**
- proposal SHA-256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

At this point P2 appeared operationally frozen and reproducible.

**Later status:** REINTERPRETED / PROVENANCE DEFECT DISCOVERED.

---

### 3.20 Independent higher-model premeasurement review

Verdict:

**MODIFY BEFORE SECOND PREFLIGHT**

Findings:

- **5 BLOCKER**
- **5 MAJOR**

Major concerns included:

- prior measurement exposure;
- lack of truly gold-blind legality;
- protected-edge/linkage weaknesses;
- alignment ambiguity;
- truncation/EOS/zip safety;
- punctuation classification;
- scorer architecture and gold separation;
- runtime/experiment locks;
- population conflict 317 vs 1918;
- incomplete failure accounting.

This review materially changed the project architecture.

**Reason for accepting the review instead of proceeding:** methodological validity was more important than obtaining an early performance number.

---

### 3.21 Measurement exposure audit

Historical attempts:

#### Attempt A

Run: `36775239051`

Failed quickly.

No final summary or per-sentence output.

#### Attempt B

Run: `36775748058`

Cancelled after approximately three hours.

Gold-aware scoring progress observed at least through:

- 100
- 200
- 300
- 400
- 500 / 1,918

Correct classification:

**PARTIAL TECHNICAL GOLD-AWARE EXECUTION OCCURRED / INVALIDATED / NO VALID FINAL OR PERSISTED METRIC OUTPUT FOUND**

Human exposure recollection:

**UNKNOWN / NOT OBSERVED BY OPERATOR / insufficient recollection**

Scientific rule:

Do not use or infer a metric from these invalid attempts.

---

### 3.22 Population precedence correction

Historical 317-record amendment was rejected as governing population for the corrected cycle.

Current primary population:

- **C_F = 1,918 cases / 764 clusters**

The 317 records remain historical context only.

---

### 3.23 Long-process monitoring

A permanent monitoring layer was added:

- `process_progress_v1.py`
- `run_with_progress_watchdog_v1.py`

Required outputs:

- processed;
- total;
- percentage;
- heartbeat;
- last progress;
- stale time;
- rate;
- ETA;
- predicted finish time;
- confidence;
- final return code.

Adaptive ETA later added using recent-rate EWMA blended with long-run rate.

**Classification:** IMPROVED OPERATIONAL OBSERVABILITY / scientific performance unchanged.

---

### 3.24 P2 generation-trace failures before successful trace

The P2 source-only trace was deliberately instrumented rather than assumed valid.

#### Failure: checkout expression

Run: `36806187894`

Cause:

incorrect escaped GitHub ref expression.

Scientific process did not run.

Repair:

workflow expression corrected.

#### Failure: missing runtime dependency

Run: `36806269662`

Cause:

reduced runtime lacked `regex`.

Scientific process did not run.

Repair:

runtime stack aligned with frozen successful P2 environment.

#### Failure: GED count mismatch detected

Run: `36806404629`

Watchdog status:

- **0 / 1,918**
- failed immediately

Example:

`dev:1003: morph/GED count mismatch 50 != 58`

This was the first direct signal of the deeper P2 provenance defect.

---

### 3.25 P2 GED word-alignment provenance defect

Source-only investigation established:

- mismatch: **1,918 / 1,918 = 100%**
- exact morphology-word/GED-label count matches: **0 / 1,918 = 0%**
- all differences positive
- minimum excess: **2**
- maximum excess: **87**
- median excess: **15**
- mean excess: **15.8191**
- total dropped GED predictions under frozen zip semantics: **30,341**

Root cause:

Frozen P2 used subword-level GED predictions after removing special tokens, then consumed them using:

`zip(morph_words, ged_labels)`

as if they were word-level labels.

The robust upstream ErrorIdentifier path instead explicitly aligns first wordpieces to words and ignores remaining wordpieces.

Classification:

**PROVENANCE / IMPLEMENTATION FAILURE**

Root-cause confidence:

**HIGH**

Repairability:

**FIXABLE_NEXT_VERSION_ONLY**

Reason:

The bug itself is technically repairable, but the current P2 artifact is already frozen and cannot be silently regenerated inside the same cycle.

---

### 3.26 Successful P2 source-only generation trace

Run: `36807862693`

Result: **SUCCESS**

- reproduced frozen outputs exactly: **1,918 / 1,918 = 100%**
- GED alignment mismatch: **1,918 / 1,918 = 100%**
- dropped GED predictions: **30,341**
- generation ceiling cases: **24 / 1,918 = 1.25%**
- missing terminal EOS: **0 / 1,918 = 0%**

Interpretation:

Reproducibility of the defect was excellent; scientific executability was not.

**Classification:** WORSENED P2 PROVENANCE / STRONGLY IMPROVED EVIDENCE QUALITY

---

### 3.27 Gold-blind executable-action legalizer

Run: `36818173661`

Result: **SUCCESS**

Hypotheses:

- **3,836**

Action sets:

- **1,918**

State distribution:

- P1_OK: **1,806 / 1,918 = 94.16%**
- P1_PROTECTED_BLOCKED: **112 / 1,918 = 5.84%**
- P2_EXECUTION_FAILED: **1,918 / 1,918 = 100%**

Frozen action-set SHA-256:

`6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`

Current-cycle scientific consequence:

P2 contributes **zero executable whole-hypothesis actions**.

This does **not** establish poor linguistic quality. It establishes failed provenance/executability.

---

### 3.28 Scorer V2 redesign

Primary fixes:

- legality loaded from frozen action artifacts rather than recomputed after gold;
- corrected punctuation classification;
- letters `a/m/p` no longer treated as punctuation;
- mixed punctuation+linguistic boundary corrections remain in the denominator;
- no-op and multiple-reference target defects fail closed;
- whole-action oracle only;
- no target-by-target P1/P2 union;
- scoring failures become explicit uncertainty intervals rather than known zero;
- `R_raw` is diagnostic-only;
- `R_clean` requires zero extra edits;
- entire target denominator is built before candidate evaluation;
- exact 95% gate uses integer arithmetic:
  `20 × N ≥ 19 × D`.

No authorized project `R_joint` measurement has been produced.

---

### 3.29 Second Preflight V2 baseline

Run: `36823611871`

Operational conclusion: **SUCCESS**

Scientific readiness conclusion:

`SECOND_PREFLIGHT_NOT_READY`

Checklist:

- PASS: **8 / 22 = 36.36%**
- PARTIAL: **13 / 22 = 59.09%**
- BLOCKED: **1 / 22 = 4.55%**
- FAIL: **0 / 22 = 0%**

Weighted remediation:

- **65.91%**

Important:

- gold loaded: **false**
- measurement authorized: **false**
- `R_joint` computed: **false**

The single blocked item was C21, concerning experiment authorization/consumption locking.

Interpretation:

The corrected architecture showed substantial methodological progress, but the second-preflight contract was not yet fully satisfied.

---

## 4. Current failure/repairability ledger

### P2 GED alignment

- class: PROVENANCE / IMPLEMENTATION
- scope: **100% of 1,918 P2 cases**
- root cause confidence: HIGH
- repairable: YES
- repair class: `FIXABLE_NEXT_VERSION_ONLY`
- current-cycle salvage: NO
- next-version options:
  - repair wordpiece→word GED alignment;
  - replace GED interface;
  - replace P2 proposer;
  - add a complementary proposer.

### P1 protected blocks

- blocked: **112 / 1,918 = 5.84%**
- status: legally blocked in current frozen cycle
- quality implication: NONE by itself
- future work: inspect whether protection rules are correctly conservative or systematically over-block useful corrections without weakening invariant safety.

### H2 family-wide automatic approval

- promoted: **0 / 5**
- reason: no family reached frozen 98% lower-bound gate
- repairability: potentially through narrower predicates, stronger evidence, or different architecture;
- prohibited response: lowering the gate merely to obtain promotion.

### H4

- split recall: 0%
- merge recall: 47.45%
- gate: ≥70%
- activation: NO
- likely future options:
  - richer evidence;
  - different boundary model;
  - replace component;
  - keep as diagnostic only.

### Second Preflight

- FAIL: 0
- PARTIAL: 13
- BLOCKED: 1
- engineering interpretation: primarily incomplete proof/test coverage rather than demonstrated architecture collapse.
- next high-priority blocker: C21 experiment lock.

---

## 5. Decision ledger — why major paths were chosen

### Why abandon a monolithic verifier?

Because coverage improved while unsafe acceptance worsened from **4.17% to 18.75%**.

### Why keep M2-R evidence but not use it as final safety?

Because it improved several residual-risk metrics but remained insufficiently precise/complete for standalone approval.

### Why heterogeneous M2-H?

Because different error families require different evidence types; generic confidence was not adequate safety evidence.

### Why dual environments?

Because historical H1 reproducibility and modern CAMeL Tools requirements were incompatible in one environment.

### Why keep reserved/internal datasets closed?

To preserve future evaluation value and reduce adaptive leakage.

### Why redefine H4 boundary gold?

Because QALB Split/Merge labels were broader than true whitespace-only boundary corrections.

### Why treat ARETA as diagnostic only?

Because it is not independent exhaustive human gold for the system's target claims.

### Why refuse to lower H2/H4 gates?

Because gates were preregistered scientific requirements, not optimization targets.

### Why move to MP-SEF whole actions?

To prevent unsafe edit-level mixing and define a measurable candidate-availability question over frozen whole hypotheses.

### Why independent higher-model review before measurement?

To detect methodological defects before consuming gold and reporting an apparently valid metric.

### Why invalidate prior scorer attempts?

Because partial technical gold-aware execution was not equivalent to a valid frozen authorized measurement.

### Why block P2 instead of correcting it in place?

Because correcting a frozen proposer after discovering a provenance defect would mutate the candidate set and damage scientific validity.

### Why create a new-version repair lane?

To preserve historical evidence while still allowing the architecture to improve.

---

## 6. Governance rules now permanently adopted

### Failure triage

Every FAIL/BLOCKED/PARTIAL requires:

1. observed failure;
2. reproducibility;
3. root cause;
4. scope;
5. confidence;
6. repairability;
7. current-cycle vs next-version repair decision;
8. regression test.

### Maximum-quality reassessment

Earlier phases are not sacred.

The project may return to:

- target definition;
- input representation;
- NoPnx policy;
- proposer selection;
- GED/morphology;
- P1/P2 architecture;
- protection;
- matching/scoring;
- model/runtime choices;
- workflow structure.

Frozen evidence must remain immutable.

### Two lanes

**Lane A — frozen evidence**

Historical runs, hashes, outputs, failures, and measurements remain unchanged.

**Lane B — versioned redesign**

New architecture is allowed when evidence justifies it.

### Long-process observability

Every new long process must expose progress, stale detection, rate, ETA, and final state.

---

## 7. Current system state as of this ledger creation

Scientific state:

**IMPROVED STRONGLY IN METHODOLOGICAL CONTROL / ARCHITECTURE STILL UNDER REASSESSMENT**

Current strongest facts:

- no valid current-cycle `R_joint` has been authorized;
- P1 has **1,806 / 1,918 = 94.16%** executable frozen proposals;
- P2 has **0 / 1,918 executable proposals** in the current cycle because of provenance;
- P2 defect itself is considered technically repairable in a new version;
- Second Preflight baseline weighted remediation is **65.91%**;
- no Second Preflight FAIL exists;
- one checklist item remains BLOCKED and 13 PARTIAL at the current baseline;
- current architecture should be re-baselined before spending additional gold-aware evaluation exposure.

Current engineering confidence that the project can reach a strong scientifically defensible system:

**approximately 85% qualitative engineering confidence**, not a statistical success probability.

This confidence must not be confused with the unknown probability of passing the future `R_joint ≥95%` gate.

---

## 8. Mandatory future re-baseline review

Before any new gold-aware measurement, compare at least:

1. KEEP CURRENT P1-only executable architecture;
2. REPAIR P2 as `P2_V2`;
3. REPLACE P2 with a stronger proposer;
4. ADD a complementary proposer;
5. CHANGE GED/morphology interface;
6. revise candidate-generation architecture while preserving frozen evidence;
7. reconsider whether whole-action-only primary evaluation remains the strongest safety/utility design;
8. reassess whether protection is overly conservative or appropriately fail-closed.

For every option record:

- expected benefit;
- scientific risk;
- implementation risk;
- exposure/contamination risk;
- testability;
- reversibility;
- resource cost;
- likely effect on candidate coverage;
- effect on protected invariants.

---

## 9. Research / doctoral-dissertation conversion map

ACAD_PASS may become academically valuable because its history contains more than an application implementation.

Potential research themes include:

### 9.1 Safe academic-document transformation

Possible question:

How can an automated academic-document transformation system maximize useful correction while preserving scientific invariants and providing auditable uncertainty?

Potential contribution:

A structured transformation architecture combining protected invariants, reversible edit transactions, independent verification, fail-closed legality, and review escalation.

### 9.2 Arabic GEC under scientific-document constraints

Possible question:

How should Arabic grammatical/error-correction candidates be verified when single-reference correction data cannot directly establish mandatory correctness or document safety?

Potential contribution:

A distinction among candidate generation, legality, linguistic matching, complete repair, and scientific-document safety.

### 9.3 Provenance-safe candidate availability

Possible question:

Can whole-hypothesis candidate availability be evaluated without allowing gold to affect executability?

Potential contribution:

Gold-blind legalizer + frozen whole-action scorer + source-only diagnostic evidence.

### 9.4 Failure-aware reproducibility

Possible question:

How should failed model/runtime/provenance paths be incorporated into trustworthy AI evaluation rather than discarded?

Potential contribution:

Failure-triage contracts, immutable evidence lane, versioned redesign lane, and one-shot/preflight measurement control.

### 9.5 Protected-invariant academic NLP

Possible question:

How can correction systems protect citations, numbers, units, equations, technical tokens, URLs, and document structure while still allowing linguistic repair?

Potential contribution:

Derived protection maps and source/output legality auditing.

### 9.6 Adaptive architecture re-baselining

Possible question:

Can a document-intelligence system systematically decide when to repair, replace, remove, or complement a component based on reproducible failure evidence?

Potential contribution:

Evidence-driven re-baselining governance.

---

## 10. What would still be required for a strong academic paper or PhD thesis

The engineering history alone is not sufficient.

A strong academic conversion would still require:

- fresh literature review;
- explicit research gap;
- defensible novelty claim;
- formal research questions/hypotheses;
- clear separation between development and independent evaluation;
- strong baselines;
- ablation studies;
- statistically justified evaluation;
- external/held-out/generalization data;
- reproducibility package;
- threat-to-validity analysis;
- human/expert evaluation where required;
- comparison with contemporary Arabic GEC and document-intelligence systems;
- careful distinction between product engineering and scientific contribution.

No thesis-level novelty claim is frozen yet.

---

## 11. Why negative results matter academically

The following failures may themselves be scientifically useful if analyzed rigorously:

- monolithic verifier unsafe-acceptance trade-off;
- incomplete value of residual-only verification;
- mismatch between QALB Split/Merge labels and pure boundary corrections;
- inability of broad deterministic orthographic families to reach a 98% gate;
- H4 precision/recall trade-off;
- P2 subword/word GED provenance defect;
- difference between output reproducibility and scientific executability;
- difference between activity rate and correction quality;
- effect of protected invariants on candidate availability;
- scorer/preflight design needed to prevent gold-contaminated legality.

Negative results must not be retroactively optimized away.

---

## 12. Academic evidence hygiene

For future paper/thesis use:

- preserve run IDs;
- preserve exact commit SHAs;
- preserve model revisions;
- preserve artifact hashes;
- preserve failures;
- preserve old versions after supersession;
- document exposure history;
- distinguish diagnostic from primary evidence;
- distinguish development feasibility from independent generalization;
- never reuse invalidated numbers as valid results.

---

## 13. Living research notebook fields for every future checkpoint

Append entries using this template:

### YYYY-MM-DD — <Stage / Version>

**Objective**

...

**Why this route**

...

**Inputs / frozen identities**

...

**Execution**

...

**Result**

- status:
- counts:
- percentages:
- gate:
- uncertainty:

**Failure analysis**

- class:
- root cause:
- confidence:
- affected scope:
- repairability:
- current-cycle repair allowed:

**Comparison with previous checkpoint**

- IMPROVED / WORSENED / MIXED
- comparable magnitude:

**Architecture consequence**

...

**Research significance**

...

**Commercial/product significance**

...

**Evidence**

- commits:
- workflow runs:
- artifacts:
- hashes:

**Next authorized step**

...

---

## 14. Relationship to RESUME_HERE.md

`RESUME_HERE.md` remains the **operational handoff**: what is true now and what to do next.

This file is the **historical/scientific ledger**: how the system got here and why.

Both must be updated after meaningful checkpoints.

If they conflict:

1. frozen artifacts/hashes and explicit superseding records take precedence;
2. update both files to document the discrepancy;
3. never silently erase the older historical state.

---

## 15. Current next step

1. complete Second Preflight remediation, beginning with the C21 experiment authorization/consumption lock;
2. close the remaining PARTIAL checks with explicit synthetic tests;
3. preserve the resulting preflight as a new historical checkpoint;
4. conduct architecture re-baseline before any new gold-aware `R_joint`;
5. prepare higher-model independent review package for the architecture decision;
6. decide whether to continue P1-only, build P2_V2, replace P2, or add complementary proposal generation;
7. only after that decision should a new measurement-authorization path be considered.



### 2026-10-01 — Advanced Second Preflight V2 revalidation

**Objective**

Re-run the stronger C01-C22 second-premeasurement preflight against the current hardened code after scorer denominator/gate changes and governance hardening.

**Why this route**

A previous advanced run had already passed 22/22, but code changed afterward. Scientific validity required revalidation on the current exact commit rather than inheriting an old PASS.

**Execution**

- run: `36825797396`
- code commit: `7c31da92a75495f11e1faac10ecc4e84685845c3`
- artifact: `11145072418`
- artifact digest:
  `sha256:fcd653251e4e6870adfdcfb26d71e2bfa8f11f14e6f15b040f054077cb008896`
- checklist SHA256:
  `3103089eaa04576816509b8f2940c721ed8a931c1f4a7a6802b1e86a0b301eb8`

**Result**

- status: PASS
- C01-C22: **22 / 22 = 100% PASS**
- FAIL: **0 / 22 = 0%**
- PARTIAL: **0 / 22 = 0%**
- BLOCKED: **0 / 22 = 0%**
- project gold loaded: false
- project metric computed: false
- measurement authorization: false

**Comparison with previous checkpoint**

Previous simplified baseline:
- strict PASS: **36.36%**
- weighted remediation: **65.91%**
- PASS/PARTIAL/BLOCKED: 8/13/1

Current advanced suite:
- strict PASS: **100%**
- change in strict PASS: **+63.64 percentage points**
- change versus weighted remediation reference: **+34.09 percentage points**

The earlier baseline is **SUPERSEDED FOR CURRENT READINESS**, not deleted. It remains historical evidence of how remediation progressed.

**Failure analysis**

No checklist failure remained in the advanced suite.

This does not imply model/candidate quality success. It establishes preauthorization engineering/methodological readiness only.

**Architecture consequence**

The successful preflight does NOT automatically authorize measurement.

Because frozen P2 contributes zero executable actions, the Maximum-Quality Reassessment Contract requires an architecture re-baseline before spending additional gold-aware measurement exposure.

**Research significance**

This checkpoint demonstrates a complete source-only preauthorization acceptance suite after an earlier independent review found 5 BLOCKER and 5 MAJOR issues.

It is potentially valuable future reproducibility/methodology evidence, but is not itself a performance result.

**Next authorized step**

Architecture re-baseline + independent higher-model review before any new R_joint authorization.


### 2026-10-01 — Arabic correction architecture re-baseline V1

**Objective**

Reassess whether the effective P1-only current cycle remains the strongest architecture after the frozen P2 provenance failure, without consuming new gold.

**Why this route**

The advanced source-only Second Preflight reached 22/22 PASS, but P2 still contributes 0/1918 executable actions. Finishing a gold-aware measurement on this asymmetric candidate space could waste evaluation exposure if a stronger source-only architecture can first be constructed.

Fresh literature and implementation review showed:

- ACL 2025 SWEET/text editing is a strong current Arabic GEC family and supports iterative/cascaded correction.
- The strongest published ensembles combine heterogeneous systems, notably Seq2Seq++ plus multiple SWEET variants.
- The ACL 2025 ensemble uses source-aligned edit majority voting and prioritizes precision.
- EMNLP 2023 Arabic Seq2Seq+GED/morphology remains a strong complementary architecture family.
- EACL 2026 Nahw indicates that current general LLMs still have substantial Arabic grammar limitations and should not be promoted to sole primary corrector/verifier.

**Decision**

The frozen V3 cycle remains immutable as the control lane.

Open a new redesign lane with:

1. P1 family retained as frozen/control SWEET NoPnx.
2. P2_V2: repair the Seq2Seq++ GED/morphology route with explicit wordpiece-to-word GED alignment and complete provenance.
3. P3_V1: add a strong reproducible iterative/cascaded SWEET variant.
4. optional heterogeneous fourth proposer only if independently reproducible and justified.

P2 is therefore:
- NOT abandoned;
- NOT repaired in place;
- FIXABLE_NEXT_VERSION_ONLY;
- strategically retained because architecture diversity is valuable.

A new MP-SEF V4 candidate may investigate source-only consensus/edit voting, but current V3 whole-action rules MUST NOT be changed retroactively.

**Research significance**

The re-baseline creates a testable research question about whether heterogeneous proposer families improve candidate diversity and later safe candidate availability while protected invariants remain fail-closed.

**Performance status**

No new correctness metric was computed.

Classification:
**IMPROVED STRATEGICALLY / PERFORMANCE NOT YET MEASURED**

**Evidence**

- re-baseline document:
  `phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_REBASELINE_V1.md`
- commit:
  `2204718b51f9580a6d4d8ddaa33a903f686eb262`

**Next step**

Prepare P2_V2 and P3_V1 source-only specifications plus independent higher-model architecture review before implementing any gold-aware measurement.


### 2026-10-01 — Versioned proposer redesign specifications + independent review gate

**Objective**

Convert the architecture re-baseline into explicit source-only implementation specifications before any new proposer execution or gold-aware measurement.

**New frozen design artifacts**

P2_V2 specification:
`phase2/redesign/MPSEF_P2_V2_IMPLEMENTATION_SPEC.md`

Commit:
`5e34e8e75dd3ef1e930d3d2b6528e7f79b709932`

Key decision:
- repair the Seq2Seq++ GED/morphology route in a NEW version;
- use first-wordpiece/ignore-index word-level GED alignment;
- prohibit zip truncation;
- preserve segmentation/truncation/EOS/provenance traces;
- no gold during implementation validation.

P3_V1 specification:
`phase2/redesign/MPSEF_P3_V1_SWEET_PNX_CASCADE_SPEC.md`

Commit:
`73ae1bee99c866dec8b91affd7f50c5465f36082`

Important discovery:
current P1 already equals `SWEET_QALB14_NOPNX_ITER2`.
Therefore a third proposer must NOT duplicate SWEET2.
P3_V1 is the published cascade:
`NoPnx ×2 -> Pnx ×1`.

Source-only proposer diversity protocol:
`phase2/redesign/MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V1.md`

Commit:
`5e0ad432b513bd65daa567cdc2e046c9d18996dd`

The protocol freezes:
- synthetic stage;
- deterministic source-only parity packet;
- hard provenance/parity/truncation gates;
- pairwise output/component diversity;
- architecture-independence labels;
- diagnostic-only consensus support;
- no correctness metrics;
- no arbitrary numeric diversity threshold before independent review.

**Fresh literature consequence**

ACL 2025 reports:
- iterative SWEET improves MSA up to two iterations;
- NoPnx then Pnx cascade improves MSA;
- heterogeneous ensemble of Seq2Seq++ + SWEET2 + SWEET2_NoPnx→SWEET_Pnx outperforms single systems;
- ensemble uses source-aligned edit majority support, prioritizing precision.

This strongly supports comparing heterogeneous proposer families rather than restoring only one failed route.

**Independent review gate**

Review package:
`phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_INDEPENDENT_REVIEW_PACKAGE_V1.md`

Commit:
`43c8a4ad27b76f3715e723e77a80f737ba330829`

Higher-model prompt:
`phase2/redesign/ACAD_PASS_HIGHER_MODEL_ARCHITECTURE_REVIEW_PROMPT_V1.md`

Commit:
`f091590971954bedb3efaaaf27627ee344f86878`

Architecture snapshot for independent review:
`5e0ad432b513bd65daa567cdc2e046c9d18996dd`

**Current classification**

**IMPROVED STRONGLY IN ARCHITECTURE DISCIPLINE / PERFORMANCE NOT YET MEASURED**

No new gold/reference metric has been computed.

**Next gate**

Obtain independent higher-model architecture review.

If verdict:
- GO: proceed to source-only synthetic prototypes;
- MODIFY: fix BLOCKER/MAJOR findings first;
- STOP/REBASELINE: do not implement the current redesign.


### 2026-10-01 — Independent architecture review remediation checkpoint

**Independent review verdict**

`MODIFY BEFORE IMPLEMENTATION`

Frozen review lock:
`phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_INDEPENDENT_REVIEW_LOCK_V1.md`

Review uploaded-file SHA256 identities:
- report: `fd66165131b6cd597c1d864f5d7d85f8c17a3dac9b273e37f89909995a635457`
- ZIP: `c9393fb260ef7e27d9fa7b2d7edb908240332f44d3e9798c9a742a24d443e9ab`
- START_HERE: `df08fd84747afc028cfe237c502428dea447c15580093905032a60d4f251c980`

Findings:
- BLOCKER: 2
- MAJOR: 5
- MINOR: 2
- 30 review questions answered
- 6 synthetic findings reproduced by independent reviewer

**B01 — design remediation**

New contract:
`phase2/redesign/MPSEF_P2_V2_WORD_IDENTITY_CONTRACT_V1.md`

Commit:
`0d32f7ff4fb75aa98ec67c92b291597ebb406faa`

Adds explicit UID→morph-word→segment→first-wordpiece→GED label→GEC subword identity, zero-token failure, single-word-over-budget failure, label-name mapping, generation-config identity, and ged_tags interface proof.

Status:
**DESIGN CLOSED / SYNTHETIC IMPLEMENTATION VALIDATED**

**B02 — design remediation**

New contract:
`phase2/redesign/MPSEF_V4_CANDIDATE_REGISTRY_ACTIONSET_CONTRACT_V1.md`

Commit:
`e7e24a1430c89bc70106abf00833e845092d07c7`

Defines:
- new V4 registry namespace;
- explicit P1/P2_V2/P3 IDs/versions/families/ancestry;
- KEEP invariant;
- exact-string dedup preserving all provenance;
- 1+N pre-dedup action capacity;
- generic future legalizer boundary;
- strict isolation from V3 scorer/guard/experiment identities.

Status:
**DESIGN CLOSED**

**M01 — P3 role remediation**

New amendment:
`phase2/redesign/MPSEF_P3_V1_ROLE_INDEPENDENCE_AMENDMENT_V2.md`

Commit:
`007247d3ad2f297b7272da3baa35379cfe91c5a6`

P3 is now:
- OPTIONAL;
- FULL_WITH_PUNCTUATION;
- same `SWEET_QALB14` family as P1;
- not an independent support vote;
- final legality evaluated original-source→P3-final.

Status:
**DESIGN CLOSED**

**M02 — diversity protocol remediation**

New protocol:
`phase2/redesign/MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md`

Commit:
`88077f47090041a61dfab8caf1df459b5bf3cc68`

Stage 1 now frozen to:
- 128 UIDs;
- 128 distinct clusters;
- deterministic source-only cluster-aware hashing;
- parity subset: 32 UIDs;
- explicit D_all / D_exec / D_joint_exec / D_legal / D_changed denominators;
- source-only legal marginal contribution;
- source-only KEEP-only reduction;
- source-only leave-one-proposer-out;
- failure-inclusive pairwise diagnostics;
- 180-minute engineering workflow timeout;
- no invented quality/diversity threshold.

Status:
**DESIGN CLOSED**

**M03 — protection diagnosis**

New shadow diagnostic:
`phase2/redesign/ACAD_PASS_PROTECTED_LINKAGE_SHADOW_DIAGNOSTIC_V1.md`

Commit:
`0d2e183023efa1a86030deed4bed30e3de5c2902`

Current frozen protection remains authoritative.
Shadow policy can only diagnose global-word-ordinal-only disagreement.

Status:
**DIAGNOSTIC CONTRACT READY / NO HISTORICAL RESCUE**

**M04 / M05 — scorer repair**

Historical scorer V2 remains unchanged.

New scorer:
`phase2/redesign/mpsef_rjoint_score_v3.py`

Commit:
`e18561cab8d50b10061f7ed5882a8b0b2081aa64`

M04 fix:
- target count comes from independently frozen target population;
- all-action scoring failure with N targets preserves conservative `[0,N]`.

M05 fix:
- combined weak route such as BOUNDARY={SPLIT,MERGE} maximizes one whole action over the union of target indices;
- no `sum(max)` across different actions.

Synthetic workflow:
- run: `36863251498`
- conclusion: SUCCESS
- artifact: `11162062048`
- artifact digest:
  `sha256:d051f6c4a93543f7d23cb07c36c711fc3de7197137e5d7b6b2dc334f07030982`

Status:
**SYNTHETIC PASS**

**P2_V2 Stage 0 identity harness**

Implementation:
`phase2/redesign/mpsef_p2_v2_identity_stage0.py`

Commit:
`27998071ba124d0126931b936ce263f585044f55`

Workflow:
`.github/workflows/phase2-mpsef-p2-v2-identity-stage0.yml`

Run:
`36863549449`

Conclusion:
**SUCCESS**

Artifact:
`11162862266`

Artifact digest:
`sha256:c6a875b7880db119ea660ea84a47c250f49f624d610b4849419e2fd5aa5893e8`

Properties:
- project source loaded: false
- project gold loaded: false
- project metric computed: false
- real model inference: false
- B01 identity/overflow/zero-token/label/EOS/ged_tags synthetic cases: PASS

**Current classification**

**IMPROVED SUBSTANTIALLY / REVIEW FINDINGS BEING CLOSED WITHOUT GOLD**

No Stage 1 source packet has been executed yet.
No new R_joint has been computed.

**Next gate**

A focused independent closure review is required for B01/B02/M01/M02 and the Stage 0 evidence before Stage 1 project-source execution.


### 2026-10-01 — Independent architecture review remediation started

Independent verdict:
**MODIFY BEFORE IMPLEMENTATION**

Frozen review lock:
`phase2/redesign/ACAD_PASS_ARABIC_ARCHITECTURE_INDEPENDENT_REVIEW_LOCK_V1.md`
commit:
`ab142dd90e0c600fa11de5650b2ab15eeb5fcc7b`

Review findings:
- BLOCKER: 2
- MAJOR: 5
- MINOR: 2

No project gold/R_joint/model population run was used by the review.

Remediation completed so far:

1. **B01 design closed**
   - `MPSEF_P2_V2_WORD_IDENTITY_CONTRACT_V1.md`
   - commit `0d32f7ff4fb75aa98ec67c92b291597ebb406faa`
   - explicit UID→word→segment→first-wordpiece→GED label→GEC subword bijection;
   - zero-token/over-budget words fail explicitly;
   - label vocab/config/generation identity frozen;
   - no count-only proof.

2. **B02 design closed**
   - `MPSEF_V4_PROPOSER_REGISTRY_ACTION_SET_CONTRACT_V1.md`
   - commit `5466e6b9e64235c34db44355d57b638206b9a939`
   - new proposer registry/action-set lane;
   - variable 1+N action capacity before dedup;
   - exact literal dedup retaining all provenance;
   - new artifact/experiment identities;
   - V3 guard/authorization explicitly invalid for V4.

3. **M01 design closed**
   - `MPSEF_P3_V1_ROLE_AMENDMENT_V2.md`
   - commit `b2f56fee86666100ce5e9690a8fe6057228cfde0`
   - P3 is optional SWEET-family cascade extension;
   - P1/P3 never count as independent support;
   - protection reruns on original source→final P3 output.

4. **M02 design closed**
   - `MPSEF_SOURCE_ONLY_PROPOSER_DIVERSITY_PROTOCOL_V2.md`
   - commit `88077f47090041a61dfab8caf1df459b5bf3cc68`
   - Stage1 packet=128 UIDs/128 clusters;
   - explicit denominators/formulas;
   - legal marginal contribution/KEEP-only reduction/source-only leave-one-out;
   - parity/resource/failure accounting;
   - no invented linguistic diversity threshold.

5. **M03 diagnostic contract added**
   - `MPSEF_PROTECTION_SHADOW_DIAGNOSTIC_CONTRACT_V1.md`
   - commit `fb4cf91396e1ef584b60177a6ad870862df05105`
   - diagnostic decomposition of global-ordinal overblocking;
   - authoritative current legalizer remains unchanged;
   - no historical V3 rescue.

Current interpretation:
**IMPROVED STRONGLY IN IMPLEMENTATION CONTRACT QUALITY / PERFORMANCE STILL UNMEASURED**

Next critical work:
- fix M04 scorer all-actions-fail interval semantics;
- fix M05 BOUNDARY whole-action aggregation;
- add synthetic regressions;
- version scorer/preflight before any future gold-aware measurement.


### 2026-10-01 — Independent-review remediation: design blockers closed; scorer M04/M05 synthetic PASS

**Independent verdict**

The external architecture review returned:
**MODIFY BEFORE IMPLEMENTATION**, with 2 BLOCKER, 5 MAJOR, 2 MINOR findings.

**Design remediation completed**

- B01: P2_V2 identity strengthened from count equality to explicit UID→word→segment→first-wordpiece→GED label→GEC subword bijection, including zero-token and single-word-over-budget failures.
- B02: a new V4 proposer registry/action-set contract separates new proposer IDs, ancestry, literal dedup with provenance, variable action count, artifact identity, and future experiment authorization from frozen V3.
- M01: P3 is optional P1-family cascade extension, not an independent vote.
- M02: source-only diversity protocol V2 defines Stage 1 as 128 UIDs from 128 clusters, explicit denominators, legal marginal contribution, KEEP-only reduction, source-only leave-one-out, parity, resource accounting and pre-Stage2 retention rules.
- M03: shadow protection diagnostics isolate global-ordinal-only blocking without weakening or rewriting V3 protection.

**M04/M05 implementation**

Historical scorer V2 was preserved.

New scorer:
`phase2/redesign/mpsef_rjoint_score_v3.py`

Commit:
`7a01d797e5fd630186910e38f5487364639e8165`

Synthetic workflow:
`36867448366`

Result:
**PASS**

Artifact:
`11164975245`

Digest:
`sha256:1ed7076c272e66dfe1b4168568113d76c4294db863418352af210ffaae90bb65`

M04 now keeps the independently frozen target count even if every action scorer fails; N>0 produces conservative [0,N] uncertainty.

M05 now computes BOUNDARY={SPLIT,MERGE} using one whole action over the union and applies the same whole-action semantics to additional-target/cluster evidence.

**Comparison**

Methodological robustness:
**IMPROVED**

Performance quality:
**NOT MEASURED**

Gold exposure:
**UNCHANGED / NO NEW GOLD**

**Next**

Implement Stage 0 synthetic source-only harness for B01/B02/M01/M03; only after Stage 0 PASS may the deterministic Stage 1 source packet be materialized and executed.


### 2026-10-01 — P2_V2 B01 source-free Stage0 closes after one implementation failure and repair

**Objective**

Prove the repaired P2_V2 word/wordpiece/GED/GEC identity path using synthetic boundary tests and then real frozen models, without project source or gold.

**Synthetic result**

Run `36863549449`:
- **20/20 PASS**
- no project source;
- no gold;
- no project metric;
- no real-model inference.

Artifact:
`11162862266`

Digest:
`sha256:c6a875b7880db119ea660ea84a47c250f49f624d610b4849419e2fd5aa5893e8`

**Real-model failure**

Run `36864163724` failed before model inference.

Root cause:
the Stage0 implementation expected `BertTokenizerFast.cls_token_type_id`, a non-required tokenizer attribute.

Classification:
**IMPLEMENTATION / RUNTIME INTERFACE**

Repairability:
**CURRENT_CYCLE_PRE_GOLD**

The failure did not imply poor GED/GEC quality.

**Repair**

Commit:
`fe49ac916d7534b7178a3f0a87092da8b0dccad5`

Used explicit zero token-type IDs for the single BERT sequence and added segment-field length assertions.

**Real-model rerun**

Run:
`36868057043`

Result:
**PASS**

- 3 synthetic/public inputs;
- repeat parity: true;
- real models executed;
- project source loaded: false;
- project gold loaded: false;
- project metric computed: false;
- quality claimed: false.

Model weight identities:
- GED: `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f`
- GEC: `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f`

Artifact:
`11165486137`

Digest:
`sha256:9cdb16ad4f3606b2af158e296a7e59e24f3718aec18d8cbc174acfa4a2d50918`

**Comparison**

Implementation/provenance confidence:
**IMPROVED STRONGLY**

The earlier universal P2_V1 word-alignment defect is no longer present in the tested Stage0 route.

Linguistic quality:
**NOT MEASURED**

**Next**

Close B02/M01/M03 with source-free Stage0 synthetic tests. After the complete Stage0 gate, perform fresh deep research and maximum-effort architecture brainstorming before materializing Stage1.


### 2026-10-01 — V4 pre-Stage1 source-free Stage0 fully closes

**Aggregate result**

- B01 synthetic: **20/20 PASS**
- B01 real-model source-free: **PASS**
- B02: **17/17 PASS**
- M01: **4/4 PASS**
- M03: **10/10 PASS**
- M04/M05 scorer V3 synthetic preflight: **PASS**

Final B02/M01/M03 fail-closed run:
`36869672029`

Artifact:
`11164888387`

Digest:
`sha256:7efc253149097073929baeec7a6b69f05eb94dcfb9405dfb7033083a83d8ba4f`

**Failures preserved**

P2_V2 real-model Stage0 initially failed on a tokenizer interface assumption and was repaired after root-cause triage.

B02/M01/M03 Stage0 initially failed because shadow diagnostics prioritized alignment ambiguity over a known protected-signature change; the workflow also lacked pipefail through tee. Both were repaired and revalidated.

**Scientific state**

No project-source Stage1 execution occurred.
No new project gold/reference was opened.
No correctness metric or R_joint was computed.

**Comparison**

Implementation/provenance readiness:
**IMPROVED STRONGLY**

Linguistic performance:
**UNCHANGED / NOT MEASURED**

**Architecture consequence**

Stage0 completion is not automatic Stage1 authorization.

A fresh 2025–2026 research review and maximum-effort architecture brainstorming gate is mandatory before materializing the deterministic Stage1 packet.

The next decision must explicitly evaluate KEEP / REPAIR / REPLACE / ADD COMPLEMENT / DEFER for P1, P2_V2, P3 and possible V4 consensus.


### 2026-10-01 — Fresh 2025-2026 research re-baseline after full Stage0 PASS

**Objective**

Challenge the proposed Stage1 roster after implementation/provenance Stage0 succeeded, using fresh current research rather than assuming the earlier architecture remained optimal.

**Fresh evidence consequence**

Current Arabic evidence continues to support SWEET/text editing as a strong, maintained architecture and Seq2Seq+GED/morphology as a heterogeneous complementary family.

Newer evidence on edit-level majority voting and minimal-edit GEC increases the plausibility of future consensus, but does not justify implementing consensus before source-only diversity is observed.

Newer Arabic ensemble/preprint work supports multi-family combination but introduces selector/conflict-resolution leakage risks.

Arabic LLM evidence remains mixed enough that general LLMs are not promoted to the primary proposer roster.

**Frozen decisions**

- P1: KEEP.
- P2_V2: KEEP / PROCEED TO STAGE1.
- P3: KEEP OPTIONAL / PROCEED TO STAGE1.
- P4: DEFER.
- V4 consensus: DEFER.
- learned selector: DEFER.
- general LLM primary proposer: DEFER.
- protection: KEEP + shadow diagnostics.
- whole-action R_joint remains future primary construct.

**Architecture insight**

P1 and P3 are one SWEET family.
Current roster has only two materially independent families: SWEET and Seq2Seq+GED/morphology.

Any future family-majority consensus may require a third independent family.

**Comparison**

Methodological/architecture readiness:
**IMPROVED**

Linguistic performance:
**NOT MEASURED**

**Forecast**

Engineering estimate:
- ~90% optimism for reaching a scientifically defensible architecture;
- ~10% architecture/implementation risk.

Primary next risks:
candidate diversity, protection burden, and whether a third independent family becomes necessary.

**Next**

Freeze deterministic Stage1 source-only packet and implement/freeze Stage1 proposer/action tooling before execution.


### 2026-10-01 — Deterministic V4 Stage1 source-only packet freezes

After the fresh 2025-2026 architecture re-baseline authorized Stage1 engineering, a deterministic packet was selected from the already frozen C_F source-only manifest.

Run:
`36871466394`

Result:
**PASS**

Population:
- **128 UIDs**
- **128 distinct clusters**
- one UID per cluster

Packet SHA:
`8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1`

No proposer output, reference, gold edit, correctness score, or target family influenced selection.

**Interpretation**

Stage1 moved from design to a frozen source-only input population without increasing gold exposure.

Methodological state:
**IMPROVED**

Linguistic performance:
**NOT MEASURED**

Next:
P2_V2 and P3 source-only proposal generation on the exact frozen packet, followed by V4 legal action/dedup/diversity diagnostics.


### 2026-10-01 — P2_V2 reaches project-source Stage1 with 127/128 executable rows

Run:
`36872617551`

Result:
**SOURCE-ONLY STAGE1 COMPLETE**

Engineering observations:
- 127/128 OK (99.21875%)
- 1/128 fail-closed generation-completeness boundary
- 126/128 changed outputs (98.4375% activity; no correctness meaning)
- repeat parity 8/8
- reversed-order parity 8/8
- no empty outputs
- main pass ~9.69 min
- median ~4.54 s/case
- p95 ~5.53 s/case
- peak RSS ~2.51 GiB

The one non-executable row reached the frozen generation ceiling with EOS at the boundary. The row remains failed in V1 and may only be addressed in a future version with a preregistered length policy.

**Comparison**

Implementation/provenance readiness:
**IMPROVED**

Coverage:
high on the frozen Stage1 packet, with one explicit fail-closed edge.

Linguistic performance:
**NOT MEASURED**

New risk signal:
very high output activity (98.44%) means later safety/legal-diversity analysis is important before any correctness interpretation.

No new gold/reference was consumed.


### 2026-10-01 — P3_V1 reaches source-only Stage1 with 128/128 executable rows

Run:
`36877195995`

Engineering result:
**PASS**

- 128/128 executable
- true batch/single parity 8/8
- exact P1 parent artifact reused
- no P1 rerun
- main batched pass ~22.19 s
- peak RSS ~1.30 GiB

Stage-B activity relative to P1:
- 118/128 MIXED
- 4/128 punctuation-only
- 6/128 unchanged

The first attempt failed before inference because the new workflow did not reproduce the already-proven P1 dependency stack. This was triaged and repaired without producing P3 outputs.

**Comparison**

P3 implementation/provenance readiness:
**IMPROVED STRONGLY**

Linguistic performance:
**NOT MEASURED**

New architecture risk signal:
P3's effect is mostly mixed rather than punctuation-only, so protection and legal marginal contribution are now more important than raw distinctness.

No gold/reference was consumed.


### 2026-10-01 — V4 Stage1 protocol-complete closure

Stage1 source-only evidence is now protocol-complete.

The post-analysis audit discovered a parity-subset compliance gap:
the proposer workflows had used local 8-case parity subsets, while the frozen M02 protocol required the exact deterministic 32-UID manifest.

The gap was preserved, triaged, and remediated without regenerating proposal artifacts.

Parity32:
- P1: 32/32 PASS
- P2_V2: 32/32 PASS
- P3_V1: 32/32 PASS

Source-only legality/diversity remains:
- P1 legal 120/128; unique legal contribution 101
- P2 legal 122/128; unique legal contribution 115
- P3 legal 119/128; unique legal contribution 111
- 123/128 UIDs have a legal non-KEEP candidate
- 98/128 have all four distinct legal actions including KEEP

P3 remains a same-family SWEET extension and is mostly MIXED relative to P1, so it must not count as an independent architecture-family vote.

**Comparison vs pre-remediation Stage1**

Protocol compliance:
**IMPROVED STRONGLY**

Proposal outputs:
**UNCHANGED**

Linguistic quality:
**NOT MEASURED**

New blockers:
none for Stage1 closure.

Remaining strategic uncertainty:
whether to introduce a materially independent P4 before full-population Stage2 and future family-level consensus.

Stage2 remains unauthorized pending fresh post-Stage1 research/brainstorming.


### 2026-10-01 — Stage2 full-C_F proposer execution closes for P2_V2 and P3_V1

**P2_V2 full population**

Run `36899056538` completed successfully on all 1,918 C_F UIDs / 764 clusters using the exact production adapter under Watchdog V2.

- completed: 1918
- aborted: 0
- not attempted: 0
- completion claim: allowed
- output SHA256: `87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7`
- artifact: `11186450279`
- digest: `sha256:c5c5d32c99ce216a5b93362748cfefa67de4ec1f5b2b1174c8d3caf0fcd914af`

**P3_V1 full population**

Run `36920015935` completed successfully on all 1,918 C_F UIDs / 764 clusters using the exact production adapter under Watchdog V2.

- completed: 1918
- aborted: 0
- not attempted: 0
- completion claim: allowed
- P1 rerun: false
- exact frozen P1 parent reused: true
- Stage-B classifier: `MPSEF_STAGEB_CHANGE_DOMAIN_CLASSIFIER_V1`
- output SHA256: `02f9bd2555b1b9f350665179dcd96dd6accf532355a269b38ef4d099ea25d4ec`
- artifact: `11192760024`
- digest: `sha256:9a31de6dcff43efb903212a7fe2e2ad378f24e177faba0ecbd46ba4dd05e4253`

**Comparison**

Engineering/provenance completeness:
**IMPROVED STRONGLY**

Full-C_F proposer coverage:
**COMPLETE FOR P2 AND P3**

Linguistic correctness:
**NOT YET MEASURED**

Gold/reference exposure:
**UNCHANGED / NONE ADDED**

**Next gate**

Full-population source-only legalizer/action-set/family analysis. P1+P3 remain one SWEET family. No R_joint, learned selector, gold-aware scoring, or family-consensus activation is authorized yet.


### 2026-10-02 — Stage2 source-only protocol completion and V4 pre-gold measurement redesign

**Stage2 source-only closure**

Historical full-C_F analysis run:
- run: `36923877787`
- artifact: `11192953283`
- digest: `sha256:d773c8b65f607e06ce811d44d7e18deaf49c0da0c17428122d2258b043f82c4b`

A post-run protocol audit found output-contract gaps: the successful V1 analysis did not emit every contract-required family artifact/diagnostic under the exact required names. This was classified as an implementation/protocol-completeness defect, not a linguistic-quality failure.

Repair:
- no proposer inference rerun;
- no legalizer rerun;
- deterministic postprocessing only over exact frozen bytes;
- historical V1 run preserved unchanged.

Lock:
`phase2/redesign/MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`
commit:
`524e3e4e63bf58a3344b90b5795550f37497b3ee`

Source-only family findings:
- >=1 legal non-KEEP family: **1843/1918 = 96.09%**
- both independent families: **1736/1918 = 90.51%**
- SWEET only: **67**
- SEQ2SEQ_GED_MORPH only: **40**
- none: **75**
- exact cross-family legal non-KEEP agreement: **167 UIDs / 144 clusters**
- P3 MIXED_FROM_P1: **1800/1918 = 93.85%**
- P2 generation-completeness fail-closed: **22/1918 = 1.15%**

Interpretation:
- both independent families provide non-redundant legal source-only availability;
- P3 remains a same-family alternate, not an independent vote;
- structural availability is not correctness evidence.

**Fresh post-Stage2 research rebaseline**

Record:
`phase2/redesign/ACAD_PASS_POST_STAGE2_FRESH_RESEARCH_REBASELINE_V1.md`
commit:
`651e55c7e1726facaf5ca23d7eb918eb4ebe2d81`

Fresh evidence included:
- ACL 2025 SWEET/text-editing;
- 2025 ArbESC+ Arabic multi-system combination;
- BEA 2026 edit-level majority voting;
- AAAI 2026 JELV;
- TACL 2026 transport-based GEC evaluation;
- EACL 2026 Nahw;
- public Gemma-3-1B Arabic GEC checkpoint;
- MTAGEC.

Decisions:
- P1 KEEP;
- P2 KEEP;
- P3 KEEP as same-family alternate;
- P4 DEFER;
- Gemma checkpoint source-only probe candidate only, not gold-eligible because training provenance does not exclude QALB overlap;
- consensus DEFER;
- selector DEFER;
- generic LLM judge DEFER from primary evidence.

Critical new finding:
historical `mpsef_rjoint_score_v3.py` is incompatible with V4 because V4 can contain four literal actions and requires P1/P3 same-family semantics.

**V4 pre-gold contract**

Contract:
`phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
commit:
`2a749a5a41d5f8e8fd57b596d5c6d25a23c7f986`

A new V4 scorer was implemented source-free:
`phase2/redesign/mpsef_rjoint_score_v4.py`
commit:
`3edee5e48c96c2930246c35783312686cf894e8b`

Synthetic harness:
`phase2/redesign/mpsef_rjoint_v4_synthetic_preflight.py`
commit:
`cf55653873c561018b5e0102c582d74510cc008c`

Observable workflow commit:
`df097dffee26b155cb013206e71d6594b3734df4`

GitHub result:
**20/20 PASS**

Status:
`acad-pass/v4-rjoint-source-free-preflight = success`

Frozen source SHA256:
- scorer: `b9fdbe205e6e00082b51a7ee16c74d0010c4bbe50406ad58d2f6f9e166db7513`
- harness: `cb07b046fbd36f2afd0c27f46efd3f7561a42f2ac90b9f4ac5f477e8dd56b8b3`
- core: `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

Closure:
`phase2/redesign/MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
commit:
`0a56dc4995dc5d28be41ddcc8f30bfcfd521ba7d`

Adversarial review packet:
`phase2/redesign/ACAD_PASS_V4_RJOINT_PRE_GOLD_ADVERSARIAL_REVIEW_PACKET_V1.md`
commit:
`493b75d2a1de7aae16f6fd8d8423d8be02ea70a0`

Scientific state:
**PRE-GOLD ONLY**

No real C_F gold/reference has been loaded.
No real R_joint has been computed.
No P4, selector, consensus, or generic LLM judge has been activated.

Classification:
**IMPROVED STRONGLY IN MEASUREMENT READINESS / LINGUISTIC PERFORMANCE UNMEASURED**
### 2026-10-02 — Stage2 source-only protocol completion and V4 pre-gold scorer re-baseline

**Stage2 protocol-complete closure**

Historical Stage2 full-C_F analysis:
- run: `36923877787`
- artifact: `11192953283`
- artifact digest: `sha256:d773c8b65f607e06ce811d44d7e18deaf49c0da0c17428122d2258b043f82c4b`

A protocol audit after the successful run found missing contract outputs, including a dedicated family-summary artifact and several family-aware/cluster-level diagnostics.

Classification:
**IMPLEMENTATION/PROTOCOL GAP / NOT A SCIENTIFIC FAILURE**

Repair:
- no proposer inference rerun;
- no legalizer rerun;
- deterministic post-processing of the exact frozen artifact bytes;
- exact frozen input SHA256 identities revalidated.

Closure:
`phase2/redesign/MPSEF_V4_STAGE2_PROTOCOL_COMPLETION_V2_LOCK.md`

Full-C_F source-only evidence:
- 1,918 UIDs / 764 clusters
- >=1 legal non-KEEP family: **1,843 / 1,918 = 96.09%**
- both independent families: **1,736 / 1,918 = 90.51%**
- SWEET-only: **67**
- SEQ2SEQ_GED_MORPH-only: **40**
- none: **75**
- exact cross-family legal non-KEEP agreement: **167 UIDs / 144 clusters**

Per proposer:
- P1 executable 1,918; legal 1,806; protection-blocked 112
- P2 executable 1,896; failed 22; legal 1,790; protection-blocked 106
- P3 executable 1,918; legal 1,768; protection-blocked 150

P2 diagnostic:
- all 1,918 passed morphology/GED/GEC tokenization/interface identity stages;
- 22 failed closed at generation completeness/ceiling;
- zero zero-token, over-budget-word, unmapped-label, or GEC-input-too-long failures.

P3 Stage-B V1:
- NO_CHANGE: 61
- PUNCTUATION_ONLY: 57
- BOUNDARY_ONLY: 0
- LEXICAL_ONLY: 0
- MIXED: 1,800
- UNAVAILABLE: 0

Interpretation:
P3 is overwhelmingly a mixed same-family extension rather than punctuation-only. It is not source-only redundant, but it must never count as an independent family vote.

**Fresh post-Stage2 research re-baseline**

Frozen record:
`phase2/redesign/ACAD_PASS_POST_STAGE2_FRESH_RESEARCH_REBASELINE_V1.md`

Fresh evidence reviewed:
- ACL 2025 SWEET/text-editing;
- ArbESC+ multi-system Arabic GEC;
- BEA 2026 edit-level majority voting;
- AAAI 2026 JELV;
- TACL 2026 edit-transport evaluation;
- EACL 2026 Nahw;
- MTAGEC;
- current public Gemma-3 1B Arabic GEC checkpoint.

Decisions:
- P1 KEEP
- P2 KEEP
- P3 KEEP as same-family alternate
- P4 primary/gold-eligible DEFER
- Gemma P4 only a reserved source-only probe because training provenance does not exclude QALB overlap
- selector DEFER
- consensus DEFER
- generic LLM judge DEFER from primary evidence
- protection KEEP
- whole-action semantics KEEP

**Critical scorer incompatibility**

Historical `mpsef_rjoint_score_v3.py` was found incompatible with V4:
- V3 groups P1/P2/PAIR only;
- V3 expects <=3 actions;
- V4 supports KEEP+P1+P2+P3 = 4 actions;
- V4 requires P1+P3 family aggregation without double counting.

Scientific consequence:
**DO NOT RUN V3 DIRECTLY ON V4**

**V4 pre-gold contract**

`phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
commit:
`2a749a5a41d5f8e8fd57b596d5c6d25a23c7f986`

**R_joint V4 source-free implementation**

Scorer:
`phase2/redesign/mpsef_rjoint_score_v4.py`
commit:
`3edee5e48c96c2930246c35783312686cf894e8b`

Synthetic harness:
`phase2/redesign/mpsef_rjoint_v4_synthetic_preflight.py`
commit:
`cf55653873c561018b5e0102c582d74510cc008c`

Final observable workflow commit:
`5c280d4cc6abda3e1f5f21c0fbcb6e79c2d6df2d`

GitHub status:
**SUCCESS**

Synthetic:
- 20/20 PASS
- M04 retained
- M05 retained
- max 4 actions supported
- proposer isolation PASS
- P1/P3 same-family semantics PASS
- cross-family provenance PASS
- ROSTER whole-action/no-fusion PASS
- punctuation separation PASS
- scorer-failure preservation PASS
- source/action identity fail-closed PASS

Frozen SHA256:
- scorer: `b9fdbe205e6e00082b51a7ee16c74d0010c4bbe50406ad58d2f6f9e166db7513`
- synthetic test source: `cb07b046fbd36f2afd0c27f46efd3f7561a42f2ac90b9f4ac5f477e8dd56b8b3`
- synthetic result: `4eb8c2510fd62b50ff3a557018bc58d52853e53e4625389572308e62b39585d2`
- core: `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

Closure lock:
`phase2/redesign/MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
final lock commit:
`544e4059af4fd891c504492faf2b876bad8fca76`

Classification:
**IMPROVED STRONGLY IN MEASUREMENT READINESS / LINGUISTIC PERFORMANCE UNMEASURED**

Next:
independent/higher-model adversarial review before any C_F gold/reference load.
### 2026-10-02 — V4 pre-gold adversarial review packet frozen

Frozen packet:
`phase2/redesign/ACAD_PASS_V4_PRE_GOLD_HIGHER_MODEL_REVIEW_PACKET_V1.md`

Commit:
`8e1257c037c196c67feabcc82f238ae31a4e29e1`

Purpose:
obtain an independent/higher-model verdict on V4 denominator freezing, provenance/family semantics, M04/M05, punctuation treatment, reference incompleteness, historical C_F exposure, action-set identity, and hidden leakage paths before any gold-aware execution.

Review contract:
- verdict must be PROCEED / MODIFY / BLOCK;
- 30 mandatory questions;
- explicit gold-authorization decision;
- no performance estimation;
- no gate weakening;
- no opening of confirmation/holdout/internal/stress populations.

Current state:
no independent higher-model endpoint is available in the present toolset, so no review result has been claimed or fabricated.

Scientific consequence:
**REAL C_F GOLD LOAD AND REAL R_joint V4 REMAIN BLOCKED PENDING INDEPENDENT REVIEW RESOLUTION.**

Classification:
**MEASUREMENT READINESS IMPROVED / REVIEW GATE OPEN / LINGUISTIC PERFORMANCE UNMEASURED**


### 2026-10-02 — V4 R_joint adversarial review, A1 repair, and hardened V4.2 verification pending

**Internal adversarial review**

Record:
`phase2/redesign/ACAD_PASS_V4_RJOINT_INTERNAL_ADVERSARIAL_REVIEW_V1.md`
commit:
`0bb90f26f745a77c2f3334789581c8f2e817c1af`

Verdict:
**MODIFY BEFORE GOLD**

Findings:
- BLOCKER: 0
- MAJOR: 4
- MINOR: 3

Major findings:
1. V4 population scorer did not yet emit the composite M05 BOUNDARY={SPLIT,MERGE} route/additional-target/additional-cluster evidence.
2. Primary-only gold scoring could count a correct reference-supported punctuation repair as an extra edit.
3. A production measurement identity-lock wrapper was not yet frozen.
4. The historical 95% candidate-availability gate was underspecified in V4.

No project gold/reference was opened during review.

**Contract amendment**

`phase2/redesign/MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1_AMENDMENT_A1.md`
commit:
`cae6c3f95e9ffdad9f7e550aa41d971f5541ff41`

A1 freezes:
- full-reference action scoring;
- projection to primary vs punctuation targets;
- PRIMARY_RECOVERY;
- PRIMARY_CLEAN_RECOVERY;
- PRIMARY_COMPLETE_REPAIR;
- ALL_REFERENCE_COMPLETE_REPAIR;
- mutually exclusive sentence reference states;
- M05 composite BOUNDARY and INSERT routes;
- family additional-target/cluster evidence;
- historical 95% ROSTER primary candidate-availability gate;
- production input-lock identity requirements.

**V4.1 repair**

Scorer:
`mpsef_rjoint_score_v4_1.py`
commit:
`61a810e3c1ae443e0671fb150c83374d2c981869`

Expanded synthetic harness:
27 cases
commit:
`4fdaafd894f3e80eec5e39901a46b7da80d05fc3`

Workflow:
`31242b687015df9c2220e68c7ae2c87cc8548d58`

Result:
**SUCCESS**

This established that the A1 construct repairs were executable source-free.

**Additional pre-closure hardening**

A second guard review found that the scorer should fail closed on malformed action sets even though the frozen Stage2 artifact itself is already deduplicated.

New requirements:
- duplicate literal output -> fail;
- non-KEEP output equal to source/KEEP -> fail;
- output SHA mismatch -> fail;
- KEEP/source SHA mismatch -> fail.

This is defensive measurement hardening, not a linguistic/model-quality change.

**V4.2**

Scorer:
`phase2/redesign/mpsef_rjoint_score_v4_2.py`

Commits:
- `6e278abbe0431043ee74e2bac4c1f6ed649f4005`
- `f5e50f2f9e3371ab7ea7f294cc1b3b499b1f4e63`

31-case harness:
`phase2/redesign/mpsef_rjoint_v4_2_synthetic_preflight.py`
commit:
`3559c73d0014f314806d2613163e3e7f536d026b`

Initial workflow commit:
`710920fd7426aa6c7aa2cfa330012fb695623459`

Observed:
- outer preflight status: FAILURE;
- scorer/test/core/result hash status publication succeeded.

Failure was preserved; no immediate rerun/repair was performed.

Diagnostic rerun:
`8654902115d3036f7a391e3a11fb8097c91e8cce`

Observed:
- diagnostic summary status appeared;
- no test-specific failure contexts were exposed.

Interpretation:
possible workflow/observability failure rather than proven scorer/test failure, but connector evidence was insufficient to conclude PASS.

A minimal unchanged verification-only workflow was therefore frozen:
commit:
`2481dcb8b2160a47d017a3a9a0409437bdb9f331`

It publishes `acad-pass/v4-2-rjoint-31of31=success` only after exact 31/31 validation.

Three polls in the current execution turn exposed no status, so polling stopped under the permanent max-3 rule.

Diagnostic lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_PREFLIGHT_ATTEMPT_DIAGNOSTIC_LOCK_V1.md`
commit:
`05f1fec3345c0c8100a2044b6cde67e2e9ea5f73`

**Current scientific classification**

**MIXED / METHODOLOGICAL HARDENING IMPROVED / CLOSURE PENDING**

Performance:
**UNMEASURED**

Gold exposure:
**UNCHANGED / NO NEW GOLD**

Next:
check only the minimal verification commit in a new continuation turn; do not alter scorer/harness until its result is known.
### 2026-10-02 — V4.2 delta-review remediation and B02 production hardening

Independent delta-review verdict:
`MODIFY`

No new BLOCKER/MAJOR finding was reported.

Historical finding state at review:
- B01 CLOSED
- B02 PARTIAL
- M01-M05 CLOSED
- N01-N02 CLOSED

Mandatory pre-gold repairs were executed without opening project gold.

Scorer repairs:
- T20 external-source-identity regression repaired;
- T24 now exercises true SPLIT+MERGE;
- identity contract is enforced before target construction;
- incomplete identity contracts fail closed;
- progress callback added for observable long-running production scoring.

Verification:
- V4.2 scorer source-free preflight: **33/33 PASS**
- V4.2 production-wrapper source-free preflight: **14/14 PASS**
- combined status: `acad-pass/v4-2-pre-gold-wrapper = success`

Production wrapper:
`phase2/redesign/mpsef_rjoint_v4_2_production_wrapper_v1.py`

Production input lock:
`phase2/redesign/MPSEF_RJOINT_V4_2_PRODUCTION_INPUT_LOCK_V1.json`

Pre-gold closure:
`phase2/redesign/MPSEF_RJOINT_V4_2_PRE_GOLD_CLOSURE_LOCK_V1.md`

Frozen implementation SHA256:
- scorer: `be9cf725b71b8d26a23eff9e9afd4ca434294a4d8f72e0271caa179ca892f2e1`
- core: `b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`
- wrapper: `72bf23c9f910c2b203caf11e6e677729fa914d66c2d1e062ac0fd7dfd6da357f`
- dependency lock: `aa66ec3d6fdb4aef1b4fada26a1b6cf794f632139655e22462a7a1c27aab7bc5`

Full-C_F identity:
- 1,918 UIDs / 764 clusters
- source SHA256: `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- action-set SHA256: `e38393abb36734d3882e29a78f3b33c80718791957b9b8c0c6e8a8ab77f6e138`
- UID SHA256: `51e2e1decf1c7c9efbc31e343eba1c7dfb08d0de314041cb57f5b3118ffd550f`
- cluster SHA256: `bb2f49c6aaf312cf9c388237090a79861fa6218da15de57d0119efd39327ae3c`
- UID-cluster map SHA256: `32b89f9dcadefa0f17cb0fddac6099433d611508a01ad96b428e0534c1057c5d`
- provenance signature map SHA256: `18561c75c397821c34e3dc06214bb4f64cc5ff8d6757f61835cbe9e6808befbd`

Gold identity remained historical/frozen only:
`971b6fbb28dc3767193e7a4b0f722c3abebfc8600155a57093ba483dac6491e8`

No gold content was newly opened and no real R_joint was computed.

Current authorization state:
exact input-lock SHA publication workflow committed at
`c49d572f82e3939ad4461ad0b78ff45655d2ac7b`.

After three sequential status checks, the SHA context was not yet exposed, so polling stopped per protocol.

Next:
capture the exact input-lock SHA, bind it into a separate single-run authorization record, validate that record, then and only then permit one DEVELOPMENT-only R_joint V4.2 run.

Classification:
**IMPROVED STRONGLY / B02 IMPLEMENTATION HARDENED / AUTHORIZATION BINDING PENDING**
### 2026-10-02 — Exact-SHA V4.2 authorization validated and one-shot DEVELOPMENT measurement started

Input-lock SHA256:
`3f3e4bd95bbd5d49ad71ec58466573d56a476eefcf0cdc3719c2c732d3de19d0`

Authorization record:
`phase2/redesign/MPSEF_RJOINT_V4_2_SINGLE_RUN_AUTHORIZATION_V1.json`

Authorization SHA256:
`c9adda76ace40df378ab4c88f193160e1edbdd6256f079e87ee4d2e185008993`

Authorization validation:
`acad-pass/v4-2-authorization-valid = success`

Authorized one-shot workflow:
`.github/workflows/phase2-mpsef-v4-2-development-rjoint-one-shot.yml`

Trigger commit:
`f84c94527df487dc0426165737450471d6da3fa4`

Observed run:
`36938833412`

Observed after three sequential checks:
`acad-pass/mpsef-rjoint-v4-2-progress = pending`

The progress context is created only after:
- exact authorization/input-lock/code identity validation;
- source-free 47/47 regression verification on the production runner;
- full 1,918-row source/action identity and provenance verification;
- durable single-run consumption claim;
- post-claim CALIBRATION/gold identity verification;
- entry into the scoring watchdog.

No fourth poll was performed.

Scientific boundary while run is active:
- result not yet interpreted;
- no selector;
- no family consensus;
- no P4;
- no LLM judge;
- no internal evaluation;
- no stress diagnostic;
- no reserved population.

Single-run authorization must now be treated as consumed once its durable claim step has executed. Any future retry after failure requires an explicit documented stop-rule decision and a new authorization record.

Classification:
**IMPROVED STRONGLY / AUTHORIZATION CLOSED PASS / DEVELOPMENT R_JOINT V4.2 IN PROGRESS**
### 2026-10-02 — Runtime dependency identity hardening before gold

A final pre-execution red-team review discovered that the V4.2 production wrapper froze the dependency-lock file identity but did not independently assert the actual installed numpy/editdistance versions.

This was treated as a real B02 reproducibility gap.

Hardening:
- production wrapper validates dependency-lock fields;
- actual Python major/minor is checked;
- actual Arabic-GEC revision is checked;
- actual numpy version is checked;
- actual editdistance version is checked;
- network-download-during-measurement policy must equal `forbidden`;
- model-inference-during-measurement policy must equal `forbidden`;
- runtime dependency identity is embedded in measurement output.

Wrapper preflight expanded:
- prior: 14/14;
- new required suite: 16/16;
- new rejects:
  - package-version mismatch;
  - runtime-policy mismatch.

Updated combined pre-gold workflow:
`f7353bd2693654a78d49a353ba04485683e79f45`

After three sequential status inspections, no status had yet been exposed; polling stopped per protocol.

Because runtime-verifying wrapper identity changed after the prior authorization:
- prior authorization SHA256 `5bb5727e6fea6d7b89e0180656660713ee1d301f1dcf4134755d47385d1cfc28` was explicitly superseded/fail-closed;
- prior input-lock SHA256 `3f3e4bd95bbd5d49ad71ec58466573d56a476eefcf0cdc3719c2c732d3de19d0` was explicitly superseded pending re-freeze.

Fail-close commits:
- authorization: `75b8afcb65831d41ff3e4642c5af708c4a58bf14`
- input lock: `ec3e7793a9c4286d3928ebeacc8d6269f3bdf7e9`

Verified one-shot consumption guard remains:
- SHA256 `895128860ba4e03f287b91c56d3505f5df5a9c31292a5555088654aedd468070`
- no consumption claim issued yet.

No project gold/reference was newly opened.
No real R_joint was computed.

Classification:
**MIXED / REPRODUCIBILITY IMPROVED / AUTHORIZATION TEMPORARILY ROLLED BACK FAIL-CLOSED**
### 2026-10-02 — Additional pre-gold runtime identity hardening

A final pre-gold adversarial check found that the V4.2 production wrapper was verifying the dependency-lock file identity but not the actually installed package versions.

Hardening applied before any gold access:
- enforce dependency-lock contents at runtime;
- require Python 3.10;
- require frozen Arabic-GEC revision;
- require numpy 1.23.5;
- require editdistance 0.6.2;
- enforce no network download during measurement;
- enforce no model inference during measurement.

Wrapper preflight expanded:
14 tests → 16 tests.

New negative tests:
- reject mismatched runtime package version;
- reject weakened runtime policy.

Code commits:
- wrapper hardening: `07bed9062757e96ce40c531e772f18d70ffe8303`
- preflight extension: `d5543b72d139248423bfbf94a905ee02d1d8dbc4`
- exact-dependency verification workflow: `500b176475b60ab5207c6715fa28e2c84f76c70e`

After three status checks, no workflow status was yet exposed, so polling stopped according to protocol.

Effect on previous authorization:
the old wrapper/input-lock/authorization identities are superseded and MUST NOT authorize gold access until the new wrapper preflight passes and all dependent hashes are regenerated.

Scientific boundary unchanged:
- gold newly opened: false
- real R_joint computed: false
- selector/consensus/P4/LLM judge: false

Classification:
**IMPROVED IN PRE-GOLD REPRODUCIBILITY HARDENING / AUTHORIZATION TEMPORARILY RE-LOCKED PENDING 16/16 VERIFICATION**
### 2026-10-02 — Runtime preflight bookkeeping defect isolated and repaired

The exact-runtime V4.2 verification run at commit
`500b176475b60ab5207c6715fa28e2c84f76c70e`
failed only at the 16-case wrapper preflight step.

Run:
`36939409747`

All of the following passed:
- exact dependency installation;
- compilation;
- scorer preflight 33/33;
- SHA publication.

Root cause:
W15 and W16 were accidentally duplicated in the source-free harness, producing 18 test records while the pass condition correctly required 16. This was a harness accounting defect, not a production-semantic failure.

Repair:
duplicate test block removed with no scorer/wrapper semantic change.

Repair commit:
`45187205641612d867a8547305fc37688493eded`

After three sequential status inspections, the repair-run status was not yet exposed; polling stopped per protocol.

Scientific boundary unchanged:
- new gold access: false
- real R_joint: false
- selector/consensus/P4/LLM judge: false

Classification:
**MIXED TEMPORARILY / ROOT CAUSE IDENTIFIED / NO SCIENTIFIC REGRESSION / REPAIRED VERIFICATION PENDING**
### 2026-10-02 — Exact-runtime V4.2 verification closed PASS; dormant one-shot path frozen

The repaired exact-runtime verification completed successfully:
- commit `705129dc9f319d835321a47a2530d48bd18ac468`
- run `36940030184`
- scorer: **33/33 PASS**
- wrapper/runtime: **16/16 PASS**
- artifact `11199084513`
- digest `sha256:5f16c02fdbe8612499c24b6b2209a19ee03f6738d529e78b10f545fe7c430b20`

Production input lock refreshed:
`f3f40b1425e272f27d2e19a41f45792310102ad7a62ef9037e78868430517ff3`

Dormant one-shot measurement workflow frozen:
`7ad25c7207700cca202b3a2727200c7a1d59c409c9ec57bfe013865d63d3f3d8`

Authorization refreshed:
`a91b25d68b2b2fb80e32326e614853026e6b90d1ce3dac4cc00f571be1425ce3`

Verified one-shot consumption guard remains:
`895128860ba4e03f287b91c56d3505f5df5a9c31292a5555088654aedd468070`

Final authorization validation launched at commit:
`8aba3486fc85c473e0c67ef4333f5ab4a8c305e8`

No validation status was exposed within the bounded three-check window, so activation was intentionally NOT created.

A non-triggering activation template was prepared at:
`phase2/redesign/MPSEF_RJOINT_V4_2_EXECUTION_ACTIVATION_V1_TEMPLATE.json`

Scientific boundary remains intact:
- new gold access: false
- real R_joint: false
- selector/consensus/P4/LLM judge: false

Classification:
**IMPROVED STRONGLY / EXACT-RUNTIME PRE-GOLD GATE CLOSED / FINAL AUTHORIZATION VALIDATION PENDING**
### 2026-10-02 — V4.2 one-shot DEVELOPMENT measurement activated

Exact-runtime pre-gold verification closed:
- scorer: 33/33 PASS
- production wrapper: 16/16 PASS
- successful verification run: 36940030184
- artifact: 11199084513
- artifact digest: sha256:5f16c02fdbe8612499c24b6b2209a19ee03f6738d529e78b10f545fe7c430b20

Refrozen input lock SHA256:
`6ac8656226c64b64e8fc6a408475dbff1e231ec3d87b7afa3da464b1dee25132`

Replacement authorization validated:
- validation commit: `679e0d73ea3f1ce936911c4b74eae3d6ead56363`
- authorization SHA256:
  `7b8a4ebd8216bd2fd06c42d919bbe16d219b6cbc0b46cfad07f286f08651fb49`

Activation commit:
`eabbd984744d3c5551e19b537d2b5b89d9cb5d8a`

One-shot workflow run:
`36940844664`

Last observed state:
- IN_PROGRESS
- activation/identity/code-checkout gates all PASS
- runtime dependency installation in progress
- consumption claim not yet observed
- gold access not yet evidenced
- real R_joint not yet observed

Polling stopped after the third sequential inspection according to protocol.

Classification:
**IMPROVED STRONGLY / PRE-GOLD GATES CLOSED / ONE-SHOT RUN ACTIVATED / METRIC RESULT PENDING OBSERVATION**
### 2026-10-02 — V4.2 DEVELOPMENT run consumed and actively measuring R_joint

Run:
`36940844664`

Consumption claim:
`acad-pass/v4-2-rjoint-consumed = success`

Gold boundary state:
- crossed lawfully after successful durable consumption claim;
- CALIBRATION download PASS;
- official M2 gold download PASS;
- post-claim gold identity verification PASS.

Current active step:
`Run one-shot DEVELOPMENT-only R_joint V4.2`

No completed metric has yet been observed.

Consequence:
this experiment is now consumed. Any future technical rerun after failure requires explicit stop-rule handling and a new documented authorization decision; silent rerun is forbidden.

Classification:
**IMPROVED / AUTHORIZED GOLD BOUNDARY CROSSED / REAL R_JOINT IN PROGRESS / RESULT NOT YET AVAILABLE**
