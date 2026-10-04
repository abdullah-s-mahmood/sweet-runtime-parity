# ACAD_PASS — FactPICO H1 V4 Focused Independent Review Decision V1

Date: 2026-10-04
Status: ACCEPTED WITH ESSENTIAL CHANGES / CHANGES INCORPORATED INTO V5

Reviewed contract:
`H1_FACTPICO_HARD_GOLD_CONTRACT_V4.md`

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

No V2.4 FactPICO prediction has been run.

## 1. Accepted decisions

### N/A policy
Retain full-source exclusion from hard H1 when any PICO field is N/A/0.

Frozen:
- 3 source clusters
- 9 summary records
- diagnostic only

Rationale:
the hard scope is intentionally restricted to fully applicable RCT PICO cases.

### Double-annotated PICO hard-error rule
Retain:
`released averaged PICO <= 1.5`

only when:
- source is in the known double-PICO subset;
- N/A source clusters are excluded;
- score is the published arithmetic aggregate.

This guarantees both underlying 1–4 ratings lie in the severe-error/missing region {1,2}.

A released value of 2.0 is NOT hard-error gold because it can represent disagreement such as (1,3).

### Thresholds
Retain:
- pair-micro >=75%
- source-macro >=75%

for both:
- decisive ERROR_STRICT rejection
- limited SAFE_STRICT_CONTROL automatic acceptance

These are research-progression thresholds on the frozen benchmark, not population guarantees.

## 2. Essential change — Results negative trigger removed

V4 proposed:
`Results <=2`
as an independent ERROR_STRICT trigger.

The reviewer rejected this because `Results` is a summary-level aggregate over multiple finding-level judgments and may also aggregate multiple human observations.

The released artifact does not expose raw numeric human score per individual finding.

Therefore V5 removes:

`Results <=2 -> ERROR_STRICT`

entirely.

Results remains:
- a required positive condition when `Results=4` for SAFE_STRICT_CONTROL;
- diagnostic/ordinal evidence for all other records.

Why Results=4 remains acceptable for a strict positive control:
all contributing Evidence Inference ratings are bounded by 1–4, so an arithmetic aggregate of exactly 4 requires every contributing rating to equal 4, assuming the published averaging contract.

No negative claim is inferred from an aggregate <=2.

## 3. Essential change — Added Information safe-control proof

Reviewer required proof that absence of an Added Information row means no highlighted addition, rather than missing annotation.

Primary-source verification establishes:
- FactPICO evaluates the generated summaries with questions addressing PICO and information added by LLMs;
- annotators are asked to highlight addition spans and assess their factuality;
- all 75 double-annotated summaries received the Added Information questions independently;
- the release stores Added Information as span-event rows rather than one row per summary.

Therefore V5 interprets absence of an Added Information span row as:
`NO HIGHLIGHTED ADDITION SPAN IN THE RELEASE`

only under these safeguards:

1. record is one of the frozen 345 canonical FactPICO records;
2. exact source/candidate identity is valid;
3. record has no exact Added Information span row;
4. source cluster is not among the 15 clusters containing an Added Information export row whose candidate identity is corrupted/unresolved.

If any identity ambiguity exists:
`ADDED_INFO_STATUS = UNKNOWN`

and the record cannot enter SAFE_STRICT_CONTROL.

This is a conservative export-integrity rule.

## 4. Safe-control decision

Reviewer verdict:
`REDEFINE`

V5 safe-control definition:

- non-N/A source;
- all PICO fields exactly 4;
- Results exactly 4;
- no exact released Added Information span;
- no unresolved Added Information identity in its source cluster.

Recalculation:
- 34 records
- 33 source clusters

Model mix:
- ALPACA: 33
- GPT-4: 1
- LLAMA-2: 0

The count remains unchanged after the corrected eligibility proof.

This remains a mandatory LIMITED positive anti-degeneracy gate.

It does NOT support:
- broad transformation diversity;
- Llama-2 safe-acceptance claims;
- reliable GPT-4-specific safe-acceptance claims.

If this limited positive gate fails, H1 cannot receive a full pass even if error detection succeeds.

## 5. Final ERROR_STRICT after review

Hard error trigger is now PICO-only.

For non-double PICO records:
any applicable P/I/C/O <=2.

For double-PICO aggregate records:
any applicable P/I/C/O <=1.5.

N/A source clusters are excluded from hard gold.

Final recalculated ERROR_STRICT:
- 149 records
- 83 source clusters

Model distribution:
- ALPACA: 35
- GPT-4: 45
- LLAMA-2: 69

Results does not independently add any record to ERROR_STRICT.

## 6. Final remaining classes

Prediction universe:
`345 records / 115 source clusters`

Final V5 classes:

- SAFE_STRICT_CONTROL: 34 records / 33 source clusters
- ERROR_STRICT: 149 records / 83 source clusters
- INTERMEDIATE: 153 records / 84 source clusters
- N_A_SOURCE_DIAGNOSTIC: 9 records / 3 source clusters

Counts sum to 345.

Source-cluster class counts overlap because one source may have different candidate classes across the three generated summaries.

## 7. Final eligibility manifest

Final metadata-only V5 eligibility manifest:

`FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5.csv`

Rows:
`345`

SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

This supersedes the V4 proposal manifest hash.

No raw source/candidate text is required in the public eligibility manifest.

## 8. Safety bound update

Final ERROR_STRICT source-cluster denominator:
`83`

If zero source clusters contain an unsafe automatic PASS:

one-sided exact 95% simple binomial upper bound:

`1 - 0.05^(1/83) ≈ 3.54496%`

The V4 value based on 91 clusters is superseded and MUST NOT be reused.

This is benchmark-cluster evidence only.

## 9. Current authorization

Independent review explicitly authorizes, AFTER these changes:

`DETERMINISTIC ADAPTER + INPUT MANIFEST + SEPARATE GOLD MANIFEST IMPLEMENTATION AND HASHING`

Still NOT authorized:
- V2.4 execution on FactPICO;
- H1 scoring;
- threshold changes;
- V2.4 modification;
- new-human recruitment;
- original custom Gate C opening;
- Arabic-track work.

## 10. Exact next checkpoint

`FACTPICO H1 ADAPTER + INPUT/GOLD MANIFEST IMPLEMENTATION FREEZE`
