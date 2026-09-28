# Full Edit-Event Gate — End Brainstorm

Date: 2026-09-28

## Highest-value observation

The project's bottleneck has moved again.

Earlier:
renderer fidelity -> candidate correctness -> surface realization -> independent acceptance.

Now:
**generalization robustness** is the primary blocker for freezing automatic Arabic proofreading acceptance.

The current 100% development precision is useful evidence but cannot increase epistemic confidence much further through same-data tuning.

## Best next experiments, ranked by scientific value

1. **Disjoint event-rule generalization** — highest value.
2. **Counterfactual context robustness** for accepted error patterns.
3. **Independent human adjudication** on a later frozen slice.
4. **Event-level generator consensus** after disjoint validation.
5. **Morphology/lexicon support for hamza subclasses** only if disjoint evidence shows meaningful missed coverage.
6. Learned verifier only after much larger disjoint labeled data exists.

## Failure triggers

MODIFY if:
- structural rules accept any HIGH/CRITICAL wrong event on disjoint evidence;
- multiword structural pattern proves context-sensitive;
- source-mark loss cannot be repaired downstream;
- passage-context perturbation flips candidate validity materially.

CONTINUE if:
- wrong accepted remains zero or very low with explicit confidence bounds;
- incremental useful coverage survives;
- review burden remains manageable;
- scientific/semantic guards stay intact.
