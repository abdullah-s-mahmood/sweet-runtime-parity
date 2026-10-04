# ACAD_PASS — FactPICO Artifact + Schema + License Audit V1

Date: 2026-10-04
Status: PARTIAL FREEZE / RAW DATA BYTES REQUIRED / NO V2.4 EXECUTION

Parent:
`H1_CONTEXT_GOLD_SEMANTICS_RESOLUTION_V1.md`

Purpose:
freeze all currently verifiable FactPICO identity, construct, schema, provenance and license evidence before any H1 adapter or V2.4 prediction.

## 1. Resource identity

Resource:
`FactPICO: Factuality Evaluation for Plain Language Summarization of Medical Evidence`

ACL 2024 DOI:
`10.18653/v1/2024.acl-long.459`

Official repository:
`lilywchen/FactPICO`

Observed main HEAD:
`2e16993a000aedb15cb348b7bcd61070d26bab14`

Repository license:
`MIT`

The repository README points to the official dataset download through a UT Austin Box shared link.

## 2. Dataset scope verified from the paper

FactPICO contains:
- `115` RCT abstracts;
- `345` plain-language summaries;
- 3 generated summaries per source abstract;
- generating models:
  - GPT-4
  - Llama-2-Chat
  - Alpaca

Source abstracts are sampled from:
`Evidence Inference V2.0`

The benchmark focuses on expert factuality assessment of critical RCT elements:
- Population
- Intervention
- Comparator
- Outcome
- Evidence Inference / reported findings
- Added Information

## 3. Human annotation schema — conceptual freeze

### 3.1 PICO element rating

For each PICO element, expert rating semantics are:

`4 = Mentioned and described accurately`

`3 = Mentioned but somewhat inaccurately or vaguely`

`2 = Mentioned but described with severe inaccuracies and/or missing critical descriptors`

`1 = Missing`

`N/A` is also available where the RCT element is not meaningful/applicable.

This directly distinguishes:
- faithful representation;
- partial/vague representation;
- severe inaccuracy / loss of critical descriptors;
- complete omission.

### 3.2 Evidence Inference rating

For each annotated result/evidence-inference span:

`4 = Accurate`

`3 = Vague / Slightly Inaccurate`

`2 = Inaccurate`

`1 = Not Mentioned`

A free-text expert rationale accompanies the rating.

### 3.3 Added Information

Annotators identify:
- output words/phrases/sentences that add or modify source information;
- whether that added/modified information is factual;
- a free-text rationale.

This supports evaluation of unsupported or incorrect additions.

### 3.4 Exhaustive Outcomes

The annotation interface separately records whether all outcome measures are exhaustively mentioned.

Important nuance:
the paper explicitly says a summary may still be considered factual when omitted outcome measures are non-critical and not mentioned further in the abstract.

Therefore:
`EXHAUSTIVE OUTCOME COVERAGE != GENERAL FACTUALITY LABEL`

This field, if present in the released data, must remain distinct from critical-preservation gold.

## 4. Context compatibility with V2.4

FactPICO annotators are shown:
- the full source RCT abstract;
- the full generated plain-language summary.

Therefore frozen V2.4 can in principle receive:

`source_text = full RCT abstract`

`candidate_text = full plain-language summary`

without a separate hidden context channel.

This removes the specific PLABA context mismatch.

No adapter semantic enrichment is needed merely to expose the same source/candidate context to V2.4.

## 5. H1 construct fit

FactPICO supports a narrow but defensible hard H1 construct:

`CRITICAL RCT-ELEMENT FIDELITY / PRESERVATION`

### H1-S support/factuality candidates

Supported by:
- PICO rating 4 vs inaccurate states;
- Evidence Inference rating;
- Added Information factuality.

### H1-C critical-content preservation candidates

Supported by:
- PICO rating 1 = missing;
- PICO rating 2 = severe inaccuracies and/or missing critical descriptors;
- Evidence Inference rating 1 = not mentioned;
- exhaustive-outcome annotation as a separate diagnostic/secondary construct.

FactPICO does NOT prove exhaustive preservation of every source statement.

## 6. Expert annotation provenance

