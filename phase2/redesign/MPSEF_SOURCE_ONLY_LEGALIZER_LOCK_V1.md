# MP-SEF SOURCE-ONLY EXECUTABLE ACTION LEGALIZER LOCK V1

Date: 2026-10-01
Status: **PASS / SOURCE-ONLY LEGALIZER ARTIFACT FROZEN**

## Run identity

- workflow: `.github/workflows/phase2-mpsef-source-only-legalizer-v1.yml`
- run: `36807189754`
- job: `110194058153`
- conclusion: **SUCCESS**
- head SHA: `4c2f29d4ff84e222571a9d5a9270b3a47d8f66e4`

## Artifact

- artifact id: `11137763396`
- name: `mpsef-source-only-legalizer-v1`
- ZIP digest:
  `sha256:a6d265295dfacd623057c6a4c9d5e111145c90e2670eae1c5bf8ee6bfef34152`

## Frozen inputs

- C_F source manifest SHA256:
  `051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`
- P1 proposal SHA256:
  `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`
- P2 proposal SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

## Population

- cases: **1,918**
- clusters: **764**
- hypotheses: **3,836 = 1,918 P1 + 1,918 P2**
- action sets: **1,918**

## Final hypothesis states

- P1_OK: **1,806 / 1,918 = 94.16%**
- P1_PROTECTED_BLOCKED: **112 / 1,918 = 5.84%**
- P2_EXECUTION_FAILED: **1,918 / 1,918 = 100%**

Every action set contains KEEP.
Because all P2 hypotheses fail source-only provenance and P1 is the only possible non-KEEP executable proposer, unique primary action-set size is:
- minimum: **1**
- maximum: **2**

## P2 provenance result

The source-only P2 GED alignment audit established:
- 1,918 / 1,918 cases have
  `len(ged_labels) != len(morph_preprocessed_text.split())`;
- total excess GED labels: 30,341;
- mean excess: 15.8191;
- median: 15;
- p95: 27;
- range: +2 to +87.

Accordingly P2 is classified source-only as:
`EXECUTION_FAILED:GED_WORD_ALIGNMENT_MISMATCH`

The frozen P2 outputs are retained as historical proposal evidence and are NOT regenerated/replaced in this cycle.

## Protected-action proof

Executable P1 hypotheses use:
- derived protection detector V2;
- exact protected-signature preservation;
- all-optimal Levenshtein-path audit;
- closed-boundary insertion veto;
- protected deletion/substitution veto;
- unique contiguous protected-character mapping;
- separator preservation;
- token-ordinal attachment preservation for structural protected categories;
- exact source/output SHA round-trip apply/inverse proof.

Across the 112 P1-blocked cases, overlapping reason events include:
- optimal path can insert at protected boundary: 76
- protected separator changed: 73
- protected signature changed: 67
- no optimal exact match for protected character: 43
- optimal path can substitute protected character: 34
- optimal path can delete protected character: 26
- protected attachment ordinal changed: 14
- protected span non-contiguous mapping: 1
- secondary protection-relevant alignment ambiguity: 1

These reason counts overlap and are not sentence percentages.

## Monitoring proof

The mandatory watchdog completed successfully:
- processed: **1,918 / 1,918**
- percent: **100.0%**
- final watchdog return code: **0**
- observed intermediate checkpoint:
  1,088 / 1,918 = 56.7258%, stale_seconds=0

This validates live operational observability for the legalizer.

## Frozen artifact hashes

- legalizer implementation:
  `4fe3fe90037b5e2ec56d426dfd1a00cfa8e5659e2e8dc0d7f68584b7c38782ae`
- progress helper:
  `01a8dfc044b5ef6ecab000e0d4518b8819d1ad0f1ee76f37062761fe0c72cbb6`
- watchdog:
  `2d808ebf587d8f62e34e24bea63df77450578f14771c76b1e853575482eeaa40`
- workflow:
  `645b0287e1990e71ce40fdaba8ed23ab006f03dfb2db1aa7106264c31e0a2a4e`
- hypotheses JSONL:
  `c91195a66a687ba8acf12d1b1e51741183b28992f89681c8510cdac8fddf9e14`
- action sets JSONL:
  `6831756520ea346d08203572831b4ac948fdf3ef4487daf18945cf6ac01ef37a`
- summary JSON:
  `06b81d2ced96b9d4e84487694af7583a62874c6befcab48f0899047c6f8ef8d6`

## Integrity

- gold/reference consulted: **false**
- R_joint computed: **false**
- selector trained: **false**
- INTERNAL_EVALUATION opened: **false**
- STRESS_DIAGNOSTIC opened: **false**
- reserved data opened: **false**

## Interpretation

Versus the prior P1/P2 proposal-freeze checkpoint:

**IMPROVED METHODOLOGICAL VALIDITY / WORSENED P2 EXECUTABILITY / QUALITY PERFORMANCE STILL UNMEASURED**

The main negative finding is material:
P2 contributes no legal executable action under the corrected source-only contract.

No reference-based metric is authorized by this lock.

Next:
1. repair scorer defects F06/F07/F10 without reading project gold;
2. make scorer consume the frozen EXECUTABLE_ACTIONS artifact rather than recomputing legality;
3. enforce fixed population/code/policy hashes before reference access;
4. implement the independent review's synthetic acceptance tests;
5. run a new second premeasurement preflight with no C_F metric output.
