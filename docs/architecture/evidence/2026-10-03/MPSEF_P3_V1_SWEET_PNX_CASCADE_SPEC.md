# MP-SEF P3_V1 SWEET PUNCTUATION CASCADE SPECIFICATION

Date: 2026-10-01
Status: PRE-IMPLEMENTATION / SOURCE-ONLY DESIGN FREEZE
Parent decision: ACAD_PASS_ARABIC_ARCHITECTURE_REBASELINE_V1
Gold use: FORBIDDEN

## 1. Purpose

P3_V1 is NOT a duplicate of current P1.

Current frozen P1 is:

`P1_SWEET_QALB14_NOPNX_ITER2`

That is:
- SWEET QALB-2014 NoPnx
- two iterative NoPnx passes
- final whole output after pass 2

P3_V1 adds the published punctuation stage:

`SWEET_NoPnx ×2 -> SWEET_Pnx ×1`

This corresponds to the ACL 2025 cascaded MSA text-editing setup.

## 2. Governing upstream family

Repository:
`CAMeL-Lab/text-editing`

Model family:
- `CAMeL-Lab/text-editing-qalb14-nopnx`
- `CAMeL-Lab/text-editing-qalb14-pnx`

Published inference pattern:

1. NoPnx decode iteration 1
2. NoPnx decode iteration 2
3. Pnx decode iteration 1

The public model card explicitly states that the Pnx model is intended to be used with the QALB14 NoPnx model.

## 3. Why P3 is useful

The ACL 2025 study found that separating non-punctuation from punctuation correction improves MSA GEC.

The published cascade:

`SWEET2_NoPnx + SWEET_Pnx`

achieved the strongest single text-editing setup reported for QALB-2014.

Therefore P3_V1 is a justified candidate-family extension rather than an arbitrary third proposer.

## 4. Source-only pipeline

For each source:

### Stage A — inherit current P1 behavior

Run the exact frozen P1-compatible two-pass NoPnx path.

The implementation must either:
- reuse the byte-identical P1 pass1/pass2 code path; or
- prove parity against the frozen P1 runner on a preregistered source-only packet.

The Stage-A output must be identical to P1 for the same frozen source and model identities.

### Stage B — punctuation pass

Feed Stage-A output words into the frozen QALB14 Pnx tokenizer/model.

Run exactly one decode iteration.

Record:
- Pnx subwords;
- Pnx labels;
- output;
- input hash;
- output hash.

No second Pnx pass is allowed in P3_V1.

## 5. Model/runtime freeze requirements

Before any project population generation, freeze:

For NoPnx:
- repository/model revision;
- weight SHA256;
- tokenizer identities;
- upstream text-editing revision.

For Pnx:
- Hugging Face revision;
- weight SHA256;
- tokenizer files/hashes;
- config hash;
- label vocabulary hash.

Environment:
- Python version;
- PyTorch version;
- Transformers version;
- text-editing code revision;
- package lock/pip freeze.

The current P1 historical identities remain historical evidence and are not rewritten.

## 6. Required proposal record

Each P3_V1 source-only record must contain:

- record_id;
- uid;
- case_id;
- cluster_id;
- source;
- source_sha256;
- proposer_id = `P3_SWEET_QALB14_NOPNX_ITER2_PNX_ITER1`;
- Stage-A pass1 output/trace;
- Stage-A pass2 output/trace;
- Stage-B Pnx output/trace;
- final full_proposer_output;
- final output_sha256;
- protected spans;
- source-only protection diagnostics;
- source-only truncation/input-length evidence;
- model/runtime identities;
- gold_reference_consulted=false;
- quality_scored=false.

## 7. Exact parity requirement with P1

On a preregistered source-only parity sample:

- P3 Stage-A pass1 == frozen P1 pass1;
- P3 Stage-A pass2 == frozen P1 pass2.

If Stage A differs, P3 is NOT a simple cascade extension and must be treated as a different architecture/version.

The parity packet must be selected before examining P3 output behavior.

## 8. Source-only diversity metrics

P3_V1 is justified only if it adds measurable non-gold diversity.

Required source-only counts against P1:

- exact final-output identity count;
- changed-only-by-punctuation count;
- changed-in-mixed punctuation+linguistic regions count;
- unique P3-only final outputs;
- source→P1 edit count;
- source→P3 edit count;
- P3-only edit components;
- protected-touch differences;
- candidate-set size before/after exact-output dedup;
- runtime overhead.

These are NOT correctness metrics.

## 9. Protection policy

P3 does not receive relaxed protection merely because it targets punctuation.

All existing protected invariants remain active, including:
- citations;
- numbers;
- units;
- percentages;
- equations;
- technical tokens;
- URLs/emails;
- structure;
- linkage/order invariants.

A punctuation change that breaks protected structure is blocked.

P3_V1 legalizer compatibility must be demonstrated source-only.

## 10. Truncation / token coverage

The runner must record:
- input token count;
- attention-mask coverage;
- any tokenizer truncation;
- output emptiness;
- rewrite failures.

Unknown truncation is non-executable.

No silent tokenizer truncation is allowed.

## 11. Required synthetic tests

At minimum:

1. punctuation-only correction;
2. mixed punctuation+word-boundary input;
3. no punctuation error -> stable output where model predicts KEEP;
4. protected citation punctuation;
5. decimal/percent/unit punctuation;
6. Arabic and Latin technical tokens;
7. empty source;
8. very long source/truncation boundary;
9. P1 Stage-A parity mismatch injection -> fail;
10. Pnx model/tokenizer revision mismatch -> fail;
11. batch-vs-single parity;
12. repeated execution byte identity.

## 12. Success definition

P3_V1 source-only stage succeeds if:

- Stage-A parity with P1 is exact;
- Pnx stage executes reproducibly;
- no silent truncation;
- all identities/hashes frozen;
- protection/legalizer compatibility proven;
- full population accounting preserved.

It does NOT require linguistic correctness during source-only validation.

## 13. Retention decision after source-only run

P3_V1 is retained for later architecture review only if it provides nontrivial candidate diversity without unacceptable provenance/protection cost.

Do not retain it merely because ACL 2025 reported strong benchmark results.

The project must measure its actual source-only distinctness on ACAD_PASS C_F.

## 14. Scientific boundary

No correctness, R_joint, precision, recall, F0.5, complete repair, or safe-repair metric may be computed during P3 source-only validation.

## 15. Next step

After P2_V2 and P3_V1 synthetic specifications are frozen:

- freeze a common proposer-diversity protocol;
- run source-only synthetic/parity prototypes only;
- package architecture for independent higher-model review before any full new measurement.
