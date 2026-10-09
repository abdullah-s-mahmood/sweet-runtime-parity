# ACAD_PASS — Limited SURUS Source-Contract Re-Review Packet V2

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `at0-en-v2.6-dev`

State:
`UPDATED_AFTER_INTERRUPTED_REVIEW_AND_V5_V6_V7 / NO_SCIENTIFIC_FIT`

Supersedes:
`AT0_EN_V26_SURUS_SOURCE_CONTRACT_REREVIEW_PACKET_V1.md`

## 1. Scope

This remains ONE bounded scientific-governance decision.

The original independent admission review already decided:
`PROCEED_SURUS_ADMISSION_WITH_CHANGES`

The question is NOT whether SURUS is generally useful.

The only unresolved question is:

> May the public release's Start/End character coordinates be prospectively frozen as the authoritative SURUS human-gold span boundaries under an explicit SURUS-specific representation contract, while TokenStart/TokenEnd and Annotation.Text are treated as non-authoritative provenance/consistency fields? Or must SURUS admission be rejected/paused because the exact original source-token/export semantics are not reproducible?

No scientific fitting is authorized by this packet.

## 2. Interrupted higher-model rereview

A higher-model rereview began but was interrupted by account usage limits before verdict.

The reviewer explicitly noted:
- high structural consistency does not itself prove the boundaries intended by the human annotators;
- the 99.6048% result measured WordPiece boundaries on raw text;
- it was checking whether this corresponds to the actual segment unit of the frozen implementation.

No final verdict was issued.

Durable evidence:
`AT0_EN_V26_SURUS_INTERRUPTED_SOURCE_CONTRACT_REVIEW_EVIDENCE_V1.md`

Do NOT infer approval or rejection from the interrupted session.

## 3. Frozen ACAD_PASS representation mechanics

Read:
`AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_V1.md`

and:
`federation_real_tokenizer_windowing.py`

The frozen mechanics preserve:
- original words/characters;
- source offsets;
- an original-to-model offset map.

Window planning:
- uses WordPiece budgets;
- rounds to complete SOURCE-WORD boundaries;
- cannot silently split/drop source words.

Representation:
- each source word is represented by the mean of its subword vectors.

Therefore:
`MODEL_WORDPIECE_BOUNDARY_ALIGNMENT != SOURCE_WORD_REPRESENTABILITY_CERTIFICATION`

This distinction must be explicitly addressed in the verdict.

## 4. Frozen SURUS release

Repository:
`surus-ai/dataset`

Commit:
`3a61790d5c304dea95fb278f76cc3b1a0ca07564`

Released:
- 523 articles;
- 48,833 annotations;
- 25 LabelIDs;
- Start;
- End;
- TokenStart;
- TokenEnd;
- Text.

The 25-ID ontology defect in the old audit has already been repaired.

## 5. Raw character/Text round-trip

Total:
`48,833`

Exact:
`Abstract[Start:End] == Annotation.Text`

for:
`44,643 = 91.4197%`

Mismatch:
`4,190 = 8.5803%`

Fixed punctuation/token-spacing diagnostic explains:
`3,060 / 4,190 = 73.0310%`

Residual Text-unexplained:
`1,130 / 48,833 = 2.3136%`

No row has been repaired, relocated, snapped or dropped.

## 6. Public-paper / code evidence

Peer-reviewed SURUS publication states:
- abstracts were tokenized using a BERT tokenizer;
- linked tokenizer/model reference is bert-base-uncased;
- BILOU labels were assigned to subword tokens;
- adjacent tokens were aggregated;
- complete NER matches require token start, token end and label.

The preprint/journal publication also said full NER model code would be made public.

Linked repository:
`https://github.com/surus-ai/dataset`

Complete accessible official history contains:
- dataset;
- annotation manual;
- README;
- images;
- license.

No training/tokenization/export/offset implementation is publicly present.

Therefore:
`ORIGINAL_TOKEN_INDEX_AND_EXPORT_IMPLEMENTATION_NOT_PUBLICLY_REPRODUCIBLE`

This is a reproducibility limitation, not proof that the released character coordinates are wrong.

## 7. V4 — frozen ACAD_PASS BiomedBERT tokenizer

Run:
`37915950311`

Artifact:
`11608843740`

Digest:
`sha256:bdd936769d8eaa4abe87d699925a950e4aa2d9aeff2cc1f327a869a57be8a081`

BiomedBERT WordPiece boundary alignment:
`48,640 / 48,833 = 99.6048%`

Released TokenStart/TokenEnd cannot be interpreted globally as those WordPiece indices.

## 8. V5 — source-paper bert-base-uncased WordPieces

Run:
`37919107413`

Artifact:
`11611123584`

Digest:
`sha256:2d43434d6ecbd33e270a423d4e29300cd75d970353bc5e782f32bdeeaf6da51f`

Pinned source-reconstruction tokenizer:
`google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`

This immutable revision predates the first public preprint; the paper itself did not pin a revision.

Start/End align to its WordPiece boundaries:
`48,719 / 48,833 = 99.7666%`

