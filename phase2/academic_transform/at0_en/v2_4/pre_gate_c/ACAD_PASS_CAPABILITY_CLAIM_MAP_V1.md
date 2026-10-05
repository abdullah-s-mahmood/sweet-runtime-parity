# ACAD_PASS — Capability / Claim / External-Evidence Map V1

Date: 2026-10-05
Status: CURRENT STRATEGIC AUTHORITY BEFORE FACTPICO PREDICTION

Purpose:
prevent any benchmark result from being interpreted as evidence for a broader construct than it actually measures.

## 1. Permanent strategic rule

`CONSTRUCT-MODULAR EXTERNAL VALIDATION`

ACAD_PASS must not use one benchmark as proof of the full pipeline.

Each capability receives:
- its own claim boundary;
- its own best-matched external evidence;
- hard-gate vs diagnostic status;
- separate readiness state.

## 2. Current capability map

| Capability | Current external evidence | Current status | Allowed claim |
|---|---|---|---|
| Critical RCT/PICO preservation/fidelity | FactPICO V5 | HARD SUBGATE / READY FOR PRE-PREDICTION INTEGRITY | Source-bounded critical RCT-element fidelity only |
| General information-loss / omission detection | InfoLossQA | FUTURE COMPLEMENT / NOT RUN | Ability to identify simplification-induced missing information |
| Authentic biomedical simplification behavior | PLABA | DIAGNOSTIC | Behavior on expert-rated biomedical plain-language transformations under PLABA semantics |
| Scientific revision usefulness/correctness | ParaReval / ParaRev / later XtraGPT-style revision evidence | FUTURE TRACK | Revision utility/instruction-following/correctness, not scientific preservation alone |
| Scientific claim support/contradiction | SciFact baseline; SciVer expansion candidate | FUTURE H2 | Claim-evidence support under benchmark-native labels |
| Predicate-argument relation fidelity | QASemConsistency | FUTURE H3 | Local supported/unsupported predicate-argument relations |
| Clinical numerical/comparison/condition reasoning | NLI4CT + 2026 inference-type annotations | FUTURE H3 COMPLEMENT | Entailment/evidence retrieval over clinical-trial conditions, comparisons, and numerical relations |
| Citation semantic support | SciCiteVal / CiteAudit candidates | FUTURE DISTINCT TRACK | Citation-to-claim correctness, not merely DOI existence |
| Citation identity/metadata/retraction | academic-refchecker + metadata/retraction services | ADAPT/INTEGRATE | Reference identity/state integrity |
| Long-document scientific factual consistency | LongSciVerify / related long-document factuality resources | FUTURE COMPLEMENT | Long-document consistency, not omission completeness |
| Structural document integrity | Docling/GROBID/Pandoc/ChkTeX and deterministic checks | ADAPT/INTEGRATE | Structure/reference/cross-link integrity only |
| Provenance / transformation lineage | W3C PROV-O + Web Annotation + ACAD_PASS hashes/IDs | REUSE + BUILD | Traceability, not semantic correctness |
| Uncertainty / abstention | ACAD_PASS PASS/REJECT/REVIEW/INVALID + future selective-prediction calibration | BUILD + EXTERNAL CALIBRATION | Bounded selective automation |
| Drift / regression after repair | ACAD_PASS META + MrDre/EditPropBench-like future evidence | BUILD + FUTURE BENCHMARKING | Change-impact regression detection |
| Repair + re-verification | ACAD_PASS controlled loop | BUILD / NOT YET EXTERNALLY PROVEN | Local repair with dependency-aware re-verification |

## 3. FactPICO interpretation lock

A future FactPICO V5 PASS means only:

“Frozen AT0-EN V2.4 met preregistered research-progression criteria for source-bounded critical RCT-element fidelity on FactPICO.”

It MUST NOT be described as proof of:
- complete H1;
- general information preservation;
- general scientific revision quality;
- citation correctness;
- document-wide structural integrity;
- repair safety;
- production readiness;
- universal academic fidelity.

