# AT0-EN V2.4 — PRE-GATE-C Higher-Model Methodology Response V1

Date: 2026-10-03
Status: RECORDED / ACCEPT_WITH_ESSENTIAL_PROTOCOL_AMENDMENTS

## Verdict

`ACCEPT_WITH_ESSENTIAL_PROTOCOL_AMENDMENTS`

The higher-model reviewer:
- accepts 80 independent source clusters / 200 transactions for Gate C research progression;
- supports explicit separation between Gate C progression and later Strong-Adoption Validation;
- does not recommend increasing sample size now;
- does not recommend redesigning the verifier;
- requires protocol amendments before opening any holdout source.

The reviewer states the review used both the supplied evidence and external research.

## Required amendments

1. Independence is defined at the original study/paper level, not excerpt level.
2. Use a mix of recent and older unseen sources rather than 2026-only.
3. Freeze first public-availability date including preprints.
4. Freeze allowed verifier/reviewer context.
5. Preserve paired source design, but hide sibling/category construction cues from prediction.
6. Prefer material-drift candidates derived from the faithful rewrite when possible to prevent class-style shortcuts.
7. Keep REVIEW allocation preregistered rather than chosen after verifier behavior.
8. Gold adjudication requires qualified independent human review for non-provisional Gate C.
9. Reviewer blinding includes verifier prediction, intended construction class, constructor rationale, and the other reviewer's initial label.
10. Gold REVIEW means evidence is genuinely insufficient for a critical relation; reviewer disagreement alone does not imply REVIEW.
11. Candidate construction intent never overrides adjudicated gold.
12. Freeze adjudication guide, materiality definition, exclusions, metrics, and reporting weights before first source selection.
13. Separate gold storage/permissions from prediction execution; hashes prove immutability, not secrecy.
14. Use neutral item identifiers that do not leak intended class/failure family.
15. Prediction execution must start from frozen text/context, not human-correct graph representations.
16. No partial-result peeking or selective retry.
17. Post-reveal gold corrections remain versioned with original result preserved; untouched status is not restored.
18. Exclude all development/research/consultation/example papers and passages from Gate C.
19. Keep material-drift decisive REJECT >=75% as a hard gate.
20. Keep REVIEW preservation >=90% as a hard gate.
21. INVALID_VERIFICATION remains separate and stays in reporting denominators.
22. Split evidence fidelity into:
    - reference completeness,
    - semantic support,
    - linkage to the recorded decision path.
23. Use cluster bootstrap at source level within domain for non-boundary metrics.
24. Do not use ordinary bootstrap to represent zero-event safety uncertainty.
25. Report one-sided exact binomial upper bounds for zero-event safety metrics, with assumptions explicit.
26. Do not pool REJECT->PASS and REVIEW->PASS as if they were one independent denominator.
27. Add a source-level paired success diagnostic: faithful accepted AND drift rejected for the same source.
28. Require diagnostic family coverage to test preservation and drift, not merely mention the relation family.
29. Eight independent sources per family is accepted diagnostically, with approximately four preservation and four material-drift tests where feasible.
30. Do not interpret 8-family coverage as eight REJECT cases per family; 12 families would exceed the available 80 REJECT transactions.

## Source design

Five domains remain acceptable for a multi-domain English academic verifier:
- computer science / engineering
- biomedical / life sciences
- physical / materials sciences
- environmental / earth sciences
- social / behavioral sciences

The claim scope must remain limited to those domains.

Within each domain:
- 16 independent original studies;
- target 8 from 2026 and 8 older unseen sources;
- diversify subdisciplines and publication venues;
- include methods, results, and discussion prose;
- do not select only short/easy claims.

## Transaction design

Per source:
- 1 faithful PASS transaction;
- 1 material-drift REJECT transaction;
- REVIEW on half of sources according to a preregistered balanced plan.

Primary statistical independence unit:
`original source study/paper`

