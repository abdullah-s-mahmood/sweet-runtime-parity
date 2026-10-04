# ACAD_PASS — Gate C EXT/META Readiness V2

Date: 2026-10-04
Status: DATASET/ADAPTER FREEZE AUTHORIZED / EXECUTION NOT AUTHORIZED

Protocol:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

## 1. Readiness ledger

| # | Condition | Status | Required evidence |
|---|---|---|---|
| 1 | Independent protocol review | PASS | Review decision V2 incorporated |
| 2 | Dataset artifacts/versions/access/licenses | SUBSTANTIAL PARTIAL / NOT PASS | User-supplied H1 ZIP bytes locally verified; manual-judgment MD5 matches publisher; local SHA-256 frozen for both archives; explicit reuse/license documentation still incomplete |
| 3 | Eligible splits/IDs/human-label provenance/context | SUBSTANTIAL PARTIAL / NOT PASS | Exact 2024 TSV physical schema, 400 abstract slots, 4,060 source sentences, 399 PMID clusters and row-level source reconciliation are frozen; final eligible subset/metric contract remains unfrozen |
| 4 | Dataset-specific adapter contracts + measurable-output mapping | H1 REDESIGNED / FACTPICO ARTIFACT FREEZE PENDING | PLABA-only hard H1 rejected; FactPICO selected as minimum hard H1 companion because full-abstract source/candidate context matches V2.4 interface; adapter contract still not ready |
| 5 | Overlap/source-cluster manifest | H1 INTERNAL PARTIAL / NOT PASS | H1 source-cluster rule frozen at PMID with 399 clusters and one duplicate PMID; cross-dataset overlap manifest remains future work |
| 6 | Metrics/thresholds/denominators/sample targets/statistics/evidence audit | H1 DESIGN PARTIAL / NOT PASS | H1 construct split resolved: FactPICO hard critical-fidelity candidate + PLABA diagnostic; exact FactPICO denominators/mappings/thresholds await artifact/schema freeze |
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
1. H1 label-function coverage is now strongly supported by TREC 2024 ACC+COM manual judgments, but exact TSV schema/record IDs and local artifact hashes remain unfrozen;
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


## 14. H1 access/artifact resolution checkpoint

Resolution file:
`H1_ACCESS_ARTIFACT_RESOLUTION_V1.md`

Commit:
`f88fe5b599ade9b85e6a301b350bc33c2163e331`

Major resolution:
- public Zenodo record `10.5281/zenodo.18637045` exposes raw PLABA 2023-2024 manual judgments;
- 2024 complete-rewrite judgment archive:
  `manual-judgments-task1-2024.zip`
  MD5:
  `589ad66e0b9324592f0151cc67974015`;
- public NIST/TREC URL for the original 2024 complete-adaptation corpus is identified;
- retrospective paper confirms 2024 ACC and COM manual axes over complete rewrite outputs for all 400 test abstracts;
- critical task-numbering mismatch is resolved and frozen;
- FaReBio identity/research-only access and expert-faithfulness construct are verified;
- SimpleText no longer needs to be a blocking H1 dependency.

Preferred H1 core candidate:
`TREC PLABA 2024 COMPLETE-REWRITE MANUAL JUDGMENTS`

Conceptual mapping:
- H1-S <- ACC
- H1-C <- COM

No binary adapter mapping is authorized yet.

Exact next H1 checkpoint:
`H1 RAW ARTIFACT + SCHEMA + TERMS FREEZE`


## 15. H1 raw artifact + schema + terms freeze checkpoint

Freeze file:
`H1_RAW_ARTIFACT_SCHEMA_TERMS_FREEZE_V1.md`

Commit:
`a4e4d01a6f3b0ff2dba6360327c523e587e1c282`

Frozen:
- canonical 2024 complete-rewrite judgment archive identity;
- Zenodo DOI/version;
- publisher MD5;
- public NIST/TREC source-corpus URL;
- 2023 raw physical schema as directly readable evidence;
- 2024 logical ACC/COM/SIM/BRV/FIN schema;
- original-abstract/PMID source-cluster rule;
- conservative TREC research-use / no-redistribution policy.

Still unresolved:
- local ZIP bytes and SHA-256;
- exact 2024 TSV physical headers;
- exact 400-record PMID manifest;
- explicit Zenodo license value;
- final H1 adapter/native metric contract.

Tooling limitation is now explicit:
the web source resolves the public ZIP, but current local runtime cannot materialize external binary bytes.

Exact next H1 checkpoint:
`H1 PHYSICAL SCHEMA + SOURCE-CLUSTER FREEZE`

