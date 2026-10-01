# MP-SEF R_JOINT V4.2 DEVELOPMENT RESULT ANALYSIS V1

Date: 2026-10-02

## 1. Decision

**MEASUREMENT: CLOSE SUCCESSFULLY**

**CURRENT CANDIDATE ARCHITECTURE: MODIFY BEFORE SELECTOR TRAINING**

This decision does NOT invalidate the completed V4.2 measurement.
It means that the measured candidate roster is not sufficiently complete or clean to justify selector training as the next step.

No silent rerun of the consumed V4.2 experiment is authorized.

## 2. Evidence identity

Workflow run:
`36940844664`

Artifact:
`11200024879`

Artifact digest:
`sha256:10ecdb75b5d80540d2c9ddf5e94672e8d64bbe3eb685ca3f53d63789c3d308af`

Summary SHA256:
`5a649c5e050b34679e27958814201d49a948e039c38961032ced263bdacddc91`

Per-sentence SHA256:
`0e6c51435e978c1c917b9a37a361fad1a5fe4f65da6e18b17759ad2ecb67cc50`

Claim scope:
`DEVELOPMENT / ADAPTIVELY_CONSUMED / REFERENCE_RELATIVE / NOT_INDEPENDENT_GENERALIZATION`

Population:
- 1,918 UIDs
- 764 clusters

Reference states:
- PRIMARY_ERROR_PRESENT: 1,864
- ALL_REFERENCE_CLEAN: 48
- PUNCTUATION_ONLY_REFERENCE: 6

Frozen denominators:
- primary targets: 9,679
- punctuation targets: 129
- all reference targets: 9,808

## 3. Primary target recovery

Reference-relative candidate recovery bounds:

| Group | Lower | Upper |
|---|---:|---:|
| P1 | 66.8251% | 66.8664% |
| P2 | 58.6941% | 58.6941% |
| P3 | 51.1520% | 51.1933% |
| SWEET family | 66.9284% | 66.9697% |
| SEQ2SEQ family | 58.6941% | 58.6941% |
| ROSTER oracle diagnostic | 72.2285% | 72.2699% |

Important:
`ROSTER` is an oracle candidate-availability diagnostic, not an executable selector and not a deployable system score.

### Complementarity

ROSTER over SWEET:
- guaranteed target gain: at least 509 targets
- possible target gain: up to 517 targets
- gain: approximately +5.26 to +5.34 percentage points

ROSTER over SEQ2SEQ:
- guaranteed target gain: at least 1,310 targets
- possible target gain: up to 1,314 targets
- gain: approximately +13.53 to +13.58 percentage points

SWEET over P1:
- marginal target gain from the P3 same-family alternate: only 6 to 14 targets
- approximately +0.06 to +0.14 percentage points

Interpretation:
- P2 provides material independent-family complementarity and should be retained.
- P3 provides only a very small primary-target increment over P1 in the current consumed development evidence.

## 4. The 95% candidate-availability gate

Gate:
`ROSTER_PRIMARY_CANDIDATE_AVAILABILITY_GATE_95 = FAIL_CANDIDATE_AVAILABILITY`

Required targets at 95% of the frozen 9,679 denominator:
`9,196`

ROSTER upper numerator:
`6,995`

Deficit:
`2,201 targets`

Percentage-point deficit:
`22.7301 pp`

This is a structural candidate-generation deficit.

A selector cannot recover a reference-supported target that is absent from all available candidate actions.

Therefore:
**selector training must not be treated as the next primary repair for this roster.**

## 5. Whole-action cleanliness and overcorrection pressure

`PRIMARY_CLEAN_RECOVERY` means the best recovered primary targets from one complete action with:
`extra == 0`.

| Group | Clean recovery lower | Clean recovery upper |
|---|---:|---:|
| P1 | 22.3680% | 22.4093% |
| P2 | 3.6367% | 3.6367% |
| P3 | 0.7026% | 0.7439% |
| SWEET | 22.3680% | 22.4093% |
| SEQ2SEQ | 3.6367% | 3.6367% |
| ROSTER | 23.6491% | 23.6905% |

The large gap between:
- ROSTER primary recovery: ~72.23%
- ROSTER clean whole-action recovery: ~23.65%

