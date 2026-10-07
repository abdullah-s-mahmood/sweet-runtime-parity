# ACAD_PASS — R4.3 Causal Forensic Audit, Literature and Next Experiment Recommendation

**Date:** 2026-10-07 (Asia/Baghdad)
**Status:** READ-ONLY SCIENTIFIC AUDIT. Historical DEV, protected external tests, FactPICO and consumed 60-RCT holdout remain closed.
**Repository:** `abdullah-s-mahmood/sweet-runtime-parity`; branch `at0-en-v2.6-dev`.

## Executive verdict

**`STOP_ARCHITECTURE_ESCALATION; FIX_NEGATIVE_GENERATION_AND_EVALUATION_CONTRACT_FIRST`.**

The current evidence does **not** establish that the next best move is BOPN, triaffine, MRC or a larger encoder. R4.3 Stage B completed technically, but neither H0 contextual MLP nor H1 contextual+b iaffine passed the frozen scientific gate. Two stronger, identifiable causal problems precede architecture selection:

1. The planned native/model-error negative training component was **entirely absent**: Stage B recorded `native_slots=0`, despite SELECT containing 250 false native B proposals. The current mining algorithm uses predictions from a B model trained on the same FIT examples and never seeds error mining from gold-empty sentences. The in-sample issue and goldless-sentence blind spot must be distinguished in a FIT-only audit.
2. The legacy cropped C-type head receives **only gold positive spans** in training, no invalid or NONE examples, yet its multi-label sigmoid outputs and exclusive threshold gates are treated as if they reject invalid boundaries and spurious candidates.

Additional issues include unvalidated BIO decoding transitions, non-comparable probability heads with a shared threshold, strong class imbalance, loss of inter-sentence/section context, possible partial gold labeling, and exposure of SELECT as a model-selection set.

These are evidence-backed shortcomings; whether each contributes materially to the 87 remaining H1 false positives has NOT been measured. Do not confound plausible mechanism with measured causal attribution.

## A. Frozen outcome and reproducibility

Stage A:
- Run `37535183682` SUCCESS; artifact `11455753005`; physical SHA verification run `37566322559` SUCCESS.
- B 10 epochs/1620 steps, model SHA `4e4852b847be5bf64cd707ed62f770e13d64ee6becea3ce049f69bde220bfb05`.
- Boundary 3 epochs/486 steps, SHA `8c0848e798dd2b2409a81931b7bac496f88fceec2c8bd589e95a186d67dacebb`.
- C Type 3 epochs/447 steps, SHA `c7d5e4d2eb1632ac39c944e28232f8addff6c037b1ea80a09436a885101aed1a`.
- FIT=320 documents/2371 gold spans, SELECT=80 documents/640 gold spans, split-manifest SHA `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`.

Stage B:
- Run `37566553994` SUCCESS technically; scientific verdict `DIAGNOSTIC_NO_ARCHITECTURE_READY`.
- Candidate ceiling 697 native proposals, 447 exact+type correct and 250 false proposals on SELECT; ceiling recall P 0.8152, I 0.6483, C 0.7297, O 0.7104. All classes meet the frozen candidate ceiling's minimum recall/support feasibility.
- Training examples: 2371 gold positives, 6157 unique local/composite negatives, **0 native FIT-error slots**, and 1982 background fallback slots.
- H0 10 epochs/1630 steps, final batch loss 0.00083949.
- H1 10 epochs/1630 steps, final batch loss 0.00080785.
- Neither passed the frozen exact-span-and-class scientific gate (per-class precision >=0.90, recall >=0.20, accepted >=10, macro precision >=0.90; t in {0.80,0.85,0.90,0.95}).

### Same-SELECT paired comparison, t=0.90

| Variant | Exact TP | False positives | Macro precision | Macro recall |
|---|---:|---:|---:|---:|
| Frozen pre-pair C-style consensus | 371 | 100 | 0.833404 | see frozen summary |
| H0 contextual MLP | 348 | 85 | 0.841786 | 0.536197 |
| H1 contextual+b iaffine | 362 | 87 | 0.843930 | 0.550659 |

