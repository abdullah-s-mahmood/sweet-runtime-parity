# AT0-EN V2.4 Gate A4 — Pre-Consultation Readiness Assessment

Date: 2026-10-03
Status: PRE-CONSULTATION / NO IMPLEMENTATION AUTHORIZED

## Evidence considered

A1 deterministic anchors:
- 35/35 TP
- 0 FP
- 0 FN
- exact provenance 35/35

A2 structural source extraction:
- 47 source sentences
- 50 assertion candidates across 12 source cases
- 62% non-CERTAIN/abstention-like output
- decimal-splitting defect found by red-team and repaired before closure
- semantic accuracy not scored in A2

A3 semantic development validation:
- 6 development-only synthetic cases
- 28 gold assertions, 27 critical
- gold coverage: 100%
- critical coverage: 100%
- false additions: 0%
- atomic one-to-one: 88%
- overmerge: 12%
- certain precision: 92.86%
- error-abstention recall: 87.5%
- unnecessary abstention: 23.53%
- context detection recall: 100%
- critical silent semantic errors: 0
- assertion type accuracy: 86.36%
- predicate: 95.45%
- subject concepts: 90.91%
- object concepts: 100%
- polarity/modality/causality: 100% on scored one-to-one cases

## Important limitations

- development-only, not blind;
- only 6 synthetic cases;
- no authentic academic-document source extraction validation;
- no candidate-side extraction yet;
- no source/candidate alignment yet;
- no cross-domain evidence;
- no end-to-end V2.4 verifier score.

## Research synthesis

Current evidence supports five conclusions:

1. Claim-extraction quality should be judged across coverage, atomicity, faithfulness and decontextualization, not one aggregate score.
2. Decomposition and downstream verification interact; incorrect atomicity can reduce verification quality.
3. Evidence/subclaim alignment is a bottleneck; decomposition may degrade verification when evidence is not granularly aligned.
4. Conservative abstention can reduce error propagation, but excessive abstention harms usability.
5. Scientific claim-to-evidence reasoning remains difficult and extraction errors should not be hidden inside later alignment.

Key current sources reviewed:
- Claimify, ACL 2025
- Optimizing Decomposition for Optimal Claim Verification, ACL 2025
- The Alignment Bottleneck in Decomposition-Based Claim Verification, 2026
- CLAIM-BENCH, IJCNLP/AACL 2025
- current selective-prediction/abstention literature

## Internal red-team

### Argument for ACCEPT now
- all pre-registered A3 thresholds pass;
- zero observed critical silent semantic errors;
- many-to-many alignment is already part of V2.4 architecture and can theoretically tolerate legitimate split/merge;
- fixing every development imperfection before alignment risks overfitting the six consumed development cases.

### Argument for REPAIR first
- 12% overmerge means alignment would receive less atomic source graphs than intended;
- certain precision is only 2.86 pp above its threshold;
- unnecessary abstention is 23.53%;
- source extraction errors can propagate into alignment and make it impossible to attribute failure cleanly;
- current development set is too small to rely on a narrow PASS margin;
- known errors are structural classes (embedded propositions, comparative/procedural overmerge, coreference), not isolated IDs.

### Argument for REDESIGN
Not supported.
The representation and abstention architecture behaved as intended:
- coverage high;
- no false additions;
- observed material errors were generally routed to uncertainty;
- no observed critical silent semantic error.

## Preliminary implementation-agent decision

**REPAIR_TARGETED_FIRST**, not redesign.

Proposed limited repairs should target principles, not case IDs:

1. safer decomposition of explicit comparison coordinations such as `compared with` and `while` when both clauses have explicit owners;
2. safer procedural split of value bundles such as iterations + seed only when ownership remains identical and provenance is retained;
3. embedded proposition handling (`found that`) so wrapper predicates do not replace the scientific proposition;
4. explicit source-coreference representation instead of unresolved pronoun subject where a unique antecedent is locally recoverable;
5. separate assertion semantic type from scientific meaning preservation so type classification can improve without changing semantic claims;
6. reduce unnecessary abstention only if the above changes improve confidence on clean cases without creating any new critical silent error.

No alignment implementation should begin until this go/no-go decision is independently reviewed.

## Decision requested from higher-model consultant

Choose one:
- ACCEPT_AND_PROCEED_TO_ALIGNMENT
- REPAIR_TARGETED_FIRST
- REDESIGN_SOURCE_EXTRACTION

Implementation remains with the current agent.
