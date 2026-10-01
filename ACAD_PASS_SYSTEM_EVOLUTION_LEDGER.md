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
