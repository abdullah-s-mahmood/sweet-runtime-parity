# H1 Official-Alignment Audit v1 — Frozen M2 Continuation

Date: 2026-09-30
Status: FROZEN BEFORE M2 CONTINUATION
Scope: CALIBRATION only

## Provenance

Source audit run:
- workflow run: 36714305860
- job: 109883334984
- commit: a2cf6fbe6c94bd37a5b4fe4fb45882c15372ce6f
- artifact id: 11095877555
- artifact ZIP SHA256: a0d1c85da57f06b2deb6b9c171d8843ccd5d13f46028eb58665c97a4b72e74c6

The run completed H1 parity and official-alignment/NoPnx gold construction and reached the M2 edit-creator invocation. It failed only because the legacy M2 edit creator was executed as a direct file and lost its package context.

Because the audit script exits before writing SOURCE/NOPNX_REFERENCE/H1_SYSTEM when any gold-construction failure, word/subword NoPnx mismatch, or character-alignment cross-validation mismatch is present, the existence of the three complete files below is evidence that these stop conditions were not triggered.

## Frozen intermediate files

All three files contain exactly 6,888 lines.

- SOURCE
  - SHA256: c633b4566f5d46ce1b896a4486bf409d343ebf9eac20881961d9c78d41db0f6d
- NOPNX_REFERENCE
  - SHA256: 4180173c8c5ca56810f7c598db33abdb6ee2aab14010b44d733be0b8cf011769
- H1_SYSTEM
  - SHA256: e806afe61f737adeb8699d46d8399c42c876bc9aeec1e9afa5f1ccf84bb6117b

## Authorized continuation

Do not recompute the 6,888-case alignment.

1. Download the exact artifact above.
2. Verify artifact provenance, line counts, and all three SHA256 values.
3. Clone the frozen official text-editing implementation at:
   4d552ca3ae98029550f27fc52aa1b22883e16e61
4. Invoke the unchanged legacy M2 edit creator through a package-context wrapper only.
5. Use:
   - max_unchanged_words = 2
   - official run_m2scorer.py
   - beta = 1.0 as already frozen by the audit protocol.
6. Produce headline Precision, Recall, F1, F0.5 and the frozen H1 recall-gate decision.

## No scientific changes

Unchanged:
- model/checkpoint/revision;
- one-pass top-1 H1 output;
- CALIBRATION population;
- NoPnx reference text;
- M2 settings;
- 80% H1 recall gate;
- INTERNAL_EVALUATION/STRESS_DIAGNOSTIC remain unopened.

This continuation is operational only and may not alter any frozen file content.
