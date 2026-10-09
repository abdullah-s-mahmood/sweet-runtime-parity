# ACAD_PASS — independent public human-gold federation review

**VERDICT: `PROCEED_FEDERATION_WITH_CHANGES`**

Finalized: 2026-10-09 (Asia/Baghdad); evidence gathered 2026-10-08/09. Repository: `abdullah-s-mahmood/sweet-runtime-parity`; branch: `at0-en-v2.6-dev`; reviewed snapshot: `5f584c5a21a0639bf9d5929166e2eaf69ce6d521`.

Existing public human annotations can replace unavailable local annotation for development and appropriately scoped public-benchmark research. They do not guarantee superiority, erase exposure, establish clinical validity, or eliminate the need to audit annotation constructs. A new local annotation campaign is not a prerequisite to publication.

This is a proposed scientific protocol, conditional on the explicit pre-fit closure requirements below. It is **not an execution authorization or a claim that manifests/adapters/comparators have passed**. This consultation trained no model, opened no VERIFY_INTERNAL rows, collected no new RCTs, generated no gold, changed no GitHub files, and reran no historical experiment. Local evidence and review files were saved. R44C remains consumed with its original scientific-failure verdict.

## 1. Mandatory changes before the first successor fit

**F01 — Repair the exposure lineage.** The new inventory puts R4.3/R44's 320-document lineage under PICO-Corpus while calling EBM-NLP_mod unresolved. The pinned R43 semantic contract explicitly identifies `BIDS-Xu-Lab/section_specific_annotation_of_PICO@bc4b878773192f38b2600ec830ca4208b82f7dc0`, `data/EBM-NLPmod/fold1/train.txt`, SHA256 `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`. That file has 400 documents; the later FIT 320 becomes DESIGN 256 plus VERIFY_INTERNAL 64. Correct the source attribution, materialize known exposed/protected identifiers through custody, and propagate aliases into original EBM-NLP and derived corpora. Do not treat a public copy of a protected record as permission to read or train on it. These documentary facts are in the [R43 contract](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/blob/5f584c5a21a0639bf9d5929166e2eaf69ce6d521/phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_GOLD_SOURCE_SEMANTIC_CONTRACT_FREEZE_V1.md) and [R44 preflight](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/blob/5f584c5a21a0639bf9d5929166e2eaf69ce6d521/phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R44_PREFLIGHT_FREEZE_V1.md).