The H1 head removed 13/100 baseline false positives but also 9/371 true positives. H0 removed 15/100 FPs but 23/371 TPs. At t=.90, H1 outperformed H0 in macro precision by only 0.002144 absolute (0.214 percentage point).

H1 accepted FP taxonomy at t=.90:
- 46 `SPURIOUS_NO_OVERLAP` (52.9%)
- 34 `SAME_CLASS_WRONG_BOUNDARY_OVERLAP` (39.1%)
- 5 `DIFFERENT_CLASS_EXACT_BOUNDARY` (5.7%)
- 2 `DIFFERENT_CLASS_WRONG_BOUNDARY_OVERLAP` (2.3%).

This is NOT the same error distribution as historical R4.2C DEV. The prior hypothesis that cross-pair errors dominate is not supported: prior `joint_invalid_fp` was a diagnostic grouping, not 48 literal composite cross-pairs; actual cross-entity boundary pairings numbered only three across the 404-candidate diagnostic.

### Quantifying the remaining precision gap

At H1, t=.90:
- P: TP=68 FP=10, precision 0.87179. To achieve >=0.90 without losing TP requires FP<=7: remove **3**.
- I: TP=148 FP=42, precision 0.77895. At fixed TP requires FP<=16: remove **26**.
- O: TP=133 FP=34, precision 0.79641. At fixed TP requires FP<=14: remove **20**.
- C: TP=13 FP=1, precision 0.92857; already satisfies precision, recall and accepted floor at t=.90.

Therefore **at least 49 precisely targeted P/I/O FPs must be removed at fixed TP** to satisfy per-class precision. Raising a global threshold alone cannot be assumed to do this; t=.95 rejects all class-C candidates and fails its recall/accepted floors.

Uncertainty: H1's descriptive document-bootstrap macro precision interval at t=.90 was approximately [0.777,0.904], and H0's [0.775,0.902]. Neither is evidence of a 90% per-class gate pass.

## B. Findings classified by evidentiary strength

### F1 — CONFIRMED: Native hard-negative component missing
**Evidence:** `slot_counts.native_slots=0`, `fallback_slots=1982`. Stage B model is trained on synthetic local, synthetic composite, or background spans, not actual B errors on FIT.

**Code:** `r43_stage_b_h0_h1_diagnostic.py:196-267`. The miner loops over gold positives and queries in-sample `fit_b`; this is prone to optimistic FIT predictions and excludes false proposals in sentences with no gold spans by construction. It does **not** prove that the B model makes zero false proposals anywhere on FIT.

**Causal hypothesis:** easy/artificial negatives create an overly easy training problem; H0/H1 final batch losses close to zero but the head generalizes poorly to high-confidence B false proposals from out-of-document SELECT.

**Next diagnostic (FIT-only, read-only):** replay the Stage-A B model on FIT and separately count native proposals in gold-bearing and gold-empty sentences; count raw predicted BIO transition violations. The script `r43_fit_b_native_error_causal_audit.py` has been prepared but at this report's timestamp has NOT been run. Do not claim measurements for it.

**Prospective remedy:** after audit, create **document-group-disjoint out-of-fold (OOF) B predictions within FIT**. Mine typed and untyped real errors from every FIT document, including **goldless sentences**, while preserving gold precedence and safe ambiguous/uncertain labels. Freeze errors and source hashes before head training.

### F2 — CONFIRMED: Positive-only cropped C type training
**Code:** `r43_fit_ancestors_train.py:105-116,165-185,210-241`. `SpanDataset` is instantiated from exact gold `span_rows` and each example uses a one-hot multi-label sigmoid target. No invalid-span or NONE examples are included in the type head's training.

**Inference:** `r43_stage_b_h0_h1_diagnostic.py:163-174,352-391`. The head is asked to reject wrong-boundary/spurious candidates, with one type's sigmoid score >=t and every other type <t.

**Consequence:** category discrimination on valid spans should not be confused with entity-existence verification. This is a **task mismatch**, though it is not a proof that the original C head is the only cause of errors.

**Prospective remedy:** learn calibrated typed existence (NONE/P/I/C/O) from actual OOF native proposals and gold labels. Separate type-only diagnostics from valid-span discrimination, or replace brittle positive-only C-type veto with a joint class/NONE head in a newly frozen architecture.

