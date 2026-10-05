# ACAD_PASS — FactPICO V2.5 Bounded Failure Analysis Report V1

Date: 2026-10-05
Status: FROZEN DIAGNOSTIC APPENDIX / NO RUNTIME CHANGE / NO RERUN

Taxonomy frozen before case coding:
`FACTPICO_V25_FAILURE_ANALYSIS_TAXONOMY_V1.md`
taxonomy commit:
`ecc458d9f46a51f5cc9f6e10b51b6d5caacc1ce7`

Frozen prediction artifact:
`11348646367`

Frozen scoring artifact:
`11351451888`

Prediction SHA-256:
`925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b`

Scoring artifact digest:
`105534207a4566c38d76174e9cd263244b87e37358b6007c76502bc250d67e77`

## 1. Scope and limits

This report analyzes only already-frozen:
- 345 joined FactPICO rows;
- immutable predictions;
- preserved assertion/relation alignments;
- preserved evidence excerpts;
- executed AT0-EN V2.5 code by static inspection.

No prediction rerun, rescoring, relabeling, threshold change, population change, or runtime modification was performed.

FactPICO is now exposed diagnostic material and MUST NOT be reused later as an independent prospective validation of any repair.

## 2. Complete outcome accounting

Frozen outcomes:
- PASS_CANDIDATE = 0 / 345
- REJECT = 37 / 345 = 10.7246%
- REVIEW = 308 / 345 = 89.2754%
- INVALID_VERIFICATION = 0

All 345 records contain at least one assertion alignment with status:
`UNCERTAIN`.

Across all 2,824 assertion/relation alignment rows:
- UNCERTAIN = 2,773 = 98.1941%
- ALTERED = 42
- PRESERVED = 9
- relation alignment rows = 0

Therefore every final output is completely accounted for by the frozen V2.5 rule:

1. critical ALTERED/CONTRADICTORY/OMITTED/NEW_INFORMATION -> REJECT;
2. otherwise any UNCERTAIN -> REVIEW;
3. otherwise PASS_CANDIDATE.

Observed:
- all 37 REJECT records contain both extraction uncertainty and at least one critical bad assertion alignment;
- all 308 REVIEW records contain assertion uncertainty and no critical reject condition;
- 300 / 308 REVIEW records have every assertion alignment marked UNCERTAIN.

This establishes the final decision mechanism without claiming that the decision policy itself is the root cause.

## 3. Primary diagnostic localization

### D1 — Extraction uncertainty propagation: ESTABLISHED

Records affected:
`345 / 345 = 100%`

The aligner function `mapping_status()` returns UNCERTAIN before semantic comparison whenever either aligned assertion group contains confidence other than CERTAIN.

Frozen reason:
`Critical/source uncertainty is preserved rather than promoted by graph agreement.`

This is an established mechanism.

However, the frozen prediction output does not retain the exact extractor-side unresolved slot for every aligned assertion. Therefore the deeper per-case origin is sometimes:
`UNRESOLVED`.

### D6 — Decision uncertainty gate: ESTABLISHED

Records where D1 becomes the final outcome trigger:
`308 / 345`

These are exactly the REVIEW records.

The frozen decision map is fail-closed and behaved as implemented. Merely relaxing REVIEW to PASS is NOT supported and is explicitly rejected as a repair strategy.

### D3 — Critical semantic/binding mismatches: ESTABLISHED

Primary direct cause across the 37 REJECT records:
- D3_CONCEPT_COVERAGE = 21
- D3_PREDICATE_CHANGE = 10
- D3_OWNER_VALUE_BINDING = 4
- D3_MODALITY = 1
- D3_BASELINE_BINDING = 1

No critical relation failure was observed.

### D7 — Representation granularity / unequal-count grouping: STRONGLY SUPPORTED

Records with at least one non-1:1 assertion group:
`339 / 345 = 98.2609%`

Records with more source assertion IDs than candidate assertion IDs:
`331 / 345 = 95.9420%`

Records with source assertion count at least 3x candidate count:
`250 / 345 = 72.4638%`

Median source:candidate assertion-count ratio:
`4.83 : 1`

Executed V2.5 static behavior for unequal counts is:
- align the first min(source,candidate) by one-to-one matching;
- append every remaining source or candidate assertion to the LAST matched group.

