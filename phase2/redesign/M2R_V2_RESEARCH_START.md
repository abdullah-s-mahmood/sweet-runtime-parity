# M2-R v2 — Fresh Research Start: Complete-Gold Residual Localization

Date: 2026-09-30
Status: PRE-REGISTERED BEFORE v2 DATA FEASIBILITY

## Why v2 exists

M2-R v1.1 proved that selective explanation annotations cannot support a whole-sentence false-positive gate. v2 separates the roles of the sources:
- QALB14 TRAIN/DEV: exhaustive human sentence correction and full edit scripts.
- ArabiGEE / ARETA: taxonomy and explanation support, not exhaustive sentence gold.

## Fresh research

The QALB shared-task description states that expert human annotators were instructed to correct **all errors** in each sentence, including spelling, punctuation, word choice, morphology, syntax, and dialectal usage. This makes its corrected sentence a defensible clean control under the corpus contract.

References:
- QALB 2014 Shared Task: https://aclanthology.org/W14-3605/
- QALB large-scale annotation framework: https://aclanthology.org/L14-1721/
- ARETA: https://aclanthology.org/2021.conll-1.47/
- Arabic text editing for GEC: https://aclanthology.org/2025.acl-long.875/
- ArabiGEE: https://arxiv.org/abs/2606.10765
- Closest-gold / multi-reference caution: https://aclanthology.org/2026.acl-long.2193/

## Scope decision

v2 tests **localization before classification**.

The verifier may still emit a dimension, but the primary gate asks only:
- did it localize mandatory residual errors?
- did it leave fully corrected expert references alone?

This avoids making an imperfect automatic taxonomy part of the core safety gate.
