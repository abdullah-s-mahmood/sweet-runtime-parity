# Phase 2 — WAW_ALIF Gate End Brainstorm

Date: 2026-09-28

## What survived

- complete edit-event representation;
- REVIEW as a first-class outcome;
- source-validity veto for valid singular/root-waw and nominal-waw forms;
- natural-corpus evaluation after frozen runtime decisions;
- counterfactual falsification as a complementary safety test.

## What failed

- local shape alone;
- candidate plural-verb morphology alone;
- candidate plural-verb morphology + source unanalyzability as sufficient auto-accept proof;
- requiring source lexical plural analysis (coverage collapses to zero).

## New failure family

**Missing-clitic vs missing-alif ambiguity**

A malformed token ending in و can be repaired in more than one way:
- terminal واو الجماعة + differentiating alif;
- non-terminal واو الجماعة + attached enclitic, where no alif is written.

A verifier that sees only the token cannot always distinguish them.

## Best next experiments

### A. Cross-corpus independent agreement — PRIORITY 1
Rather than invent another hand rule, run the strongest independent candidate systems on an untouched external slice and evaluate exact edit-event consensus.

### B. Parser-assisted context — PRIORITY 2
Use dependency structure only as an additional evidence source:
- controller/subject number;
- explicit object/complement;
- token dependency role;
- candidate/source parse stability.

Never let parser output be the sole oracle.

### C. Expand counterfactual suite — PRIORITY 3
Create paired cases where only context changes the valid correction. Require the verifier to abstain when the local form is ambiguous.

## Avoid

- more GED thresholds;
- lexical exception lists;
- hardcoding specific verbs;
- promoting Recovery from 3/4;
- counting Strict 0/0 as 100%;
- using ZAEBUC TEST;
- starting Phase 3.
