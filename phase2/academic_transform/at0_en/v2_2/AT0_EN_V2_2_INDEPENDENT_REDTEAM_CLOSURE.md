# AT0-EN V2.2 — Independent Red-Team Closure

Date: 2026-10-03
Status: **RED-TEAM COMPLETE / CONTRACT NEEDS ONE MORE OFFLINE GENERALIZATION GATE**
New model inference during red-team: **NONE**

## 1. Scope

This review independently challenged the frozen V2.2 offline validator after the first V2.2 replay. It used only:
- the already-consumed AT0-EN V2.1 artifact from run `37123963805`;
- the 12 frozen synthetic English cases;
- deterministic mutation tests;
- higher-model semantic red-team review;
- fresh literature review.

No V2.1 cell was regenerated or replaced.

## 2. Why the first V2.2 result was not accepted at face value

The first V2.2 replay reported:
- PASS_CANDIDATE 32
- REJECT 3
- REVIEW 8
- REVIEW_ESCALATED 1
- UNAVAILABLE 4

Independent inspection of the 32 PASS_CANDIDATE outputs found false negatives. The validator was therefore hardened before any future-live authorization.

## 3. False negatives discovered by red-team

### EN03 mechanism conflation
A MODEL_B PLANNED output stated that Studies A-D reported findings about the “impact of edge aggregation on latency and energy consumption,” even though Studies C/D concern message batching.

Disposition after repair: **REJECT**.

### EN04 claim-strength change
A MODEL_A DIRECT output changed:
- source: adaptive signal timing **reduced** mean queue length;
- output: signal timing **was associated with a reduction**.

The direction is conservative but the scientific relation is not identical.

Disposition after repair: **REJECT**.

### EN01 modality strengthening
A MODEL_A DIRECT output changed:
- source: continuous observations **can support** faster congestion identification;
- output: observations **facilitate** faster identification.

The source modal limitation was removed.

Disposition after repair: **REJECT**.

### EN08 scope-of-negation broadening
Two MODEL_A outputs changed a specific statement that the experiment did not establish a causal effect in other networks into a broader statement that the findings did not allow generalization to other networks.

Disposition after repair: **REVIEW**, not automatic rejection.

### EN09 inferred weight stability
A MODEL_A PLANNED output added that weights “remain constant throughout the scheduling process,” while the source explicitly says only that weights are fixed before the run.

Disposition after repair: **REVIEW**.

## 4. Final regression suite

Final validator regression suite:
- 12 frozen source self-checks
- 19 adversarial mutations
- total: **31/31 PASS**

New adversarial classes added by red-team:
- modal strengthening
- study/mechanism conflation
- direct-effect to association weakening
- blanket generalization restriction
- causal-plus-blanket restriction
- inferred throughout-run parameter stability

Final local SHA-256 identities:
- validator: `8a2f044b81affe9a606a7692d9c12655b6f5e214c4c17a04a7daf2be7f3ee2f9`
- regression test: `dbf387a5450b3614e4519cfd67b2745675c38874666e43a85c17870a17029648`
- final red-team replay JSONL: `edc83ca938aa185739441e45ce01d44e6a38fd49ce7cfab606228acf50036bff`
- final red-team summary: `a323761e5c1ebf23fa8940b6d69ec49b46ec441cf01cc96572eb4aa53ab7ab37`

Repository hardening commits:
- validator red-team hardening: `76dcb642733ed8dcfa019b2f886cfd6fe6a563cb`
- expanded regression suite: `fdd187f94f048de6538e4233357f38ee1086c5ff`

## 5. Final frozen replay after red-team

Across the original 48 V2.1 slots:

- PASS_CANDIDATE: **26**
- REJECT: **7**
- REVIEW: **10**
- REVIEW_ESCALATED: **1**
- UNAVAILABLE: **4**

This supersedes the preliminary 32/3/8/1/4 V2.2 diagnostic counts.

Interpretation:
- 26 PASS_CANDIDATE means no violation was found by the bounded synthetic-case validator.
- It does **not** mean general scientific fidelity is established.
- REVIEW is a deliberate uncertainty state, not a failure accusation.
- REJECT indicates a concrete mismatch against the frozen source contract.
- UNAVAILABLE means no deterministic final text was available for this offline replay.

## 6. False-positive red-team

No current **REJECT** was judged an obvious false positive after semantic inspection.

