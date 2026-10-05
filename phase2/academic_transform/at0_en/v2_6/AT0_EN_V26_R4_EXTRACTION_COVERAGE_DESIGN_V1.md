# AT0-EN V2.6-DEV — R4 Extraction Coverage Design V1

Date: 2026-10-05
Status: DESIGN FROZEN BEFORE R4 IMPLEMENTATION

## Trigger evidence

After R1-R3 mechanics passed 260/260, an independent 30-document real-RCT development diagnostic from PICO-Corpus was run under thresholds frozen before observation.

After closing R1 boundary defects:
- short evidence <=3 chars: 0
- empty representations: 0
- over-128 assertion documents: 0
- non-CERTAIN assertions: 354 / 396 = 89.39%
- unresolved predicates: 348 / 396 = 87.88%
- documents with >30% non-CERTAIN assertions: 30 / 30 = 100%

Frozen R4 trigger thresholds:
- aggregate non-CERTAIN >20%, OR
- aggregate unresolved >15%, OR
- >20% of documents with non-CERTAIN >30%

Therefore:
`R1_INCOMPLETE = FALSE`
`R4_RECOMMENDED = TRUE`

R4 is activated by preregistered development criteria, not by FactPICO tuning.

## Competing R4 strategies considered

### A. Add benchmark-shaped regex templates
REJECTED.
High overfitting risk and poor generalization.

### B. Immediately add a learned PICO/LLM model as sole extractor
REJECTED for first R4 increment.
The frozen architecture forbids any single model as the safety oracle, requires independently auditable extraction/provenance, and model calibration would create a larger architecture transition.

### C. Section/PICO-aware deterministic proposition coverage + preserved uncertainty
SELECTED as R4.1.
This is the narrowest reversible repair compatible with the frozen architecture and current evidence.

### D. Hybrid learned extraction witness
RESERVED as R4.2 only if R4.1 fails its untouched internal holdout.
The original architecture already permits deterministic Lane A plus semantic/model Lane B, but any learned witness must be separately pinned, calibrated, and evaluated.

## Research basis

Recent RCT/PICO extraction literature favors:
- section-aware processing;
- structured PICO representations rather than flat token checks;
- explicit treatment-group / endpoint structure;
- extractive or NER approaches with provenance;
- careful abstention and evaluation rather than untraceable holistic judgments.

R4.1 therefore expands explicit scientific proposition representation without removing uncertainty when structure is not recoverable.

## R4.1 scope

Add a generic RCT/scientific surface proposition layer BEFORE the current fallback.

Supported proposition families are domain-general, not copied from FactPICO or the 30 diagnostic abstracts:

1. STUDY_DESIGN
   - randomized/controlled/double-blind/phase/cohort/trial/study descriptions.
2. POPULATION
   - explicit participant/patient/women/men/children/cohort sample descriptions and counts.
3. ASSIGNMENT / INTERVENTION
   - assigned/randomized/allocated/received/underwent/treated/administered.
4. OUTCOME_DEFINITION / MEASUREMENT
   - primary/secondary outcome/end point; assessed/measured/evaluated.
5. RESULT / COMPARISON
   - increased/decreased/improved/reduced/higher/lower/differed/similar/no difference/associated/correlated.
6. FOLLOW_UP / PROCEDURE
   - followed/completed/continued/performed.
7. SAFETY / EVENT
   - adverse events/toxicity/deaths/tolerated where explicitly asserted.
8. CONCLUSION / EFFECT
   - explicit effect statements with preserved modality.

Each emitted assertion must preserve:
- exact evidence;
- subject;
- normalized predicate;
- object;
- polarity;
- modality;
- quantities/units/anchors when available;
- explicit population/group/baseline/time bindings when syntactically present;
- confidence;
- criticality;
- provenance.

## Criticality rules

CRITICAL:
- population identity/count when claim-defining;
- intervention/comparator assignment;
- primary/secondary endpoint identity;
- quantitative treatment/result claims;
- polarity/causality/modality of effect claims;
- explicit safety/toxicity/death claims.

MATERIAL:
- background rationale;
- setting;
- generic study design metadata unless it changes interpretation;
- non-outcome procedural metadata;
- bibliographic/footer material.

Unmatched MATERIAL source assertions do not force REJECT.
Unmatched CRITICAL source assertions remain explicit and fail closed.

## No confidence laundering

R4.1 may mark CERTAIN only when an explicit surface construction supports the frame.
It must not convert ambiguous fragments to CERTAIN merely to reduce REVIEW.

Unsupported or structurally ambiguous clauses remain UNCERTAIN/AMBIGUOUS.

## Split/merge policy

R3 atomic partial assignment remains authoritative.
R4.1 should reduce artificial count imbalance by extracting multiple atomic propositions from coordinated RCT sentences when deterministic decomposition is explicit.

No return to the V2.5 "append leftovers to last group" behavior.

## Development evidence partitions

- Diagnostic/dev set: first 30 frozen PICO-Corpus documents already opened.
- Internal holdout: next 60 lexicographically selected PICO-Corpus documents, identities frozen before R4 implementation in:
  `AT0_EN_V26_R4_INTERNAL_HOLDOUT_MANIFEST_V1.json`

The 60-document holdout must not be opened until R4.1 code and acceptance criteria are frozen.

Neither partition is external validation.

## R4.1 pre-open acceptance criteria

Existing 260 mechanics suite must remain:
- 260/260 PASS;
- safe paraphrase 60/60 PASS;
- critical errors 80/80 REJECT;
- unsafe critical PASS = 0;
- unequal-count 60/60;
- INVALID = 0;
- fresh-process deterministic.

On the 30-document diagnostic set, before holdout opening:
- short evidence <=3 = 0;
- empty documents = 0;
- over-128 documents = 0;
- aggregate unresolved predicate rate <=35%;
- aggregate non-CERTAIN rate <=40%.

Only if these are met may the 60-document internal holdout be opened.

On the untouched 60-document internal holdout:
- short evidence <=3 = 0;
- empty documents = 0;
- over-128 documents = 0;
- aggregate unresolved predicate rate <=40%;
- aggregate non-CERTAIN rate <=45%;
- at least 80% of documents have non-CERTAIN rate <=50%.

These are development criteria, not scientific performance claims.

## R4.2 trigger

If R4.1 preserves safety mechanics but fails the frozen 60-document holdout coverage thresholds:
- do NOT loosen thresholds;
- preserve failure;
- authorize design of a pinned auxiliary biomedical extraction witness or weak-supervision layer;
- keep deterministic provenance and fail-closed fusion;
- freeze model identity/calibration before inference.

## STOP boundary

R4.1 implementation and development evaluation are authorized.
No FactPICO rerun/rescoring.
No external validation.
No production claim.
No Arabic work.
