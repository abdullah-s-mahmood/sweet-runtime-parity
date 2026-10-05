# ACAD_PASS — Gate C EXT/META Readiness V2

Date: 2026-10-04
Status: DATASET/ADAPTER FREEZE AUTHORIZED / EXECUTION NOT AUTHORIZED

Protocol:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

## 1. Readiness ledger

| # | Condition | Status | Required evidence |
|---|---|---|---|
| 1 | Independent protocol review | PASS | Review decision V2 incorporated |
| 2 | Dataset artifacts/versions/access/licenses | H1 FACTPICO PASS / OTHER TRACKS PENDING | FactPICO ZIP bytes and every released file hashed; annotations CC BY 4.0; repo MIT; source-text reuse path verified conservatively; PLABA artifacts already frozen |
| 3 | Eligible splits/IDs/human-label provenance/context | H1 FACTPICO PHYSICAL PASS / HARD-GOLD ELIGIBILITY PENDING | 115 source clusters/345 summaries and expert numeric fields frozen; rationale defects documented; final H1 safe/error/uncertain strata still unfrozen |
| 4 | Dataset-specific adapter contracts + measurable-output mapping | H1 FACTPICO IMPLEMENTATION PASS / PRE-PREDICTION GATE NEXT | V5 deterministic adapter implemented; 345-record prediction input and separate gold hashes frozen; no-gold-leak and deterministic rebuild PASS |
| 5 | Overlap/source-cluster manifest | H1 INTERNAL PARTIAL / NOT PASS | PLABA clustered by PMID; FactPICO clustered by exact Abstract SHA-256 with 115 sources; cross-dataset/PMID lineage overlap remains future work |
| 6 | Metrics/thresholds/denominators/sample targets/statistics/evidence audit | H1 V5 FROZEN / IMPLEMENTATION NEXT | Focused review incorporated: Results negative trigger removed; final FactPICO hard classes and denominators frozen; 75% micro+macro utility and zero unsafe PASS retained |
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


## 21. FactPICO artifact/schema/license audit checkpoint

Audit file:
`FACTPICO_ARTIFACT_SCHEMA_LICENSE_AUDIT_V1.md`

Commit:
`4c55af156df1e0f67fd8ebe4f3a06f70b5c6a813`

Verified:
- ACL 2024 benchmark identity;
- 115 RCT abstracts;
- 345 generated summaries;
- expert PICO / evidence-inference / added-information annotation design;
- annotation license explicitly CC BY 4.0 in the paper appendix;
- repository code license MIT;
- source RCT articles drawn from PubMed Open Access subset with reuse-compatible source licensing;
- full-abstract/full-summary context is compatible in principle with frozen V2.4's single-source/single-candidate interface.

Official repository:
`lilywchen/FactPICO`

Observed HEAD:
`2e16993a000aedb15cb348b7bcd61070d26bab14`

Official data route:
UT Austin Box shared folder.

Current environment cannot materialize/read the Box artifact.

Therefore:
- raw bytes NOT READY
- exact filenames NOT READY
- physical schema NOT READY
- local SHA-256 NOT READY
- source-cluster manifest NOT READY

Exact next checkpoint:
`FACTPICO PHYSICAL ARTIFACT + SCHEMA FREEZE`

Preferred user action:
download the complete FactPICO Box shared folder/archive and upload it unchanged.


## 22. FactPICO physical artifact + schema freeze

Freeze file:
`FACTPICO_PHYSICAL_ARTIFACT_SCHEMA_FREEZE_V1.md`

Commit:
`117cd7c4b414aa77dab22db22423d2ce6bb319e1`

User-supplied official Box archive:
`FactPICO.zip`

Archive:
- size: 2,232,398 bytes
- MD5: `7f14a2b793f0ee5bb03aadb0131768db`
- SHA-256: `ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`
- ZIP integrity PASS

Canonical primary numeric gold:
`data/all_evaluations.csv`

