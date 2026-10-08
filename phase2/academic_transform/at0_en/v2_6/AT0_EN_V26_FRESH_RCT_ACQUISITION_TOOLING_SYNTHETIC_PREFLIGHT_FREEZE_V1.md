# ACAD_PASS — Fresh RCT Acquisition Tooling Synthetic Preflight Freeze V1

Date: 2026-10-08

State:
`FRESH_RCT_ACQUISITION_TOOLING_SYNTHETIC_PREFLIGHT_PASS`

Acquisition:
`NOT_AUTHORIZED`

Real PubMed contact:
`NONE`

New RCT records:
`NONE`

Protected-corpus opening:
`NONE`

## 1. Official run

Workflow:
`Fresh RCT acquisition tooling synthetic preflight`

Run:
`37828800778`

Head SHA:
`d4080675a0cecec01ea931b0171b1a0f73282ab4`

Conclusion:
`SUCCESS`

Artifact:
- ID `11572806239`
- name `fresh-rct-acquisition-tooling-synthetic-preflight`
- digest `sha256:c5bf089d064987692fa4b8780252c7e6283531a47b0dc47a71f19b0a8be36dbc`

## 2. Frozen implementation

Script:
`phase2/academic_transform/at0_en/v2_6/fresh_rct_acquisition_tooling.py`

No network client exists in the readiness implementation.
Before acquisition authorization, only `--synthetic-preflight` is accepted.

## 3. Retrieval structural mechanics verified

The synthetic closure verified that:

- the literal frozen PubMed query must match byte-for-byte;
- a mutated query fails;
- parent result count must reconcile to the complete unique PMID set;
- page indices must be contiguous from zero;
- duplicate PMIDs across pages fail;
- missing PMIDs relative to parent count fail;
- raw response hashes are persisted;
- complete PMID-list SHA256 is produced;
- deterministic partition unions must equal the parent count;
- overlapping partitions fail.

Verified states:
- `RETRIEVAL_SNAPSHOT_STRUCTURAL_PASS`
- `PARTITION_RECONCILIATION_PASS`

This validates archive/reconciliation mechanics only.
It does NOT claim the live PubMed frame is feasible or complete.

## 4. Duplicate/provenance triggers verified

Frozen screening thresholds:

- normalized-title Levenshtein similarity >= `0.90`;
- abstract word-5-gram Jaccard >= `0.80`;
- abstract word-5-gram containment >= `0.90`.

Implemented documentary-review triggers:
- exact PMID;
- exact normalized DOI;
- exact normalized title;
- near-title Levenshtein;
- 5-gram Jaccard;
- 5-gram containment;
- shared normalized registry ID.

Registry parser includes:
- NCT;
- ISRCTN;
- ACTRN;
- ChiCTR;
- CTRI;
- IRCT;
- UMIN;
- jRCT;
- DRKS;
- EudraCT/EU-CTR style identifiers.

The synthetic closure verified:
- exact identity triggers;
- near-text triggers;
- shared-registry triggers;
- unrelated fixture does not spuriously trigger;
- identifier normalization is deterministic.

## 5. Important limitation

These are fixed **screening triggers**, not automatic trial-family truth.

The governing protocol still requires:
- two-human documentary review of flagged pairs;
- manual trial-family checks when registry IDs are missing;
- conservative exclusion of unresolved suspected overlap.

Absence of a software trigger does NOT establish independence.

No learned embedding model is authorized for this gate.

## 6. Current readiness effect

The following readiness items advance only to:
`SYNTHETIC_MECHANICS_PASS / REAL_EXECUTION_BLOCKED`

- retrieval archive tooling;
- duplicate/provenance screening-trigger tooling.

Still unresolved:
- complete prior-exposure inventory;
- protected-corpus custody/fingerprints;
- human screeners/annotators;
- senior adjudicator;
- independent custodian;
- funding/resource feasibility;
- access controls;
- live frame feasibility;
- manual trial-family adjudication process staffing;
- final acquisition sign-off.

Therefore:

`ACQUISITION_REMAINS_BLOCKED`
