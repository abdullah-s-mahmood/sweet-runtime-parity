# Cross-Training Tri-Model Voting — Research Start

Date: 2026-09-29

## Fresh research

- ACL 2025 Arabic text-editing work reports SOTA Arabic GEC performance and additional gains from model ensembles.
- BEA 2026 reports that edit-level majority voting can mitigate over-correction.
- TACL 2026 emphasizes edit representations as the appropriate granularity for GEC evaluation.
- CAMeL-Lab currently publishes MIT-licensed QALB14 and ZAEBUC SWEET NoPnx checkpoints and QALB14 AraBART GEC/GED checkpoints.

## Contamination check

AraBART-ZAEBUC is excluded because its public card describes training data including QALB-2015. SWEET-ZAEBUC is retained because its card describes ZAEBUC training, making QALB15 a cross-corpus evaluation for that voter.

## Hypothesis

If the 15 unsafe two-model agreements are partly caused by QALB14-specific correlated behavior, requiring support from a ZAEBUC-trained edit tagger may improve precision without collapsing coverage.