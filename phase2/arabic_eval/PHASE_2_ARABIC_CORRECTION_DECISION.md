# Phase 2 — Real Arabic Correction Evaluation: current evidence state

**PHASE NOT COMPLETE; decision not issued.** This is an execution block on quality measurement, not evidence that SWEET failed. The four requested outcomes GO WITH CONSTRAINTS / MODIFY / PIVOT / STOP require actual correction and safety results; assigning one from the official demo would be unsound.

## Completed now

- Fresh research and technical opportunity scan at start.
- 150 development single-target expert-annotated pairs from 41 Nahw passages, with full provenance and 59 prior-sealed passage IDs excluded; source correlation remains high.
- 12 project-authored scientific invariant stress inputs clearly separate from human annotations.
- Existing deterministic minimal tagger ran on 150 pairs: 0 changed, 0 target exact matches. This is a narrow baseline, not comparative model quality.
- Reproducible official-runtime development runner prepared and syntax checked; it rejects missing files and verifies both weight hashes before import/inference.

## Blocker

In this workspace Python is 3.12.14, and PyTorch/Transformers, the two model directories, and the claimed official runtime outputs are absent. The user's established official runtime success is retained as project evidence, but outputs on the new 150 pairs cannot be generated here. The earlier NumPy/SciPy implementation is deliberately not substituted for quality evaluation.

## Exact next execution

Run `run_official_sweet_development.py` in the proven Python 3.10 environment with `--nopnx`, `--pnx` and `--gec-repo` pointing to the local official directories. Return `OFFICIAL_DEVELOPMENT_RAW.jsonl`, exact source commit, and runtime log to this workspace. The script uses local weights only and records subwords, raw labels, softmax top-1 confidence, outputs and timing for NoPnx×2, Pnx-only and full pipeline. Then measure target-edit coverage, review burden and failure types, perform the required mid-phase challenge, freeze a bounded policy, obtain a genuinely independent sealed set, and finally issue one of the four decisions. A certified clean-input sample and science-domain human corrections remain additional external data gaps.

No Phase 3, user recruitment, commercial pilot, or sealed evaluation was started.
