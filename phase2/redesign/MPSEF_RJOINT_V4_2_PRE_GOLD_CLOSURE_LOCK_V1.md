# MP-SEF R_JOINT V4.2 PRE-GOLD CLOSURE LOCK V1

Date: 2026-10-02
Status: PASS / PRE-GOLD IMPLEMENTATION CLOSED / AUTHORIZATION NOT YET ISSUED

## 1. Governing review

Independent delta-review verdict:
`MODIFY`

New BLOCKER/MAJOR findings:
`NONE`

Historical findings:
- B01 CLOSED
- B02 PARTIAL at review time
- M01 CLOSED
- M02 CLOSED
- M03 CLOSED
- M04 CLOSED
- M05 CLOSED
- N01 CLOSED
- N02 CLOSED

Required fixes before gold were:
1. repair V4.2 synthetic preflight defects;
2. complete A1 §A1.6 production wrapper/input lock;
3. freeze V4.2 closure evidence;
4. issue a separate exact-SHA-bound single-run authorization.

## 2. Scorer remediation closure

Scorer:
`phase2/redesign/mpsef_rjoint_score_v4_2.py`

Final scorer SHA256:
`be9cf725b71b8d26a23eff9e9afd4ca434294a4d8f72e0271caa179ca892f2e1`

Core:
`phase2/redesign/mpsef_rjoint_core_v2.py`

Core SHA256:
`b9f8c81706c266b75786e04a4363f8af8a5900eb9629acc99dac15ad72389d3c`

Repairs:
- T20 now isolates the intended external source-identity mismatch;
- T24 now contains a true SPLIT plus true MERGE route fixture;
- identity mismatch is enforced in `score_population_v4_2()` before target construction;
- incomplete identity contract fails closed;
- progress callback added without altering metric semantics.

Final source-free scorer preflight:
- PASS
- **33/33**
- status:
  `acad-pass/v4-2-rjoint-33of33 = success`

Harness SHA256:
`da31f7c1dd6d1f0bfd5356a54a19aba518742ce489f9f3d7d59242609566c25c`

Result SHA256:
`c46ac5e3fe6ffc349273104c6f8849b9628fa0383780e40e20fb077ad50b5a1e`

## 3. Production wrapper / B02 closure evidence

Production wrapper:
`phase2/redesign/mpsef_rjoint_v4_2_production_wrapper_v1.py`

Wrapper SHA256:
`72bf23c9f910c2b203caf11e6e677729fa914d66c2d1e062ac0fd7dfd6da357f`

Dependency contract:
`phase2/redesign/MPSEF_RJOINT_V4_2_DEPENDENCY_LOCK_V1.txt`

Dependency-lock SHA256:
`aa66ec3d6fdb4aef1b4fada26a1b6cf794f632139655e22462a7a1c27aab7bc5`

Wrapper preflight:
`phase2/redesign/mpsef_rjoint_v4_2_production_wrapper_preflight_v1.py`

Wrapper-test SHA256:
`d62696e3a2df2ee9fbb20839cef35bca7e4b0aec39155206837af400686c3ab8`

Wrapper result SHA256:
`1b03bf5a0192b35abd03d38b8d31c5a7396473fe1509bb39f591f418cf27a27e`

Source-free wrapper verification:
- PASS
- **14/14**

Combined status:
`acad-pass/v4-2-pre-gold-wrapper = success`

The wrapper fail-closes before any gold/reference read on:
- authorization mismatch;
- input-lock mismatch;
- source/action file SHA mismatch;
- population case/cluster mismatch;
- UID set mismatch;
- UID/cluster map mismatch;
- source text SHA mismatch;
- source/action identity mismatch;
- proposer/version/family/ancestry mismatch;
- scorer/core/wrapper/dependency identity mismatch;
- Python version mismatch;
- Arabic-GEC revision mismatch;
- matching/family/punctuation/result schema mismatch.

## 4. Exact full-C_F frozen identities

Population:
- UIDs: **1,918**
- clusters: **764**

Source manifest SHA256:
`051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

Legal action-set SHA256:
`e38393abb36734d3882e29a78f3b33c80718791957b9b8c0c6e8a8ab77f6e138`

Population UID SHA256:
`51e2e1decf1c7c9efbc31e343eba1c7dfb08d0de314041cb57f5b3118ffd550f`

Population cluster SHA256:
`bb2f49c6aaf312cf9c388237090a79861fa6218da15de57d0119efd39327ae3c`

UID↔cluster map SHA256:
`32b89f9dcadefa0f17cb0fddac6099433d611508a01ad96b428e0534c1057c5d`

Provenance-signature map SHA256:
`18561c75c397821c34e3dc06214bb4f64cc5ff8d6757f61835cbe9e6808befbd`

Observed complete full-population provenance signatures:
- KEEP / SYSTEM / KEEP / KEEP
- P1 / P1_FROZEN_V1 / SWEET_QALB14 / SWEET_NOPNX_ITER2
- P2 / P2_V2_1 / SEQ2SEQ_GED_MORPH / ARABIC_GEC_EMNLP2023_WORDALIGNED_REPAIR
- P3 / P3_V1_1 / SWEET_QALB14 / P1_CONTROL_PLUS_PNX1

No extra proposer/family signature was observed.

## 5. Gold identity remains frozen but unopened

Historical/frozen QALB M2 identity:
`971b6fbb28dc3767193e7a4b0f722c3abebfc8600155a57093ba483dac6491e8`

Calibration UID digest:
`3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9`

Gold projection version:
`MPSEF_CF_GOLD_PROJECTION_V2`

No gold/reference content was opened by the remediation or closure work recorded here.

## 6. Production input lock

File:
`phase2/redesign/MPSEF_RJOINT_V4_2_PRODUCTION_INPUT_LOCK_V1.json`

Commit:
`d71ad97e9b3ee47c4fbcbaf4a6d6fcdc66fcd744`

Input-lock SHA publication workflow:
`.github/workflows/phase2-mpsef-v4-2-input-lock-identity.yml`

Workflow commit:
`c49d572f82e3939ad4461ad0b78ff45655d2ac7b`

At closure time, three sequential status checks had not yet exposed the exact input-lock SHA context.

Therefore the following remains intentionally BLOCKED:
- final single-run authorization lock;
- any project gold/reference read;
- real R_joint V4.2 execution.

## 7. Scientific boundary

- linguistic quality newly measured: false
- real R_joint newly computed: false
- project gold newly opened: false
- selector trained: false
- family consensus activated: false
- P4 executed: false
- LLM judge used: false
- reserved/internal/stress populations opened: false

## 8. Classification

**IMPROVED STRONGLY / V4.2 SCORER + B02 WRAPPER VERIFIED / EXACT INPUT-LOCK SHA OBSERVABILITY IS THE ONLY REMAINING AUTHORIZATION BINDING STEP**

## 9. Exact next action

On the next continuation:
1. inspect commit `c49d572f82e3939ad4461ad0b78ff45655d2ac7b`;
2. capture `acad-pass/v4-2-input-lock-sha256/<SHA256>`;
3. bind that exact SHA into a separate single-run authorization lock;
4. validate the authorization lock itself;
5. only then allow one DEVELOPMENT-only V4.2 R_joint run under A1.
