# Residual GED Target-Clean — Research End

Date: 2026-09-29

## Research conclusion

Current GEC literature supports the observed result rather than contradicting it.

- Correction Acceptability Discrimination (Cao et al., LREC-COLING 2024) explicitly targets sentence-level correctness after a proposed correction and reports gains from discriminating invalid correction combinations.
- Detection-correction architectures show that explicit error detection can strengthen correction systems, but detection is not equivalent to proof that a repair is complete.
- Recent edit-voting and ensemble work shows that consensus can reduce over-correction without eliminating correlated errors.
- Arabic grammar evaluation remains difficult even for strong models, supporting conservative escalation instead of broadening local rules.

## Consequence for ACAD_PASS

Residual GED is retained as a useful independent risk feature, but the zero-unsafe auto-accept hypothesis is closed.

The next scientifically differentiated direction is a pairwise/source-candidate **acceptability discriminator**, evaluated as a safety/ranking layer on consumed evidence before any new disjoint population.
