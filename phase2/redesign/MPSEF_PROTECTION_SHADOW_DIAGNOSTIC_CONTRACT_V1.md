# MP-SEF PROTECTION SHADOW DIAGNOSTIC CONTRACT V1

Date: 2026-10-01
Status: FROZEN SOURCE-ONLY DIAGNOSTIC CONTRACT
Addresses: Independent Review MAJOR M03
Gold/reference use: FORBIDDEN
Authoritative legalizer policy: UNCHANGED

## 1. Purpose

Investigate whether the current protected-attachment policy sometimes blocks distant source edits solely because a protected entity's global word ordinal changes, even when the entity text and local attachment remain unchanged.

This contract is DIAGNOSTIC ONLY.

It MUST NOT:
- weaken current protection;
- make any blocked V3 hypothesis executable;
- retroactively rescue any of the 112 P1 protected-blocked cases;
- alter V3 action artifacts;
- use gold/reference correctness.

## 2. Governing principle

The current legalizer remains authoritative.

For each source/output pair the system records:
1. current-authoritative protection result;
2. diagnostic decomposition of WHY it blocked/passed;
3. optional shadow-policy result;
4. disagreement reason.

Shadow PASS never overrides authoritative FAIL.

## 3. Diagnostic reason taxonomy

Every protected-attachment failure is decomposed into one or more of:

- ENTITY_TEXT_CHANGED
- ENTITY_COUNT_CHANGED
- ENTITY_ORDER_CHANGED
- LOCAL_SEPARATOR_CHANGED
- LOCAL_ATTACHMENT_CHANGED
- LOCAL_CONTEXT_CHANGED
- GLOBAL_ORDINAL_ONLY_CHANGED
- CITATION_MOVED
- NUMBER_UNIT_LINK_CHANGED
- PERCENT_LINK_CHANGED
- TECHNICAL_TOKEN_LINK_CHANGED
- ALIGNMENT_AMBIGUOUS
- ALIGNMENT_FAILED
- PROOF_BUDGET_EXCEEDED
- OTHER_FROZEN_GUARD_REASON

A UID may have multiple reasons.

## 4. Global-ordinal-only definition

A candidate is tagged `GLOBAL_ORDINAL_ONLY_CHANGED` only if ALL are true:

1. protected entity text is byte/text identical;
2. entity count is unchanged;
3. entity order relative to other protected entities is unchanged;
4. source/output entity mapping is unambiguous;
5. local separator around entity is unchanged under frozen local definition;
6. local attachment/link target is unchanged;
7. typed entity category is unchanged;
8. only the number of ordinary words/tokens before or after the entity differs because of edits outside the local attachment window.

If any stronger failure exists, do not label the case ordinal-only.

## 5. Local attachment window

For diagnostics only, define local context from source-derived typed spans.

Record:
- nearest non-whitespace token left;
- nearest non-whitespace token right;
- punctuation/separator characters between entity and neighbors;
- linked unit/citation marker if defined by source-only extraction;
- stable source span IDs.

The shadow policy compares these structural relationships rather than total sentence word ordinal.

This does NOT become the active protection policy in V1.

## 6. Shadow result states

- SHADOW_PASS_LOCAL_ATTACHMENT_STABLE
- SHADOW_FAIL_ENTITY_CHANGED
- SHADOW_FAIL_LOCAL_ATTACHMENT_CHANGED
- SHADOW_FAIL_LINK_CHANGED
- SHADOW_FAIL_ALIGNMENT
- SHADOW_UNKNOWN

The authoritative result is stored separately.

## 7. Required synthetic cases

M03-S01:
source contains `الجرعة 5 mg يوميا`;
insert an unrelated word at sentence start;
entity and local attachment unchanged.
Expected:
- authoritative may report ordinal change;
- diagnostic must identify GLOBAL_ORDINAL_ONLY_CHANGED;
- shadow may PASS.

M03-S02:
same source;
move `5 mg` away from its linked context.
Expected shadow FAIL.

M03-S03:
change `5 mg` to `6 mg`.
Expected shadow FAIL ENTITY_TEXT_CHANGED.

M03-S04:
keep number but change unit `mg -> g`.
Expected shadow FAIL NUMBER_UNIT_LINK_CHANGED or entity change.

M03-S05:
citation `[1]` unchanged, unrelated prefix word inserted.
Expected ordinal-only diagnostic if local relation unchanged.

M03-S06:
move citation `[1]` to a different clause.
Expected shadow FAIL CITATION_MOVED/LOCAL_ATTACHMENT_CHANGED.

M03-S07:
insert punctuation directly between protected entity and its attachment.
Expected shadow FAIL LOCAL_SEPARATOR_CHANGED when relevant.

M03-S08:
ambiguous repeated identical protected entities.
Expected SHADOW_FAIL_ALIGNMENT or SHADOW_UNKNOWN, never automatic PASS.

## 8. Population diagnostics when Stage 2 is later authorized

For each proposer report over all source-only rows:

- authoritative protected-block count;
- GLOBAL_ORDINAL_ONLY_CHANGED count;
- shadow-policy disagreement count;
- counts by protected entity type;
- distinct clusters affected;
- overlap with alignment ambiguity/budget failures.

Do not report:
- false-positive protection;
- useful repair recovered;
- correctness gain.

Those require external correctness evidence.

## 9. Relationship to 112 historical P1 blocks

The 112 V3 P1 protected-blocked rows remain frozen exactly as historical evidence.

This diagnostic may later classify reason structure on source-only copies, but:
- their V3 terminal states remain unchanged;
- no action is added to V3;
- no historical metric is recomputed.

## 10. Activation rule for any future lighter policy

A future active protection-policy change requires:

1. separate version;
2. source-only synthetic PASS;
3. document-structure/linkage review;
4. independent review;
5. new preflight;
6. no retroactive change to V3;
7. evaluation only under a newly authorized experiment.

## 11. Scientific boundary

This contract diagnoses overblocking mechanisms only.

It does not prove that blocked candidate text is correct or useful.
