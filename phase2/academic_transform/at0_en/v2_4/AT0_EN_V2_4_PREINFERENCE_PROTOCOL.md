# AT0-EN V2.4 — Fresh Development Population and Live Protocol Freeze

Date: 2026-10-03
Status: **FROZEN PRE-INFERENCE PROTOCOL**
Backend inference under V2.4: **NOT STARTED**

## 1. Purpose

V2.4 tests whether the V2.2/V2.3 redesign—minimal model output plus external scientific verification—improves execution reliability and scientific preservation on a fresh development population.

The prior EN01–EN12 cases are permanently development-consumed and are not reused for a new improvement claim.

## 2. Fresh population

Frozen population:
- cases: **16**
- file: `phase2/academic_transform/at0_en/v2_4/V24_CASES.jsonl`
- local SHA-256 before repository freeze:
  `94ee40c2041389a01b37751418865dd7966f28403a25cc587e9cc06ca6a2a683`
- freeze commit:
  `206ca6232657e41954060bfe640fcd4746fd3cb7`

Domains:
1. biomedical
2. epidemiology
3. chemistry
4. materials
5. machine learning
6. networking
7. energy
8. economics
9. psychology
10. education
11. methods/randomization/blinding
12. physics/equations
13. literature/citation synthesis
14. longitudinal results
15. missing-data analysis
16. generalization/field-readiness

All cases are synthetic. They are development material, not human gold and not a representative production benchmark.

## 3. Frozen scientific constraint graph

File:
`phase2/academic_transform/at0_en/v2_4/V24_SCIENTIFIC_CONSTRAINT_GRAPH.json`

Local SHA-256 before repository freeze:
`4f773a6db107f04ad45fcc694a3f15a915905e39b82001cca6fa3e931e241f5c`

Freeze commit:
`07ec52160236d671e90264fafb7ac5180a7656c1`

The graph is evaluated by the generic V2.3 graph validator. No V24-specific scientific branch is allowed in validator code.

## 4. Pre-inference graph validation

The population was not frozen until the graph passed all source self-checks and mutation checks.

### Source self-check
- 16/16 PASS_CANDIDATE

### Mutation preflight
- 16/16 mutations detected

The first version had only 8/16 mutation detection; binding defects were repaired before freeze.

### Confirmation sequence
A separate confirmation set initially scored 12/16 and exposed:
- elongation/composite binding
- subgroup-efficacy negation
- comparator timepoint order
- sensitivity-population binding

After repair it reached 16/16.

A second confirmation set initially scored 14/16 and exposed:
- numeric-boundary error (9% matching 19%)
- missing-count binding error

After repair it reached 16/16.

A third fresh confirmation set, created after those repairs, scored:
- **16/16 detected**

This failure history is part of the evidence and must not be replaced by the final score alone.

## 5. Models

Reuse the exact V2.1 open-weight identities to isolate protocol/population effects:

MODEL_A:
- Qwen3-4B-Instruct-2507 Q4_K_M
- SHA-256:
  `2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e`

MODEL_B:
- SmolLM3-3B Q4_K_M
- SHA-256:
  `8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e`

Runtime:
- llama.cpp commit:
  `b92761a515ea31e852e7fbc1fad5f874b46f3718`

No model substitution after V2.4 live execution begins.

## 6. Experimental arms

Retain two arms for development comparison:

### DIRECT
One revision call with the full source, editorial instruction and preservation constraints.

### PLANNED
One short visible editorial-plan call, followed by one realization call only if the plan is valid.

The plan is advisory, not evidence of scientific correctness.

## 7. Minimal generation envelope

The final generation response is limited to:

```json
{
  "status": "REVISE | KEEP | REVIEW",
  "revised_paragraph": "string | null",
  "uncertainty": []
}
```

The model does **not** generate:
- content-unit mapping
- protected-status certification
- transaction identity
- provenance metadata
- scientific PASS/FAIL labels

