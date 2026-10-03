# AT0-EN V2.4 — Gate B2 Extraction-to-Alignment Bridge Contract V1

Date: 2026-10-03
Status: FROZEN PRE-IMPLEMENTATION

## Purpose

Define the only allowed mechanical transformation from the frozen A2 extraction graph to the frozen B1 alignment graph schema.

The bridge is not a semantic repair model.

## Assertion field mapping

For every extracted assertion:

- B1 `id` <- A2 `assertion_id`
- B1 `criticality` <- A2 `criticality`
- B1 `subject` <- A2 `subject`
- B1 `predicate` <- A2 `predicate_normalized`
- B1 `object` <- A2 `object`
- B1 `polarity` <- A2 `polarity`
- B1 `modality` <- A2 `modality`
- B1 `causality` <- A2 `causality`
- B1 `scope` <- A2 `scope_operators`
- B1 `time` <- A2 `temporal_context`
- B1 `population` <- A2 `population`
- B1 `baseline` <- A2 `baseline`
- B1 `confidence_status` <- A2 `extraction_status`
- B1 `evidence` <- exact quote from the first referenced A2 evidence span

## Binding conversion

Bindings may be created only from anchors explicitly referenced by that extracted assertion.

Allowed mechanical conversions:

- one VALUE anchor -> `value`
- one UNIT anchor -> `unit`
- one SEED anchor -> `seed`
- COUNT anchors -> `count_1`, `count_2`, ...
- SYMBOL anchors -> `symbol_1`, `symbol_2`, ...
- EQUATION anchors -> `equation_1`, `equation_2`, ...
- other explicitly referenced deterministic anchors -> stable type-indexed scalar keys

If multiple anchors make ownership ambiguous:
- preserve them as separate indexed keys;
- do not guess which value belongs to which entity.

## Relations

The frozen A2 extractor emits no semantic relations.

Therefore B2 bridge output must use:

`relations: []`

The bridge MUST NOT infer:
- CITES
- PRECEDES
- DEFINES
- RELATIVE_TO
- DISTINCT_FROM
- equation-symbol ownership
- or any other missing relation.

This intentional limitation is part of the B2 degradation measurement.

## Invalid conditions

Return an invalid bridge record if:
- an assertion references a missing evidence span;
- an assertion references a missing anchor;
- an enum value cannot map to B1 schema;
- no assertions are produced for non-empty raw text.

Invalid bridge records are reported separately and cannot be treated as PASS.

## Leakage prohibition

The bridge must not read:
- B1 gold alignment mappings;
- expected pair outcome;
- source graph when bridging candidate extraction;
- candidate graph when bridging source extraction;
- scenario class to alter behavior.

## Versioning

Any later change to this bridge creates a new B2 repair version and requires preserving the first B2 result.
