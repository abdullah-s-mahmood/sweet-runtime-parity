# AT0-EN V2.6-DEV — R4.1B Open-30 Coverage Addendum V1

Date: 2026-10-05
Status: FROZEN BEFORE R4.1B IMPLEMENTATION

## Trigger

R4.1 has passed all synthetic/mechanics safety suites:
- legacy mechanics: 260/260
- R4 surface suite: 120/120
- safe biomedical paraphrases: 30/30 PASS_CANDIDATE
- critical biomedical mutations: 40/40 REJECT
- compression/material omission: 20/20 PASS_CANDIDATE
- unsafe critical PASS: 0

However, the already-open 30-RCT development diagnostic remains below the frozen pre-holdout coverage gate:
- total assertions: 394
- unresolved predicates: 225 / 394 = 57.11%
- non-CERTAIN assertions: 227 / 394 = 57.61%
- short fragments <=3 chars: 0
- empty documents: 0
- >128-assertion documents: 0

Required before opening the 60-RCT internal holdout remains unchanged:
- unresolved <=35%
- non-CERTAIN <=40%
- short fragments =0
- empty documents =0
- >128 assertions/doc =0

## Open-30 unresolved audit

Audit artifact:
AT0_EN_V26_R4_OPEN30_UNRESOLVED_AUDIT_V1

Dominant categories overlap because one sentence may contain several scientific roles:
- population: 95
- intervention: 82
- follow-up: 52
- statistics: 51
- result direction: 44
- outcome: 36
- randomization: 26
- conclusion: 20
- safety: 15
- objective: 9
- other: 37

This addendum uses only the already-open 30-document development set. The 60-document holdout remains unopened.

## R4.1B authorized generic surface families

1. COUNT_ONLY_OR_PREFIXED_POPULATION
   - explicit human population counts, including temporal prefixes and adjective-modified population nouns.
   - exact count binding required.

2. STUDY_OBJECTIVE
   - explicit aim/objective/purpose/evaluate/assess/compare/investigate constructions.
   - MATERIAL unless the sentence itself asserts a clinical result.

3. OUTCOME_DEFINITION_VARIANTS
   - main/primary/secondary endpoint/outcome formulations, including "among the endpoints", "main study endpoint", and "endpoint was to record".
   - CRITICAL.

4. NO_DIFFERENCE_AND_SIGNIFICANCE
   - explicit "no difference", "did not differ", "not significantly different", and equivalent surface constructions.
   - CRITICAL; polarity preserved.

5. NUMERIC_RESULT_SURFACE
   - explicit outcome/rate/incidence/survival/response/event statements with numeric/percentage/ratio evidence.
   - CRITICAL when outcome/result-bearing.
   - all quantities remain exact bindings.

6. SAFETY_TOLERABILITY
   - explicit death/adverse-event/toxicity/tolerability assertions.
   - CRITICAL; negation preserved.

7. EFFECT_EFFICACY_CONCLUSION
   - explicit effective/superior/beneficial/effect/conclusion claims with modality such as appears/seems/may preserved.
   - CRITICAL when asserting treatment effect; generic recommendation/rationale may remain MATERIAL.

8. EXPLICIT_METHOD_STATISTICS
   - two-sided tests, regression/model/assay/computation/assessment procedure statements.
   - MATERIAL unless they contain a clinical outcome claim.

9. FOLLOW_UP_PROCEDURE
   - explicit follow-up schedules, assessment procedures, and performed procedures.
   - MATERIAL unless intervention/outcome semantics make them CRITICAL.

10. STUDY_DESIGN_OR_TITLE_METADATA
   - randomized/controlled/phase/trial/study title/design statements not already captured by more specific critical parsers.
   - MATERIAL.

## Anti-overfitting constraints

- No PMID-specific logic.
- No FactPICO text or labels.
- No exact sentence whitelist.
- No threshold changes.
- No conversion of residual ambiguity to CERTAIN unless an explicit surface construction matches.
- Existing specialized parsers retain priority.
- Existing 260 + 120 suites must remain fully passing.
- Holdout remains closed until the unchanged 30-RCT pre-open thresholds are met.

## STOP

Implement R4.1B and rerun only:
1. 260 mechanics suite;
2. 120 R4 surface suite;
3. already-open 30-RCT diagnostic;
4. already-open unresolved audit.

Do NOT open the 60-RCT internal holdout unless the pre-open gate is met.
