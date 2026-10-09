# ACAD_PASS — SURUS Auxiliary Human-Gold Admission Evidence Freeze V1

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `at0-en-v2.6-dev`

State:
`SURUS_PUBLIC_HUMAN_GOLD_CANDIDATE_EVIDENCE_FROZEN / NOT_YET_ADMITTED_TO_FEDERATION_PROTOCOL`

## 1. Purpose

Freeze the read-only public-source evidence gathered for SURUS before any decision that could alter the prospectively frozen ACAD_PASS federation protocol.

This record does NOT authorize:
- successor scientific training;
- adding SURUS to D0-D4;
- changing native P/I/C/O labels;
- changing D2-D4 auxiliary loss structure;
- opening VERIFY_INTERNAL;
- opening or scoring AD/COVID external benchmark labels;
- replacing any frozen source or arm.

## 2. Public source identity and schema audit

GitHub Actions run:
`37900075427`

Workflow:
`Federation SURUS public schema audit`

Run state:
`COMPLETED / SUCCESS`

Artifact:
`11602016518`

Artifact digest:
`sha256:0549f36abf6d1cac39d87dec2206514c7a5a59a8ba2ca083d89c54d53ff26772`

Pinned SURUS source:
- repository: `surus-ai/dataset`
- commit: `3a61790d5c304dea95fb278f76cc3b1a0ca07564`
- license: `CC-BY-NC-4.0`
- license SHA256: `1cbffd11334c34e0ac50fffc799a8fd470ff0398b40b199511711fd8dbe4278c`

Observed public corpus structure:
- article rows: 523
- unique PMIDs: 523
- annotation rows: 48,833
- in-domain documents: 400
- indication out-of-domain documents: 90
- study-type out-of-domain documents: 33
- label count: 25
- label-class count: 7
- missing article foreign keys: 0
- missing label foreign keys: 0
- invalid coordinate rows: 0

The audit emitted no raw article text, no PMID values, and no scientific metric.

Audit interpretation:
`Candidate auxiliary human-gold source only; no native P/I/C/O mapping is authorized by this audit.`

## 3. Published human-annotation evidence

The 2025 peer-reviewed SURUS evaluation reports a manually annotated dataset built under a strict annotation guide. The paper reports:
- 400 clinical abstracts for the main annotated evaluation set;
- 39,531 labels in the described training/evaluation subset;
- inter-annotator agreement Cohen's kappa = 0.81;
- inter-annotator F1 = 0.88;
- evaluation over 25 fine-grained entity labels.

The publication's reported model F1 values are NOT directly comparable to ACAD_PASS strict exact-span native P/I/C/O metrics and MUST NOT be headline-ranked against ACAD_PASS without a matched task/schema/split/matching procedure.

Reference:
Peeters C, et al. Evaluation of SURUS: a named entity recognition NLP system to extract knowledge from interventional study records. BMC Medical Research Methodology. 2025;25(1):184. DOI 10.1186/s12874-025-02624-z. PMID 40745274.

## 4. Protected/exposed overlap custody audit

GitHub Actions run:
`37900288357`

Workflow:
`Federation SURUS overlap custody audit`

Run state:
`COMPLETED / SUCCESS`

Artifact:
`11602601668`

Artifact digest:
`sha256:915be5e4fd758b90b959eae4700c774b441dda19f358310165ccfcd6a6517a5e`

SURUS population:
- all: 523
- in-domain: 400
- OOD: 123

Observed exact PMID overlaps for SURUS_ALL:
- DESIGN: 0
- VERIFY_INTERNAL: 0
- OLD_SELECT: 0
- AD resolved whole/test: 0 / 0
- COVID-19 resolved whole/test: 0 / 0
- EvidenceOutcomes: 7
- PICO-Corpus: 2
- TrialSieve train/validation: 1

In-domain overlaps:
- EvidenceOutcomes: 6
- PICO-Corpus: 2
- TrialSieve train/validation: 0
- protected historical sets: 0

OOD overlaps:
- EvidenceOutcomes: 1
- PICO-Corpus: 0
- TrialSieve train/validation: 1
- protected historical sets: 0

No PMID values, protected IDs, or raw text were emitted.

## 5. Limitations

This custody evidence is necessary but not sufficient for full family independence.

Explicit limitations:
1. PMID equality is not full trial-family identity.
2. AD/COVID title resolution remains partial.
3. Historical EBM mapping remains partial.
4. Any SURUS inclusion must still use per-fold family decontamination.
5. CC-BY-NC-4.0 does not authorize unrestricted raw-data redistribution or commercial use; no broader license permission is inferred here.

## 6. Scientific interpretation

SURUS is a credible candidate auxiliary human-gold corpus because:
- it is manually annotated;
- annotation quality is documented in peer-reviewed literature;
- it has a fine-grained ontology that can remain native rather than being collapsed into P/I/C/O;
- exact PMID custody found no overlap with currently mapped DESIGN / VERIFY_INTERNAL / OLD_SELECT;
- its overlap with other auxiliary public corpora is small and can be deterministically decontaminated.

However, the current frozen D0-D4 protocol names the allowed auxiliary sources and does not include SURUS.

Therefore adding SURUS to D2-D4 is a MATERIAL PROTOCOL CHANGE.

No automatic admission is authorized.

## 7. Frozen decision boundary

Current decision:
`SURUS_ELIGIBLE_FOR_INDEPENDENT_ADMISSION_REVIEW_ONLY`

Allowed next:
- independent adversarial scientific review of whether SURUS should be added as a native fine-grained auxiliary head/source to D2-D4;
- review must determine exact admitted partition, decontamination rule, ontology handling, license/redistribution boundary, and whether adding it changes the fairness of D0/D1 vs D2-D4 comparisons.

Not allowed before that review:
- SURUS scientific fitting;
- changing the frozen 45-fit attempt budget;
- adding a seventh adaptive arm;
- using SURUS to tune thresholds against protected or external benchmark data;
- mapping SURUS fine-grained labels directly to native P/I/C/O without a separately justified prospective rule.

## 8. Existing campaign state remains unchanged

The authoritative hardware-independent pre-fit snapshot remains:
- F01-F06 closure: 94.5%
- first-fit process readiness: 89.7%
- successor scientific training: NOT STARTED
- R44C: FROZEN / CONSUMED
- VERIFY_INTERNAL: CLOSED
- D5: CANCELED WITHOUT REPLACEMENT

SURUS evidence does not itself increase these readiness percentages because it is an optional candidate expansion, not closure of a current blocking requirement.

Exact next safe operation:
`INDEPENDENT_SURUS_ADMISSION_REVIEW -> KEEP_OR_REJECT_PROTOCOL_CHANGE -> THEN_RESUME_GPU_QUALIFICATION_AND_FINAL_PREFIT_CLOSURE`
