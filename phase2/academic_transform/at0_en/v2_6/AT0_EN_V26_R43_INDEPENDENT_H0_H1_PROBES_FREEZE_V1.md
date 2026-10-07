# AT0-EN V2.6 — R4.3 Independent H0/H1 Exploratory Probes Freeze V1

Date: 2026-10-07

## Scope and governance

Two different, completed, FIT-only internal probes. Both used the safe frozen untrained base and neither used Stage-A outputs, SELECT, historical DEV, protected tests, other folds, FactPICO, or consumed holdouts.

These probes are NON-DECISION diagnostics; they do not modify R4.3 Stage-B design, frozen candidate population, threshold grid or scientific gate. Their two inner subsets are NOT identical, so differences may reflect split composition and negative sampling as well as architecture.

## Probe A — base H0/H1

Run: `37540851386`; SUCCESS.

- internal FIT train documents = 256; evaluation documents = 64
- 6,515 train examples; 1,591 eval examples
- H0 accuracy = 0.9063482285; macro-F1 = 0.8054956018
- H1 accuracy = 0.9088623524; macro-F1 = 0.8211368806
- H1–H0 macro-F1 delta = **+0.0156412788**
- H1–H0 accuracy delta = +0.0025141239
- H0/H1 heads have 579,461/662,666 trainable parameters.

Interpretation: on this frozen inner partition, H1 added a small improvement.

## Probe B — independent inner H0/H1

Run: `37541116791`; SUCCESS.

Artifact: `11448468354`.
Digest: `sha256:9663602ba8ba24722751171923134a11d6ed91f41c8790f5a3fa1dc7fa52a9d7`.

- internal FIT train documents = 256; evaluation documents = 64
- 8,349 train examples; 2,042 eval examples
- H0 accuracy = 0.9378060699; macro-F1 = 0.8457482739
- H1 accuracy = 0.9319294691; macro-F1 = 0.8277176235
- H1–H0 macro-F1 delta = **-0.0180306503**
- H1–H0 accuracy delta = -0.0058766007.

Interpretation: on a distinct frozen inner partition, the simpler H0 did better.

## Cross-probe interpretation

The head ranking REVERSED across these separate exploratory setups (H1 +0.01564 in Probe A, H0 +0.01803 in Probe B). Their numeric metrics are NOT an apples-to-apples randomized controlled head comparison across a common evaluation set, and neither used Stage-A trained ancestors.

Thus:
- Evidence does NOT justify prematurely declaring biaffine beneficial or harmful.
- H0 must remain the strong simplicity baseline.
- Biaffine efficacy may be split- and negative-distribution-sensitive.
- Exactly one already-prospectively-frozen Stage-B H0-vs-H1 diagnostic remains the next experiment once Stage-A hashes are verified.
- No adaptation, extra seeds, threshold search or independent-test opening based on these exploratory numbers.

## Next

Verify completed Stage-A model artifact hashes via compact verification; freeze results; then trigger exactly one frozen Stage B. Strictly sequential scientific processing resumes.
