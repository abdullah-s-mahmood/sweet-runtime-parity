# M2-R v1.1 — End Review

Date: 2026-09-30

## Decision

**Benchmark formulation: INVALID for the full sentence-level gate.**  
**Scientific understanding: IMPROVED.**  
**Direct annotated-error localization: weak.**  
**P1 is not run on this benchmark.**

P0 predictions were frozen before gold.

Directly interpretable measurements:
- Context residual recall: 51.11%.
- Annotated-error localization recall: 34.71%.
- Controlled expert-reinserted residual recall: 60.00%.
- Orthographic recall: 44.34%.
- Morphological recall: 51.16%.
- Syntactic recall: 20.00%.
- Lexical recall: 8.70%.

The proposed CLEAN_TARGET_CONTEXT assumption was falsified after the key was opened: several target contexts still contained clear mandatory errors outside the selected ArabiGEE annotations. Therefore observed clean false-positive rate and claim precision cannot be interpreted as true full-sentence metrics.

ArabiGEE remains valuable for taxonomy, structured explanation, direct expert error/target pairs, and per-annotation recall. It is not used as exhaustive zero-residual sentence gold.

Fresh end research confirms that QALB annotators were explicitly instructed to correct all errors in each sentence across spelling, punctuation, word choice, morphology, syntax, and dialectal usage. QALB14 TRAIN/DEV are therefore the stronger basis for M2-R v2 clean controls and full edit scripts.

No threshold is lowered. No confirmation/holdout is opened.
