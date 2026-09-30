# M2-R v1.1 — End Brainstorming

Date: 2026-09-30

KEEP:
- exact residual-span output;
- mandatory-vs-optional separation;
- exact-surface validation;
- ArabiGEE taxonomy/explanation support.

REMOVE FROM PRIMARY GATE:
- ArabiGEE target contexts as globally clean controls;
- full-sentence precision/false-positive metrics against selective annotations.

NEXT DESIGN:
- QALB14 TRAIN+DEV full human-corrected references for clean controls;
- official M2 as complete reference edit script where reconstruction is verified;
- controlled all-but-one residuals from reconstructable M2 lines;
- punctuation/register-sensitive edits reported separately from the strict mandatory-error gate.

DO NOT:
- run ArabiGEE P1;
- open ArabiGEE confirmation/holdout;
- open QALB14 TEST or QALB15;
- open A7ta reserve;
- lower thresholds.
