# ACAD_PASS — Gate C EXT/META Readiness V2

Date: 2026-10-04
Status: DATASET/ADAPTER FREEZE AUTHORIZED / EXECUTION NOT AUTHORIZED

Protocol:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

## 1. Readiness ledger

| # | Condition | Status | Required evidence |
|---|---|---|---|
| 1 | Independent protocol review | PASS | Review decision V2 incorporated |
| 2 | Dataset artifacts/versions/access/licenses | PARTIAL / NOT PASS | H1 identity/access audit completed; SimpleText annotation bytes/license and PLABA/TREC reusable artifacts still unresolved |
| 3 | Eligible splits/IDs/human-label provenance/context | PARTIAL / NOT PASS | H1 construct provenance clarified; exact SimpleText/TREC judgment IDs and final eligible records still unfrozen |
| 4 | Dataset-specific adapter contracts + measurable-output mapping | NOT READY | Frozen contract proving comparison to actual V2.4 outputs without new semantic inference |
| 5 | Overlap/source-cluster manifest | NOT READY | IDs/hashes/lineage/cluster counts |
| 6 | Metrics/thresholds/denominators/sample targets/statistics/evidence audit | NOT READY | Frozen per-track quantitative contract |
| 7 | META independent oracle/contracts/cases/seeds/exclusions | NOT READY | Oracle package independent from extractor/verifier semantics |
| 8 | Runtime + adapter identity | PARTIAL | V2.4 frozen; adapter hashes pending |
| 9 | Prior exposure + prediction/gold separation | NOT READY | Exposure register + frozen procedural separation |
| 10 | One-shot failure/exclusion/correction/retest/full-report policy | PARTIAL | EXT/META-specific closure required |

Overall:
`NOT_READY_GATE_C_EXT_META`

## 2. Current hard-track functional requirements

### H1
Must cover BOTH:
- H1-S: output-content support/factuality
- H1-C: preservation/completeness of required source content

Current candidate freeze order:
1. CLEF SimpleText human-annotated real-system material
2. eligible PLABA/TREC human judgments

Conditional gap fillers:
- FactPICO
- FaReBio

Diagnostic:
- LongSciVerify

Do not freeze final H1 membership until actual label schemas demonstrate coverage.

### H2
Primary:
`SciFact`

Before PASS readiness:
- prove exact measurable comparison to V2.4 outputs;
- freeze context policy;
- distinguish gold-evidence-conditioned evaluation from evidence retrieval.

### H3
Primary:
`QASemConsistency`

Before PASS readiness:
- trace parent dataset/source lineage;
- freeze relation-level denominator;
- preserve unsupported-label nuance;
- prevent gold QA decomposition from assisting inference;
- prove measurable comparison to V2.4 outputs without semantic helper.

### H4
Before PASS readiness:
- freeze independent oracle source/justification;
- applicability predicates;
- matched controls;
- per-family minimum case/source coverage;
- seeds;
- invalid-oracle handling;
- REVIEW ambiguity proof rule.

## 3. H1 freeze decision rule

Final H1 membership is based on construct coverage, not resource count.

A candidate resource may enter H1 only if its exact released human/expert annotations can support one or both of:
- H1-S
- H1-C

Final H1 must jointly cover both.

If SimpleText + eligible PLABA/TREC jointly cover both with adequate independent source clusters:
no extra hard resource is required.

If not:
choose the smallest conditional substitute that closes the documented gap.

## 4. Adapter contract mandatory fields

Each hard dataset must freeze:

1. dataset name/citation
2. release/version/date
3. license/access route
4. exact raw artifact files
5. raw hashes
6. native task
7. native labels
8. human/expert annotation provenance
9. annotator context/allowed evidence
10. source/candidate/context fields
11. eligible splits
12. eligible IDs
13. exclusions
14. V2.4 prediction input construction
15. actual V2.4 output field(s) being evaluated
16. exact mapping, if any
17. proof that mapping adds no semantic capability
18. denominator
19. metric
20. threshold
21. source-cluster unit
22. minimum sample/source-cluster target + justification
23. uncertainty method
24. zero-event treatment
25. missing/invalid-output treatment
26. evidence-location audit rule
27. semantic-support audit rule
28. overlap/lineage fields
29. prior-exposure note
30. adapter/config hash
31. prediction/gold separation method

No implicit mapping.

## 5. Semantic-adapter rejection test

A proposed adapter operation is INVALID if success would materially decrease without the adapter because the adapter itself:
- resolves entailment;
- resolves coreference/reference;
- resolves ambiguity;
- creates scientific claims/relations;
- corrects ownership/negation/scope/equations;
- selects evidence using gold rationale;
- infers a missing semantic label.

