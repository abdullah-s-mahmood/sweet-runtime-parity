# AT0-EN V2.4 Gate A4 — Higher-Model Readiness Consultation Response

Date: 2026-10-03
Role: independent Chief Architect / Research Reviewer

## Verdict

`ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Authorization is limited to alignment research on development data.
It does not approve the extractor for production and does not establish end-to-end system safety.

## Blocking issues

No currently demonstrated issue blocks beginning alignment research.

Overmerge becomes blocking only if it causes loss of:
- relation ownership;
- negation;
- scope;
- or other material scientific semantics,
and the merged representation is then treated as correct/certain.

The observed overmerge rate alone does not establish that failure.

## Non-blocking issues

1. Comparative/procedural overmerge at 12%:
   non-blocking by itself under the frozen 1:N / N:1 architecture.
   Distinguish meaning-preserving aggregation from meaning-losing merge.

2. Embedded propositions and local coreference:
   real errors worth future repair, but currently observed examples were routed to UNCERTAIN and do not block development alignment.

3. Assertion-type classification:
   defer improvement as long as type mismatch alone cannot bypass semantic checks or cause claim omission.

4. Unnecessary abstention at 23.53%:
   primarily an efficiency/usability issue.
   Reducing it now is not scientifically required and may overfit six development cases.

## Minimum required repairs before alignment

None are mandatory.

During alignment research:
- first use correct/human-reviewed source and candidate representations to isolate alignment error;
- then separately test extracted representations;
- uncertainty must remain explicit;
- agreement between two uncertain graphs is not evidence that their meanings are correct;
- merged and abstained cases must remain in denominators/diagnostics;
- only repair overmerge later when evidence shows loss of relation ownership, scope, negation, or other material meaning.

## Minimum revalidation gate

No additional extractor run or new holdout is required before beginning alignment research.

If the extractor is changed later:
- rerun the same six-case development evaluation using the frozen thresholds;
- include a small number of contrastive examples tied to the repair class;
- critical silent semantic errors must remain zero;
- do not require 100% atomicity;
- do not introduce a new abstention target merely to improve the metric.

## Authentic-text timing

`AFTER_ALIGNMENT_PROTOTYPE`

Introduce authentic academic excerpts with their context once a diagnosable alignment prototype exists, but before freezing the system or claiming integrated validity.

## Final rationale

GO for alignment research.

The source extractor is not proven generally reliable, but the current evidence is sufficient for a limited development transition because:
- critical coverage is complete on the current development reference;
- observed material extraction failures were generally abstained from;
- no critical silent semantic error was observed;
- alignment errors can be isolated using human-correct representations;
- the architecture already supports one-to-many and many-to-one matching.

The evidence does not justify production acceptance, extractor generalization claims, or end-to-end V2.4 safety claims.
