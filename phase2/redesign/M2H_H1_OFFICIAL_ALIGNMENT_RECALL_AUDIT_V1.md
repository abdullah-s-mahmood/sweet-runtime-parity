# M2-H H1 Official-Alignment Recall Audit v1

Date: 2026-09-30
Status: **FROZEN BEFORE AUDIT METRICS**
Scope: **CALIBRATION only**
Purpose: resolve the provisional H1 recall blocker before H5/H6.

## 1. Why this audit is required

The provisional H1 recall calculation matched current `difflib` candidate transactions directly against QALB M2 edits.

That comparison is not representation-invariant.

Observed CALIBRATION examples show that QALB may represent one final correction as multiple edits, e.g.:
- an Edit reducing a fused token;
- plus a zero-width Add_before;
while H1 may generate the same final corrected string as one Split transaction.

Therefore exact candidate-transaction identity can undercount correction coverage even when the H1 final rewrite is correct.

A second confound is that the frozen checkpoint is `SWEET_NoPnx`, while raw QALB gold includes punctuation corrections. The official system separates punctuation and non-punctuation edits.

The original H1 feasibility target remains:
- candidate edit-instance recall >= 80%.

This audit does not lower that target. It determines which reproducible representation should be used to assess it.

## 2. Frozen resources

H1 model:
`CAMeL-Lab/text-editing-qalb14-nopnx`

Model revision:
`21286e56ce98a86362db540863f91c083b8970f9`

Weight SHA256:
`9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d`

Official implementation:
`CAMeL-Lab/text-editing`

Implementation revision:
`4d552ca3ae98029550f27fc52aa1b22883e16e61`

CALIBRATION:
6,888 frozen cases only.

Current H1 artifact:
run `36691616010`
artifact `11088155733`.

## 3. Audit A — public model-card inference parity

The frozen checkpoint's public model card documents direct inference using:
- `BertTokenizer`;
- `BertForTokenClassification`;
- `tokenizer(text, is_split_into_words=True)`;
- top-1 labels excluding special tokens;
- `gec.tag.rewrite`.

This is the primary public checkpoint-use contract.

Create a deterministic 256-case CALIBRATION parity sample.

Sampling salt:
`M2H-H1-PUBLIC-PARITY-V1-20260930-A`

Rank by:
`SHA256(salt + "|" + uid)`

On those 256 cases, recompute one-pass inference exactly in the model-card style and compare with the frozen H1 artifact:
- subword sequence;
- top-1 labels;
- normalized H1 rewrite.

Required parity:
**100% on all three fields for all 256 non-truncated cases**.

Any mismatch is a critical implementation blocker.

This parity audit does not use gold/reference text.

## 4. Audit B — official SWEET NoPnx gold construction

For each CALIBRATION source/reference pair, build a non-punctuation target using the frozen official edit pipeline:

1. official word-level alignment;
2. official character-level alignment;
3. official `Edit` / `SubwordEdits` creation;
4. official insertion-to-append conversion;
5. official `separate_pnx_edit`;
6. apply only the non-punctuation edit component to the raw source subwords;
7. detokenize to obtain `reference_nopnx`.

This follows the architecture used to create SWEET punctuation-separated data.

No hand-written punctuation filter is allowed for the headline audit.

Validation:
- reconstructing the full combined edits must reproduce the full reference;
- NoPnx target generation failures are counted and reported;
- no failed row may be silently excluded from headline metrics.

## 5. Audit C — representation-invariant M2 rewrite evaluation

The H1 system output is the frozen one-pass `h1_rewrite` from the existing artifact.

For the same CALIBRATION ordering:
- source = original source;
- gold target = official `reference_nopnx`;
- system output = frozen one-pass H1 rewrite.

Create a derived NoPnx gold M2 file using the frozen official M2 `edit_creator.py` from:
`source -> reference_nopnx`.

Evaluate the frozen H1 rewrites with the repository's official M2 scorer:
- `max_unchanged_words=2`;
- `beta=1.0`;
- timeout 30 seconds per sentence, matching official evaluation defaults.

Headline metrics:
- M2 precision;
- M2 recall;
- F1;
- F0.5;
- skipped/timeouts.

The key H1 feasibility diagnostic is:
**official-alignment one-pass NoPnx M2 recall**.

## 6. Calibration sanity references

The frozen official repository contains a one-pass QALB14 dev NoPnx result:
- precision: 88.25%
- recall: 77.66%
- F1: 82.62%
- F0.5: 85.91%

This is a sanity reference only.
It is a different population from ACAD_PASS CALIBRATION and must not be treated as directly comparable performance.

## 7. Secondary diagnostics

Report separately:
- exact sentence equality between H1 rewrite and `reference_nopnx`;
- source-copy rate;
- current transaction exact-match recall, labeled `TRANSACTION_DECOMPOSITION_SENSITIVE`;
- number of gold M2 edits in derived NoPnx target;
- sentence-level M2 recall distribution if available.

Do not combine these into the headline metric.

## 8. Interpretation rule

If model-card parity fails:
- stop;
- current H1 artifact is not reproducibly valid;
- do not interpret downstream H2/H3/H4 candidate-stream results until H1 is repaired.

If model-card parity passes but official-alignment NoPnx M2 recall remains substantially below the frozen 80% feasibility gate:
- H1 feasibility is scientifically weak under one-pass mode;
- do not silently switch to iterative decoding;
- prepare a focused higher-level review packet before deciding H5/H6 viability.

If official-alignment NoPnx M2 recall reaches or exceeds 80%:
- H1 feasibility gate passes;
- audit downstream dependency validity before H5/H6.

If within 5 percentage points below 80%:
- classify as borderline and escalate to the focused higher-level review because the official QALB14 dev one-pass reference itself is 77.66%.

## 9. No tuning

Forbidden after audit metrics:
- changing one-pass to two-pass inside H1-v1;
- changing top-k;
- changing confidence thresholds;
- altering the 80% gate;
- selecting a different denominator to improve the result;
- opening INTERNAL_EVALUATION.

Iterative decoding may be discussed only as a separately versioned future option.

## 10. Reserved data

Remain unopened:
- INTERNAL_EVALUATION;
- STRESS_DIAGNOSTIC;
- Confirmation;
- Holdout;
- A7'ta reserve;
- reserved Nahw IDs;
- QALB15 TEST.
