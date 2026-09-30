# M2-H H4 Boundary Rules v1

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION

Goal: a deliberately narrow, high-precision starting rule set for Arabic word-boundary errors.

These rules generate/validate boundary hypotheses only. They do not prove full sentence correctness.

## Global hard guards

G0. Arabic-only structural change
- H4 may only insert or remove whitespace.
- Character sequence after deleting whitespace must be identical before/after.
- Any character substitution/insertion/deletion => NOT_APPLICABLE to H4.

G1. Protected-context exclusion
- abstain on URLs, emails, code-like tokens, identifiers, formula fragments, citation keys, mixed alphanumeric strings, or spans containing Latin letters/digits unless a later explicit rule authorizes them.

G2. Exact-span requirement
- the proposed source span must occur exactly in the candidate sentence.

G3. Morphology dependency
- no SUPPORTED decision is allowed solely from a hand-written boundary rule.
- at least one independent morphology/lexical plausibility signal must also support the result.

## MERGE rules: observed tokens should attach

### M1 — Single-letter proclitic attachment
Observed adjacent tokens:
- first token exactly one of: `و`, `ف`, `ب`, `ك`, `ل`, `س`
- second token begins with Arabic letters.

Proposal:
- concatenate the two tokens without changing characters.

Support conditions:
1. merged form has at least one valid MSA morphological analysis;
2. the first token is licensed in that analysis as the corresponding proclitic/particle;
3. no protected-context guard fires.

Notes:
- standalone mathematical/letter-name uses are excluded by G1 or become UNCERTAIN.
- `ل` and `س` require feature-compatible analyses rather than attachment by string alone.

### M2 — Multi-clitic chain attachment
Observed sequence consists only of licensed detachable single-letter proclitic tokens from M1 followed by an Arabic host.

Proposal:
- concatenate the clitic chain and host.

Support:
- resulting full form must have an analysis whose proclitic sequence matches the observed chain.

### M3 — Detached definite article
Observed adjacent tokens:
- first token exactly `ال`;
- second token Arabic lexical host.

Proposal:
- `ال` + host.

Support:
- merged form has a valid analysis containing the definite-article feature;
- separated `ال` is not independently licensed in context.

This is conservative because `ال` should normally be orthographically attached in MSA.

## SPLIT rules: observed token should contain a whitespace boundary

### S1 — Frozen closed-list fused multiword expressions
Only exact normalized forms in the following initial list are eligible:

- `منخلال` -> `من خلال`
- `منأجل` -> `من أجل`
- `علىالرغم` -> `على الرغم`
- `فيحين` -> `في حين`
- `إلىأن` -> `إلى أن`
- `الىأن` -> `الى أن`
- `بعدأن` -> `بعد أن`
- `قبلأن` -> `قبل أن`

Support conditions:
1. both resulting words are lexically/morphologically analyzable;
2. no valid single-token analysis exists that licenses the fused form as an orthographically correct lexical item;
3. no protected-context guard fires.

The list is frozen before CALIBRATION. Additions require a new protocol version, not post-hoc editing.

### S2 — Conservative morphology-supported internal split
For a token not covered by S1:
1. enumerate internal character boundaries;
2. both sides must contain at least two Arabic letters, except a side explicitly licensed as a standalone function word;
3. both sides must have valid MSA analyses;
4. unsplit token must have no valid analysis OR only analyses explicitly marked out-of-lexicon/unknown by the frozen analyzer configuration;
5. contextual evidence must independently favor the two-token sequence if E5 is enabled.

Under v1:
- S2 may produce UNCERTAIN_BOUNDARY candidates during CALIBRATION;
- S2 is NOT eligible for SUPPORTED_BOUNDARY_ERROR until a contextual evidence source is separately frozen.

## Explicit non-rules / traps

Do NOT split or merge solely because a string resembles:
- `فيما`, `مما`, `عما`, `إنما`, `كلما`, `لأن`, `لكن`, or other lexicalized/grammaticalized forms that can be valid as written.
- punctuation adjacency.
- stylistic tokenization preference.
- dialect normalization.

Do NOT treat every one-letter Arabic token as an error.

## Decision evidence requirement

SUPPORTED_BOUNDARY_ERROR requires:
- G0-G3 all pass;
- one explicit M/S rule fires;
- morphology/lexical evidence independently supports it;
- no contradictory valid analysis creates unresolved ambiguity.

Otherwise:
- UNCERTAIN_BOUNDARY or REJECTED_BOUNDARY_ERROR.

## Unit-test obligation

Before evaluation, each rule must receive:
- >=5 positive synthetic/held-development-safe construction tests;
- >=5 negative trap tests;
- exact audit output showing triggered rule and morphology evidence.

Synthetic tests are software tests only and do not count toward scientific evaluation metrics.
