# MP-SEF SHADOW PROTECTION DIAGNOSTICS CONTRACT V1

Date: 2026-10-01
Status: FROZEN SOURCE-ONLY DIAGNOSTIC CONTRACT
Closes design portion of: Independent Review MAJOR M03
Gold/reference use: FORBIDDEN
V3 protection decision: UNCHANGED / AUTHORITATIVE

## 1. Purpose

The current V3 protection policy can emit:
`PROTECTED_ATTACHMENT_ORDINAL_CHANGED`

when the number of whitespace tokens before/after a protected entity changes,
even if the protected entity text, local separator, and local attachment remain intact.

This contract introduces SHADOW DIAGNOSTICS ONLY.

It does NOT:
- relax V3 protection;
- rescue any historical blocked action;
- change any frozen executable-action artifact;
- label a blocked action as correct/useful;
- use gold/reference.

## 2. Governing principle

For every protected entity touched by source->output analysis, separate these causes:

1. ENTITY_TEXT_CHANGED
2. ENTITY_CREATED_OR_DELETED
3. LOCAL_SEPARATOR_CHANGED
4. LOCAL_ATTACHMENT_CHANGED
5. GLOBAL_ORDINAL_ONLY_CHANGED
6. CITATION_MOVEMENT
7. NUMBER_UNIT_LINKAGE_CHANGED
8. PERCENT_LINKAGE_CHANGED
9. DOCUMENT_STRUCTURE_LINKAGE_CHANGED
10. ALIGNMENT_AMBIGUOUS
11. ALIGNMENT_FAILED
12. ALIGNMENT_BUDGET_EXCEEDED
13. MULTIPLE_CAUSES

The current V3 legalizer result remains the only authoritative legal/blocked state.

## 3. Global-ordinal-only definition

A protected span qualifies as:

`GLOBAL_ORDINAL_ONLY_CHANGED`

only when ALL are true:

- protected signature unchanged;
- protected entity text unchanged;
- unique contiguous source->output mapping proven;
- left local separator unchanged;
- right local separator unchanged;
- local attachment signature unchanged;
- no entity movement relative to its local attachment;
- no number-unit/percent/citation/document-linkage change;
- only the global left/right whitespace-token counts differ.

This state is diagnostic only.

## 4. Local attachment signature

For each protected span derive a source-only local signature from a bounded context window.

Required fields:

- protected category;
- exact protected text;
- immediate left separator;
- immediate right separator;
- nearest non-whitespace lexical token on left, if any;
- nearest non-whitespace lexical token on right, if any;
- punctuation directly attached on left/right;
- typed neighboring protected entity IDs, if any;
- source character offsets;
- output mapped character offsets.

The context window must be defined by source structure only.

No gold/reference token may enter the signature.

## 5. Linkage-specific diagnostics

### Citation

Record:
- citation text identity;
- local lexical anchor identity;
- movement across sentence/structural boundaries;
- separator changes;
- ordinal-only disagreement.

### Number + unit

Record:
- number identity;
- unit identity;
- distance/separator relation;
- order;
- whether another number/unit became the nearest partner.

### Percent

Record:
- numeric identity;
- percent symbol identity;
- adjacency/separator relation.

### Technical/Latin token

Record:
- token identity;
- immediate lexical/punctuation attachment;
- whether only distant token count changed.

### Equation/document structure

Record:
- exact structure/entity identity;
- local boundary identity;
- movement across structural markers.

## 6. Shadow policy

A shadow diagnostic MAY compute what a more local linkage policy would have done.

Allowed outputs:

- V3_BLOCKED_SHADOW_BLOCKED
- V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY
- V3_PASS_SHADOW_PASS
- V3_PASS_SHADOW_BLOCKED
- SHADOW_INCONCLUSIVE

Important:

`V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY`

does NOT mean:
- false positive;
- useful repair recovered;
- correct correction;
- safe correction.

It means only that the V3 block is attributable to the global-ordinal rule under the shadow local-linkage definition.

## 7. Required synthetic tests

M03-S01:
source `الجرعة 5 mg يوميا`
output adds a distant word before the phrase while preserving `5 mg` and local linkage.
Expected:
- V3 may block ordinal;
- shadow classification = GLOBAL_ORDINAL_ONLY_CHANGED.

M03-S02:
source `كما ورد [1] هنا`
output adds a distant lexical word before the citation.
Expected:
- same citation/local attachment preserved;
- global ordinal diagnostic isolated.

M03-S03:
move `[1]` to a different local anchor.
Expected:
- CITATION_MOVEMENT / LOCAL_ATTACHMENT_CHANGED;
- shadow MUST NOT call ordinal-only.

M03-S04:
change `5 mg` to `6 mg`.
Expected:
- ENTITY_TEXT_CHANGED / NUMBER_UNIT_LINKAGE_CHANGED.

M03-S05:
keep number and unit strings but separate/reassociate them with another number/unit.
Expected:
- linkage change, not ordinal-only.

M03-S06:
change only separator directly adjacent to protected span.
Expected:
- LOCAL_SEPARATOR_CHANGED.

M03-S07:
alignment ambiguous.
Expected:
- ALIGNMENT_AMBIGUOUS;
- no local-pass claim.

M03-S08:
alignment work budget exceeded.
Expected:
- ALIGNMENT_BUDGET_EXCEEDED;
- no local-pass claim.

M03-S09:
multiple simultaneous causes.
Expected:
- all specific reasons preserved + MULTIPLE_CAUSES.

M03-S10:
identity output.
Expected:
- no diagnostic disagreement.

## 8. Stage-2 source-only reporting

If Stage 2 is later authorized, report for each proposer:

- total V3 protected-blocked UIDs;
- blocked UID count by reason;
- distinct cluster count by reason;
- GLOBAL_ORDINAL_ONLY_CHANGED UID/cluster count;
- V3_BLOCKED_SHADOW_WOULD_PASS_LOCAL_ONLY count;
- alignment ambiguous/budget-exceeded count;
- multiple-reason count.

Denominator:
ALL authorized Stage-2 source UIDs.

No blocked row is removed from denominator.

## 9. Population interpretation

Source-only diagnostics may answer:

- how often global ordinal logic contributes to blocking;
- which protected entity categories are affected;
- whether the issue is concentrated in certain proposer families;
- how much candidate availability changes under a shadow policy.

They may NOT answer:

- whether the blocked edits are correct;
- whether V3 has a false-positive rate;
- whether shadow policy is safer/better;
- whether a blocked correction should be rescued.

Those require a separately authorized evaluation.

## 10. Future policy change rule

Any future protection-policy relaxation requires:

1. a NEW protection-policy version;
2. source-only synthetic regression suite;
3. separate independent review;
4. new source-only action artifacts;
5. new measurement protocol/guard if gold-aware evaluation follows.

Historical V3 artifacts remain unchanged.

## 11. M03 closure status

M03 DESIGN is CLOSED when:
- this contract is frozen;
- shadow diagnostic implementation exists;
- M03-S01..S10 PASS.

M03 POPULATION IMPACT remains UNKNOWN until a later authorized source-only population run.

No gold is required for design/implementation closure.