### F3 — CONFIRMED ON SYNTHETIC INPUT: Illegal BIO transition silently normalized
**Code:** `r43_stage_b_h0_h1_diagnostic.py:112-124`.

Actual-code AST-extraction test: `r43_semantic_contract_audit.py`, GitHub run `37568400156`, SUCCESS. On synthetic labels `[O, I-P, I-P, O]`, the decoder emitted a confident P entity `[1,3)` despite the invalid I-after-O transition. On `[B-P,I-I,I-I]`, it emitted P and I spans at an invalid type switch.

**Impact on actual data: UNKNOWN.** Count such transitions on FIT using the frozen model before attributing spurious SELECT FP to this decoder. A gold example starting `I-X` may legitimately denote a continuation segment under our special source convention; it must not be blindly rewritten.

**Prospective correction:** explicit BIO grammar/constraints and documented handling of source continuation segments, plus unit tests for O->I, wrong-type I, adjacent entities, begin/end; preserve a record of invalid transitions instead of converting them silently.

### F4 — CONFIRMED STRUCTURAL LIMIT: Head can only veto B proposals
**Code:** `metric_counts` keeps exactly `(B type,B start,B end)` when head top-class matches B type. It cannot change endpoints, recover missed entities or correct a B type. This is a cascade architecture limitation, not a runtime bug.

**Diagnostic:** candidate recall ceiling exceeds scientific recall floor in each class, so candidate repair is **not a precondition** for passing the frozen gate; the immediate barrier is persistent precision/FP rejection in P/I/O. Repair is still relevant if overall recall and practical coverage are prioritized in a future design.

### F5 — CONFIRMED: Heterogeneous, uncalibrated scores gated at one common t
B minimum per-token argmax probability, boundary START+ BOTH/END+BOTH softmax probability, positive-only cropped C sigmoid, and 5-way H0/H1 softmax are NOT interchangeable probabilities of the same event.

The fourfold consensus may cause high-confidence wrong acceptances and unnecessary true rejections. Class C has 37 gold examples on SELECT and collapses to zero accepted at global threshold 0.95.

**Remedy:** avoid posthoc SELECT threshold shopping. For a future version, derive one candidate-level calibrated estimate of `P(exact span AND exact type | native proposal, evidence)` using FIT-internal held-out/OOF calibration and report reliability, Brier/ECE, risk–coverage and per-class CIs. Any target threshold/policy must be frozen before independent assessment.

### F6 — CONFIRMED: False-positive taxonomy is reference-relative, not clinical truth
`SPURIOUS_NO_OVERLAP` means no overlap with annotated gold in the current reference, not that the phrase is definitely clinically irrelevant. Flat BIO labels may omit valid nested/alternative spans and the original EBM-NLP annotation literature documents variable span granularity and label quality.

Code `fp_taxonomy` prioritizes same-class overlap over different-class overlap if both occur, so the categories are a deterministic operational partition and not disjoint causal mechanisms.

**Remedy:** maintain separate code-level and annotation-ambiguity flags; report exact/IoU/type measures but do not replace frozen exact gate with forgiving metrics. Examine label guidelines, class C ontology, partial annotation and cross-sentence continuation in TRAIN only before calling every gold-absent span an unquestionable NONE.

### F7 — CONFIRMED LIMIT: Sentence-only representation loses abstract/section information
Code `make_sentence_rows` and `infer_boundary_and_context` encode each blank-delimited model example separately. The so-called FULL context is the full current **sentence**, not the entire RCT abstract; P/I/C/O can depend on ABSTRACT SECTION, comparison arms, preceding sentences and study design.

**Scientific implication:** section-aware/discourse representations are a strong domain-matched alternative to adding pair bilinear capacity. A 2023 section-specific PICO work described the importance of RCT sections and harder role distinctions. No source section metadata has yet been proven available in the pinned CoNLL file; do not invent it.

### F8 — POTENTIAL FUTURE METRIC BUG: Duplicate acceptance
The current `metric_counts` increments TP/FP/accepted for each accepted candidate row, while using a set to compute FN. If future generators emit the same coordinate twice, recall/counts can be biased. Current BIO proposal decoding produces unique contiguous spans, so there is NO evidence this explains R4.3 Stage-B metrics. Add deduplication before counting and synthetic invariant tests before any union/repair generator is introduced.

