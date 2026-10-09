# ACAD_PASS — Federation Adapter Contract V1

Date: 2026-10-09

State:
`FEDERATION_ADAPTER_CONTRACT_FROZEN_SUPERSEDING_TRIALSIEVE_TEST_EXCLUSION`

No scientific fit is authorized by this contract.

## Common interchange record

Every admitted span record must retain:

- `source_corpus`
- `source_revision`
- `source_document_id`
- `canonical_family_id` or explicit unresolved-family status
- `source_scope`
- `text_sha256`
- original text/word offsets
- `start`
- `end`
- `native_label`
- `task_head`
- `gold_strength = NATIVE_HUMAN | AUXILIARY_HUMAN | WEAK`
- adapter version
- exclusion/provenance flags.

Adapters never overwrite native source labels.

## A1 — Native EBM-NLP_mod / AD / COVID PICO adapter

Input:
source token column + P/I/C/O BIO labels.

Output:
native four-channel P/I/C/O spans.

Entity start:
raw `B-X` only.

A valid source/example-initial `I-X` continuation with a known same-type predecessor is continuation metadata, not a new source-compatible entity.

Invalid standalone I:
flag `INVALID_INITIAL_I`;
do not silently repair.

Primary source-compatible gold:
B-start spans only.

No type mapping occurs.

## A2 — Original EBM-NLP auxiliary adapter

Input:
`annotations/aggregated/starting_spans/{participants,interventions,outcomes}/train`

Only training annotations are admitted.

Output heads:
- EBM_P
- EBM_I
- EBM_O

The intervention hierarchical subtype `Control` is NOT converted to native C.

Original EBM medical-professional test labels are excluded from first-campaign training.

## A3 — TrialSieve auxiliary adapter

Canonical source:
`data/processed_for_modeling.json`
SHA256
`376854be993257dacde3abc5c3d53a1d08462b5d954fcbbc568d17905b5d9de5`

Expected:
- exactly 1,609 documents;
- exactly 52,638 spans;
- exactly 20 native tags;
- no zero-span docs.

The frozen stored split is respected.

Admitted first-campaign auxiliary pool:
- train = 1,148;
- validation = 223;
- total admitted = 1,371.

Reserved/not admitted to first-campaign training:
- test = 238.

The canonical 1,609-document file is still audited in full for schema identity, but TrialSieve test records MUST NOT enter training, representation learning, threshold selection or model selection.

For each span:
- preserve source start/end;
- preserve exact one of 20 native tags;
- assign auxiliary head `TRIALSIEVE_20`.

Never map:
- Non-Study Drug -> C;
- Group Name -> P/C;
- Outcome -> native O;
- Drug Intervention -> native I.

Those labels supervise representation only through the separate auxiliary head.

## A4 — EvidenceOutcomes adapter

Admitted file:
`500RCT-CoNLL.tsv`
only.

Expected:
- exactly 500 PMIDs;
- labels exactly `B-Outcome,I-Outcome,O`;
- zero malformed rows.

Task head:
`EVIDENCE_OUTCOME`.

Span type:
native source Outcome auxiliary type only.

Scope:
source Results/Conclusions construct.

It does NOT:
- create native Title/Methods O;
- create negative native P/I/C;
- change native PICO gold.

`140EBMNLP-CoNLL.tsv` is reserved/not used in first-campaign training.

## A5 — PICO-Corpus auxiliary adapter

Expected:
- 1,011 PMID text/ann pairs;
- 17,739 BRAT text-bound spans;
- 26 frozen native types.

Task head:
`PICO_CORPUS_26`.

Every source type remains its own channel.

No:
- control -> native C;
- intervention -> native I;
- outcome -> native O;
- participant-like types -> native P
mapping in the first campaign.

BRAT discontinuous/multi-segment text-bound records, if present in any future revision:
retain native components;
mask from contiguous span loss unless a separately frozen adapter supports them.

## A6 — DISTANT-CTO weak adapter

D5 only.

Expected semantic subtype inventory:
11 classes:
- drug
- other
- device
- behavioral
- procedure
- biological
- dietary supplement
- diagnostic test
- radiation
- genetic
- combination product

Admission requires exact source text/character span, semantic subtype, recoverable trial provenance and no held-out/protected family alias.

Gold strength:
`WEAK`.

No native P/I/C/O labels emitted.

## Cross-source decontamination

Before an adapter record is admitted to a particular fit:

1. resolve exact PMID/DOI/registry/title/text aliases where available;
2. collapse/identify trial-family component;
3. if its family intersects the fit's held-out external benchmark, exclude it;
4. if family identity is unresolved and source is known to derive from the held-out corpus, exclude conservatively;
5. protected VERIFY_INTERNAL aliases are checked inside custody;
6. exclusion occurs before model/tokenizer training artifacts are created.

## Fail-closed conditions

Adapter closure fails if:
- source revision/hash differs;
- expected label inventory changes;
- malformed coordinates exist;
- duplicate source span identities exist without source-defined justification;
- text/offset reconstruction fails;
- an adapter emits native P/I/C/O from a source not authorized as native four-class gold;
- held-out family exclusion cannot be enforced.

No automatic fallback mapping is allowed.
