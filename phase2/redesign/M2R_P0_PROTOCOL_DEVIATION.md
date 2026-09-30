# M2-R P0 — Protocol Deviation and Compliant Re-score

Date: 2026-09-30

The frozen M2-R protocol excluded QALB15 and ZAEBUC DEV/TEST. Post-gold analysis of the ArabiGEE-derived P0 packet showed 86 QALB14-dev cases, 27 QALB15-dev cases, and 7 ZAEBUC-dev cases. Thus 34/120 cases (28.33%) violated the source-exclusion rule, although the raw excluded corpora were not opened directly.

The original 120-case P0 result remains diagnostic only. Using the same frozen predictions (SHA-256: 5cc66688e544ed91bf6a77852f199a6851f05ca8b6d93da36b9748bdee1a76be), the protocol-compliant QALB14-dev-only subset contains 86 cases:

- CRR: 41/64 = 64.06% — FAIL vs >=85%
- GELR: 47/92 = 51.09% — FAIL vs >=80%
- CFPR: 12/22 = 54.55% — FAIL vs <=5%
- NCWR: 19/24 = 79.17% — FAIL vs >=90%
- Claim precision: 45/150 = 30.00%
- Invalid-surface rate: 0/150 = 0%

Dimension recall:
- Orthography: 39/64 = 60.94%
- Morphology: 14/23 = 60.87%
- Syntax: 2/9 = 22.22%
- Lexical: 2/13 = 15.38%

Therefore the provenance violation does not explain the failure. M2-R P0 still fails clearly on the compliant subset.

P1, if executed, must use a fresh packet filtered to QALB14-dev before sampling, be disjoint from every QALB14 context already exposed in P0, and leave Confirmation/Holdout closed. If a sufficiently large compliant disjoint packet cannot be built, stop M2-R rather than relax the source rule post hoc.