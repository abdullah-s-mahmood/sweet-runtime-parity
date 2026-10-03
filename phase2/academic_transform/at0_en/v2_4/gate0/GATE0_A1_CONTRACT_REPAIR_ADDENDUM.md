# AT0-EN V2.4 — Gate 0 Contract Repair Addendum from Gate A1

Date: 2026-10-03
Status: CANONICAL CONTRACT REPAIR / PASS

Gate A1 exposed two Gate 0 representation defects before semantic extraction:

1. deterministic anchors existed only inside assertions, preventing pre-ownership extraction;
2. anchor provenance referenced evidence span IDs without a global evidence-span inventory.

Repairs:
- added top-level `anchors`;
- added top-level `evidence_spans`;
- replaced embedded assertion evidence objects with `evidence_span_ids`;
- assertion `anchor_refs` are convenience references only;
- semantic ownership remains graph-based;
- added `EXTRACT_BEFORE_OWNERSHIP` anchor inventory policy;
- added `GLOBAL_EVIDENCE_SPANS_ARE_CANONICAL` provenance policy.

Final repair validation:
- workflow run: `37142006598`
- trigger commit: `e67bc19dcd653530feadfd212b43a32e4e521845`
- artifact id: `11280702653`
- artifact SHA-256: `0f97953ed6a5a09b21b24c3578cb9134d29194a413da4fd3e3072a209401e2cb`
- checks: **326/326 PASS**
- model inference: none

Canonical Gate 0 hashes after repair:
- schema: `df986f759a114bd86525b84f00f8d2f362d71bb31546441992291d21c5ebd69f`
- criticality: `1599bf6bdb10afd462ba45a422b3e276a4ddbb47656d3d6047a0ff9b39acc48d`
- outcome contract: `aeff55ec0d5c10a949afc2f86a5eae46e610043f3885497643561b17aa669905`
- development reference: `c5fc21cf8ea60f0bd4b403b3a6e9220be33c1d390283a71f0365751ea54ed303`
- contract test: `d3315f86490d33c61ce311cf5efa9480fe70b2e79f9c59d8a6b81621935e1c7f`

The original Gate 0 closure remains historical provenance; this addendum supersedes its schema/criticality/test hashes as the canonical contract identity.
