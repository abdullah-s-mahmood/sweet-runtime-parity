# ACAD_PASS — FREE-SPEED V1 Decision Policy

Date: 2026-10-07
Status: ACTIVE TECHNICAL POLICY / DOES NOT ALTER CURRENT R44-A SCIENCE

## Verified repository facts
- Workflow files before this optimization work: 199.
- Historical Actions runs at audit time: 555 total.
- FREE-SPEED static audit run: 37595953052 SUCCESS.
- Static audit now scans 200 workflows because the audit workflow itself was added.
- Candidate counts:
  - CACHE_SAFE_CANDIDATE: 171
  - CANCEL_SUPERSEDED_CANDIDATE: 20
  - CPU_TUNING_CANDIDATE_REQUIRES_REPRO_BENCHMARK: 12
  - PARALLEL_CANDIDATE_REQUIRES_INDEPENDENCE_PROOF: 1
  - NO_OBVIOUS_FREE_SPEED_CHANGE: 25
- Static flags are conservative candidates, not blanket authorization.

## Current R44-A
Official run 37581447046 remains unchanged and sequential.
- Fold 0 SUCCESS.
- Fold 0 elapsed wall-clock roughly 2h24m from run start to fold summary.
- Fold 1 then started; folds 2-4 remain queued.
- Current workflow version remains max-parallel=1.
- Do not cancel/restart merely for speed.

Fold 0 confirms real OOF distribution:
- gold 384
- native candidates 407
- exact typed 275
- target NONE 126
- native typed precision 0.6756757
- native typed recall 0.7161458
- same-class wrong boundary 64
- spurious/no-overlap 58
- wrong-type exact coordinate 6
- different-class wrong boundary 4
- goldless candidates 21
- BIO invalid/unmatched runs 25 (24 O_TO_I_RUN, 1 CROSS_TYPE_I_RUN)
- candidate bank SHA256 159b4924a919520fea98c3aacbebb73af0a4d87adf1a1efa0b4933f0550aa4ce
This validates the scientific need for OOF error mining.

## Adopted immediately for future workflows

### 1. Immutable preconverted BiomedBERT base
Run 37596247997 SUCCESS.
Artifact:
- name: r44-immutable-converted-biomedbert-base
- artifact id: 11470867918
- artifact digest: sha256:040918879e47afeb8d2e5f7a79e9de2c9a4e0402495ee778a766db506b752441
- artifact size: 406,356,908 bytes.
Inside artifact, model.safetensors must equal:
3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68.

Future folds can consume this artifact instead of:
- installing JAX/Flax in every fold;
- downloading the same BiomedBERT source in every fold;
- converting Flax -> PyTorch in every fold.

The fold script now has a hash-guarded --preconverted-base fast path. Default old --model-dir behavior remains available.

### 2. Pip cache for future fold jobs
Future FAST candidate uses setup-python pip caching keyed by requirements/r44a_fold_fast.txt.
Scientific package versions remain pinned.

### 3. Parallel independent folds — future candidate only
Prepared workflow:
.github/workflows/r44a_fast_candidate.yml

Properties:
- max-parallel: 5
- same frozen DESIGN/preflight inputs
- same fold script, seed, epochs, batch size, optimizer and scientific code
- immutable preconverted base physically hash-verified
- fold outputs namespace-isolated
- aggregate waits for all folds
- no trigger has been created.

Reason parallel execution is scientifically plausible:
- folds have immutable common inputs;
- fold train/heldout documents are disjoint according to frozen manifest;
- no fold consumes another fold's output;
- each matrix job already runs on a fresh GitHub runner even in sequential mode;
- the only join is aggregate-after-all.

The current official R44-A is not changed retroactively.

## Deferred until reproducibility/performance benchmark

### torch.set_num_threads(2)
Do not change yet.
Rationale:
- may improve CPU utilization if runner has spare cores;
- may change floating-point reduction ordering/model hashes;
- exact speedup is hardware/workload dependent.

Required before adoption:
- same pinned base/data/code;
- thread2 vs candidate thread count;
- compare wall-clock, model SHA, candidate-bank SHA, losses and metrics;
- if bitwise identity fails, treat as versioned scientific implementation change, not transparent optimization.

### dataloader_num_workers=0
Lower priority than thread tuning.
The current TokenDataset pre-tokenizes/materializes tensors before Trainer iteration, so worker count may add multiprocessing overhead rather than improve throughput.
Benchmark only; do not assume improvement.

## Selective cancel-in-progress policy
Do NOT globally change concurrency.

Eligible only after review:
- smoke tests;
- mechanics;
- preflight;
- non-durable diagnostics where a newer commit logically supersedes an older one.

Never auto-cancel:
- frozen/one-shot science;
- confirmatory runs;
- long training producing unique evidence;
- runs cited by manifests or papers.

## Expected speed impact

For R44-like five-fold CPU jobs:
- sequential baseline wall-clock is approximately 5 x one-fold duration plus setup/aggregate.
- observed Fold 0 ~2h24m suggests a serial order near ~12h before variability.
- if five independent folds run concurrently and GitHub supplies five runners, theoretical wall-clock approaches the slowest fold (~2.5-3h) plus aggregate.
- Do NOT claim guaranteed 5x: queueing, runner availability, fold-duration variance and account concurrency can reduce speedup.

Converted-base reuse and pip caching reduce startup overhead but will not dominate multi-hour CPU training.

## Financial decision
No evidence currently justifies purchasing a larger runner/GPU solely to solve orchestration inefficiency.
First use safe free orchestration improvements and measure.
GPU remains a separate cost/performance decision if future nested OOF workload becomes dominant.

## Next technical action
Let official R44-A finish unchanged.
After aggregate:
1. scientific OOF bank audit;
2. higher-model/adversarial review;
3. freeze R44-B;
4. use FAST orchestration for future independent-fold workloads only when its scientific identity conditions are satisfied.

Do not prioritize repository-wide mass edits while the core scientific pipeline is still evolving.
