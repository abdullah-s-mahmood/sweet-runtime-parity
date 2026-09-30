# M2-H Component Manifest v1

Date: 2026-09-30
Status: FROZEN BEFORE DOWNLOAD / EXECUTION

## H1 — Structured edit candidate generator

Model ID:
- `CAMeL-Lab/text-editing-qalb14-nopnx`

Model role:
- non-punctuation structured edit candidate generator only.

Model card:
- Hugging Face model currently identifies the checkpoint as SWEET_NoPnx QALB-2014.
- license: MIT.
- base: AraBERTv02.
- task: token classification / explicit text editing for Arabic GEC.

Implementation repository:
- `CAMeL-Lab/text-editing`
- frozen repository HEAD: `4d552ca3ae98029550f27fc52aa1b22883e16e61`
- default branch: `master`

Documented compatibility environment from official repository:
- Python >=3.10
- PyTorch 1.12.1
- Transformers 4.30.0

Important:
- model artifact file SHA256 is NOT yet frozen because no model file has been downloaded in M2-H.
- before first inference, download once, record exact Hugging Face revision if available, enumerate artifact filenames, and SHA256 every downloaded model/config/tokenizer artifact.
- inference is prohibited until those hashes are committed.

## H2 — Orthographic validator

Implementation:
- local deterministic rules in ACAD_PASS.
- no external model confidence accepted as a safety proof.

Versioning:
- rules must be versioned in-repo.
- every rule must have positive/negative unit tests before evaluation.

## H3 — Morphology validator

Primary codebase:
- `CAMeL-Lab/camel_tools`
- frozen repository HEAD: `be79ca9fc493f0df795375a7255bafef246a802d`
- default branch: `master`

Data/model requirement:
- exact installed CAMeL data package(s) and their licenses must be recorded separately at installation time.
- no inference may begin until the selected MSA morphology DB identity/version and package checksum are committed.

Fallback/research codebase:
- `CAMeL-Lab/camel_morph`
- frozen repository HEAD: `15f5aede4b609db54abd6f87aded1f5ec5d930af`
- default branch: `main`

Current public Camel Morph MSA release referenced by the official repository:
- `camel_morph_msa_v1.0.db` (LREC-COLING 2024 release).

## H4 — Boundary validator

Implementation:
- local deterministic high-precision validator.
- specification: `M2H_H4_BOUNDARY_VALIDATOR_SPEC_V1.md`
- initial rules: `M2H_H4_BOUNDARY_RULES_V1.md`

External H1 confidence is forbidden as validation evidence.

## Evaluation taxonomy

Primary:
- QALB M2 operation labels and exact spans.

Secondary/diagnostic:
- ARETA only when its reference-dependent use is methodologically valid.

## Reproducibility lock

Before any M2-H inference:
1. freeze Python environment lock;
2. freeze exact H1 Hugging Face revision and SHA256s;
3. freeze CAMeL data package identity/checksum/license;
4. freeze H2/H4 rule test suite;
5. freeze development split manifest;
6. commit all above.

No silent dependency upgrade is allowed after the first inference.