shows that much of the current recoverable signal is entangled with reference-unsupported extra edits at whole-action level.

Because the evaluation uses finite references, `REFERENCE_UNSUPPORTED_EXTRA` is NOT equivalent to linguistically wrong.
However, it is sufficient to show that direct whole-sentence action selection cannot be assumed safe.

## 6. Complete repair

PRIMARY complete repair across 1,864 primary-error sentences:

| Group | Lower | Upper |
|---|---:|---:|
| P1 | 20.3326% | 20.3863% |
| P2 | 3.7017% | 3.7017% |
| P3 | 0.8047% | 0.8584% |
| SWEET | 20.3326% | 20.3863% |
| SEQ2SEQ | 3.7017% | 3.7017% |
| ROSTER | 21.8884% | 21.9421% |

ALL-REFERENCE complete repair across 1,870 non-clean-reference sentences:

ROSTER:
- lower: 21.1765%
- upper: 21.2299%

Interpretation:
candidate union improves target-level recoverability more than sentence-level complete clean repair.

## 7. Clean-reference activity

Among 48 ALL_REFERENCE_CLEAN sentences, the number with at least one non-KEEP candidate carrying reference-unsupported extra edits was:

- P1: 3 / 48 = 6.25%
- P2: 36 / 48 = 75.00%
- P3: 43 / 48 = 89.58%
- SWEET: 43 / 48 = 89.58%
- SEQ2SEQ: 36 / 48 = 75.00%
- ROSTER: 45 / 48 = 93.75%

This is candidate activity, NOT deployed false-positive rate.
No selector was trained.

Nevertheless, any future selector must prove a strong KEEP/abstention mechanism before deployment.

The clean-reference denominator is only 48 sentences, so no broad production-rate claim is permitted from this statistic alone.

## 8. Punctuation

Punctuation target recovery:
- P1: 31/129 = 24.03%
- P2: 23/129 = 17.83%
- P3: 22/129 = 17.05%
- SWEET: 33/129 = 25.58%
- ROSTER: 38/129 = 29.46%

The SWEET family adds only 2 punctuation targets over P1 under this reference projection.

P3 remains a same-family alternate and is not an independent vote.

## 9. Boundary route

Boundary route denominator:
23 targets = SPLIT + MERGE

SWEET:
18/23 = 78.26%

SEQ2SEQ:
14/23 = 60.87%

ROSTER:
18/23 = 78.26%

SWEET contributes 4 additional boundary-route targets across 4 clusters beyond SEQ2SEQ.
SEQ2SEQ contributes no additional boundary-route target beyond SWEET in this consumed evidence.

The denominator is very small, so this is diagnostic rather than a broad generalization claim.

## 10. Scoring failures

Recorded group-level scoring failures:
12

Unique affected UIDs:
2

The uncertainty induced by these failures is narrow:
ROSTER primary recovery interval spans only 4 targets.

The failure handling therefore preserved denominator continuity without materially changing the structural conclusion that the 95% availability gate fails.

## 11. Fresh post-result research / red-team

### ArbESC+ — Arabic edit-selection system combination

Alrehili & Alhothali, 2025.
`ArbESC+: Arabic Enhanced Edit Selection System Combination for Grammatical Error Correction`
arXiv:2511.14230.

Relevant implication:
Arabic GEC can benefit from multi-system combination and conflict-aware edit selection.

Our result supports the motivation for combination because P2 adds substantial independent-family recovery beyond SWEET.

But the current V4.2 result also shows that selector training alone cannot solve the 22.73 pp candidate-availability deficit.

### STAGEET — stage-wise typed edit tagging

Lou & Akef, 2026.
`STAGEET: Stage-wise Typed Edit Tagging for Grammatical Error Correction with Arabic as a Case Study`
arXiv:2608.28614.

Relevant implication:
typed/staged executable edits are a plausible direction for increasing locality and inspectability relative to selecting monolithic full-sentence outputs.

This is research motivation only.
STAGEET is NOT automatically authorized as a new proposer.

### JELV — limited-reference validity

Zhan et al., AAAI 2026.
`JELV: A Judge of Edit-Level Validity for Evaluation and Automated Reference Expansion in Grammatical Error Correction`
DOI: 10.1609/aaai.v40i41.40761.