Eight fixed token-index conventions tested:
- 0/1 based;
- inclusive/exclusive;
- with/without special-token shift.

Best exact TokenStart/TokenEnd pair recovery:
`279 / 48,833`

Therefore:
`TOKENSTART_TOKENEND_ARE_NOT_DIRECT_BERT_BASE_UNCASED_WORDPIECE_INDICES`

## 9. V6 — source-unit reconstruction

Run:
`37919404071`

Artifact:
`11610764435`

Digest:
`sha256:0ec7e0dc73a1096b51d9702f9ffba69613b5d9ab47b91a2ea206e5c2e65fdb2e`

Fixed source-unit candidates:
1. bert-base-uncased BERT pre-tokenizer;
2. deterministic regex word+punctuation;
3. whitespace.

Character boundary alignment:

BERT pre-tokenizer:
`48,336 / 48,833 = 98.9822%`

Word+punctuation:
`48,483 / 48,833 = 99.2833%`

Whitespace:
`27,595 / 48,833 = 56.5089%`

Best absolute released token-pair recovery:

Word+punctuation:
`12,585 / 48,833 = 25.7715%`

BERT pre-tokenizer:
`12,155 / 48,833 = 24.8910%`

Thus:
`TOKENSTART_TOKENEND_ARE_NOT_GLOBAL_INDICES_OF_THE_TESTED_SOURCE_UNITS`

## 10. V7 — token-width and local-shift structure

Run:
`37919734516`

Artifact:
`11611114778`

Digest:
`sha256:fbedf6dbdb16c0d8bffca3a859a2f1db11fd4ae9834eeeb8e8c0c4212aef5970`

Released inclusive width:
`TokenEnd - TokenStart + 1`

matches char-derived source-unit span width for:

Word+punctuation:
`42,419 / 48,833 = 86.8654%`

BERT pre-tokenizer:
`42,242 / 48,833 = 86.5030%`

Exclusive width matches only ~2.3-2.5%.

Therefore:
`TOKENEND_IS_STRONGLY_MORE_COMPATIBLE_WITH_INCLUSIVE_WIDTH_SEMANTICS`

But absolute shifts are not stable.

Word+punctuation:
- single observed shift/article = 22;
- multiple shifts/article = 501.

BERT pre-tokenizer:
- single observed shift/article = 21;
- multiple shifts/article = 502.

Therefore:
`SIMPLE_GLOBAL_OR_PER_ARTICLE_LOCAL_OFFSET_HYPOTHESIS_REJECTED`

## 11. Combined evidence

Strong evidence FOR structural Start/End validity:
- all numeric offsets are in bounds;
- raw Text round-trip succeeds for 91.42%;
- most Text mismatches have a fixed punctuation/token-spacing mechanism;
- >99.6% align to BERT-family WordPiece boundaries;
- >99.2% align to a deterministic word+punctuation source segmentation;
- released token fields preserve inclusive span-width structure for ~86.9%.

Strong evidence AGAINST claiming full released source semantics are reproduced:
- 1,130 Text mismatches remain unexplained;
- TokenStart/TokenEnd absolute semantics cannot be reconstructed;
- public promised training/export code is absent from the linked repository;
- ACAD_PASS frozen span mechanics currently use source-word representations, not arbitrary raw WordPiece endpoints;
- 350 released char spans do not align to the deterministic word+punctuation source units;
- 497 do not align to BERT pre-token units.

## 12. Forbidden interpretations

Do NOT:
- relocate Start/End using TokenStart/TokenEnd;
- relocate Start/End by searching Annotation.Text;
- snap boundaries;
- drop rows merely because Text mismatches;
- choose a source tokenizer using downstream native performance;
- use protected benchmark results to decide the source contract;
- infer that 99.x% alignment proves annotator intent;
- infer that unrecoverable TokenStart/TokenEnd makes Start/End invalid.

## 13. Decision alternatives for independent review

### A — KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT

Possible only if the reviewer concludes that Start/End are sufficiently authoritative released human-gold anchors independently of unrecovered TokenStart/TokenEnd.

The reviewer MUST then specify:
- exact source-unit/representation contract;
- exact policy for character spans not exactly representable by that source unit;
- whether SURUS may use a source-specific auxiliary representation distinct from the word-mean mechanics;
- whether that constitutes an acceptable bounded amendment before any fit.

### B — KEEP_SURUS_WITH_OTHER_CHANGES

Use if a defensible bounded representation exists but differs from the candidate char-coordinate contract.

The reviewer must specify the exact rule prospectively.

No tuning/sweep/adaptive fallback is allowed.

### C — REJECT_OR_PAUSE_SURUS

Use if:
- the original source-unit semantics are scientifically necessary;
- the public release cannot certify them;
- or any required representation change would create excessive degrees of freedom or invalidate campaign comparability.

If rejected/paused:
- preserve all V1-V7 evidence;
- revert to the four-source federation path;
- resume GPU/runtime/final-prefit closure;
- no replacement auxiliary source is automatically authorized.

## 14. Questions requiring explicit answers

