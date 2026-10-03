# AT0-EN V2.4 — Gate 0 Contract Closure

Date: 2026-10-03
Status: CLOSED / PASS AS CONTRACT INTEGRITY / NO PERFORMANCE CLAIM

## Final execution

Workflow:
`AT0-EN V2.4 Gate 0 Contract`

Final run:
`37141161540`

Trigger commit:
`61761190dccc191c587896ffb220e8b6cee0c7ce`

Conclusion:
**SUCCESS**

Artifact:
- id: `11280860872`
- name: `at0-en-v2-4-gate0-37141161540`
- SHA-256: `4d34010a29f2cb1d08308d3e2a008d6b42395f6844401f6e1d68175ff7f606f9`

No model inference occurred.

## Final Gate 0 test result

- checks passed: **322/322**
- reference cases: **6**
- reference assertions: **28**
- reference relations: **33**
- development cases: EN04, EN05, EN06, EN07, EN09, EN12
- result: **PASS**

This result establishes internal contract integrity only.
It does NOT establish extractor accuracy, alignment accuracy, verifier safety, paraphrase robustness, or scientific fidelity.

## Frozen file hashes

- schema:
  `74c20c219e8cc2cc240792b772e6f12ca0c60d79b7d2772e44fd06a3fafaeecf`
- criticality rules:
  `49dfdfc6c0f3226161db0b219d3adc7ecd17e04070a6f5bd0367deb579ddeb1c`
- outcome contract:
  `aeff55ec0d5c10a949afc2f86a5eae46e610043f3885497643561b17aa669905`
- development reference:
  `c5fc21cf8ea60f0bd4b403b3a6e9220be33c1d390283a71f0365751ea54ed303`
- contract test:
  `844ea8fb5ab1ec68ca35460c7ffe5fd982bce5f098dfe4b99126ecad6f7c3199`
- source cases:
  `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

## Gate 0 deliverables

1. `SCIENTIFIC_ASSERTION_GRAPH_SCHEMA_V1.json`
2. `CRITICALITY_RULES_V1.json`
3. `OUTCOME_CONTRACT_V1.json`
4. `GATE0_DEV_REFERENCE_V1.jsonl`
5. `check_gate0_contract.py`

## Important design findings during Gate 0

The initial contract contained real inconsistencies that were caught before closure:

1. schema omitted assertion fields required by the frozen architecture:
   - exclusions
   - citation_refs
   - equation_refs
   - symbol_bindings
   - quantifiers

2. some development-reference relation labels did not match the schema.

3. the test initially referenced the wrong parent path for `cases.jsonl`.

4. frame slots and graph relations created a possible dual-source-of-truth problem.

All were repaired before the final run.

Final canonicality policy:
`FRAME_AND_GRAPH_MUST_AGREE`

- frame = local assertion semantics/extracted slots;
- graph = explicit ownership, dependency and cross-assertion/context relations;
- if the same critical scientific fact is represented in both, normalized meanings must agree;
- a critical frame-graph disagreement produces `INVALID_VERIFICATION`, not confidence voting or silent reconciliation.

## Four frozen transaction outcomes

Precedence:

1. `INVALID_VERIFICATION`
2. `REJECT`
3. `REVIEW`
4. `PASS_CANDIDATE`

`PASS_CANDIDATE` requires:
- valid transaction;
- complete critical source coverage;
- no critical deterministic contradiction;
- no material omission;
- no unsupported material new assertion;
- all critical bidirectional alignments preserved/supported;
- no critical uncertainty;
- traceable evidence for every critical decision dependency.

One critical wrong relation is non-compensatory.

## Development-reference status

The 6 reference cases are:
`DEVELOPMENT-ONLY / NOT HOLDOUT / NOT PERFORMANCE EVIDENCE`

They are manually specified from already-consumed synthetic source cases and cover:
- citation-to-claim binding;
- association/causality/scope;
- quantitative value/unit/group/time/baseline ownership;
- procedure order/exclusion/reproducibility;
- equations/symbol definitions/priority direction;
- metric definition/fixed-parameter purpose.

They are intentionally small and are not claimed representative of all scientific domains.

## Fresh research conclusion

End-stage review supports keeping Gate 0 narrow:

- Claimify emphasizes claim coverage, decontextualization and ambiguity-aware extraction.
- SciEvent shows that scientific extraction requires event segments plus argument roles, and correct argument identity alone is insufficient without the correct role.
- Optimizing Decomposition shows that decomposition atomicity and verification performance interact.
- Table-Text Alignment shows that a correct final verification label may still lack a faithful evidence rationale.
- EventRelBench shows that coreference, temporal, causal and hierarchy/subsumption relations remain challenging.

These findings support explicit ownership, uncertainty, provenance and evidence traces, but do not validate the ACAD_PASS implementation.

## Quality delta

Experimental performance:
**UNCHANGED**

Last measured verifier result remains:
- V2.3 adversarial escape: 9/24 = 37.5%
- safe automatic acceptance: 3/12 = 25%
- BOTH_FAIL

Gate 0 introduced no new verifier predictions, so no percentage performance improvement may be claimed.

Methodological status:
**IMPROVED**

Evidence:
- architecture translated into a machine-readable contract;
- outcome precedence frozen;
- criticality rules frozen;
- manual development reference frozen;
- frame/graph canonicality risk identified and repaired;
- 322/322 final integrity checks passed.

## Completion

Gate 0:
**100% COMPLETE**

Whole ACAD_PASS:
**approximately 22% ±5% complete** as a planning estimate, not a scientific metric.

The estimate increased modestly because the V2.4 architecture now has an executable contract and fixed development reference, but no validated extractor or aligner exists yet.

## Exact next authorized stage

`AT0-EN V2.4 GATE A — SOURCE/EXTRACTOR PROTOTYPE AND VALIDATION PREPARATION`

Scope:
- implement only the offline source-side extraction contract;
- begin with deterministic anchors and provenance;
- define extraction outputs against the frozen schema;
- prepare extractor-validation scoring against the 6-case development reference;
- measure coverage, false additions, atomicity, role/ownership binding, context/decontextualization, polarity/modality, and abstention;
- do not implement end-to-end candidate verification yet unless Gate A later authorizes it.

Not authorized:
- new live generation
- HW1-EN
- new untouched holdout
- claims of scientific-fidelity improvement
- case-specific patching from the consumed V2.3 holdout

Higher-model consultation is NOT required at Gate A start unless a new architecture/construct-validity issue appears.