Relevant implication:
reference-based evaluation can classify valid alternative edits as unsupported due to limited reference diversity.

Therefore this analysis never equates `REFERENCE_UNSUPPORTED_EXTRA` with linguistic wrongness.

JELV/LLM judging remains supplemental only and is NOT activated as a gold oracle.

### CLEME2.0

Ye et al., ACL 2025.
`CLEME2.0: Towards Interpretable Evaluation by Disentangling Edits for Grammatical Error Correction`
DOI: 10.18653/v1/2025.acl-long.10.

Relevant implication:
edit-disentangled evaluation supports investigating finer-grained correction behavior instead of relying only on whole-sentence candidate outcomes.

## 12. Architecture decisions after V4.2

### P1
**KEEP**

Reason:
- strongest current single proposer/family anchor;
- comparatively low candidate activity on the small clean-reference subset;
- substantial primary recovery.

### P2
**KEEP**

Reason:
- genuinely independent family;
- adds approximately 509–517 primary targets beyond the SWEET family in the current roster oracle;
- therefore provides material complementarity even though its standalone clean/complete metrics are weak.

### P3
**KEEP AS DIAGNOSTIC SAME-FAMILY ALTERNATE / DEFER AS PRIMARY PRODUCT ROUTE**

Reason:
- only 6–14 primary-target marginal gain beyond P1;
- only +2 punctuation targets beyond P1;
- high clean-reference candidate activity;
- not independent from P1.

Do not delete historical P3 evidence.

### Current whole-sentence ROSTER
**DO NOT TRAIN SELECTOR YET**

Reason:
- 95% candidate-availability gate fails by 2,201 targets / 22.73 pp;
- a selector cannot create absent candidates;
- clean whole-action recoverability remains only ~23.65%.

### P4 / third independent family
**REOPEN RESEARCH GATE, NOT GOLD EVALUATION**

The prior specific P4 candidate remains deferred until:
- training-data provenance is auditable;
- QALB overlap risk is resolved;
- exact checkpoint/config/tokenizer identity is frozen.

Current V4.2 gold results MUST NOT be used to repeatedly test/tune new proposers on the consumed C_F population.

### Candidate representation
**REPAIR / REDESIGN GATE**

Primary next research direction:
- decompose proposer outputs into provenance-preserving atomic edits;
- construct conflict components;
- keep full source/action ancestry;
- allow KEEP/abstain at edit/component level;
- prohibit arbitrary fusion;
- preserve protection constraints;
- investigate typed/staged edit representations.

This is a new architecture gate, not permission to implement immediately without a new source-only contract and preflight.

## 13. Evaluation-contamination boundary

C_F is now:
`ADAPTIVELY_CONSUMED DEVELOPMENT / NOT CLEAN HOLDOUT`

Therefore:
- no future architecture tuned from this result may claim independent validation on C_F;
- no repeated proposer search on C_F gold;
- no threshold optimization on C_F followed by reporting C_F as confirmation;
- a new untouched evaluation population must be frozen before future selector/architecture confirmation.

Candidate choices for a future untouched population require a separate provenance/overlap audit before selection.

## 14. Phase decision

### V4.2 measurement stage
**CLOSE**

The authorized experiment completed successfully and its evidence is frozen.

### Arabic candidate architecture
**MODIFY**

Reason:
- current union demonstrates useful family complementarity;
- but fails the candidate availability requirement by a large margin;
- whole-action cleanliness is too low to justify direct selector training;
- the next scientific bottleneck is candidate generation / representation, not selector optimization.

### Selector
**DEFER**

### Family consensus
**DEFER**

### Generic LLM judge
**DEFER AS PRIMARY / MAY REMAIN SUPPLEMENTAL RESEARCH ONLY**

### Immediate next phase gate

`POST-V4.2 CANDIDATE ARCHITECTURE REDESIGN GATE`

Required order:
1. preserve this consumed result as immutable;
2. source-only architecture brainstorming/red-team;
3. provenance audit for any proposed new family;
4. define edit-level representation/conflict contract;
5. define untouched future evaluation population before any gold-aware tuning;
6. source-free synthetic preflight;
7. independent review before opening any new reference set.