Preferred resolution:
upload/materialize exactly:
1. `manual-judgments-task1-2024.zip`
2. `PLABA_2024-Task_2.zip`


## 16. H1 physical schema + source-cluster freeze checkpoint

Freeze file:
`H1_PHYSICAL_SCHEMA_SOURCE_CLUSTER_FREEZE_V1.md`

Commit:
`1cb73aa79658462d105be0de02f2e2acb6f16023`

User supplied both exact public ZIPs.

Raw integrity:
- `manual-judgments-task1-2024.zip`
  - size 7,054,073 bytes
  - MD5 `589ad66e0b9324592f0151cc67974015`
  - publisher MD5 match = YES
  - SHA-256 `8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce`
- `PLABA_2024-Task_2.zip`
  - size 231,126 bytes
  - MD5 `daa454a5234161489fef52eab1ebec26`
  - SHA-256 `f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e`

Exact 2024 TSV schema:
`Abstract, Sentence, Source, Target, Accuracy, Completeness, Simplicity, Brevity`

Source corpus:
- 40 questions
- 400 abstract slots
- 4,060 source sentences
- 399 unique PMIDs

Duplicate:
`PMID 15857353`
appears as:
- `Q14_A3`
- `Q37_A5`
with identical 7-sentence source text.

Therefore:
`MAX H1 INDEPENDENT SOURCE CLUSTERS = 399`

Judgment archive:
- 19 runs
- 76,790 retained judgment rows
- 14/19 runs contain all 4,060 source-sentence rows
- 5/19 runs contain missing rows
- 350 missing run×sentence rows total
- 315 unique source-sentence pairs missing in >=1 run
- 0 extra rows
- 0 empty targets
- every retained row source text exactly matches `test.json`

Score alphabet on all axes:
`-1, 0, 1`

Current exact next checkpoint:
`H1 ADAPTER + NATIVE METRIC CONTRACT FREEZE`


## 17. H1 adapter + native metric contract V2 checkpoint

Preferred contract:
`H1_ADAPTER_NATIVE_METRIC_CONTRACT_V2.md`

Commit:
`23a613da183157c14ef5c1c82051a5014dbca18e`

Review packet:
`H1_CONTRACT_V2_HIGHER_MODEL_REVIEW_PACKET.txt`

Review-packet commit:
`0f583d601f8d195797e597308887465864dd3c94`

Key V2 changes relative to V1:
1. confirmatory utility restricted to 14 complete PLABA runs;
2. hard safety retains all observed extreme-negative gold across all 19 runs;
3. exact Source==Target positive rows excluded from primary transformed-positive utility and retained as identity controls.

Gold strata:
- QUALIFIED_POSITIVE = ACC==1 AND COM==1
- QUALIFIED_NEGATIVE = ACC==-1 OR COM==-1
- all other cells = diagnostic only; 0 is NOT mapped to REVIEW

Primary H1 safety:
- all 19 runs
- 4,275 negative rows
- 396 negative-exposed PMID clusters
- any PASS_CANDIDATE = safety failure

Primary positive utility:
- 14 complete runs
- non-identical positive rows only
- 33,660 rows
- 399 PMIDs
- PMID-macro PASS_CANDIDATE >=75%

Primary negative utility:
- 14 complete runs
- 3,677 negative rows
- 394 PMIDs
- PMID-macro REJECT >=75%

Statistics:
- PMID cluster unit
- 10,000 bootstrap resamples
- seed 20261004
- 95% percentile CI
- exact one-sided zero-event upper bound for safety

Current status:
`H1 CONTRACT V2 SUPERSEDED BEFORE EXECUTION`

No V2.4 H1 prediction was run under V2.

Exact next checkpoint changed after duplicate/disagreement audit:
`USER-MEDIATED HIGHER-MODEL REVIEW OF H1 CONTRACT V3`


## 18. H1 contract V3 canonical-pair correction

Preferred contract:
`H1_ADAPTER_NATIVE_METRIC_CONTRACT_V3.md`

Commit:
`672bbc119eaa174e22365f5c4907bb47f9474a7d`

Independent review packet:
`H1_CONTRACT_V3_HIGHER_MODEL_REVIEW_PACKET.txt`

Packet commit:
`78e5562cba86b99655acc5c54cec277e1196cbc4`

Reason V3 was required before any prediction:
- 76,790 human rows collapse to 62,315 unique PMID+Source+Target prediction pairs;
- repeated identical text across runs must not create repeated deterministic V2.4 predictions;
- 1,340 canonical pairs have human class conflict and cannot receive a forced hard expected outcome;
- V2 complete-run selection could alter utility population based on run-level missingness rather than canonical gold availability;
- V3 uses every canonical pair with >=1 published human judgment and preserves external-gold missingness separately.

