# M2-H ARETA Diagnostic Preflight Specification v1

Date: 2026-09-30
Status: FROZEN BEFORE PREFLIGHT EXECUTION

## Purpose

Validate a reproducible diagnostic-only runtime for the enhanced ARETA pipeline used to enrich CALIBRATION cases for H2/H3 stratification.

This preflight is NOT a verifier evaluation and must not open INTERNAL_EVALUATION or STRESS_DIAGNOSTIC text.

## Frozen source revision

Repository:
CAMeL-Lab/arabic-gec

Revision:
8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf

Relevant paths:
- areta/aligner/align_text.py
- areta/annotate_err_type_ar.py
- areta/scripts/annotation/
- areta/scripts/explainability/

## Candidate diagnostic runtime

Python:
- 3.8

CAMeL Tools:
- 1.2.0

Compatibility rationale:
- scikit-learn==0.23.2 has a Linux CPython 3.8 wheel but no CPython 3.9 wheel;
- Python 3.8 therefore preserves the frozen historical package pins while avoiding an unsupported source-build path through numpy==1.17.3;
- no ARETA dependency version is loosened in this compatibility revision.

Aligner requirements:
- docopt==0.6.2
- editdistance==0.5.3

ARETA requirements:
- use the repository-pinned requirements as a compatibility reference;
- do not silently upgrade packages merely to force installation;
- if exact historical pins fail on current runners, record the incompatibility before deciding any bounded compatibility adjustment.

## Pipeline to validate

1. Prepare two tiny synthetic Arabic sentence files.
2. Run the official aligner:
   python align_text.py --raw RAW --correct CORRECT --mode align --out PREFIX
3. Confirm that PREFIX.coAlign is produced.
4. Confirm the first line is a header and subsequent rows are:
   RAW<TAB>CORRECT
   with blank-line sentence separators.
5. Run enhanced ARETA on the produced alignment.
6. Confirm that non-empty diagnostic labels are produced and that unknown cases are explicitly reported as UNK.

## Preflight pass criteria

PASS requires all of the following:
- environment installs successfully;
- official aligner imports and executes;
- coAlign output is generated in the expected format;
- enhanced ARETA imports and executes;
- synthetic annotation produces at least one non-UNK diagnostic label;
- no CALIBRATION, INTERNAL_EVALUATION, STRESS_DIAGNOSTIC, Confirmation, Holdout, A7'ta reserve, reserved Nahw, or QALB15 TEST text is opened;
- package versions and pip-freeze SHA256 are persisted;
- exact source revision is persisted.

## Failure handling

A dependency failure is a software-compatibility result only.

It must NOT be interpreted as:
- H2 failure;
- H3 failure;
- H4 failure;
- scientific evidence about verifier accuracy.

If exact historical pins fail:
1. record the exact incompatibility;
2. do not loosen versions in the same run;
3. decide the next compatibility experiment in a separate checkpoint.

## Scientific role

ARETA remains:
- diagnostic;
- stratification-only;
- development-only.

ARETA is not:
- independent human gold;
- a standalone safety verifier;
- an approval oracle.

## Environment isolation

This ARETA environment is separate from:
- H1 / SWEET runtime;
- H3 / current CAMeL morphology runtime.

Only serialized artifacts may cross environment boundaries.

## Current status

Scientific performance:
UNCHANGED.

Deployment:
REVIEW-first.

Next authorized action:
Create and run the diagnostic preflight workflow exactly against this frozen specification.

## Compatibility Revision 2026-09-30

Preflight v1 on Python 3.9 failed before any ARETA execution because scikit-learn==0.23.2 attempted a source build and pulled numpy==1.17.3 as a build dependency, which failed during metadata generation with `NameError: CCompiler is not defined`.

Decision: change only Python 3.9 -> 3.8. Keep CAMeL Tools 1.2.0 and all repository-pinned ARETA requirements unchanged.
