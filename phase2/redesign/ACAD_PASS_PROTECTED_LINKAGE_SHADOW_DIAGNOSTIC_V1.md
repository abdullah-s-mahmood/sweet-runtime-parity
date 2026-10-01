# ACAD_PASS PROTECTED-LINKAGE SHADOW DIAGNOSTIC CONTRACT V1

Date: 2026-10-01
Status: SOURCE-ONLY DIAGNOSTIC CONTRACT
Addresses: Independent Review MAJOR M03
Decision authority: CURRENT FROZEN PROTECTION POLICY ONLY
Gold/reference use: FORBIDDEN

## 1. Purpose

Investigate whether the current protected-linkage policy blocks candidates because of a global word-ordinal change even when the protected entity and its local attachment remain unchanged.

This contract does NOT weaken, replace, or reinterpret the current protection gate.

The existing policy remains authoritative for executability.

## 2. Historical evidence boundary

V3 blocked outputs remain blocked exactly as frozen.

No historical P1/P2 hypothesis is promoted or rescued.

Shadow diagnostics are stored separately and are not legalizer outputs.

## 3. Required reason decomposition

For every current protection failure involving a protected span/linkage, classify source-only reasons independently:

- ENTITY_TEXT_CHANGED
- ENTITY_TYPE_CHANGED
- ENTITY_COUNT_CHANGED
- ENTITY_ORDER_CHANGED
- LOCAL_SEPARATOR_CHANGED
- LOCAL_ATTACHMENT_CHANGED
- DOCUMENT_LINKAGE_CHANGED
- CITATION_MOVED
- QUANTITY_UNIT_LINK_CHANGED
- PERCENT_LINK_CHANGED
- TECHNICAL_TOKEN_CHANGED
- GLOBAL_WORD_ORDINAL_CHANGED_ONLY
- ALIGNMENT_AMBIGUOUS
- ALIGNMENT_FAILED
- PROOF_BUDGET_EXCEEDED
- MULTIPLE_REASONS
- OTHER_FROZEN_GUARD_REASON

A UID may have multiple reasons.

## 4. Global-ordinal-only definition

A failure may be labelled:

`GLOBAL_WORD_ORDINAL_CHANGED_ONLY`

only if all are proven source-only:

1. protected entity text unchanged;
2. protected entity type unchanged;
3. number of protected entities unchanged;
4. protected entity relative order unchanged;
5. local separators around the entity unchanged under the frozen local-window definition;
6. local attachment/typed linkage unchanged;
7. no citation/quantity-unit/percent/document linkage moved;
8. alignment proof is unique and within budget;
9. the ONLY remaining failed frozen predicate is global whole-sentence word ordinal/count before/after the entity.

If any other reason exists, do not assign "only".

## 5. Local attachment shadow model

The shadow diagnostic may derive typed source-only entities:

- NUMBER
- UNIT
- PERCENT
- CITATION
- DOI
- URL
- EMAIL
- TECHNICAL_TOKEN
- EQUATION_TOKEN
- OTHER_FROZEN_PROTECTED_TYPE

For each entity record:

- source protected_id;
- source char span;
- output matched char span;
- entity type;
- exact text;
- preceding/following local tokens within a frozen window;
- typed partner IDs if the current extraction provides them;
- separator signature;
- local offset map.

No gold/reference information is permitted.

## 6. Frozen local window

For V1 diagnostics only:

- two whitespace tokens before;
- two whitespace tokens after;

plus any directly linked typed entity under the frozen source extractor.

This window is descriptive.
It is not a new protection policy.

Changing it requires a new diagnostic version.

## 7. Shadow-policy result

For every candidate:

- `FROZEN_POLICY = PASS|FAIL`
- `SHADOW_LOCAL_LINKAGE = PASS|FAIL|INCONCLUSIVE`
- `DISAGREEMENT_CLASS`

Allowed disagreement classes:

- BOTH_PASS
- BOTH_FAIL
- FROZEN_FAIL_SHADOW_PASS_GLOBAL_ORDINAL_ONLY
- FROZEN_FAIL_SHADOW_INCONCLUSIVE
- FROZEN_PASS_SHADOW_FAIL
- ALIGNMENT_UNAVAILABLE

The shadow result NEVER changes executability.

## 8. Mandatory synthetic tests

M03-S01:
add an unrelated word at the beginning while an unchanged "5 mg" entity remains locally attached.
Expected:
frozen policy may fail;
shadow local linkage PASS;
class GLOBAL_ORDINAL_ONLY if no other reason.

M03-S02:
same for unchanged citation "[1]".

M03-S03:
move citation "[1]" to another clause.
Expected:
shadow FAIL; not global-ordinal-only.

M03-S04:
change "5 mg" to "6 mg".
Expected:
ENTITY_TEXT_CHANGED / quantity linkage fail.

M03-S05:
change "5 mg" to "5 g".
Expected:
UNIT/linkage failure.

M03-S06:
insert token between quantity and unit so local relationship changes.
Expected:
LOCAL_ATTACHMENT_CHANGED.

M03-S07:
duplicate protected citation.
Expected:
ENTITY_COUNT_CHANGED.

M03-S08:
swap order of two protected citations.
Expected:
ENTITY_ORDER_CHANGED or DOCUMENT_LINKAGE_CHANGED.

M03-S09:
alignment ambiguity around repeated identical protected text.
Expected:
INCONCLUSIVE or FAIL; never shadow PASS.

M03-S10:
proof-budget exhaustion.
Expected:
INCONCLUSIVE; never shadow PASS.

## 9. Stage 1 reporting

For each proposer report over D_all:

- frozen protection PASS count;
- frozen protection FAIL count;
- shadow local PASS/FAIL/INCONCLUSIVE;
- disagreement matrix;
- global-ordinal-only UID count;
- global-ordinal-only cluster count;
- reason-combination counts by protected type.

Do NOT report:
- recovered useful corrections;
- protection false-positive rate;
- correctness.

## 10. Stage 2 interpretation

If source-only Stage 2 later shows material frozen-vs-shadow disagreement:

- preserve current policy;
- freeze disagreement artifact;
- perform separate architecture review;
- if a new protection policy is proposed, give it a new version;
- re-run source-only legalizer under the new policy in a new lane before any gold-aware evaluation.

No post-gold relaxation is allowed.

## 11. Product/document structure note

This diagnostic remains a text-level approximation.

It does not claim full document-semantic linkage safety.

Future DOCX/LaTeX structured-document protection may supersede text-only ordinal/linkage heuristics with explicit document-object identities.

## 12. Scientific boundary

This diagnostic can reveal over-conservative structural mechanisms.

It cannot determine whether a blocked correction is linguistically useful without a later separately authorized evaluation.
