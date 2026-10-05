# AT0-EN V2.6-DEV Internal Evidence Review and Implementation Authorization V1

Date: 2026-10-05
Status: INTERNAL TECHNICAL REVIEW / BOUNDED DEV IMPLEMENTATION AUTHORIZED

## Governance

Under the user-approved consultation-minimization rule, this development change does not require another higher-model consultation because:
- it is isolated to a new development version;
- it does not alter or rerun frozen FactPICO evidence;
- it is reversible before any external validation;
- the repair scope is already localized by frozen evidence.

This is NOT an independent external scientific review.

## Competing hypotheses considered

H1: final REVIEW policy alone is too conservative.
Rejected as primary repair target: all 345 frozen records contain upstream assertion uncertainty, and relaxing REVIEW would risk unsafe promotion.

H2: relation handling is the dominant bottleneck.
Rejected for the current repair: frozen relation-alignment rows were zero across all 345 FactPICO records.

H3: extraction/segmentation/representation creates pervasive local uncertainty.
Supported: 345/345 records contain assertion uncertainty; preserved short fragments and markup artifacts were observed.

H4: unequal-count grouping amplifies local uncertainty.
Strongly supported: 339/345 records use non-1:1 groups; current code appends all leftovers to the final group.

H5: the problem is only insufficient biomedical predicate vocabulary.
Plausible but not yet sufficient to justify broad R4 implementation. R4 remains conditional after R1-R3 development evidence.

## External research check

Peer-reviewed clinical NLP literature independently supports treating sentence boundary detection as a domain-specific preprocessing problem rather than a trivial general-English split:
- Xu et al. (2024), "Automatic sentence segmentation of clinical record narratives in real-world data": clinical text contains fragmented/ungrammatical structures and domain-specific segmentation materially improves performance.
- Knoll et al. (2019), "Recurrent Deep Network Models for Clinical NLP Tasks: Use Case with Sentence Boundary Disambiguation": general-domain segmentation performs poorly on clinical documentation.
- Lilli et al. (2025), "Improving Clinical Report Classification with Sentence Boundary Detection": sentence segmentation improved downstream clinical classification and interpretability.

RCT/PICO literature also supports section-aware and PICO-specific representation:
- EBM-NLP provides ~5,000 annotated RCT abstracts for PICO development.
- Section-specific PICO extraction work reports that title/method sections contain most PICO information and highlights annotation/representation complexity.

These sources support R1 and the later use of independent RCT material, but they do not justify benchmark-specific tuning.

## Internal verdict

AUTHORIZED FOR IMPLEMENTATION:
- R1 boundary/markup normalization;
- R2 localized assertion confidence;
- R3 exact partial alignment with explicit unmatched nodes;
- deterministic development mechanics suite.

NOT AUTHORIZED YET:
- R4 broad biomedical predicate expansion;
- changing final safety ordering;
- FactPICO rerun/rescoring;
- using FactPICO as a development acceptance set;
- external validation.

## Development order

1. Freeze a deterministic mechanics test suite independent of FactPICO.
2. Implement R1-R3 in AT0-EN V2.6-DEV only.
3. Run the mechanics suite.
4. If mechanics pass, add an independent real-RCT stress diagnostic selected outside FactPICO.
5. Decide whether R4 is necessary from development-only evidence.
6. Stop before any external validation or production claim.
