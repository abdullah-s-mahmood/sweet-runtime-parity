# ACAD_PASS — SURUS Pause and Four-Source Reversion Freeze V1

Date: 2026-10-10
Timezone: Asia/Baghdad (UTC+3)
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `at0-en-v2.6-dev`

State:
`SURUS_PAUSED_CURRENT_CAMPAIGN / FOUR_SOURCE_FALLBACK_RESTORED / PREFIT_REBIND_IN_PROGRESS / NO_SCIENTIFIC_FIT`

## Authority

Independent final review:
`FINAL_SURUS_SOURCE_CONTRACT_REREVIEW_V2.md`

Frozen verdict:
`REJECT_OR_PAUSE_SURUS`

Exact authorized operation:
`FREEZE_SURUS_PAUSE_AND_REBIND_ORIGINAL_FOUR_SOURCE_PREFIT_MANIFESTS`

Review SHA256 supplied and verified:
`3bc60c5c0ef42a13982fd65a346c674c57471c25252f7df4320ac79d3b29ffd5`

Evidence-package SHA256:
`c6f9fe664ab1ad65d7fc6b80d29ccbc4fcd3a61011be16f746e28158677f7e45`

Evidence ZIP internal manifest:
`41 / 41 entries verified; 0 hash mismatches`

GitHub review freeze commit:
`d63e73ad4df001c4e4c1afb9a6c9dd4eefa09f87`

Evidence verification commit:
`938b33ec61961e0d68321c7f9ea0321010c3ed66`

## 1. SURUS status

SURUS is:
`PAUSED / NOT_ADMITTED_TO_CURRENT_SCIENTIFIC_CAMPAIGN`

This is a bounded campaign decision.

It does NOT assert:
- that SURUS human annotations are generally invalid;
- that released Start/End are wrong;
- that SURUS cannot be reconsidered in a future prospectively reviewed campaign.

Reopening requires materially new source evidence identifying authoritative fields, exact text serialization/offset semantics, and a prospectively fixed lossless representation for every admitted positive.

No further unguided tokenizer/convention search is authorized as the current next step.

All SURUS V1-V7 evidence remains immutable historical evidence.

The five-source Amendment V2 remains preserved as historical protocol evidence but is:
`NON_EXECUTING_FOR_CURRENT_CAMPAIGN`

It is not deleted or rewritten.

## 2. Restored auxiliary source set

Current first-campaign auxiliary human-gold sources are exactly:

1. original EBM-NLP P/I/O auxiliary;
2. TrialSieve 20-type auxiliary, admitted stored train+validation only;
3. EvidenceOutcomes outcome-only auxiliary;
4. PICO-Corpus native fine-grained auxiliary ontology.

SURUS is not source 5.

DISTANT-CTO remains non-training contextual evidence because D5 was canceled prospectively.

No replacement source is authorized.

## 3. Restored auxiliary loss

Freeze:

`L_aux = (L_EBM + L_TrialSieve + L_EvidenceOutcomes + L_PICO) / 4`

`L = L_native + 0.25 * L_aux`

Therefore each admitted source contributes an effective total-loss coefficient:

`0.25 / 4 = 0.0625`

No:
- coefficient sweep;
- source-weight tuning;
- dynamic weighting;
- SURUS term;
- replacement-source term.

The existing four-head synthetic architecture preflight already implements:
`.25 * mean([EBM, TrialSieve, EvidenceOutcomes, PICO])`

## 4. Restored auxiliary document sampler

Total auxiliary documents per optimizer update:
`8`

Equal four-source allocation is deterministically:

`2 / 2 / 2 / 2`

because:
`8 total documents / 4 equal admitted sources = 2 documents/source/update`.

Canonical sampler contract:
`AT0_EN_V26_FEDERATION_FOUR_SOURCE_SAMPLER_CONTRACT_V1.json`

Freeze commit:
`cd87de53da1718eda06468afdfe42296fc9cf8b7`

Document ordering remains label-independent and deterministic.

Matched D2/D3/D4 fold/seed instances must use identical source membership and source schedules.

## 5. Existing executable manifests were not five-source mutated

Inspection after the review established that the canonical execution manifests still predate SURUS execution:

- `AT0_EN_V26_FEDERATION_SOURCE_ADMISSION_V1.json` contains the original four auxiliary sources and no SURUS training admission;
- `AT0_EN_V26_FEDERATION_SOURCE_PIN_MANIFEST_V1.json` contains no SURUS source pin;
- `AT0_EN_V26_FEDERATION_SCIENTIFIC_RUNTIME_CONTRACT_V1.json` contains the original model/runtime identities and no SURUS-specific runtime;
- `AT0_EN_V26_FEDERATION_DEVELOPMENT_ATTEMPT_MANIFEST_V1.json` still binds the original 45 active D0-D4 attempt identities.

Therefore this operation is a prospective versioned REBIND, not a destructive rollback.

No old manifest is silently edited to pretend the SURUS review never happened.

## 6. Attempt continuity

Current manifest:
`AT0_EN_V26_FEDERATION_DEVELOPMENT_ATTEMPT_MANIFEST_V1.json`

Verified:
- D0 = 9 slots;
- D1 = 9;
- D2 = 9;
- D3 = 9;
- D4 = 9;
- active D0-D4 = 45;
- active slots NOT_STARTED = 45/45;
- active slots consumed = 0;
- scientific_training_authorized = false for all active slots.

D5:
- 9 slots;
- state `CANCELED_NO_OFFICIAL_SEMANTIC_TYPE_LABELS`;
- consumed = 0;
- no replacement.

Same attempt IDs must be preserved in the rebound manifest.

No new attempt namespace is authorized.

## 7. Existing data binding

The 45 active slots currently reference the same three per-fold data-manifest hashes:

Fold 0:
`7c79f752c38f30a7b4f220c5ab3ff7db3ec559baa1c80797f13b65833203e0b0`

Fold 1:
`1955fa751bb90960af10fcdae40fabe3ae36c06602b4aa00ad74aec9c6466e02`

Fold 2:
`eb28ffdc603f6e0df7a42e216909aa0540b52772008a843fca31cb0f815cb939`

Original evidence:
- run `37897592120`;
- artifact `11601066403`.

These existing data identities must be rebound, not regenerated merely because SURUS was paused.

Known contamination exclusions and protected reservations remain unchanged.

Previously excluded aliases are not automatically re-admitted.

## 8. Runtime binding

Canonical software runtime remains:
`AT0_EN_V26_FEDERATION_SCIENTIFIC_RUNTIME_CONTRACT_V1.json`

Current state:
`SCIENTIFIC_SOFTWARE_RUNTIME_FROZEN_GPU_SPECIFIC_BINDING_PENDING`

The 45 active attempts still carry:
`runtime_manifest_sha256 = PENDING_GPU_QUALIFICATION`

Therefore the four-source rebind does not invent a runtime change.

Outstanding requirement:
qualify and hash the real scientific GPU runtime before final pre-fit approval.

## 9. Protected evidence

Remain CLOSED:
- VERIFY_INTERNAL;
- AD/COVID external scoring;
- SURUS OOD scoring.

No protected score may be used in rebind or GPU qualification.

## 10. Exact current sequence

1. Run one non-scientific four-source manifest/binding preflight.
2. Freeze the resulting protocol/data/sampler/runtime/attempt binding.
3. Resume GPU qualification.
4. Bind qualified GPU runtime hash to the same 45 unconsumed attempt IDs.
5. Run final independent pre-fit review.
6. STOP until that independent pre-fit review returns PASS.
7. Only then may the first scientific job be considered.

No scientific training is authorized by this freeze.