**F02 — Replace the asserted weak I/C role supervision.** DISTANT-CTO explicitly merges intervention and comparator roles into one intervention entity category, subsequently distinguished by semantic intervention types. It is not a source of separate experimental-versus-control role gold. Replace “directly targets I/C distinction” with “may improve treatment representation; benefit to I/C roles is unproven.” TrialSieve NonStudyDrug and C-TrO arm membership also must not be mechanically relabeled C. [DISTANT-CTO, Section 4.3](https://aclanthology.org/2022.bionlp-1.34/).

**F03 — Freeze source-compatible scoring and text-only preprocessing.** The Hu source `utils_ner.py::update_data_to_max_len` consults O/non-O gold tags when choosing new chunk boundaries; `PICO_ner.py` applies it to train/dev/test. The historical R43 audit established zero inserted boundaries on its training file; it does not establish zero effect on other files. New chunking must never consult gold. Preserve the historical B-start/continuation contract and emit source-compatible and document-continuity results separately if both are produced. No silent initial-I repair, dropped empty-token rows, or changed recall denominator. A comparator with changed preprocessing is an adapted reproduction, not a literal historical replication. [Pinned preprocessing](https://github.com/BIDS-Xu-Lab/section_specific_annotation_of_PICO/blob/bc4b878773192f38b2600ec830ca4208b82f7dc0/utils_ner.py), [caller](https://github.com/BIDS-Xu-Lab/section_specific_annotation_of_PICO/blob/bc4b878773192f38b2600ec830ca4208b82f7dc0/PICO_ner.py).

**F04 — Qualify benchmark eligibility before fitting.** AD and COVID are candidates, not certified untouched tests. Freeze the actual official split membership, trial-family overlap report, prior-exposure report, annotation/scorer versions, and per-fit training exclusions. Do not assume the five released splits have disjoint test sets simply because the paper calls the procedure five-fold cross-validation. Never repair contamination by deleting official test cases and retaining the original benchmark name.

**F05 — Remove incompatible headline comparisons.** AlpaPICO's inspected `metric.py::calculate_metrics` uses sets of mention strings and awards a true positive for both-empty lists; `prediction.py` evaluates OUT/INT/PAR. That code path is not occurrence-offset exact four-class scoring. This does not establish that every paper table used that path. FinePICO's AD/COVID transfer evaluation uses any-token overlap. PICOX merges I/C. These results cannot be ranked directly against ACAD_PASS exact P/I/C/O. [AlpaPICO scorer](https://github.com/shrimonmuke0202/AlpaPICO/blob/54904417d9d9ab436eb8525f2112b6ea13fa385d/metric.py), [FinePICO evaluation](https://arxiv.org/html/2412.19346v1), [PICOX](https://pmc.ncbi.nlm.nih.gov/articles/PMC11031223/).

**F06 — Replace the eleven-component proposal with the finite study below.** No new large verifier, relation stack, LLM teacher, generative ensemble, or iterative pseudo-labeling in this first campaign. A benefit from each additional mechanism must be demonstrated before a later protocol can authorize it.

Repository documents requiring future changes: `AT0_EN_V26_FRESH_RCT_PRIOR_EXPOSURE_INVENTORY_V1.md`; `AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_PACKET_V1.md`; `AT0_EN_V26_DATA_RESET_AND_EVIDENCE_POLICY_V1.md` (clarify per-fit test roles and historical exposure). Create a separately reviewed `PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL` plus manifests. **Do not change the R44C result freeze.** All listed documents are under `phase2/academic_transform/at0_en/v2_6/`.

## 2. Exact dataset-role matrix

Counts below are published inventories before deduplication, split protection, and exposure exclusions; they are not additive independent trial counts.

| Resource | Construct / evidence tier | Role in first campaign | Test status / restrictions |
|---|---|---|---|
| EBM-NLP_mod, 500 abstracts | Native section-specific human P/I/C/O; separate C | Core native training. Development starts from the documented exposed, unprotected portion of fold1 TRAIN; expected at most 336 after excluding VERIFY 64, before other exclusions | No whole-corpus or five-fold “new independent test” claim. Other split files are not presumed unseen. No EBM-NLP_mod external scoring in this campaign |
| COVID-19, 150 | Same native four-class annotation family | Reserved initially; after procedure freeze, authorized training partitions may be used inside isolated benchmark fits | Primary official-split candidate and separate whole-corpus transfer candidate, both conditional on custody audit |
| AD, 150 | Same native four-class annotation family | Same policy as COVID | Same conditional status; no claim that AD/COVID/EBM_mod are three independent annotation families |
| PICO-Corpus, 1,011 | Human fine-grained PICO/arm/value annotations; definite project exposure | Auxiliary native-schema head on approved training/development records; no automatic broad-span or value-to-PICO conversion | TRAIN/DEVELOPMENT ONLY for this study; no new independent benchmark claim |
| Original EBM-NLP, 4,993 | Crowd/aggregated training P/I/O with hierarchy; professional test annotation | Approved training partition only; independent 3-channel P/I/O auxiliary head | Expert test remains reserved and excluded from auxiliary training. It is not cleared for this campaign's four-class benchmark. Hierarchical control subtype does not equal the core flat C construct |
| TrialSieve, 1,609 | Human rich schema, 20 entity types; 52,638 final spans, not 170,557 independent gold spans | Approved train partition; separate 20-type auxiliary head, preserving released gold | No P/I/C/O test conversion. NonStudyDrug is not universally comparator. Reserved released test partitions remain excluded |
| EvidenceOutcomes, 640 | Human outcome spans in Results/Conclusions; includes 140 EBM-NLP abstracts | Approved train partition; separate outcome head and annotation-scope mask | Never infer negative P/I/C or Title/Methods O labels from this dataset. Parent EBM overlap must be resolved |
| C-TrO, 211 | Human entities/templates/relations in glaucoma and T2DM | Reserve for a later relation-specific study; weight 0 now | No flat-PICO gold mapping; arm membership alone does not prove experimental/control role |
| DISTANT-CTO | Registry-derived distant labels; merged I/C role, intervention semantic types | One bounded weak-supervision ablation only, with separate semantic-type head; no main-head I/C relabeling | Never gold, never evaluation; trial/registry overlap exclusions apply before filtering |
| FinePICO outputs, LLM labels, other pseudo-labels | Silver or method evidence | Weight 0; no generation in this campaign | Never final gold; underlying human corpora retain their original provenance |
| FactPICO, consumed holdouts, old SELECT, R4/R44 diagnostics | Historical exposed material with heterogeneous tasks | Exposure ledger and methodological knowledge; supervised use only where an existing compatible gold task is explicitly listed above | No new independent test claims; factuality labels are not PICO span gold |
| VERIFY_INTERNAL and all aliases | Protected historical resource | Excluded from every stream, prompt, cache, auxiliary corpus and threshold selection | Remains closed; no authorization here |
| Sundaram 2026 RCT-derived resource | Explicitly automatically derived registry-field P/I/O labels | Excluded, weight 0 | Not new human gold; no additional acquisition authorized |

The native three-corpus collection is a defensible **small native core**, not proof of adequate comparator diversity or universal performance. Source counts are 800 abstracts / 6,821 entities, including 523 C, before exclusions. Original EBM-NLP, EvidenceOutcomes and EBM-NLP_mod overlap; simple addition inflates the evidence base. [Native corpus paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10500081/), [original EBM-NLP](https://github.com/bepnye/EBM-NLP), [TrialSieve release](https://github.com/pathology-dynamics/trialsieve_final/tree/62dd931124e36a8c1d9dc4a2469893553d90d2e4), [EvidenceOutcomes](https://pmc.ncbi.nlm.nih.gov/articles/PMC12976956/), [C-TrO](https://github.com/ag-sc/CT-Corpus), [2026 registry-derived paper](https://zenodo.org/records/21918559).

## 3. Provenance, contamination and test protection

Before the first fit, an isolated custodian process must freeze the following without exposing protected text/labels to developers:

1. Source URL, release/commit, file SHA256, license/usage terms, native annotation guideline, human/crowd/weak provenance, official split, exact record count, and native label ontology for every input file. No floating branch or model `main` reference in execution.
2. Canonical document IDs with PMID, normalized DOI, registry IDs and aliases where available; raw-text SHA256; NFC/whitespace-normalized text fingerprint; title fingerprint; original-to-model offset map. Do not overwrite raw text with normalized text.
3. A global alias graph joining identical PMID/DOI/registry IDs, exact normalized text, translated/derived versions, and confirmed same-trial reports. Candidate near duplicates: case-folded title token Jaccard >=0.90, or abstract token 5-gram Jaccard >=0.80, or shorter-abstract 5-gram containment >=0.90. These are conservative screening rules, not proof of distinctness below threshold. Preserve reasons/edges, source record versions, and ambiguous matches.
4. Trial-family screening across all historical ACAD_PASS corpora, R4/R44 splits, FactPICO's 115 source clusters, SELECT/holdouts, attachments, identifiable examples, registry-derived weak corpora, and all proposed auxiliary sources. Missing registry IDs do not prove no trial overlap. Unresolved plausible matches are excluded from training against a protected test family; they cannot be certified independent by an LLM.
5. Separate status fields for developer text exposure, gold exposure, score-driven use, model-training exposure, and base-model pretraining uncertainty. An aggregate paper score is method knowledge; an identifiable labeled example is record exposure.
6. Per-fit manifests: all members/aliases of the held-out document/trial family are absent from native, auxiliary, weak, calibration, prompt-example and cached learned-feature streams. Fold-held-out development records require the same exclusion. Native and auxiliary versions of one record cannot be opposite sides of a split.
7. Within-training duplicates share one canonical sampling identity. Keep multiple native annotation views attached to that identity; average their applicable auxiliary losses instead of counting copied documents as independent samples. Conflicting schemas remain separate heads; no majority-vote invention of new gold.

Preserve official test membership and gold. Remove offending training-side aliases. If official training membership must change, label the result a **decontaminated matched protocol**, and apply identical exclusions to comparators; do not silently claim exact reproduction of published training conditions. If a test record itself was already exposed, the official benchmark result is descriptive for this project. A separately identified clean subset is a different benchmark, not the original SOTA leaderboard. Do not score the exposed official test in this first independent campaign.

AD/COVID text and labels remain inaccessible to interactive development. After procedure freeze, isolated jobs can read only their own authorized training partitions; inference receives held-out text without labels. In fixed cross-validation, a record can legitimately be training in one fit and test in another, provided weights/features never cross and no result informs another fit. “Union of every CV test file must never appear in any training fit” would make ordinary CV impossible; protection is per fit plus a global prohibition on feedback. All external predictions across systems, seeds and protocols must be frozen before any external metric is released.

Base encoder raw-text pretraining overlap must be distinguished from target-label leakage. Audit declared pretraining/continued-training/NER-supervision datasets and exact checkpoint identity. Known target test-label training disqualifies a purported independent comparator. An unavailable complete PubMed pretraining inventory is an explicit limitation, not a fabricated clean certificate and not, by itself, a ban on conventional public-benchmark research. No temporal-freshness claim is justified for these old public corpora.

## 4. Frozen minimal architecture and alternatives

Freeze the **procedure and finite alternatives**, not a claim that an untested architecture is already best. The preferred starting candidate is one end-to-end encoder with a small joint span head; the simpler control remains eligible to win.

Preserved historical evidence: R44C at t=.95 has P/I/C/O precisions 89.189% / 81.711% / 93.182% / 86.612%, macro precision 87.673%, and 130 FPs. Its freeze attributes 123/130 FPs (94.615%) to target-NONE boundary/spurious groups. This supports investigating span formation and rejection, but does **not** show that all I errors are I/C role confusions or that more role modules are necessary. The same freeze reports 16 type fixes versus 27 breaks and lower conditional type accuracy than copy-B. Retain the lesson of limited verifier capacity. These are historical reported observations, not recomputed results or a new authorization to adapt R44.

| Component | First-campaign specification |
|---|---|
| Reference encoder | `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract@d673b8835373c6fa116d6d8006b33d48734e305d`; fresh public pretrained weights for every fit |
| One modern challenger | `thomas-sounack/BioClinical-ModernBERT-base@c3648aa87af95837c809e6f0c5f85d08160db437`; no large-model sweep |
| Text/offset representation | Preserve native word/character coordinates, punctuation and every record; no lowercasing of stored offsets or punctuation stripping for matching |
| Context windows | BiomedBERT: at most 510 content wordpieces, next window starts 256 wordpieces later. Modern challenger: at most 8190 content pieces, next window starts 4096 pieces later. Round starts down and ends down to complete word boundaries while requiring forward progress and full coverage; no gold boundary lookup. Tokenizer-empty words use an explicit UNK representation and retained offset, not deleted records. A single word exceeding the window limit is an explicit preflight failure, never silent truncation |
| Window combination | For each word choose its complete-word occurrence with greatest minimum left/right context; tie by earliest window. Represent a word by mean of its subword vectors. Score document-level word-boundary pairs from those vectors; every valid pair is considered, including pairs whose endpoints used different windows |
| Span head | Four class-specific 64-dimensional start/end projections; GlobalPointer-style relative-position dot-product score `z_c(i,j)`, scaled by sqrt(64), for every legal `i<=j` within one in-scope contiguous source block. Dropout 0.1; no hidden verifier MLP, hard start/end pruning, top-k pruning, or 12-word maximum |
| NONE / invalid spans | All four span scores below threshold means no entity. All fully annotated non-gold pairs supply negative supervision. Missing annotation scope is masked, not treated as negative. This is explicit span rejection without an additional trained verifier |
| I versus C | Separate native I and C output channels learning contextual roles. No rule that first arm=I or placebo/NonStudyDrug=C. No transfer of registry semantic types into role labels |
| Overlap | Preserve all above-threshold typed spans; no NMS, no forced flattening, no fabricated union boundaries. Same offsets with different types are separate predictions; wrong extra types are FPs. Identical `(document, start, end, type)` outputs deduplicate once |
| Auxiliary heads | Original EBM P/I/O: 3 channels. TrialSieve: its 20 released types. EvidenceOutcomes: its native outcome type. PICO-Corpus: one channel for each released native BRAT entity type, ordered lexicographically in the ontology manifest; no semantic collapse. Same small span-head form; dropped at inference |
| Non-contiguous auxiliary entities | Retain component coordinates/provenance; they are unknown for the contiguous head, never silently fused or turned into false negatives. A source with material unsupported annotation structure must fail adapter closure, not be relabeled |
| Excluded additions | C-TrO relation module, generative ensemble, LLM judge/teacher, iterative self-training, learned high-capacity verifier, stacking, calibration fitting, and continued encoder pretraining: all absent |

The native exact-span gold view follows the already frozen source-compatible B-start contract; initial-I continuation fragments do not become new gold entities. Model context may span source segments, but a prediction may not bridge an unannotated section. If original text offsets are unavailable, use document-relative original token intervals and label the metric token-boundary exact; do not invent character offsets from an arbitrary reconstructed string.

The head jointly models starts and ends. A separate boundary-first hard gate is not necessary: a missed start/end would otherwise make a valid entity unrecoverable. PICOX is the necessary mechanistic comparator, not evidence that its particular two-stage structure is automatically optimal. GlobalPointer is a reasonable bounded hypothesis, not a claimed 2026 PICO SOTA. [GlobalPointer](https://arxiv.org/abs/2208.03054), [PICOX](https://pmc.ncbi.nlm.nih.gov/articles/PMC11031223/).

BioClinical ModernBERT supplies a reproducible long-context alternative, but its biomedical NER successes do not prove native PICO superiority. The 2026 ModernBERT-bio paper also shows PubMedBERT remaining stronger on several short-context NER datasets. Therefore no further encoder sweep is justified before this finite comparison. ModernBERT-bio `almanach/ModernBERT-bio-base@ee044b78afd30bfcb6dbb190c44d5472e535bce9` is researched but not another arm; its instruction-data provenance would need its own audit. [BioClinical ModernBERT](https://arxiv.org/abs/2506.10896), [ModernBERT-bio 2026](https://arxiv.org/abs/2605.12438).

## 5. Losses, weights and weak-label admission

For a fully annotated class c and document d, let G be its gold pairs and N its eligible non-gold pairs. Use:

`L_c = log(1 + sum_{(i,j) in G} exp(-z_c(i,j))) + log(1 + sum_{(i,j) in N} exp(z_c(i,j)))`.

Compute with stable log-sum-exp. Average equally over the four native classes, then documents. This balances classes without pretending all possible negative spans are independent observations. Unknown scope/unsupported spans are masked. Auxiliary heads use the same loss under their own ontology and scope; average applicable auxiliary views per canonical document. There is no gold mapping learned from external tests.

Human-federation arm: `L = L_native + 0.25 L_aux`. Native stream batches and auxiliary stream batches each contain 8 canonical documents; sample uniformly within the respective union. Average all native-schema views of a duplicated auxiliary record before weighting. Missing auxiliary classes do not become native negatives. Loss means are per document and per annotated class; corpus size does not multiply the 0.25 coefficient.

Weak ablation only: `L = L_native + 0.25 L_aux + 0.05 L_weak`. A separate **11-way semantic intervention-type softmax head**, using concatenated start/end representations and a single linear classifier, learns only from admitted DISTANT-CTO labeled mentions. `L_weak` is ordinary mean cross-entropy on those labeled mentions. Unmatched text is unknown, not Outside; no C/I role loss is generated. Discard this head at inference. This ablation tests semantic representation transfer, not direct comparator-role learning.

Admit only already-released weak labels whose source text, exact character span, semantic type and registry provenance are recoverable; require exact surface alignment with the retained source text and no conflicting semantic labels at identical coordinates. Exclude fuzzy-only matches, irreversible normalization alignment, unresolved source provenance, and every held-out/protected trial family. From the survivors select at most 10 labeled mentions per trial and at most 100,000 total, by ascending SHA256 of `ACAD_PASS_FED_V1_WEAK|trial_id|document_id|start|end|type`. No replacement to hit the cap. Class count must match the released 11-type schema or the weak arm is canceled before all fits; do not invent a replacement corpus. Use batches of 64 weak mentions; no weak warm-start or extra native epochs.

The native-only arms use weights `(1,0,0)`; human-federation arms `(1,0.25,0)`; weak arm `(1,0.25,0.05)`. Pseudo-labels, LLM outputs and C-TrO relation losses have weight zero. These are prospective design constants, not empirically optimal weights. No weight sweep is permitted.

## 6. Exact training sequence and finite development comparison

**Stage 0 — closure, without model fitting.** Resolve F01–F05; freeze source/file/model hashes, ontologies, document/family manifests, comparator recipes, metric implementation and environment. Synthetic tests must cover repeated strings at distinct offsets, both-empty outputs, orphan I tags, wordpiece/character alignment, punctuation, nested/overlapping spans, missing/duplicate/nonfinite output, and gold-independent chunking. Audit corpus licenses and preserve third-party annotation provenance. No benchmark examples in debugging fixtures.

**Stage 1 — exposed development only.** Use the confirmed exposed, unprotected EBM-NLP_mod pool, plus authorized auxiliary training records. AD/COVID remain sealed. Split development by complete trial-family component into three folds: sort components by SHA256 of `ACAD_PASS_FED_V1_DEV|canonical_family_id` and assign sorted positions modulo 3. No seed search or balancing swaps. Freeze counts; require each held-out fold to contain all four classes and at least 20 native C entities. If this fails, stop before fitting and return for protocol review; no opportunistic reshuffle. Expected 336 native documents is not an audited final denominator.

Run exactly these six arms, each on all three folds and seeds **44, 45, 46**:

| Arm | Native inference model | Training supervision | Scientific contrast |
|---|---|---|---|
| D0 | BiomedBERT + linear 9-way BIO token classifier | Native only | Simple reference |
| D1 | BiomedBERT + four-channel span head | Native only | D1–D0: span representation |
| D2 | Same token classifier as D0, same auxiliary span heads as D3 | Native + auxiliary human | D2–D0: data effect for simple model |
| D3 | Same span model as D1 | Native + auxiliary human | D3–D1: federation; D3–D2: architecture at matched data |
| D4 | BioClinical ModernBERT + same span/auxiliary heads | Native + auxiliary human | D4–D3: one encoder alternative |
| D5 | Same model as D3 + disposable semantic-type weak head | Native + auxiliary human + filtered weak | D5–D3: weak-label contribution |

For the BIO controls, train 9-way cross-entropy on native fully annotated tokens; use fixed BIO-valid Viterbi constraints at inference, with no learned CRF transitions. Native flat BIO is required for this control; do not flatten an unexpected nested gold corpus. Auxiliary heads/weights match the corresponding span arm. The standard BIO decision is maximum valid-sequence probability, not a new tuned threshold.

**Training constants:** full encoder fine-tuning; AdamW, encoder LR `2e-5`, heads LR `1e-4`, betas `(0.9,0.999)`, epsilon `1e-8`, weight decay `0.01` except biases/normalization parameters, global gradient clipping `1.0`, dropout `0.1`, 10% linear warm-up then linear decay to zero. Exactly `20 * ceil(N_native_train/8)` updates. Native documents reshuffled per epoch; auxiliary/weak streams cycle with seeded shuffling. No native oversampling by model error, no early-stopping search, no best-epoch cherry-pick: use the final checkpoint. Mixed precision/accumulation/hardware must be pinned by the runtime manifest before fitting; effective batches cannot change after a result is viewed.

All six arms start independently from the public pretrained encoder, never from another arm or R44 weights. Every development fold excludes its held-out families from **all** training streams. This is end-to-end supervised fitting, not reuse of the R44 OOF bank; nested pair-exclusion stacking is unnecessary because no learned stack is present.

**Stage 2 — one selection.** Complete and freeze every development prediction before comparing arms. Rank by strict four-class micro-F1 pooled across the three held-out folds, then averaged across seeds. For arms within 0.005 absolute F1 of the maximum, choose the lowest-numbered arm. This favors the simpler procedure and prevents an unbounded “best model” search. Report class-wise and worst-fold results, but do not add criteria after seeing them. Report every arm, including negative results.

**Stage 3 — freeze selected procedure and optional selective mode.** Select the single global selective threshold as specified below. Freeze selected arm, training recipe, exact input manifests and all comparator versions before external jobs. No further encoder, loss, boundary rule, seed, example, or data-source substitution.

**Stage 4 — isolated external benchmark jobs.** Retrain from public base weights for each authorized benchmark fit. Never initialize external fits from development-fold weights. All four systems below use the same test population, runtime input scope and one scorer. Freeze predictions for the entire campaign before releasing any score.

**Stage 5 — one deterministic scoring batch, freeze, STOP.** Preserve all predictions, counts, metrics, error status, hashes and unsuccessful runs. No test-guided repair, rerun or selective reporting. A new hypothesis requires a new protocol and a still-unconsumed evaluation resource; it cannot recycle this study's independent-test claim.

## 7. Benchmark matrix and comparison eligibility

| Benchmark cell | Training | Evaluation | Status / meaning |
|---|---|---|---|
| B1: AD official released splits 1–5 | That split's authorized train + exposed unprotected EBM_mod pool + COVID fold1 train/dev, plus selected auxiliary streams; no AD test-family aliases anywhere | Corresponding original `data/AD/fold{1..5}/test.txt`; preserve source metric/aggregation identity | Conditional primary supplied-scope P/I/C/O benchmark with additional training data. AD official dev is unused for adaptive tuning in this campaign |
| B2: COVID official released splits 1–5 | Target split train + exposed unprotected EBM_mod pool + AD fold1 train/dev, plus selected auxiliary streams; no COVID test-family aliases anywhere | `data/COVID-19/fold{1..5}/test.txt` | Same conditional additional-data status |
| B3: leave AD out | Authorized exposed EBM_mod training and COVID official fold1 train/dev only, plus auxiliary training with all AD families removed | Entire original 150-abstract AD corpus, one canonical record each | Secondary corpus-transfer benchmark; target AD text/labels absent from every training/selection stream |
| B4: leave COVID out | Authorized exposed EBM_mod training and AD official fold1 train/dev only, plus auxiliary training with all COVID families removed | Entire original 150-abstract COVID corpus | Secondary corpus-transfer benchmark |
| EBM_mod | Exposed development only | None in this campaign | No new independent full-corpus/5-fold evidence |
| Original EBM-NLP expert test | Reserved | Deferred | Potential future native P/I/O benchmark after lineage audit; no separate-C claim |
| TrialSieve / C-TrO / EvidenceOutcomes tests | Reserved | Deferred | Native-schema transfer evidence would be a separate protocol, not pooled four-class PICO |
| Semantic LLM extraction | No new teacher/annotation | No new semantic judging here | Literature comparison only; existing compatible human semantic benchmark needed before empirical semantic superiority claim |

The exact unique held-out denominator in B1/B2 is **pending split audit**. Never substitute “150 independent test documents per five-fold average” without proving it. If test files repeat documents, preserve official results but cluster uncertainty by original trial and disclose repeats.

All four systems are fixed before external scoring:

1. The selected D0–D5 procedure.
2. BiomedBERT linear BIO reference: target official training partition only for B1/B2 (a closed-data reference); the authorized native source pool for B3/B4. This uses the D0 architecture and fixed training recipe.
3. BiomedBERT linear BIO with exactly the same native, auxiliary and weak training streams as the selected procedure. The weak stream, if needed, uses the same disposable semantic-type head. If any system is identical to another, reuse its predictions rather than add fits.
4. PICOX adapted to native four-class P/I/C/O, using its published boundary-detector/span-classifier design: target official training partition only for B1/B2 and the authorized native source pool for B3/B4. The adaptation and exact upstream notebook/code hashes, defaults, fixed seed handling and independent stage budgets must be reviewed/frozen in Stage 0. An unavailable or substantively ambiguous recipe is **not** permission to invent a weak comparator: stop this comparison before fitting and narrow the claim by independent protocol review.

Systems 1/3 establish the data-matched architecture comparison. Systems 2/4 are explicitly labeled native-data reference systems; a gain over them alone cannot establish architectural superiority or closed-data SOTA. B1/B2 preserve official TEST membership but the main candidate uses an augmented training-data track. Any original train/test-family leakage requiring training exclusions also changes literal historical reproduction status, and must be disclosed for every system.

PICOX's four-class adaptation is not its published merged-I/C result. For each comparator, list original versus changed input scope, label adapter, training sources, split membership, preprocessing and metric. Compare the strongest reproducible **comparable** baseline, not merely the easiest source baseline to beat. If the stronger Hu section-classification pipeline cannot be reproduced with the same information access, the permitted claim is “best among these reproduced supplied-scope systems”; it is not an unrestricted SOTA claim over every section-specific pipeline.

OpenBioNER-v2 and GLiNER-BioMed are relevant contemporary alternatives, but their generic biomedical-type results do not establish four-role PICO performance. OpenBioNER-v2's training example-derived type descriptions require careful zero-shot wording. GLiNER-BioMed base's released `max_width=12` limits long-span capacity; its paper also excludes discontinuous entities and uses entity-preserving chunks. Neither is an automatic drop-in replacement or another unbudgeted fit. Their matched-task reproduction may be nominated only before a later benchmark's first fit; this study must explicitly list them as not head-to-head tested. [OpenBioNER 2025](https://aclanthology.org/2025.findings-naacl.47/), [OpenBioNER-v2](https://huggingface.co/disi-unibo-nlp/openbioner-base-v2), [GLiNER-BioMed 2026](https://doi.org/10.1093/bioinformatics/btag322), [released configuration](https://huggingface.co/Ihor/gliner-biomed-base-v1.0/blob/main/gliner_config.json).

## 8. Metrics, selection, uncertainty and SOTA wording

**Primary metric:** strict occurrence-level typed entity micro-F1, `2TP/(2TP+FP+FN)`, on each of B1 and B2. A TP requires identical document identity, start, end and P/I/C/O class, with one-to-one matching. Repeated identical strings at different coordinates remain distinct entities. Both-empty output/gold contributes zero TP. All documents, unpredicted gold, wrong classes and boundary errors remain in the denominator. No relaxed match, token overlap or entity-surface set score substitutes for this metric.

Require exactly one explicit completion/status record per expected document, including valid empty predictions. Missing/duplicate UIDs, nonfinite scores, out-of-range coordinates or an incomplete inference job invalidate the affected fit; never silently drop rows or treat execution failure as successful abstention. Freeze the failure and stop its scoring authorization. Only a separately labeled conservative diagnostic may treat a failed document as no predictions while retaining all its gold FNs. A failed/incomplete comparator cannot be used as a zero-score straw baseline, and a candidate missing any prescribed seed/fold cannot be nominated under this protocol.

For official split benchmarks, report the arithmetic mean of per-split micro-F1, then the mean across the three seeds, alongside pooled descriptive TP/FP/FN. Do not equate mean-of-fold F1 with pooled F1. For B3/B4, compute micro-F1 over the unique held-out corpus, then average over seeds. Cross-corpus mean is the unweighted mean of B3/B4; it is not a new universal leaderboard score.

**Secondary metrics:** exact P/R/F1 for every class, class-macro F1, all TP/FP/FN counts, goldless-document FP rate, boundary-only versus wrong-type error decomposition, I↔C confusion with exact-boundary conditioning, recall including unrecoverable spans, per-document/trial yield, risk–coverage and precision–recall curves, performance by span length/section/corpus, prediction validity/failure counts, model size, training/inference cost and reproducibility deviations. Partial-match and token metrics, if emitted, are clearly separate descriptive outputs, never used for selection or superiority.

**Uncertainty:** 20,000 paired trial-family cluster bootstrap replicates, random seed 4404. Each sampled family brings all its records, fold appearances and paired-system outputs; average across all three seeds inside each replicate. Never bootstrap tokens/spans/seeds as independent trials. Report 95% descriptive intervals. For confirmatory comparisons against three comparators across B1–B4, use Bonferroni-adjusted two-sided percentile intervals at `1 - 0.05/12 = 99.5833%` for each difference. These are approximate resampling intervals, not finite-sample or domain-shift guarantees. If too few independent families or degenerate resamples prevent a meaningful interval, label the comparison inconclusive.

**Superiority rule:** a corpus-specific superiority claim requires positive adjusted lower bounds against every eligible comparator for that cell, with all results reported. A suite-wide claim requires this in both primary cells; cross-corpus robustness must be stated separately using B3/B4. Merely improving macro precision by abstention is not exact-span F1 superiority.

**Matching rule:** predeclare a one-percentage-point absolute F1 noninferiority margin. “Within 1 F1 point of the strongest reproduced comparator” requires the adjusted lower bound of the difference to exceed -0.01 against each relevant comparator. A nonsignificant difference is not equivalence. Beating/matching fewer reproduced systems supports only that explicitly bounded claim. A missing eligible stronger published comparator blocks a broad SOTA claim, not honest publication of the finite study.

**High-precision mode:** separate from standard F1. For span models use score `s=sigmoid(z)`; this is a confidence score, not an established calibrated probability. For BIO controls use the minimum assigned-tag softmax score over the decoded span. Freeze threshold candidates `{0.80,0.85,0.90,0.95}` for this successor study only; do not rescore R44. From selected-arm DEVELOPMENT OOF outputs, choose the threshold with greatest mean class-macro recall subject, in each seed, to observed precision >=0.90 and recall >=0.33 in every class, at least 30 accepted mentions/class from at least 20 distinct trial families/class. Break ties toward the higher threshold. If none qualifies, declare `NO_HIGH_PRECISION_MODE_NOMINATED`; do not enlarge the grid or suppress a class. Standard span decoding remains `z>0` regardless.

Apply that one threshold unchanged in all external cells. External selective-mode success requires the same precision, recall and unique-support criteria in each corpus and seed; averages cannot hide a failed class. Release counts, cluster intervals and all four class metrics; a point precision >=0.90 is only observed benchmark precision. Small C support may make certification impossible. Do not claim calibrated 90% reliability from sigmoid scores, or let duplicated fold appearances satisfy the minimum support count. Degenerate all-correct bootstrap intervals are not proof of certainty. No temperature/isotonic fit or probability-calibration module is authorized here. A future formal risk-control protocol needs an independent adequate calibration sample and an explicitly matched risk definition; exchangeability does not follow across corpora. [Learn then Test](https://arxiv.org/html/2110.01052v5).

## 9. From-scratch reset, exact budget and stopping

Archive historical manifests, code, learned weights and all outcomes read-only; remove old weights from permitted initialization paths rather than deleting scientific evidence. Initialize each new fit from the pinned public pretrained encoder and freshly seeded task heads. Rebuild permitted corpus views from immutable originals, using reviewed adapters. Do not reuse R44/R44B/R44C candidate-bank predictions, fitted heads, learned boundary weights, normalizers, temperature fits, thresholds as learned artifacts, or optimizer state. Historical method knowledge and exposed training data may be reused under this new objective. Scientific exposure cannot be reset.

**Budget:** one prospectively registered successor study, exactly six development configurations; 3 folds x 3 seeds each = **54 end-to-end development fits**. No adaptive seventh configuration. If the weak stream fails provenance closure before any fit, D5 is canceled without replacement: 45 fits remain. All canceled slots are recorded, not reused.

External campaign ceiling: 4 systems x 3 seeds x (5 AD splits + 5 COVID splits + 1 AD-out + 1 COVID-out) = **144 pipeline fits**. PICOX has two independently trained stages, so its 36 pipeline fits account for 72 model-training stages; other systems account for at most 108. External ceiling = **180 model-training stages**; total study ceiling = **234 model-training stages**, not “one run.” Identical systems are reused, so realized totals can be lower. This is a capped comparison budget, not a computational claim that all fits are necessary or cheap. No extra final refit/deployment model or additional external corpus is included. The runtime/resource feasibility manifest must be accepted before allocating any of these slots; reducing the budget requires a prospective protocol amendment before results, not selective cancellation afterward.

Finite attempts are a methodological judgment, not a number established by the literature. The 2x2 native/federated x token/span comparison is necessary to distinguish data from architecture; the one encoder and one weak arm test two specific alternatives. Three seeds characterize stochastic sensitivity without selecting a lucky seed. Per-source leave-one-out auxiliary ablations, another lambda, another encoder, role relations and teacher/student sweeps are not authorized.

Consume an attempt when its first scientific training job starts. Crash/OOM/nonfinite results remain in the ledger. A byte-identical resume from the last immutable checkpoint, including RNG/optimizer state, is a continuation; a changed seed/order/loss/data/batch or restart from initialization is a new attempt and not authorized. Hardware qualification and synthetic smoke checks must occur before these starts. No test metric is released while later jobs can still be adapted.

**Stop before training** if lineage, protected aliases, native schema, official split identity, gold-independent preprocessing, comparator recipes, or deterministic attempt controls remain unresolved. **Stop after the six-arm comparison** for protocol review if there is no executable valid candidate or no eligible external benchmark. **Stop after external scoring** regardless of success/failure. No tuning on the resulting error analysis in this study.

Evidence against the proposed mechanisms is explicit: no D2–D0 or D3–D1 improvement undermines the human-federation benefit on development; no D3–D2 gain undermines architectural novelty at matched data; D5 failing D3 undermines weak-label utility; gains vanishing after decontamination undermine the original interpretation; positive in-domain but poor B3/B4 results limit transfer claims; no selective threshold meeting support/precision/recall means the high-precision objective is unmet. An inconclusive interval is not proof of no effect. Failure to improve remains publishable; it does not authorize chasing the tests.

Alternative hypotheses remain live: (a) annotation conventions rather than model capacity explain many boundary errors; diagnose per-source boundary/continuation patterns without changing gold; (b) gains come from extra data rather than the span head; D0–D3 isolates this; (c) contextual truncation explains failures; D4 tests one long-context alternative; (d) weak terminology supervision worsens role decisions; D5 and I/C diagnostics can disconfirm its use; (e) low C counts explain apparent precision gains; support counts and clustered uncertainty prevent a strong claim from a few successes; (f) public benchmark style/pretraining exposure explains apparent generalization; B3/B4 and provenance disclosures limit that interpretation. These analyses explain frozen outcomes; they cannot trigger adaptive repairs in this campaign.

## 10. Research findings that constrain the design

| Primary source | Decision-relevant finding | Consequence |
|---|---|---|
| Hu et al., native PICO resource | Separate C, constrained sections, one annotation lineage; code-level preprocessing caveat | Use its native schema; audit source parity; restrict task claim |
| PICOX, JAMIA 2024 | Boundary/span mechanism and overlap support; merged I/C evaluation | Adapt and reproduce prospectively; no direct four-class headline comparison |
| FinePICO, JAMIA 2025 / 2024 preprint | Semi-supervision is promising, but sentence-level PICO-Corpus splits and partial-match AD/COVID transfer do not prove exact four-class gains here | No automatic adoption; no random sentence split; teacher weight zero initially |
| AlpaPICO, Methods 2024 | Instruction tuning/ICL; inspected string-set scorer differs from exact occurrence evaluation | Semantic/string metrics remain separate; no copied leaderboard claim |
| TrialSieve 2025 | Useful rich human annotation; annotation total includes raw repeated votes, not independent gold | Own schema/head; no flat comparator relabeling |
| EvidenceOutcomes 2025 | Clinically meaningful Results/Conclusions outcomes; 140 EBM-NLP parents | Separate outcome scope/head and duplicate lineage |
| C-TrO | Arm/intervention/outcome relations may support role reasoning, but task/ontology differ | Plausible later hypothesis; no unvalidated extra relation module now |
| DISTANT-CTO | Roles explicitly merged; weak semantic intervention labeling | Small separate semantic-type ablation only |
| OpenBioNER 2025 / v2 2026 | Type-description transfer using synthetic supervision and description-generation choices | Relevant comparator family; not independent human gold or proof of PICO-role SOTA |
| GLiNER-BioMed, Bioinformatics 2026 | Synthetic teacher/student data; bounded spans and benchmark preprocessing constraints | Do not make it default or inherit gold-informed chunking |
| BioClinical ModernBERT 2025; ModernBERT-bio 2026 | Real encoder alternatives, no universal short-context superiority | One challenger, no architecture escalation by recency alone |
| Hao et al., JMIR 2026 | Llama 3.2-3B; P/I/O only; exact mention-text matching; acknowledges public benchmark contamination uncertainty | Another current comparator with mismatched task; not four-role coordinate SOTA |
| Sundaram 2026 | Registry-field labels without manual annotation; token P/I/O evaluation | Not the fresh human corpus sought; excluded |
| GPT-4o mass extraction 2024 | 342/350 abstracts judged semantically accurate/comprehensive | Practical semantic evidence only, not 98% exact-span precision |
| Learn then Test | Risk control requires specified calibration/testing assumptions | No unsupported conformal/precision guarantee under corpus shift |

Additional primary links: [TrialSieve paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12109152/), [C-TrO paper](https://doi.org/10.1186/s13326-022-00271-7), [Hao 2026 full paper](https://www.jmir.org/2026/1/e91215/PDF), [Hao code](https://github.com/zeyuanhao-cs/PICO), [GPT-4o mass extraction](https://pmc.ncbi.nlm.nih.gov/articles/PMC11473607/).

This was a targeted current primary-literature and source-code review, including disconfirming sources, not a claim of an exhaustive systematic review. Papers are not independent replication simply because they reuse several differently named versions of the same underlying abstracts.

## 11. Forty required decisions — closure index

| # | Decision |
|---|---|
| 1 | YES: existing public human annotation can support development without new local experts |
| 2 | YES conditionally: frozen, compatible, exposure-audited public tests and credible comparators support scoped benchmark claims |
| 3 | Native core: EBM-NLP_mod / COVID / AD; PICO-Corpus has human PICO structure but different granularity and exposed status |
| 4 | Original EBM-NLP, TrialSieve, EvidenceOutcomes, fine-grained PICO-Corpus: native-schema auxiliary heads; C-TrO deferred |
| 5 | DISTANT-CTO and all pseudo/LLM labels are weak/silver; never human gold |
| 6 | Previously exposed unprotected ACAD_PASS records, including EBM_mod lineage and PICO-Corpus, remain train/development |
| 7 | AD/COVID official tests are candidates only; none is declared eligible before custody audit; original EBM expert test reserved |
| 8 | Exact file/record/schema/split hashes, alias/trial-family graph, prior-exposure ledger and per-fit exclusions in Section 3 |
| 9 | YES as a small native core, not 800 newly independent records or three annotation families |
| 10 | Original EBM training P/I/O head; no automatic separate-C mapping; reserve expert test |
| 11 | TrialSieve 20-type head; no NonStudyDrug=C assumption or invented PICO gold |
| 12 | C-TrO may help roles, but arm links are not proof; relation module weight zero in first campaign |
| 13 | YES, EvidenceOutcomes auxiliary O within its actual annotation scope, with overlap screening |
| 14 | One role-agnostic semantic-type weak arm; exact-match provenance filters, cap, weight 0.05, unknown negatives masked |
| 15 | FinePICO-style semi-supervision is a later hypothesis, not justified as a mandatory first component; no iterative pseudo-labeling now |
| 16 | No LLM teacher in this campaign |
| 17 | NO: silver does not become final human gold; without qualified independent human validation it remains silver |
| 18 | One encoder + small four-channel joint span scorer; finite simpler/encoder/weak alternatives, Section 4 |
| 19 | Pinned BiomedBERT reference; one pinned BioClinical ModernBERT-base challenger |
| 20 | Word-boundary pairs, low-rank start/end score; no hard proposal bottleneck or short maximum span |
| 21 | Native separate I/C contextual output channels; no registry/arm-order relabeling |
| 22 | Native-schema entity heads for four auxiliary sources; no relation stack |
| 23 | Class-balanced multilabel span log-sum-exp loss; BIO control CE; weak semantic-type CE |
| 24 | Native/human/weak weights 1 / 0.25 / 0.05, with weak absent except D5 |
| 25 | Typed coordinate sets preserving nesting/overlap; no union fusion or NMS; unsupported discontinuities masked and audited |
| 26 | No generative inference ensemble |
| 27 | No additional verifier; the low-capacity joint span score already rejects invalid spans |
| 28 | One development-selected global selective threshold; no fitted calibration or cross-domain probability guarantee |
| 29 | Conditional AD/COVID official supplied-scope tests plus two corpus-transfer cells; other task metrics separate |
| 30 | Per-corpus strict typed occurrence micro-F1 with identical denominators/aggregation |
| 31 | Per-class metrics/counts, macro F1, error decomposition, selective curves/support/uncertainty, failure/cost diagnostics |
| 32 | Two predefined whole-corpus transfer directions, complete target-family exclusion and one frozen procedure |
| 33 | Custody, per-fit access isolation, all predictions frozen before any external scores, no feedback/retry |
| 34 | Same schema/splits/scope/matcher/data regime or explicitly adapted reproduction; no direct incompatible headline ranking |
| 35 | YES: GPT-4o 98% remains a separate historical semantic comparator, not a strict-span number |
| 36 | Six development configurations, 54 fits; one external campaign with ceiling 144 pipeline fits / 180 model-training stages; total ceiling 234 stages |
| 37 | Fixed token/span x native/human factorial, one encoder contrast, one weak contrast; no retrospective component hunt |
| 38 | Falsification/limitation rules in Section 9, including data-matched failure, poor transfer, unsupported selective mode and contamination |
| 39 | NO: new annotation is not inherently necessary before a sound public-benchmark publication |
| 40 | Strong prospective clinical validation needs independent fit-for-purpose evidence, which could come from a later external human-gold source or qualified external annotators; it need not be local, and annotation alone is insufficient |

**Required next checkpoint:** `PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_AND_PROVENANCE_CLOSURE_BEFORE_FIRST_FIT`. It must contain the corrected ledger, eligible benchmark decision, complete source/ontology/scorer/comparator/runtime hashes, training/attempt manifests, and synthetic-only preflight evidence. No successor training is authorized merely by this review's favorable direction.