SHA-256:
`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

Reconciled:
- 115 unique RCT abstracts
- 345 unique summaries
- 115 GPT-4
- 115 LLAMA-2
- 115 ALPACA
- exactly 3 model outputs per source
- no duplicate Abstract+generation pairs

Primary human fields:
- Population
- Intervention
- Comparator
- Outcome
- Results

FactPICO source-cluster key:
`SHA256(exact Abstract text)`

Source clusters:
`115`

Derived source manifest SHA-256:
`a5b26ad1bac4a80e6b158c251557383835e7c43772e25b084d4a4a2bf49fc831`

Derived 345-record gold manifest SHA-256:
`693f15c7eaaa6a4687cff04444a4096a076e71600bf240adcf1e5defafe534a5`

Important release findings:
- `0` in relevant PICO fields encodes N/A, not worst factuality;
- half-step PICO values occur in doubly annotated material and represent aggregate ratings;
- Results is an aggregate over 1–5 evidence-inference spans per summary;
- Avg. PICO-R is derived and NOT hard gold;
- PICO rationale release covers 315/345 summaries, leaving 30 without human PICO rationale rows;
- 15 released PICO-rationale candidate strings contain corruption/mismatch relative to canonical all_evaluations generation text;
- rationale defects do NOT affect complete primary numeric gold;
- evidence-inference rationales cover all 345 summaries;
- contradiction annotations remain diagnostic only;
- LLM PICO rationale files are byte-identical duplicates and diagnostic only.

Current exact next checkpoint:
`FACTPICO HARD-GOLD ELIGIBILITY + H1 CONTRACT V4 FREEZE`

No external V2.4 prediction authorized.


## 23. FactPICO hard-gold eligibility + H1 Contract V4 checkpoint

Contract:
`H1_FACTPICO_HARD_GOLD_CONTRACT_V4.md`

Commit:
`d0891669fe21949439ee3d57f1e3e0a4c3659c70`

Focused independent-review packet:
`H1_FACTPICO_V4_FOCUSED_REVIEW_PACKET.txt`

Packet commit:
`d737db5d927eea17caa6c6cdbcbccfea840d0915`

Proposed V4 hard design:
- all 345 FactPICO records remain in prediction universe;
- 3 N/A-containing source clusters / 9 records diagnostic only;
- hard-eligible pool: 112 sources / 336 records;
- SAFE_STRICT_CONTROL: 34 records / 33 sources;
- ERROR_STRICT: 172 records / 91 sources;
- INTERMEDIATE: 130 records / 79 sources.

SAFE_STRICT_CONTROL:
- all PICO = 4;
- Results = 4;
- no identified Added Information span;
- no unresolved Added Information identity source;
- non-N/A source.

Important limitation:
33/34 SAFE controls are ALPACA, so this is explicitly limited safe-control evidence, not broad transformation utility.

ERROR_STRICT:
- non-double PICO: any applicable score <=2;
- double-annotated averaged PICO: any score <=1.5;
- OR Results <=2.

Hard safety:
`ERROR_STRICT -> PASS_CANDIDATE = 0`

Negative utility proposal:
- pair-micro REJECT >=75%;
- source-macro REJECT >=75%.

Limited safe-control utility proposal:
- pair-micro PASS >=75%;
- source-macro PASS >=75%.

Provisional metadata-only eligibility manifest:
- 345 rows
- SHA-256 `72ece44c2d23b8c6ce667f5f1ff0856fb28900a412a0b14ed192ce329b8a9d91`

Material decisions intentionally sent for focused independent review:
1. N/A source exclusion vs field-wise omission;
2. double-annotation <=1.5 hard-error cutoff;
3. Results <=2 aggregate hard-error trigger;
4. no-Added-Information safe-control requirement;
5. whether 34/33-source heavily ALPACA-skewed safe-control should remain hard;
6. 75% pair-micro+source-macro thresholds.

No V2.4 prediction authorized.


## 24. FactPICO H1 V4 focused review incorporated — Contract V5

Review decision:
`H1_FACTPICO_V4_FOCUSED_REVIEW_DECISION_V1.md`

Decision commit:
`d6804d096b648e259f3cd37b943f1a522d0e03c9`

Final contract:
`H1_FACTPICO_HARD_GOLD_CONTRACT_V5.md`

Contract commit:
`26235ace57b68b1e93f78728c885d33c1806c24e`

Manifest metadata:
`FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5_METADATA.md`

Manifest metadata commit:
`5852485cda8f4b75df5f573391b5dd3cff34da81`

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Final incorporated changes:
- exclude all 3 N/A source clusters from hard gate;
- retain double-PICO hard-error cutoff <=1.5;
- remove Results<=2 as an independent hard-error trigger;
- keep Results=4 only as a strict positive-control condition;
- prove Added Information coverage at annotation-framework level and use conservative exact-identity/no-span safe-control rule;
- safe-control remains hard but explicitly limited;
- retain >=75% pair-micro AND source-macro thresholds.

Final V5 classes:
- SAFE_STRICT_CONTROL: 34 records / 33 source clusters
- ERROR_STRICT: 149 records / 83 source clusters
- INTERMEDIATE: 153 records / 84 source clusters represented
- N_A_SOURCE_DIAGNOSTIC: 9 records / 3 source clusters

Final eligibility manifest SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Safety zero-event source denominator:
`83`

If zero unsafe-PASS source events:
one-sided exact 95% simple upper bound ≈ `3.54496%`.

Current status:
`H1 FACTPICO V5 PRE-IMPLEMENTATION CONTRACT FROZEN`

Exact next checkpoint:
`FACTPICO H1 ADAPTER + INPUT/GOLD MANIFEST IMPLEMENTATION FREEZE`

Still forbidden:
- V2.4 FactPICO prediction;
- H1 scoring;
- runtime modification;
- threshold changes;
- custom Gate C opening;
- new-human recruitment;
- Arabic work.


## 25. FactPICO H1 adapter/input/gold implementation freeze

Landscape reset:
`SCIENTIFIC_VERIFICATION_LANDSCAPE_RESET_V1.md`

Landscape commit:
`f723cb718dc7451c2b484df43cb13a34e3603348`

Implementation freeze:
`FACTPICO_H1_ADAPTER_IMPLEMENTATION_FREEZE_V1.md`

Freeze commit:
`ee41d5908c5f703aa6738c4a6a3078e69f0e0f25`

Adapter:
`factpico_h1_adapter_v5.py`

Adapter commit:
`c36aef499fe28c83b80f1d7a9f296deefa309d2d`

Adapter SHA-256:
`ab128309261eeffdb734464f2a2fef52cef4ce37bdb3b9654317d6b5bba0b7e1`

Build manifest:
`FACTPICO_H1_V5_BUILD_MANIFEST.json`

Build-manifest commit:
`8450003be24db1b101cb7a8be663431a934dbd76`

Frozen private prediction-input SHA-256:
`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Frozen separate private-gold SHA-256:
`6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`

