# POST-V4.2 CANDIDATE ARCHITECTURE REDESIGN GATE V1

Date: 2026-10-02

Status:
**OPEN / SOURCE-ONLY DESIGN GATE / NO NEW GOLD AUTHORIZED**

Predecessor:
`MPSEF_RJOINT_V4_2_DEVELOPMENT_MEASUREMENT_CLOSURE_LOCK_V1`

## 1. Why this gate exists

The completed V4.2 DEVELOPMENT measurement established:

- current ROSTER primary reference-relative recovery: ~72.23%
- frozen candidate-availability requirement: 95%
- deficit: 2,201 primary targets / 22.73 pp
- current ROSTER clean whole-action recovery: ~23.65%
- current ROSTER primary complete repair: ~21.9%

Therefore:
1. selector optimization alone cannot solve the missing-candidate deficit;
2. whole-sentence candidates entangle useful edits with extra unsupported edits;
3. candidate generation and representation must be redesigned before selector training.

## 2. Hard boundaries

This gate is SOURCE-ONLY.

Forbidden:
- reopen V4.2 gold for tuning;
- rerun consumed V4.2;
- train selector;
- activate family consensus;
- activate generic LLM judge as oracle;
- test new P4/P5 against consumed C_F gold;
- open internal/stress/reserved populations;
- weaken frozen protection stack;
- claim linguistic improvement from source-only diagnostics.

C_F may be used only as explicitly labeled adaptively-consumed development context.
It is not a clean confirmation set.

## 3. Architecture objective

Replace the current monolithic whole-sentence action view with a provenance-preserving candidate representation that can:

- isolate local corrections from unrelated extra edits;
- preserve source span identity;
- preserve proposer/family/ancestry identity;
- express KEEP/abstain locally;
- prevent arbitrary edit fusion;
- expose conflicts explicitly;
- retain whole-sentence reconstruction deterministically;
- remain compatible with protection constraints;
- fail closed on alignment ambiguity.

## 4. Candidate representation proposal

### 4.1 Atomic Edit Transaction

Each proposer output is decomposed relative to the frozen source into atomic transactions.

Required fields:

- uid
- cluster_id
- source_sha256
- proposer_id
- proposer_version
- family_id
- ancestry_id
- parent_action_id
- edit_id
- source_token_start
- source_token_end
- source_char_start
- source_char_end
- source_text
- replacement_text
- edit_type
- alignment_version
- protection_status
- transaction_sha256

No transaction may exist without a reversible source span.

### 4.2 Edit types

Initial operational types:

- INSERT
- DELETE
- SUBSTITUTE
- SPLIT
- MERGE
- PUNCTUATION
- COMPLEX_LOCAL
- UNREPRESENTABLE

`UNREPRESENTABLE` must fail closed and cannot silently enter the candidate set.

Typed labels are operational, not claims of linguistic diagnosis.

## 5. Provenance-aware deduplication

Literal identical edits over the same frozen source span may be deduplicated into one edit candidate while retaining every provenance record.

Never collapse:
- same replacement over different spans;
- different replacements over same span;
- P1 and P3 into independent family votes.

P1 and P3 remain:
`SWEET_QALB14`

P2 remains:
`SEQ2SEQ_GED_MORPH`

## 6. Conflict components

Construct an interval/conflict graph where edits conflict if they:

- overlap source spans;
- insert incompatibly at the same boundary;
- imply incompatible split/merge boundaries;
- violate frozen protection invariants;
- reconstruct to non-deterministic text.

Connected components become local decision units.

Each component must include an explicit:
`KEEP_COMPONENT`

## 7. No arbitrary fusion rule

Compatible edits from distinct non-overlapping components may be reconstructed together only through a deterministic composition rule.

Within a conflict component:
- choose at most one mutually exclusive edit/bundle;
- KEEP is always legal;
- no gold-aware fusion;
- no reference-aware component construction;
- no same-family double vote.

Cross-component composition must be source-order deterministic.

## 8. Candidate bundles

Atomic edits alone may fail to represent intrinsically coupled corrections.

Therefore allow a `BUNDLE` only when:
- all member edits originate from the same parent proposer action;
- coupling is required for reversible reconstruction or local semantic integrity;
- bundle span is explicit;
- member edit IDs are frozen;
- provenance is retained;
- bundle creation rule is source-only and deterministic.

Do not create bundles from gold co-occurrence.

## 9. Protection integration

