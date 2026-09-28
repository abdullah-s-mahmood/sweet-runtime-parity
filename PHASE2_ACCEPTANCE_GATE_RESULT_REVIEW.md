# Phase 2 — Independent Candidate Acceptance Gate: Result Review

Date: 2026-09-28

Status: DEVELOPMENT gate executed successfully. Not sealed. No production acceptance policy frozen. Phase 3 not started.

## Canonical successful execution

GitHub Actions:
- workflow: Phase 2 Independent Candidate Acceptance Gate
- run: 36459266906
- conclusion: SUCCESS
- workflow source commit: 2b032bb6aaeb9a6e7bb5953746791302684fa6fd
- persisted evidence commit: 5d3f735ea322b9ce115da05ec1a675a372c1c6a4

Official Arabic-GEC upstream:
- CAMeL-Lab/arabic-gec
- pinned commit: 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Resolved public models:
- CAMeL-Lab/camelbert-msa-qalb14-ged-13 @ 447179dc63d186e4bff09a993e90e73ad622d571
- CAMeL-Lab/arabart-qalb14-gec-ged-13 @ 410588a318d988cdcfdbf64cf5745ed4adea0f6a

Runtime candidate population:
- 60 source-preserving NoPnx1 surgical edits
- 19 reversible-normalized recovery candidates
- 79 total candidate edits
- 37 source passages represented

Important anti-leakage property:
- runtime features and ACCEPT/REVIEW/REJECT decisions were materialized before loading prior human adjudication labels;
- Nahw target corrections/explanations were not runtime features.

## Integration issue encountered and resolved

The first workflow attempt exposed a reproducibility incompatibility between CAMeL Tools 1.4.1 and a newer unpinned cachetools release:
`AttributeError: 'LFUCache' object has no attribute '_LFUCache__links'`.

CAMeL Tools 1.4.1 did not pin cachetools in its historical setup metadata. The gate was repaired by explicitly pinning:
`cachetools==4.2.4`.

This was an environment/runtime compatibility failure, not a model-quality result.

## Main acceptance-policy results

### STRICT_CONSENSUS

Runtime-observable conditions:
- AraBART local base-form agreement;
- GED error probability >= 0.30;
- no deterministic hard veto;
- source-safe direction evidence (surgical source-local path, or normalized direct/morphology support).

Development result:
- accepted: 20/79
- supported: 20
- wrong: 0
- partial: 0
- unnecessary: 0
- HIGH/CRITICAL wrong accepted: 0
- supported precision: 20/20 = 100%
- supported coverage: 20/62 = 32.26% of all previously supported/alternative candidates
- accepted candidates span 17 passages
- stream composition: 17 surgical + 3 normalized
- operation composition: 18 INSERT + 2 REPLACE + 0 DELETE

This is the first tested runtime-only policy in the Arabic track that simultaneously:
- materializes decisions without gold/human labels;
- accepts no previously adjudicated wrong/partial/unnecessary candidate on this development population;
- retains materially more than the direct-patch-only normalized surface path.

However, the 100% figure is retrospective evaluation on the same development population and must not be interpreted as independent production precision.

### ARABART_BASE_AGREEMENT

- accepted: 40
- supported: 37
- wrong: 1
- partial: 2
- supported precision: 92.5%
- supported coverage: 59.68%
- HIGH/CRITICAL wrong accepted: 1

Conclusion:
AraBART agreement alone is not safe enough.

### ARABART_BASE_PLUS_GED

- accepted: 22
- supported: 21
- wrong: 0
- partial: 1
- supported precision: 95.45%
- supported coverage: 33.87%

Conclusion:
GED improves risk filtering, but one incomplete normalized candidate still passes. It remains evidence rather than proof.

### REVIEW_FIRST

- accepted: 36
- supported: 34
- wrong: 1
- partial: 1
- supported precision: 94.44%
- supported coverage: 54.84%
- HIGH/CRITICAL wrong accepted: 1

Conclusion:
exact/core agreement alone still allows a serious false acceptance.

## Known counterexamples

### Defective noun: correctly rejected

`وساعٍ → وساعا`

Evidence:
- SWEET normalized candidate is wrong.
- CAMeL morphology previously accepted/ranked the malformed direction.
- AraBART itself leaves the base as `وساع`, so base agreement does not rescue the SWEET candidate.
- deterministic veto `DEFECTIVE_NOUN_YAA_RESTORATION_RISK` rejects the candidate under every tested policy.

Required form in context:
`وساعيًا`.

This is a successful example of narrow linguistic veto + independent-model evidence outperforming morphology consensus alone.

### Imperative hamzat-al-wasl: useful but conservative