If invalid:
- remove it;
- or classify that track `NOT_READY`.

## 6. Evidence audit

Before execution freeze separately:

### Location/reference audit
Does the cited evidence point to the intended source material?

### Semantic-support audit
Does that material actually support the critical decision/relation?

Must freeze:
- eligible/auditable decision set;
- denominator;
- sampling or full-audit policy;
- required coverage;
- failure semantics.

Empty audit denominator cannot PASS.

## 7. Statistical freeze requirements

For each hard track specify:
- independence unit;
- source-cluster count;
- per-class count;
- target CI width or tolerated upper error bound or power target;
- resulting sample-size rationale;
- cluster-aware CI/bootstrap method;
- zero-event exact upper-bound method;
- invalid-output denominator policy;
- confirmatory vs diagnostic subgroup status.

Do not convert:
- relations;
- sentences;
- annotations;
- model outputs;
into independent source-study counts.

## 8. META independent-oracle freeze

For each family freeze:
- independent semantic statement of relation;
- source selection rule;
- applicability predicate;
- deterministic/seeded transformation;
- oracle outcome;
- proof/rationale template independent from extractor rules;
- prohibited cases;
- matched control;
- source cluster;
- immutable case ID;
- exclusion rule frozen before predictions.

For REVIEW cases:
oracle must establish unresolvedness, not merely absence.

## 9. Public benchmark exposure

Freeze an exposure register containing:
- dataset name;
- whether project agents inspected examples;
- whether examples appeared in previous consultations;
- whether adapter development used examples;
- whether labels were visible to implementers;
- mitigation/separation procedure.

Public exposure does not automatically invalidate the benchmark.
It limits the strength of the independence claim.

## 10. One-shot policy requirements

Before execution freeze:
- eligible IDs and denominators;
- adapter hashes;
- runtime hash;
- prediction input hashes;
- no selective retry policy;
- missing/invalid treatment;
- exclusion policy;
- gold-correction policy;
- post-result protocol-change policy;
- full negative-result reporting;
- versioning rule if any runtime/adapter change occurs.

## 11. Current blockers

Methodological blockers still open:
1. H1 label-function coverage is partially verified conceptually, but exact SimpleText/TREC record-level labels remain inaccessible/unfrozen;
2. actual H2 measurable-output mapping not yet frozen;
3. actual H3 measurable-output mapping not yet frozen;
4. dataset artifacts/licenses/versions not yet frozen;
5. overlap/source-cluster manifest absent;
6. per-track quantitative/statistical contracts absent;
7. META oracle package absent;
8. adapter identities absent;
9. exposure register absent;
10. final one-shot EXT/META policy absent.

These are readiness blockers, not V2.4 failures.

## 12. Authorized next checkpoint

`PRE-GATE-C EXT/META — DATASET / VERSION / SPLIT / ADAPTER / METRIC / OVERLAP FREEZE`

Scope:
- inspect actual candidate dataset releases;
- freeze exact files/versions/licenses;
- inspect exact label schemas;
- choose eligible splits/IDs;
- test adapter feasibility conceptually/structurally WITHOUT verifier predictions;
- define denominators and source clusters;
- calculate/justify sample targets;
- construct overlap manifest;
- draft META oracle contract.

Still forbidden:
- running V2.4 on external evaluation records;
- revealing/using gold to tune V2.4;
- opening original custom 80-study Gate C;
- recruiting new humans;
- changing V2.4.


## 13. H1 dataset/access audit checkpoint

Audit file:
`H1_DATASET_VERSION_ACCESS_LABEL_AUDIT_V1.md`

Audit commit:
`87485c350c148668fcba85fc6d6bca802b1c5001`

Key findings:
- SimpleText 2025 real human-annotated outputs remain a strong H1-S candidate.
- Official 2026 documentation confirms reuse of manual 2025 annotations as ground truth for information-distortion classification.
- SimpleText H1-C sufficiency is not yet established until the actual annotation artifact is inspected.
- PLABA original dataset identity is verified: 750 abstracts / 7,643 aligned sentence pairs.
- PLABA human references are not automatic full-preservation PASS gold because omission is permitted.
- TREC PLABA 2023 completeness/faithfulness is sampled over selected question-relevant sentences.
- TREC PLABA 2024 expert evaluation directly includes accuracy and completeness on complete abstract adaptation and is currently the strongest PLABA-family H1-C candidate.
- TREC 2024 reusable judgment artifact/access/license terms are not yet frozen.
- article/publication license must not be silently treated as dataset/judgment license.

H1 current state:
`PARTIAL FREEZE / ACCESS + ARTIFACT RESOLUTION REQUIRED`

Exact next H1 subcheckpoint:
`H1 ACCESS + ARTIFACT RESOLUTION`