Eligibility manifest SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Expected build-manifest SHA-256:
`67bfbd4302f66d2248009c8a6fe9cef658a6f202d278450b73e942c68cb6f16b`

Validation:
- 345 prediction IDs
- exactly one input record/ID
- prediction keys only: record_id/source_text/candidate_text
- zero gold fields in inference artifact
- prediction/gold ID sets exact match
- deterministic rebuild repeated twice with identical hashes
- no V2.4 execution

Environmental note:
an unrelated artifact_tool spreadsheet-warmup warning appeared during Python startup, but adapter returned code 0 and deterministic second build matched all hashes.
Classified tooling/environment only.

Fresh landscape conclusion:
`MANY STRONG RESOURCES EXIST; PROBLEM = CONSTRUCT MATCHING + EVALUATION INTEGRITY`

Strategy:
`REUSE MORE / FORCE LESS`

Future H2/H3 resource choices are explicitly reopened for modern-resource audit before their execution:
- SciVer
- CLAIM-BENCH
- SciClaimEval
- SciCiteVal/CiteAudit
- SciTab/Table-Text Alignment
while established prior resources remain candidates/baselines.

Exact next checkpoint:
`H1 FACTPICO PRE-PREDICTION INTEGRITY GATE`

V2.4 prediction remains unauthorized.


## 26. Strategic landscape review reconciliation + pre-prediction integrity gate

Higher-model strategic review decision:
`STRATEGIC_LANDSCAPE_HIGHER_MODEL_REVIEW_DECISION_V1.md`

Commit:
`a1a9975797a6e3879ed8174c82e4ffbacd4dea7e`

Final strategic verdict:
`B. PROCEED WITH MAJOR STRATEGIC MODIFICATIONS`

Current authoritative capability/claim map:
`ACAD_PASS_CAPABILITY_CLAIM_MAP_V1.md`

Commit:
`bba139f93af7b5b0be95ce6de1dde593cf77ffc6`

FactPICO Added Information completeness decision:
`FACTPICO_ADDED_INFORMATION_COMPLETENESS_DECISION_V1.md`

Commit:
`99372a2e67594f17eaf67ddf5b2a00a84ea9c189`

Decision:
`PASS_WITH_NARROW_CLAIM`

Allowed statement:
`NO_HIGHLIGHTED_ADDED_INFORMATION_SPAN_IN_THE_RELEASE`

Not:
no possible addition / full source entailment.

Readiness supersession index:
`PRE_GATE_C_READINESS_SUPERSESSION_INDEX_V1.md`

