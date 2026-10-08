# ACAD_PASS — Late-Supplied R44-B Independent Review Archive Audit V1

Date: 2026-10-08

State: `LATE_INDEPENDENT_REVIEW_ARCHIVE_VERIFIED_NO_CONTRADICTION`

## 1. Purpose

After the one-shot R44-B DEVELOPMENT experiment and its read-only causal diagnosis were already completed/frozen, the user supplied the two original external-review deliverables that had not been attached to the working conversation during execution:

- `ACAD_PASS_R44B_INDEPENDENT_REVIEW(1).md`
- `ACAD_PASS_R44B_INDEPENDENT_REVIEW_2026-10-08.zip`

This audit is provenance-only. It does not alter or rerun any scientific result.

## 2. Exact report identity

The standalone Markdown review and the copy embedded in the ZIP are byte-identical.

SHA-256:
`ec18268fc33ee18d4546bdf5a0c3b4480e4578ab411c7ba401ab70d4f30c3f1e`

Embedded path:
`r44b_independent_review/ACAD_PASS_R44B_INDEPENDENT_REVIEW.md`

Reviewed commit recorded by that report:
`81f5bc008c80edc01a846a8cc16901e501b991ff`

External verdict:
`PROCEED_WITH_NONSCIENTIFIC_IMPLEMENTATION_FIXES_ONLY`

## 3. Additional archive evidence newly inspected

The ZIP contains:
- the external review report;
- `INDEPENDENT_ARTIFACT_AUDIT.json`;
- `EVIDENCE_INDEX.json`;
- `RESUME.md`;
- `verify_frozen_artifacts.py`;
- reviewed source/workflow snapshots;
- relevant GitHub job logs;
- four retained evidence ZIPs.

The contained independent audit records:
`INDEPENDENT_ARTIFACT_IDENTITY_AND_NESTED_ROW_AUDIT_PASS`.

The included verifier was executed again locally against the supplied archive after upload and independently reproduced the same PASS.

Verified findings include:
- canonical manifest hash recomputation PASS;
- pair/side exclusion PASS;
- no coordinate duplicates within outer/role banks;
- repeated-coordinate targets consistent;
- exact equality of all 1,942 outer-evaluation rows to frozen R44-A rows except declared provenance additions;
- meta counts 1567/1519/1499/1535/1551;
- C counts 68/66/71/69/71;
- mechanics report J0 parameters 584,631 and J1 parameters 667,836;
- scientific head training performed in mechanics = false;
- threshold evaluation performed in mechanics = false;
- VERIFY_INTERNAL used = false;
- protected data used = false.

## 4. Independently rechecked embedded ZIP hashes

All hashes listed by the external reviewer were recomputed from the supplied archive and matched:

- `r44b-nested-banks.zip`
  `98383b4bec040f19d6e4076fea1a70dcb406366dfd4bd724d1ad2fac6d2018fb`

- `artifact-11461461773.zip`
  `62f92359aeae66363af756a997dc684eb876784ccb6b2104111662fb3c43ff08`

- `artifact-11506754163.zip`
  `166f9ad326efbb52a9945171e15bc7f39011fe469f50cb80e3bd0435e0e7b669`

- `artifact-11517764421.zip`
  `80d77e63701c9ff80b6b4fc7e571b7b089fbd2120c3bf00693a1c9c9ce570455`

## 5. Reconciliation with work already executed

No contradiction was found.

The late-supplied archive confirms the exact pre-experiment conditions already enforced before run `37706558889`:
- I1 scientific executor closure was required before first fit;
- I2 documentation/provenance corrections were required;
- J0/J1, ordinary five-way CE and the frozen threshold grid were not to be changed before the first baseline;
- 1,942 outer outputs per head were required;
- recall denominators P=271, I=829, C=115, O=677 were required;
- score-driven retries/checkpoint shopping were forbidden;
- the result had to be frozen even on failure;
- execution had to STOP before VERIFY_INTERNAL or final refit.

Those requirements were implemented before the one-shot scientific run.

The resulting one-shot failure therefore remains scientifically valid as DEVELOPMENT evidence and is not invalidated by the late delivery of this archive.

## 6. Effect on current causal diagnosis

The archive does not contain post-R44-B scientific results and therefore cannot independently confirm the later validity/type causal diagnosis.

It does, however, strengthen the provenance of the inputs on which that diagnosis rests.

No observed evidence in the archive requires:
- re-running J0/J1;
- replacing the frozen result;
- reopening thresholds;
- reopening calibration;
- opening VERIFY_INTERNAL;
- changing the current post-R44-B review question.

## 7. Current authorization boundary

Current checkpoint remains:

`R44B_B1_ONE_SHOT_COMPLETE_NO_ARCHITECTURE_NOMINATED -> READ_ONLY_CAUSAL_DIAGNOSIS_COMPLETE -> HIGHER_MODEL_REVIEW_OF_NEXT_FACTORIZED_PROTOCOL_REQUIRED`.

The late archive is supporting provenance evidence only.

No new scientific fit is authorized by this audit.


---

## 8. Provenance correction — same higher-model review deliverables

User clarification on 2026-10-08:

The standalone Markdown report and ZIP were not a separate later external review by another reviewer. They were companion deliverables produced with the **same higher-model review response** whose textual verdict had already been supplied earlier.

Therefore supersede any wording that could imply these files constitute a second independent reviewer or a separate scientific adjudication.

Correct interpretation:
- textual verdict + Markdown report + ZIP are one higher-model review package;
- the package itself is not independent corroboration beyond that single review;
- our later local re-execution of the archive's verifier and SHA checks is an independent **artifact/provenance verification step**, not an independent scientific review;
- no additional scientific weight should be assigned merely because the same review was delivered in both text and files.

This provenance correction does not change:
- the higher-model verdict;
- I1/I2 closure;
- run 37706558889;
- the frozen R44-B no-pass result;
- the read-only causal diagnosis;
- the current requirement for a new post-R44-B higher-model review before any new scientific fit.
