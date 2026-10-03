# AT0-EN V2.4 — Gate A2 Source Assertion Decomposition Closure

Date: 2026-10-03
Status: CLOSED / STRUCTURAL-PROTOTYPE PASS / SEMANTIC ACCURACY NOT YET SCORED

## Final execution

Workflow:
`AT0-EN V2.4 Gate A2 Source Assertions`

Final run:
`37142951015`

Trigger commit:
`cb5513ceb03e077e9136fed33c44905512579436`

Artifact:
- id: `11281086502`
- SHA-256: `09bb99ecccac334f17275f4f81e8976e4afd4d58a579d584245c4d99b5230468`

No model inference occurred.
Gold development reference was not read by the extractor or A2 structural scorer.

## Final A2 structural result

Across all 12 frozen synthetic source cases:
- source sentences: **47**
- source assertions emitted: **50**
- anchors carried from A1: **43**
- structural sentence representation: **47/47 = 100%**
- exact evidence/provenance span checks: **140**
- relations emitted: **0**
- semantic anchor ownership assessed: **NO**
- semantic coverage claimed: **NO**
- coverage status: `UNKNOWN_BY_DESIGN`

Extraction status:
- CERTAIN: **19/50 = 38%**
- UNCERTAIN: **13/50 = 26%**
- AMBIGUOUS: **18/50 = 36%**
- non-CERTAIN / abstention-like output: **31/50 = 62%**

Assertion types:
- RELATIONAL: 25
- DEFINITIONAL: 9
- PROCEDURAL: 6
- COMPARATIVE: 3
- ASSOCIATIONAL: 2
- EQUATION: 2
- NEGATION: 1
- QUANTITATIVE: 1
- SCOPE: 1

## Important negative evidence preserved

Initial A2 run:
- run: `37142805075`
- artifact: `11281051423`
- artifact SHA-256: `d77fb3708abdc5086723814a15b5c1394c11ba74a9dd0d068978ca17d6c1d453`

The initial structural workflow passed, but manual red-team found a critical segmentation defect:
decimal points inside values such as `42.0`, `51.5`, `46.2`, `49.8`, and `4.2` were treated as sentence boundaries.

This created five artificial fragments and false assertions.

Initial -> final:
- sentence spans: 52 -> 47
- assertions: 55 -> 50
- CERTAIN: 21 -> 19
- UNCERTAIN: 12 -> 13
- AMBIGUOUS: 22 -> 18
- non-CERTAIN rate: 34/55 = 61.82% -> 31/50 = 62.0%

The repair:
- made sentence segmentation decimal-safe;
- added regression guards preventing decimal boundaries;
- added conservative abstention for embedded propositions such as `found that`;
- added abstention for `whether` / `rather than` scope structures.

All five identified artificial decimal fragments were removed.

## Frozen final hashes

- source assertion extractor:
  `32c68926de1bb20d03f7033d30319862102fe344a3a41f784bff7e648306c0f1`
- A2 structural validation script:
  `c8b0ca44341f3c8c48e19ff078afa4fcbdd2be97a32daf529e0f7310d7712dd8`
- final source-assertion predictions:
  `12bb579866311320701458afdb826daddd7007cb70a56d032ea0f404e7f1f8c8`
- final summary:
  `1d474a292e9d1428101eea3c94a6fce996b7b69ff894dc9952597b45380e1e68`
- canonical schema:
  `df986f759a114bd86525b84f00f8d2f362d71bb31546441992291d21c5ebd69f`
- source cases:
  `d91fae326afbca4a82b7b84e99bca0e817947d964fc4b676e3faebd28a1868f7`

Repository frozen summary:
`phase2/academic_transform/at0_en/v2_4/gate_a/results/GATE_A2_SOURCE_ASSERTION_SUMMARY_FROZEN.json`

## Interpretation

Classification:
**PASS AS A CONSERVATIVE STRUCTURAL SOURCE-EXTRACTION PROTOTYPE / ACCURACY NOT ESTABLISHED**

A2 proves only that the prototype:
- preserves exact source provenance;
- emits schema-compatible assertion candidates;
- records uncertainty/ambiguity explicitly;
- avoids semantic ownership claims before relation extraction;
- keeps source coverage status explicitly unknown;
- can conservatively abstain on complex structures.

A2 does NOT establish:
- assertion coverage accuracy;
- atomicity accuracy;
- subject/predicate/object accuracy;
- decontextualization correctness;
- role/ownership correctness;
- polarity/modality correctness;
- abstention calibration;
- end-to-end scientific fidelity.

The 62% non-CERTAIN rate is diagnostic, not success or failure. A3 must determine whether it reflects appropriate abstention or excessive brittleness.

## End-stage research interpretation

Current literature supports the chosen caution:
- claim decomposition can help or hurt downstream verification depending on atomicity;
- decontextualization and decomposition can conflict;
- ambiguity-aware extraction should abstain when interpretation is not reliable;
- exact span match is insufficient for semantic event arguments;
- argument-role interrelations matter and should be validated explicitly later.

Therefore no additional heuristic tuning on the frozen gold reference is authorized before A3 scoring.

## Quality delta

End-to-end scientific-fidelity performance:
**UNCHANGED**
- last measured adversarial escape: 37.5%
- last safe automatic acceptance: 25%
- status: BOTH_FAIL

A2 internal structural delta versus its initial defective run:
- five artificial decimal-fragment assertions removed;
- false decimal sentence boundaries reduced from 5 observed defects to 0 under regression checks;
- structural sentence representation remains 100%;
- abstention rate remains essentially stable: 61.82% -> 62.0%.

Methodological status:
**IMPROVED**

## Completion

Gate A2:
**100% COMPLETE**

Gate A overall:
**approximately 65% complete**

Whole ACAD_PASS:
**approximately 24% ±5% complete** as a planning estimate.

## Exact next authorized checkpoint

`AT0-EN V2.4 GATE A3 — EXTRACTOR VALIDATION AGAINST FIXED DEVELOPMENT REFERENCE`

A3 must measure, without pre-score tuning:
- assertion coverage;
- false additions;
- atomicity;
- subject/predicate/object fidelity;
- context/decontextualization;
- critical role/ownership binding where represented;
- polarity/modality/causality;
- abstention quality;
- critical silent errors.

A3 may use the existing six-case development reference because it is development evidence, not untouched holdout.

Not authorized:
- candidate-text alignment;
- end-to-end verifier scoring;
- new live generation;
- HW1-EN;
- new untouched holdout;
- performance claims beyond the measured extractor-development metrics.

Higher-model consultation is not required before A3 unless scoring reveals a new construct-validity or architecture problem.
