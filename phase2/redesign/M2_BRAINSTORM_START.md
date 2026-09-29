# M2 — Adversarial Brainstorming Before Verifier Execution

Date: 2026-09-30

## Candidate designs considered

### A. Ask the LLM “Is this correction correct? yes/no”
REJECT.
This conflates local correctness, completeness, overcorrection, ambiguity and residual error.

### B. Give the expert reference to the judge
REJECT FOR PRIMARY M2.
That would test reference matching, not reference-free verification. The expert reference remains hidden and is used only for scoring.

### C. Multi-agent panel immediately
DEFER.
A panel can amplify correlated errors and obscures whether one strong verifier adds value. Start with one verifier.

### D. Pairwise source-vs-candidate preference only
INSUFFICIENT.
A candidate can be better than source yet still incomplete. Preference is useful but cannot be the sole decision.

### E. Structured selective verifier
SELECTED.
The verifier produces:
- candidate_status: KEEP_CORRECT / REPAIR_COMPLETE / REPAIR_INCOMPLETE / CANDIDATE_WRONG / AMBIGUOUS
- necessity: CHANGE_NEEDED / NO_CHANGE_NEEDED / UNCERTAIN
- local_correctness: CORRECT / INCORRECT / NOT_APPLICABLE / UNCERTAIN
- contextual_correctness: CORRECT / INCORRECT / UNCERTAIN
- residual_error: NONE / PRESENT / UNCERTAIN
- meaning_preservation: PRESERVED / CHANGED / UNCERTAIN
- decision: ACCEPT / REVIEW / REJECT
- confidence: LOW / MEDIUM / HIGH

The final production-like gate uses ACCEPT/REVIEW/REJECT, while the diagnostic axes show why.

## Development/confirmation design

### Development packet
120 blinded cases from QALB14 TRAIN/DEV and ZAEBUC TRAIN only:
- 24 QALB_CLEAN_REFERENCE_KEEP
- 24 QALB_ERRONEOUS_SOURCE_KEEP
- 24 QALB_FULL_EXPERT_REPAIR
- 12 QALB_ONE_OF_MANY_PARTIAL
- 12 QALB_ALL_BUT_ONE_PARTIAL
- 12 ZAEBUC_CLEAN_REFERENCE_KEEP
- 12 ZAEBUC_FULL_EXPERT_REPAIR

Labels/family/source metadata are placed in a separate hidden key.

### Prompt revision policy
- Version P0 is frozen before seeing development labels.
- Run P0 on all 120 development cases.
- If P0 fails the development gate, one and only one prompt revision P1 is allowed.
- P1 must be derived from aggregate error categories, not case-specific memorization.
- P1 is evaluated on a fresh, disjoint 120-case QALB/ZAEBUC development packet.
- After P1, stop prompt tuning regardless of result.

### External confirmation
Only if P0 or P1 passes development:
- freeze prompt;
- evaluate the 88 reserved A7'ta pairs as:
  - 88 A7TA_CLEAN_REFERENCE_KEEP
  - 88 A7TA_EXPERT_RULE_PAIR
  - 88 A7TA_ERRONEOUS_SOURCE_KEEP
- 264 confirmation cases total.
- no prompt/threshold changes after confirmation begins.

## Why not use arbitrary synthetic wrong edits?

The dominant Phase-2 failure is not random corruption; it is locally plausible but incomplete repair. M2 therefore prioritizes human-reference full repairs, unchanged erroneous sources, clean KEEP, and withheld-human-edit partials.
