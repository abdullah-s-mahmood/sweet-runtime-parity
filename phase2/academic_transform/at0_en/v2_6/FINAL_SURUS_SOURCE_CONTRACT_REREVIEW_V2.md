# ACAD_PASS — Final limited SURUS source-contract rereview V2

Review date: 2026-10-10 (Asia/Baghdad).

Verified active branch: **at0-en-v2.6-dev**, HEAD [f746136ccbe52d960206efeb68b5be8118f1c2d9](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/tree/f746136ccbe52d960206efeb68b5be8118f1c2d9). The latest durable state is V7, with P1 open and 45 scientific attempts unstarted. The interrupted review supplied no verdict.

I verified existing [V5](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/actions/runs/37919107413), [V6](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/actions/runs/37919404071), and [V7](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/actions/runs/37919734516): successful first attempts; downloaded aggregate ZIP hashes match the freezes; their embedded diagnostic-code hashes match the reviewed code. No diagnostic was repeated, no model ran, and no protected corpus or scoring was opened.

1. **Are Start/End sufficiently authoritative?**

   **Not sufficiently established for unconditional human-gold authority in this campaign.** They are the strongest released boundary candidates. However, structural alignment cannot resolve which field is authoritative when coordinates and Annotation.Text disagree. Independently, no examined representation preserves every released positive under the frozen mechanics. This is a bounded admission failure, not a finding that SURUS annotations are generally invalid.