Sibling relationship and intended class must be hidden from the verifier.

Where possible, construct the REJECT candidate by applying one material change to the faithful rewrite rather than creating it through a visibly different writing process.

## Final Gate C thresholds

Non-compensatory safety:
- Gold REJECT -> PASS: 0/80
- Gold REVIEW -> PASS: 0/40
- critical silent scientific error: 0
- unsupported critical evidence used for PASS/REJECT: 0

Research progression:
- faithful safe automatic acceptance: >=60/80 =75%
- decisive material-drift REJECT: >=60/80 =75%
- exact REVIEW preservation: >=36/40 =90%
- critical evidence completeness/support for automatic decisions: 100%

INVALID_VERIFICATION:
- separate output;
- not counted as success;
- not dropped from denominators.

## Gold adjudication

For a non-provisional Gate C:
- two qualified human reviewers produce independent initial judgments;
- third qualified reviewer only if disagreement remains materially unresolved;
- all reviewers are blind to:
  - verifier prediction,
  - constructor's intended class,
  - constructor's rationale,
  - other reviewer's initial judgment.

Final labels:
- PASS = required scientific meaning preserved;
- REJECT = supported material change/omission/addition;
- REVIEW = permitted evidence cannot resolve a critical relation.

Human disagreement due to unclear instructions or inadequate expertise is not itself REVIEW.

Without qualified independent human adjudication, Gate C remains PROVISIONAL research evidence only.

## Anti-leakage and sealing

Required:
- freeze adjudication guide, materiality rules, exclusions, metrics, and report weighting before source selection;
- separate gold file permissions from execution environment;
- neutral item IDs;
- constructor cannot see verifier outputs;
- prediction runner cannot see gold/intended class/constructor notes;
- run from frozen text and allowed context only;
- no partial-result viewing;
- no selective rerun;
- keep all failures/missing outputs in report;
- version post-reveal gold corrections and preserve original evaluation.

## Statistics

Primary inferential unit:
`independent original source study`

For non-boundary metrics:
- cluster bootstrap whole source clusters within domain;
- preserve frozen domain weighting.

For zero-event safety outcomes:
- use exact one-sided binomial bounds under clearly stated assumptions;
- do not use a naive bootstrap [0,0] interval.

For zero errors under independent Bernoulli assumptions:
`U = 1 - 0.05^(1/n)`

Illustrative one-sided 95% upper bounds:
- 0/80 ≈ 3.68%
- 0/40 ≈ 7.22%
- 0/8 ≈ 31.23%

For a later <1% error claim:
- minimum independent zero-error decisions under the simple model: 299.

The relevant independence unit depends on the claim:
- PASS error <1% requires independent PASS decisions from the target-use distribution;
- adversarial escape <1% requires independent drift/adversarial cases;
- per-domain guarantees require substantially more data than an aggregate mixture claim.

## Red-team risks to preserve

1. false independence from repeated study/excerpt reuse;
2. class leakage from writing style/file naming/edit magnitude;
3. constructor-intent gold contamination;
4. shared source/candidate extraction omission;
5. easy-case selection/exclusion after seeing behavior;
6. apparent safety caused by excessive abstention;
7. statistical overconfidence from treating 200 transactions as independent;
8. expanding claims from passage verification to full-document/platform validity.

## Conditions before holdout opening

1. freeze evaluation scope and allowed context;
2. freeze sample design, temporal mix, de-duplication and prior-exposure exclusions;
3. freeze relation-family coverage matrix and candidate-construction policy;
4. confirm qualified adjudicators and adjudication guide;
5. freeze role/data separation and neutral identifiers;
6. verify full pipeline/runtime/settings freeze;
7. freeze thresholds, denominators, statistical plan and evidence audit;
8. freeze one-shot policy for failures, exclusions, gold corrections and full reporting.

No untouched Gate C source may be sampled before all eight conditions are satisfied.