1. Is Start/End sufficiently authoritative to retain SURUS despite unrecovered absolute TokenStart/TokenEnd semantics?
2. Does 91.42% raw Text round-trip + systematic explanation of most mismatches support treating Text as provenance metadata rather than boundary authority?
3. Does the absence of promised public training/export code materially weaken source admissibility enough to reject?
4. Does the frozen ACAD_PASS word-representation architecture require exact recovery of the original SURUS source-token unit?
5. If not, what exact deterministic SURUS-specific representation is acceptable?
6. Is deterministic word+punctuation segmentation scientifically acceptable when 350 char spans do not align to it?
7. What exact fail-closed policy applies to those 350?
8. May a SURUS-specific auxiliary span head use model-token endpoints instead of source-word means, or would that create an unfair/material architecture change?
9. If model-token endpoints are allowed, how must D2/D3/D4 comparability be preserved?
10. Is document-level exclusion permitted if any positive is unrepresentable, or does the whole source fail?
11. Do the 1,130 unresolved Text mismatches require exclusion, quarantine flag only, or source rejection?
12. Should TokenStart/TokenEnd be ignored entirely in scientific training and retained only as provenance?
13. What exact claim boundaries must be added?
14. Final verdict:
    - KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT
    - KEEP_SURUS_WITH_OTHER_CHANGES
    - REJECT_OR_PAUSE_SURUS
15. Exact next NON-SCIENTIFIC operation.

## 15. Required review behavior

Perform:
- Deep Research;
- Adversarial Review;
- Alternative Hypotheses;
- Failure Analysis;
- Disconfirming Evidence Search;
- reproducibility audit;
- source-semantics audit;
- degrees-of-freedom audit;
- implementation-aware review.

Do NOT optimize for retaining SURUS.

Do NOT train a model.
Do NOT open VERIFY_INTERNAL.
Do NOT score AD/COVID.
Do NOT change the 45-fit ceiling.

## 16. Copy-ready continuation prompt

Continue the previously interrupted ACAD_PASS limited SURUS source-contract rereview.

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

Branch:
`at0-en-v2.6-dev`

The prior attempt was interrupted by the account usage limit BEFORE a verdict. Do not restart broad SURUS admission review and do not repeat already completed diagnostics.

Read first:
1. `ACAD_PASS_LATEST_STATE.md`
2. `ACAD_PASS_BOOTSTRAP_CONTRACT.md`
3. `phase2/academic_transform/at0_en/v2_6/FINAL_SURUS_ADMISSION_REVIEW_V1.md`
4. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_ADMISSION_PROTOCOL_AMENDMENT_V2.md`
5. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_INTERRUPTED_SOURCE_CONTRACT_REVIEW_EVIDENCE_V1.md`
6. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_PINNED_TOKEN_ALIGNMENT_DIAGNOSTIC_FREEZE_V4.md`
7. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_SOURCE_BERT_ALIGNMENT_DIAGNOSTIC_FREEZE_V5.md`
8. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_SOURCE_UNIT_DIAGNOSTIC_FREEZE_V6.md`
9. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_TOKEN_WIDTH_SHIFT_DIAGNOSTIC_FREEZE_V7.md`
10. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_SOURCE_CONTRACT_REREVIEW_PACKET_V2.md`

Your previously interrupted reasoning correctly raised that WordPiece-boundary alignment alone does not prove compatibility with the frozen implementation's source-word segment unit. That concern has now been investigated without scientific fitting.

New durable evidence:
- 48,833 annotations;
- raw Text round-trip 44,643 = 91.4197%;
- 3,060/4,190 raw Text mismatches explained by fixed punctuation/token-spacing;
- 1,130 Text mismatches remain unexplained;
- Start/End align to source-paper bert-base-uncased WordPiece boundaries in 48,719/48,833 = 99.7666%;
- released TokenStart/TokenEnd are NOT direct bert-base-uncased WordPiece indices: best exact recovery 279/48,833;
- Start/End align to deterministic word+punctuation boundaries in 48,483/48,833 = 99.2833%;
- released TokenStart/TokenEnd are NOT direct indices of BERT pre-token or regex word+punctuation units: best exact recovery 12,585/48,833;
- however inclusive released token-span WIDTH matches regex-derived span width in 42,419/48,833 = 86.8654%;
- token absolute shifts vary within 501/523 articles, rejecting a simple per-article local offset;
- public linked SURUS repository still lacks the promised model/tokenization/export implementation;
- frozen ACAD_PASS mechanics use original source words/characters and source-word representations, so this remaining distinction matters.

Perform Deep Research, Adversarial Review, Alternative Hypotheses, Failure Analysis, Disconfirming Evidence Search, reproducibility/source-semantics review and degrees-of-freedom audit.

Answer every question in Section 14 of V2.

Do NOT repeat V1-V7.
Do NOT train anything.
Do NOT open VERIFY_INTERNAL.
Do NOT score AD/COVID.
Do NOT change the 45-fit budget.
Do NOT repair/drop/relocate source spans.

End with exactly one verdict:
`KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT`
or
`KEEP_SURUS_WITH_OTHER_CHANGES`
or
`REJECT_OR_PAUSE_SURUS`

Then state the exact next non-scientific operation.
