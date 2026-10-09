# ACAD_PASS — Public Human-Gold Federation Protocol V1

Date: 2026-10-09

State:
`PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_FROZEN_PENDING_PROVENANCE_CLOSURE`

Training authorization:
`NOT_AUTHORIZED`

VERIFY_INTERNAL:
`CLOSED`

Canonical independent review:
`FINAL_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_V1.md`

Verdict:
`PROCEED_FEDERATION_WITH_CHANGES`

This protocol implements the finite first-campaign design accepted by the independent review. It does not itself certify benchmark eligibility or authorize fitting.

## 1. Historical evidence boundary

R44C remains frozen and consumed.

Do NOT modify:
`AT0_EN_V26_R44C_LINEAR5_DEVELOPMENT_RESULT_FREEZE_V1.md`

Previously exposed scientific evidence remains exposed.

A computational reset may discard learned artifacts but cannot restore unseen status to previously inspected or score-driving records.

## 2. Corrected data lineage

R43/R44 native source:
- repository `BIDS-Xu-Lab/section_specific_annotation_of_PICO`
- commit `bc4b878773192f38b2600ec830ca4208b82f7dc0`
- file `data/EBM-NLPmod/fold1/train.txt`
- SHA256 `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`

The R43/R44 320-document lineage belongs to EBM-NLP_mod, NOT PICO-Corpus.

R44:
- DESIGN 256 documents;
- VERIFY_INTERNAL 64 documents;
- VERIFY_INTERNAL remains protected and excluded from every stream.

PICO-Corpus is separately exposed and is TRAIN/DEVELOPMENT only in this campaign.

## 3. Dataset-role matrix

### Native four-class core

#### EBM-NLP_mod
Role:
core native TRAIN/DEVELOPMENT.

Expected development source:
the documented exposed, unprotected portion of fold1 TRAIN after protected aliases and any other forbidden families are removed.

No new independent EBM-NLP_mod benchmark claim.

#### AD
Role:
conditional external benchmark and, in isolated per-fit protocols, authorized training partition when not held out.

No AD test is certified eligible until benchmark custody/provenance closure.

#### COVID-19
Same policy as AD.

### Auxiliary human gold

#### PICO-Corpus
- preserve native BRAT ontology;
- one auxiliary channel per released native entity type;
- no semantic collapse into broad native P/I/C/O;
- TRAIN/DEVELOPMENT only.

#### Original EBM-NLP
- approved training partition only;
- independent P/I/O auxiliary head;
- no automatic separate-C mapping;
- expert test remains reserved/deferred.

#### TrialSieve
- approved training partition only;
- 20 released entity types in a separate auxiliary head;
- NonStudyDrug is NOT automatically C;
- no flat P/I/C/O conversion.

#### EvidenceOutcomes
- auxiliary O head in its native Results/Conclusions scope;
- never infer negative P/I/C or Title/Methods O;
- parent EBM overlap must be resolved.

#### C-TrO
- weight 0 in first campaign;
- reserve for later relation-specific study;
- no flat PICO mapping.

### Weak/silver

#### DISTANT-CTO
- not human gold;
- does not supply direct I/C role labels;
- may appear only in D5 as role-agnostic semantic intervention-type supervision;
- no native main-head I/C relabeling.

#### FinePICO outputs / LLM labels / pseudo-labels
- weight 0;
- no generation in first campaign;
- never final gold.

## 4. Gold-independent preprocessing

New preprocessing MUST NOT use gold to choose chunk/window boundaries.

The historical Hu source:
`utils_ner.py::update_data_to_max_len`
uses O/non-O label state when selecting an insertion point and was called on train/dev/test.

Therefore first-campaign preprocessing is a new text-only implementation.

Historical Hu numbers remain historical.
Any comparator using corrected text-only preprocessing is labeled an adapted reproduction.

### Coordinates

Preserve:
- native document identity;
- original words/characters;
- punctuation;
- source offsets;
- original-to-model offset map.

