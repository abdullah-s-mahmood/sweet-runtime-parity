# AT0-EN V2.1 — Frozen Result Analysis and Higher-Model Decision

Date: 2026-10-03  
Evidence: run `37123963805`, artifact `11275534001`  
Closure lock: `AT0_EN_V2_1_LIVE_MATRIX_CLOSURE_LOCK.md`

## 1. Decision summary

**ENGINEERING_STATUS: PASS_LIVE_WITH_ACCOUNTED_OUTPUT_FAILURES**  
**TRANSFORMATION_FEASIBILITY: MIXED**  
**STRUCTURED_OUTPUT_RELIABILITY: MIXED**  
**SCIENTIFIC_FIDELITY_STATUS: NOT_ESTABLISHED; MATERIAL DRIFT OBSERVED**  
**HUMAN_WRITING_STATUS: NOT_ASSESSED**  
**LENGTH_PRESERVATION_STATUS: MIXED / SOFT BAND NOT A QUALITY GATE**  
**AT0-EN V2.1: CLOSED; NO SILENT RERUN**  
**HW1-EN: NOT AUTHORIZED YET**

The experiment proves that the V2.1 open-weight backend can execute the complete bounded matrix reproducibly at zero additional monetary cost, while retaining raw prompts/responses and accounting for all failures. It does not establish a production-safe academic transformation pipeline.

## 2. Exact execution results

### Overall

- slots: **48/48 accounted**
- logical calls: **71/72**
- `COMPLETE_RAW`: **36/48 = 75.00%**
- failed parse output: **3/48 = 6.25%**
- failed parse plan: **1/48 = 2.08%**
- failed schema output: **8/48 = 16.67%**
- usable final `REVISE` proposals among complete slots: **35**
- one complete slot returned `REVIEW` with no revision
- additional monetary cost: **USD 0.00**
- total recorded model tokens: **64,883**
  - prompt: 47,402
  - completion: 17,481

### Model/arm structural completion

| Model | Arm | Complete slots | Rate |
|---|---|---:|---:|
| MODEL_A / Qwen3-4B | DIRECT | 11/12 | 91.67% |
| MODEL_A / Qwen3-4B | PLANNED | 12/12 | 100.00% |
| MODEL_B / SmolLM3-3B | DIRECT | 3/12 | 25.00% |
| MODEL_B / SmolLM3-3B | PLANNED | 10/12 | 83.33% |

Planning therefore improved **structural completion** for MODEL_B by **+58.33 percentage points**, and MODEL_A by **+8.33 points**. This is an engineering observation only; it is not evidence that planning improves scientific fidelity or writing quality.

## 3. Structured-output failure anatomy

Eight slots parsed as JSON but failed the required final schema. All eight were MODEL_B DIRECT.

- In **7/8**, the model echoed the full input/context object and placed the proposed answer inside the nested `required_output` field instead of returning the final proposal contract.
- In the remaining case (EN10), the model returned a plausible revision object but omitted the required top-level `status`.

Four additional calls were invalid JSON:
- MODEL_A EN09 DIRECT: LaTeX-style `\(` / `\)` sequences were emitted as invalid JSON escapes.
- MODEL_B EN09 PLANNED REALIZE: same invalid JSON-escape pattern.
- MODEL_B EN04 DIRECT: two JSON objects were emitted consecutively.
- MODEL_B EN12 PLAN: truncated/malformed plan JSON.

The current task therefore mixes two burdens:
1. generating a scientifically safe academic revision;
2. emitting a relatively heavy machine contract.

The second burden materially hurts the smaller model and creates failures unrelated to the prose itself.

## 4. Parser audit

All 71 saved raw responses were replayed post hoc with:
1. strict `json.loads(raw.strip())`;
2. one-outer-fence normalization;
3. the current live parser, which can additionally extract first-to-last `{...}`.

For this run, all three methods had the **same parse-success/failure set**. No reported cell succeeded only because of permissive brace extraction. Therefore the observed V2.1 execution result is not an artifact of that permissive fallback.

However, first/last-brace salvage is not accepted as a future scientific contract. V2.2 should allow at most explicitly versioned transport framing (for example, raw JSON or one standard outer JSON fence) and reject other surrounding text without content retry.

## 5. Length diagnostics

The architecture's 0.85–1.15 word-count band was explicitly a soft experimental hypothesis.

Among the **35 structurally valid REVISE outputs**, only **18/35 = 51.43%** fell inside that band.

