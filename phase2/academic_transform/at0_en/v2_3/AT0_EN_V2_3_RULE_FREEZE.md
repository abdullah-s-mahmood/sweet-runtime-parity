# AT0-EN V2.3 — Relation-Graph Rule Freeze

Date: 2026-10-03
Status: FROZEN BEFORE POST-FREEZE RED-TEAM
New model inference: NONE

## Frozen architecture

V2.3 uses a declarative typed SOURCE_RELATION_LEDGER and a generic relation verifier. Case IDs select data only; verifier code contains no EN01–EN12 case literals/branches.

Decision semantics:
- any VIOLATED relation => REJECT
- no VIOLATED but one or more UNRESOLVED => REVIEW
- all protected relations VERIFIED => PASS_CANDIDATE

PASS_CANDIDATE remains bounded synthetic evidence only.

## Development gate

Run: 37131967804
Trigger SHA: e9252aecf753dc0f23e9d95a669ea00f2e781ecd
Conclusion: SUCCESS
Artifact: 11277596087
Artifact digest: sha256:fe2b66c66c72e766b31a44941ead745424bbfbd5a5a022839dda05e27b45319c

Gate:
- total checks: 36
- passed: 36
- failed: 0
- legacy SAFE controls acceptable: 12/12
  - PASS_CANDIDATE: 9
  - REVIEW: 3
  - REJECT: 0
- V2.2 REDTEAM_V1 attacks caught: 24/24
- attack escapes: 0
- case-specific verifier literals: 0

Frozen identities from the successful run:
- SOURCE_RELATION_LEDGER.json: 50aa4df116164f2a6eb9ae74cfef4bb7c0254f48fb2fb1dbee1603bb65e71afa
- at0_v2_3_relation_verifier.py: a9e010c38b87ed2e30dfdada13ef8f22626373c8f603d6ed1e5c57d9f98a2725
- test_v2_3_relation_verifier.py: a2e76c8d15bc005643d0bd12cbc34fb16fde9aec2fd5076ac699bca2b3cd0d10
- development-gate detail: a2d45966da2e8dd66505fe3ae4a9422869c6b388154fb6b511762ff9612880b9
- development-gate summary: 382534a913ad9a4db7d69c5233ea01cfe2658c23a4c5376dc7043b2be6ff4130

## Frozen V2.2-pass replay

Run: 37132105455
Trigger SHA: 0a070893ef72c88898df86106c686d414fc209a1
Conclusion: SUCCESS
Artifact: 11277671099
Artifact digest: sha256:12cee86492a0d08db594a5d50ddcbed35e7c9a47ced07e36a90820269ae7148e

Input: exact 30 PASS_CANDIDATE cells from hardened V2.2 replay artifact 11276398612.

V2.3 adjudication:
- PASS_CANDIDATE: 10
- REVIEW: 16
- REJECT: 4
- known MODEL_A-EN01-DIRECT modality drift: REVIEW
- known EN01 drift no longer auto-passes: PASS

Interpretation:
V2.3 is substantially more conservative. REVIEW is not a claim of error; it means the typed protected relations were not all independently reconstructed.

## Freeze boundary

After this commit, do not modify the relation ledger or verifier in response to the post-freeze red-team.

Exact next action:
create a fresh REDTEAM_V2 after this freeze, with new counterfactual attacks not used to design V2.3. Run it once against these frozen hashes. Any failure is evidence for higher-model review, not permission to patch silently.

No live generation, HW1-EN, DR, Arabic resumption, reserved-data opening, or V4.2 rerun is authorized.
