# M2 P1 — Unsafe-Accept Forensic Audit

Date: 2026-09-30  
Workflow: 36646367644  
Purpose: interpret the nine reference-partial cases accepted by P1 without changing the preregistered gate.

## Strict preregistered result

P1 accepted 9/48 construction-unsafe cases = 18.75% UAR.

That result remains the official gate result. The audit does not change thresholds or relabel the experiment post hoc.

## Reference-quality caveat

Recent GEC evaluation research and QALB guidelines both warn that a fixed reference does not enumerate every acceptable correction. In particular, punctuation and register/dialect edits can be optional or variable. Therefore we audited the exact withheld expert edits in the nine accepted partial constructions.

## Audit findings

- M2P1D-015: withheld comma insertion — potentially stylistic/register-sensitive.
- M2P1D-025: `متل → مثل` — dialect-to-MSA normalization; linguistic necessity depends on register policy.
- M2P1D-041: `ايران → إيران` — clear Hamza orthographic correction.
- M2P1D-047: `اغلب → أغلب` — clear Hamza orthographic correction.
- M2P1D-054: `اكبر → أكبر` — clear Hamza orthographic correction.
- M2P1D-072: withheld comma insertion — potentially optional.
- M2P1D-103: `واش → وما` — dialect/register normalization; not automatically mandatory under a register-preserving policy.
- M2P1D-113: withheld comma insertion — potentially optional.
- M2P1D-117: ONE_OF_MANY case; withheld edits are dominated by punctuation/deletion of dot sequences.

## Robust safety conclusion

Even under the maximally charitable interpretation—treating all six punctuation/dialect/reference-sensitive cases as acceptable—three accepted cases contain clear mandatory Hamza spelling errors.

Thus at least 3 of the 48 reference-unsafe development cases are unquestionably unsafe ACCEPTs = **6.25%**, already above the preregistered 5% ceiling.

Therefore the M2 safety failure is not an artifact of punctuation-only or single-reference strictness.

## Additional implication

The concentration of clear misses in simple Hamza orthography is especially important: a frontier semantic/reasoning judge can overlook low-level residual errors that a deterministic or specialized orthographic checker may detect cheaply. This supports decomposition rather than adding more general-purpose judge agents.
