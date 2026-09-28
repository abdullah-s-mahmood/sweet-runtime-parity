# Phase 2 — Selective Gate End Research + Brainstorming

Date: 2026-09-28

This document closes the mandatory end-of-gate research/brainstorming cycle. It does not freeze the architecture, create sealed data, or start Phase 3.

## Fresh end-of-gate research

### Arabic GEC / SWEET
SWEET remains a credible fast Arabic edit-tagging baseline and reports state-of-the-art or near-state-of-the-art results on Arabic GEC benchmarks, but our results show that raw final rendering is unsuitable for strict-fidelity academic editing. The best current role is candidate generation under source-preserving controls.
- ACL 2025: https://aclanthology.org/2025.acl-long.875/

### Arabic grammar remains intrinsically difficult
Nahw 2026 shows substantial deficits across grammar understanding, detection, correction and explanation, and reports that natural high-quality data can outperform synthetic fine-tuning. This reinforces the need for real human-corrected evaluation and narrow claims.
- EACL 2026: https://aclanthology.org/2026.eacl-long.296/

### A newer Arabic/English benchmark exists
ZAEBUC* (LREC 2026) provides bilingual written/spoken Arabic-English data with GEC and morphology-related benchmarking. It is a future external-validation candidate, but contamination/training overlap and licensing/provenance must be checked before it is considered for a sealed set.
- LREC 2026: https://aclanthology.org/2026.lrec-1.137/

### Arabic writing assistance is already a real product/research category
ARWI (2025) combines Arabic editing, grammatical error detection/correction and learner feedback, confirming that Arabic writing assistance has practical value. Our differentiation should therefore be strict academic/scientific fidelity, source preservation, risk-aware review and document integrity rather than merely “Arabic correction exists.”
- In2Writing 2025: https://aclanthology.org/2025.in2writing-1.2/

### Reference-based GEC evaluation can under-credit valid alternatives
Recent multilingual GEC evaluation work shows that standard reference matching can systematically mis-evaluate systems when multiple valid corrections exist. This supports continuing human/linguistic adjudication of supported alternatives rather than relying on exact match alone.
- ACL 2026: https://aclanthology.org/2026.acl-long.2193/

### Edit-representation evaluation continues to evolve
TACL 2026 proposes evaluation by optimally transporting edit representations. This is relevant to future metric design when multiple valid edits and boundary choices differ, but it is a WATCH item rather than a blocker for the current gate.
- TACL 2026: https://aclanthology.org/2026.tacl-1.77/

### Arabic GED remains research-supported
The EMNLP 2023 Arabic GED/GEC work reports gains from explicit GED information across multiple Arabic datasets and publishes public GED models. Our direct-source hard-gate experiment did not improve the current precision/coverage trade-off, but the original paper used contextual morphological preprocessing, so a faithful morph-preprocessed GED experiment remains a legitimate future test.
- EMNLP 2023: https://aclanthology.org/2023.emnlp-main.396/
- Repository: https://github.com/CAMeL-Lab/arabic-gec

## End-of-gate brainstorming

### A. Operation-aware NoPnx1 + surgical renderer
**INTEGRATE AS DEVELOPMENT REFERENCE**

Reason:
- 38 retained edits
- 37 supported under prior labels
- 0 prior wrong edits retained
- 12/12 scientific stress sources unchanged
- source-preserving by construction

Constraint:
- must undergo fresh selective-output adjudication before any freeze.

### B. Hard GED gate
**WATCH / DO NOT INTEGRATE**

Reason:
The direct-source GED gates reduce useful coverage without reducing the already-zero wrong-edit proxy.

Potential future role:
- review prioritization
- error localization explanation
- candidate ranking feature
- selective second-pass trigger

### C. Morph-preprocessed GED
**TEST**

Reason:
The published Arabic GED setup includes contextual morphological preprocessing. A faithful reproduction may produce better localization than the direct-source feasibility probe.

Do not use it as a production gate unless it demonstrates incremental value on held-out development evidence.

### D. Reversible normalized NoPnx model view
**PROTOTYPE — HIGH PRIORITY**

