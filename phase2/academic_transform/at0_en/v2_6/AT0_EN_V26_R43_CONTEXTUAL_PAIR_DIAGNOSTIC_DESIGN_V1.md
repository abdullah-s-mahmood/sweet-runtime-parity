# AT0 EN V2.6 — R4.3 Contextual Typed Pair Diagnostic Design V1

Date: 2026-10-07
Status: DESIGN FROZEN FOR PREFLIGHT ONLY
Branch: `at0-en-v2.6-dev`

## 1. Decision basis

An independent higher-model architecture review rejected immediate commitment to a single R4.3 architecture and selected:

`RUN_ONE_MORE_TRAIN_ONLY_DIAGNOSTIC_BEFORE_ARCHITECTURE_SELECTION`

The exact next operation is a bounded comparison using ORIGINAL TRAIN ONLY:

- H0 = contextual typed MLP verifier
- H1 = the same verifier plus class-specific biaffine start/end interaction

No model training is authorized by this design document. The current checkpoint is design + data/mechanics preflight only.

### Critical correction to prior interpretation

The R4.2C diagnostic field `joint_invalid_fp` must NOT be interpreted as 48 literal cross-entity start/end pairings at t=0.90.

At t=0.90:
- accepted FP = 56
- different-class exact-boundary FP = 8
- the remaining 48 fail exact-boundary matching despite individually passing the frozen endpoint support threshold
- only 3 literal gold-boundary cross-pairs were observed across all 404 candidates

Therefore the evidence supports at least three competing hypotheses:

1. missing contextual information in cropped-span classifiers;
2. negative-distribution mismatch;
3. a need for explicit start/end interaction.

H0 versus H1 is designed specifically to distinguish hypothesis 3 from 1/2 while holding context, data, negatives and training fixed.

## 2. Protected-data boundary

This diagnostic may read ONLY the exact pinned fold-1 TRAIN file:

`data/EBM-NLPmod/fold1/train.txt`

Expected SHA256:
`6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`

It MUST NOT read:
- the historical fold-1 DEV file;
- fold-1 TEST;
- any other fold's train/dev/test file;
- EBM/COVID/AD protected external tests;
- FactPICO;
- the consumed 60-RCT holdout;
- the previously opened 30-RCT diagnostic.

The historical DEV is now treated as exposed development/regression evidence, not an independent architecture-selection set.

## 3. Source-aligned normalization

Preserve the already validated empty-surface normalization used by R4.2C/R4.2D.

Expected removed literal-empty TRAIN rows:
- O = 5
- I-I = 5
- I-P = 6
- I-O = 1
- total = 17

Do not change labels or repair annotations.

## 4. Document recovery and duplicate grouping

The source CoNLL TRAIN file contains `-DOCSTART-` markers.

A document is one complete block between consecutive `-DOCSTART-` markers.

Sentence boundaries remain blank-line boundaries inside a document.

Create for every document:
- sequential source document index;
- canonical normalized token-only SHA256 including sentence-boundary separators;
- canonical token+tag SHA256;
- per-class exact gold span counts P/I/C/O;
- sentence count;
- token count.

Exact duplicate-document groups are defined by the normalized TOKEN-ONLY SHA256, not by labels.

All members of one duplicate group MUST remain in the same partition.

Also report any duplicate-token documents whose tag sequences differ. Such a conflict is a preflight warning and must be frozen before any fitting.

No PMID is invented if it is absent from the pinned CoNLL source.

## 5. Frozen TRAIN-internal FIT/SELECT split

Purpose:
replace repeated use of the exposed historical DEV for architecture selection.

Target:
approximately 80% FIT / 20% SELECT at the DOCUMENT-GROUP level.

Seed:
`42`

### Deterministic grouped stratification

For each duplicate group define the vector:

`[document_count, P_count, I_count, C_count, O_count]`.

Target SELECT vector is 20% of the full TRAIN totals.

Use one deterministic greedy grouped assignment:

1. Start SELECT empty.
2. For each unselected group, compute the objective that would result from adding it:

`E = ((docs-target_docs)/max(1,target_docs))^2
   + sum_c ((class_c-target_c)/max(1,target_c))^2`

3. At each step add the group producing the LOWEST objective.
4. Ties are broken by SHA256 of:
   `seed|group_token_sha256`, ascending.
5. Stop after SELECT document count first reaches or exceeds `round(0.20 * total_documents)`.
6. FIT is the complement.
7. No redraw, swap, or optimization is allowed after the manifest is frozen.

The preflight must report deviation from the 20% class targets.

Preflight fails if:
- FIT or SELECT lacks any P/I/C/O class;
- SELECT contains fewer than 20 gold spans for any class;
- a duplicate group crosses FIT/SELECT;
- any document crosses FIT/SELECT.

Once created, the exact membership manifest is immutable for this diagnostic.

## 6. Flat-representation audit

The current source representation is assumed to be flat and single-label.

Preflight MUST verify:
- no identical coordinates within one sentence have conflicting P/I/C/O labels;
- no malformed BIO continuation is silently converted into a different label;
- every gold span width is 1–64 words;
- exact coordinate scoring is well defined.

If the representation contains incompatible multilabel coordinates, STOP before fitting.

## 7. TRAIN-only example construction

Labels for the pair head:
`NONE / P / I / C / O`

### 7.1 Positives

Every exact FIT gold span becomes one positive pair with its true P/I/C/O label.

### 7.2 Local hard negatives

For each FIT gold span `[s,e)`, enumerate candidate perturbations:

- start delta in `{-2,-1,0,1,2}`;
- end delta in `{-2,-1,0,1,2}`;
- exclude `(0,0)`;
- require sentence bounds;
- require `end > start`;
- require width <=64;
- exclude every exact gold boundary in that sentence.

Sort eligible candidates by SHA256 of:

`seed|doc|sentence|gold_type|s|e|cand_s|cand_e|LOCAL`

and retain at most TWO.

Each retained perturbation receives `NONE`.

### 7.3 Composite negatives

For each FIT gold span, create a pool using its boundary with boundaries from other gold entities in the SAME sentence:

- `[this_start, other_end)`;
- `[other_start, this_end)`.

Eligibility:
- valid coordinates;
- width <=64;
- not an exact gold boundary.

For each source gold span, retain at most ONE composite.

To ensure both relation families are represented without adaptive balancing:
- if SHA256 of the source-gold key has an even low bit, prefer SAME-class counterpart composites;
- otherwise prefer DIFFERENT-class counterpart composites;
- if the preferred pool is empty, fall back to the other pool.

Within the chosen pool, select the lowest deterministic SHA256 key.

Label:
`NONE`

Preflight must separately report SAME-class and DIFFERENT-class composite counts.

### 7.4 Native FIT-model mistake negative

This source is defined prospectively but cannot be materialized in a no-training preflight.

After the future FIT-only R4.2B replica is trained and frozen, generate native BIO proposals on FIT.

Every proposal that is NOT an exact gold span+class is eligible as `NONE`, except:
- if its coordinates exactly match another gold class, retain that exact gold class instead of NONE.

For each gold source example, add at most ONE native erroneous proposal selected deterministically from the same sentence, prioritizing:
1. overlap with the source gold;
2. otherwise any erroneous proposal in the same sentence.

Tie-break by frozen SHA256 ordering.

If no native error exists, use the background fallback below.

### 7.5 Length-matched background fallback

For a gold span of width `w`, enumerate same-sentence spans of width `w` that:
- are not exact gold boundaries;
- do not overlap any gold entity;
- width <=64.

Choose one by frozen SHA256 ordering only when the native-error slot cannot be filled.

Label:
`NONE`

### 7.6 Deduplication and precedence

Training coordinates are unique by:
`(document, sentence, start, end)`.

Precedence:
1. exact gold P/I/C/O;
2. otherwise NONE.

A coordinate can never simultaneously remain NONE and an entity class.