2. **Can Annotation.Text become provenance metadata?**

   **Plausible, but not certified by these percentages.** Exact round-trip succeeds for 91.4197%; fixed spacing rules account for another 6.2667%; 2.3136% remains unexplained. The 3,060 explained rows are the union of several rules, not reproduction of one documented export process.

   The strongest benign explanation is display/token reconstruction. Local text-version changes, mixed export conventions, and some incorrect coordinates remain alternative explanations. Partial matches within every article do not exclude localized edits.

   Character-authoritative annotation is legitimate when documented: [brat](https://brat.nlplab.org/standoff.html) explicitly distinguishes offsets and reference text; [W3C](https://www.w3.org/TR/annotation-model/#text-position-selector) emphasizes binding positions to the correct resource representation. Neither establishes SURUS's CSV semantics. Reading Abstract[Start:End] establishes a selected slice, not independent verification of its intended boundary.

3. **Does missing public code require rejection?**

   **Not by itself.** The [official source](https://github.com/SURUS-AI/dataset/tree/3a61790d5c304dea95fb278f76cc3b1a0ca07564) and accessible history contain data, manual, images and license, but no training/export implementation. A release-specific schema or authoritative export description could suffice without recovering the original training system.

   Here, missing export semantics materially prevents resolution of conflicting fields. The [paper's BERT/BILOU description](https://pmc.ncbi.nlm.nih.gov/articles/PMC12315421/) concerns model processing and does not specify how the annotation platform produced these CSV coordinates.

4. **Must ACAD_PASS recover SURUS's original token unit?**

   **No.** It needs a deterministic, lossless mapping from authoritative source boundaries to its own representation. Original token indices are unnecessary if that mapping exists.

   The frozen [implementation](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/blob/f746136ccbe52d960206efeb68b5be8118f1c2d9/phase2/academic_transform/at0_en/v2_6/federation_real_tokenizer_windowing.py) tokenizes source words separately and plans complete-word windows. V4/V5 tested whole-abstract WordPiece offsets. Their alignment percentages cannot certify that different path.

5. **What exact deterministic representation is acceptable?**

   The smallest word-based candidate is the V6 rule: Python Unicode **\w+|[^\w\s]** matches over the unchanged Abstract, with each match retaining its original half-open character offsets. Tokenize each unit using the pinned encoder tokenizer; retain the existing word-mean, complete-word window and explicit-UNK policies.

   Admit a positive only if its exact start and end map to unit boundaries, round-trip unchanged, and remain in the applicable annotation mask. Segmentation and windows must not consult labels or gold boundaries. Pin text bytes, Unicode/runtime semantics and tokenizer files. This candidate is precisely specified but **fails the existing evidence; it is not approved for SURUS admission**. No alternative character grid or gold-induced splitting is authorized.

6. **Is word-plus-punctuation segmentation acceptable with 350 unaligned spans?**

   **Not as a complete adapter for this release.** Its 99.2833% coverage leaves 350 positives outside its endpoint space. Keeping their coordinates in metadata while training on covering tokens would change the supervised boundaries.

   These counts concern the full 523-record release. They do not establish how many survive the independent training-admission exclusions. Do not call them 350 erroneous annotations or 350 eligible training failures.

7. **Exact fail-closed policy for those 350?**

   Preserve the original rows and record UNREPRESENTABLE_UNDER_REGEX_UNIT in audit custody. No snapping, splitting from gold, relocation, conversion to negatives, or removal from the loss denominator to obtain PASS. If any otherwise-admitted positive is unrepresentable, adapter closure fails. The current all-positive closure remains unestablished; retain P1_NOT_CLOSED.

8. **May SURUS use model-token endpoints?**

   **Not authorized in this campaign on current evidence.** Such a head is possible in principle, but changes candidate pairs, position units and auxiliary gradients. It is a scientific representation amendment.

   It also does not solve the observed coverage problem: V4 leaves **193** spans unaligned to BiomedBERT; V5 leaves **114** unaligned to a different, reconstruction-only BERT tokenizer. D4 compatibility is not certified. Choosing the tokenizer with the best diagnostic percentage or introducing character endpoints solely to retain SURUS would add unjustified flexibility.

9. **How would D2/D3/D4 comparability have to be preserved?**

   For any separately reviewed future amendment: identical source membership, unchanged character gold and scope, document schedules, source weights, head form, class denominators and update counts; identical SURUS machinery in D2/D3. D4 must preserve the same character-level task and explicit candidate-support contract despite its different encoder. Model-dependent positive dropping is forbidden.

   Encoder-specific candidate spaces would make D4 a combined encoder/representation intervention and require that qualified claim. No such amendment or additional fit is authorized here.

10. **May documents with unrepresentable positives be excluded?**

    **No representability-driven exclusion is authorized.** It selects a population according to annotation boundaries and may selectively remove difficult structures or labels. Existing independently justified custody/dedup exclusions remain valid; they must not be expanded into a mechanism for selecting an easier SURUS subset.

    Under the frozen every-positive rule, an unresolved admitted positive blocks the source adapter. It need not block the already-authorized four-source alternative.

11. **Policy for the 1,130 unresolved Text mismatches?**

    Preserve them unchanged with a provenance flag, and **pause the entire SURUS admission**. Flagging alone does not authorize their training use. Do not exclude the 1,130 or train only the remaining rows.

    Their overlap with the 350, 193 and 114 alignment failures is not established; do not sum these counts. Nor is 2.3136% an estimated human annotation error rate.

12. **Policy for TokenStart/TokenEnd?**

    Retain verbatim as provenance, excluded from scientific target construction, relocation, windowing and loss. Their unrecovered semantics do not prove Start/End invalid.

    V7 supports inclusive-width compatibility under the tested units; it does not recover a historical tokenization. Its multiple-shift result rejects a single constant article offset for those tested segmentations, not every possible annotation-platform or local-index mechanism.

13. **Required claim boundaries and reopening condition**

    Allowed: “The pinned release has highly coherent character coordinates, with unresolved text/export semantics and incomplete certification against the intended representation.”

    Disallow claims of fully reproduced original SURUS tokenization, validated human-boundary accuracy of 99.x%, or equivalence to the paper's evaluation. The paper's Figure 1 itself reports **48,833**, while its partition counts sum to **49,538**: retain the 705 discrepancy as an internal publication/release inconsistency, not proof of missing release rows. [SURUS paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12315421/)

    Reopening needs materially new source evidence identifying the authoritative field, exact text serialization and offset convention, plus a prospectively specified lossless representation for every admitted positive. More ungrounded tokenizer/convention searches are not the next step. A published schema/export clarification could satisfy the source-semantics part without full training code. No retrospective four-versus-five-source comparison is authorized.

14. **Final verdict**

    **REJECT_OR_PAUSE_SURUS**

    Pause SURUS admission for the current campaign and take the V2 packet's four-source fallback. The joint source-authority and representation conditions remain open. No completed scientific evidence is invalidated or consumed.

15. **Exact next non-scientific operation**

    **FREEZE_SURUS_PAUSE_AND_REBIND_ORIGINAL_FOUR_SOURCE_PREFIT_MANIFESTS**

    Freeze this verdict and V1–V7 evidence; record a versioned four-source reversion without deleting the five-source amendment. Restore the original four auxiliary sources, their equal-source loss (0.0625 each within total auxiliary coefficient 0.25), and eight auxiliary documents total. Rebind protocol, data, sampler, runtime and the same 45 unconsumed attempt identities; preserve D5 cancellation, known contamination exclusions and protected reservations. Do not automatically re-admit previously excluded aliases.

    Update the durable latest-state/handoff/progress records, then resume outstanding GPU/runtime and final pre-fit closure for that four-source path. **STOP before the first scientific job until the independent final pre-fit gate passes.** No SURUS adapter, replacement source, diagnostic rerun, training, VERIFY_INTERNAL access, AD/COVID scoring or budget increase is authorized by this review.
