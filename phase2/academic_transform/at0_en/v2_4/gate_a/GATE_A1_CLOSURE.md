# AT0-EN V2.4 — Gate A1 Deterministic Anchors Closure

Date: 2026-10-03
Status: CLOSED / PASS WITH NARROW SCOPE / DEVELOPMENT EVIDENCE ONLY

## Execution identity

Workflow:
`AT0-EN V2.4 Gate A1 Deterministic Anchors`

Run:
`37142176334`

Trigger commit:
`a55c3bfd83b2131db3b4ab8f1e060a4b09d37cb0`

Artifact:
- id: `11280995699`
- SHA-256: `dc8ed8978f09dc80281f386a871a1f7487286493069463b45a08a4cd21d80e5b`

No model inference occurred.

## Scope

A1 validates deterministic source-anchor inventory and exact provenance only.

It does NOT evaluate:
- assertion decomposition;
- semantic ownership;
- relation alignment;
- source/candidate equivalence;
- scientific-fidelity end-to-end performance.

All extracted anchors remain intentionally unowned until semantic extraction assigns relation ownership.

## Development reference

Cases:
EN04, EN05, EN06, EN07, EN09, EN12

Gold deterministic anchors:
**35**

Anchor families represented:
- citations
- explicit clock times
- groups
- numeric values
- units
- counts
- seeds
- equations
- symbols

EN05 is a zero-anchor negative control.

## Result

- predicted anchors: **35**
- TP: **35**
- FP: **0**
- FN: **0**
- precision: **100%**
- recall: **100%**
- F1: **100%**
- exact provenance span checks: **35/35**
- EN05 false positives: **0**
- semantic ownership assessed: **NO**

Frozen hashes:
- extractor: `65d0da4b32b8297dd58ba6108fb2a49e0cb96dfa726ce270f0382318919e20db`
- reference: `49e1d4d4029c5f7db0c49242d316ff1e6d3e6e2c0cdba6fff3812ea4d601ed4e`
- validation script: `5848099971ec594b448e5a7ab72e69daa0cb87c704c4bacaa2fb15eb89d7b9d6`
- predictions: `436dff2f365b92797f4f401fab97bf94dbba1b04a69ff1f8bf3b212d6fe877f3`
- summary: `bc7222b85c7cd52e4a40f3055822700e482a1c3d40597b4461f6f947583654ab`
- source cases: `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

## Interpretation

Classification:
**PASS WITH NARROW DEVELOPMENT SCOPE**

This 100% result is not a general extraction-performance claim.

Reasons:
- only 35 hand-annotated deterministic anchors;
- only six already-consumed synthetic development cases;
- regex coverage is intentionally limited;
- semantic relation ownership is not part of A1;
- real scientific documents include broader citation, equation, unit, and formatting conventions.

The result establishes that the deterministic inventory layer can correctly identify and provenance the currently specified anchor types on the fixed development reference.

## Architecture findings discovered during A1

A1 exposed two Gate 0 defects before semantic extraction:
- no global pre-ownership anchor inventory;
- no global provenance span inventory.

Both were repaired and revalidated in:
`phase2/academic_transform/at0_en/v2_4/gate0/GATE0_A1_CONTRACT_REPAIR_ADDENDUM.md`

Canonical Gate 0 after repair:
- 326/326 contract checks PASS
- top-level anchors and evidence spans are canonical
- ownership is deferred to graph relations

## End-stage red-team and research

Important limitations:

1. Exact span match is appropriate for explicit deterministic anchors in A1, but must not be reused as the sole metric for semantic/event arguments; recent event-argument work shows semantically correct arguments may not match a single exact span.

2. The current regex catalog is not a complete representation of real academic formats. Examples not established by A1 include:
   - broad numeric citation styles;
   - author-year citation variants;
   - LaTeX/Unicode equation diversity;
   - word-number hyphenated durations such as five-minute;
   - implicit or scattered semantic arguments.

3. Inter-argument role relations are explicitly out of A1 scope and must be evaluated in later Gate A work.

4. Coverage and ambiguity remain independent safety properties; no A1 PASS can substitute for source assertion coverage or abstention quality.

Relevant research reviewed:
- Claimify / ACL 2025: coverage, decontextualization, ambiguity-aware extraction.
- Event Pattern-Instance Graph / ACL Findings 2025: role interrelations matter for argument extraction.
- BEMEAE / NAACL 2025 and REGen / EMNLP Findings 2025: exact span match can underestimate semantically valid event arguments.

## Quality delta

System-level scientific-fidelity performance:
**UNCHANGED**

Last end-to-end verifier evidence remains:
- adversarial escape: 37.5%
- safe automatic acceptance: 25%
- BOTH_FAIL

A1 component metric:
- deterministic anchor precision/recall: 100% / 100%
- no prior directly comparable A1 baseline exists, so no improvement percentage is claimed.

Methodological status:
**IMPROVED**

## Completion

Gate A1:
**100% COMPLETE**

Gate A overall:
**approximately 35% complete**

Whole ACAD_PASS:
**approximately 23% ±5% complete** as a planning estimate.

## Exact next authorized checkpoint

`AT0-EN V2.4 GATE A2 — SOURCE ASSERTION DECOMPOSITION + ABSTENTION PROTOTYPE`

A2 scope:
- source side only;
- use the repaired global evidence/anchor inventories;
- extract candidate source assertions into the frozen schema;
- preserve provenance;
- do not perform candidate-text alignment;
- explicitly represent uncertainty/ambiguity;
- begin coverage accounting;
- do not claim end-to-end verifier improvement.

Not authorized:
- live generation
- HW1-EN
- new untouched holdout
- end-to-end candidate verification
- semantic alignment implementation before source extraction behavior is understood

Higher-model consultation is not required at A2 start unless a new architecture/construct-validity issue appears.
