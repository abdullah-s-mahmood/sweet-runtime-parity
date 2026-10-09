# ACAD_PASS — Federation Per-Fold Data Manifest Custody Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PER_FOLD_DATA_MANIFEST_CUSTODY_PASS`

Run:
`37897592120`

Artifact:
`11601066403`

Digest:
`sha256:525f7a524d08ee26f17b69cfb36ece6e9a17bd1a4d016ef451f1b7120fb05e42`

Scientific training:
false

Protected/raw identifiers emitted:
none.

## Fold 0

Native:
- train = 172 documents
- eval = 84 documents
- held-out mapped PMIDs = 84
- unresolved held-out documents = 0

Auxiliary decontamination:
- original EBM P/I/O: 4794 source -> 4708 admitted; 86 known family aliases excluded
- EvidenceOutcomes 500RCT: 500 -> 500
- PICO-Corpus 26-type: 1011 -> 1011
- TrialSieve train+validation 20-type: 1371 -> 1371

Manifest SHA256:
`7c79f752c38f30a7b4f220c5ab3ff7db3ec559baa1c80797f13b65833203e0b0`

## Fold 1

Native:
- train = 167
- eval = 89
- held-out mapped PMIDs = 83
- unresolved held-out documents = 6

Auxiliary:
- original EBM P/I/O: 4794 -> 4711; 83 known family aliases excluded
- EvidenceOutcomes: 500 -> 500
- PICO-Corpus: 1011 -> 1011
- TrialSieve train+validation: 1371 -> 1371

Manifest SHA256:
`1955fa751bb90960af10fcdae40fabe3ae36c06602b4aa00ad74aec9c6466e02`

The six unresolved native eval documents are already forced into the conservative unresolved family component by the frozen fold assignment. They are not silently assumed independent.

## Fold 2

Native:
- train = 173
- eval = 83
- held-out mapped PMIDs = 83
- unresolved held-out documents = 0

Auxiliary:
- original EBM P/I/O: 4794 -> 4711; 83 known family aliases excluded
- EvidenceOutcomes: 500 -> 500
- PICO-Corpus: 1011 -> 1011
- TrialSieve train+validation: 1371 -> 1371

Manifest SHA256:
`eb28ffdc603f6e0df7a42e216909aa0540b52772008a843fca31cb0f815cb939`

## Arm use

D0/D1:
native fold train/eval only.

D2/D3/D4:
native fold train/eval plus the decontaminated auxiliary sources above under their frozen native auxiliary heads.

D5:
canceled.

## Interpretation

Known PMID/DOI/registry family aliases are removed from auxiliary training relative to the held-out native development fold.

Remaining limitation:
unknown/unresolved family identity cannot be mathematically excluded; it is preserved as an explicit limitation rather than assumed absent.

This PASS authorizes data-hash binding only.
It does NOT authorize scientific fitting until GPU/runtime closure and final review PASS.