Do not:
- lowercase stored matching text;
- strip punctuation for exact scoring;
- delete tokenizer-empty records;
- synthesize character offsets from arbitrary reconstructed text.

Tokenizer-empty words receive explicit UNK representation and keep original offsets.

### BiomedBERT windows

Checkpoint:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract@d673b8835373c6fa116d6d8006b33d48734e305d`

At most:
510 content wordpieces/window.

Next candidate start:
256 wordpieces later.

Round starts/ends down to complete word boundaries while requiring:
- forward progress;
- full document coverage;
- zero gold access.

A single source word exceeding the window limit:
`PREFLIGHT_FAIL`

### BioClinical ModernBERT challenger

Checkpoint:
`thomas-sounack/BioClinical-ModernBERT-base@c3648aa87af95837c809e6f0c5f85d08160db437`

At most:
8190 content pieces/window.

Next candidate start:
4096 pieces later.

Same complete-word/full-coverage/gold-independence rules.

### Word representation

For each word:
choose its complete-word occurrence with greatest minimum left/right context.

Tie:
earliest window.

Represent word:
mean of its subword vectors.

Document-level boundary pairs may use endpoint representations originating from different overlapping windows.

## 5. Native architecture

Preferred first-campaign span model:

- one encoder;
- four typed channels: P/I/C/O;
- class-specific 64-dimensional start projection;
- class-specific 64-dimensional end projection;
- GlobalPointer-style relative-position dot-product score `z_c(i,j)`;
- scale by `sqrt(64)`;
- legal `i<=j` pairs only;
- pair must remain within one in-scope contiguous annotated source block;
- dropout 0.1.

No:
- hidden verifier MLP;
- hard start/end proposal gate;
- top-k pruning;
- fixed 12-word maximum;
- NMS;
- forced flattening.

### Invalid/NONE behavior

No separate learned NONE head.

For each class:
fully annotated non-gold pairs are negative supervision.

Unknown/unannotated scope:
masked, never negative.

Inference:
a typed span exists when the corresponding span score exceeds the standard span decision boundary.

Absence of all positive typed spans corresponds to no entity.

## 6. Overlap semantics

Preserve all typed spans above decision threshold.

Same offsets with different types are distinct predictions.

Identical:
`(document,start,end,type)`
deduplicate once.

Wrong extra type:
FP.

No fabricated union boundaries.

Unsupported discontinuous auxiliary structures:
retain provenance/components, mask from contiguous-head loss, and fail adapter closure if materially unsupported.

## 7. Native semantic contract

Source-compatible entity starts follow the frozen B-start contract.

A valid example-initial I-X continuation does NOT become a new gold entity.

Invalid initial I:
flag, do not silently repair.

If both SOURCE_COMPATIBLE and DOCUMENT_CONTINUITY outputs are produced:
they are scored/reported separately.

Primary comparable benchmark mode:
`SOURCE_COMPATIBLE`

## 8. Auxiliary heads

All auxiliary heads use the same bounded span-head form unless their native task requires the explicit weak semantic classifier below.

Heads:
- original EBM-NLP P/I/O = 3 channels;
- TrialSieve = 20 released native types;
- EvidenceOutcomes = native outcome type/scope;
- PICO-Corpus = one channel per released native BRAT entity type, lexicographically frozen in ontology manifest.

Auxiliary heads are discarded at native P/I/C/O inference.

Missing auxiliary annotation does not create native negatives.

## 9. Losses

For fully annotated class c in document d:

`L_c = log(1 + sum_{g in G_c} exp(-z_g)) + log(1 + sum_{n in N_c} exp(z_n))`

Use numerically stable log-sum-exp.

Native loss:
equal average over applicable P/I/C/O classes and documents.

Human-federation:
`L = L_native + 0.25 * L_aux`

Weak D5 only:
`L = L_native + 0.25 * L_aux + 0.05 * L_weak`

No coefficient sweep.

### Weak D5 head

Separate 11-way semantic intervention-type softmax classifier.

Input:
concatenated start/end mention representations.

Classifier:
single linear layer.

Loss:
mean cross-entropy on admitted DISTANT-CTO mentions only.

No main-head I/C role loss.

Unmatched source text:
unknown, not Outside.

Drop weak head at inference.

Weak-label admission:
- exact recoverable source text;
- exact recoverable character span;
- released semantic type;
- recoverable registry provenance;
- no same-coordinate conflicting semantic labels;
- no held-out/protected family aliases.

Exclude:
- fuzzy-only alignment;
- irreversible normalization alignment;
- unresolved provenance.

Sampling cap:
- <=10 weak mentions/trial;
- <=100,000 total;
- ascending SHA256 of
  `ACAD_PASS_FED_V1_WEAK|trial_id|document_id|start|end|type`;
- no replacement.

If released type count does not resolve to 11:
cancel D5 before fitting and do not replace the arm.

## 10. Six finite development arms

Development data:
confirmed exposed, unprotected EBM-NLP_mod native pool + authorized auxiliary training records.

AD/COVID sealed from interactive development.

Development split:
complete trial-family components.

Rank components by:
`SHA256("ACAD_PASS_FED_V1_DEV|" + canonical_family_id)`

Assign sorted positions modulo 3.

No seed search.
No class-balancing swaps.

Each held-out development fold must contain:
- all P/I/C/O classes;
- >=20 native C entities.

Otherwise:
`STOP_FOR_PROTOCOL_REVIEW_BEFORE_FIT`

Seeds:
`44,45,46`

Exactly these arms:

- D0: BiomedBERT + linear 9-way BIO native-only.
- D1: BiomedBERT + four-channel span head native-only.
- D2: BiomedBERT BIO + human auxiliary heads.
- D3: BiomedBERT span + human auxiliary heads.
- D4: BioClinical ModernBERT span + human auxiliary heads.
- D5: D3 + weak semantic-type head.

Total planned development fits:
`6 arms * 3 folds * 3 seeds = 54`

If D5 fails weak-stream closure before any D5 fit:
cancel D5 without replacement;
remaining budget = 45 fits.

No seventh adaptive arm.

## 11. BIO controls

Native labels:
9-way BIO:
O + B/I for P/I/C/O.

Training:
token cross-entropy.

Inference:
fixed BIO-valid Viterbi constraints.

No learned CRF transition parameters.

Standard decision:
maximum valid-sequence probability.

Do not flatten unexpected nested native gold merely to preserve BIO eligibility.

## 12. Training constants

Full encoder fine-tuning.

Optimizer:
AdamW.

Encoder LR:
`2e-5`

Task-head LR:
`1e-4`

Betas:
`(0.9,0.999)`

Epsilon:
`1e-8`

Weight decay:
`0.01`
except bias and normalization parameters.

Gradient clip:
`1.0`

Dropout:
`0.1`

Warmup:
first 10% of total updates, linear.

Decay:
linear to zero.

Updates:
`20 * ceil(N_native_train / 8)`

Native effective batch:
8 canonical documents.

Auxiliary effective batch:
8 canonical documents.

Weak batch:
64 weak mentions.

Final checkpoint only.

No:
- early stopping;
- best-epoch selection;
- error-based oversampling;
- seed selection;
- hyperparameter sweep.

Hardware/mixed precision/gradient accumulation:
must be pinned in runtime manifest before first fit.

## 13. Development selection

All 54 authorized development predictions must be frozen before arm comparison.

Primary development selector:
strict four-class occurrence-level exact micro-F1 pooled across the three held-out development folds and averaged across seeds.

If multiple arms are within absolute 0.005 F1 of maximum:
choose lowest-numbered arm.

Report all arms.

Also report:
- per-class P/R/F1;
- macro F1;
- worst-fold results;
- all TP/FP/FN;
- failure state.

No new criterion after results.

## 14. Optional high-precision mode

This is separate from standard F1 decoding.

Candidate threshold grid:
`{0.80,0.85,0.90,0.95}`

Span-model confidence:
`sigmoid(z)`
descriptive score, not calibrated probability.

BIO span confidence:
minimum assigned-tag softmax across decoded span.

Choose one global threshold from selected-arm DEVELOPMENT OOF outputs.

For every seed and every class require:
- observed precision >=0.90;
- recall >=0.33;
- >=30 accepted mentions/class;
- >=20 distinct trial families/class.

Among passing thresholds:
maximize mean class-macro recall.

Tie:
higher threshold.

If none:
`NO_HIGH_PRECISION_MODE_NOMINATED`

Do not:
- enlarge grid;
- suppress a class;
- fit calibration.

External selective threshold remains unchanged.

## 15. External benchmark candidates

Benchmark eligibility remains CONDITIONAL until provenance closure.

### B1 — AD official released splits 1–5
Training:
authorized target split train + exposed unprotected EBM_mod pool + COVID fold1 train/dev + selected allowed auxiliary streams.

Held-out:
the corresponding AD official test.

Exclude all AD test-family aliases from every training stream.

### B2 — COVID official released splits 1–5
Symmetric policy.

### B3 — leave AD out
Training:
authorized exposed EBM_mod + COVID fold1 train/dev + allowed auxiliary streams with all AD families removed.

Evaluation:
entire original 150-abstract AD corpus, one canonical record/family representation as defined by manifest.

### B4 — leave COVID out
Symmetric policy.

No EBM_mod external score in first campaign.

Original EBM expert test:
reserved/deferred.

TrialSieve/C-TrO/EvidenceOutcomes tests:
reserved/deferred.

## 16. External systems

Freeze before any external metric release:

1. selected D0–D5 procedure;
2. BiomedBERT linear BIO reference on matched authorized native training regime;
3. BiomedBERT linear BIO with the same native/auxiliary/weak streams as selected procedure;
4. PICOX adapted prospectively to native four-class P/I/C/O.

If PICOX exact reproducible recipe cannot be frozen without substantive ambiguity:
stop that comparator before fitting and narrow the claim.

Do not invent a weak comparator.

If two systems are byte/procedure-identical for a cell:
reuse predictions.

## 17. Primary scoring

Primary metric:
strict occurrence-level typed entity micro-F1.

TP requires identical:
- document;
- start;
- end;
- P/I/C/O type.

One-to-one exact matching.

Repeated same strings at different coordinates remain distinct.

Both-empty:
zero TP.

Include:
- all documents;
- all unpredicted gold FNs;
- wrong-type FP/FN;
- wrong-boundary FP/FN.

No relaxed/token/partial/string-set score substitutes for primary metric.

Every expected document must emit exactly one status record, including valid empty output.

Missing/duplicate UID, invalid coordinates, nonfinite scores, or incomplete inference:
fit invalid / fail closed.

## 18. Aggregation

B1/B2:
- micro-F1 per official split;
- arithmetic mean across splits;
- then mean across three seeds;
- pooled TP/FP/FN descriptive only.

B3/B4:
- micro-F1 over unique held-out corpus;
- then mean across seeds.

Cross-corpus transfer summary:
unweighted mean of B3 and B4.

Do not call it a universal leaderboard score.

## 19. Secondary metrics

Report:
- exact class-wise P/R/F1;
- class-macro F1;
- TP/FP/FN;
- goldless-document FP rate;
- boundary-only vs wrong-type decomposition;
- exact-boundary-conditioned I<->C confusion;
- recall including unrecoverable spans;
- per-document/trial yield;
- risk-coverage;
- precision-recall curves;
- span-length/section/corpus strata;
- failure/validity counts;
- model size;
- training/inference cost;
- reproducibility deviations.

Partial/token metrics:
descriptive only.

## 20. Uncertainty

20,000 paired trial-family cluster bootstrap replicates.

Seed:
`4404`

One sampled family brings:
- all its records;
- all fold appearances;
- paired-system outputs.

Average across all three model seeds inside each bootstrap replicate.

Descriptive 95% intervals.

Confirmatory system differences:
12 comparisons across B1–B4 and 3 comparators.

Bonferroni-adjusted two-sided percentile interval level:
`1 - 0.05/12 = 99.583333...%`

If too few independent families or degenerate resamples:
comparison = INCONCLUSIVE.

## 21. Superiority and matching claims

Corpus-specific superiority:
adjusted lower bound of candidate-minus-comparator F1 > 0 against every eligible comparator in that cell.

Suite-wide superiority:
must satisfy this in both B1 and B2.

Cross-corpus robustness:
reported separately using B3/B4.

Noninferiority/matching margin:
`0.01 absolute F1`

"Within one F1 point":
adjusted lower bound > -0.01 against each relevant comparator.

A nonsignificant difference is not equivalence.

If a stronger eligible comparator cannot be reproduced:
broad unrestricted SOTA claim is blocked;
bounded reproduced-comparator claim remains possible.

## 22. Incompatible historical comparisons

Do NOT headline-rank:
- AlpaPICO inspected string-set OUT/INT/PAR scorer;
- FinePICO AD/COVID any-token-overlap transfer metric;
- PICOX published merged-I/C score;
- GPT-4o 342/350 semantic review number

against strict occurrence-level exact four-class ACAD_PASS.

They may be discussed only as task-/metric-qualified literature evidence.

## 23. From-scratch reset

For every new scientific fit:
- start from pinned public pretrained encoder;
- create fresh task heads;
- no initialization from R44/R44B/R44C;
- no R44 candidate-bank predictions;
- no historical fitted normalizer/calibrator;
- no historical learned thresholds;
- no optimizer-state reuse.

Historical:
- code;
- manifests;
- results;
- methodological knowledge;
- exposed authorized training data

remain preserved and may be reused according to this protocol.

## 24. Attempt budget

Development:
54 fits maximum, or 45 if D5 is prospectively canceled for failed weak provenance.

External pipeline ceiling:
144 pipeline fits.

PICOX two-stage accounting:
external model-training-stage ceiling = 180.

Total campaign ceiling:
`234 model-training stages`

Identical fits may be reused, reducing realized total.

No freed/canceled slot can be repurposed to a new hypothesis.

Attempt consumed:
first scientific training job start.

Byte-identical resume from immutable checkpoint with RNG/optimizer state:
continuation.

Restart from initialization or any change to:
- seed;
- data;
- ordering;
- loss;
- batch;
- optimizer;
- model;
is a new attempt and is unauthorized beyond budget.

## 25. Stop rules

STOP BEFORE TRAINING if any remains unresolved:
- lineage;
- protected aliases;
- native schema;
- official split identity;
- gold-independent preprocessing;
- comparator recipe;
- deterministic attempt controls;
- runtime/resource feasibility.

STOP AFTER DEVELOPMENT ARM COMPARISON for protocol review if:
- no executable valid selected candidate;
- no eligible external benchmark.

STOP AFTER EXTERNAL SCORING regardless of success/failure.

No test-guided repair within this campaign.

## 26. Falsification rules

Federation benefit undermined if:
- D2 <= D0 and D3 <= D1 without meaningful positive improvement.

Span architecture novelty undermined if:
- D3 <= D2.

Weak-label utility undermined if:
- D5 <= D3.

Original interpretation weakened if:
- gains vanish after decontamination.

Transfer claim limited if:
- in-domain positive but B3/B4 poor.

High-precision objective fails if:
- no frozen threshold satisfies support/precision/recall contract.

None of these failures authorizes adaptive test chasing.

## 27. Current authorization

Allowed before first fit:
- provenance closure;
- source/file/license/ontology/split hashing;
- protected alias custody;
- gold-independent preprocessing implementation;
- native/auxiliary adapter implementation;
- scoring implementation;
- comparator recipe closure;
- runtime/environment pinning;
- synthetic-only preflight;
- attempt-manifest creation.

Forbidden:
- successor scientific training;
- AD/COVID metric release;
- opening VERIFY_INTERNAL;
- R44/R44B/R44C rerun;
- new local gold generation;
- score-driven benchmark selection.

Next mandatory checkpoint:
`PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_AND_PROVENANCE_CLOSURE_BEFORE_FIRST_FIT`
