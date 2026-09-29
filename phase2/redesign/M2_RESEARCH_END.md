# M2 — Fresh Research End

Date: 2026-09-30

## Evidence after P0 and P1

The two frozen verifier prompts reveal a safety–coverage instability:
- P0 was conservative and relatively safe but had very low useful coverage.
- P1 relaxed style/register overcorrection and improved coverage sharply, but near-complete residual errors escaped.

This behavior is consistent with recent external evidence.

## Fresh literature

### Multilingual LLM-as-a-Judge reliability
Fu & Liu, Findings EMNLP 2025, evaluate five judge models across 25 languages and report low consistency, with average Fleiss' kappa around 0.3 and weaker behavior in low-resource languages. Increasing model scale or multilingual training alone did not guarantee consistency.
https://aclanthology.org/2025.findings-emnlp.587/

### General judge variability
Bavaresco et al., ACL 2025 JUDGE-BENCH, find substantial judge variability across tasks, models, properties, expertise levels and human/model-generated text.
https://aclanthology.org/2025.acl-short.20/

Haldar & Hockenmaier, Findings EMNLP 2025, document low intra-rater reliability across repeated LLM-as-a-judge runs.
https://aclanthology.org/2025.findings-emnlp.1361/

### Abstention is itself difficult
Madhusudhan et al., COLING 2025, show even strong closed and open models struggle with abstention, though strict prompting/CoT can help.
https://aclanthology.org/2025.coling-main.627/

Wen et al., TACL 2025 survey abstention as a safety mechanism and emphasize task-specific calibration rather than assuming abstention is a universal meta-capability.
https://aclanthology.org/2025.tacl-1.26/

### Fixed-reference GEC evaluation can be misleading
Rozovskaya & Roth, ACL 2026, show fixed human references can underestimate valid corrections because multiple correct outputs exist; closest-gold evaluation correlates better with human judgments.
https://aclanthology.org/2026.acl-long.2193/

Goto et al., TACL 2026, motivate edit-focused evaluation because sentence similarity is dominated by unchanged tokens.
https://aclanthology.org/2026.tacl-1.77/

### Arabic-specific evidence
Nahw, EACL 2026, shows strong LLMs still have substantial deficits in Arabic grammar, with GPT-4o averaging 67% across the benchmark tasks and natural high-quality data outperforming synthetic-only fine-tuning.
https://aclanthology.org/2026.eacl-long.296/

QALB annotation guidelines explicitly note that punctuation can be stylistic and ask annotators to avoid over-correcting informal/colloquial style. This supports the forensic separation between mandatory errors and reference-only differences.

ARETA provides a structured Arabic error taxonomy and reports 85.8% micro-F1 on a manually annotated blind ALC portion; Hamza errors are a distinct orthographic category.
https://aclanthology.org/2021.conll-1.47/

## End research conclusion

A single absolute sentence-level frontier judge should not be the final Arabic safety oracle. The literature and M2 both support a more decomposed, auditable architecture:
- edit validity/necessity;
- explicit residual-error span detection;
- deterministic/specialized checks for low-level orthography/morphology;
- semantic preservation;
- selective abstention.

The next experiment should change the *task formulation*, not merely loosen/tighten the same prompt.
