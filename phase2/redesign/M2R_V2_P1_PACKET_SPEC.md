# M2-R v2 P1 Packet Specification

Date: 2026-09-30
Status: FROZEN BEFORE P1 PACKET MATERIALIZATION

Prompt:
- `phase2/redesign/M2R_V2_PROMPT_P1.md`

Sources:
- QALB14 TRAIN + DEV only.
- No QALB15.
- No ZAEBUC DEV/TEST.
- No Confirmation/Holdout.
- No A7'ta reserve.

Partition:
- Use the existing M2-R v2 partition function.
- DEVELOPMENT only.

Disjointness contract:
1. Reconstruct the complete P0 selection deterministically using salt `M2R-V2-P0-DEV-A`.
2. Collect all 120 P0 UIDs.
3. Exclude those UIDs before any P1 family selection.
4. Select P1 with salt `M2R-V2-P1-DEV-B`.
5. Hard fail if P0/P1 UID overlap is non-zero.

P1 family counts:
- 60 NATURAL_QALB_SOURCE
- 30 CLEAN_QALB_REFERENCE
- 30 QALB_ALL_BUT_ONE_STRICT

All 120 P1 UIDs must be unique.

STRICT construction:
- exactly as in P0;
- one strict edit is withheld deterministically using the P1 salt;
- all other M2 edits are applied;
- the withheld source surface must remain verbatim.

Blind artifact:
- case_id
- candidate

Hidden key:
- uid / split / line
- family
- expert gold surfaces/replacements/M2 operation
- controlled-counterfactual flag

Pre-judgment quality gates:
- exactly 120 blind rows;
- exactly 120 key rows;
- family counts 60/30/30;
- 120 unique P1 UIDs;
- P0/P1 overlap = 0;
- every P1 UID is DEVELOPMENT;
- no Confirmation/Holdout exposure;
- no forbidden source family.

No threshold changes.
No P2 after P1.