`إستشعِر → استشعر`

- AraBART independently agrees on the corrected base form.
- the prior normalized candidate is supported.
- GED marks the location UC with very low error probability.
- therefore STRICT_CONSENSUS routes it to REVIEW rather than ACCEPT.

This is a false negative for the strict policy and shows where explicit high-precision orthographic validators could recover coverage later.

### Partial case correction: correctly not accepted by strict policy

`باسمًا → باسم`

- AraBART agrees with the incomplete base direction.
- GED also supplies error evidence.
- the normalized candidate is only PARTIAL because nominative surface `باسمٌ` is still required.
- ARABART_BASE_PLUS_GED would accept it, but STRICT_CONSENSUS routes it to REVIEW because normalized source-safe surface evidence is absent.

This supports keeping candidate acceptance and surface realization as separate gates.

## Second-generator evidence beyond the known 79 candidates

AraBART generated 67 additional one-to-one aligned substitutions at source word locations not already represented by the 79 SWEET/normalized candidates:

- 67 rows
- 32 passages
- 23 rows overlap 23 published localized Nahw targets
- 44 rows do not overlap an extracted target and therefore cannot be called wrong from Nahw absence alone
- GED non-UC: 31
- GED UC: 36
- alignment cost <= 0.20: 45
- cost >0.20 to <=0.50: 17
- cost >0.50: 5

The raw examples are deliberately mixed:
- plausible useful corrections such as `وامتلئت → وامتلأت`, `يعرفوا → يعرفون`, `تمشِ → تمشي`;
- clearly concerning changes such as `الطلبة → الطلبه`, `الفاضلة → الفاضله`, and removal of hamzas from already correct words.

Therefore AraBART is promising as an independent candidate/evidence source, but its new edits must be adjudicated before any claim about incremental precision or coverage.

A dedicated queue has been persisted:
- `PHASE2_ARABART_EDIT_ADJUDICATION_QUEUE.jsonl`
- `PHASE2_ARABART_EDIT_ADJUDICATION_QUEUE_SUMMARY.json`

Scope limitation:
this queue covers one-to-one aligned substitutions. AraBART insertion/deletion/multiword alignment events still require a separate extractor before a complete second-generator quality estimate.

## Fresh end-of-gate research

### Generator + verifier is a validated GEC architecture

Sorokin (EMNLP 2022) explicitly separates edit generation from verification: a first model proposes edits and a second model classifies them as correct/false. This closely matches the component now emerging in this project.
Reference:
https://aclanthology.org/2022.emnlp-main.785/

### Edit-aware verification/ranking remains active research

Edit-Aware Reward Modeling (ACL 2026, Chinese GEC) reports gains from explicitly weighting and ranking edit tokens rather than relying on coarse sentence-level reward. This is not Arabic evidence, but it reinforces the architectural decision to make the verifier edit-centric.
Reference:
https://aclanthology.org/2026.acl-long.1900/

### Edit-level voting can reduce over-correction

Goto et al. (BEA 2026) report that edit-level majority voting over multiple generated candidates mitigates over-correction across nine non-Arabic GEC benchmarks. This supports multi-source edit agreement as one feature, not as an Arabic deployment guarantee.
Reference:
https://aclanthology.org/2026.bea-1.60/

### Arabic system combination is directly relevant

ArbESC+ (2025 preprint) combines AraT5, ByT5, mT5, AraBART, AraBART+Morph+GEC and text-editing outputs, then uses edit-selection features/classification. It reports improved QALB F0.5 over single models. The preprint status means it motivates testing, not immediate integration.
Reference:
https://arxiv.org/abs/2511.14230

### Public Arabic AraBART+Morph+GED reproduction is now proven in this project

CAMeL-Lab's public Arabic GEC stack documents contextual morphology preprocessing, GED tags and AraBART generation; the current workflow successfully reproduced this integration on all 41 project development passages.
References:
https://github.com/CAMeL-Lab/arabic-gec
https://aclanthology.org/2023.emnlp-main.396/

### Edit-centric evaluation should remain the default

UOT-ERRANT (TACL 2026) represents/aligns edits and offers interpretable edit transport rather than depending primarily on whole-sentence similarity.
Reference:
https://aclanthology.org/2026.tacl-1.77/

### Arabic grammar remains hard enough to justify selective abstention

Nahw (EACL 2026) reports substantial deficits in Arabic grammar knowledge/correction even for strong models. This supports the current precision-first ACCEPT/REVIEW/REJECT architecture.
Reference:
https://aclanthology.org/2026.eacl-long.296/

## Maximum-effort brainstorming after execution