### F9 — FUTURE STRUCTURAL HAZARD: Overlapping gold in single-label boundary tags
`r43_fit_ancestors_train.py:118-126` overwrites one boundary tag per token, losing overlapping START/END flags when spans overlap. A synthetic actual-code test demonstrated this. Current pinned source labels are flat BIO and cannot represent nested spans; this is NOT an active verified defect on R4.3. If nested support is later desired, migrate gold representation and boundary head together (multi-label or span grid).

### F10 — METHODOLOGICAL: Reusing SELECT and unstable exploratory findings
R4.2B/C/D and R4.3 results already guided successive method choices; Stage-B SELECT is now exposed for architecture decisions. Reusing this as independent test for further adaptive versions would overstate evidence.

Two independent FIT-only H0/H1 probes on distinct inner splits disagreed in ranking:
- run `37540851386`: H1 macro-F1 advantage +0.01564.
- run `37541116791`: H1 macro-F1 disadvantage -0.01803.

Context-signal FIT-only probe was positive (+0.07797 macro-F1 versus cropped content), but the context-locality probe's zero lexical-label collisions at +/-4 words may be driven by unique longer keys; it **does not** prove generalization.

**Remedy:** new nested, document-grouped FIT-internal CV for prospective model selection. Treat original SELECT as exposed regression evidence, and authorize a genuinely untouched final benchmark only once after model/protocol freeze. Keep protected tests closed now.

## C. Literature audit — source and limits

### C1. Direct PICO evidence
- **PICOX**, Zhang et al., *JAMIA* (2024), DOI `10.1093/jamia/ocae065`, https://pmc.ncbi.nlm.nih.gov/articles/PMC11031223/. Joint boundary generation, span typing, composite negative augmentation. Strongest directly domain-matched precedent. Its reported entity F1 is NOT comparable to our per-class precision gate without aligning protocol.
- **Section-specific PICO extraction**, *JAMIA* (2023), https://pmc.ncbi.nlm.nih.gov/articles/PMC10500081/. Highlights difficulty of PICO spans and dependence on abstract discourse/section, plus label complexity.
- **BLINK-LSTM / BioLinkBERT**, Ghosh et al. (2024), DOI `10.1145/3632410.3632442`. Stronger biomedical encoder plus recurrent/ensemble context pathway; potential baseline, not proof of better exact-gate precision in this exact split.
- **AlpaPICO** (2024), DOI `10.1016/j.ymeth.2024.04.005`. LLM/ICL PICO extraction as independent structured-extraction baseline, not a replacement for span-offset safety.

### C2. Boundary and joint span models
- **BEAN**, Wang et al., *BMC Bioinformatics* (2025), DOI `10.1186/s12859-025-06086-4`: triaffine head/tail/global context and type modeling; GENIA/NCBI Disease etc. Strong model but a larger step than correcting native negatives.
- **BGNER**, *Journal of King Saud University Computer and Information Sciences* (2025), DOI `10.1007/s44443-025-00059-6`: boundary-aware GlobalPointer and span-boundary relation modeling.
- **Multi-head Tri-Affine Attention**, Zhang et al. (2026), DOI `10.1007/s44163-026-01357-2`: multihead triaffine span+interior modeling, boundary smoothing; evaluated on nested datasets and a flat RESUME dataset; not an RCT-PICO benchmark.
- **BOPN**, Tang et al., *Findings EMNLP* (2023), DOI `10.18653/v1/2023.findings-emnlp.989`: bounded offset correction.
- **Locate-and-Label**, Shen et al., *ACL* (2021), DOI `10.18653/v1/2021.acl-long.216`: IoU-aware proposals, local boundary regression.
- **GLiNER-biomed** (2025 preprint), https://arxiv.org/abs/2504.00676: task-description and synthetic biomedical training. Open-weight baseline/teacher, not proven PICO gate.
- **OpenBioNER-v2**, *Expert Systems with Applications* (2026), DOI `10.1016/j.eswa.2026.131725`: biomedical lightweight zero-shot type-description models. This is a **candidate independent baseline**, not a promised strict exact-PICO improvement.

