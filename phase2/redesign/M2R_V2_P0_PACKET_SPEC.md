# M2-R v2 P0 Packet Specification

Date: 2026-09-30
Status: FROZEN BEFORE FEASIBILITY RESULT

Salt: `M2R-V2-P0-DEV-A`.

Selection from DEVELOPMENT only:

1. Select 30 fully reconstructable lines with at least one STRICT edit for QALB_ALL_BUT_ONE_STRICT.
   - choose withheld STRICT edit deterministically by hash;
   - apply all other M2 edits;
   - withheld source surface must remain verbatim.

2. Select 60 remaining fully reconstructable lines with >=1 primary-detectable edit for NATURAL_QALB_SOURCE.

3. Select 30 remaining fully reconstructable lines for CLEAN_QALB_REFERENCE.

All 120 sentence IDs are unique.

Blind artifact:
- case_id
- candidate

Hidden key:
- split / line ID
- family
- primary-detectable gold surfaces + replacements
- withheld edit metadata for STRICT family.

Quality gates:
- 120 cases / 120 unique sentence IDs;
- family counts 60/30/30;
- STRICT pool selected 30;
- NATURAL cases each have >=1 primary-detectable gold edit;
- CLEAN candidates equal full human corrected reference;
- no confirmation/holdout IDs.
