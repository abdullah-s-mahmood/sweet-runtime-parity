# ACAD_PASS — Federation Progress Snapshot V4

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

State:
`PREFIT_CLOSURE_NEAR_COMPLETE / SURUS_CANDIDATE_FROZEN_PENDING_INDEPENDENT_ADMISSION_REVIEW / GPU_BACKEND_AND_FINAL_PREFIT_REVIEW_PENDING / NO_SUCCESSOR_SCIENTIFIC_FIT`

## Current quantified readiness

Mandatory independent-review findings F01-F06:
`94.5%`

First scientific federation-fit process readiness:
`89.7%`

Previous intermediate snapshot:
- F01-F06: 90.0%
- first-fit readiness: 73.5%

Change versus that intermediate snapshot:
- F01-F06: +4.5 percentage points
- first-fit readiness: +16.2 percentage points

These percentages are protocol/mechanical readiness only, NOT model accuracy and NOT probability of scientific success.

## Latest durable evidence

### SURUS public schema audit
- run `37900075427` SUCCESS
- artifact `11602016518`
- digest `sha256:0549f36abf6d1cac39d87dec2206514c7a5a59a8ba2ca083d89c54d53ff26772`
- source `surus-ai/dataset@3a61790d5c304dea95fb278f76cc3b1a0ca07564`
- license `CC-BY-NC-4.0`
- 523 articles / 523 unique PMIDs
- 48,833 annotation rows
- 25 labels / 7 label classes
- 400 in-domain + 123 OOD
- no raw article text or scientific metric emitted.

### SURUS overlap custody audit
- run `37900288357` SUCCESS
- artifact `11602601668`
- digest `sha256:915be5e4fd758b90b959eae4700c774b441dda19f358310165ccfcd6a6517a5e`
- exact PMID overlap with mapped DESIGN / VERIFY_INTERNAL / OLD_SELECT = 0 / 0 / 0
- resolved AD whole/test overlap = 0 / 0
- resolved COVID-19 whole/test overlap = 0 / 0
- overlaps requiring decontamination: EvidenceOutcomes 7, PICO-Corpus 2, TrialSieve train/validation 1
- no protected IDs, raw text, or PMID values emitted.

Frozen record:
`AT0_EN_V26_SURUS_AUXILIARY_ADMISSION_EVIDENCE_FREEZE_V1.md`
commit:
`be5a2ee8cf66cec5d86d878aa9b5a558f78552cc`

## Scientific-performance state

No federation successor fit has been run.

Latest real model evidence remains frozen R44C at t=.95:
- macro precision 0.8767348592080204
- P 0.8918918918918919
- I 0.8171091445427728
- C 0.9318181818181818
- O 0.8661202185792349

Scientific-performance delta:
`NOT COMPARABLE / NO NEW MODEL RESULT`

## What improved

- hardware-independent pre-fit closure remains near complete;
- 45 active D0-D4 attempts remain bound to frozen data/runtime contracts;
- exact checkpoint/resume mechanics are closed;
- SURUS now has a durable public-source schema and overlap-custody evidence package;
- SURUS appears scientifically credible as a possible fine-grained auxiliary human-gold source without observed mapped protected-set PMID collisions.

## What worsened / new risk

No observed model-performance deterioration.

New protocol risk:
SURUS was not part of the currently frozen auxiliary-source matrix. Adding it to D2-D4 would materially change the protocol and could affect comparison fairness. Therefore it is NOT admitted automatically.

Residual blockers:
1. qualified real GPU backend;
2. GPU qualification artifact and exact runtime hash;
3. bind GPU runtime hash into all 45 active attempt slots;
4. final independent pre-fit review;
5. residual external trial-family identity remains an explicit limitation.

## Current authorization

Current GO/NO-GO:
`NO-GO FOR SCIENTIFIC FIT`

SURUS:
`CANDIDATE_ONLY / INDEPENDENT_ADMISSION_REVIEW_REQUIRED`

VERIFY_INTERNAL:
`CLOSED`

R44C:
`FROZEN / CONSUMED / NOT_RERUN`

D5:
`CANCELED_WITHOUT_REPLACEMENT`

## Exact next sequential operation

`INDEPENDENT_SURUS_ADMISSION_REVIEW`

The review must either:
- REJECT SURUS and preserve the current D0-D4 protocol unchanged; or
- AUTHORIZE a narrowly specified protocol amendment defining source partition, family decontamination, native auxiliary ontology, license boundary, and comparison fairness.

Only after this decision:
`QUALIFY_REAL_GPU -> BIND_GPU_RUNTIME_HASH_TO_45_SLOTS -> FINAL_INDEPENDENT_PREFIT_REVIEW -> FIRST_D0_D4_SCIENTIFIC_FIT`
