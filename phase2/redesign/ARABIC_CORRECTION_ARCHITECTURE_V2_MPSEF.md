# ACAD_PASS Arabic Correction Architecture v2
## Multi-Proposer Selective Edit Fusion (MP-SEF)

Date: 2026-09-30
Status: ARCHITECTURE DECISION — FROZEN BEFORE IMPLEMENTATION
Scope: Phase 2 Arabic correction redesign after closure of M2-H
Previous path: M2-H CLOSED before H5/H6

## 1. Why a new architecture is justified

The previous M2-H path is closed because its frozen one-pass H1 candidate generator achieved only 69.39% official-alignment NoPnx M2 recall against a preregistered >=80% feasibility gate.

The redesign must not tune H1-v1, weaken its gate, or reopen closed H2/H3/H4 components.

The new design is based on five established observations:

1. A single candidate generator is a recall bottleneck.
2. Sequence-to-sequence Arabic GEC models provide strong contextual coverage but cannot be trusted as direct document rewriters in ACAD_PASS because they may alter arbitrary text.
3. Edit-tagging systems provide locality and speed but can miss corrections, especially under a single-pass constraint.
4. Modern Arabic GEC literature increasingly benefits from system combination / edit selection rather than a single model.
5. ACAD_PASS values scientific fidelity, reversibility, protected invariants, and REVIEW-first operation more than benchmark-only full-sentence correction.

## 2. Design principle

Separate:

**proposal generation**

from

**edit authorization**

No neural generator is allowed to directly rewrite the user document.

Every model output must first be converted back into reversible, source-anchored candidate edit transactions.

## 3. Architecture overview

### Layer A — Source and invariant lock

Before any GEC model runs:

- freeze exact source text and token/character offsets;
- identify protected spans:
  - numbers;
  - units;
  - equations;
  - citations;
  - URLs;
  - emails;
  - Latin/code fragments;
  - proper names when confidently detected;
  - document structural markers;
- store immutable hashes for source and protected-span map.

Protected content may be used as context but cannot be automatically changed.

### Layer B — Heterogeneous proposer pool

Initial v2 feasibility pool may contain only reproducible public components whose model identity can be frozen.

#### P1 — SWEET iterative proposer

Use the public QALB14 NoPnx text-editing model in its documented iterative mode.

Purpose:
- local edit proposals;
- high speed;
- explicit edit trajectory.

Important:
this is NOT H1-v1.
H1-v1 remains CLOSED FAIL.
P1 belongs to a new architecture and must receive a new frozen identity and protocol.

Punctuation remains a separate proposer/process.

#### P2 — AraBART + Morph + GED proposer

Use the public CAMeL-Lab QALB14 AraBART GEC model with:
- contextual morphological preprocessing;
- its paired CAMeLBERT GED model;
- frozen model revisions;
- deterministic inference configuration.

Purpose:
- contextual seq2seq proposal coverage;
- GED error-type information as auxiliary evidence;
- diversity relative to edit tagging.

#### P3 — Cross-domain AraBART proposer candidate

The public ZAEBUC AraBART+GED model may be evaluated as an optional diversity proposer only after:
- model revision and preprocessing are frozen;
- marginal candidate-recall contribution is measured;
- domain mismatch risk is recorded.

Do not retain it merely to increase proposer count.

#### Conditional research proposers

MTAGEC:
- code and large synthetic dataset are public;
- current repository requires local training rather than providing a clearly packaged final checkpoint;
- therefore it is NOT an initial required proposer;
- may later contribute error type/evidence/explanation if a reproducible checkpoint is established.

STAGEET:
- promising 2026 staged typed edit-tagging architecture;
- public paper evidence is recent;
- original reproducible code/weights were not established in the current audit;
- therefore it is research-track only until reproducibility is demonstrated.

Generic LLMs:
- never automatic authorizers;
- REVIEW/diagnostic only in v2.

## 4. Canonical edit transaction layer

Every proposer output is converted to a common transaction:

- transaction_id
- proposer_id
- source_start_char
- source_end_char
- source_text
- replacement_text
- normalized_source
- normalized_replacement
- operation_family
- punctuation_only
- protected_span_overlap
- proposer_trace
- reversible_inverse
- alignment_confidence/status

The transaction representation must be invariant to proposer-specific edit decomposition.

Candidate equivalence is defined by applying the edit to the original source, not by requiring identical internal tag sequences.

## 5. Candidate union and conflict graph

Construct the union of all source-anchored candidate edits.

For each canonical candidate record:

- supporting proposers;
- proposer diversity count;
- identical replacement agreement;
- competing replacement set;
- overlapping-edit conflict edges;
- nested/conflicting span relationships;
- operation family;
- whether candidate is isolated or conflict-dependent.

A proposer can improve recall without being trusted to authorize its own candidate.

## 6. Independent evidence layer

The decision layer may use evidence but must distinguish proposal evidence from safety evidence.

Allowed candidate features may include:

### Agreement evidence
- number of agreeing proposers;
- number of architecturally distinct agreeing proposer families;
- exact replacement consensus;
- conflict count.

### GED evidence
- token-level error presence;
- error category;
- localized GED confidence;
- consistency between GED location and proposed edit span.

GED confidence alone is not approval.

### Morphological evidence
- contextual analyses;
- lemma/POS/feature consistency;
- agreement features;
- segmentation legality;
- candidate/source feature deltas.

Prior H2/H3 results establish that analyzability alone is insufficient.

### Structural evidence
- exact character preservation for whitespace-only boundary edits;
- deterministic protected-span preservation;
- operation-specific invariants.

Prior H4 shows structural invariants can be highly safe even when coverage is low.

### Proposal-model scores
May be included only as weak/calibration features.
A model's confidence in its own proposal is not independent safety evidence.

