# Local-Edit Semantic Backstop — Brainstorm Start

Date: 2026-09-29

| Idea | Decision | Reason |
|---|---|---|
| Whole-sentence historical mDeBERTa rule | TEST | Existing ACAD_PASS baseline; may miss small local changes or over-review Arabic. |
| Local-window historical rule | TEST | Gives the changed span greater semantic weight. |
| Contradiction-only whole/local veto | TEST | Lower review burden candidate; low entailment alone is not proof of danger. |
| Tune many NLI thresholds | DROP | Consumed slice would overfit rapidly. |
| LLM judge | DROP | Not reliable enough as sole correctness oracle. |
| Train a meta-classifier on 159 labels | DROP | Too small and repeatedly inspected. |
| Combine risk-family labels with NLI immediately | DEFER | Measure NLI marginal value independently first. |
| Promote directly from this diagnostic | PROHIBITED | Requires fresh disjoint validation. |
| Persist QALB text | PROHIBITED | License and evidence rules. |

## Main question

Can a semantic backstop remove a meaningful fraction of the 15 unsafe exact-agreement edits while retaining at least 80% of the 144 supported edits and reviewing no more than 25% of the stream?