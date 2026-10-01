# ACAD_PASS ARCHITECTURE RE-BASELINE V1

Date: 2026-10-01
Status: PRE-MEASUREMENT ARCHITECTURE REVIEW
Measurement authorization: NO
Project gold use in this review: NONE

## 1. Why this re-baseline is mandatory

The current corrected cycle achieved 22/22 Second Preflight PASS on the hardened codebase, but the frozen executable-action space remains structurally asymmetric:

- P1 executable: 1,806 / 1,918 = 94.16%
- P1 protected-blocked: 112 / 1,918 = 5.84%
- P2 executable: 0 / 1,918
- P2 execution-failed: 1,918 / 1,918 = 100%

The P2 failure is a provenance/implementation defect, not a demonstrated linguistic-quality failure.

Because measurement exposure is valuable and the project objective is maximum final-system quality rather than preservation of the current architecture, a fresh architecture decision is required BEFORE any new gold-aware R_joint run.

## 2. Current evidence base

### 2.1 P1 / text-editing route

The current H1/P1 route is based on CAMeL-Lab text-editing.

Recent external evidence (ACL 2025) reports that Arabic text-editing:
- derives edit tags directly from data rather than language-specific hand-coded edit sets;
- achieves state-of-the-art results on two Arabic GEC benchmarks and parity with SOTA on two others;
- is reported to be more than six times faster than earlier Arabic GEC systems;
- supports ensemble combinations.

Engineering interpretation:
P1 remains a strong component worth retaining unless new direct evidence contradicts this.

### 2.2 P2 / older GED-conditioned seq2seq route

The frozen P2 route is based on the earlier CAMeL-Lab Arabic-GEC stack.

Current-cycle source-only audit proved a universal GED word/subword provenance defect:
- 1,918/1,918 mismatch;
- 30,341 GED predictions dropped by frozen zip semantics;
- 1,918/1,918 frozen outputs reproducible exactly;
- 24 generation-ceiling cases;
- 0 missing terminal EOS cases.

Engineering interpretation:
the frozen implementation is unusable in the current cycle, but the underlying architecture is not scientifically disproven.

### 2.3 Newer seq2seq evidence

A 2025 open-access study evaluated pretrained seq2seq transformers including:
- AraT5;
- AraBART;
- mT5;
- mBART.

It reports strong Arabic GEC performance and argues that pretrained seq2seq models are useful under limited parallel-data conditions.

Engineering interpretation:
if ACAD_PASS needs a generative complement to P1, it is not necessary to assume the old P2 stack is the only candidate.

### 2.4 Multi-system combination evidence

Recent Arabic GEC work on system combination reports benefits from combining heterogeneous systems including:
- AraT5;
- ByT5;
- mT5;
- AraBART;
- morphology-enhanced variants;
- text-editing.

Engineering interpretation:
the next architecture should explicitly test complementarity, not merely replace one proposer with another by intuition.

### 2.5 2026 benchmark/explanation evidence

Recent Arabic resources such as Nahw and ArabiGEE indicate continued gaps in Arabic grammatical competence and increasingly structured evaluation/explanation taxonomies.

Engineering interpretation:
future ACAD_PASS research should consider structured error-type/explanation evidence and independent benchmark use, while preserving current closed/reserved-set rules.

## 3. Candidate architecture options

### Option A — KEEP CURRENT P1-ONLY PRIMARY ARCHITECTURE

Description:
Use KEEP + current frozen executable P1 only.

Benefits:
- highest provenance maturity;
- already preflighted;
- simple;
- fast;
- no new proposer implementation risk.

Risks:
- candidate-availability ceiling may be limited;
- no heterogeneous complementary proposer;
- may under-cover families P1 does not handle.

Current assessment:
SAFE BASELINE, but not preferred as the final maximum-quality architecture without comparison.

### Option B — REPAIR OLD P2 AS P2_V2

Description:
Retain the earlier GED-conditioned Arabic-GEC architecture but implement correct wordpiece-to-word GED alignment and complete provenance tracing.

Mandatory repair requirements:
1. explicit first-wordpiece word alignment;
2. no silent zip truncation;
3. exact word coverage assertions;
4. fail closed on unmapped words;
5. GED/GEC input-length and truncation tracing;
6. decoder start/EOS/PAD/max-length evidence;
7. regression tests for split-word tokenization;
8. source-only reproducibility before any gold-aware evaluation.

Benefits:
- preserves a known heterogeneous generative architecture;
- root cause is highly repairable at implementation level;
- existing runtime/reproducibility knowledge can be reused.

Risks:
- old architecture may no longer be the strongest generative complement;
- fixing provenance does not guarantee complementary linguistic coverage;
- retracing an older stack has maintenance cost.

Current assessment:
VIABLE, but must compete against newer complements.

### Option C — REPLACE P2 WITH A MODERN PRETRAINED SEQ2SEQ COMPLEMENT

Candidate families:
- AraT5;
- AraBART;
- mT5;
- mBART;
- other reproducible Arabic-capable encoder-decoder models with stable checkpoints.

