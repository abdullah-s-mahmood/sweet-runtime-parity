1. **VERDICT — PROCEED_WITH_CHANGES**

   **PROCEED_SURUS_ADMISSION_WITH_CHANGES.** Admit SURUS prospectively as a separate auxiliary task in D2/D3/D4, subject to the mandatory changes below. This authorizes a protocol amendment, **not a scientific fit**.

   Reviewed repository snapshot: [2ee3bf67d22187d4b4ecba8e624367032fd64d97](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/tree/2ee3bf67d22187d4b4ecba8e624367032fd64d97), branch at0-en-v2.6-dev, research cutoff 2026-10-09. I verified both official audit runs as successful first attempts and downloaded their aggregate artifacts: both ZIP SHA256 values match the packet. The attempt manifest contains 45 NOT_STARTED/unconsumed slots and nine canceled D5 slots. These are mechanical findings; they do not establish contamination clearance or scientific benefit.

2. **Strongest arguments FOR admission**

   SURUS supplies human annotations reviewed by experts, a released fine-grained ontology, reproducible source files, and supervision plausibly relevant to contextual distinctions and entity boundaries. It qualifies as **expert-reviewed human gold**, not evidence that every record received independent double annotation.

   Its potential value is complementary supervision for the shared encoder. This is a hypothesis worth testing before the first fit, with no additional scientific arms and no conversion to native P/I/C/O. Separate source identities and loss isolation address the annotation incompatibility highlighted by [SRU-NER, BioNLP 2025](https://aclanthology.org/2025.bionlp-1.20/).

   **Yes, this narrowly bounded information gain justifies one prospective amendment.** Near-completion percentages alone are not a scientific reason to reject it.

3. **Strongest arguments AGAINST admission**

   More sources can worsen the target task. [GERBERA, 2024](https://arxiv.org/abs/2406.10671) demonstrates inconsistent gains from adding biomedical tasks. The [22-dataset ablation study](https://pubmed.ncbi.nlm.nih.gov/35413440/) also found that multitasking generally did not improve performance. SRU-NER itself reports an average in-corpus advantage of 0.82 percentage points for its single-task models despite stronger cross-corpus results.

   The [2026 loss-masking study](https://www.nature.com/articles/s41598-026-48856-x_reference.pdf) explicitly reports residual negative transfer, including BioNLP09 degradation from 90.02 to 69.24. Its description of test-set-based model selection also limits how strongly its numerical gains should influence this decision.

   SURUS changes source weights, gradient interactions, head capacity and example exposure. Its source-task F1 does not establish native-PICO improvement, calibration, or comparator-role precision. **The strongest conservative alternative remains retaining four sources.** I reject that alternative here because the amendment precedes every fit and can be bounded without result-driven selection—not because benefit is proven.

4. **Hidden failure modes, leakage and negative transfer**

   Four concrete problems require closure:

   - **Ontology corruption in the audit:** federation_surus_schema_audit.py::main keys class lookup and annotation counts by label name. The downloaded artifact collapses 25 IDs into 22 count keys and misassigns METHODOLOGY/PARAMETER DETERMINATION and PARAMETER BASELINE to RESULT. Do not build the head from that artifact’s labels array.
   - **Incomplete coordinate certification:** the same function checks start >= 0 and end > start, but not end <= text length, exact substring identity, token/character consistency or representability. Its PASS string is unconditional. Zero reported invalid coordinates is therefore insufficient.
   - **Incomplete exclusion machinery:** federation_per_fold_data_manifest_custody.py checks known held-fold aliases, defaults missing metadata to empty sets, and does not itself enforce the full protected registry or SURUS-OOD exclusions. Placing six unidentified native documents together does not exclude their aliases from auxiliary training.
   - **Implementation evidence is narrower than the claim:** TypedSpanHead.forward lacks explicit relative-position scoring; the D4 fixture does not exercise its auxiliary heads; federation_training_loop_resume.py uses TinyModel, not the scientific five-source data path.

   Alternative explanations for later improvement include changing old-source weights, general regularization, repeated exposure, source-specific boundary shortening and additional optimization work. Negative transfer may arise because SURUS rewards section-dependent, concise annotations that differ from native target conventions. High auxiliary performance could coexist with worse native precision. Potential abstract exposure during base-encoder pretraining must be distinguished from supervised label leakage; this review does not certify SURUS OOD as absent from pretraining.

   The paper’s reported partition annotation counts total **49,538**, versus **48,833** released rows. Record this 705-row discrepancy and establish release-specific counts; do not silently claim an identical paper dataset or invent its explanation.

5. **Exact accepted SURUS partition policy**

   - Candidate training membership is exactly Dataset == Indomain at commit 3a61790d5c304dea95fb278f76cc3b1a0ca07564: **400 candidates before exclusions**, not 400 guaranteed training documents.
   - All **90 indication-OOD + 33 study-type-OOD** records remain reserved. No training, source-weight choice, thresholding, stopping, architecture selection or interactive error inspection on them.
   - Freeze membership, exclusions and exposure status before fitting. No replacement sampling, split search or disease balancing.
   - Reserve the two OOD strata separately. Their later eligible evaluation populations may be smaller after provenance/exposure exclusions; publish that accounting rather than silently redefining 123.
   - An OOD family already exposed through native DESIGN, another inspected source, or a published/manual worked example cannot acquire “previously unseen” status by resealing. Quarantine it from any independence claim.

   **Accept the split with these qualifications.** Reservation preserves an auxiliary generalization check and is preferable for this bounded campaign to consuming all 523. It is not proven to maximize native-PICO accuracy and does not create fresh independent native-PICO gold.

6. **Exact admitted ontology and head definition**

   Source of truth: the pinned [label.csv](https://github.com/SURUS-AI/dataset/blob/3a61790d5c304dea95fb278f76cc3b1a0ca07564/data/dataset/label.csv) joined to label_class.csv. Primary key: (source_commit, released_LabelID); channels ordered by numeric ID 1–25. Store ClassID, class name and label name as checked metadata.

   The 25 channels are exactly:

   | Released IDs | Class and names, in ID order |
   |---|---|
   | 1 | DISEASE::INDICATION |
   | 2–7 | DRUG::{CLASS, DEVICE, FORMULATION, FUNDER, MOLECULE, TREATMENT_GROUP} |
   | 8 | ID::TRIAL |
   | 9–14 | METHODOLOGY::{DETERMINATION, INCLUSION_CRITERIA, OUTCOME, STUDY_DESIGN, STUDY_DURATION, STUDY_SIZE} |
   | 15–17 | PARAMETER::{BASELINE, DETERMINATION, EFFECT} |
   | 18–23 | RESULT::{BASELINE, DETERMINATION, SIGNIFICANCE, UNIT, VALUE, VARIABILITY} |
   | 24–25 | THERAPY::{DOSE_REGIME, METHOD_OF_ADMINISTRATION} |

   Use one separate 25-channel span head with the frozen 64-dimensional start/end projections, dropout 0.1, sqrt(64) scaling, legal contiguous pairs and source-scope masking. Restore the protocol’s explicit relative-position operation before re-certifying the shared span-head implementation; do not silently substitute the current plain dot product.

   No mapping of CLASS/placebo, TREATMENT_GROUP or any other SURUS type to native C; no shared-label softmax; no SURUS head at native inference. Retain the auxiliary weights in the immutable training checkpoint for any separately authorized later audit. Preserve exact duplicates once, distinct typed spans separately, and genuine overlap/nesting. No gold-dependent windowing, boundary snapping or span union.

   The annotation manual’s opening “26” conflicts with the released 25-ID table; the release governs this amendment. Its section-sensitive and repetition rules must remain source-specific. Title or other coverage not established by the release is masked, never assumed fully annotated. The manual was inspected, including its color-coded scope rules: :codex-file-citation{path="C:/Users/LENOVO/.codex/.chatgpt-projects/g-p-6abacc5b002881918cd1e6e0aa86ab70/surus_admission_review/evidence/SURUS_Annotation_Manual.pdf" purpose="source"}

7. **Exact fixed L_aux equation**

   Freeze **equal weight for each of the five sources**:

   \[
   L_{\mathrm{aux}}=\frac{L_{\mathrm{EBM}}+L_{\mathrm{TrialSieve}}+
   L_{\mathrm{EvidenceOutcomes}}+L_{\mathrm{PICO}}+L_{\mathrm{SURUS}}}{5},
   \qquad L=L_{\mathrm{native}}+0.25L_{\mathrm{aux}}.
   \]

   Each source coefficient is **0.05**. Each previous coefficient changes from 0.0625 to 0.05: a **20% relative reduction**, explicitly part of the amended intervention. Equal-source weighting prevents corpus size or channel count from directly determining source weight; it does not equalize gradient magnitude or claim optimality. Reject arbitrary new SURUS fractions, dynamic weighting and coefficient searches.

   Define each source loss as a document mean of the existing stable positive/negative log-sum-exp loss, averaged over that document’s fully annotated applicable classes. A fully annotated class with no positives remains a valid negative-supervision class. Unknown classes/scope contribute neither loss nor denominator. Require every positive to be representable and inside its valid mask; an empty source for any fold is STOP, not automatic renormalization.

   Preserve **eight auxiliary documents total per optimizer update**. With fixed source order EBM, TrialSieve, EvidenceOutcomes, PICO, SURUS, give every source one document and give the three cyclic sources t, t+1, t+2 modulo 5 one additional document. Thus batches rotate 2/2/2/1/1 and each source receives eight documents over five updates. Compute each source’s own mean before the equal five-source mean.

   Within sources, freeze label-independent document permutations using domain-separated hashes of protocol ID, fold, existing seed, source, cycle and canonical record ID; consume without replacement within each cycle. Preserve native schedules across paired arms, save all cursors/RNG state, and do not interpret batch eight as eight per source. D2/D3/D4 use identical source membership and schedules for matched fold/seed.

8. **Exact per-fold decontamination rule**

   Build a single identity graph under custody across SURUS, all approved source partitions, all protected/reserved partitions and the historical exposure registry. Include the **entire original EBM auxiliary train and reserved expert-test identities**, not only mapped R44 subsets. EvidenceOutcomes auditing must distinguish the admitted 500RCT stream from its 140EBM stream.

   Identity edges use exact PMID, normalized DOI, normalized title/abstract fingerprints and validated trial registry IDs; compute connected components to closure. Use a separate normalized identity view—never normalize stored scoring text. For additional conservative candidate detection, use NFKC/casefold/whitespace-normalized word five-gram Jaccard >= 0.90 or containment >= 0.95 with at least 20 shared five-grams. These thresholds trigger custody review/quarantine, not an asserted trial identity. Freeze them before any performance visibility. A shared trial identifier links a family only when it identifies the reported study, not a cited unrelated trial.

   **Precedence, fixed before fold processing:**

   1. Existing protected/forbidden families and unresolved suspicious matches exclude new training admission. Existing native DESIGN membership stays fixed; an OOD collision with DESIGN loses eligibility for an independence claim.
   2. Clean reserved SURUS-OOD families exclude their aliases from **every auxiliary training source**, not only SURUS.
   3. Any SURUS in-domain family colliding with native DESIGN, a reserved source test, or any previously approved auxiliary candidate family is removed from SURUS. Existing approved sources win over the new source. Do this globally before fold exclusions so an old source’s removal in one fold cannot re-admit its SURUS alias.
   4. For fold f, remove every held-out native family from every auxiliary stream. Preserve each retained source’s existing native annotation semantics; never combine annotations across sources into synthetic gold.

   Exact duplicate SURUS records have one canonical representative, chosen by numeric PMID then released ArticleID; distinct publications in one family share one family identity. Report documents and families separately. Missing PubMed responses are not evidence of independence. Identity comparisons must cover unresolved native/protected texts through a blinded custodian; irreducibly unresolved suspicious candidates remain excluded or the gate remains open. Absence of a registry ID alone is not proof of contamination and does not require rejecting an otherwise auditable record; report the residual limits of family matching.

   The known 6 EvidenceOutcomes and 2 PICO in-domain overlaps therefore lose SURUS eligibility. Reserved OOD aliases in EvidenceOutcomes/TrialSieve must be handled in the other streams too. Counts are set unions: **do not infer 392 retained cases by subtracting 6+2**. If a newly discovered family bridges existing native folds, STOP for explicit fold-protocol review; do not silently move records or shrink evaluation denominators.

9. **Exact fit budget and attempt-manifest consequence**

   Retain **45 scientific fits = D0–D4 × 3 folds × seeds 44/45/46**. D5 remains canceled without replacement. No SURUS-only, four-versus-five-source or seventh arm.

   Archive the old manifest and create a versioned successor retaining the same attempt identities and cancellation history. Bind every active slot to amended protocol, source release, ontology, admission/exclusion manifests, fold identities, adapter, loss/sampler, scientific code and qualified GPU/runtime hashes.

   Preserve the existing consumption rule: **a slot is consumed when its first scientific training job starts**, not after a successful optimizer update. Rebinding cannot reset a started slot. Current data-only and synthetic implementation preflights do not consume these slots.

   No existing scientific result is invalidated or consumed by this amendment. Existing mechanical preflights remain historical evidence but cease to certify the changed data path. D0/D1 retain native-only inputs. D2-vs-D0 and D3-vs-D1 remain fair tests of the **amended federation package**, not tests of SURUS’s isolated contribution. They are matched in native updates, not necessarily compute.

10. **Required new preflights before optimizer update**

   Mandatory closure, without protected scoring or scientific pilot fits:

   - **Schema/coordinates:** repair federation_surus_schema_audit.py::main to join/count by ID, verify class foreign keys, reject unknown/duplicate IDs, validate exact text/offset round trips and fail on violated invariants. Freeze per-partition/per-ID counts and explain or explicitly mark the paper/release count difference unresolved; do not fabricate equality.
   - **Adapter:** extend federation_adapters.py and federation_adapter_preflight.py with SURUS-native identity, source-specific scope, no-native-promotion and exact-boundary tests. Freeze the released coordinate origin and exact text serialization; do not guess a Title/Abstract concatenation. Verify Unicode, punctuation, repeated mentions, same-name/different-class labels, nesting and spans crossing windows. Any unrepresentable positive halts closure; no silent loss.
   - **Custody:** replace the limited admission logic in federation_surus_overlap_custody.py and federation_per_fold_data_manifest_custody.py with the exclusion union in item 8, including transitive aliases and unresolved-text checks. Freeze complete counts and reason-coded exclusions while keeping protected identities private.
   - **Architecture/loss:** update federation_architecture_preflight.py::AuxSpanHeads, TypedSpanHead.forward and multilabel_categorical_loss. Prove all 25 SURUS channels, actual D4 auxiliary integration, intended gradient routing, zero native-head supervision from auxiliary labels, applicable-class denominators and the exact weighted gradient calculation. Do not treat a missing positive masked away by pos & valid as success.
   - **Executable schedule/resume:** exercise the actual scientific data path with synthetic fixtures, not TinyModel alone; validate the 2/2/2/1/1 schedule, source means, unchanged native ordering, shared-component initialization and full interrupted/resumed state. Appending a head must not accidentally shift paired native initialization through RNG ordering.
   - **Resource/runtime:** qualify the real GPU with the amended shapes and masking/chunking behavior; bind deterministic settings, memory realization and checkpoint hashes. No hidden truncation, reduced effective batch or altered scientific schedule to fit memory.
   - **Manifest closure:** rebind AT0_EN_V26_FEDERATION_SOURCE_PIN_MANIFEST_V1.json, the versioned protocol, ontology/admission/fold manifests, runtime contract and AT0_EN_V26_FEDERATION_DEVELOPMENT_ATTEMPT_MANIFEST_V1.json; reconcile latest-state/handoff prose. Final independent prefit approval remains mandatory.

   These checks repair concrete defects or verify newly changed paths. They are not invitations to run comparative scientific experiments.

11. **What remains sealed**

   VERIFY_INTERNAL; AD/COVID protected texts/labels and external scoring; reserved original-EBM expert test; TrialSieve test; and SURUS OOD texts, labels and record-level errors remain inaccessible to development except existing authorized, isolated identity custody.

   R44C stays consumed. Previously exposed evidence stays exposed. Aggregate audit counts, published paper results and ontology metadata do not authorize record-level opening. Record this review’s access to the public paper/manual examples in the exposure ledger.

   SURUS OOD evaluation is **not authorized by this amendment**. Any later use requires a separately frozen evaluation population and deterministic scoring/checkpoint plan after model/procedure selection; it cannot feed back into this campaign.

12. **Claim boundaries**

   Allowed: “A prospectively amended five-source auxiliary federation was compared with native-only controls under matched native development folds and schedules.”

   Not allowed: “SURUS caused the gain,” “five sources are better than four,” “SURUS supplied new native comparator gold,” “123 newly independent PICO tests,” or “the source paper’s 0.95 predicts ACAD_PASS precision.” There is no matched no-SURUS federated arm.

   SURUS’s published IAA F1 is **token-level**; its NER score uses complete entity matches, but a different ontology and evaluation design. Neither certifies ACAD_PASS’s strict four-role task. [SURUS publication](https://link.springer.com/article/10.1186/s12874-025-02624-z).

   Maintain attribution, license link, revision and change notices for the [CC-BY-NC-4.0 release](https://github.com/SURUS-AI/dataset/blob/3a61790d5c304dea95fb278f76cc3b1a0ca07564/LICENSE). Noncommercial research admission does not establish unrestricted commercial deployment rights. The license permits qualifying redistribution; the project can nevertheless keep raw content out of public artifacts and publish provenance/aggregates instead. [Official license](https://creativecommons.org/licenses/by-nc/4.0/).

13. **Falsification criteria**

   **Admission failure:** unresolved ontology identity, unrecoverable positive spans, an unclosed protected-family path, empty admitted source, incompatible licensing purpose, or inability to execute the frozen loss/schedule. These prevent fitting; they do not justify tuning around the defect.

   **Scientific disconfirmation:** after all authorized outputs are frozen, report the prespecified paired native contrasts D2−D0 and D3−D1, by class and seed as well as pooled performance. If both contrasts are nonpositive, the prediction that this federation improves native extraction is unsupported in both matched architectures. Better auxiliary scores alongside worse native precision support the negative-transfer alternative. Failure of the existing precision/recall gates remains failure.

   **Identifiability limit:** neither success nor failure isolates SURUS’s marginal effect. A causal SURUS-only hypothesis cannot be conclusively tested by these 45 fits; a future independent ablation would require separate authorization. Do not add it now, invent a post-hoc rescue threshold, or treat folds/seeds as independent new clinical samples. The existing selector and its 0.005 tie policy remain unchanged.

14. **Whether a different corpus or design is superior**

   I found **no verified stronger drop-in human span corpus that warrants replacing SURUS or adding another source before this campaign**. This is a scoped research conclusion, not a claim of exhaustive nonexistence.

   - TrialSieve and EvidenceOutcomes are relevant human resources but are already represented; source duplication is not new evidence. [TrialSieve 2025](https://www.mdpi.com/2306-5354/12/5/486), [EvidenceOutcomes](https://pubmed.ncbi.nlm.nih.gov/40775953/).
   - FinePICO’s semi-supervised labels and revised-scheme experiments do not establish a fresh independent human-gold replacement. [FinePICO 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11833487/).
   - The 2026 JMIR PICO study reuses existing corpora; it does not release a new independent four-role span corpus. [JMIR 2026](https://www.jmir.org/2026/1/e91215).
   - The public MJ16 pharmacoeconomic dataset claims 250 expert-annotated records, but its documented output is structured fields rather than occurrence offsets, with one annotating expert and publication details pending. It is not an evidence-supported replacement for this span auxiliary task. [Dataset card](https://huggingface.co/datasets/MJ16/pharmacoeconomic-evidence-extraction-dataset).
   - General-domain auxiliary pretraining followed by target-only fine-tuning is a plausible GERBERA-style alternative, but introduces another training-stage choice. A 2026 validation-driven weighting controller explicitly uses feedback that conflicts with this campaign’s fixed-loss constraints. Neither is authorized here. [RouteB-v4](https://www.sciencedirect.com/science/article/pii/S1532046426000973).

   The smallest defensible intervention is the source-isolated admission above. Do not substitute a new encoder, verifier, optimizer, calibration fit or adaptive weighting method.

15. **Final GO/NO-GO for protocol amendment**

   **GO for the bounded protocol amendment; NO-GO for scientific execution today.**

   Required change: add the decontaminated in-domain SURUS task, reserve OOD with honest exposure accounting, freeze the five-source loss/sampler and repair/re-certify the affected implementation.

   Reason/expected benefit: additional human boundary/context supervision without changing native gold or adding scientific arms. New risks: negative transfer, 20% lower old-source weights, changed gradient/head interactions, reduced usable corpus after exclusions and noncommercial-use constraints.

   Historical results and consumed attempts remain intact. All 45 currently unstarted D0–D4 fits can still run prospectively after the new closure and final authorization. If the mandatory gates cannot close, STOP; do not improvise a subset, weight, arm or fallback fit.

16. **Exact next operation after this review**

   **PREPARE_AND_FREEZE_SURUS_ADMISSION_PROTOCOL_AMENDMENT_V2 — NO_SCIENTIFIC_FIT.**

   Prepare the exact amendment and its release/ontology/loss/sampler/exclusion specifications first; then perform the listed mechanical custody/adapter/runtime closure, bind the 45 slots, and submit the complete amended packet for **FINAL_INDEPENDENT_PREFIT_REVIEW**. No training begins merely because this admission review says GO.

   This consultation performed no model run, corpus sampling, protected benchmark opening, scoring, GitHub mutation or scientific attempt. Review findings and verified aggregate evidence are saved locally with a SHA256 manifest and a completion checkpoint.