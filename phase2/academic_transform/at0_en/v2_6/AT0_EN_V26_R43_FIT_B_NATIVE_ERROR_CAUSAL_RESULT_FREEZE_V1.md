# ACAD_PASS R4.3 — Frozen FIT-only B Generalization-Shift Causal Audit V1

Date: 2026-10-07
Status: READ-ONLY PHYSICAL REPLAY SUCCEEDED; NO NEW TRAINING.

## Source / execution identity
- Frozen Stage-A B run: `37535183682`
- B model SHA256: `4e4852b847be5bf64cd707ed62f770e13d64ee6becea3ce049f69bde220bfb05`
- Pinned TRAIN SHA256: `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`
- Frozen FIT/SELECT split SHA256: `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`
- Read-only replay run `37568769890` concluded SUCCESS.
- Replay artifact `11460495207`
- Artifact digest `sha256:e76de599341742c69c3202cfd299c9677d4f07c914c255d1c9b3b32ae175e9c0`

## Direct FIT replay outcome

- FIT documents: 320
- FIT sentences: 1292
- Gold-bearing sentences: 993
- Gold-empty sentences: 299
- Gold entities: 2371
- Total B native proposals: 2371
- B exact span AND class correct proposals: 2371
- B false proposals anywhere on FIT: **ZERO**
- B proposals in gold-empty sentences: ZERO
- Per-class exact: P=342, I=1038, C=144, O=847.

Therefore, on exactly its own FIT documents, the Stage-A B model achieved raw native **100% entity precision and 100% entity recall**. In Stage-B SELECT the same frozen model produced 697 native proposals, of which 447 were exact correct and 250 false; reference SELECT gold=640, so native proposal precision ~=64.13% and recall ~=69.84%.

This is a striking in-sample-to-out-of-document generalization gap. It is consistent with severe memorization / overfitting, but the present audit does not partition it into model capacity, source annotation ambiguity or small-sample statistical variation.

## Revised causal attribution

- `native_slots=0` in Stage B is **fully explained** by the frozen Stage-A B model emitting ZERO erroneous native proposals on its own FIT examples.
- Previous suspicion of an implementation bug suppressing existing FIT errors must be RETRACTED for this run; no such errors existed there to suppress.
- The miner's separate design blind spot (looping only over gold-bearing sentences) is still real, but on the current in-sample FIT replay it caused **no missed errors**, because gold-empty sentences also had zero native B proposals.
- **Dominant immediate scientific design fault**: train upstream B on FIT, generate its own easy/perfect in-sample proposals there, and expect downstream verifier to learn real out-of-document failures from them. It cannot.
- **Next remedy** is document-group-disjoint OOF B mining, and likely cross-fitting C_BOUNDARY context features and C_TYPE outputs, all WITHIN FIT, rather than tweaking the H0/H1 thresholds or adding triaffine capacity.

## Predicted BIO transition audit on FIT

- Raw predicted tokens analyzed: 33,244.
- Noncanonical I transitions: 7.
- All 7 occurred at word index ZERO of a blank-delimited sentence/example.
- No internal invalid-I transitions were observed on FIT.
- The 7 initial continuations may be legitimate under the pinned source's 11 documented `I-X` cross-example continuation segments. Do not classify them as false positives without matching each gold continuation metadata.
- The synthetic actual-code BIO unit test still proved that, in general, an invalid I-after-O can silently create a span; current **real FIT evidence did not observe internal manifestations**. Maintain a unit test and source-aware decoder, but do not attribute Stage-B FP to this phenomenon without SELECT leakage or a prospectively justified diagnostic.

## Experiment integrity

No scientific training, SELECT outcomes, historical DEV, protected external tests, other folds, FactPICO or consumed 60-RCT holdout were accessed by this replay. The only external benchmark numbers used for comparison were pre-frozen Stage-B summary counts.

## Decision

`FREEZE_B_IN_SAMPLE_PERFECT_REPLAY; PRIORITIZE_OOF_UPSTREAM_FEATURE_AND_HARD_ERROR_BANK`.

Next action:
1. adversarial review of newly validated memorization/generalization gap and original EBM-NLPmod protocol;
2. one prospectively frozen TRAIN-only document-grouped cross-fitting plan for B and C contextual features, including gold-empty candidates, followed by typed-existence head, not architecture shopping;
3. STOP before any new training or protected benchmark.
