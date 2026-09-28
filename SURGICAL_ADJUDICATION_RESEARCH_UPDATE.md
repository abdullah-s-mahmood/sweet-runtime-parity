# Focused research update — surgical Arabic GEC adjudication

## Focus before final recommendations

- The SWEET paper frames Arabic GEC as edit tagging and reports public benchmark performance and efficiency. It does not validate these Nahw passages or a source-preserving surgical renderer: https://aclanthology.org/2025.acl-long.875/
- Nahw supplies local grammatical corrections and explanations. Its single-location references cannot score a whole passage as fully corrected: https://aclanthology.org/2026.eacl-long.296/
- Selective prediction research supports a coverage–risk tradeoff; top-1 confidence still needs calibration for the actual edit task, especially by error type: https://aclanthology.org/2021.acl-long.84/
- Edit-disentangled GEC evaluation and edit-level voting are relevant to avoiding whole-sentence agreement as a false signal: https://aclanthology.org/2025.acl-long.10/ ; https://aclanthology.org/2026.bea-1.60/
- Arabic morphological tooling and alternative sequence-to-sequence GEC models provide research-backed candidates for future *tests*, not evidence that they outperform this run: https://aclanthology.org/2024.lrec-main.240/ ; https://aclanthology.org/2023.emnlp-main.396/
- Diacritics can affect token fragmentation. The current queue establishes 98 TOKENIZER_UNK_WORD suppressions; a new normalization path would have to preserve original graphemes and invert the mapping safely: https://aclanthology.org/2026.findings-eacl.22/

## What this adjudication adds

- On the same 41 passages, unknown-token/fragment contamination dropped from 37 raw NoPnx1 outputs to zero surgical NoPnx1 outputs, while 100 predicted hazards were suppressed.
- Among 60 applied edits, 49 are supported, seven wrong, two partial and two unnecessary. A confidence cutoff alone is insufficient: a wrong parenthesis deletion has top-1 confidence 0.970, while a supported بنيهم edit has confidence 0.347. Calibration must be measured against adjudicated edits, not inferred from a logit.
- Two suppressed tags plausibly address published targets (صناعتي, يتساوَ), but the queue lacks a safe mapped output and confidence; confirmed useful loss is zero and *possible* useful loss is two.
- Five automated exact target flags have no applied edit at that target. Metric alignment must explicitly require an edit and inspect the local result.
- Scientific-text preservation remains unproven: 12 authored stress inputs are useful invariant probes but not human-gold academic Arabic editing.

These sources inform interpretation and possible next tests. No broad market cycle, benchmark, safety-stack modification or threshold tuning was performed.
