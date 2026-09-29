# Fine-Tuned Arabic CAD — Brainstorm Start

Date: 2026-09-29

| Option | Decision | Reason |
|---|---|---|
| Lower frozen-model threshold | PROHIBITED | Would tune to a failed external result. |
| Nonlinear MLP on same frozen features | DROP | AUC 0.584 suggests representation, not just linear boundary, is the main weakness. |
| Fine-tune CAMeLBERT pair classifier on external QALB14 | FINAL TEST | Closest practical Arabic analogue to trainable CAD. |
| Train on current 14/36 labels | PROHIBITED | Direct leakage. |
| Change negative construction | PROHIBITED in this test | Keep external task identical so improvement is attributable to representation learning. |
| Use QALB14 dev for early stopping/model selection | DROP | Dev remains threshold/reporting set; final epoch fixed in advance. |
| Try MARBERT/AraBERT after failure | NOT AUTHORIZED | Would start model shopping on the same evidence. |
| Spend fourth QALB15 slice | NOT YET | Requires external + consumed criteria first. |