The paper reports:
- two senior fifth-year medical students;
- expert/medical-domain annotation experience;
- `75` summaries double annotated;
- discussion was used to improve PICO agreement on part of the doubly annotated material;
- `15` later double-annotated summaries were independently annotated after the discussion;
- reported PICO inter-evaluator agreement is moderate-to-high depending on element.

Important:
discussion-resolved judgments are not equivalent to independent duplicate judgments.

Future gold contracts must distinguish:
- consensus/discussion-resolved annotations;
- independently duplicated annotations;
- single available annotation.

## 7. License freeze

### Repository code

Official repository license:
`MIT`

This applies to repository software/documentation subject to the repository license.

### FactPICO annotations

The paper Appendix B states:

`FactPICO annotations are released under CC BY 4.0`

Therefore:
`ANNOTATION LICENSE = CC BY 4.0`

### Source RCT abstracts

The paper states that source articles come from the PubMed Open Access subset and include license terms allowing reuse.

Therefore:
`SOURCE-ARTICLE REUSE PATH = VERIFIED AT PAPER LEVEL`

But each underlying article may retain its own source license.

No claim is made that every raw source abstract is itself CC BY 4.0.

## 8. Data access route

Official repository data README points to:

`https://utexas.box.com/s/mpe5idxrqrzs1wcakphng7xfi7h4g83j`

Equivalent indexed form observed elsewhere:

`https://utexas.app.box.com/s/mpe5idxrqrzs1wcakphng7xfi7h4g83j`

The current environment cannot read/download this Box share.

Therefore:

`DATA ACCESS ROUTE = VERIFIED`

`RAW DATA BYTES = NOT YET FROZEN`

`FILE NAMES = NOT YET FROZEN`

`LOCAL SHA-256 = NOT YET FROZEN`

## 9. Physical schema evidence from official code

FactPICO evaluation code directly expects at least:

`Abstract`

and:

`generation`

columns/fields for full source and generated summary.

The result-evaluation code also expects:

`results_span`

for evidence-inference evaluation.

This establishes conceptual field usage, but it does NOT prove the exact released data file schema.

Therefore:

`CONCEPTUAL SCHEMA = PARTIALLY FROZEN`

`PHYSICAL RELEASE SCHEMA = NOT YET FROZEN`

## 10. What must be obtained from the Box artifact

Need exact released files in order to freeze:

1. filenames;
2. directory structure;
3. raw file hashes;
4. exact source/summary identifiers;
5. PubMed/PMID or Evidence-Inference source IDs;
6. generator/model identity;
7. PICO rating column names;
8. Evidence Inference rating/rationale fields;
9. Added Information fields/spans/labels;
10. Exhaustive Outcome field if released;
11. annotator/double-annotation/provenance fields if released;
12. N/A encoding;
13. missing-value conventions;
14. duplicate records;
15. exact count reconciliation to 115 abstracts / 345 summaries.

## 11. Current readiness impact

FactPICO resource identity:
`PASS`

Paper/benchmark construct:
`PASS`

Annotation-license evidence:
`PASS — CC BY 4.0`

Repository code license:
`PASS — MIT`

Whole-abstract/full-summary context compatibility:
`PASS IN PRINCIPLE`

Raw artifact identity/files:
`NOT READY`

Physical data schema:
`NOT READY`

Local hashes:
`NOT READY`

Exact source-cluster manifest:
`NOT READY`

H1 Contract V4:
`NOT READY`

Overall:
`NOT_READY_GATE_C_EXT_META`

## 12. Required user-assisted artifact

Because the official Box share is not accessible through the current environment, the preferred next action is:

1. open the official FactPICO Box link;
2. use Box `Download` / `Download all`;
3. preserve the downloaded ZIP/folder exactly as provided;
4. upload that archive here without modifying filenames or contents.

Preferred:
`the complete FactPICO shared folder/archive`

rather than selecting individual unknown files.

After upload, the next agent can:
- compute SHA-256;
- inspect exact schema;
- reconcile all counts;
- freeze source clusters;
- audit duplicates;
- determine the final hard-gold eligibility contract.

## 13. Exact next checkpoint

`FACTPICO PHYSICAL ARTIFACT + SCHEMA FREEZE`

No V2.4 prediction is authorized before that checkpoint is complete.
