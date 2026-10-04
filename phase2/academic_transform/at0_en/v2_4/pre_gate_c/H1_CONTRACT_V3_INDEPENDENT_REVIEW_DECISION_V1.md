# ACAD_PASS — H1 Contract V3 Independent Review Decision V1

Date: 2026-10-04
Status: ACCEPTED WITH ESSENTIAL CHANGES / H1 NOT EXECUTION-READY

Independent review source:
user-mediated higher-model review of H1 Contract V3.

Verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

No V2.4 PLABA prediction has been run.

## 1. Decision

The review is accepted.

The canonical-pair/deduplication direction of V3 is methodologically improved and remains preferred over V1/V2.

However, V3 is NOT authorized for implementation or prediction yet because two construct-alignment issues remain unresolved:

1. PLABA human judgments are sentence-level but account for the context of the entire abstract.
2. PLABA preservation/completeness semantics permit task-specific omission/generalization that is not automatically equivalent to ACAD_PASS strict protected-detail preservation.

Current H1 status:

`H1_NOT_READY_CONTEXT_GOLD_ALIGNMENT`

## 2. Independently verified PLABA context facts

The PLABA retrospective paper states that:
- Task 1 creates sentence-aligned adaptations but expects the rewritten abstract to read fluently as one document;
- PLABA is sentence-level evaluation while accounting for the context of the entire abstract;
- source sentences may be dropped if not relevant to consumer understanding;
- PLABA allows more semantic freedom than machine translation, including adding/removing content.

The official annotation guidelines additionally permit:
- resolving source pronouns using the previous sentence;
- leaving already understandable sentences unchanged;
- ignoring some sentences not relevant to consumer understanding;
- omitting confidence intervals, p-values, and similar measurements;
- using wider publication/outside sources where term intent is ambiguous;
- adding explanatory material for jargon/named entities.

Therefore:

`PLABA SAFE_STRICT != AUTOMATIC ACAD_PASS STRICT-PRESERVATION PASS GOLD`

without a frozen compatibility argument.

## 3. V2.4 context capability audit

Frozen V2.4 source extraction receives a single raw text field.

The frozen extraction bridge calls the source assertion extractor on exactly that text.

No independent field exists for:
- contextual evidence available to interpretation,
while simultaneously:
- excluding that contextual text from completeness/preservation obligations.

Naively prepending the previous sentence or whole abstract would create false preservation obligations when comparing against a single target sentence.

Therefore the current V2.4 runtime does NOT provide a validated non-semantic context channel sufficient to replicate PLABA's contextual human judgment conditions.

This is a construct/interface blocker, not a V2.4 performance failure.

## 4. V3 components retained

Retain:
- canonical unit direction:
  `PMID + exact Source + exact Target`;
- prediction deduplication;
- 399 PMID source clusters;
- human score 0 is NOT REVIEW;
- HUMAN_CONFLICT is diagnostic, not REVIEW gold;
- single-rater records may remain eligible in a limited published-human-gold design;
- repeated ratings are not independent reviewers by assumption;
- pair-micro and PMID-macro reporting;
- PMID cluster bootstrap;
- zero-event safety reporting;
- public-gold / prospective-procedure claim boundary.

## 5. Required changes before V4

### R1 — Context contract
Freeze exactly what context PLABA annotators could use and what V2.4 can validly receive.

Do NOT:
- inject whole abstract as protected source text for a sentence target;
- inject prior target text into candidate if it was not the evaluated candidate;
- use semantic helper inference.

If no context-equivalent non-semantic interface exists in frozen V2.4:
- PLABA sentence-local positive gold cannot be a full H1 hard gate;
- narrow PLABA to a diagnostic/conditional role or use another compatible resource.

### R2 — Gold-semantics contract
Define which PLABA ACC/COM labels are genuinely compatible with ACAD_PASS protection semantics.

Task-permitted omissions must not be silently reclassified as ACAD_PASS-safe preservation.

### R3 — Exact-copy policy
Primary transformed-positive acceptance must exclude:
`Source == Target`

These remain:
- identity controls;
- full-record evidence;
- separately reported diagnostics.

Do not reuse V2 row counts.
Recalculate canonical V3-compatible denominators after context/gold eligibility is frozen.

### R4 — Prediction artifact integrity
Freeze explicit rule:
- exactly one output for each frozen prediction ID;
- missing prediction invalidates completeness;
- duplicate prediction ID invalidates evaluation;
- unknown/extra prediction ID invalidates evaluation.

### R5 — Human-rating provenance wording
Do not call repeated judgments independent annotators unless annotator identity establishes independence.

Use:
`multiple observed judgments`
when identity is unavailable.

## 6. Safety interpretation retained but narrowed

Potential hard safety rule:

`eligible ERROR_STRICT -> PASS_CANDIDATE = 0`

is acceptable only after context/gold eligibility is frozen.

Interpretation:

“zero automatic acceptance of cases for which all available eligible published human judgments assign the worst level on at least one PLABA fidelity axis.”

Do NOT call these automatically:
- critical scientific errors;
- universally unsafe transformations.

PLABA does not encode ACAD_PASS criticality.

## 7. Statistics

Retain:
- PMID cluster as primary document/source unit;
- 10,000 whole-PMID bootstrap replicates;
- seed `20261004`;
- 95% percentile intervals;
- exact one-sided zero-event upper bound when denominator is frozen and complete.

Important:
PMID clustering handles within-abstract dependence but does not prove full independence of underlying studies, retrieval questions, generating systems, or annotation process.

Any denominator change after context/gold eligibility resolution requires freezing the new eligible PMID count before prediction.

## 8. Additional data / humans

No new human recruitment is required now.

No second H1 dataset is automatically mandatory by name.

But PLABA alone may remain insufficient as a hard H1 gate if the context/preservation mismatch cannot be resolved without changing V2.4.

If so:
- narrow PLABA's hard role;
- identify the smallest published expert/human resource that closes the specific uncovered construct;
- do not add datasets merely for benchmark count.

## 9. Current authorization

AUTHORIZED:
`H1 CONTEXT + GOLD-SEMANTICS RESOLUTION`

NOT AUTHORIZED:
- H1 adapter implementation;
- PLABA prediction input freeze;
- V2.4 PLABA predictions;
- H1 scoring;
- V2.4 modification;
- new-human recruitment;
- original custom 80-study Gate C opening;
- Arabic-track work.

## 10. Exact next checkpoint

`H1 CONTEXT + GOLD-SEMANTICS RESOLUTION`

Tasks:
1. freeze PLABA human-evaluation context semantics from primary sources;
2. characterize task-permitted omissions/additions against ACAD_PASS protection semantics;
3. determine whether a valid hard subset can be selected WITHOUT semantic cherry-picking or V2.4-dependent filtering;
4. determine whether frozen V2.4 can consume required context without creating false preservation obligations;
5. if not, define PLABA's narrower valid role and identify the minimum published external replacement/companion resource;
6. only then draft H1 Contract V4.