Selection criteria:
- public reproducible checkpoint;
- deterministic/frozen inference path;
- Arabic GEC evidence;
- source-only traceability;
- complementary output diversity relative to P1;
- manageable latency/memory;
- exact truncation/EOS provenance;
- compatibility with protected-invariant legalizer.

Benefits:
- may provide stronger generative coverage than repaired historical P2;
- naturally heterogeneous relative to text-editing P1.

Risks:
- larger output space may increase unsafe edits;
- stronger protection/legalization burden;
- runtime cost.

Current assessment:
HIGH-PRIORITY ALTERNATIVE.

### Option D — ADD A COMPLEMENTARY PROPOSER RATHER THAN REPLACE P2

Description:
Keep P1 and optionally repaired P2, but add one carefully selected complementary model.

Benefits:
- explicitly targets candidate availability;
- aligns with recent ensemble evidence;
- allows leave-one-out complementarity analysis.

Risks:
- more hypotheses per sentence;
- larger legality/scoring workload;
- increased chance of unsafe proposals;
- must retain whole-action primary semantics unless contract is explicitly versioned.

Current assessment:
HIGH POTENTIAL, but requires strict source-only pruning/legalization.

### Option E — MULTI-SYSTEM EDIT-SELECTION / ENSEMBLE ARCHITECTURE

Description:
Use multiple proposers but perform selection/combination only through a separately validated architecture.

Important constraint:
the current primary MP-SEF contract forbids edit-level hybrid fusion.

Therefore any edit-level combination would require:
- a new versioned architecture;
- a new contract;
- fresh preflight;
- new source-only legality proof;
- no retroactive modification of current evidence.

Benefits:
- recent Arabic work suggests system combination can improve correction performance.

Risks:
- high methodological complexity;
- edit-level fusion can violate protected invariants or create unseen outputs;
- risks contaminating the clean whole-action provenance design.

Current assessment:
RESEARCH-INTERESTING, but NOT the first next implementation.

## 4. Re-baseline decision matrix

### KEEP
Current P1/text-editing:
KEEP as a mandatory baseline and likely primary proposer.

### REPAIR
Historical P2:
REPAIR only as a versioned P2_V2 candidate, not as an assumed final solution.

### REPLACE
P2:
Actively evaluate modern seq2seq replacement candidates.

### ADD
Complementary proposer:
Strongly consider one additional heterogeneous proposer if it demonstrates source-only complementarity.

### REMOVE
Current frozen P2:
REMOVE from current executable architecture only; preserve frozen artifact historically.

## 5. Recommended source-only experimental order

No project gold is used in these steps.

### R0 — inventory and reproducibility screen

For each candidate proposer:
- exact model/revision/license;
- runtime requirements;
- deterministic inference;
- truncation behavior;
- EOS/PAD/decoder metadata;
- output identity hashing;
- protected-touch diagnostics;
- latency/memory;
- public reproducibility evidence.

Reject candidates that cannot be frozen/reproduced.

### R1 — source-only complementarity screen

On an allowed development-source population without reference scoring, measure:
- changed-output rate;
- exact-output duplication with P1;
- unique whole-output rate;
- protected-touch rate;
- empty/failure rate;
- truncation rate;
- output length anomalies;
- runtime;
- morphological/orthographic surface diversity diagnostics.

This does NOT establish linguistic quality.

### R2 — legality screen

Run every candidate through the gold-blind legalizer.

Measure:
- executable fraction;
- blocked fraction by reason;
- provenance failures;
- protection failures;
- truncation failures;
- duplicate whole actions after exact-text deduplication.

### R3 — independent architecture review

Before any new gold-aware measurement:
- compare P1-only;
- P1 + repaired P2_V2;
- P1 + modern seq2seq candidate;
- P1 + selected complementary proposer;
- justify why the chosen action space is strongest.

### R4 — freeze one architecture

Only one architecture is frozen for the next authorized metric exposure.

No post-metric candidate shopping is allowed within that cycle.

## 6. Current provisional recommendation

Do NOT immediately authorize R_joint on the current P1-only effective action space.

Retain P1.

Prepare two competing source-only complementary paths:

1. P2_V2 repaired alignment implementation;
2. one modern pretrained seq2seq complement selected by reproducibility and Arabic-GEC evidence.

Compare them source-only first.

If one clearly dominates on provenance, legality, complementarity, and operational cost, freeze that architecture.

If neither adds meaningful executable diversity safely, return to P1-only and authorize measurement with that limitation explicitly documented.

## 7. Higher-model consultation

Independent higher-model review is now recommended BEFORE choosing the final complementary architecture.

The review should receive:
- the full system evolution ledger;
- current 22/22 Second Preflight PASS;
- P2 root-cause/repairability record;
- this re-baseline document;
- frozen P1/P2/action hashes;
- recent Arabic GEC literature options;
- explicit question: KEEP P1-only vs REPAIR P2_V2 vs REPLACE/ADD modern complement.

## 8. Scientific status

Current classification:

IMPROVED STRONGLY IN METHODOLOGICAL READINESS / ARCHITECTURE RE-BASELINE REQUIRED BEFORE PERFORMANCE MEASUREMENT

No new project quality metric has been computed in this re-baseline.

