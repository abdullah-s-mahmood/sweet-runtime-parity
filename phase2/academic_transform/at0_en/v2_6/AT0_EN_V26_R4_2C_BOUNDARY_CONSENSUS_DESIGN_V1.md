# AT0-EN V2.6 R4.2C — Boundary-Consensus Witness Design V1

Date: 2026-10-06
Status: DESIGN FROZEN BEFORE R4.2C IMPLEMENTATION
Branch: `at0-en-v2.6-dev`

## 1. Evidence basis

R4.2B source-aligned training:
- run: `37409097042`
- artifact: `11397202598`
- artifact digest: `sha256:45d204d5f073aa5ecc5944dc49bee88be5bb677e0160b8c17720f2250de6fa71`
- exact entity micro-F1 on frozen dev: `0.6783919598`
- exact entity macro-F1 on frozen dev: `0.6917395606`
- frozen calibration: FAIL

Dev-only boundary diagnostic:
- run: `37445035553`
- artifact: `11402997860`
- artifact digest: `sha256:6718d7007ed8b16f9644a33879e540ebadd26bcdbb248f98f21d5a74c8e0f5b1`
- diagnostic canonical pre-hash: `dc5920c1d3148f4b78c7fcde36d25efe78cbf3471db406a5c51e79d36b2d8431`
- tests/holdouts used: 0

At threshold 0.95:
- accepted entities: 326
- exact TP: 249
- exact-span errors: 77
- same-type boundary errors: 47 / 77 = 61.039%
- all overlap-related boundary/type errors: 59 / 77 = 76.623%
- spurious errors without overlap: 18 / 77 = 23.377%

Per-class exact precision at threshold 0.95:
- P: 40/52 = 0.769231
- I: 103/132 = 0.780303
- C: 14/15 = 0.933333
- O: 92/127 = 0.724409

Diagnostic same-class partial-overlap matching:
- exact entity micro-F1: 0.678392
- partial-overlap micro-F1: 0.831658
- diagnostic delta: +0.153266 (+15.33 pp)

Partial matching is DIAGNOSTIC ONLY. It does not replace or weaken the frozen exact-span gate.

## 2. Mechanism conclusion

The dominant failure is not simple low confidence.

The current confidence function is the minimum probability over tokens INSIDE the predicted entity. It is structurally unable to penalize a confidently predicted contracted span when omitted gold boundary tokens lie OUTSIDE the predicted entity. This explains why many exact-span errors survive a 0.95 threshold.

The observed pattern is consistent with published biomedical/PICO NER evidence that exact boundary selection is a major error source and that span-oriented architectures can complement sequence taggers.

Relevant literature:
- Hu et al., Bioinformatics 2023, DOI 10.1093/bioinformatics/btad542.
- Zhu & Li, ACL 2022, DOI 10.18653/v1/2022.acl-long.490.
- Verma et al., BioNLP 2023, DOI 10.18653/v1/2023.bionlp-1.24.
- Zhang et al., JAMIA 2024 (PICOX), DOI 10.1093/jamia/ocae065.

## 3. Feasibility bound without threshold relaxation

If an independent verifier rejected only the overlap-related boundary/type-disagreement errors at threshold 0.95, while pessimistically allowing every currently spurious prediction to remain, the resulting oracle upper-bound precisions would be:

- P: 40/(40+3) = 0.930233
- I: 103/(103+7) = 0.936364
- C: 14/(14+0) = 1.000000
- O: 92/(92+8) = 0.920000
- macro precision = 0.946649

Recall of the preserved exact TPs would remain:
- P: 0.740741
- I: 0.635802
- C: 0.482759
- O: 0.625850

All are well above the frozen 0.20 recall floor, and all classes retain >=10 exact TPs.

Therefore the frozen gate is feasible WITHOUT lowering thresholds if boundary/type-disagreement can be selectively detected.

## 4. R4.2C architecture decision

R4.2C will be a SELECTIVE BOUNDARY-CONSENSUS VERIFIER.

Frozen R4.2B remains the candidate BIO detector.

Add an architecturally different span-boundary witness:
1. start/end boundary localization;
2. P/I/C/O span classification;
3. same safe PubMedBERT-family base path unless a preflight proves another safe identity is necessary;
4. train only on the already-authorized training split;
5. frozen dev is development/calibration only;
6. no EBM/COVID/AD test access during design or tuning.

Automatic witness acceptance requires:
- R4.2B candidate survives the frozen confidence threshold;
- span verifier predicts the SAME class;
- span verifier agrees on EXACT start/end boundaries;
- span verifier confidence satisfies its pre-frozen acceptance rule;
- no deterministic critical contradiction exists.

Any disagreement -> REVIEW.
The span verifier can never override a critical deterministic contradiction.

## 5. Explicitly rejected alternatives

Rejected:
- lowering the 0.90 per-class precision gate;
- changing the frozen threshold grid after observing results;
- replacing exact-span scoring with partial-match scoring;
- regex/post-hoc boundary patching learned from individual dev examples;
- rerunning FactPICO;
- rerunning the consumed 60-RCT holdout;
- opening EBM/COVID/AD test sets;
- retraining the same BIO model alone as the primary repair.

## 6. R4.2C development gate

Keep the existing calibration requirements unchanged:
- precision >=0.90 for each P/I/C/O;
- recall >=0.20 for each P/I/C/O;
- >=10 accepted predictions for each class;
- macro precision >=0.90;
- use the lowest threshold in the frozen grid that satisfies all requirements.

Additional R4.2C integrity requirements:
- exact boundary agreement is mandatory for auto-acceptance;
- disagreements are REVIEW, never silently repaired;
- all selected weights are safetensors;
- deterministic hashes and provenance recorded;
- tests remain unopened until R4.2C development gate passes.

If no candidate threshold passes:
`R4_2C_BOUNDARY_CONSENSUS_NOT_READY`

## 7. Exact next step

Run one development-only R4.2C PRE-FLIGHT:
- verify training/dev identities and no test access;
- verify span-candidate capacity and label construction;
- verify model-safe-loading path;
- verify exact-agreement scorer mechanics;
- freeze training protocol before any R4.2C training.

No R4.2C training is authorized until that preflight passes.
