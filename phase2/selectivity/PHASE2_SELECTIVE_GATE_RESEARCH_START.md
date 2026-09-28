# Phase 2 — Selective Surgical Gate: Start Research

Date: 2026-09-28

This gate remains DEVELOPMENT ONLY. No sealed benchmark, production threshold, Phase 3 work, model-weight modification, or frozen safety-stack modification is permitted.

## Fresh research check before execution

1. **Arabic GED/GEC has a public reproducible path.** CAMeL-Lab's EMNLP 2023 Arabic GEC work defines multi-class Arabic grammatical error detection (GED), publishes GED/GEC models, and reports that GED auxiliary information improves GEC across three datasets. The public repository exposes `CAMeL-Lab/camelbert-msa-qalb14-ged-13` for token classification.  
   - Paper: https://aclanthology.org/2023.emnlp-main.396/  
   - Repository: https://github.com/CAMeL-Lab/arabic-gec  
   - Model collection: https://huggingface.co/collections/CAMeL-Lab/arabic-ged-and-gec

2. **SWEET remains relevant as an edit candidate generator.** The ACL 2025 SWEET work is token-edit based, publishes the exact model family already used in this repository, and reports strong Arabic benchmark performance and efficiency. The present gate therefore tests routing/selectivity rather than replacing SWEET by assumption.  
   - https://aclanthology.org/2025.acl-long.875/

3. **Selective prediction supports explicit abstention.** Risk–coverage analysis is a better framing than forcing a correction on every candidate.  
   - https://aclanthology.org/2021.acl-long.84/

4. **Edit-disentangled evaluation is preferred.** Hit/wrong/under/over-correction should remain separated; whole-passage exact equality is not the quality metric.  
   - https://aclanthology.org/2025.acl-long.10/

5. **Arabic tokenization/diacritics require caution.** Recent Arabic evidence shows diacritics can increase token fragmentation. This motivates a reversible model-view probe only; delivered source text remains untouched.  
   - https://aclanthology.org/2026.findings-eacl.22/

## Pre-execution hypotheses

- H1: An operation-aware gate will remove most known wrong NoPnx1 surgical edits while retaining a useful subset of supported edits.
- H2: DELETE edits will remain the riskiest family and should be abstained from by default in this bounded prototype.
- H3: A separate Arabic GED model will provide useful localization signal, but it must not be treated as ground truth and must not be tuned against Nahw target locations in this gate.
- H4: Reversible diacritic stripping may reduce some tokenizer-UNK cases; any normalization that cannot round-trip to exact source offsets must remain diagnostic only.
- H5: Precision may improve materially, but coverage of the 150 published corrections is likely to remain the main bottleneck.

## Anti-leakage rule

Nahw target spans may be used only for **evaluation** of GED localization and target recovery. They MUST NOT be used by the runtime selective policy.

The runtime policies may use only:
- SWEET edit operation family;
- SWEET top-1 confidence;
- source-safe mapping status;
- scientific protected-span locks;
- tokenizer hazard state;
- independently predicted GED labels/probabilities.