This can create very large mixed groups.
Observed maximum source-side group size:
`95 assertions`.

Since `mapping_status()` marks a whole group UNCERTAIN if ANY member has non-CERTAIN confidence, this grouping behavior can amplify local extraction uncertainty into alignment-level uncertainty.

The evidence supports this as a major interacting weakness, but not as the sole cause because a small number of REVIEW cases remain 1:1 and still show uncertainty.

## 4. Static extraction/representation findings

The executed relation-aware extractor contains explicit parsers primarily for narrow forms such as:
- equations and symbol definitions;
- quantitative Group A / Group B constructions;
- run/seed statements;
- explicit scope/noncausal templates;
- density/reduction/measured-as patterns;
- a small set of explicit scientific predicates.

Other text falls back to the A2 assertion extractor or to UNRESOLVED.

The A2 predicate inventory is also narrow and marks multiple common constructions as unresolved or uncertain, including embedded propositions.

This is materially narrower than general biomedical RCT prose.

### Preserved evidence of segmentation/markup artifacts

Without rerunning any extractor, frozen alignment evidence shows:
- 48 records contain source evidence fragments of length <=3 characters;
- recurring fragments include `e` and `i`, consistent with abbreviation fragmentation;
- candidate evidence in 116 records contains escaped/tag-like fragments such as `&lt`, `s&gt`, or `/s&gt`.

Static sentence segmentation protects decimal points but does not generally protect biomedical abbreviations.

These artifacts are direct preserved observations plus a static-code mechanism.
They are not sufficient to claim that every failure is caused by segmentation.

## 5. Relation layer finding

Relation alignment rows:
`0 across all 345 records`.

Because `align_relations()` would emit rows for preserved, omitted, altered, or candidate-only relations, zero rows implies the executed source and candidate relation representations contributed no relation objects to these cases.

Therefore:
- relation uncertainty did NOT cause the 308 REVIEW outcomes;
- relation failure did NOT cause the 37 REJECT outcomes;
- the current relation layer was effectively inactive on FactPICO.

This does not prove relations are unnecessary; it shows they were not operationally contributing in this evaluation.

## 6. SAFE_STRICT_CONTROL priority audit

Frozen:
`34 records / 33 source clusters`

Outcomes:
- PASS = 0
- REVIEW = 28
- REJECT = 6

All 34 contain extraction uncertainty.

Among 28 REVIEW:
- all are directly explained by D1 + D6;
- 27 / 28 also show D7 non-1:1 grouping;
- median source:candidate assertion ratio = 2.25.

The 6 REJECT records and direct mechanisms are:

1. `05e345d7633ac324f4694c0e0fddf5b3de38cba13d6357f03c7e4904d364dc1c`
   - source: `00db558cec4a01de115f813edd668423dc93b3f4349c7143d1119f9fdfeb928e`
   - mechanism: D3_MODALITY
   - direct frozen reason: modality/evidential commitment changed
   - alternative: genuine candidate-strength change vs representation mismatch remains a bounded manual question.

2. `1b074161aa7f6dce5944a25383e1213e723a0c823685ae2e466ca8f05d76cd42`
   - source: `5c914340cd207cb3b287694c91bec682b5ec21545591bb0b22d2215e4a46d295`
   - mechanism: D3_OWNER_VALUE_BINDING

3. `2f010c886c0a7a3b2f05dad1a614836ed0446d17bc02e1a762e7f74085aaad5b`
   - source: `7eb69d25aad6ae54e715cb03ac47c7fd232799cefb58b0a522113351199e9a9c`
   - mechanism: D3_PREDICATE_CHANGE

4. `91e72f09c8ad26b6bfe308b9d6c04a1080e0149106e4e253964ce8b5553d9ef6`
   - source: `7dacb1c09c62095fd272bacbb79680c715dad29c7354b51af7901734f9c5768e`
   - mechanism: D3_OWNER_VALUE_BINDING

5. `bbc8413bdf3b0019d4039f4b7b46afeeb29f30c213660829f7bedaa407a42aeb`
   - source: `bfea8f7fff9b5c337c908dec11b5a531b3c930d4577880ec04e4b926edcbee74`
   - mechanism: D3_CONCEPT_COVERAGE
   - frozen coverage reason includes source->candidate 0.12 / candidate->source 0.08.