Frozen V3 classes:
- SAFE_STRICT: 40,609 pairs / 399 PMIDs
- ERROR_STRICT: 3,566 pairs / 396 PMIDs
- INTERMEDIATE: 16,800 pairs / 399 PMIDs
- HUMAN_CONFLICT: 1,340 pairs / 320 PMIDs

V3 hard rules:
- ERROR_STRICT automatic PASS = 0
- SAFE_STRICT pair-micro PASS >=75%
- SAFE_STRICT PMID-macro PASS >=75%
- ERROR_STRICT pair-micro REJECT >=75%
- ERROR_STRICT PMID-macro REJECT >=75%

V3 keeps exact-copy positives in the primary gold universe but requires explicit subgroup reporting.

V1 and V2 remain preserved and were never executed.

Current exact next checkpoint:
`USER-MEDIATED HIGHER-MODEL REVIEW OF H1 CONTRACT V3`

Until that review:
- no H1 adapter implementation;
- no V2.4 PLABA prediction;
- no H1 scoring.


## 19. H1 V3 independent review decision — context/gold blocker

Decision file:
`H1_CONTRACT_V3_INDEPENDENT_REVIEW_DECISION_V1.md`

Commit:
`5488022080f2d55265f1e12e168c5efef5e6c59f`

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Accepted:
- canonical PMID+Source+Target deduplication;
- HUMAN_CONFLICT remains diagnostic;
- score 0 is not REVIEW;
- single published expert rating may remain usable under narrow claims;
- pair-micro + PMID-macro framework;
- PMID-cluster bootstrap;
- zero unsafe PASS as a non-compensatory rule after eligibility is frozen.

Blocking issue verified from primary PLABA sources:
- PLABA sentence-level evaluation explicitly accounts for entire-abstract context;
- task/guidelines allow some omission, generalization and contextual resolution;
- these semantics are not automatically identical to ACAD_PASS strict protected-detail preservation.

Frozen V2.4 currently lacks a separate context channel that can provide PLABA interpretation context without making that context itself part of the preservation obligations.

Therefore:
`H1_NOT_READY_CONTEXT_GOLD_ALIGNMENT`

Required exact-copy correction:
primary transformed-positive utility must exclude `Source == Target` and report identity controls separately.

Current authorization:
`H1 CONTEXT + GOLD-SEMANTICS RESOLUTION`

Still forbidden:
- H1 adapter implementation;
- V2.4 PLABA predictions;
- H1 scoring;
- V2.4 modification;
- new-human recruitment;
- original custom Gate C opening;
- Arabic work.


## 20. H1 context + gold-semantics resolution

Resolution file:
`H1_CONTEXT_GOLD_SEMANTICS_RESOLUTION_V1.md`

Commit:
`0db47c57fc012dd95cc7a147b27745e5d8356314`

Design-level resolution:
- PLABA-only hard H1 is rejected because its human-gold semantics use abstract context and permit task-specific omission/generalization that is not equivalent to ACAD_PASS strict protected-detail preservation.
- No post-hoc PLABA hard subset will be created using surface/semantic filtering.
- PLABA remains an important diagnostic/authentic-transformation H1 track.
- FactPICO is selected as the minimum hard-H1 replacement/companion resource.

Why FactPICO:
- whole RCT abstract -> whole plain-language summary;
- no separate hidden context channel required by V2.4;
- expert ratings explicitly cover PICO elements and evidence inference;
- rating levels encode accurate, vague/inaccurate, missing critical descriptors, and missing;
- added-information spans and correctness are annotated;
- therefore it covers both H1-S factual support and H1-C critical-content preservation at a narrow RCT-critical-element scope.

FactPICO paper:
`10.18653/v1/2024.acl-long.459`

Official repository:
`lilywchen/FactPICO`

Observed main HEAD:
`2e16993a000aedb15cb348b7bcd61070d26bab14`

Repository license:
`MIT`

Separately hosted data artifact/license:
`NOT YET FROZEN`

Default diagnostic:
`InfoLossQA`
for information-loss characterization only; not promoted to hard because its QA representation would otherwise require semantic adapter logic.

Exact next checkpoint:
`FACTPICO ARTIFACT + SCHEMA + LICENSE FREEZE`

Still forbidden:
- V2.4 external predictions;
- H1 scoring;
- runtime modification;
- new-human recruitment;
- original custom Gate C opening;
- Arabic work.