### Semantic/factual risk features
- protected entity/number/unit/citation overlap;
- lexical substitution magnitude;
- named-entity change;
- content-word deletion/insertion;
- cross-script changes;
- high semantic-drift risk.

These features may veto automation even when multiple proposers agree.

## 7. Decision dispositions

Every canonical candidate must end in exactly one state:

- AUTO_SAFE
- REVIEW_RECOMMENDED
- CONFLICT_REVIEW
- REJECTED
- UNSUPPORTED

Default is not AUTO_SAFE.

## 8. Sentence/document completion logic

A sentence is not automatically declared clean merely because no AUTO_SAFE edit remains.

Escalate to REVIEW when any of the following holds:

- unresolved high-confidence GED error;
- conflicting proposer corrections;
- unsupported proposal touching meaningful content;
- protected-span risk;
- candidate coverage uncertainty;
- residual proposer disagreement;
- semantic-drift risk.

This preserves the REVIEW-first Arabic policy.

## 9. First feasibility experiment — candidate generation only

Before building any selector, verifier, or fusion classifier:

1. freeze P1 and P2 exact model/revision/inference identities;
2. run both on CALIBRATION only;
3. convert outputs to canonical representation-invariant edits;
4. measure:
   - each proposer recall;
   - union recall;
   - marginal recall gain;
   - operation-family recall;
   - exact sentence coverage;
   - conflict rate;
   - protected-span proposal rate;
   - candidate volume per sentence;
5. do NOT fit an authorization model yet.

### Candidate-union feasibility gate

Proceed to selector design only if:

- representation-invariant candidate-union recall >=95% on the frozen CALIBRATION definition;
- no material class of mandatory corrections is structurally unreachable;
- canonicalization failure <=0.5%;
- protected-span map construction has zero integrity failures.

Why 95%:
the final system still needs to reject unsafe candidates. A proposal stage near the eventual >=90% recall requirement leaves insufficient headroom for selective filtering.

If union recall is 90% to <95%:
classify as BORDERLINE and perform focused methodological review before adding another proposer.

If union recall <90%:
do not build the selector; revisit proposer architecture.

## 10. Proposer retention rule

A proposer is retained only if it contributes one of:

- >=1.0 percentage point unique union recall;
- materially improves a preregistered weak operation family;
- reduces conflict uncertainty through corroboration;
- provides unique evidence required by the decision layer.

Otherwise remove it to avoid unnecessary complexity.

## 11. Selector stage — only after proposal gate passes

Only after the candidate-union gate is frozen as PASS may a selective edit authorization protocol be written.

That later protocol must freeze before fitting:

- target labels;
- feature list;
- train/calibration split;
- model family;
- probability calibration method;
- auto-apply threshold;
- REVIEW threshold;
- conflict policy;
- protected-span vetoes.

No post-hoc threshold tuning on INTERNAL_EVALUATION.

## 12. Intended safety target

For AUTO_SAFE edits, target:

- conservative mandatory-edit precision lower bound >=98%;
- zero protected-invariant failures;
- zero unauthorized number/unit/citation changes.

Coverage is secondary.
Low-confidence valid edits should go to REVIEW rather than lowering the precision gate.

## 13. What is explicitly not allowed

- direct full-sentence replacement from any seq2seq model;
- treating proposer agreement as proof of correctness;
- using H1-v1 failure data to tune its gate;
- reopening H2/H3/H4 tuning;
- treating MTAGEC explanations as ground-truth evidence;
- treating LLM explanation quality as automatic authorization;
- opening INTERNAL_EVALUATION or STRESS_DIAGNOSTIC before v2 calibration decisions are frozen;
- opening QALB15 TEST, Confirmation, Holdout, A7'ta reserve, or reserved Nahw IDs.

## 14. Current evidence base

Recent evidence motivating the architecture includes:

- SWEET: efficient Arabic text-editing GEC and ensemble gains.
- Alhafni et al. 2023: GED auxiliary input and contextual morphological preprocessing improve Arabic GEC.
- Ismail et al. 2025: strong AraT5/AraBART seq2seq Arabic GEC performance.
- ArbESC+ 2025: edit-level multi-system combination outperforms individual systems on QALB benchmarks.
- MTAGEC 2025/2026: joint correction, error type, evidence extraction, and explanation with large synthetic data.
- STAGEET 2026: staged typed edit-tagging with interpretable correction trajectories.

These published benchmark values are not directly comparable to the ACAD_PASS frozen metrics.

## 15. Expected improvement and limits

Expected strong improvements:
- candidate recall through union;
- robustness to one model's blind spots;
- explainable provenance;
- safer abstention;
- easier debugging;
- preservation of source/protected content.

Not guaranteed:
- dramatic benchmark F-score jumps;
- high AUTO_SAFE coverage;
- elimination of Arabic ambiguity;
- generalization from QALB to all academic Arabic genres.

The likely primary gain is:
**better recall before selection + substantially better control over unsafe automation.**

## 16. Scientific classification relative to closed M2-H

**IMPROVED ARCHITECTURALLY / PERFORMANCE NOT YET MEASURED**

The architecture directly addresses the demonstrated H1 single-generator recall bottleneck while retaining the strongest safety lessons from H2-H4 and M2-R.

## 17. Exact next authorized step

Do not implement the full selector.

Next:
1. freeze exact reproducible identities for P1 SWEET iterative and P2 AraBART+Morph+GED;
2. verify runtime parity on a tiny non-scoring CALIBRATION sample;
3. freeze canonical edit extraction;
4. run the candidate-generation-only feasibility experiment on CALIBRATION;
5. stop and decide based on union recall before any selector training.

Reserved datasets remain closed.