Protection is evaluated:
1. source span → atomic edit;
2. bundle aggregate if present;
3. final deterministic reconstruction.

Any protected-invariant violation fails closed.

The active protection gate is NOT weakened in this phase.

## 10. Source-only diagnostics

Before any new gold:

- transaction extraction success rate;
- unrepresentable rate;
- ambiguous-alignment rate;
- edits per UID;
- conflict components per UID;
- component size distribution;
- KEEP-only component rate;
- family participation;
- literal cross-family edit agreement;
- same-family P1/P3 overlap;
- protection rejection rate;
- deterministic reconstruction parity;
- exact reconstruction back to original proposer output;
- runtime and memory cost.

No correctness metric is inferred from these diagnostics.

## 11. New-family research gate

The V4.2 result justifies reopening research for a genuinely independent candidate family because the current union has a large availability deficit.

Candidate classes to investigate source-only:

1. typed/staged edit tagger inspired by STAGEET;
2. provenance-auditable independent GEC checkpoint;
3. lightweight orthographic/morphological specialist only if it adds a genuinely distinct family;
4. rule-backed high-precision specialist only if it has executable provenance and strict scope.

Every candidate must have:
- exact checkpoint;
- tokenizer revision;
- code/config revision;
- license;
- training-source inventory;
- QALB/QALB-adjacent overlap audit;
- input normalization;
- max length;
- output decoding policy;
- deterministic inference settings;
- cost/runtime profile.

No new family is gold-eligible merely because it is public.

## 12. P3 disposition during redesign

P3 remains available for source-only transaction extraction because:
- it may expose locally useful edits hidden inside globally noisy whole-sentence outputs;
- its whole-action primary marginal gain was small;
- it is same-family with P1.

It may NOT become an independent family vote.

## 13. Research basis

Fresh evidence considered:

### ArbESC+ (2025)
Arabic multi-system edit selection supports investigating edit-level conflict-aware combination.

### STAGEET (2026)
Stage-wise typed edit tagging supports investigating localized executable edit representations.

### JELV (AAAI 2026)
Finite references under-cover valid alternatives; therefore source-only redesign must not treat prior `REFERENCE_UNSUPPORTED_EXTRA` as synonymous with wrong.

### CLEME2.0 (ACL 2025)
Edit-disentangled evaluation motivates separating correction components for interpretable analysis.

## 14. Red-team questions that must be answered before implementation closure

1. Can source→candidate alignment be made deterministic across Arabic normalization variants?
2. How are zero-width INSERT edits ordered at identical boundaries?
3. How are SPLIT/MERGE transactions represented without losing token/character identity?
4. Can a parent action reconstruct exactly from extracted transactions?
5. When does local decomposition change the semantics of a coupled correction?
6. What is the maximum allowed component size before fail-closed review?
7. How are punctuation edits isolated without contaminating primary scope?
8. How are same-family P1/P3 duplicates represented without fake consensus?
9. Can compatible components be composed without introducing an output never proposed by any system?
10. If composition creates a novel full sentence, what provenance semantics are required?
11. What prevents combinatorial explosion?
12. How are protection invariants evaluated after multi-component reconstruction?
13. What is the fallback for ambiguous alignment?
14. How are exact source offsets preserved through Arabic normalization?
15. How is future selector training prevented from leaking consumed C_F labels?
16. What untouched evaluation population will be frozen before any gold-aware model selection?

## 15. Initial architecture disposition

### KEEP
- P1
- P2
- protection stack
- explicit KEEP
- family/ancestry semantics
- exact provenance
- frozen-source identity
- fail-closed behavior
- deterministic reconstruction requirement

### REPAIR
- whole-sentence action representation
- conflict handling
- local edit extraction
- candidate cleanliness

### ADD
- atomic edit transactions
- conflict components
- deterministic bundle semantics
- edit-level source-only diagnostics
- new independent-family provenance audit

### DEFER
- selector
- learned consensus
- generic LLM judge
- gold-aware threshold tuning
- new-family gold evaluation

## 16. Exit criteria for this design gate

Before implementation may be considered source-only ready:

- representation contract frozen;
- deterministic alignment algorithm specified;
- bundle rule specified;
- conflict rule specified;
- normalization/offset contract specified;
- protection integration specified;
- synthetic adversarial test matrix defined;
- no gold dependency in any design rule;
- independent review packet prepared.

Next artifact:
`POST_V4_2_EDIT_TRANSACTION_CONTRACT_V1.md`
