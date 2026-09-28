# Surgical adjudication architecture brainstorm

These are next-test priorities, not changes to the frozen architecture.

## 1. NoPnx1 + current surgical renderer — INTEGRATE

Retain as development reference: 49/60 supported edits and no unknown-token output, while seven wrong edits block production auto-accept.

## 2. NoPnx1 + confidence threshold — TEST

Calibrate coverage and risk by passage clusters; a 0.970-confidence wrong deletion disproves a simple high-confidence guarantee.

## 3. Per-edit rather than per-passage abstention — PROTOTYPE

Filter seven wrong/ambiguous edits without discarding useful edits in the same passage; preserve source spans and recompute locally.

## 4. Error-type-dependent threshold — TEST

Separate hamza, case, weak verb, punctuation and relation-sensitive changes; avoid assuming one score transfers.

## 5. Selective recovery of suppressed safe edits — TEST

Only two plausible lost opportunities were observed, neither proven; require safe mapped output and invariant checks first.

## 6. Tokenizer normalization before SWEET — PROTOTYPE

Make a reversible diacritic/Unicode view and offset map; never expose normalized surface as delivered text without edit mapping.

## 7. Source span mapping improvements — PROTOTYPE

The five false exact flags and 98 unknown-word suppressions justify provenance-preserving alignment with round-trip checks.

## 8. Morphology-aware validation — TEST

Use independent morphology to validate inflection and hamza candidates; do not let it overwrite context or scientific terms.

## 9. Candidate generation → safety verifier → quality ranker — PROTOTYPE

Generate alternatives, protect invariants, then rank quality with explicit abstention; require independent verification.

## 10. Deterministic rules for poorly handled classes — TEST

Consider narrow hamza/weak-verb and punctuation spacing rules only after an error-specific precision audit.

## 11. Alternative Arabic GEC model — TEST

Compare a seq2seq candidate on the same 41 passages under identical source-preserving application and review rules.

## 12. Router by error type — WATCH

Routing could improve coverage but the sample is small and annotated corrections are clustered; measure before adding complexity.

## 13. Leave difficult cases to review — INTEGRATE

Preserve original text for unsafe mappings and surface the candidate/reason to reviewers.

## 14. Strict scientific vs general Arabic mode — PROTOTYPE

Scientific mode must lock terminology, quantities, citations and claims; general mode may permit broader style changes.

## 15. Narrow SWEET commercial role — TEST

Try a precision-first orthography and bounded grammar assistant rather than assuming full Arabic proofreading; test segment value later without market claims now.

## Challenge to the premise

Source preservation solved an as-run corruption mode, yet 7/60 applied edits remain wrong and 108/150 local Nahw errors remain unresolved. A quality ranker may reject wrong edits but will not recover misses. In parallel, compare a different Arabic candidate and a narrow deterministic route. The two plausible suppressed opportunities do not justify weakening the unknown-token lock without reversible mapping and passage-level checks.
