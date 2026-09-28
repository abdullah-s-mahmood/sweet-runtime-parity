# Phase 2 Arabic development handoff

This folder transfers fixed development inputs and analysis code to `phase2-arabic-eval`. It contains no model binaries or sealed benchmark contents. `PROVENANCE_LEDGER.jsonl` is the original 150-case file unchanged; `DEVELOPMENT_TARGETS.jsonl` adds stable `target_id` metadata without changing case selection, source, reference, or original case IDs.

## Integrity gate

Run `python phase2/arabic_eval/validate_transfer.py` from the repository root. It checks 150 targets, 41 passage groups, 12 `NON_HUMAN_GOLD` scientific cases, the 59 excluded passage IDs, unique target IDs, provenance, and known input hashes. It does not execute SWEET.

## Eventual official runtime command

Only in the proven Python 3.10 / PyTorch 1.12.1 CPU / Transformers 4.30.0 environment, with `models/nopnx`, `models/pnx`, and pinned `upstream/text-editing` populated externally:

`python phase2/arabic_eval/run_official_sweet_development.py`

The runner verifies the two model hashes and CAMeL source commit before inference. It emits `artifacts/OFFICIAL_DEVELOPMENT_RAW.jsonl`, `artifacts/OFFICIAL_DEVELOPMENT_RUN_LOG.txt`, `artifacts/OFFICIAL_DEVELOPMENT_MANIFEST.json`, and separate scientific stress output. No runtime or weight acquisition occurs in this transfer.

After the raw file exists, `python phase2/arabic_eval/analyze_official_development.py` prepares conservative targeted-recovery and collateral-edit diagnostics. Collateral edits default to `REVIEW_REQUIRED`. Optional `--bootstrap` samples passage clusters, not 150 independent targets. Human/independent adjudication remains necessary for edit precision and semantic safety.