Every NONE example records provenance:
- LOCAL
- COMPOSITE_SAME
- COMPOSITE_DIFFERENT
- NATIVE_FIT_ERROR
- BACKGROUND_FALLBACK

H0 and H1 MUST receive the exact same frozen example manifest.

## 8. Input-label collision audit

Because R4.2D used cropped content only and failed, preflight must explicitly audit representation ambiguity.

Report on complete TRAIN and separately FIT:
- identical cropped token strings occurring with multiple gold entity classes;
- identical cropped token strings occurring as both gold entity and synthetic NONE;
- identical tokenizer input-ID sequences occurring with conflicting labels;
- counts and top conflict patterns.

These conflicts do NOT automatically invalidate the contextual heads, because H0/H1 use full-sentence contextual representations.

They do invalidate any claim that cropped span content alone provides a separable validity signal.

## 9. Complete model ancestry isolation

Existing globally-trained R4.2B/C artifacts remain immutable REFERENCES ONLY.

They MUST NOT generate features or proposals for SELECT in this diagnostic.

When later training is separately authorized, initialize all task-adapted ancestors from the verified safe base using FIT only.

Base:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract`

Revision:
`d673b8835373c6fa116d6d8006b33d48734e305d`

Expected safe converted-base safetensors SHA256:
`3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`

### FIT-only ancestor B — BIO candidate generator

Fixed training:
- seed 42
- learning rate 5e-5
- weight decay 0.0
- batch 8
- 10 epochs
- linear scheduler
- zero warmup
- final epoch checkpoint
- NO SELECT or historical DEV epoch selection

### FIT-only ancestor C-boundary

Fixed training:
- five labels OUT/START/END/BOTH/IN
- seed 42
- learning rate 5e-5
- weight decay 0.01
- batch 8
- 3 epochs
- linear scheduler
- zero warmup
- final epoch checkpoint
- NO SELECT or historical DEV epoch selection

Frozen boundary feasibility threshold remains:
`0.25`

### FIT-only ancestor C-type

Fixed training:
- exact FIT gold spans only
- classes P/I/C/O
- same established independent-sigmoid formulation
- seed 42
- learning rate 2e-5
- weight decay 0.01
- batch 16
- 3 epochs
- linear scheduler
- zero warmup
- final epoch checkpoint
- NO SELECT or historical DEV epoch selection

Freeze all ancestor hashes BEFORE fitting H0/H1.

## 10. Shared contextual representation

The contextual encoder for H0/H1 is the FINAL FIT-only C-boundary model encoder.

It is FROZEN while H0/H1 train.

Input:
complete normalized sentence.

Coordinates:
`[s,e)`; end word representation is at `e-1`.

Use first-wordpiece contextual vectors for words.

For every candidate pair collect:
- start word vector;
- end word vector;
- mean contextual vector across words `s:e`;
- immediately previous word vector;
- immediately following word vector;
- learned sentence-edge vector when previous/following word does not exist;
- learned 16-dimensional width embedding for clipped width 1–64.

Use separate learned linear projections:
`768 -> 128`
for start, end, interior-mean, previous, following vectors.

Concatenated contextual feature size:
`5*128 + 16 = 656`.

## 11. H0 — contextual typed MLP

Input:
the shared 656-dimensional feature vector.

Head:
- Linear 656 -> 128
- GELU
- Dropout 0.1
- Linear 128 -> 5 logits

Classes:
`NONE/P/I/C/O`

Loss:
multiclass cross-entropy.

No focal loss.
No label smoothing.
No auxiliary loss.
No class weighting.

## 12. H1 — contextual typed MLP + biaffine interaction

Use the IDENTICAL H0 feature path and logits.

Additionally use the projected start and end vectors.

Append scalar bias 1 to each:
- start_aug dimension 129
- end_aug dimension 129

For each class `k in NONE/P/I/C/O`, learn:

`b_k = start_aug^T U_k end_aug`

where:
`U_k in R^(129x129)`.

Final H1 logits:
`H0_logits + biaffine_logits`.

Additional biaffine parameters:
`5 * 129 * 129 = 83,205`.

No triaffine term is permitted in this comparison.

## 13. H0/H1 fixed training protocol

Identical for both:
- seed = 42
- optimizer = AdamW
- learning rate = 0.001
- weight decay = 0.01
- batch = 64 pairs
- epochs = 10 fixed
- final epoch checkpoint only
- linear LR decay
- warmup = 0
- gradient clip = 1.0
- dropout = 0.1
- encoder frozen
- no seed sweep
- no encoder unfreezing
- no hyperparameter search

Cached contextual features and the exact same ordered example manifest MUST be used for both heads.

## 14. SELECT evaluation population

Scientific comparison uses NATIVE SELECT BIO proposals generated only by the FIT-only B model.

Synthetic negatives are training examples, not the scientific evaluation population.

All SELECT gold entities remain in recall denominators, including gold spans absent from the candidate proposals.

Report candidate ceiling before applying verifier filters:
- exact candidate TP availability per class;
- maximum possible candidate recall per class;
- candidate count and FP count.

If candidate ceiling makes any frozen recall/support gate mathematically impossible, STOP and reopen candidate-repair architecture design rather than blaming H0/H1.

## 15. Frozen inference rule

For threshold `t in {0.80,0.85,0.90,0.95}`, a SELECT BIO proposal is automatically accepted only if ALL hold:

1. FIT-only B proposal confidence >= t.
2. FIT-only boundary start support >= 0.25.
3. FIT-only boundary end support >= 0.25.
4. width <=64.
5. FIT-only C-type probability for the proposal class >= t.
6. no other C-type class probability >= t.
7. pair-head top class equals the proposal class.
8. pair-head softmax probability for that class >= t.

Otherwise:
`REVIEW`.

No pair-head-specific threshold exists.

## 16. Unchanged scientific gate

Exact span + exact class only.

For every P/I/C/O:
- precision >=0.90
- recall >=0.20
- accepted >=10

And:
- macro precision >=0.90

For each H0/H1 choose the LOWEST existing-grid threshold satisfying all gates.

If neither passes:
`DIAGNOSTIC_NO_ARCHITECTURE_READY`

If one passes:
nominate it.

If both pass:
prefer H0 unless H1 increases macro recall by >=2.00 percentage points while preserving EVERY gate.

No silent refit on SELECT.

## 17. Additional diagnostic comparison

In addition to the unchanged gate, report FP rejection at a prespecified matched-retention diagnostic point:

Target TP retention:
`>=80% of the unfiltered C-style accepted TP roster`.

For H0 and H1, identify the strictest existing-grid threshold that still retains >=80% TP.

Report:
- TP retention
- FP rejection
- per-class retention/rejection
- not as a replacement gate

Also report document-cluster bootstrap uncertainty using SELECT documents:
- 2000 bootstrap replicates
- seed 42
- resample documents with replacement
- metrics are descriptive only and do not alter selection.

## 18. Required preflight outputs before any training authorization

The no-training preflight must freeze:

1. exact source TRAIN hash;
2. recovered document count;
3. sentence/token counts;
4. exact duplicate groups;
5. token-identical/tag-conflicting documents;
6. FIT/SELECT membership manifest and SHA256;
7. FIT/SELECT document/sentence/token counts;
8. FIT/SELECT P/I/C/O gold counts and target deviations;
9. flat-representation collision audit;
10. max gold span width;
11. synthetic local-negative count;
12. composite SAME/DIFFERENT counts;
13. background-fallback availability count;
14. synthetic coordinate collision count;
15. cropped-token and tokenizer-ID conflicting-label audits;
16. estimated H0/H1 parameter counts;
17. access guard proving no DEV/test/other-fold file was read;
18. deterministic preflight artifact hashes.

Preflight MUST NOT train B, boundary, type, H0 or H1.

## 19. Stop boundary

After preflight:
STOP.

No training run is authorized by this document.

A later explicit checkpoint must review the frozen preflight evidence and decide whether to authorize exactly one FIT/SELECT contextual pair diagnostic.

Protected external tests remain closed.