## 4. H1 strategic split

H1 is no longer a single undifferentiated construct.

### H1-A — Candidate support/factual consistency
Question:
Are the scientific statements present in the candidate supported by the source?

Current evidence:
- FactPICO critical RCT dimensions;
- later FaReBio/other support resources if needed.

### H1-B — Required-information preservation
Question:
Did the transformation omit information that should have remained?

Current evidence:
- FactPICO only for critical RCT/PICO omissions;
- InfoLossQA is the primary future complement for broader information loss.

### H1-C — Revision usefulness
Question:
Did the requested revision improve the document appropriately while respecting the task?

Future evidence:
- ParaReval / ParaRev;
- later context-aware scientific revision resources.

These subconstructs must never be averaged into one compensatory score.

## 5. H2 strategic direction

Keep:
`SciFact`
as a clean established textual baseline if adapter compatibility remains valid.

Audit before execution:
`SciVer`
for broader expert scientific evidence verification.

Important:
benchmark labels such as SUPPORT / CONTRADICTION / NEI are not automatically equivalent to ACAD_PASS:
PASS / REJECT / REVIEW.

If frozen V2.4 outputs cannot be mapped without semantic helper inference:
`TRACK = NOT_READY`.

## 6. H3 strategic direction

Primary relation-localization candidate:
`QASemConsistency`

Clinical numeric/comparison complement:
`NLI4CT`

Known QASemConsistency limitation:
predicate-argument decomposition can miss implicit inter-sentence discourse/causal relations.

Therefore ACAD_PASS-specific relation tests remain necessary for:
- ownership;
- denominator/baseline binding;
- causality vs association;
- cross-sentence scope;
- implicit discourse relations.

## 7. H4 / META

Retain an independent metamorphic track.

External literature may improve perturbation families, but MUST NOT replace:
- independent oracle semantics;
- bidirectional safe/unsafe transformation tests;
- frozen critical invariants.

No consumed custom set may be relabeled as a clean holdout.

## 8. Distinct citation track

Citation/reference integrity must remain separate from generic H2.

Five distinct checks:
1. reference identity/existence;
2. version/retraction/state;
3. citation placement and ownership;
4. semantic support of claim;
5. adequacy of attribution for content requiring citation.

A valid DOI proves none of 3–5.

## 9. Structural track

Use existing tools for:
- PDF/document parsing;
- bibliography extraction;
- cross-references;
- figure/table/equation IDs;
- acronyms;
- links;
- numbering.

Do not build:
- general OCR;
- general academic editor;
- global scientific search engine
from scratch unless a specific unsolved requirement remains.

## 10. Novelty boundary

Do NOT claim:
“first AI scientific writing checker/editor.”

Defensible research hypothesis instead:

A scientific editing pipeline governed by explicit preservation obligations, independent evidence verification, non-compensatory safety gates, provenance, dependency-aware repair, and re-verification reduces material scientific regression at comparable useful-edit acceptance and cost.

This remains a hypothesis to test.

## 11. Evidence hierarchy

Prefer:
1. expert/human gold that matches the construct;
2. published benchmark-native metrics;
3. externally frozen datasets;
4. independent metamorphic oracle tests;
5. diagnostic automatic metrics.

Never let:
- LLM-as-judge;
- semantic adapter inference;
- internally generated gold
silently replace external gold for hard claims.

## 12. Current operational consequence

Before FactPICO:
- do NOT add another benchmark;
- do NOT alter FactPICO V5;
- do NOT broaden the claim;
- complete pre-prediction integrity only.

After FactPICO:
- freeze predictions before gold join;
- report V5 unchanged;
- then decide whether InfoLossQA is the next H1 complement based on the exact remaining claim gap.

## 13. Supersession

This file is the current authoritative capability/claim map for external-validation interpretation.

Older documents remain historical evidence and must not override these claim boundaries.
