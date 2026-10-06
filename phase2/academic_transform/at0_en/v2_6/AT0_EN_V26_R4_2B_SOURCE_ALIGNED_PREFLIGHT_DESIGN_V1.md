# AT0-EN V2.6 R4.2B — Source-Aligned Preflight Design V1

Date: 2026-10-06

V5 completed valid training and calibration but ended \`R4_2_WITNESS_NOT_READY\`.

Frozen V5 identity:
- run \`37372306905\`, attempt 2;
- artifact \`11385322641\`;
- digest \`sha256:1d52c85a514e56defe471a6690f5367d046f65c93f52659ed94ea3d104ffb7d0\`;
- selected model SHA256 \`65a790b56e232d847b84a2fd19df86a1fdc87e56eb2a6147e5d6b82fea8ab6d0\`;
- best exact entity macro-F1 \`0.6841077577026645\`;
- exact entity micro-F1 \`0.665\`.

At threshold 0.95:
- P precision 0.7400;
- I precision 0.843137;
- C precision 0.941176;
- O precision 0.831325;
- macro precision 0.838910.

The limiting factor is high-confidence exact-entity false positives for P/I/O, not recall or minimum accepted-count degeneracy.

Pinned source repository:
\`BIDS-Xu-Lab/section_specific_annotation_of_PICO@bc4b878773192f38b2600ec830ca4208b82f7dc0\`

Source-code audit found material V5 differences:
- source weight_decay 0.0 vs V5 0.01;
- source warmup_steps 0 vs V5 warmup_ratio 0.10;
- source seed 42 vs V5 20261005;
- source eval batch 8 vs V5 16;
- source fixed 10 epochs without V5 early stopping/best-checkpoint loading;
- source update_data_to_max_len safely splits long sequences at an effective 252-wordpiece budget;
- V5 hard-truncated at tokenizer max_length 256.

Purpose: quantify protocol/preprocessing mismatch before authorizing any new training.

No training. No EBM/COVID/AD tests. No FactPICO. No consumed 60-RCT holdout.
