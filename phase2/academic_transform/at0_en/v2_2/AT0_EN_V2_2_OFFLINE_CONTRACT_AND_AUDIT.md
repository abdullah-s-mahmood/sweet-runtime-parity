# AT0-EN V2.2 Offline Contract Redesign and Frozen Audit

Date: 2026-10-03
Status: FROZEN OFFLINE CHECKPOINT
Predecessor: AT0-EN V2.1 run 37123963805
New model inference: NONE

## 1. Decision

Keep the English-first reversible transaction architecture, but separate semantic revision generation from machine packaging and independent verification.

V2.2 does not retroactively change V2.1 outcomes and does not authorize a V2.1 rerun.

Future minimal generation envelope:
- status: REVISE | KEEP | REVIEW
- revised_paragraph: string | null
- uncertainty: array

The generator is no longer authoritative for:
- content-unit mapping
- protected-status certification
- transaction identity
- provenance packaging
- scientific-safety PASS

Those are external system responsibilities.

## 2. Transport boundary

Future acceptance must use a narrow, versioned transport contract.

Allowed:
- raw JSON object
- optionally, one explicitly specified outer Markdown JSON fence if retained by the next authorization

Not accepted:
- first/last-brace salvage
- surrounding prose
- multiple JSON objects
- malformed JSON repaired by another content-generation call

Malformed content remains evidence and is rejected without quality retry.

## 3. Independent protection axes

The offline validator checks or escalates:
- quantities and units
- group/value and time/baseline binding
- citation-to-claim linkage
- negation
- uncertainty/hedge strength
- association versus causation
- scope and population restrictions
- comparison direction
- equation/symbol identity and definition binding
- exclusions and ordered methodology conditions
- new-information / assertive-language candidates

A deterministic PASS_CANDIDATE is only a bounded engineering result on the frozen synthetic case contract. It is not human-quality or general scientific-fidelity proof.

## 4. V2.1 offline replay policy

The frozen V2.1 artifact is replayed without model calls.

For V2.1 schema-valid outputs, the final proposal is audited directly.

For V2.1 schema-invalid outputs, candidate text may be extracted only for DIAGNOSTIC analysis when a deterministic location exists, for example nested required_output. Diagnostic extraction does not retroactively convert the V2.1 cell into a valid cell.

Parse failures with no deterministic final text remain UNAVAILABLE.

A model-generated REVIEW with no revision is recorded as REVIEW_ESCALATED rather than as a parser failure.

## 5. Validator calibration

Validator SHA-256 before repository commit:
b65956b81be087917f02cea9987c3fd42dc6171125e908d5139f607d56faed8d

Adversarial/source test harness SHA-256:
92188f70db94a7ccb6e9cf0d7d9bc374919ce8e81559b2d4d2ad8091c767087e

Calibration result:
25/25 PASS

Composition:
- 12/12 frozen source self-checks PASS
- 13/13 adversarial mutations NOT PASS

Adversarial mutations covered:
- EN01 restriction weakening
- EN02 15-minute interval mutation
- EN03 causal/evidential strengthening
- EN04 citation swap
- EN05 hedge removal
- EN05 causality reversal
- EN06 group/value swap
- EN07 seed mutation
- EN08 causal conclusion reversal
- EN09 U_i / D_i definition swap
- EN10 measurement-rate mutation
- EN11 duplicate-policy reversal
- EN12 retuning-policy reversal

The validator was tightened after the first adversarial pass exposed two validator defects: group/value binding and U_i/D_i definition binding. No V2.1 output was changed.

## 6. Frozen V2.2 audit result

Input artifact:
- V2.1 run: 37123963805
- artifact id: 11275534001
- artifact SHA-256: 842a9ff304c3ed9c854790ac8f205bfe156289b007b556cd06fa4aa19b609326

Offline audit JSONL SHA-256:
4a6c411e1c8f2c6d1a04e75fbc635116561d8c09125aee69849a94009bed1b34

