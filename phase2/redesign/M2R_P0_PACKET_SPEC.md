# M2-R Development Packet Specification v1

Date: 2026-09-30
Status: FROZEN BEFORE PACKET MATERIALIZATION

Use DEVELOPMENT contexts only from the partition in M2R_RESIDUAL_SPAN_PROTOCOL_V1.

Packet size: 120 unique context IDs:
- 60 NATURAL_ERROR_CONTEXT
- 30 CLEAN_TARGET_CONTEXT
- 30 ALL_BUT_ONE_RESIDUAL

No context ID may appear in more than one family.

## Selection order

1. Build all reconstructable ALL_BUT_ONE candidates.
2. Hash-rank and select 30.
3. From remaining DEVELOPMENT context IDs, hash-rank and select 60 natural error contexts.
4. From remaining DEVELOPMENT context IDs, hash-rank and select 30 clean target contexts.

Salt: `M2R-P0-DEV-A`.

## ALL_BUT_ONE construction

A context is eligible only when:
- it contains at least two distinct expert error/correction pairs;
- every erroneous surface maps uniquely in the source context;
- mapped spans do not overlap;
- applying all expert corrections reconstructs the expert target context after whitespace normalization;
- after applying all but one correction, the withheld erroneous surface remains uniquely present.

The withheld pair is chosen deterministically by hash.

## Blinding

Blind artifact contains only:
- case_id
- candidate sentence

Gold key contains:
- origin context ID
- family
- expert residual annotations needed for scoring
- source dataset
- construction metadata.

The verifier never receives the gold key, source/reference family, or original erroneous/reference sentence pair.

## Quality gates before judgment

- exactly 120 blind cases;
- exactly 120 key rows;
- 0 duplicate context IDs;
- 0 family overlap by context;
- 30 reconstructable ALL_BUT_ONE cases;
- at least 20 orthographic gold error instances across error-containing cases;
- at least 20 total morphology+syntax+lexical instances across error-containing cases;
- CONFIRMATION/HOLDOUT cases absent from both artifacts.