Reason:
98/98 previous tokenizer-UNK hazard words became tokenizable after reversible combining-mark/tatweel removal.

Required safety properties:
1. preserve exact original source bytes outside accepted edit span;
2. maintain normalized-to-source offset map;
3. never deliver normalized model text directly;
4. reject any edit that cannot round-trip exactly;
5. preserve scientific locks before normalization;
6. independently verify morphology/semantics before acceptance.

### E. DELETE edits
**ABSTAIN BY DEFAULT**

The current development evidence shows DELETE is much riskier than INSERT/REPLACE, including high-confidence destructive edits.

Future recovery path:
DELETE may be allowed only with independent validation, e.g.:
- explicit GED localization;
- morphology/grammar validation;
- paired punctuation structure check;
- scientific invariant check.

### F. INSERT operations
**TEST FOR HIGH-PRECISION AUTO-CANDIDATE ROLE**

Non-space INSERT edits were 18/18 supported in the prior development adjudication. This is promising but not sealed evidence.

### G. REPLACE operations
**TEST WITH OPERATION-SPECIFIC CALIBRATION**

A confidence threshold carries useful signal for REPLACE, but a single universal confidence threshold is not justified.

### H. Confidence calibration
**TEST, NOT FREEZE**

Use passage-clustered calibration and reliability curves by:
- operation family;
- error type;
- scientific/general mode;
- GED signal;
- protected-span proximity.

### I. NoPnx2
**TEST_SELECTIVELY**

Use only when an independent trigger predicts a likely unresolved correctable error. Do not run globally.

### J. Pnx
**TEST_SELECTIVELY FOR PUNCTUATION MODE**

Pnx remains unsuitable as an always-on strict proofreading stage because it adds review burden without target-recovery gain in the current development slice.

### K. Alternative Arabic GEC model
**TEST AFTER SELECTIVE ADJUDICATION**

Candidate families:
- AraBART/AraT5 Arabic GEC models from CAMeL-Lab;
- a current credible Arabic GEC model with reproducible provenance.

Use the identical:
- 41-passage development set;
- source-preserving edit application;
- protected scientific spans;
- target/collateral adjudication protocol.

The goal is not to replace SWEET automatically. The goal is to recover misses that SWEET cannot cover.

### L. Multi-candidate edit voting / quality ranker
**WATCH -> PROTOTYPE AFTER A SECOND STRONG CANDIDATE EXISTS**

If SWEET and a second Arabic GEC source independently propose compatible edits, edit-level agreement may improve precision and reduce over-correction.

### M. Strict Scientific Mode
**PROTOTYPE**

Policy should be stricter than general Arabic proofreading:
- quantities/units/citations/entities/equations/technical English locked;
- DELETE default deny;
- high-confidence is insufficient by itself;
- unsupported normalized mapping abstains;
- semantic verifier required.

### N. General Arabic Proofread Mode
**PROTOTYPE SEPARATELY**

Can permit broader linguistic edits but should still preserve original source outside approved edits and expose review provenance.

## Most important new conclusion

The architecture should no longer be framed as:

SWEET -> corrected text.

The evidence now supports:

Error signal(s)
-> NoPnx1 edit candidates
-> operation-aware selective gate
-> source-preserving surgical mapper
-> scientific locks
-> morphology/semantic validation
-> accept / review / abstain.

The next improvement opportunity is primarily **coverage recovery**, not further aggressive precision pruning.

## Immediate next gate

Before any additional architecture tuning, perform fresh adjudication of:

- PHASE2_SELECTIVE_ADJUDICATION_QUEUE.jsonl
- primary variant: op_aware
- secondary GED variants for comparison

The prior adjudication labels are intentionally omitted from the queue's Pass 1.

After this adjudication:
1. quantify true precision and target coverage of the selective output;
2. compare against prior surgical NoPnx1;
3. decide whether the operation-aware policy is frozen;
4. then prototype reversible normalized inference to recover coverage;
5. only after architecture freeze create an independent sealed Arabic evaluation set.