Offline summary SHA-256:
b59db59a5e303669f1c043e09ad7e390c43fe10f57a2d3dde644a5721ba708ce

Dispositions across 48 frozen slots:
- PASS_CANDIDATE: 32
- REJECT: 3
- REVIEW: 8
- REVIEW_ESCALATED: 1
- UNAVAILABLE: 4

By model and arm:
- MODEL_A DIRECT: 9 PASS_CANDIDATE, 1 REJECT, 1 REVIEW, 1 UNAVAILABLE
- MODEL_A PLANNED: 7 PASS_CANDIDATE, 2 REJECT, 2 REVIEW, 1 REVIEW_ESCALATED
- MODEL_B DIRECT: 9 PASS_CANDIDATE, 2 REVIEW, 1 UNAVAILABLE
- MODEL_B PLANNED: 7 PASS_CANDIDATE, 3 REVIEW, 2 UNAVAILABLE

Diagnostic extraction:
- V21_SCHEMA_VALID: 36
- DIAGNOSTIC_NESTED_REQUIRED_OUTPUT: 7
- DIAGNOSTIC_TOPLEVEL_INCOMPLETE: 1
- NO_AUDITABLE_FINAL_TEXT: 4

Eight V2.1 structurally invalid cells contained deterministically auditable candidate text:
- 7 were PASS_CANDIDATE under the bounded V2.2 scientific-protection checks
- 1 was REVIEW

This is evidence that a substantial portion of V2.1 structural failure was packaging burden rather than unusable prose. It does not retroactively validate those V2.1 cells.

## 7. Remaining hard/review evidence

REJECT examples include:
- MODEL_A EN01 PLANNED: evaluation restriction was weakened/rebound to congestion identification
- MODEL_A EN03 DIRECT: Study C was strengthened from reported/when to demonstrated/due to
- MODEL_A EN03 PLANNED: similar evidential/causal strengthening

REVIEW examples include:
- ambiguous "performance increased" for a route time increase
- new assertive rationale such as accuracy/relevance/efficiency/crucial
- attribution strengthening via "ensuring" / "attributable"

These findings confirm that semantic relation preservation cannot be replaced by JSON validity or a planning stage.

## 8. Fresh research alignment

The redesign is consistent with:
- Jourdan et al., ACL 2025, Identifying Reliable Evaluation Metrics for Scientific Text Revision: hybrid task-specific evaluation is needed; LLM judges are better at instruction following than correctness.
- Geng et al., 2025, Generating Structured Outputs from Language Models: structured validity and generated-content quality are separate axes.
- Ray, 2026, The Constraint Tax: small models can pay a semantic cost for hard output constraints; delayed packaging is a relevant design pattern.
- Chavan, 2026, Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap: schema validity is necessary but not semantic correctness.

These sources motivate the design but do not establish the correctness of this project-specific validator.

## 9. Classification versus V2.1

IMPROVED METHODOLOGICALLY / PERFORMANCE CLAIM UNCHANGED

Improved:
- semantic generation is separated from packaging
- self-certified mappings are no longer safety evidence
- relation-level deterministic checks catch concrete drift classes
- packaging-only failures can be diagnosed separately
- safe REVIEW is separated from unavailable output

Not yet improved/proven:
- human writing quality
- general scientific fidelity outside the 12 synthetic cases
- cross-domain performance
- voice
- document fidelity
- detector robustness
- commercial usefulness

## 10. Exact next authorized step

No new inference is authorized yet.

Next:
1. freeze and review this V2.2 offline contract and validator;
2. perform an independent red-team of PASS_CANDIDATE false negatives and REJECT/REVIEW false positives;
3. define a future versioned live protocol only after that review;
4. keep HW1-EN blocked until the higher-model review decides whether V2.2 is sufficiently safe to justify the next live experiment.

Arabic active research remains frozen. Arabic V4.2 remains closed. Reserved Arabic data remain closed.
