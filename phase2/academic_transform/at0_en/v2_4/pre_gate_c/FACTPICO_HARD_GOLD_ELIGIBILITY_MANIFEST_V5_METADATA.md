# FactPICO H1 V5 Eligibility Manifest Metadata

Date: 2026-10-04

Canonical local manifest:
`FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5.csv`

Rows:
`345`

SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

The manifest contains metadata/hashes only and no raw source/candidate text.

## Frozen reconstruction inputs

FactPICO ZIP SHA-256:
`ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`

Primary gold CSV SHA-256:
`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

Record ID:
`SHA256("FACTPICO_REC_V1\0" + source_sha256 + "\0" + model_type + "\0" + candidate_sha256)`

Source cluster:
`SHA256(exact Abstract text)`

## Frozen V5 class counts

- SAFE_STRICT_CONTROL: 34 records / 33 source clusters
- ERROR_STRICT: 149 records / 83 source clusters
- INTERMEDIATE: 153 records / 84 source clusters represented
- N_A_SOURCE_DIAGNOSTIC: 9 records / 3 source clusters

## Frozen V5 class rules

N_A_SOURCE_DIAGNOSTIC:
source cluster contains any released PICO value 0/N/A.

SAFE_STRICT_CONTROL:
- source not N/A-excluded;
- Population=4;
- Intervention=4;
- Comparator=4;
- Outcome=4;
- Results=4;
- no exact Added Information span row for canonical source/candidate;
- source cluster not among the 15 clusters with unresolved Added Information candidate identity.

ERROR_STRICT:
source not N/A-excluded AND:
- non-double-PICO record has any applicable P/I/C/O <=2;
OR
- double-PICO aggregate record has any applicable P/I/C/O <=1.5.

Results does NOT independently trigger ERROR_STRICT.

INTERMEDIATE:
all other non-N/A records.

## Model distributions

SAFE_STRICT_CONTROL:
- ALPACA 33
- GPT-4 1
- LLAMA-2 0

ERROR_STRICT:
- ALPACA 35
- GPT-4 45
- LLAMA-2 69

INTERMEDIATE:
- ALPACA 44
- GPT-4 66
- LLAMA-2 43

N_A_SOURCE_DIAGNOSTIC:
- 3 per model

## Safety bound

ERROR_STRICT source-cluster denominator:
`83`

If zero unsafe automatic-PASS source clusters:

one-sided exact 95% upper bound:
`1 - 0.05^(1/83) ≈ 3.54496%`

## Status

This metadata freezes the V5 manifest identity.

The actual deterministic manifest file must be regenerated and byte-hash verified during:
`FACTPICO H1 ADAPTER + INPUT/GOLD MANIFEST IMPLEMENTATION FREEZE`

No V2.4 prediction is authorized.
