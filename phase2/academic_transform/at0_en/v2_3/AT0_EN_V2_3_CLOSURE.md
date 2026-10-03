# AT0-EN V2.3 Assertion-Graph Verifier — Closure

Date: 2026-10-03
Status: CLOSED / USEFUL HARD GUARD / FAILED AS STANDALONE VERIFIER
New model inference: NONE

## Evidence chain

### V2.2 independent red-team
- run: 37130259582
- trigger commit: 4ab44badeced0b0f8a847a9c65aef110ccc9bd1f
- artifact: 11276616582
- artifact digest: sha256:cee42205419c467dbecdeb0111dcc2109b996cb7855b2987693de5e169a2d960
- safe controls: 12/12 accepted
- adversarial attacks caught: 3/24
- adversarial attacks escaped: 21/24
- escape rate: 87.5%

Interpretation: the V2.2 regex-oriented validator was overfit to known checks and mainly proved lexical witness presence. It was not a valid standalone scientific-preservation verifier.

### V2.3 assertion-graph known external gate
Frozen verifier after serialization-only repair:
- commit: c6180f97d1d98dbe9039728777572a65a9842aa4
- run: 37132825529
- conclusion: SUCCESS
- artifact: 11277318066
- digest: sha256:f397133558e06e5ae2d78107b09d91cda87cf9e7f4714459356b19cef1815794

The 24 already-observed V2.2 adversarial attacks were all rejected by V2.3 after redesign. This is development evidence only because these attacks were consumed during redesign.

A benchmark defect was also identified:
- V2.2 SAFE_EN09 omits the source relation that a task receives larger priority only when the weighted combination becomes larger.
- the frozen EN09 content_units also omit this relation even though source_text contains it.
- therefore source_text, not content_units alone, is authoritative for preservation.

### V2.3 unseen holdout
Verifier was frozen before holdout creation/execution.
- run: 37132991961
- trigger commit: cde4d9b9c9f91826a51898a6a60dbfd5561f2d12
- artifact: 11277443135
- artifact digest: sha256:dbec7fe4fa4cf3c4c7d6e49fd9102673557dfb24645d95f4d3bb231a752b2c3f
- verifier SHA-256 inside artifact: d82af97d276131477ab2f8c452f24e3302703f54b856a8ad46547af59d7ec0da
- holdout SHA-256: 9253b4d51f40189d027f89e5aa0a18a6a07f887cac8f9625a72436b8e9ad6e95
- results SHA-256: f95e79eb9a1188b9810e763868126e7917676abe47741f535345cfb62ac7d862
- summary SHA-256: 7adc64c15d49d2e9f83d204b4ef314b7bfd34440bd7289f54ff8aef1d2d79c93

Holdout result:
- safe paraphrases: 12
- safe PASS_CANDIDATE: 1/12 = 8.33%
- safe false positive / non-pass: 11/12 = 91.67%
- adversarial attacks: 12
- attacks caught: 9/12 = 75%
- attacks escaped: 3/12 = 25%

Escaped attacks:
- H_EN02_vehicle_synonym: collection trucks / comparison decoy
- H_EN05_direction_synonym: greater discovery time
- H_EN10_imputation_synonym: filled synthetically

The same lexical-paraphrase limitation caused both unsafe escapes and safe false positives.

## Scientific interpretation

V2.3 materially improves explicit relation and contradiction checking but fails paraphrase robustness. It is therefore retained only as a deterministic high-precision/hard-invariant layer, not as the overall verifier.

Do NOT patch V2.3 against the consumed holdout and then claim that holdout as confirmation.

Classification versus V2.2:
- deterministic contradiction coverage: IMPROVED
- unseen attack escape: improved relative to the failure mode, but different populations prevent a causal numeric comparison to V2.2
- paraphrase robustness: WORSENED / explicitly exposed as inadequate
- standalone verifier readiness: FAIL

## Architecture implication

A viable verifier must combine:
1. deterministic hard guards for exact/protected invariants;
2. source-derived assertion graph;
3. semantic entailment/contradiction verification for paraphrase;
4. candidate-to-source checks for unsupported additions;
5. explicit REVIEW on disagreement or insufficient evidence.

No HW1-EN or new generation experiment is authorized from V2.3.
