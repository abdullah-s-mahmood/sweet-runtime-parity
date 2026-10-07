# ACAD_PASS R4.3 — Gold / Source Semantic Contract Freeze V1

Date: 2026-10-07
Status: PROSPECTIVE CONTRACT FOR NEXT TRAIN-ONLY PHASE; NO NEW TRAINING AUTHORIZED.

## Evidence identity

Pinned source:
- `BIDS-Xu-Lab/section_specific_annotation_of_PICO@bc4b878773192f38b2600ec830ca4208b82f7dc0`
- `data/EBM-NLPmod/fold1/train.txt`
- TRAIN SHA256 `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`.

Valid audits:
1. Corrected source pipeline semantics V2: run `37570964586`, SUCCESS, artifact `11461020272`, digest `sha256:0e68754de553ff71b827d95a96c493df3aec4ba649dc7cff261250905dd1c75f`.
2. Source maxlen preprocessing audit: run `37571146392`, SUCCESS, artifact `11460558757`, digest `sha256:c8b0c54ed362ecd6c4774c6375c99e8db24fbefa636ba229ad2b97ee262239b9`.

Invalid/superseded audit:
- run `37570558785` used source `load_bio()` in a way that retained newline characters in entity keys and yielded zero P/I/C/O counts. It is a TOOLING ERROR and must never be cited as scientific evidence.

## Source pipeline facts

### update_data_to_max_len(256)
Using the exact pinned PubMedBERT tokenizer:
- effective wordpiece threshold = 252 (source subtracts 4);
- tokenizer-empty rows removed = 17;
- additional blank/split boundaries inserted = **0**;
- entity B-start counts unchanged by preprocessing.

Thus our current removal of the 17 empty-surface rows is compatible with the source's actual preprocessing path.

### Entity inventory under source exact-evaluation semantics
Source loader and external evaluator both produce:
- P = 426
- I = 1326
- C = 181
- O = 1067
- total = **3000** entities.

Current ACAD_PASS parser produces:
- P = 434
- I = 1328
- C = 181
- O = 1068
- total = **3011**.

Exact difference:
- P +8
- I +2
- O +1
- C +0
- total +11.

The 11 differences are exactly valid example-initial `I-X` fragments whose preceding example ends in the same entity type.

## Diagnosis

The previous ACAD_PASS convention treated each valid example-initial `I-X` continuation as a **new local entity**.

This is not defensible as a canonical entity inventory:
- it double-counts one annotation chain as two entities;
- it disagrees with the source exact evaluator, which starts entities only on `B-X`;
- the raw contexts show continuation fragments that plausibly continue the prior P/I/O description rather than denote independent entities.

The correct interpretation is **continuation fragment**, not new entity.

## Frozen semantic contract for future work

### 1. Raw preprocessing
- remove the same tokenizer-empty rows as source preprocessing;
- preserve document boundaries from `-DOCSTART-`;
- preserve ordinary blank-delimited example boundaries;
- do not insert max-length splits for the current pinned TRAIN because the source audit proved none are necessary at 256.

### 2. Gold entity starts
- only a raw `B-X` starts a new P/I/C/O entity for source-compatible entity counting.
- an example-initial `I-X` with previous example ending `B-X` or `I-X` is tagged `CONTINUATION_OF_PREVIOUS_X`, not a new entity.
- an initial `I-X` without valid same-type predecessor is `INVALID_INITIAL_I`; never silently normalize it to a new entity.

### 3. Two explicit representations

**SOURCE_COMPATIBLE**
- exact entity inventory follows original external evaluator B-start semantics;
- total TRAIN inventory = 3000;
- used whenever comparing against source-paper exact entity metrics.

**DOCUMENT_CONTINUITY**
- retain the continuation fragment and link it to its parent entity in the previous example within the same DOCSTART document;
- one logical entity ID spans the fragment chain;
- do NOT increase entity count because of continuation fragments;
- preserve fragment coordinates for model/chunk provenance.

No future report may mix SOURCE_COMPATIBLE counts with DOCUMENT_CONTINUITY spans without labeling the metric.

### 4. Model chunking / decoding
- chunk boundaries must not create new entities merely because the first predicted tag is `I-X`;
- use explicit continuation metadata or source-aware carry state where document context is available;
- when carry state is unavailable, abstain/flag the fragment rather than manufacture a new entity;
- synthetic unit tests must cover valid continuation, invalid O->I, type-switch I, empty-token removal, and entity ending exactly at a chunk boundary.

### 5. Evaluation
Primary ACAD_PASS scientific gate remains exact span + exact class, but the evaluator must additionally emit:
- semantic mode (`SOURCE_COMPATIBLE` or `DOCUMENT_CONTINUITY`);
- entity count by P/I/C/O;
- number of continuation fragments;
- number of invalid initial-I events;
- duplicate predicted coordinates;
- source-to-output offset provenance.

Legacy R4.3 results remain frozen under their old local-continuation convention and are not retroactively rewritten.

## Decision

`ACCEPT_SOURCE_PARITY_FINDING_AND_RETIRE_LOCAL_CONTINUATION_AS_INDEPENDENT_ENTITY_FOR_FUTURE_PHASES`.

NEXT:
design all future cross-fitted OOF candidate / contextual-feature data under this semantic contract, then adversarially review the complete protocol before training.
