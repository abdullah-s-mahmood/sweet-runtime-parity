# MP-SEF P2_V2 IMPLEMENTATION SPECIFICATION

Date: 2026-10-01
Status: PRE-IMPLEMENTATION / SOURCE-ONLY DESIGN FREEZE
Parent decision: ACAD_PASS_ARABIC_ARCHITECTURE_REBASELINE_V1
Gold use: FORBIDDEN
Purpose: repair the Seq2Seq++ / GED-morphology proposer in a new versioned lane

## 1. Why P2_V2 exists

Frozen P2 V1 is non-executable because its GED predictions are subword-level while the downstream loop consumes them as if they were word-level labels.

Observed V1 failure:
- population: 1,918
- GED/morphology word-count mismatch: 1,918 / 1,918
- exact count match: 0 / 1,918
- total silently dropped predictions under zip semantics: 30,341
- current P2 executable actions: 0 / 1,918

This is an implementation/provenance defect, not evidence of poor linguistic quality.

P2_V2 is a NEW proposer version.
It MUST NOT overwrite, replace, or mutate frozen P2 V1 evidence.

## 2. Governing upstream implementation

Repository:
`CAMeL-Lab/arabic-gec`

Frozen upstream revision:
`8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`

Authoritative GED alignment implementation:
`gec/mle/error_identifier/__init__.py`

The internal `ErrorIdentifier` implementation is authoritative for word-level GED alignment.

The simplified README inference example MUST NOT be used as the P2_V2 word-alignment implementation because direct special-token stripping does not guarantee one prediction per source word.

## 3. Required GED wordpiece→word alignment

For each morphology-preprocessed source sentence:

1. split the source into words;
2. tokenize each source word independently with the frozen GED tokenizer;
3. assign the real word label position to the FIRST wordpiece only;
4. assign cross-entropy `ignore_index=-100` to all remaining wordpieces;
5. preserve sentence/segment identity;
6. if the sentence exceeds the GED segment limit, segment only at whole-word boundaries;
7. run GED inference;
8. discard predictions only where the paired label position is `ignore_index`;
9. collate segment predictions back to the original sentence order;
10. assert:
   `len(word_level_ged_labels) == len(morph_words)`.

Any mismatch is:
`EXECUTION_FAILED:GED_WORD_ALIGNMENT_MISMATCH`

There is no zip-based truncation fallback.

## 4. GED segmentation requirements

The upstream robust implementation uses:

- maximum GED sequence length: 256;
- special tokens included in the sequence;
- segmentation boundary: whole wordpiece groups belonging to complete words;
- segment outputs collated by sentence id.

P2_V2 must record for every source:

- original morphology word count;
- total GED wordpiece count;
- number of GED segments;
- per-segment word count;
- per-segment wordpiece count;
- first-wordpiece index map;
- ignored wordpiece positions;
- returned word-level GED count;
- exact coverage boolean.

No sentence may be marked executable unless exact word coverage is proven.

## 5. Morphological preprocessing identity

P2_V2 must freeze:

- morphology model/database version;
- preprocessing code hash;
- source text hash;
- morphology-preprocessed text hash;
- morphology word sequence.

Any morphology failure or empty/unknown preprocessing state must be explicit.

No gold/reference may be used to repair morphology.

## 6. Projection of word-level GED labels into GEC tokenizer space

Only after exact word-level GED alignment is proven:

For each morphology word:

1. tokenize the word with the frozen GEC tokenizer;
2. require at least one GEC token or emit an explicit failure;
3. repeat that WORD'S GED label across all GEC subwords for that word;
4. preserve exact word→GEC-subword mapping;
5. add frozen BOS/EOS IDs;
6. add the corresponding fixed GED boundary labels required by the model;
7. assert exact equality between:
   - GEC input-id length;
   - GED-label-id length;
   - attention-mask length.

Any mismatch is an execution failure.
No truncating zip is permitted.

