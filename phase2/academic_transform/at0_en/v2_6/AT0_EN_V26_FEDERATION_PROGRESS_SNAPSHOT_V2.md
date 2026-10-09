# ACAD_PASS — Public Human-Gold Federation Progress Snapshot V2

Date: 2026-10-09

State:
`PREFIT_CLOSURE_ADVANCED / NO_SUCCESSOR_SCIENTIFIC_FIT_YET`

## 1. Mandatory independent-review findings F01-F06

Conservative completion rubric:

- F01 exposure lineage and historical identity: **85%**
  - R43/R44 lineage corrected to EBM-NLP_mod;
  - 359/400 EBM-NLP_mod records mapped to original PMIDs;
  - DESIGN mapping 250/256;
  - VERIFY_INTERNAL mapping 49/64 without exposing protected IDs;
  - unresolved records remain conservatively unresolved.

- F02 weak-role semantics: **100%**
  - DISTANT-CTO does not provide native I/C role labels;
  - official Zenodo release audited;
  - D5 canceled without replacement.

- F03 gold-independent preprocessing: **100%**
  - historical Hu gold-aware chunking defect verified;
  - text-only planner synthetic PASS;
  - real pinned-tokenizer execution PASS on all 400 exposed development documents;
  - full source-word coverage and deterministic output;
  - no benchmark test or gold labels consumed.

- F04 benchmark eligibility/provenance: **85%**
  - AD/COVID official file identity and split structure frozen;
  - exact-text overlap checks PASS;
  - target PMID resolution partial PASS;
  - DOI/registry PubMed custody checks show zero resolved collisions against DESIGN/VERIFY_INTERNAL/OLD_SELECT;
  - unresolved target records and same-trial multi-publication risk remain explicit limitations.

- F05 incompatible comparison prevention: **100%**
  - AlpaPICO/FinePICO/PICOX/GPT-4o metric/task mismatches frozen;
  - strict occurrence-level four-class scorer is authoritative.

- F06 finite study design: **100%**
  - D0-D4 frozen;
  - D5 canceled prospectively;
  - active budget exactly 45 development fits;
  - no seventh arm;
  - architecture mechanics synthetic PASS.

Arithmetic mean:
`95.0%`

This percentage measures closure of the six independent-review findings, not model performance.

## 2. Readiness for FIRST federation scientific fit

Ten-domain conservative rubric:

1. Source identity/file/license/ontology/split closure: **75%**
2. Global alias/trial-family graph: **75%**
3. Protected custody mechanism: **85%**
4. AD/COVID benchmark eligibility: **85%**
5. Gold-independent preprocessing/tokenizer: **100%**
6. Dataset adapters: **90%**
7. Strict scorer/statistics: **85%**
8. Comparator recipes/identity: **80%**
9. GPU runtime/hardware determinism: **35%**
10. Attempt/data/runtime manifest binding: **85%**

Arithmetic mean:
`79.5%`

Interpretation:
the main remaining bottleneck is now execution/runtime rather than unresolved architecture design.

## 3. Development family-fold readiness

Run:
`37890941364`

Artifact:
`11597963894`

Result:
PASS.

Frozen folds:
- fold0: 84 docs, P82/I267/C33/O247
- fold1: 89 docs, P93/I320/C43/O214
- fold2: 83 docs, P96/I242/C39/O216

All:
- contain P/I/C/O;
- C >= 20;
- family-aware component allocation;
- no label-driven swaps.

## 4. Real tokenizer readiness

Run:
`37890868248`

Artifact:
`11597948931`

Result:
PASS.

For all three pinned tokenizers:
- deterministic;
- 400/400 source documents covered;
- no gold consumed;
- no benchmark test used;
- no source word dropped;
- 17 tokenizer-empty words preserved with explicit UNK.

## 5. Architecture readiness

Run:
`37891265928`

Artifact:
`11598720182`

Result:
PASS.

D0-D4:
- forward PASS;
- backward PASS;
- finite gradients PASS;
- deterministic head initialization PASS;
- fixed BIO-valid decoding PASS;
- span loss PASS.

D5:
canceled by frozen source-availability rule.

## 6. Current scientific performance

No successor federation model has been trained.

Therefore scientific performance remains the frozen R44C result:
- macro precision at t=.95 = 0.8767348592080204
- P = 0.8918918918918919
- I = 0.8171091445427728
- C = 0.9318181818181818
- O = 0.8661202185792349

No accuracy improvement is claimed from pre-fit closure.

## 7. Highest-impact remaining blockers

1. GPU execution backend qualification.
2. Final PyTorch/CUDA/cuDNN/determinism/mixed-precision manifest.
3. Per-fit immutable data-manifest hashes and binding into 45 active attempt slots.
4. Executable adapted-PICOX runtime preflight.
5. Remaining source-license/terms cautions.
6. Final pre-fit independent review/authorization.

## 8. Exact next state

`CLOSE_EXECUTION_RUNTIME -> BIND_DATA_RUNTIME_MANIFESTS -> FINAL_INDEPENDENT_PREFIT_REVIEW -> FIRST_SCIENTIFIC_FIT`
