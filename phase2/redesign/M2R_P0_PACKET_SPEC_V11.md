# M2-R P0 Development Packet Specification v1.1

Date: 2026-09-30
Status: FROZEN BEFORE MATERIALIZATION

Salt: M2R-P0-DEV-A-V11

Selection:
1. Build eligible EXPERT_REINSERTED_RESIDUAL cases from DEVELOPMENT.
2. Select 30 by hash.
3. Select 60 NATURAL_ERROR_CONTEXT from remaining context IDs.
4. Select 30 CLEAN_TARGET_CONTEXT from remaining context IDs.

Eligibility for reinserted residual:
- nonempty erroneous_word and target_word;
- erroneous_word != target_word;
- target_word occurs exactly once in target_context;
- after reverse replacement, erroneous_word is present;
- no punctuation context;
- expert annotation has at least one structured dimension.

Quality gates:
- 120 total / 120 unique context IDs;
- family counts 60/30/30;
- >=20 orthographic gold instances;
- >=20 combined morphology+syntax+lexical gold instances;
- no confirmation/holdout context;
- blind and key artifacts separate.
