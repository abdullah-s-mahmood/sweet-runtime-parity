# ACAD_PASS ARABIC CORRECTION ARCHITECTURE RE-BASELINE V1

Date: 2026-10-01
Status: PRE-GOLD ARCHITECTURE REASSESSMENT
Scope: Arabic correction / MP-SEF redesign lane
Measurement status: NO NEW PROJECT GOLD / NO R_joint

## 1. Why this re-baseline exists

The current frozen MP-SEF cycle achieved a complete 22/22 source-only Second Preflight PASS, but its executable candidate space is asymmetric:

- P1 executable: 1,806 / 1,918 = 94.16%
- P1 protected-blocked: 112 / 1,918 = 5.84%
- P2 executable: 0 / 1,918 = 0%
- P2 execution/provenance failure: 1,918 / 1,918 = 100%

The P2 failure is a reproducible implementation/provenance defect in GED wordpiece-to-word alignment, not evidence of poor linguistic quality.

Because the current primary measurement would therefore be effectively P1-only, the Maximum-Quality Reassessment Contract requires architectural reassessment before spending additional gold-aware evaluation exposure.

## 2. Fresh external evidence considered

### ACL 2025: SWEET / text editing

Alhafni & Habash (ACL 2025), "Enhancing Text Editing for Grammatical Error Correction: Arabic as a Case Study", reports:

- Arabic text editing reaches SOTA on two benchmarks and is competitive on two others.
- Text-editing models are substantially faster than prior Arabic GEC systems.
- iterative correction improves MSA GEC up to two iterations;
- separating non-punctuation and punctuation correction improves MSA performance;
- the strongest text-editing cascade uses two NoPnx iterations followed by one punctuation iteration;
- heterogeneous ensembles improve performance further.

The paper's 3-model ensemble for QALB-2014/ZAEBUC combines:
1. Seq2Seq++;
2. SWEET2;
3. SWEET2_NoPnx followed by SWEET_Pnx.

The ensemble first aligns each model output back to the source, extracts proposed edits, then retains an edit only if at least k-1 of k models predict it.

This explicitly prioritizes precision over recall.

Published test F0.5:
- QALB-2014: 3-Ensemble 81.3; 4-Ensemble 81.7
- QALB-2015: 3-Ensemble 81.3; 4-Ensemble 82.9
- ZAEBUC: 3-Ensemble 85.9; 4-Ensemble 87.2

The paper also reports that SWEET/text editing is much faster than Seq2Seq++, while the ensemble is much heavier.

### EMNLP 2023: Arabic Seq2Seq + GED/morphology

Alhafni et al. (EMNLP 2023) shows that:
- Transformer-based Arabic Seq2Seq GEC is strong;
- GED auxiliary information improves GEC across three datasets;
- contextual morphological preprocessing helps;
- the architecture provides a strong complementary family to text editing.

The public CAMeL-Lab implementation exposes GED + AraBART GEC models.

Important local finding:
the frozen P2 wrapper did not preserve a valid word-level GED alignment when consuming subword predictions. The upstream repository contains a more rigorous word-level alignment implementation that should govern any P2_V2 repair.

### EACL 2026: Nahw

Mubarak et al. (EACL 2026) demonstrates that current LLMs still have substantial deficiencies in Arabic grammar understanding/detection/correction.

Therefore a general LLM should not become the sole primary correction engine or safety verifier merely because it is newer.

LLMs may remain:
- diagnostic;
- explanation-oriented;
- optional diversity candidates in a separately controlled lane;
- independent review aids.

## 3. Re-baseline alternatives

### Option A — KEEP current P1-only executable architecture

Advantages:
- already source-only legalizable;
- strongest methodological maturity;
- no new proposer engineering;
- minimum contamination/exposure risk.

Disadvantages:
- no proposer diversity;
- P2 contributes zero executable actions;
- candidate-coverage ceiling may be unnecessarily low;
- wastes evidence that heterogeneous ensembles can complement SWEET.

Decision:
DO NOT SELECT AS FINAL ARCHITECTURE YET.
Retain as frozen baseline/control.

### Option B — REPAIR P2 only

Repair:
- explicit wordpiece-to-word GED mapping;
- one GED label per morphology/source word;
- no silent zip truncation;
- exact GED coverage assertions;
- source-only generation traces;
- input/output truncation and EOS evidence;
- new P2_V2 hashes/version.

Advantages:
- root cause is known and highly repairable;
- restores architecture diversity: edit tagging + autoregressive Seq2Seq;
- based on published strong Arabic GEC architecture.

Disadvantages:
- older/heavier architecture than SWEET;
- repair alone does not prove complementarity;
- may still underperform or overlap heavily with P1.

Decision:
RECOMMENDED, BUT NOT AS THE ONLY REDESIGN.

### Option C — REPLACE P2 with another SWEET/text-editing variant

Candidate variants:
- SWEET2 iterative correction;
- SWEET Pnx;
- SWEET2_NoPnx + SWEET_Pnx cascade;
- alternate encoder/checkpoint from the published text-editing family.

Advantages:
- strong current published evidence;
- high speed;
- clean source anchoring and interpretable edit structure.

Disadvantages:
- less architectural diversity if P1 is itself SWEET NoPnx;
- correlated failure modes may reduce complementary coverage.

Decision:
RECOMMENDED AS AN ADDITIONAL CANDIDATE FAMILY, NOT A PURE P2 REPLACEMENT.

### Option D — ADD heterogeneous complementary proposer(s)

Proposed next-version candidate pool:

