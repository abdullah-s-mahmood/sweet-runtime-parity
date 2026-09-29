# Phase 2 — Sentence-Level Acceptability Feasibility Brainstorm Start

Date: 2026-09-29

| Candidate | Decision | Reason |
|---|---|---|
| English GRECO checkpoint directly on Arabic | DROP | English DeBERTa quality estimator is not defensible as an Arabic verifier without transfer evidence. |
| Generic Arabic NLI verifier | DROP | Earlier NLI-style evidence was not sufficient and does not target repair completeness. |
| CAD-style Arabic source/candidate discriminator | TEST | Directly targets sentence/context acceptability. |
| Train on current 14/36 adjudications | PROHIBITED | Direct leakage/overfitting. |
| Train on QALB15 corrected TRAIN | DROP for training | Current development source family should remain evaluation evidence. |
| Train on QALB14 external source/gold evidence | TEST | Pinned, independent from current QALB15 adjudications. |
| Random synthetic corruption | DROP | Weak match to observed partial-repair failure. |
| Gold-grounded local partial examples | TEST | Constructed from real QALB14 gold edits and directly models incomplete local repair. |
| Full BERT fine-tuning immediately | DEFER | Expensive; first establish signal with frozen encoder + lightweight classifier. |
| Frozen CAMeLBERT-MSA encoder | TEST | Arabic MSA model with exact public revision and reproducible inference. |
| Tune threshold on current labels | PROHIBITED | Threshold must freeze on QALB14 dev first. |