6. `bd49f60f9149122ee241ca6678a632361c92fcb10764a2f2c409a1aabad6e96c`
   - source: `2fd01b625c01cdaf526b3bffd74ce1b3e0b85fbcb2da88061ca0e3028ba5e973`
   - mechanism: D3_OWNER_VALUE_BINDING

Important counterexample to a grouping-only explanation:
`357663177531777c9f63a108414c8bdeae1d30db624c64169dbd673eea0a0f31`
is SAFE_STRICT_CONTROL / REVIEW with an observed 1:1 assertion count (11 vs 11), yet 9 assertion alignments are UNCERTAIN.

Therefore D7 is major but cannot be the complete explanation.

## 7. ERROR_STRICT comparison

Frozen:
`149 records / 83 source clusters`

Outcomes:
- REJECT = 16
- REVIEW = 133
- PASS = 0

All 149 contain D1 extraction uncertainty.

Among ERROR_STRICT:
- D7 grouping imbalance = 147 / 149;
- median source:candidate assertion ratio = 5.67.

Primary causes of the 16 REJECT records:
- concept coverage = 11;
- predicate change = 4;
- baseline binding = 1.

Representative established mechanisms:

- concept coverage:
  record `0f2f318a37d0cadb6546a8ea5e4122d3adc87833ddda65d0f588e129603c028c`
  source `793c7dbf031fcb541e9d0711eb4ec33bad091da705979d406fbebaab2ffe8afd`

- baseline binding:
  record `15f1e7db3ac3f980eb4201ffc695d3c100d2f2251eed8a2fcf78d511c30cce3c`
  source `cb1d194fbb72304c49b2686f31e2f1be6bda26d5424d791b670d143cac7cecae`

- predicate change:
  record `5bea6c4e08ff29c49f6157533fcaa216547d0271c355f7181fd331bd5963ecf7`
  source `8b93380611fa38ec57139f300ec9d9c2e291d3ee45ee6a64c4e290528e35fd80`

The 133 ERROR_STRICT REVIEW records demonstrate the central utility failure:
the system rarely reaches decisive rejection because extraction/representation uncertainty blocks the semantic decision before a reject condition can be established.

That statement is a supported mechanistic interpretation, not a reclassification of any frozen outcome.

## 8. Most defensible failure localization

### Established

1. The current system is fail-closed.
2. Universal assertion uncertainty exists in the frozen trace.
3. The uncertainty gate directly produces all 308 REVIEW outcomes.
4. Critical semantic/binding mismatches directly produce all 37 REJECT outcomes.
5. No relations participate in the frozen FactPICO decisions.
6. Unequal assertion counts are handled by a last-group leftover merge.
7. Representation granularity is strongly asymmetric across most cases.

### Strongly supported hypothesis

The dominant bottleneck is the interaction:

`EXTRACTION / REPRESENTATION UNCERTAINTY`
+
`UNEQUAL-COUNT GROUPING THAT AMPLIFIES LOCAL UNCERTAINTY`
+
`FAIL-CLOSED REVIEW GATE`

This explains the observed absence of PASS_CANDIDATE and low decisive REJECT rate more defensibly than a decision-policy-only explanation.

### Not established

- which exact extractor side/slot is causal in every case;
- that all SAFE rejects are false positives;
- that all ERROR reviews should have been rejects;
- that simply changing confidence thresholds would be safe;
- that relations are unnecessary in future versions;
- that the failure generalizes to all disciplines or Arabic;
- full H1 failure.

## 9. Repair-direction conclusion

The frozen evidence does NOT justify changing:
- the FactPICO threshold;
- gold classes;
- pair_outcome safety ordering;
- REVIEW semantics;
- critical mismatch definitions solely to improve this benchmark.

The narrowest defensible repair target is upstream:
`REPRESENTATION + UNEQUAL-COUNT ALIGNMENT / CONFIDENCE LOCALIZATION`.

A separate repair-design document defines this without implementing it.

## 10. Current checkpoint

FactPICO V2.5 experiment:
`100% COMPLETE`

Frozen result:
`H1_FULL_PASS_NOT_ACHIEVED`

Current authorized diagnostic phase:
`FAILURE ANALYSIS COMPLETE`

Next:
`FAILURE_ANALYSIS_AND_REPAIR_DESIGN_REVIEW`

No modified runtime is authorized.