### C3. Real vs synthetic label noise
- **NoiseBench**, Merdjanovska et al., *EMNLP* (2024), DOI `10.18653/v1/2024.emnlp-main.1011`, https://aclanthology.org/2024.emnlp-main.1011/: realistic human/automatic/LLM NER annotation noise differs materially from easy synthetic label corruption.
- **CMiNER**, Wei et al., *Expert Systems with Applications* (2025), DOI `10.1016/j.eswa.2025.126987`: addresses missing and mislabeled NER annotations.
- **EBM-NLP original corpus**, Nye et al., *ACL* (2018), DOI `10.18653/v1/P18-1019`: multi-annotator/aggregated train annotations and medical-expert test labels; type and boundary standards are not trivial.
- **Not so weak PICO** (2023), https://pmc.ncbi.nlm.nih.gov/articles/PMC9828146/: evaluates annotation inconsistency and error-corrected label alternatives.

**Implication:** realistic OOF error-bank + annotation-risk filtering should precede ever-more synthetic negatives or complicated scorer tensors.

## D. What operational systems do (not identical metrics)

1. **Trialstreamer**, *JAMIA* (2020), DOI in https://academic.oup.com/jamia/article/27/12/1903/5907063 : classify RCT/human studies -> extract PICO spans with an LSTM-CRF -> normalize concepts to MeSH -> store/rank with provenance. Reports **token-level** PICO F1 near 0.71/0.65/0.63 for P/I/O from prior model, not guaranteed strict exact span accuracy.
2. **Elicit Systematic Review** (2025 published system description) uses retrieval, screening, structured data extraction, supporting quotes/citations and editable/reviewer-overridable decisions. Vendor's accuracy claims should be separated from external measurements: https://elicit.com/blog/how-we-evaluated-elicit-systematic-review .
3. **Independent Elicit audit**, Bianchi et al. (2025), DOI `10.1002/cesm.70033`: many variables partially equal to manual extraction, particularly nuanced intervention effects; reviewers still necessary.
4. **Mass GPT-4o PICO extraction study** (2024), DOI `10.1007/s40290-024-00539-6`: authors report 98% of 350 sampled abstracts sufficiently extracted on their human-reviewed task. That is NOT an exact-span-and-type 90% precision benchmark; reporting denominator and adjudication differ.
5. **GLiNER2** (2025 open-source framework) uses schema/type descriptions to guide extraction and outputs structured entities; can be a strong independent candidate but is not evidence of ACAD_PASS exact PICO gate performance.

**Architectural lesson:** credible applied systems separate extraction from evidence support, terminology normalization and selective human/review escalation rather than treating every high softmax number as publishable or safe.

## E. Recommended next work, sequenced and pre-registered

### Gate 0 — READ-ONLY ROOT-CAUSE AUDIT (NEXT ACTION; NO TRAINING)
0a. Replay frozen B on **FIT only**; count exact proposals, false proposals in gold-containing vs gold-empty sentences, and invalid BIO transitions. Verify Stage-B `native_slots=0` without accessing SELECT again. Prepared script: `r43_fit_b_native_error_causal_audit.py`, not yet executed.

0b. Inspect 100% of FIT synthetic negative provenance for: exact-gold collisions, same surface used as NONE and GOLD in differing contexts, overlapping valid but unannotated spans, and balanced representation of no-gold sentences.

0c. Test BIO decoding and metric invariants on entirely synthetic fixtures; actual-code semantic test run `37568400156` SUCCESS already proves an illegal-transition normalization bug and warns about future duplicate-candidate counting.

0d. Audit corpus ontology against original PICO guidelines, source `EBM-NLPmod` and official `evaluate.py`; clarify class C vs I, cross-example `I-X` continuation fragments (11 cases), token-to-wordpiece and exact offset mapping. The original source `evaluate.py` does not by itself define our task's authoritative macro precision gate.

0e. Check near-duplicate/PMID/trial leakage (exact document duplicates already zero; semantic duplicates untested). Do not falsely report PMID isolation without verifying source identity.

**Stop:** if gate 0 exposes a metric/protocol error, make only a tightly scoped unit-tested technical repair in a new version while preserving frozen Stage-B evidence.

