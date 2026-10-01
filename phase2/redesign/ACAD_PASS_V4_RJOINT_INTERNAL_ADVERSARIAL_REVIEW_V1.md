# ACAD_PASS V4 R_JOINT INTERNAL ADVERSARIAL REVIEW V1

Date: 2026-10-02
Status: COMPLETE
Verdict: **MODIFY BEFORE GOLD**
Review type: internal adversarial methodological review
Higher-model endpoint used: false
Gold/reference loaded: false

## 1. Scope

Reviewed:
- `MPSEF_V4_PRE_GOLD_DEVELOPMENT_MEASUREMENT_CONTRACT_V1.md`
- `MPSEF_RJOINT_V4_SOURCE_FREE_PREFLIGHT_CLOSURE_LOCK_V1.md`
- `mpsef_rjoint_score_v4.py`
- `mpsef_rjoint_v4_synthetic_preflight.py`
- `mpsef_rjoint_core_v2.py`
- Stage2 protocol-completion lock
- post-Stage2 research rebaseline
- historical `mpsef_rjoint_score_v3.py` for semantic comparison

No project gold/reference was opened.

## 2. Verdict

**MODIFY**

Findings:
- BLOCKER: **0**
- MAJOR: **4**
- MINOR: **3**

All findings are repairable pre-gold.

## 3. MAJOR findings

### M01 — composite M05 route semantics are not fully emitted by V4

The helper `whole_action_additional_target_bounds` exists and the synthetic suite proves one whole-action behavior.

However, `score_population_v4` currently reports only per-error-family recovery. It does not emit the frozen composite route:
`BOUNDARY={SPLIT,MERGE}`

and it does not emit the additional-target/additional-cluster route evidence that historical V3 used under M05.

Risk:
a later implementation could reconstruct BOUNDARY as `sum(max SPLIT, max MERGE)`, reintroducing the exact M05 defect already repaired historically.

Required repair:
- explicitly freeze composite route map;
- aggregate one whole action over the union of member target indices;
- emit group-vs-group additional target and cluster bounds under one-action semantics;
- add synthetic regression at population-output level, not helper-only level.

### M02 — punctuation exclusion and R_clean/extra-edit semantics are construct-ambiguous

Current V4 builds `primary_gold` by removing PUNCTUATION_ONLY edits, then evaluates actions against that reduced gold.

Consequence:
a candidate that correctly performs a punctuation edit present in the full reference can be counted as having an `extra` edit in the primary scorer because that punctuation gold was removed before M2 matching.

This can make `clean_target_recovery` conflate:
- true reference-unsupported extra edits;
- correct punctuation-only reference edits intentionally excluded from the primary target denominator.

Required repair:
- freeze all gold targets first;
- evaluate whole actions against the full reference for reference-supported/extra-edit accounting;
- derive primary non-punctuation target recovery from matched full-gold target indices;
- derive punctuation recovery separately;
- do not penalize a full-reference-supported punctuation correction as an extra edit;
- preserve a separately labelled historical-primary-only diagnostic only if desired for comparability.

### M03 — no exact production measurement input-lock wrapper exists yet

The scorer validates UID/source relationships but does not itself prove that the real measurement consumes:
- exact C_F source manifest SHA;
- exact V4 legal action-set SHA;
- exact scorer/core SHA;
- exact target builder/family map versions;
- exact gold source identity;
- exact environment identity.

This was acceptable for source-free testing but is insufficient for gold execution.

Required repair:
freeze a separate premeasurement input lock + wrapper before gold. The wrapper must fail closed on every frozen identity mismatch.

### M04 — candidate-availability gate semantics are underspecified in the V4 contract

Historical V3 had a frozen 95% candidate-availability interval gate.
V4 contract says to report gate state "where applicable" but does not explicitly state:
- which V4 group is gated;
- whether the 95% threshold is inherited;
- whether a new threshold exists;
- whether no automatic gate is intended.

Required repair:
freeze one interpretation before gold.

Recommended interpretation:
- preserve the historical **95%** threshold;
- apply it to the **ROSTER whole-action primary-target availability interval** only;
- proposer/family groups remain descriptive diagnostics;
- this is a development candidate-availability gate, not linguistic correctness.

## 4. MINOR findings

### N01 — clean sentence label needs decomposition

Current `clean_sentences` means zero primary non-punctuation targets.
It may include sentences with punctuation-only reference targets.

Required:
report separately:
- ALL_REFERENCE_CLEAN
- PUNCTUATION_ONLY_REFERENCE
- PRIMARY_ERROR_PRESENT

### N02 — frozen identity metadata should be embedded in final result

Final result should include:
- scorer version/SHA;
- core matching version/SHA;
- target family map version;
- action-set SHA;
- source manifest SHA;
- gold-input SHA/identity;
- punctuation policy version.

### N03 — same-family/cross-family wording

Cross-family exact output agreement may be credited to both family groups but must never be described as two independent votes producing a majority.

Wording must remain:
"shared legal whole-output availability", not "two votes".

## 5. Review questions

Q1 denominator freezing:
PASS.

Q2 historical exposure wording:
PASS.

Q3 source-only action availability:
PASS conceptually; production hash lock still required (M03).

Q4 proposer isolation:
PASS.

Q5 P1/P3 double counting:
PASS.

Q6 SWEET whole-action aggregation:
PASS for current recovery groups.

Q7 ROSTER whole-action semantics:
PASS.

Q8 M04:
PASS.

Q9 M05:
**MODIFY** — helper correct, population composite route evidence incomplete.

Q10 clean recovery:
**MODIFY** — punctuation construct issue.

Q11 complete repair:
PASS under the primary-target construct, but must be relabelled after M02 repair.

Q12 zero-target:
PASS mechanically; reporting categories need N01.

Q13 punctuation:
**MODIFY** under M02.

Q14 mixed punctuation/linguistic:
PASS in inherited target_scope.

Q15 single-reference limitation:
PASS in contract wording.

Q16 scorer failures:
PASS.

Q17 family-specific recovery:
PASS for individual families; composite route requires M01.

Q18 immutable identity:
**MODIFY** under M03.

Q19 hidden leakage:
PASS in current architecture; no embedded selector/P4/consensus path exists.

Q20 verdict:
**MODIFY BEFORE GOLD**.

## 6. Required new synthetic regressions

In addition to the existing 20:
21. full-reference punctuation correction is not counted as extra when primary denominator excludes punctuation;
22. punctuation recovery is reported separately;
23. all-reference-clean vs punctuation-only-reference sentence classification;
24. population-level BOUNDARY={SPLIT,MERGE} one-whole-action aggregation;
25. population-level additional-target/additional-cluster M05 evidence;
26. 95% ROSTER gate PASS/FAIL/INCONCLUSIVE exact integer semantics;
27. production identity mismatch contract helper fails closed.

Minimum next preflight:
**27/27 PASS**

## 7. Required remediation

Create:
- contract amendment A1;
- new scorer version (do not overwrite frozen V4 evidence);
- expanded source-free synthetic preflight;
- production premeasurement input-lock design.

Rerun source-free preflight:
**YES**

Gold loading after remediation:
**NOT YET** — only after expanded preflight PASS and remediation closure review.

## 8. Higher-model note

No separate higher-model endpoint was available in this tool environment.

A focused review packet already exists:
`ACAD_PASS_V4_RJOINT_PRE_GOLD_ADVERSARIAL_REVIEW_PACKET_V1.md`

No claim is made that this internal review is an external/higher-model review.

## 9. Classification

**IMPROVED METHODOLOGICALLY / GOLD REMAINS CLOSED**
