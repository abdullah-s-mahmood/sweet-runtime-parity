# ACAD_PASS — V2.4 Synthetic Scalability Preflight V1

Date: 2026-10-05
Status: FAIL_SCALABILITY / FACTPICO NOT TOUCHED / HIGHER-MODEL DECISION REQUIRED

## 1. Purpose

Measure the scalability of the frozen V2.4 B1.1 assertion matcher using synthetic data only.

No FactPICO record, source text, candidate text, gold label, or prediction was passed through V2.4.

This preflight is execution-validity evidence only.

## 2. Frozen code under test

Frozen component:

`phase2/academic_transform/at0_en/v2_4/gate_b1/b1_aligner.py`

Relevant functions:

- `best_one_to_one(source, candidate)`
- `assertion_groups(source, candidate)`

The frozen implementation enumerates:

`itertools.permutations(candidate, len(source))`

When counts differ and both are >1, the fallback uses:

`n = min(len(source), len(candidate))`

then performs the same permutation search on the first `n` assertions.

Therefore worst-case search is factorial in:

`n = min(source_assertion_count, candidate_assertion_count)`.

## 3. Synthetic benchmark method

A standalone synthetic benchmark reproduced the exact frozen helper logic used by `best_one_to_one`:

- `tokens`
- `jacc`
- `owner_tokens`
- `owner_incompatible`
- `assertion_similarity`
- `best_one_to_one`

Synthetic assertions contained:
- unique group owner;
- predicate;
- object;
- numeric binding;
- unit;
- time;
- population;
- baseline;
- polarity;
- causality;
- modality.

Candidate assertions were reversed to ensure the matcher still traversed the complete permutation space.

No benchmark or external evaluation text was used.

Environment:
current implementation container / Python runtime.

## 4. Measured results

| n assertions | permutations | measured seconds | measured permutations/sec |
|---:|---:|---:|---:|
| 3 | 6 | 0.00140 | 4,291 |
| 4 | 24 | 0.00410 | 5,858 |
| 5 | 120 | 0.02483 | 4,833 |
| 6 | 720 | 0.17669 | 4,075 |
| 7 | 5,040 | 1.41590 | 3,560 |
| 8 | 40,320 | 12.94802 | 3,114 |

Observed throughput falls as `n` grows.

The measured `n=8` result alone establishes that factorial cost is operationally material.

## 5. Optimistic extrapolation from n=8 throughput

Using the observed `n=8` throughput of approximately 3,114 permutations/sec as a CONSTANT optimistic rate:

| n | permutations | optimistic time |
|---:|---:|---:|
| 9 | 362,880 | 1.94 min |
| 10 | 3,628,800 | 19.42 min |
| 11 | 39,916,800 | 3.56 h |
| 12 | 479,001,600 | 42.73 h |
| 13 | 6,227,020,800 | 23.14 d |
| 14 | 87,178,291,200 | 324.02 d |
| 15 | 1,307,674,368,000 | 13.31 y |

These are optimistic because measured permutations/sec already decreased with increasing n.

They are not predictions of FactPICO assertion counts.

## 6. FactPICO exposure statement

FactPICO was NOT run through:
- A1;
- A2;
- B2.2;
- B1.1;
- final outcome engine.

No FactPICO assertion counts were measured.

Therefore the external evaluation relationship remains unconsumed.

## 7. Root cause

The matcher solves a one-to-one assignment objective:

For each possible source/candidate pair it computes additive pairwise terms:
- hard owner mismatch;
- owner similarity;
- semantic similarity.

The global objective is lexicographic:

1. minimize total hard-owner mismatches;
2. maximize total owner similarity;
3. maximize total semantic similarity.

Because these terms are additive over assignments, the underlying mathematical structure is an assignment problem.

Full permutation enumeration is not required in principle.

## 8. Why this cannot be silently optimized

The canonical V2.4 runtime is frozen.

Replacing permutation enumeration with:
- Hungarian assignment;
- min-cost flow;
- ILP/MILP;
- branch-and-bound;
- another deterministic scalable matcher

changes executable behavior and implementation identity.

Even if the intended objective is preserved, this must be:

`NEW PIPELINE VERSION`

unless the project explicitly adopts a separately justified patch-version policy.

No such policy currently authorizes silent replacement.

## 9. Execution-policy options

### Option A — Preserve canonical V2.4 and run with a predeclared timeout

Before any FactPICO input:
- freeze per-record resource/time limit;
- freeze restart policy;
- timeout/crash -> `INVALID_VERIFICATION`;
- every one of 345 records remains denominator-visible;
- no adaptive retry after observing benchmark behavior.

Advantages:
- produces a true canonical V2.4 external baseline;
- preserves reviewer recommendation to measure frozen baseline first.

Risks:
- external one-shot may be dominated by execution INVALID rather than scientific capability;
- many full-document records may never receive a semantic transaction result;
- timeout threshold becomes scientifically material and must be benchmark-independent.

### Option B — Version-bump to a scalable assignment implementation before external prediction

Create a new runtime version.

Requirements:
- preserve V2.4 as frozen historical baseline;
- specify scalable assignment objective and tie policy before external data;
- rerun all existing development/regression tests;
- demonstrate no safety regression;
- freeze new runtime identity;
- FactPICO prospectively evaluates the new version.

Advantages:
- avoids knowingly executing factorial code on full documents;
- external result is more likely to measure semantic capability rather than implementation tractability.

Risks:
- no external measurement of canonical V2.4;
- algorithm/tie changes may alter prior outcomes;
- requires a new runtime freeze and regression evidence.

### Option C — Other path

Only if an independent methodological review identifies a cleaner alternative.

## 10. Preflight verdict

`FAIL_SCALABILITY`

Current FactPICO status:

`NOT_READY_FOR_FACTPICO_PREDICTION`

Reason:

`KNOWN FACTORIAL ALIGNMENT IMPLEMENTATION WITH MEASURED n=8 = 12.95s`

## 11. Escalation requirement

This is a material architecture/execution decision.

Per project working rules, it should be escalated to the higher-model reviewer before choosing A vs B.

The consultation must be focused:
- no new broad landscape research;
- no code;
- no FactPICO execution;
- no benchmark redesign;
- no threshold tuning.

## 12. Current recommendation from implementation agent

`PREFER VERSION-BUMP SCALABLE MATCHER, SUBJECT TO INDEPENDENT REVIEW`

Reason:
the blocker is algorithmic rather than semantic, is known before external prediction, and can cause the one-shot evaluation to measure factorial runtime failure instead of verification quality.

However, canonical V2.4 must remain preserved and all negative history retained.

## 13. Exact next checkpoint

`FOCUSED HIGHER-MODEL DECISION: CANONICAL V2.4 TIMEOUT BASELINE VS VERSION-BUMP SCALABLE MATCHER`

No FactPICO prediction authorized.
