# ACAD_PASS — R4.4 Read-only Preflight Freeze V1

Date: 2026-10-07
Status: PASS / AUTHORIZE R44-A OOF UPSTREAM BANK ONLY

## Identity

- Run: `37572165532`
- Conclusion: SUCCESS
- Artifact: `11461461773`
- Artifact digest: `sha256:62f92359aeae66363af756a997dc684eb876784ccb6b2104111662fb3c43ff08`
- R4.4 manifest SHA256: `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`
- Seed: 44
- Parent R4.3 FIT only; old R4.3 SELECT excluded.

## Parent corrected source-compatible inventory

320 documents, 1292 examples, 33,244 tokens.
P/I/C/O = 339/1036/144/846.
Goldless examples = 302.
TITLE/METHODS/UNKNOWN = 361/931/0.

The reduced P/I/O counts versus legacy R4.3 are exactly explained by retiring example-initial continuation fragments as independent entities.

## Frozen R4.4 split

### DESIGN
- 256 docs
- 1034 examples
- 26,595 tokens
- P/I/C/O = 271/829/115/677
- goldless examples = 242
- TITLE/METHODS/UNKNOWN = 288/746/0

### VERIFY_INTERNAL
- 64 docs
- 258 examples
- 6,649 tokens
- P/I/C/O = 68/207/29/169
- goldless examples = 60
- TITLE/METHODS/UNKNOWN = 73/185/0

VERIFY deviations from the exact 20% target:
- P +0.295%
- I -0.097%
- C +0.694%
- O -0.118%
- tokens +0.003%
- goldless -0.662%
- TITLE +1.108%
- METHODS -0.644%.

VERIFY was obtained by deterministic pair swaps on the same predeclared objective:
- initial objective 0.0834606824
- final objective 0.00018151794
- swaps = 11.
No seed/tolerance/data-universe change occurred.

## Five OOF folds inside DESIGN

Fold 0: 52 docs, P55/I169/C23/O137.
Fold 1: 51 docs, P54/I165/C23/O135.
Fold 2: 51 docs, P54/I165/C23/O135.
Fold 3: 51 docs, P54/I165/C23/O135.
Fold 4: 51 docs, P54/I165/C23/O135.

All folds satisfy:
- C support >=15;
- every P/I/C/O balance deviation <=25%;
- fixed fold sizes;
- zero overlap;
- complete DESIGN coverage.

Inter-fold deterministic fixed-constraint optimization:
- swaps = 56
- final objective = 0.00422551598.
The large initial objective reflects pre-existing hard-constraint penalty terms; no scientific metric participated.

## Section result

UNKNOWN section rate = 0.0.
Therefore TITLE/METHODS section metadata may remain enabled for R44-A candidate-bank metadata.

## Guards

- old R4.3 SELECT excluded = true
- historical DEV = false
- fold1 test = false
- other folds = false
- FactPICO = false
- consumed 60-RCT = false
- training during preflight = false.

## Adversarial review disposition

Canonical review:
`AT0_EN_V26_R44_ADVERSARIAL_PROTOCOL_REVIEW_V1.md`.

Important correction:
ordinary head CV over the same OOF bank is NOT authorized because of second-order stacking leakage. R4.4 is split into:

- **R44-A:** train only the five OOF B and Boundary ancestors and freeze actual held-out candidate/error/evidence bank.
- STOP.
- **R44-B:** design leakage-safe head selection only after the OOF bank is audited; choose nested outer/inner CV or a fully disjoint stack-development protocol.

VERIFY_INTERNAL stays unopened during R44-A.

## Decision

`R44_READ_ONLY_PREFLIGHT_PASS / AUTHORIZE_R44A_OOF_UPSTREAM_BANK_ONLY`

NEXT_ACTION:
`IMPLEMENT_AND_RUN_R44A_SEQUENTIALLY -> FREEZE_OOF_CANDIDATE_BANK -> AUDIT_REAL_ERROR_DISTRIBUTION -> DESIGN_R44B`.
