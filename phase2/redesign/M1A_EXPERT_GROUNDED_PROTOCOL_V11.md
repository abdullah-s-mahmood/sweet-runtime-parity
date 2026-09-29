# M1-A — Expert-Grounded Reference Bootstrap Protocol v1.1

Date: 2026-09-30  
Status: PRE-REGISTERED AFTER v1 FEASIBILITY FAILURE; BEFORE v1.1 MATERIALIZATION

## Research question

Can multiple previously published human/expert Arabic correction resources bootstrap the measurable parts of ACAD_PASS Edit Contract v1 without fabricating human gold, while keeping unsupported dimensions unresolved?

## Inputs

### 1. QALB14 L1 — already consumed
Pinned repository: CAMeL-Lab/arabic-gec  
Revision: 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf  
Splits: TRAIN and DEV only.

Use:
- raw source
- human corrected reference
- official M2 edits

Do not read QALB14 TEST or any QALB15 data.

### 2. ZAEBUC Arabic — independent professional correction source
Pinned repository: CAMeL-Lab/arabic-gec  
Same revision.  
Use TRAIN only:
- data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.raw
- data/gec/ZAEBUC-v1.0/data/ar/train/train.sent.cor

ZAEBUC reports professional Arabic annotators, weekly quality checks, and text-correction inter-annotator Dice similarity 97.1% on the evaluated Arabic subset.

DEV and TEST remain unread for M1-A.

### 3. A7'ta — expert-book parallel errors/corrections
Pinned repository: iwan-rg/A-Monolingual-Arabic-Parallel-Corpus-  
Revision: 6e3acf8b38e159391131eaa448a55f0124e603f2

The published data article reports 470 erroneous/error-free pairs manually collected from the linguistic reference book “Linguistic Error Detector — Saudi Press as a Sample,” which presents the error, correction, and linguistic rule. License reported by the data article: CC BY 4.0.

A deterministic 80% hash partition is used for M1-A bootstrap; 20% is marked RESERVED_A7TA_M2 and not materialized into the bootstrap manifest.

### 4. Nahw
Keep the existing frozen 150 Phase-2 development targets available as local-reference evidence only. Nahw references never imply whole-passage completeness.

## Evidence model

No source is an absolute oracle.

Every example records:
- provenance;
- source quality tier;
- direct assertions;
- unresolved axes;
- whether the case is natural or controlled counterfactual.

Reference mismatch alone never proves WRONG.

## Case families

### CLEAN_REFERENCE_KEEP
Input = human/expert corrected reference.
Candidate = same corrected reference.
Direct claim: expert-supported corrected text should not require re-introducing an error.
This replaces the flawed v1 requirement that enough naturally unchanged raw source lines must exist.

### ERRONEOUS_SOURCE_KEEP
Input = raw source when source != human corrected reference.
Candidate = unchanged raw source.
Direct claim: correction remains incomplete relative to the expert reference.

### FULL_EXPERT_REPAIR
Raw source → full human corrected reference.

### SINGLE_EDIT_COMPLETE
QALB line with exactly one reconstructable official edit.

### ONE_OF_MANY_PARTIAL
Apply one official QALB edit from a multi-edit line and withhold the others.

### ALL_BUT_ONE_PARTIAL
Apply all but one official QALB edit.

### ZAEBUC_FULL_EXPERT_REPAIR
Raw ZAEBUC sentence → professionally corrected version.

### ZAEBUC_CLEAN_REFERENCE_KEEP
Corrected ZAEBUC sentence → itself.

### ZAEBUC_ERRONEOUS_SOURCE_KEEP
Changed raw ZAEBUC sentence → unchanged raw sentence.

### A7TA_EXPERT_RULE_PAIR
Expert-book erroneous expression/sentence → corresponding correct form.

### A7TA_CLEAN_REFERENCE_KEEP
A7'ta correct side → itself.

## Unsupported dimensions

QALB, ZAEBUC and A7'ta do not by themselves establish:
- factual truth;
- scientific claim correctness;
- citation integrity;
- numeric/statistical relation preservation;
- DOCX/OOXML integrity;
- author intent in genuine ambiguity;
- correctness of an arbitrary non-reference alternative.

Those remain unresolved or REVIEW_REQUIRED.

## Safe persistence

Runtime may read public upstream text.
Committed M1-A outputs contain hashes and provenance only, not raw Arabic text.

## Deterministic sampling caps

Persist:
- QALB_FULL_EXPERT_REPAIR: 500
- QALB_CLEAN_REFERENCE_KEEP: 500
- QALB_ERRONEOUS_SOURCE_KEEP: 500
- QALB_SINGLE_EDIT_COMPLETE: up to 250
- QALB_ONE_OF_MANY_PARTIAL: 500
- QALB_ALL_BUT_ONE_PARTIAL: 500
- ZAEBUC_FULL_EXPERT_REPAIR: up to 300
- ZAEBUC_CLEAN_REFERENCE_KEEP: up to 300
- ZAEBUC_ERRONEOUS_SOURCE_KEEP: up to 300
- A7TA_EXPERT_RULE_PAIR: all bootstrap-partition pairs up to 400
- A7TA_CLEAN_REFERENCE_KEEP: matching bootstrap correct sides up to 400

## v1.1 DATA_READY criteria

All must pass:
1. QALB14 TRAIN/DEV source/reference line counts match.
2. QALB changed lines >=1,000.
3. QALB clean-reference KEEP available >=1,000.
4. QALB erroneous-source KEEP available >=1,000.
5. QALB multi-edit reconstructable >=300.
6. QALB ONE_OF_MANY_PARTIAL >=300.
7. QALB ALL_BUT_ONE_PARTIAL >=300.
8. ZAEBUC TRAIN raw/corrected line counts match.
9. ZAEBUC TRAIN total aligned pairs >=100.
10. ZAEBUC TRAIN changed pairs >=50.
11. A7'ta paired error/correct records discovered >=450.
12. A7'ta bootstrap partition pairs >=300.
13. A7'ta reserved partition pairs >=80.
14. At least three independent expert-evidence source families are present.
15. No QALB14 TEST, QALB15, ZAEBUC DEV/TEST, reserved Nahw, or sealed benchmark data are read.
16. No raw Arabic text is persisted in safe committed outputs.
17. Every persisted case has provenance, evidence tier, and unresolved axes.

Failure does not authorize threshold reduction. It triggers another explicit design review.

## Success meaning

DATA_READY means the reviewer-availability blocker is materially reduced for M1 calibration and future verifier testing.

It does not mean:
- independent human confirmation of ACAD_PASS project cases exists;
- Arabic auto-accept is safe;
- scientific fidelity is solved;
- any frontier verifier has improved.