Those are external responsibilities.

PLAN envelope:

```json
{
  "status": "PLAN | REVIEW",
  "operations": [],
  "uncertainty": []
}
```

## 8. Transport policy

Allowed:
- raw JSON object;
- one standard outer Markdown JSON fence only if the versioned parser explicitly normalizes exactly that frame.

Forbidden:
- first/last-brace salvage;
- arbitrary surrounding prose extraction;
- multiple-object salvage;
- content retry for malformed JSON;
- best-of-N regeneration.

Malformed model content is preserved and counted as a failure.

## 9. Matrix

16 cases × 2 models × 2 arms = **64 slots**

Logical-call ceiling:
- DIRECT: 32 calls
- PLANNED: up to 32 plan + 32 realization calls
- maximum: **96 logical calls**

Execution:
- strictly sequential
- one model at a time
- one request at a time
- no concurrent matrix strategy
- no quality reruns
- additional monetary cost ceiling: **USD 0.00**

## 10. Preregistered measurements

Report independently:

### A. Transport / schema
- raw/fence-normalized parse success
- schema-valid final response rate
- malformed/truncated rate
- PLAN failure rate

### B. Scientific preservation
- HARD-constraint violation rate
- REVIEW rate
- per-constraint retention
- quantity/unit/binding failures
- causality/modality/scope failures
- citation/equation failures
- unsupported-new-claim candidates

### C. Information / transformation behavior
- exact no-op rate
- KEEP rate
- REVIEW escalation rate
- source/output word ratio
- sentence-count delta
- protected content-unit retention diagnostics

### D. Operations
- latency by model/arm
- prompt/completion token counts
- total logical calls
- additional monetary cost

## 11. Preregistered gates

### Engineering execution gate
Required:
- 64/64 slots accounted
- ≤96 logical calls
- no source/hash/scope corruption
- zero prohibited-data access
- full raw evidence preserved

### Transport gate
Required:
- schema-valid final response rate **>= 95% overall**
- and **>= 90% in each model × arm cell group**

This is a transport gate only.

### Scientific-safety gate
Among auditable final proposals:
- HARD scientific-constraint violation rate **<= 5% overall**
- no model × arm group may exceed **10%**
- citation/equation identity failures are automatic hard failures
- any source/scope/protected-data corruption is immediate gate failure

REVIEW is not counted as a hard violation, but review burden is reported independently and cannot be hidden.

### Usefulness diagnostics
No preregistered superiority PASS is assigned to prose quality from synthetic cases alone.

Report:
- exact-source/no-op rate
- REVISE/KEEP/REVIEW distribution
- compression/expansion
- qualitative higher-model review of all safety-relevant failures

Do not optimize safety thresholds post hoc to make the run pass.

## 12. Claims that V2.4 cannot establish

V2.4 cannot establish:
- human writing superiority
- production readiness
- general cross-domain scientific fidelity
- detector robustness
- voice fidelity
- document/DOCX fidelity
- Arabic performance
- commercial usefulness

Those require later independent tracks.

## 13. Stop conditions

Stop and preserve evidence for:
- model hash mismatch
- runtime identity mismatch
- source/population hash mismatch
- constraint-graph mismatch
- source/scope corruption
- prohibited-data access
- logical-call ceiling breach
- inability to preserve raw output/accounting

Local content failures do not justify rerunning the cell.

## 14. Exact next step

Before V2.4 inference:
1. freeze DIRECT/PLAN/REALIZE V2.4 prompts;
2. freeze minimal-envelope parser and V2.4 runner;
3. rerun offline transport/schema fixtures;
4. verify cases and graph bytes/hashes at runtime;
5. higher-model review the complete pre-inference packet;
6. only then authorize one V2.4 live development run.

HW1-EN remains blocked.
Arabic active research remains frozen.
Reserved Arabic populations remain closed.
