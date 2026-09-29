# Phase 2 — Post-Edit Stability + Morphology Environment-Repair Diagnostic

Date: 2026-09-29
Status: DIAGNOSTIC-ONLY; POLICY UNCHANGED

## Purpose

Recover the previously blocked Post-Edit Stability & Morphological Identity diagnostic without rerunning successful second-pass model inference.

The original run 36519213784 produced successful artifacts for:
- postedit-consensus-internal;
- postedit-sweet-q14;
- postedit-sweet-zaebuc;
- postedit-arabart.

The only failed component was contextual morphology runtime initialization. The failure was environmental: transformers 4.57.6 disabled model loading because the job had torch 1.11.0.

## Scientific invariants

This repair MUST NOT change:
- the 142-event consumed UNANIMOUS_3 population;
- first-pass votes;
- jointly corrected text;
- second-pass SWEET/AraBART outputs;
- morphology identity fields;
- target/window stability definitions;
- decision policies;
- evaluation thresholds;
- labels or adjudications.

Only the morphology runtime environment is repaired using the already-successful contextual-guard stack:
- torch 2.2.2+cpu
- transformers 4.44.2
- camel-tools 1.4.1
- cachetools 4.2.4
- numpy <2
- protobuf 3.20.3
- sentencepiece 0.2.0

## Evidence order

1. Reuse frozen artifacts from run 36519213784.
2. Run contextual morphology without reading labels.
3. Materialize POSTEDIT_MORPH feature decisions and hash them.
4. Only then run the existing evaluator against already-consumed labels.
5. Persist no QALB text.
6. QALB15 TEST remains unread.

## Interpretation

This is consumed-slice diagnostic evidence only. It cannot promote any policy.

A policy is merely considered promising for a future disjoint validation if it satisfies the already-coded diagnostic contract. No thresholds or rules may be changed after seeing this rerun.

No Phase 3. No sealed benchmark.
