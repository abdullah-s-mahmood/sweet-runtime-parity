# M2-R v2 P0 — End Research, Brainstorming, and Result Review

Date: 2026-09-30

## Scientific result

M2-R v2 P0 uses QALB14 complete human correction gold and frozen predictions committed before gold opening.

Result: **FAIL**

- Context Residual Recall (CRR): 82.22% vs >=85%
- Gold Error Localization Recall (GELR): 29.14% vs >=80%
- Clean False Positive Rate (CFPR): 60.00% vs <=5%
- Strict Residual Recall: 63.33% vs >=90%
- Claim Precision diagnostic: 63.47%
- Invalid Surface Rate: 0% (passes <=2%)

Confirmation, Holdout, and A7'ta reserve remain closed.

## What improved

### Scientific validity — IMPROVED strongly
v1.1 ArabiGEE target contexts were not exhaustive sentence-level clean gold. v2 uses QALB complete human corrections and M2 edit scripts, so clean controls and residual completeness are now interpretable.

### Context-level residual detection — descriptively improved
Against the prior ArabiGEE diagnostic, CRR moved from 51.11% to 82.22% (+31.11 pp).
This is descriptive only because the benchmark definition changed.

### Strict residual detection — slightly improved descriptively
Controlled/strict residual recall moved from 60.00% to 63.33% (+3.33 pp), again on a changed benchmark.

### Surface discipline — stable and strong
Invalid surface claims remain 0%.

## What worsened or remains unacceptable

### Clean false positives — severely unacceptable
CFPR is 60.00% against complete QALB references. The model is still inventing mandatory errors in many human-corrected sentences.

### Complete error enumeration — very weak
GELR is only 29.14%. The model often detects that a sentence has an error but fails to enumerate the full expert edit set.

### Strict near-complete residual detection — inadequate
63.33% is far below the >=90% safety target.

### Precision — insufficient
Only 63.47% of predicted mandatory-error claims match a gold surface exactly under the current diagnostic.

## Overall comparison

Versus M2-R v1.1:
- **Evaluation validity: IMPROVED materially**
- **CRR: descriptively improved**
- **Strict residual recall: slightly improved descriptively**
- **GELR: descriptively worsened (34.71% -> 29.14%, -5.57 pp), but not directly comparable**
- **Deployment readiness: UNCHANGED — not safe**
- **Arabic auto-apply: UNCHANGED — REVIEW-first**

Overall status: **MIXED technically, IMPROVED scientifically, NOT IMPROVED for deployment.**

## Fresh research synthesis

Recent Arabic evaluation work (Nahw; AraLingBench) shows strong LLMs still struggle with deep Arabic grammar and syntax despite surface fluency.

Recent GEC evaluation work argues for edit-focused evaluation because whole-sentence similarity is dominated by unchanged tokens.

Recent multilingual GEC evaluation also warns that one fixed reference may undercount valid corrections; therefore exact reference mismatch is not automatically a model error. For ACAD_PASS this means:
- exact edit matching is useful diagnostic evidence;
- production safety still requires distinguishing mandatory errors from valid alternatives.

Arabic text-editing research in 2025 achieved strong GEC performance using explicit edit representations, reinforcing the value of structured edit-level modeling instead of relying only on a free-form LLM judge.

## Brainstorming: why P0 failed

The failure pattern suggests two different problems:

1. **Over-detection / calibration problem**
   The model treats questionable or stylistic forms as mandatory errors, producing CFPR 60%.

2. **Enumeration problem**
   It can often recognize that a sentence is problematic (CRR 82.22%) but does not enumerate all gold edits (GELR 29.14%).

A single instruction such as "be stricter" would likely worsen the first problem while helping the second, repeating the P0/P1 safety-coverage tradeoff seen in M2.

## Candidate P1 strategies considered

### A. More aggressive scanning
Rejected as sole change: likely raises recall while worsening CFPR.

### B. More conservative threshold language
Rejected as sole change: likely lowers CFPR while worsening GELR/strict recall.

### C. Two-pass structured reasoning inside one prompt
Preferred candidate for the single allowed P1:
1. Pass 1: enumerate possible error spans exhaustively.
2. Pass 2: classify each candidate span as MANDATORY / OPTIONAL / UNCERTAIN.
3. Only MANDATORY survives to final output.
4. Require a minimal linguistic rule justification for every surviving error.
5. Explicitly prohibit style/literary normalization and redundant edits.
6. Perform a second scan for missed independent errors before finalizing.

This changes reasoning structure, not the evaluation threshold.

### D. Specialized deterministic/edit model fusion
Promising architecture, but not allowed to replace the single P1 experiment. Consider only after P1 closes.

## Decision before P1

Do **not** freeze P1 yet.

First perform aggregate error analysis on v2 P0:
- false-positive categories on CLEAN_QALB_REFERENCE;
- missed edit types on NATURAL/STRICT cases;
- number of cases where one error was found but additional edits were missed;
- orthography vs morphology vs syntax vs lexical failure distribution;
- whether false positives cluster around dialect/register/style/punctuation-like phenomena.

P1 may use only aggregate categories, never case-specific examples.

No threshold changes.
No Confirmation/Holdout.
No A7'ta reserve.
No P2 after P1.