### 1. STRICT_CONSENSUS
Decision: **KEEP AS LEADING DEVELOPMENT ACCEPTANCE POLICY**

Reason:
20/20 supported on already-adjudicated candidates with zero wrong/partial/unnecessary accepted, using runtime-only evidence.

Do not freeze yet because:
- same development population;
- only 20 accepted edits;
- new AraBART-only edits remain unadjudicated.

### 2. AraBART agreement alone
Decision: **DROP AS SOLE ACCEPTOR**

It accepted one HIGH/CRITICAL wrong candidate and two partial candidates.

### 3. GED
Decision: **KEEP AS SOFT/CONSENSUS FEATURE**

It improves selectivity when combined with AraBART but causes false negatives on valid hamza/orthographic edits. Do not restore hard GED gating globally.

### 4. Deterministic narrow grammar/orthography validators
Decision: **PROTOTYPE NEXT**

Potential high-value validators:
- hamzat al-waṣl/qaṭʿ in known morphological patterns;
- defective noun accusative yā restoration;
- five-verbs nūn retention/deletion;
- sound masculine plural case suffix;
- punctuation-structure preservation;
- base no-op rejection;
- tanween/case realization completeness.

Use them as veto/recovery rules only when linguistically narrow and auditable.

### 5. AraBART-only candidates
Decision: **ADJUDICATE NEXT**

They may materially raise recall, but the visible mix of useful and harmful edits makes automatic integration unjustified.

### 6. AraBART full-sentence output
Decision: **DROP**

Never accept it directly. Keep source-local aligned edits only.

### 7. Learned candidate verifier
Decision: **WATCH / PROTOTYPE ONLY AFTER DATA EXPANSION**

79 labeled candidates are too small and clustered to justify a serious learned verifier without overfitting.
A future verifier should be trained on a substantially larger disjoint edit dataset and validated passage-wise.

### 8. Edit-aware neural verifier
Decision: **HIGH-PRIORITY FUTURE PROTOTYPE**

Sorokin-style edit verification or a pairwise edit-aware scorer is more appropriate than a generic sentence classifier once sufficient labels exist.

### 9. Multi-model agreement
Decision: **INTEGRATE AS A FEATURE, NOT AN ORACLE**

SWEET–AraBART agreement is valuable but not sufficient. Add morphology, GED, deterministic vetoes, safety locks and abstention.

### 10. Strict Scientific mode
Decision: **INTEGRATE**

No linguistic ACCEPT can bypass:
- protected spans;
- citations;
- numbers/units;
- equations;
- p-values/CI;
- technical terms/entities;
- semantic equivalence verification.

### 11. Review-forward product UX
Decision: **INTEGRATE**

The architecture should treat REVIEW as a product state:
- show source edit;
- show candidate;
- show independent-model agreement;
- show error-type/morphology evidence;
- explain why auto-accept is withheld.

### 12. English transfer
Decision: **WATCH, then reuse architecture**

Once the Arabic acceptance architecture is frozen, the same generator→local-edit→verifier→surgical-apply framework should be applied to the English GEC track instead of assuming the earlier English results are sufficient.

## What improved

- a public independent Arabic seq2seq model family has now been executed successfully on the project development population;
- runtime decisions are demonstrably separated from human/gold labels;
- STRICT_CONSENSUS reaches 20/20 supported accepted candidates on the existing adjudicated pool;
- the known defective-noun failure is rejected without Nahw gold;
- candidate acceptance is now separated cleanly from morphology surface realization;
- a second-generator incremental-edit queue has been created for quality adjudication.

## What worsened / became clearer

- independent-model agreement alone still accepts a HIGH/CRITICAL wrong edit;
- STRICT_CONSENSUS coverage is only 32.26% of supported candidates;
- 67 new AraBART-only substitutions have unknown quality and visibly include both useful corrections and over-corrections;
- the current extractor does not yet include AraBART insertion/deletion/multiword events;
- development precision estimates remain based on the same 41 clustered passages and cannot justify production claims.

## Current interpretation

The gate has produced the strongest independent acceptance signal so far, but Phase 2 should not be frozen yet.

The next evidence need is narrow and explicit:

1. adjudicate the 67 AraBART-only substitutions;
2. quantify how many provide genuinely new supported target recoveries versus collateral over-corrections;
3. inspect target-overlap vs non-target quality without treating non-target edits as automatically wrong;
4. then decide whether STRICT_CONSENSUS remains the leading verifier or should be expanded with a small set of deterministic recovery validators;
5. separately extract AraBART insertion/deletion/multiword edit events before making a complete claim about second-generator behavior.

No sealed benchmark should be created until that evidence is closed.
