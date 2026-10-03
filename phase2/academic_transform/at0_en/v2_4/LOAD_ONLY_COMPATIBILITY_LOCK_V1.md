# AT0-EN V2.4 — Load-Only Compatibility Evidence Lock

Date: 2026-10-03
Status: PASS
Semantic inference performed: NO

Run:
- id: 37134546523
- trigger commit: e2e15a0e7b210995e444092c7f93c7e8b79d9553
- artifact id: 11278246583
- artifact digest: sha256:815d7c229a634a5a877a184a95da54456ef31d5c12b39d5aa5af6aa5551586ef

Runtime:
- Python 3.11.16
- torch 2.2.2+cpu
- transformers 4.39.3
- safetensors 0.4.3
- sentencepiece 0.2.0

Safety controls:
- all 16 acquired files re-hashed against SEMANTIC_MODEL_FILE_HASH_LOCK_V1: PASS
- network blocked inside model-loading process after acquisition
- torch.nn.Module.__call__ replaced by a hard-fail guard before model loading
- no forward pass
- no semantic text pair scored
- no threshold calibrated

HHEM:
- class: HHEMv2ForSequenceClassification
- config: HHEMv2Config
- tokenizer: T5TokenizerFast from the pinned local FLAN dependency
- parameters: 109,630,082
- observed RSS after load: 715,716 kB
- load time: 0.355 s
- foundation overridden only from moving repo name to the pinned local FLAN directory; no semantic configuration changed

DeBERTa NLI:
- class: DebertaV2ForSequenceClassification
- config: DebertaV2Config
- tokenizer: DebertaV2TokenizerFast
- parameters: 184,424,451
- observed RSS after load: 1,040,116 kB
- load time: 0.298 s
- labels: 0 entailment / 1 neutral / 2 contradiction

Evidence file SHA-256:
- load_only_smoke.py: 16caf337841148c5081728ace1082addbe87a740a5e19cf1f824c206bcb9175f
- SEMANTIC_MODEL_FILE_HASH_LOCK_V1.json: 2f9e16aa18f3156a9ff3d73be5545d3c03f83e3b143e98c62017aac547dfb048
- LOAD_ONLY_COMPATIBILITY_SUMMARY.json: 1629261173908a75dd5416e91cb00aed4d1045974774a99ebd7c2a41ffa9be7b
- pip_freeze.txt: bf93b519f9bb8eafae063e6b6b9797c1a77c11c3055892f9f7b5788583d67603

Interpretation:
This establishes executable identity and load compatibility only. It does not establish semantic accuracy, calibration quality, scientific fidelity or threshold validity.
