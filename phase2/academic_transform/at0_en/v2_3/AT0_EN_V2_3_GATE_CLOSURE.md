# AT0-EN V2.3 — Scientific Constraint Generalization Gate

Date: 2026-10-03
Status: **OFFLINE GATE CLOSED / DEVELOPMENT EVIDENCE ONLY**
New backend model inference: **NONE**

## 1. Objective

V2.3 addresses the main weakness exposed by the V2.2 independent red-team: scientific preservation logic must not live in case-id-specific code branches.

The validator is now graph-driven:
- case-specific scientific constraints live in a declarative `ScientificConstraintGraph`;
- one generic validator evaluates every case;
- the validator code contains no `if case_id == ...` scientific logic.

Graph:
`phase2/academic_transform/at0_en/v2_3/SCIENTIFIC_CONSTRAINT_GRAPH_V0_1.json`

Generic validator:
`phase2/academic_transform/at0_en/v2_3/at0_v2_3_graph_validator.py`

Repository commits:
- graph: `315958e469449a694beb2956b0feaf249245c28d`
- validator: `3d626a41c080345c5c01e7a90b0fabfae3c25b2c`

## 2. Frozen local identities

- final graph SHA-256:
  `840a94f067e44c852c92e5727345594877f96886e5889d5a24aaaa6ba444443f`
- generic validator SHA-256:
  `afee3852a1430d66990480b63623114682d0d79ef7f9aa0c2959315d52e1d2ef`
- 31-case regression runner SHA-256:
  `e8f4b04f81fcbb8f986f02963afc20bbdc48643f8a52f45582e329316287131d`
- V2.3 replay JSONL SHA-256:
  `917ad5eb60cb29ba44ad5f68e41bd634282cfb1c880e24bfeefb20acb4593ecf`

## 3. Behavioral equivalence to red-teamed V2.2

The graph-driven V2.3 validator was replayed over the exact frozen V2.1 evidence.

Final disposition:
- PASS_CANDIDATE: **26**
- REJECT: **7**
- REVIEW: **10**
- REVIEW_ESCALATED: **1**
- UNAVAILABLE: **4**

This is exactly identical, slot-by-slot, to the final red-teamed V2.2 result.

Therefore moving constraints from case-specific code to the graph changed representation, not outcome.

## 4. Regression suite

The V2.3 generic validator passed the full V2.2 red-team regression suite:

- 12/12 frozen source self-checks
- 19/19 adversarial mutations
- total: **31/31 PASS**

The suite includes scope, modality, quantity, citation, causality, mechanism conflation, group/value binding, method seed, definition binding, generalization scope, equation semantics, imputation, duplicate policy and retuning mutations.

## 5. New counterfactual holdouts

The purpose of the holdouts was to test unseen failure forms rather than only replay known red-team mutations.

### Holdout 1 — initial V2.3 graph
Result: **10/12 caught**

Missed:
1. EN04: roadside-unit density direction changed from reduced to increased.
2. EN09: equation operator changed from `+` to `-`.

Repairs:
- explicit density-direction binding;
- exact equation/operator identity.

The original 10/12 failure remains part of the evidence and is not erased.

### Holdout 2 — after first repair
Result before repair: **11/12 caught**

Missed:
- EN08 direction inversion:
  lower channel occupancy → lower delivery ratio.

Repair:
- explicit direction constraint for the occupancy/delivery relationship.

A first strict direction encoding caused a false positive on a semantically equivalent phrase:
“negative association between channel occupancy and delivery ratio.”

The constraint was therefore broadened to accept both equivalent representations while still rejecting the inverted relationship.

### Holdout 3 — fresh confirmation after repairs
Result: **12/12 caught**

New mutations covered:
- real-time → once/day monitoring;
- travel distance → fuel consumption;
- Study A lower → higher latency;
- packet loss increased → decreased;
- shorter → longer discovery time;
- 49.8 s → 59.8 s;
- pre-fixed → tuned parameters;
- delivery-ratio direction reversal;
- D_i definition corruption;
- removal of timestamp;
- duplicate-report acceptance;
- reliability metric replacement.

Holdout 3 JSON SHA-256:
`e51e0fe68d9afc990e3f37143d9994ffc5a9b4a89d267eae8eca2185a3336d70`

## 6. Scientific interpretation

### Improved

V2.3 demonstrates:
- case-specific validation branches are not required for the current 12-case development set;
- constraints can be represented declaratively and evaluated by a common engine;
- the same engine detects multiple unseen counterfactual mutations after graph hardening;
- equivalent scientific wording can be explicitly represented without weakening direction checks;
- historical failures remain visible.

### Remaining limitation

The graph is still authored from only 12 synthetic cases.

Therefore:
- 31/31 regression success is not a generalization claim;
- 12/12 final holdout success is not a universal scientific-fidelity claim;
- regex/lexical realization is still language-specific evidence;
- graph creation itself is currently manual and requires trusted source interpretation;
- these 12 cases and their V2.1 outputs are now deeply development-consumed.

The correct conclusion is:
**IMPROVED ARCHITECTURAL GENERALITY / GENERAL SCIENTIFIC FIDELITY NOT ESTABLISHED**

## 7. Fresh research alignment

Jourdan et al., ACL 2025:
https://aclanthology.org/2025.acl-long.335/

Their findings support hybrid, task-specific revision evaluation and warn that LLM judging is more reliable for instruction following than correctness.

CLAIM-BENCH, IJCNLP-AACL 2025:
https://aclanthology.org/2025.ijcnlp-long.127/

Its claim-evidence results support decomposition and relation-level verification rather than one monolithic semantic score.

CLAIMCHECK, Findings of EMNLP 2025:
https://aclanthology.org/2025.findings-emnlp.1185/

Its expert claim-grounding framework supports explicit linkage between critique/assessment and the underlying scientific claim.

StructureBench, IJCAI 2026:
https://www.ijcai.org/proceedings/2026/267

Its separation of structural validity from semantic correctness supports ACAD_PASS's separation between transport/schema success and scientific preservation.

Chavan 2026:
https://arxiv.org/abs/2609.23742

The reported semantic gap after constrained decoding further supports treating structured output as an interface mechanism, not a safety verifier.

## 8. Higher-model decision

**KEEP V2.3 architecture.**

**DO NOT rerun the consumed 12-case live matrix.**

**DO NOT claim V2.3 generalization from the current cases.**

The current 12 cases become:
`AT0_EN_DEV_CONSUMED_V1`

The next authorized gate is:

# AT0-EN V2.4 — FRESH DEVELOPMENT POPULATION FREEZE

Before any new backend inference:
1. create a fresh synthetic development population not derived from the V2.1 model outputs;
2. cover multiple academic domains and distinct semantic-risk classes;
3. freeze source texts, content units, protected relations and graph before inference;
4. freeze prompts, minimal generation envelope and transport policy;
5. include mutation-based graph preflight before opening the population to models;
6. preserve DIRECT and PLANNED as separate experimental arms only if the new protocol still requires that comparison;
7. preregister success/failure metrics separately for:
   - transport/schema validity;
   - scientific constraint preservation;
   - information retention;
   - unsupported additions;
   - revision usefulness/no-op rate;
   - latency/cost;
8. no human-writing superiority claim until later qualified human assessment.

No HW1-EN, detector robustness, DOCX integration, Arabic resumption, reserved-data opening or paid launch is authorized by V2.3 closure.
