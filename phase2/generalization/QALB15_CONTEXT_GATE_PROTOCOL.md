# Phase 2 — QALB-2015 L2 Context-Aware Structural Gate

Date: 2026-09-28
Status: PRE-REGISTERED BEFORE READING QALB-2015 L2 DEV GOLD CONTENT

## Purpose

Falsify or support a narrower automatic Arabic proofreading rule after ZAEBUC DEV showed that context-free nun insertion/deletion is unsafe.

This remains Phase 2. No Phase 3 and no final sealed benchmark.

## External corpus

Source: CAMeL-Lab/arabic-gec pinned to commit:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Corpus:
QALB-2015 L2 DEV

Raw runtime input:
data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/dev/QALB-2015-L2-Dev.sent.no_ids

Gold, read only after runtime decisions are materialized:
data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/dev/QALB-2015-L2-Dev.cor.no_ids

License:
internal research/evaluation only; no redistribution.
Therefore no QALB sentence text or corrected text may be committed to this project repository.

QALB-2015 TEST remains unread.

## Population selection

Use a deterministic raw-only 100-line slice:
- strip only outer whitespace;
- compute SHA-256("phase2-qalb15-l2-context-v1|" + raw_line);
- choose the 100 lowest hashes;
- selection happens before gold is read;
- retain only original line IDs and source hashes in persisted evidence.

## Generator

Keep the existing independent generator frozen:
- CAMeL-Lab/camelbert-msa-qalb14-ged-13
- CAMeL-Lab/arabart-qalb14-gec-ged-13
- same pinned CAMeL-Lab Arabic-GEC runtime.

No QALB15 fine-tuning.

## Frozen policy families

### 1. WAW_ALIF_VERB_ONLY

Candidate auto-accept hypothesis:
- exactly one changed token;
- substitution only;
- normalized source ends with Arabic waw "و";
- normalized candidate equals source + final alif "ا";
- edit cost <= 0.25;
- CAMeL contextual morphology for the source whitespace token has POS exactly "verb";
- no word-boundary change.

Intent:
test differentiating-alif restoration after plural verbal waw without conflating noun forms ending in waw.

### 2. ACCUSATIVE_ALIF_SINGLE — comparator only

Do NOT promote automatically in this gate.
Measure:
- exactly one changed token;
- output = source + final alif;
- source does not end in waw;
- cost <= 0.25.

This tests how context-sensitive accusative/tanwin alif remains on a new corpus.

### 3. FINAL_ALIF_GENERIC — comparator only

Same generic final-alif family used previously, without promotion.

### 4. NUN FAMILY

REVIEW ONLY.
No nun insertion/deletion event can be auto-accepted in this gate.

## Runtime order

1. read QALB15 DEV raw only;
2. select deterministic 100-line slice;
3. run frozen QALB14 GED+AraBART generator;
4. align complete events;
5. attach source-token contextual morphology;
6. materialize all policy decisions;
7. write a runtime artifact containing no QALB text;
8. only then read matching corrected lines;
9. compare accepted events to gold;
10. persist aggregate/hash-only evaluation;
11. manually inspect non-exact accepted WAW_ALIF_VERB_ONLY events from upstream only if necessary;
12. do not tune this policy on the same slice.

## Primary success criterion

WAW_ALIF_VERB_ONLY may advance only if:
- at least one accepted event exists;
- no demonstrably wrong accepted event;
- no partial accepted event;
- non-exact accepted events can be adjudicated as valid alternatives without lexical exceptions.

If any accepted event is demonstrably wrong:
MODIFY.

ACCUSATIVE_ALIF_SINGLE and FINAL_ALIF_GENERIC are diagnostic comparators and remain REVIEW-only regardless of their result in this one gate.

## Data handling

Persist:
- upstream commit;
- file Git blob SHAs / SHA-256;
- selected line IDs;
- raw line hashes;
- event hashes;
- policy counts;
- aggregate gold classifications;
- hashes of non-exact cases.

Do NOT persist:
- QALB raw text;
- QALB corrected text;
- reconstructed QALB passages;
- candidate excerpts derived from QALB text.

No QALB TEST.