## 7. Input truncation and maximum-length policy

P2_V2 must record independently:

- GED input truncation status;
- GEC input truncation status;
- GEC generation maximum length;
- decoder start token id;
- EOS token id;
- PAD token id;
- generated token ids;
- first natural EOS position;
- whether generation hit the ceiling before a valid natural EOS.

Unknown truncation status is non-executable.

Reaching generation ceiling is non-executable unless a separately preregistered proof establishes a complete output. Default policy is FAIL CLOSED.

No post-discovery max-length increase may be applied inside a frozen proposer version.

## 8. Frozen output requirements

Each P2_V2 proposal record must contain at least:

- uid;
- case_id;
- cluster_id;
- source;
- source_sha256;
- proposer_version;
- upstream_revision;
- morphology_preprocessed_text;
- morphology_sha256;
- morphology_word_count;
- GED tokenizer/model identities;
- GED wordpiece count;
- GED segment metadata;
- first-wordpiece alignment map;
- word_level_ged_labels;
- GED exact coverage status;
- GEC tokenizer/model identities;
- GEC word→subword map;
- GEC input ids hash;
- GED label ids hash;
- decoder/generation trace;
- full_proposer_output;
- output_sha256;
- source_only=true;
- gold_reference_consulted=false;
- quality_scored=false.

## 9. Required negative tests

Before any C_F generation, P2_V2 self-tests must include:

1. one word split into multiple GED wordpieces;
2. multiple words each split into multiple wordpieces;
3. a source long enough to require >1 GED segment;
4. a word producing zero tokens -> explicit failure;
5. one GED label deliberately removed -> failure;
6. one extra GED label injected -> failure;
7. reordered word-level labels -> identity/alignment failure;
8. mismatched source hash -> failure;
9. mismatched morphology hash -> failure;
10. GEC input/GED-label length mismatch -> failure;
11. unknown input truncation -> non-executable;
12. generation reaches max_length -> non-executable;
13. decoder prefix equal to EOS token id -> must not be mistaken for terminal EOS;
14. missing terminal EOS -> non-executable;
15. apply/reproducibility run must produce byte-identical output for the same frozen input/runtime.

## 10. Parity and reproducibility gates

Before generating the full source-only C_F population:

- single-vs-batch parity must be tested;
- deterministic seeds/runtime must be frozen;
- model/tokenizer revisions and weight hashes must be frozen;
- environment lock must be stored;
- synthetic alignment tests must pass.

For the full source-only population:

- every UID must produce exactly one proposal record;
- no dropped UID;
- no duplicated UID;
- all failure states retained in denominator/accounting;
- no reference/gold loaded.

## 11. Success definition for P2_V2 source-only stage

The source-only stage does NOT require linguistic correctness.

It requires:

- exact population identity;
- exact GED word coverage for all executable cases;
- zero silent zip truncation;
- zero unknown truncation among executable cases;
- reproducible generation;
- complete provenance;
- protected/legalizer compatibility.

If failures remain, they must be triaged rather than converted to known-zero quality.

## 12. Comparison against P2 V1

P2_V2 is considered implementation-improved only if:

- the V1 universal GED alignment defect is eliminated;
- no new silent coverage loss is introduced;
- source-only provenance is stronger or equal;
- reproducibility is maintained.

This does NOT claim improved GEC quality.

## 13. Scientific boundary

No P2_V2 correctness, R_joint, precision, recall, F0.5, complete-repair, or safe-repair metric may be computed during implementation/provenance validation.

P2_V2 remains a candidate generator until a separately frozen and independently reviewed evaluation protocol authorizes otherwise.

## 14. Next step

Implement a minimal P2_V2 alignment/provenance prototype on synthetic/source-only examples only.

Do not run it on project gold.

After synthetic PASS, run a small frozen source-only parity packet, then decide whether full C_F source-only generation is justified.
