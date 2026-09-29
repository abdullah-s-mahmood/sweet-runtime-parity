# Post-Edit Stability & Morphological Identity — Research Start

Date: 2026-09-29

## Research signals

1. Multi-pass GEC research shows that iterative decoding/refinement can improve corrections and exposes cases where a first-pass output still requires editing. This motivates fixed-point/stability as a repair-completeness signal, not as a correctness oracle.
2. Context robustness work in GEC shows that local correction validity can depend on surrounding context, reinforcing the need to re-evaluate a correction in the corrected sentence rather than judging the token alone.
3. CAMeL Tools contextual morphology exposes lexical lemma, POS and inflectional features including person, aspect, voice, gender, number and clitic analyses. These features are directly relevant to failures such as clitic loss, tense/aspect drift and lexical substitution.
4. Previous ACAD_PASS evidence already falsified morphology analyzability/consensus as a correctness oracle. The current use is narrower: identity-preservation risk detection after independent candidate agreement.

## Falsifiable expectation

Post-edit stability should be more sensitive to incomplete/partial repairs. Morphological identity should be more sensitive to lexical/clitic/person/tense drift. Their conjunction may improve safety if the two error signals are complementary, but may also over-review legitimate spelling corrections.