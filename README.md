# SWEET Official Runtime Parity

This repository performs a reproducible Phase 2 verification of the official PyTorch/Transformers execution path for the CAMeL-Lab SWEET Arabic grammatical error correction models.

## Previously established real-weight evidence

- NoPnx SHA-256: `584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6`
- Pnx SHA-256: `195696eaf09a5b92d8141f473e0e3a0d5a710649114b3180afb25cf76cdaa4f3`
- NoPnx classifier: 315 x 768
- Pnx classifier: 51 x 768
- Real-weight NumPy/SciPy pipeline: PASS
- Official PyTorch/Transformers parity: pending

This repository tests runtime parity only. It does not claim semantic safety or final benchmark validity.