The REVIEW pool intentionally includes borderline cases such as:
- “performance increased” when elapsed time increased;
- “crucial” versus the source’s “important”;
- “efficiency” inferred from travel-distance/overflow metrics;
- explicit throughout-run weight stability inferred from pre-run fixed weights;
- broader non-generalizability language;
- stronger attribution language.

These should remain REVIEW until a stronger independent semantic verifier or qualified human judgment resolves them. The purpose of REVIEW is to prevent uncertainty from becoming automatic approval.

## 7. Fresh research challenge

### Scientific text revision evaluation
Jourdan et al., ACL 2025, *Identifying Reliable Evaluation Metrics for Scientific Text Revision*:
https://aclanthology.org/2025.acl-long.335/

The paper reports that LLM-based evaluation is effective for instruction following but weaker for correctness, and that hybrid task-specific evaluation better aligns with human judgments. This supports retaining domain/relation checks and later human assessment rather than a single model judge.

### Claim-evidence reasoning
CLAIM-BENCH / IJCNLP-AACL 2025:
https://aclanthology.org/2025.ijcnlp-long.127/

The study reports persistent difficulty in linking scientific claims and evidence, with multi-pass or one-by-one approaches improving performance at additional cost. This supports decomposed relation verification but also argues against treating one verifier as an oracle.

### Grounded scientific critique
CLAIMCHECK / Findings of EMNLP 2025:
https://aclanthology.org/2025.findings-emnlp.1185/

Its motivation and expert annotations reinforce that plausible scientific language is not enough; critiques/assessments must be grounded in the paper’s actual claims.

### Structured output
Chavan, 2026, *Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap*:
https://arxiv.org/abs/2609.23742

The reported separation between schema validity and semantic correctness strongly supports V2.2’s decision not to use structured-output success as scientific-safety evidence.

StructureBench, IJCAI 2026:
https://www.ijcai.org/proceedings/2026/267

This benchmark likewise evaluates structural validity and semantic correctness separately and reports that constrained decoding can guarantee form without reliably improving semantic accuracy, especially in smaller models.

## 8. What improved and what worsened

### IMPROVED
- five additional semantic failure modes were discovered before any new live experiment;
- PASS_CANDIDATE false negatives were reduced;
- regression coverage expanded from 25, then 27/30, to **31** frozen checks;
- no REJECT currently appears to be an obvious false positive;
- uncertainty is explicitly retained in REVIEW rather than optimized away.

### WORSENED / exposed risk
- PASS_CANDIDATE fell from 32 to **26**, demonstrating that the initial validator was over-permissive;
- the validator remains heavily case-specific and regex-driven;
- passing 31/31 tests cannot establish generalization because the tests were derived from only 12 synthetic cases;
- iterative patching risks overfitting the validator to observed V2.1 outputs.

Overall classification:
**IMPROVED SCIENTIFICALLY / MIXED ENGINEERING GENERALIZABILITY**

## 9. Higher-model decision

**DO NOT authorize a new live inference experiment yet.**

The red-team demonstrates that another live run would be premature because the current safety layer can still improve simply by adding case-specific rules after observing outputs.

The next phase is authorized as:

# AT0-EN V2.3 — OFFLINE SCIENTIFIC CONSTRAINT GENERALIZATION GATE

V2.3 must not tune against individual V2.1 outputs. It should replace case-specific acceptance logic with a declarative scientific-constraint representation and generic validator classes.

Required V2.3 work:
1. define a versioned `ScientificConstraintGraph` schema;
2. encode each frozen case declaratively using claim/relation nodes rather than case-id-specific validation branches;
3. distinguish deterministic invariants from semantic constraints requiring REVIEW;
4. implement generic validators for:
   - exact quantities/units;
   - entity/value/time/baseline bindings;
   - citation-to-claim bindings;
   - negation/modality;
   - causal/association relation type;
   - scope/population restrictions;
   - comparison direction;
   - equation/symbol/definition bindings;
   - method order/exclusion constraints;
5. generate adversarial mutations from the constraint graph itself where possible, rather than hand-writing one mutation per observed failure;
6. rerun the frozen V2.1 artifact offline only;
7. compare V2.2 versus V2.3 dispositions and explain every change;
8. freeze the V2.3 validator and red-team before higher-model review.

Do not use a generic LLM judge as the approval oracle.

No new model inference, HW1-EN, detector robustness, DOCX work, Arabic resumption, reserved-data opening, or paid launch is authorized by this closure.