### Gate 1 — Correct TRAIN-ONLY OOF data construction
Only after design/freeze and explicit authorization:
- Group-disjoint, deterministic 2- or 3-fold B candidate training **inside FIT**.
- Generate OOF native proposals in held-out FIT folds, including gold-empty sentences.
- Retain false proposals stratified as: no overlap, wrong-boundary same type, cross-type, composite/endpoints, and high-confidence valid-looking FP.
- Gold coordinate precedence, provenance trace, label noise/uncertain protection, near-duplicate group safety.
- Prospectively freeze negative reservoir, class mix, caps, BERT weights and all exact coordinates before head training.
- Include goldless negatives. Do not use SELECT/DEV to tune mixture proportions.

### Gate 2 — Fair architecture trial using FIT-internal nested selection
Priority:
1. **Corrected contextual H0 / joint NONE-P-I-C-O typed existence** using OOF error bank; minimal new complexity.
2. **H1 biaffine** with *identical* examples and context to establish true incremental value, with macro precision, recall, risk–coverage and per-class evidence.
3. Only if mechanism merits: **boundary-repair gate + small bounded offset head** for verified local errors; separately reject composite/spurious.
4. Compare one section/discourse-aware candidate architecture where the source provides valid section context.
5. Consider triaffine/GlobalPointer/GLiNER-biomed/OpenBioNER-v2/LLM teacher as prospectively chosen baselines after current engineering defects are fixed.

Do not run an unconstrained model zoo on exposed SELECT. Freeze comparisons inside FIT with independent document-grouped CV; once the architecture and threshold are locked, request a separately approved untouched final test/benchmark.

### Gate 3 — Production selective-risk discipline
- Exact-span+exact-type confidence must be calibrated; report ECE/Brier and per-class risk–coverage.
- Define evidence provenance to original abstract offsets and confirm exact substring restoration.
- Abstain/REVIEW for uncertainty and annotation ambiguity; do not pretend an LLM or public article label is an expert adjudicator.
- Keep outputs reversible, typed and versioned; run downstream ACAD_PASS protect/verify/drift gates.
- Report both scientific exact gate and downstream safety/utility separately.

## F. Priority ranking

| Rank | Work | Evidence strength | Expected value | Cost/risk |
|---|---|---|---|---|
| 1 | FIT-only native B replay, goldless negative count, BIO checks | STRONG / direct code | Expose real failure cause without training | Low |
| 2 | Correct OOF error mining and annotation-aware NONE | STRONG causal rationale, outcome unproven | Highest reasonable probability of addressing 46 no-overlap and 34 near-boundary FPs | Medium/high (OOF models) |
| 3 | Corrected joint contextual typed existence + calibrated score | Strong context probe, incomplete implementation | Addresses overconfident false acceptance and positive-only type mismatch | Medium |
| 4 | Near-boundary repairability gate (BOPN/Locate-and-Label) | Strong TRAIN structural feasibility, not native outcome | Recall recovery and exact boundary correction | Medium |
| 5 | Section/discourse-aware PICO representations | Strong domain rationale, source section mapping unverified | Better I/C/O disambiguation | Medium |
| 6 | Triaffine / GlobalPointer / stronger biomedical encoder | Peer-reviewed general BioNER, not direct causal evidence yet | Potential later uplift | High |
| 7 | LLM extraction teacher/comparator | Practical systems show value but different metrics | Candidate generation, ambiguous spans, adjudication assistance | Variable cost / hallucination |

## G. Current disposition

- **Scientific Stage B:** TERMINAL, TECHNICAL PASS, SCIENTIFIC FAIL.
- **No new training authorized or run by this forensic review.**
- **Prepared read-only FIT replay exists, but the workflow dispatch is not completed; do not claim its results.**
- **No protected data opened.**

**NEXT_ACTION = COMPLETE_FIT_ONLY_CAUSAL_REPLAY_AND_PROTOCOL_AUDIT; THEN SEEK_ONE_ADVERSARIAL_HIGHER_MODEL_REVIEW; ONLY THEN FREEZE_ANY_NEW_TRAINING.**

Remember: a stronger model on mislabeled/easy negatives is unlikely to provide scientifically defensible progress. Repair the supervision and truth-conditions first.