By model/arm:
- MODEL_A DIRECT: 5/11
- MODEL_A PLANNED: 6/11
- MODEL_B DIRECT: 2/3
- MODEL_B PLANNED: 5/10

This does **not** imply that the other 17 are poor revisions. Several strong redundancy-removal cases legitimately became much shorter, e.g. generic/promotional or repetitive inputs. The result confirms that raw length ratio must remain diagnostic and subordinate to **information-unit retention and scientific fidelity**.

Two structurally valid `REVISE` outputs were exactly identical to the source text:
- MODEL_A PLANNED EN11
- MODEL_B DIRECT EN05

This is safe with respect to content but is a transformation-quality failure if the requested revision need remains unresolved.

## 6. Scientific-fidelity red-team

This section is a **post-hoc higher-model diagnostic review**, not human gold, not a preregistered benchmark score, and not a release metric. It identifies concrete failure modes that block a claim of established scientific fidelity.

### Material examples

**MODEL_A DIRECT / EN03**
- source: Study C *reported* a 12% decrease *when* messages were batched;
- output: Study C *demonstrated* a decrease *due to* batching.
- risk: evidential/causal strengthening.

**MODEL_A DIRECT / EN04**
- source claim: adaptive signal timing *reduced* mean queue length;
- output: it *was associated with a reduction*.
- risk: author claim strength changed, even though the direction is conservative.

**MODEL_A DIRECT / EN12**
- source: fixed parameters are used to determine whether changes arise under load rather than retuning;
- output: fixed parameters *ensure* variations are attributable to load.
- risk: stronger attribution than the source supports.

**MODEL_A PLANNED / EN01**
- source: evaluation is *only* for arterial roads during weekday peak periods;
- output: congestion identification occurs *particularly* on arterial roads during weekday peak periods.
- risk: restriction weakened and attached to a different proposition.

**MODEL_A PLANNED / EN03**
- output again strengthens Study C to “demonstrates” / “through message batching”.
- risk: evidential and causal strengthening.

**MODEL_A PLANNED / EN06**
- output: “Group A's performance increased by 4.2 seconds.”
- source: required route-completion time increased by 4.2 s.
- risk: “performance increased” can imply improvement although more time is worse/neutral without an explicit direction-of-goodness definition.

**MODEL_B PLANNED / EN01**
- adds claims that continuous data supports “more efficient traffic management and response to emerging issues” and that the restricted evaluation scope “ensure[s] accuracy and relevance”.
- risk: unsupported new information and rationale.

**MODEL_B PLANNED / EN03**
- frames all four studies as findings about the “impact of edge aggregation on latency and energy consumption”, although Studies C/D concern message batching.
- risk: mechanism conflation.

### Additional warning examples

- MODEL_A PLANNED EN10 adds an inferred benefit (“enabling precise tracking and organization”) not supplied as a claim.
- MODEL_B PLANNED EN02 adds “assess the system's efficiency”, which is plausible but not explicitly stated and should not be invented by a preservation-first rewrite.
- MODEL_B PLANNED EN10 uses stronger evaluative wording (“crucial”) without need.

The central observation is that **literal values/citations can remain intact while relations, modality, scope, causality, or interpretation drift**. This exactly matches the architecture's distinction between token preservation and scientific preservation.

## 7. What improved versus the prior checkpoint

**IMPROVED**
- moved from `0/48 NOT_RUN` to a complete, auditable 48-slot experiment;
- both frozen open-weight models executed on the intended backend;
- no paid API/GPU was required;
- all failures are preserved rather than silently retried;
- the planning arm substantially improved MODEL_B structural adherence;
- evidence now exposes concrete scientific-drift and packaging failure modes rather than hypothetical risks.

## 8. What worsened / new risks exposed

**MIXED / NEW RISKS**
- only 75% of slots produced a structurally valid final proposal;
- MODEL_B DIRECT is not viable under the current heavy output contract (25% completion);
- generic planning is not a safety mechanism: it can improve format adherence while still introducing scientific drift;
- exact-number/citation preservation is insufficient; relation/modality/scope checks are mandatory;
- the soft ±15% length band fits only about half of valid rewrites and would wrongly penalize useful compression in some cases;
- generator-declared `content_unit_mapping` and `protected_status` are not trustworthy evidence because they are self-reports from the same model that generated the text;
- the old `PROMPT_CASE_POLICY_MANIFEST.json` still describes pre-V2.1 blocked access state and must not be used as the live-run identity record.

## 9. Fresh end-of-phase research and implications

### Scientific text revision evaluation

