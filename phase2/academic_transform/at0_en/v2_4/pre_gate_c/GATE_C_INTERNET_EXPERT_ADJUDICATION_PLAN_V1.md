# ACAD_PASS — Gate C Internet Expert Adjudication Plan V1

Date: 2026-10-03
Status: OPERATIONAL SOLUTION / HOLDOUT STILL UNOPENED

## Problem

The project owner does not have an existing pool of qualified independent human reviewers for Gate C.

The final Gate C protocol requires qualified, independent human adjudication for a non-provisional Gate C.

This plan solves reviewer acquisition without weakening that requirement.

## Primary solution: recruit qualified reviewers over the internet

### Route A — Kolabtree

Use Kolabtree to recruit domain-specific scientists / peer-review consultants.

Why it fits:
- specifically markets scientific and peer-review expertise;
- supports private projects;
- supports confidentiality / NDA;
- allows selection by subject expertise;
- appropriate for research-grade adjudication rather than general crowd work.

Recommended use:
- primary or adjudication reviewers where discipline specificity matters most.

### Route B — Prolific Domain Experts

Use Prolific Domain Experts for verified specialist recruitment.

Relevant platform properties:
- domain experts can be recruited directly;
- expert verification can include skills tests, academic/professional credentials, publication history and experience;
- suitable expert categories include STEM, healthcare, senior professionals and AI/fact-checking related expertise.

Recommended use:
- scalable recruitment of primary reviewers;
- supplement disciplines where enough suitable experts are visible in the pool.

## Reviewer structure

For each of the 5 Gate C domains:

- Primary Reviewer A
- Primary Reviewer B
- Reserve/Adjudicator C

Target pool:
- 10 primary independent reviewers total;
- up to 5 reserve/adjudicators, one per domain or shared only where expertise genuinely overlaps.

Reviewers must be independent of:
- candidate construction;
- verifier implementation;
- Gate C prediction execution.

No reviewer may see:
- verifier prediction;
- intended construction class;
- constructor rationale;
- the other primary reviewer's first judgment.

## Reviewer qualification

Platform verification alone is necessary but not sufficient.

Every reviewer must pass a frozen qualification step before Gate C gold work.

### Qualification components

1. Domain credentials
   - appropriate postgraduate training and/or publication/professional research record.

2. Scientific-fidelity task
   - distinguish faithful preservation from material scientific drift.

3. Evidence-span task
   - identify the minimal source/candidate evidence supporting the judgment.

4. Ambiguity task
   - distinguish genuine REVIEW from simple difficulty/disagreement.

5. Critical-relation task
   - ownership, scope, negation, causality/association, values/units, attribution/citation, or domain-relevant relation.

### Calibration material

Use public human/expert-annotated scientific verification material only for reviewer qualification/calibration, never as Gate C holdout material.

A suitable calibration source is SciFact:
- expert-written scientific claims;
- SUPPORT/CONTRADICT labels;
- annotated evidence/rationales.

SciFact calibration does NOT replace Gate C adjudication because its construct differs from source-candidate academic transformation fidelity.

## Qualification gate

Freeze reviewer-qualification rules before inviting reviewers.

Proposed minimum:
- no material safety mistake on a small critical qualification subset;
- >=90% overall qualification correctness;
- evidence-span support judged adequate on all critical qualification items;
- qualification disagreement reviewed before acceptance.

These are reviewer-screening criteria, not ACAD_PASS system metrics.

## Assignment

Within each domain:
- each Gate C transaction receives two independent initial judgments;
- primary reviewers do not communicate before both judgments are frozen;
- unresolved material disagreement goes to the reserve/adjudicator;
- reviewer identities are replaced by neutral reviewer IDs in the scoring package.

Avoid having one reviewer adjudicate all work across all five domains.

## Conflict-of-interest policy

Reviewer must disclose:
- authorship/co-authorship of the evaluated source;
- direct involvement in the underlying study;
- close current collaboration with source authors where it could bias judgment.

Conflicted items are reassigned before prediction/gold reveal workflow proceeds.

## Cost-control strategy

To minimize cost without weakening Gate C:

1. Use only two initial reviewers per transaction.
2. Use a third reviewer only for unresolved material disagreement.
3. Give reviewers domain-matched batches rather than paying each reviewer to learn all five domains.
4. Use the frozen qualification test to reject unsuitable reviewers before expensive Gate C adjudication.
5. Pilot the adjudication interface on non-holdout calibration examples only.
6. Do not open Gate C source sampling until the reviewer pool and access separation are ready.

Prolific currently recommends premium rates for verified Domain Experts; exact project cost depends on task duration and field.

## Low-budget fallback

If the project cannot recruit enough qualified humans:

- Gate C may still be executed as `PROVISIONAL_RESEARCH_EVIDENCE`;
- use multiple independent model judges plus deterministic evidence checks and existing expert-annotated calibration datasets;
- keep model judges blind to verifier output and constructor intent;
- require disagreement escalation rather than majority-vote certainty;
- do NOT call the resulting gold independent human gold;
- do NOT use it for non-provisional Gate C or strong-adoption claims.

This fallback preserves research momentum but does not satisfy the frozen non-provisional gold requirement.

## Existing expert-labeled datasets

Existing datasets such as SciFact may be used for:
- reviewer qualification;
- adjudication-guide calibration;
- sanity checking;
- secondary external benchmarking where construct overlap is appropriate.

They must NOT silently replace Gate C because Gate C evaluates faithful academic transformation relative to authentic source/context, a broader and different construct.

## Operational next steps

Before Gate C source sampling:

1. Freeze reviewer qualification pack using only non-Gate-C public examples.
2. Freeze reviewer qualification thresholds.
3. Create recruitment brief for each of the five domains.
4. Recruit 2 primary reviewers/domain and 1 reserve where possible.
5. Verify qualification and conflicts.
6. Freeze reviewer IDs and assignments.
7. Configure gold/prediction access separation.
8. Only then change Gate C opening readiness from NOT_AUTHORIZED to AUTHORIZED.

## Decision

`INTERNET_RECRUITED_QUALIFIED_HUMAN_ADJUDICATION`

is the preferred solution for non-provisional Gate C.

No requirement is weakened merely because the project owner does not personally know reviewers.
