# ACAD_PASS — NO-NEW-HUMAN Gate C Alternative Research Plan V1

Date: 2026-10-03
Status: RESEARCHED ALTERNATIVE / PROTOCOL NOT YET CHANGED

## Core conclusion

It is scientifically plausible to eliminate the need for NEW human adjudicators at Gate C by replacing newly-created gold with a triangulated suite of already-published human/expert-labeled benchmarks plus deterministic metamorphic tests.

This does NOT mean one public dataset is equivalent to ACAD_PASS.
The proposed substitute is a multi-track construct-validation suite.

Recommended working name:

`EXTERNAL_HUMAN_GOLD_COMPOSITE_VALIDATION`

## Why this is credible for ACAD_PASS

The frozen V2.4 verifier:
- uses no model inference;
- has fixed deterministic/hybrid extraction and alignment code;
- is frozen before selecting a new external validation suite.

Therefore pretrained-model benchmark memorization is not the primary concern for the verifier itself.

Main risks instead are:
- development exposure to benchmark examples;
- construct mismatch;
- overlapping/duplicated examples;
- adapting code after seeing results.

Mitigation:
- select only datasets/cases not used during development;
- freeze dataset list/splits before execution;
- do not tune pipeline after score;
- report each track separately;
- never claim a broader construct than each track supports.

## Track A — scientific claim/evidence verification

### SciFact

Why useful:
- ~1.4K expert-written scientific claims;
- research-paper abstracts;
- expert SUPPORT/CONTRADICT evidence labels;
- evidence rationales.

Use to test:
- scientific claim support/refutation;
- evidence alignment;
- relation/claim preservation;
- attribution to source evidence.

Limit:
does not directly test academic rewrite fidelity.

### SciFact-Open

Why useful:
- open-domain scientific claim verification over ~500K abstracts;
- annotated evidence gathered through pooling;
- harder generalization setting.

Use to test:
- scientific verification beyond a tiny closed corpus;
- evidence retrieval/alignment stress.

Limit:
not a rewrite benchmark.

## Track B — academic full-document evidence grounding

### QASPER

Why useful:
- 5,049 information-seeking questions over 1,585 NLP papers;
- questions written by NLP practitioners;
- answers provided by a separate set of practitioners;
- supporting evidence paragraphs supplied.

Use to test:
- whether extracted/verified assertions can remain grounded in full-paper evidence;
- evidence-span fidelity;
- abstention when full-text evidence is absent.

Limit:
QA construct, not PASS/REJECT rewrite construct.

## Track C — human-edited factual correction

### DeFacto

Why useful:
- human demonstrations;
- corrective instructions;
- human-edited summaries;
- natural-language explanations of factual inconsistency.

This is especially close to ACAD_PASS repair:
- inconsistent text -> human correction;
- source document available;
- human explanation of the factual defect.

Use:
- original inconsistent summary = negative candidate;
- human-edited corrected summary = positive candidate;
- human explanation provides defect localization.

Limit:
primarily summarization/news domain rather than academic prose.

## Track D — large human factual-consistency collections

### TRUE
- standardized collection of 11 manually annotated factual-consistency datasets;
- diverse grounded text generation tasks;
- example-level evaluation.

### SummaC
- six factual-consistency datasets.

### AGGREFACT
- aggregates nine public human factual-consistency datasets;
- includes recent/older summarization systems;
- de-duplicates examples and resolves some label disagreements.

### FRANK
- human annotations with a factual-error typology.

### FENICE long-form factuality annotations
- human factuality annotations for long-form summarization;
- claim-level source alignment.

### QASemConsistency 2026
- >3K human-annotated fine-grained factual consistency instances;
- several attributable text-generation tasks;
- localized factual errors.

Use:
- external human-gold consistency testing;
- error-family analysis;
- evidence localization;
- transfer/generalization diagnostics.

Limit:
mostly summarization/grounded generation, not specifically scholarly rewriting.

## Track E — biomedical/scientific specialized factuality

### Clinical study summarization annotations
Tang et al. 2023:
- expert and crowd-worker factual-consistency annotations on clinical-study summarization.

### PlainFact / PlainQAFact
- fine-grained human-annotated biomedical plain-language factual-consistency data;
- evaluates source-simplified and elaborative sentences.

Use:
- high-risk biomedical language;
- scientific simplification/rephrasing;
- domain transfer.

## Track F — rich correction/evidence benchmarks

### USB — Unified Summarization Benchmark
Human-labeled benchmark across six domains with tasks including:
- evidence for summary sentences;
- factual accuracy;
- unsubstantiated-span identification;
- factual error correction.

Use:
- evidence + error localization + correction in a unified benchmark.

## Track G — deterministic ACAD_PASS-specific metamorphic validation

Published human gold cannot fully cover ACAD_PASS-specific relation binding.

Add oracle-free / deterministic metamorphic tests derived from authentic academic text.

Metamorphic testing is specifically useful when explicit gold is unavailable.

Allowed transformations whose expected outcome is logically known by construction:

### PASS-preserving
- sentence split/merge preserving propositions;
- clause reordering preserving ownership;
- explicit synonym substitution from frozen safe lexicon;
- format-only changes;
- citation-style formatting with identical citation ownership;
- variable-order formatting where semantic binding is unchanged.