- P1_V2: current/frozen SWEET NoPnx family retained as baseline.
- P2_V2: repaired Seq2Seq++/AraBART + GED/morphology.
- P3_V1: strongest published SWEET iterative/cascaded variant.
- optional P4_DIAGNOSTIC: LLM/minimal-edit output, never automatically trusted and not required in primary architecture.

Advantages:
- maximizes diversity;
- mirrors published evidence that heterogeneous ensembles outperform single models;
- supports leave-one-proposer-out analysis;
- gives ACAD_PASS a path to measure complementarity instead of assuming it.

Disadvantages:
- more runtime and provenance work;
- more source-only legalizer complexity;
- consensus/edit fusion needs a new contract.

Decision:
STRONGLY RECOMMENDED FOR THE REDESIGN LANE.

### Option E — Adopt edit-level consensus as primary executable action

Published ensemble evidence uses source-aligned edit majority voting.

Potential ACAD_PASS adaptation:
- each proposer produces a frozen whole output;
- a source-only aligner derives proposer edits;
- only source-only legality/protection is allowed before gold;
- an edit is consensus-eligible only when supported by a preregistered number of independent proposer families;
- protected invariants remain fail-closed;
- consensus output is generated and frozen before gold.

Advantages:
- aligns with strong published ensemble evidence;
- may increase precision;
- may reduce unsupported edits.

Risks:
- previous MP-SEF V3 explicitly prohibited edit-level hybrid fusion in the current primary cycle;
- changing this now would create a new architecture, not a patch;
- edit independence and overlapping-edit semantics require rigorous contracts;
- correlated models must not count as independent evidence merely because they are distinct checkpoints.

Decision:
DO NOT MODIFY THE CURRENT FROZEN V3 CYCLE.
OPEN AS A NEW VERSIONED ARCHITECTURE EXPERIMENT (MP-SEF V4 candidate).

## 4. Current recommended architecture

### Frozen control lane

Preserve current V3:
- KEEP;
- P1_FINAL;
- current P2 remains EXECUTION_FAILED;
- 22/22 preflight PASS remains immutable evidence;
- do not consume new gold merely to finish the old cycle.

### New redesign lane

Build a source-only candidate-diversity study before any new gold-aware primary measurement.

Candidate systems:

1. SWEET NoPnx baseline / P1 family.
2. repaired Seq2Seq++ GED/morphology / P2_V2.
3. iterative/cascaded SWEET variant / P3_V1.
4. optionally one clearly different modern proposer if reproducible and license/runtime constraints permit.

For each proposer measure SOURCE-ONLY:
- execution success;
- truncation;
- output identity/change activity;
- protected-touch;
- exact duplicate-output overlap;
- pairwise edit/output diversity;
- candidate-set size;
- runtime;
- provenance completeness.

No linguistic correctness metric is allowed in this source-only diversity stage.

## 5. Decision on P2

P2 should NOT be abandoned.

The current frozen P2 artifact remains invalid for executability.

A new P2_V2 should be implemented because:
- the root cause is known;
- it is technically repairable;
- the underlying Seq2Seq+GED architecture has strong published Arabic GEC evidence;
- architectural diversity is scientifically valuable.

However, P2_V2 should be compared against adding a stronger contemporary SWEET variant rather than automatically restored as the sole second proposer.

## 6. Decision on LLMs

Do not promote a general LLM to sole primary proposer or verifier.

Reason:
- current Arabic grammar benchmarks still show substantial limitations;
- reproducibility, cost, model drift, and minimal-edit control are weaker than frozen open models.

Possible uses:
- diagnostic comparison;
- explanation;
- adversarial reviewer;
- optional fourth proposer only under a separate frozen/reproducible contract.

## 7. Proposed MP-SEF V4 research question

Source-only architecture question:

Can heterogeneous proposer families provide materially greater candidate diversity while preserving protected invariants and provenance, before any gold-aware correctness evaluation?

Later gold-aware question, only after source-only freeze:

Does a preregistered heterogeneous whole-action or consensus candidate set improve candidate availability and safe complete repair relative to the frozen P1-only control?

## 8. Required next steps

1. Create P2_V2 implementation specification from the upstream robust GED alignment path.
2. Create P3_V1 specification for the strongest reproducible SWEET iterative/cascaded variant.
3. Freeze a source-only proposer-diversity protocol.
4. Run only source-only smoke/parity/provenance tests.
5. Quantify duplicate vs complementary outputs without reference/gold.
6. Decide whole-action pool vs V4 consensus architecture based on source-only evidence.
7. Package this decision for independent higher-model review.
8. Only after independent review freeze the next measurement protocol.

## 9. Current classification

Versus the previous P1-only effective architecture:

IMPROVED STRATEGICALLY / PERFORMANCE NOT YET MEASURED.

The re-baseline expands the technically credible design space without weakening any scientific gate or overwriting frozen evidence.

Current confidence that the project can reach a strong scientifically defensible architecture:
HIGH qualitative engineering confidence.

No new R_joint, correctness, precision, recall, or safe-repair percentage is claimed here.

## 10. References

- Alhafni, B. & Habash, N. (2025). Enhancing Text Editing for Grammatical Error Correction: Arabic as a Case Study. ACL 2025.
- Alhafni, B., Inoue, G., Khairallah, C., & Habash, N. (2023). Advancements in Arabic Grammatical Error Detection and Correction: An Empirical Investigation. EMNLP 2023.
- Mubarak, H., Hawasly, M., & Mohamed, A. (2026). Nahw: A Comprehensive Benchmark of Arabic Grammar Understanding, Error Detection, Correction, and Explanation. EACL 2026.
- Luhtaru, A., Korotkova, E., & Fishel, M. (2024). No Error Left Behind: Multilingual Grammatical Error Correction with Pre-trained Translation Models. EACL 2024.
