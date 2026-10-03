# AT0-EN — English Academic Transformation Feasibility Slice

Status: V2.1 open-weight backend frozen; offline engineering gates passed; live 48-slot matrix has not started yet.

This slice validates reversible paragraph transactions, provenance, scope protection, deterministic replay/rollback, length diagnostics, and a language-pack boundary. It does **not** establish human-writing quality or scientific fidelity.

## Frozen offline evidence

```bash
python tests/run_preflight.py
python tests/run_portability_audit.py
```

Established before V2.1:
- frozen fixtures: 30/30 PASS;
- language portability audit: 10/10 PASS;
- F07 `authorized_scope` repair retained;
- critical Arabic evidence preserved without reopening reserved data.

## V2.1 execution backend

See:
- `docs/architecture/ACAD_PASS_AT0_EN_EXECUTION_BACKEND_AMENDMENT_V2_1.md`
- `MODEL_MANIFEST.json`
- `config.json`

Frozen real model configurations:
1. Qwen3-4B-Instruct-2507, GGUF Q4_K_M.
2. SmolLM3-3B, GGUF Q4_K_M.

Runtime: frozen `llama.cpp` commit recorded in `MODEL_MANIFEST.json`.

The intended execution environment is the free standard GitHub-hosted runner for this public repository. The workflow is:

`.github/workflows/at0_en_v2_1_open_weight.yml`

It contains a single job and executes all operations sequentially. No GitHub matrix/concurrent model jobs are used.

Additional monetary cost ceiling: USD 0.00.

## Live matrix

The frozen matrix remains:
- 12 cases;
- 2 model families;
- DIRECT and PLANNED;
- 48 slots;
- maximum 72 logical generations.

The backend runner writes slots, prompts and raw responses after every slot so partial evidence survives interruption. No best-of-N or quality regeneration is allowed.

Do not start HW1-EN, detector robustness, Arabic research, training, fine-tuning, or reserved-data access from this phase.

After the live workflow closes or hits a hard blocker, return a compact higher-model review packet before any later phase.