Jourdan et al., ACL 2025, *Identifying Reliable Evaluation Metrics for Scientific Text Revision*:
https://aclanthology.org/2025.acl-long.335/

Key implication: similarity metrics alone are inadequate; LLM judges are useful for instruction following but struggle with correctness, and hybrid task-specific evaluation is more reliable. This supports separate scientific-relation checks plus later qualified human assessment rather than one aggregate judge.

### Context-aware academic revision

Chen et al., ACL 2026, *XtraGPT: Context-Aware and Controllable Academic Paper Revision via Human-AI Collaboration*:
https://aclanthology.org/2026.acl-long.47/

Key implication: academic revision benefits from explicit criteria/intent alignment and context-aware revision rather than treating direct prompting as sufficient. Our data agree that an explicit plan can help execution, but also show that **generic planning alone does not guarantee preservation**.

### Structured generation

Geng et al., 2025, *Generating Structured Outputs from Language Models: Benchmark and Studies*:
https://arxiv.org/abs/2501.10868

Key implication: constrained decoding should be evaluated separately for constraint coverage, efficiency and generated-content quality. Schema validity is an engineering axis, not a semantic-fidelity proof.

Ray, 2026, *The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models*:
https://arxiv.org/abs/2605.26128

The preprint reports that hard schemas can improve validity while reducing answer correctness in small models and motivates delayed packaging. This is directly relevant to the MODEL_B behavior observed here; it is used as design evidence, not as a universal law.

Chavan, 2026, *Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap*:
https://arxiv.org/abs/2609.23742

This recent preprint similarly separates structural correctness from semantic correctness. It reinforces that JSON grammar cannot replace scientific verification.

## 10. Higher-model architecture decision

**KEEP the English-first transaction architecture.**  
**REPAIR the generation/output boundary and independent verification before HW1-EN.**  
**DO NOT rerun V2.1.**  
**DO NOT treat generic planning or constrained JSON as a scientific-safety solution.**

### Authorized next phase: AT0-EN V2.2 OFFLINE CONTRACT REDESIGN

No new model inference is authorized yet.

V2.2 should:

1. **Separate revision generation from machine packaging.**
   - The generator should not be responsible for authoritative content-unit mapping or protected-status certification.
   - Use a minimal generation envelope: `status`, `revised_paragraph`, and explicit uncertainty only.
   - Build provenance, mappings, transaction identity and validator findings outside the generator.

2. **Move scientific protection to independent post-generation checks.**
   Required classes include:
   - quantities, units, groups, times and baselines;
   - citation-to-claim links;
   - negation and scope;
   - hedge/modality strength;
   - association-versus-causation;
   - comparison direction;
   - equation/symbol identity;
   - restrictions and exclusions;
   - new-information candidates.

3. **Use late, deterministic packaging.**
   - accept only raw JSON or a single explicitly specified outer JSON fence if the transport policy retains that allowance;
   - remove first/last-brace salvage from the acceptance contract;
   - no content retry to repair malformed model output.

4. **Treat the plan as an advisory candidate, not a privileged route.**
   - preserve DIRECT and PLANNED as experimentally separable strategies;
   - a plan must itself pass constraint checks before realization;
   - no assumption that PLANNED is globally superior.

5. **Replace length-as-gate with information-first diagnostics.**
   - keep word ratio and sentence counts;
   - make frozen content-unit retention/new-information detection primary;
   - do not pad or reject a faithful concise rewrite merely for being below 0.85.

6. **Replay V2.1 outputs through V2.2 validators offline.**
   - no model calls;
   - produce a deterministic audit of which existing outputs would be PASS / REVIEW / REJECT and why;
   - compare structural acceptance with scientific-preservation findings.

7. **Return to higher-model review after the offline V2.2 audit.**
   - only then decide whether a narrowly versioned new live experiment is justified;
   - `HW1-EN`, detector robustness, DOCX work, Arabic resumption and any paid launch remain blocked.

## 11. Forecast

Expected improvement from V2.2 is primarily in **failure localization, safety, and interpretability**, not guaranteed prose quality. The strongest opportunity is to stop asking a small generator to simultaneously rewrite, map, certify and serialize the transaction.

Main blockers:
- semantic relation checking cannot be reduced to literal token equality;
- some preservation judgments will remain `UNCERTAIN/REVIEW`;
- genuine human-writing quality still requires qualified human evaluation later;
- a future live rerun, if approved, must be a new versioned experiment rather than replacement of V2.1 evidence.
