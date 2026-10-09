# ACAD_PASS — EBM-NLP_mod to Original PMID Mapping Custody Freeze V1

Date: 2026-10-09

State:
`FEDERATION_EBM_MOD_TO_ORIGINAL_PMID_MAPPING_PARTIAL_PASS`

Run:
`37881123349`

Artifact:
`11594720967`

Digest:
`sha256:08acea95fd9358587901a18a538688c6a4f6ab4a6a7a13d4ddd20465638e4c81`

No PMIDs, protected text or gold labels were emitted.

## Mapping sources

Derived corpus:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO@bc4b878773192f38b2600ec830ca4208b82f7dc0`

Derived file:
`data/EBM-NLPmod/fold1/train.txt`

Original corpus:
`bepnye/EBM-NLP@43a4a1ea3f0a21cfb8820c040b843dfaf66192d0`

Original archive:
`ebm_nlp_2_00.tar.gz`

Original EBM numeric PMID documents found:
`4961`

## Conservative mapping rule

Text-only lexical exact evidence:
- 7-token n-grams;
- unique best candidate required;
- >=12 shared 7-grams;
- best-minus-second >=6;
- best/shared coverage >=0.12.

Unmatched or ambiguous records are NOT mapped and remain unresolved.

## Results

All EBM-NLP_mod fold1 TRAIN:
- documents: 400
- accepted PMID mappings: 359
- accepted fraction: **89.75%**
- unresolved: 41
- duplicate accepted PMID assignments: 0

DESIGN:
- documents: 256
- accepted mappings: 250
- accepted fraction: **97.65625%**
- unresolved: 6
- duplicate accepted PMID assignments: 0

VERIFY_INTERNAL:
- documents: 64
- accepted mappings: 49
- accepted fraction: **76.5625%**
- unresolved: 15
- duplicate accepted PMID assignments: 0

OLD_SELECT:
- documents: 80
- accepted mappings: 60
- accepted fraction: **75.0%**
- unresolved: 20
- duplicate accepted PMID assignments: 0

Important:
the R44 partitions are not disjoint partitions of all 400 in a simple 256+64+80 sense for mapping accounting purposes; OLD_SELECT is the historically excluded 80-record set and DESIGN/VERIFY are the 320 FIT partition. Mapping results are reported per frozen role exactly as the R44 manifest defines them.

## Interpretation

This materially strengthens provenance identity for exposed/protected EBM-derived records.

It does NOT:
- resolve the remaining 41 EBM-NLP_mod records;
- map AD/COVID to PMID;
- prove trial-family independence;
- authorize opening VERIFY_INTERNAL;
- authorize scientific training.

Unresolved protected records must remain conservatively protected and may not be treated as non-overlapping by assumption.

Next:
isolated public-target PMID resolution and aggregate-only overlap/family audit.