Commit:
`8ef29c7c00d46ade02f6b1c358bba9a58d879532`

FactPICO pre-prediction integrity gate:
`FACTPICO_H1_PRE_PREDICTION_INTEGRITY_GATE_V1.md`

Commit:
`160a823c4712815c364a30b9bcce42c4c9d03d93`

Integrity checks PASS:
- claim boundary frozen;
- Added Information interpretation closed;
- readiness authority unified;
- artifact hashes frozen;
- no gold leakage;
- adapter deterministic;
- prediction/gold IDs exact match;
- frozen runtime unchanged since canonical pipeline freeze.

Runtime drift audit:
GitHub compare from freeze trigger commit
`c0193aa3f578cc32b454a031ead73ff7e56c8918`
to gate-time HEAD found:
`0 changes`
to the seven frozen runtime components.

NEW BLOCKER:
`FACTORIAL ALIGNER SCALABILITY`

Frozen B1.1 aligner enumerates permutations for one-to-one assertion assignment.

Worst-case enumeration in
`n = min(source_assertions,candidate_assertions)`:

- n=10 -> 3,628,800
- n=12 -> 479,001,600
- n=15 -> 1,307,674,368,000

The B2 implementation itself describes the unequal-count fallback as appropriate for a small mechanics set.

FactPICO uses full abstracts/full summaries.

Therefore:
`NOT_READY_FOR_FACTPICO_PREDICTION`

Reason:
`BLOCKED_BY_SCALABILITY_PREFLIGHT`

Do NOT conflate this execution-validity blocker with FactPICO scientific performance.

Exact next checkpoint:
`V2.4 SYNTHETIC SCALABILITY PREFLIGHT + EXECUTION-POLICY DECISION`

Still forbidden:
- FactPICO V2.4 prediction;
- H1 scoring;
- frozen runtime modification without version bump;
- threshold tuning;
- custom Gate C opening;
- Arabic work.


## 27. Full higher-model report reconciliation + synthetic scalability preflight

Full strategic reconciliation:
`FULL_STRATEGIC_LANDSCAPE_RECONCILIATION_V1.md`

Commit:
`b724f618eb8067e44edd7ac3ae823b52f292ae01`

Newly incorporated from full reviewer report:
- three-level evidence hierarchy:
  ARTIFACT/CONFORMANCE -> CONSTRUCT CAPABILITY -> COMPLETE TRANSACTION;
- stronger later-version architecture around executable obligations, native-document authority, context/obligation separation, coverage audit and dependency-aware repair;
- concrete integration candidates and code/license warnings;
- explicit unresolved failure modes:
  shared extraction blindness, benchmark packaging leakage, multiplicity collapse, context laundering, evidence cherry-picking, stale verification, compensatory repair, hidden document layers, scientific-state confusion, authoritative-source drift;
- later novelty/baseline requirement:
  compare against simpler imported baselines and simplify ACAD_PASS if the richer architecture does not add measurable value.

No change to FactPICO V5.

Synthetic scalability preflight:
`V2_4_SYNTHETIC_SCALABILITY_PREFLIGHT_V1.md`

Commit:
`03609245bab8d22e4c164708fd8ed2d9ded36803`

Synthetic-only measured frozen matcher runtime:
- n=6: 0.1767 s
- n=7: 1.4159 s
- n=8: 12.9480 s

n=8 throughput:
~3,114 permutations/sec.

Optimistic constant-throughput extrapolation:
- n=9: ~1.94 min
- n=10: ~19.42 min
- n=11: ~3.56 h
- n=12: ~42.73 h
- n=15: ~13.31 years

No FactPICO record was used.

Preflight verdict:
`FAIL_SCALABILITY`

Current external prediction status:
`NOT_READY_FOR_FACTPICO_PREDICTION`

Focused higher-model review packet:
`V2_4_SCALABILITY_HIGHER_MODEL_REVIEW_PACKET.txt`

Packet commit:
`481c45c8a77f2446f9f2759c46c620c55054c1f2`

Decision requested:
- canonical V2.4 + preregistered timeout/INVALID baseline;
vs
- version-bumped scalable matcher before FactPICO;
vs
- another explicitly cleaner path.

Implementation-agent preliminary recommendation:
`PREFER VERSION-BUMP SCALABLE MATCHER, SUBJECT TO INDEPENDENT REVIEW`

Reason:
known factorial execution defect may confound the one-shot external measurement.

FactPICO remains untouched/unconsumed.
