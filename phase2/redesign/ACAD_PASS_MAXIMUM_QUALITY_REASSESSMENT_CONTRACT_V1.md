# ACAD_PASS MAXIMUM-QUALITY REASSESSMENT CONTRACT V1

Date: 2026-10-01
Status: FROZEN PROJECT GOVERNANCE RULE

## Primary objective

The project objective is not to preserve the current architecture, phase plan, proposer set, or workflow.
The objective is to obtain the strongest scientifically defensible ACAD_PASS system that can be built from the available evidence and resources.

A previously completed phase is evidence, not a sacred design choice.

## Mandatory reassessment rule

At any point, if new evidence indicates that an earlier assumption, model, proposer, gate, data transformation, protection policy, matching method, evaluation method, runtime path, or process design materially limits the final system, the project MUST consider returning to that earlier decision.

Returning to an earlier design point is allowed and encouraged when justified.

However, scientific evidence already frozen MUST NOT be overwritten.

## Two-lane discipline

### Lane A — Frozen evidence lane
Preserve completed evidence exactly:
- frozen source populations;
- proposal artifacts and hashes;
- exposure records;
- failed and successful workflow evidence;
- legalizer outputs;
- preflight results;
- authorized measurements.

This lane is immutable.

### Lane B — Versioned redesign lane
A redesign may:
- replace a proposer;
- repair P1/P2;
- add or remove model stages;
- change routing/fusion;
- replace an evaluation implementation;
- change runtime architecture;
- return to an earlier phase;
- introduce new source-only diagnostics;
- create a new development cycle.

Every such change receives a new explicit version and fresh hashes.
It MUST NOT retroactively rewrite Lane A.

## Triggers requiring architectural reassessment

A structured re-baseline review is required when one or more of the following occurs:

1. a proposer fails provenance for a material fraction of the population;
2. a single remaining proposer creates an obvious candidate-coverage bottleneck;
3. Second Preflight exposes repeated structural blockers rather than isolated test gaps;
4. an authorized metric later fails far below its preregistered gate;
5. diagnostic evidence shows one architecture cannot reach required target families;
6. a better model/process becomes available with materially stronger evidence or reproducibility;
7. a prior design choice was made under an assumption later falsified;
8. repair cost exceeds the cost/benefit of replacing the component;
9. protection/safety constraints systematically block useful corrections;
10. the current path can pass only by weakening a scientific gate.

## Re-baseline scope

When triggered, the reassessment may go back as far as necessary, including:
- target definition;
- input representation;
- NoPnx handling;
- P1/P2 proposer selection;
- Arabic-GEC architecture;
- morphology/GED handling;
- candidate generation;
- protection architecture;
- whole-sentence action policy;
- matching/evaluation;
- calibration split usage;
- workflow topology;
- model acquisition/runtime parity.

The review MUST ask whether the current process remains the best architecture, not merely whether it can be patched.

## Decision rule

For every material component, compare at least:

- KEEP CURRENT
- REPAIR CURRENT
- REPLACE
- REMOVE
- ADD COMPLEMENTARY COMPONENT

The choice must be evidence-based and must report:
- expected benefit;
- scientific risk;
- implementation risk;
- contamination/exposure risk;
- reversibility;
- testability;
- cost;
- effect on frozen evidence.

## Failure handling

Every FAIL/BLOCKED/PARTIAL follows the Failure Triage and Repairability Contract.
A failure is never treated as merely an output label.

Root cause must be investigated before deciding whether to:
- retry infrastructure;
- repair implementation;
- create a new version;
- redesign architecture;
- accept a scientific limitation.

## P2 consequence

The frozen P2 failure does NOT imply abandoning P2-style correction.

Current P2 remains blocked in the frozen cycle.
A corrected or replaced P2 is explicitly allowed in a new versioned redesign lane.

The project should evaluate whether P2_V2 should:
- repair the existing Arabic-GEC wordpiece-to-word GED alignment;
- replace the GED interface;
- replace the proposer entirely;
- or add a complementary proposer if this improves candidate coverage safely.

## Higher-model independent review checkpoints

Independent higher-model review SHOULD be requested at these checkpoints:

1. after Second Preflight remediation reaches a stable candidate for PASS and BEFORE any new gold-aware measurement authorization;
2. before committing to a major P2_V2 or architecture replacement, using a package containing the root-cause record, alternatives, frozen evidence, and proposed design;
3. after any authorized measurement that materially fails its gate, before deciding whether to patch or re-baseline;
4. before claiming a final architecture is ready for sealed/independent evaluation.

The independent review is advisory evidence, not permission to weaken gates.

## Maximum-quality rule

The system MUST NOT be optimized merely to preserve previous work.

If the strongest evidence supports rebuilding an earlier stage, the project should rebuild it in a new versioned lane.

Scientific honesty requires preserving the old result while allowing the architecture to improve beyond it.

## Reporting requirement

Every major checkpoint must report:

- IMPROVED / WORSENED / MIXED versus the previous checkpoint;
- magnitude using comparable metrics where possible;
- newly discovered risks;
- whether the current architecture still appears best;
- whether a re-baseline is recommended;
- forecast of likely progress;
- blockers;
- whether higher-model independent review is recommended now.
