# AT0-EN — English Academic Transformation Feasibility Slice

Status: offline engineering implementation active; live matrix blocked until two authorized model identities and a cost ceiling are available.

This slice validates reversible paragraph transactions, provenance, scope protection, deterministic replay/rollback, length diagnostics, and a language-pack boundary. It does **not** establish human writing quality or scientific fidelity.

## Offline preflight

```bash
python tests/run_preflight.py
```

The command writes `results/offline-preflight/preflight_results.json` and exits non-zero if any of the 30 frozen fixtures fails.

## Live matrix

Not authorized by this repository state. Populate `MODEL_MANIFEST.json` and the budget fields in `config.json` only with already-authorized access, then freeze hashes before any live request. No Arabic data is an input to this harness.