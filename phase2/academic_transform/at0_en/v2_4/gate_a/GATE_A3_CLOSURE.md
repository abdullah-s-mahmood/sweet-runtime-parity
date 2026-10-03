# AT0-EN V2.4 — Gate A3 Extractor Validation Closure

Date: 2026-10-03
Status: CLOSED / PASS_DEVELOPMENT / DEVELOPMENT-ONLY

## Canonical execution

Workflow:
`AT0-EN V2.4 Gate A3 Extractor Validation`

Canonical run:
`37143729167`

Trigger commit:
`8afeac02f465c462d015204aebe536366663bfdf`

Artifact:
- id: `11281706053`
- SHA-256: `d96fb79a65834f79b80c4b597a59092f73d6f795efbb5de12f0f418c8639671d`

No model inference occurred.
The extractor remained frozen at:
`32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`

## Canonical result

Status:
**PASS_DEVELOPMENT**

Development cases:
6

Gold assertions:
28

Critical gold assertions:
27

Predicted assertions:
25

Metrics:
- gold assertion coverage: **28/28 = 100%**
- critical gold coverage: **27/27 = 100%**
- false additions: **0/25 = 0%**
- atomic one-to-one predictions: **22/25 = 88%**
- overmerged predictions: **3/25 = 12%**
- oversplit gold assertions: **0**
- certain predictions: 14
- clean CERTAIN predictions: 13
- certain precision: **13/14 = 92.86%**
- error-abstention recall: **87.5%**
- unnecessary abstention rate: **23.53%**
- context-dependency detection recall: **100%**
- context false-alarm rate: **6.25%**
- critical silent errors: **0**

Field diagnostics on one-to-one alignments:
- assertion type: **19/22 = 86.36%**
- predicate: **21/22 = 95.45%**
- subject concepts: **20/22 = 90.91%**
- object concepts: **22/22 = 100%**
- polarity: **22/22 = 100%**
- modality: **22/22 = 100%**
- causality: **22/22 = 100%**
- population binding checks: **100%**
- baseline binding checks: **100%**
- scope checks: **100%**

## Pre-registered threshold margins

Against the frozen A3 development gates:

- overall coverage: 100% vs >=90% -> **+10 percentage-point margin**
- critical coverage: 100% vs >=95% -> **+5 pp**
- false addition: 0% vs <=10% -> **10 pp better than maximum**
- atomic one-to-one: 88% vs >=75% -> **+13 pp**
- certain precision: 92.86% vs >=90% -> **+2.86 pp**
- error-abstention recall: 87.5% vs >=80% -> **+7.5 pp**
- critical silent errors: 0 vs required 0 -> **meets hard gate**

These are threshold margins, not improvements versus a prior comparable extractor baseline.

## Preserved evaluator negative evidence

First A3 run:
- run: `37143592151`
- artifact id: `11281531213`
- artifact SHA-256: `a03c184f4bb8b0ee02888760e8fe34f1cdb7b04c4c2d7cf03ab82c3a6db6ca37`
- initial result: `FAIL_CRITICAL_SILENT_ERROR`
- alleged critical silent error: `EN12-AS-001`

The first evaluator incorrectly treated an isolated assertion-type mismatch
(`RELATIONAL` vs gold `SCOPE`) as a critical silent scientific error even though subject, predicate, object concepts, polarity, modality, and causality were preserved.

The preregistered contract did not define assertion-type disagreement alone as a critical silent semantic failure.

Therefore:
- first score was frozen;
- extractor/gold/thresholds remained unchanged;
- evaluator-contract repair was documented;
- canonical rerun changed critical silent errors from 1 to 0 because the evaluator construct was corrected, **not because extractor performance improved**.

Repair documentation:
`phase2/academic_transform/at0_en/v2_4/gate_a/GATE_A3_EVALUATOR_REPAIR_ADDENDUM_V1.md`

## Remaining extraction errors

Eight predicted assertions have at least one development diagnostic error:

1. EN04-AS-002 — predicate + subject mismatch around embedded `found that`; UNCERTAIN
2. EN04-AS-003 — assertion-type mismatch; UNCERTAIN
3. EN06-AS-001 — overmerge; UNCERTAIN
4. EN06-AS-002 — overmerge; UNCERTAIN
5. EN07-AS-002 — unresolved subject/coreference; UNCERTAIN
6. EN07-AS-004 — overmerge; UNCERTAIN
7. EN12-AS-001 — assertion-type mismatch only; CERTAIN
8. EN12-AS-005 — assertion-type mismatch; UNCERTAIN

Key positive observation:
all observed critical semantic errors/atomicity failures were abstained from except the isolated assertion-type classification mismatch, which is tracked diagnostically but is not by itself a preregistered critical silent semantic error.

## Interpretation

A3 supports the statement:

**The conservative source extractor is development-viable under the current six-case reference, with high coverage and no observed critical silent semantic error, but it remains imperfect in atomicity, assertion typing, and abstention efficiency.**

A3 does NOT establish:
- cross-domain extraction generalization;
- performance on authentic academic documents;
- candidate-text extraction behavior;
- source/candidate graph alignment;
- end-to-end scientific-fidelity safety;
- production readiness.

The reference is development-only and was not blind:
A2 outputs had been qualitatively inspected before the A3 slot-reference supplement was frozen.

## End-stage research / red-team

Fresh review supports maintaining separate metrics for:
- atomicity;
- faithfulness;
- decontextualization;
- coverage/focus;
- claim-set alignment.

Recent work also shows:
- document-level claim-set alignment remains a difficult evaluation problem;
- context/rhetorical cues can remain challenging even in newer claim-extraction settings;
- auditable/versioned benchmark rationales are safer than assuming one-shot labels are infallible.

Therefore:
- do not tune solely to maximize one aggregate score;
- preserve error classes separately;
- keep benchmark/reference revisions versioned and auditable.

## Quality delta

End-to-end ACAD_PASS scientific-fidelity performance:
**UNCHANGED**

Last end-to-end verifier evidence remains:
- adversarial escape: 37.5%
- safe automatic acceptance: 25%
- BOTH_FAIL

A3 introduces the first semantic source-extractor development metrics, so there is no valid directly comparable prior A3 performance percentage.

Methodological status:
**IMPROVED**

Evaluator repair effect:
- reported critical silent errors: 1 -> 0
- this is **not an extractor improvement**; it is correction of evaluator-contract mismatch.

## Completion

Gate A3:
**100% COMPLETE**

Gate A overall:
**approximately 85% complete**

Whole ACAD_PASS:
**approximately 25% ±5% complete** as a planning estimate.

## Exact next authorized checkpoint

`AT0-EN V2.4 GATE A4 — SOURCE-EXTRACTOR READINESS / REPAIR DECISION`

A4 is an interpretation/go-no-go checkpoint.

It must decide whether to:
- ACCEPT the current source extractor for progression to relation-alignment research;
- REPAIR specific development weaknesses first;
- or REDESIGN source extraction.

A4 must explicitly consider:
- 12% overmerge rate;
- 86.36% assertion-type accuracy;
- 23.53% unnecessary abstention;
- 92.86% certain precision;
- 87.5% error-abstention recall;
- zero observed critical silent semantic errors on the current development reference;
- limited/synthetic nature of the reference.

No candidate alignment implementation starts before A4 closes.

Higher-model consultation may be justified at A4 because it is a go/no-go architecture/readiness decision. If requested, it must remain consultation-only and budget-conscious.
