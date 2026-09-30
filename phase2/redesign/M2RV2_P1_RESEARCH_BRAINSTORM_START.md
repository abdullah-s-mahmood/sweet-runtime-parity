# M2-R v2 P1 — Fresh Research & Brainstorming Start

Date: 2026-09-30
Status: FROZEN BEFORE P1 PACKET OR JUDGMENT

## Trigger from P0

P0 failed because of two simultaneous defects:
- under-enumeration: CRR 82.22% but GELR only 29.14%;
- over-assertion: CFPR 60% on complete QALB human references.

The model often noticed that a sentence was problematic, but failed to enumerate all expert edits; at the same time, it invented mandatory errors in clean references. Confidence was not a useful safeguard because 23/24 clean false-positive claims were HIGH confidence.

## Fresh external evidence

1. Alhafni & Habash (ACL 2025) show that explicit text-edit representations are effective and interpretable for Arabic GEC, achieving state-of-the-art results on two benchmarks and comparable state of the art on two others, with substantially faster inference than prior Arabic GEC systems.
   https://aclanthology.org/2025.acl-long.875/

2. Mubarak et al. (EACL 2026), Nahw, show substantial remaining deficits in Arabic grammar understanding, detection, correction, and explanation even for strong LLMs. This argues against assuming that a single global self-judgment is sufficient.
   https://aclanthology.org/2026.eacl-long.296/

3. Haldar & Hockenmaier (Findings EMNLP 2025) report low intra-rater reliability for LLM-as-a-judge across repeated runs. Self-reported confidence therefore cannot be treated as a calibrated correctness signal.
   https://aclanthology.org/2025.findings-emnlp.1361/

4. Recent calibration work (EMNLP 2025) further shows that raw model confidence and correctness are separable and can require explicit calibration mechanisms.
   https://aclanthology.org/2025.emnlp-main.530/
   https://aclanthology.org/2025.emnlp-main.742/

## Alternatives challenged

### More aggressive scan only
Rejected. It may improve GELR while worsening the already unacceptable CFPR.

### More conservative output only
Rejected. It may reduce CFPR but worsen enumeration and strict residual recall.

### Confidence thresholding
Rejected for P1. P0 showed HIGH confidence on nearly all clean false positives.

### Case-specific few-shot examples from P0
Prohibited. This would overfit the consumed development set.

### Multi-agent panel
Deferred. The single permitted P1 must test whether a better task decomposition can fix the failure before adding correlated judges.

### Structured two-pass verifier
Selected.

The verifier must first enumerate plausible spans broadly, then independently classify each span as mandatory/optional/uncertain. A final category-by-category scan then searches for missed independent errors. Only spans that survive the mandatory test are returned as mandatory errors.

## P1 hypothesis

Separating candidate generation from mandatory-error adjudication can reduce false positives while preserving or improving enumeration, because the same reasoning act no longer has to simultaneously discover and approve a correction.

This is a structural prompt hypothesis, not a threshold change.

## Integrity constraints

- No P0 case-specific examples.
- No threshold changes.
- Fresh disjoint P1 packet only.
- QALB14 TRAIN/DEV complete-gold evidence only.
- No QALB15.
- No ZAEBUC DEV/TEST.
- No Confirmation/Holdout.
- No A7'ta reserve.
- No P2 after P1.