### REJECT-guaranteed
- swap owner/value pairs;
- swap group labels while preserving numbers;
- flip explicit negation;
- strengthen MAY/CAN to IS when unsupported;
- association -> causation mutation;
- swap citation owners;
- swap equation coefficient-variable bindings;
- alter denominator/baseline;
- alter temporal scope;
- delete a critical qualifier.

### REVIEW-guaranteed
Only use where the mutation removes necessary context in a formally preregistered way.
Do not assume every truncation is REVIEW.

Important:
metamorphic tests validate expected relations, not natural-use prevalence.

## Proposed replacement architecture for Gate C

Do NOT use one 80-study custom human-labeled holdout.

Instead build a sealed EXTERNAL HUMAN-GOLD COMPOSITE suite:

1. SCIENTIFIC-EVIDENCE track
   - SciFact
   - SciFact-Open subset

2. FULL-PAPER GROUNDING track
   - QASPER subset

3. HUMAN-CORRECTION track
   - DeFacto

4. FACTUALITY-CONSISTENCY track
   - QASemConsistency / FENICE / AGGREFACT / FRANK / TRUE
   - de-duplicate overlaps

5. SCIENTIFIC/BIOMEDICAL track
   - clinical-study factuality annotations
   - PlainFact when available

6. ACAD_PASS RELATION-STRESS track
   - deterministic metamorphic academic mutations

No new human annotators are required to create gold.

## How to preserve independence

Before executing:
- choose datasets/splits before inspecting verifier output;
- exclude every example/dataset used directly in development;
- use official test/dev splits where labels are legally/publicly available;
- hash selected examples;
- freeze mapping from external labels to ACAD_PASS outcomes;
- freeze exclusion criteria;
- freeze all transformations;
- freeze scoring;
- run once.

Do not tune V2.4 after seeing composite results.

## Outcome mapping caution

External labels must NOT be naively translated.

Example:
- SUPPORT does not automatically mean PASS unless the task input/candidate mapping supports that interpretation.
- CONTRADICT can map to REJECT in a properly defined source-claim pair.
- human factual-consistency positive/negative pairs can map more directly to PASS/REJECT.
- insufficient-evidence/neutral examples can only map to REVIEW where the dataset's evidence condition truly matches ACAD_PASS REVIEW semantics.

Every dataset requires a preregistered adapter contract.

## Can this be called non-provisional?

Recommended scientific wording:

If the suite uses only independently published human/expert labels and deterministic metamorphic oracles, and the V2.4 pipeline is frozen before suite selection/execution:

`NON_PROVISIONAL_EXTERNAL_BENCHMARK VALIDATION`

is defensible for the constructs actually represented by those benchmarks.

However it is NOT equivalent to:
- fresh bespoke human adjudication of the exact 80-study Gate C construct;
- proof of real-world prevalence;
- proof of the full ACAD_PASS product.

Therefore the claim must be bounded:

`Externally validated against multiple independent published human-gold factuality/scientific-evidence benchmarks plus ACAD_PASS-specific metamorphic relation tests.`

Do not claim:
`human-adjudicated fresh Gate C`
unless new human adjudication actually occurs.

## Recommended decision

Replace the current new-human Gate C requirement with a two-layer validation program:

### Gate C-EXT — External Human-Gold Composite Validation
No new human reviewers.

Hard requirement:
pass multiple independent published human-gold tracks without tuning.

### Gate C-META — ACAD_PASS Metamorphic Relation Validation
No human gold required.

Hard requirement:
zero dangerous relation mutations accepted where the oracle is deterministic.

Only if a later publication/reviewer specifically demands bespoke fresh human labels:
add a small targeted human study then, rather than 200 fresh adjudications now.

## Strong-adoption interpretation

This alternative can provide stronger evidence than a small bespoke study in some respects because:
- thousands of human-labeled cases already exist;
- annotations were produced independently of ACAD_PASS;
- multiple teams/datasets reduce single-protocol bias;
- some datasets include expert scientific evidence/rationales;
- deterministic metamorphic oracles target exact ACAD_PASS failure modes.

But it cannot estimate deployment prevalence unless the benchmark mixture matches intended usage.

## Research support

Relevant published lines:
- SciFact: expert scientific claims + evidence rationales.
- SciFact-Open: open-domain scientific verification.
- QASPER: practitioner questions/answers + evidence over research papers.
- DeFacto: human corrections + explanations of factual errors.
- TRUE: 11 manually annotated factual-consistency datasets.
- SummaC: six factual-consistency datasets.
- AGGREFACT: nine human-evaluated factuality datasets.
- FRANK: human factual error typology.
- FENICE: human long-form factuality annotations.
- QASemConsistency: >3K localized human factual-consistency annotations.
- USB: evidence/factuality/error-localization/error-correction tasks across six domains.
- metamorphic testing literature: oracle-free consistency testing when gold labels are unavailable.

## Exact next research decision

Do NOT open the custom 80-study holdout yet.

Next recommended checkpoint:

`PRE-GATE-C — EXTERNAL HUMAN-GOLD COMPOSITE FEASIBILITY AUDIT`

Tasks:
1. inventory candidate datasets;
2. verify licenses/downloadability;
3. verify label schemas;
4. quantify available public labeled examples;
5. detect dataset overlap/deduplicate;
6. define ACAD_PASS adapter contract for each dataset;
7. identify which ACAD_PASS construct dimensions remain uncovered;
8. decide whether custom human adjudication can be removed entirely or reduced to a very small residual study.

No V2.4 runtime changes.
