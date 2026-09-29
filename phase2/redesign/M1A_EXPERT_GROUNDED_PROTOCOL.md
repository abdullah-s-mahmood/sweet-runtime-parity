# M1-A — Expert-Grounded Reference Bootstrap Protocol

Date: 2026-09-30  
Status: PRE-REGISTERED

## Research question

Can expert human correction evidence already present in published Arabic corpora bootstrap the measurable parts of ACAD_PASS Edit Contract v1 without fabricating human gold or consuming fresh reserved data?

## Inputs

### QALB14 L1
Pinned upstream:
- repository: CAMeL-Lab/arabic-gec
- revision: 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf
- splits read: TRAIN, DEV
- source: *.sent.no_ids
- corrected: *.cor.no_ids
- official edits: *.m2

TRAIN/DEV were already consumed in the earlier CAD work.

### Nahw
Use only the frozen 150 targets in the existing 41 Phase-2 development passages.

## Exclusions

The bootstrap must fail if code attempts to read:
- QALB14 TEST;
- any QALB15 DEV or TEST;
- any new QALB15 TRAIN slice;
- reserved/sealed Nahw material.

## Data handling

Raw QALB sentence text is used only at runtime.
Committed outputs contain:
- corpus/split/line identifiers;
- case family;
- source/candidate/reference SHA-256 hashes;
- counts of reference edits;
- applied/withheld reference-edit indices;
- evidence tier;
- axes directly supported by the evidence;
- axes explicitly not established.

No QALB raw Arabic sentence text may be committed by this workflow.

## Official edit parsing

Parse standard M2 blocks.
Use annotator 0 when multiple annotations are encoded in the same M2 record.
For partial case synthesis:
- apply edits to whitespace-tokenized source in descending span order;
- verify that applying all selected official edits reconstructs the corresponding corrected line after whitespace normalization;
- if reconstruction fails, skip partial synthesis for that line and count it explicitly.

Full source→reference pairs do not depend on M2 reconstruction.

## Deterministic sampling

The full corpus is scanned for counts.
Persist a deterministic hash-ranked sample capped at:
- FULL_EXPERT_REPAIR: 500
- EXPERT_KEEP: 250
- SINGLE_EDIT_COMPLETE: 250
- ONE_OF_MANY_PARTIAL: 500
- ALL_BUT_ONE_PARTIAL: 500
- NAHW_LOCAL_REFERENCE: all 150 frozen targets

The sample is for calibration/analysis, not a fresh performance test.

## Partial labels

Each persisted case has:
- direct_assertions: what the expert/reference evidence directly supports;
- protocol_support: corpus-level goals that provide context but are not per-item gold;
- unresolved_axes: M1 dimensions not established by this reference.

For ONE_OF_MANY_PARTIAL and ALL_BUT_ONE_PARTIAL:
- local applied edit(s) are reference-supported;
- candidate has known unapplied reference corrections;
- sentence is incomplete **relative to the expert reference**;
- relationship among residual edits is not inferred automatically.

## Pre-registered data-quality criteria

M1-A bootstrap is DATA_READY only if all are true:
1. QALB14 TRAIN and DEV source/corrected line counts match within each split.
2. At least 1,000 source!=reference lines exist across the allowed splits.
3. At least 100 source==reference lines exist.
4. At least 300 multi-edit lines are reconstructable from M2 for controlled partial synthesis.
5. Both ONE_OF_MANY_PARTIAL and ALL_BUT_ONE_PARTIAL contain at least 300 cases before sample capping.
6. No forbidden split is read.
7. No raw QALB Arabic text appears in committed JSON/JSONL outputs.
8. Every case records provenance and evidence tier.

Failure means repair the data pipeline or narrow the claim. It does not authorize reading new splits.

## What success means

Success means:
- the human-reviewer availability blocker is reduced for M1 calibration;
- M1 now has expert-grounded controlled examples for local-support versus repair-completeness distinctions.

Success does NOT mean:
- Arabic auto-accept improved;
- the M1 contract has independent human validation on ACAD_PASS academic documents;
- a future LLM verifier is accurate;
- QALB reference equals absolute linguistic truth.

## Next gate

Only after DATA_READY:
1. audit the bootstrap families and evidence assertions;
2. perform M1-A end research/brainstorming;
3. decide whether to revise Edit Contract v1 → v1.1;
4. define a frozen M2 verifier protocol using expert-grounded cases, while keeping the original 24-case project challenge set as unconfirmed/project-local evidence.
