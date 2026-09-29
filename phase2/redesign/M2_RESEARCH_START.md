# M2 — Fresh Research Start: Frontier Reasoning Verifier

Date: 2026-09-30
Status: PRE-REGISTERED BEFORE ANY M2 VERIFIER JUDGMENT

## Goal

Test whether one strong frontier reasoning model can act as a selective Arabic correction verifier over expert-grounded cases, without using the expert reference in the judge input.

The question is not whether the model can generate good Arabic. The question is:

> Given SOURCE and CANDIDATE only, can the verifier safely decide whether to KEEP, accept a repair, reject an erroneous/unrepaired candidate, or abstain when the repair is incomplete/uncertain?

## Fresh research findings

1. Kobayashi et al. (BEA 2024), *Large Language Models Are State-of-the-Art Evaluator for Grammatical Error Correction*, reports that GPT-4 achieved Kendall rank correlation 0.662 with human GEC judgments, outperforming existing automatic metrics in that study. This supports testing a strong LLM as an evaluator, not treating it as ground truth.

2. Kobayashi et al. (TACL 2024), SEEDA, shows that edit-level and sentence-level human judgment granularity matter and that traditional metrics can degrade on fluent neural corrections. M2 therefore scores correction correctness and repair completeness separately.

3. Bavaresco et al. (ACL 2025), JUDGE-BENCH, finds substantial variance in LLM judge reliability across tasks, judge expertise levels, and human/model-generated text. M2 therefore requires validation against expert-grounded evidence and source-stratified reporting.

4. Xu et al. (ACL 2025), ContextualJudgeBench, shows contextual evaluation is specifically challenging. M2 must give the full sentence and cannot assume isolated edit correctness implies contextual correctness.

5. Jourdan et al. (ACL 2025), scientific revision evaluation, finds LLM judges useful for instruction-following but weaker on correctness; hybrid evaluation with task-specific metrics is more reliable. Scientific fidelity therefore remains outside M2's linguistic success claim.

6. Östling et al. (LREC-COLING 2024) advocate human post-editing and separate grammaticality, fluency and meaning preservation. These dimensions motivate the verifier rubric, but M2's expert-grounded labels do not fully establish scientific meaning fidelity.

7. Li et al. (EMNLP 2025) survey LLM-as-a-judge opportunities and failure modes; Chen & Goldfarb-Tarrant (ACL 2025) show judge decisions can be highly sensitive to artifacts. M2 therefore hides generator identity, reference, prior labels and confidence and uses fixed structured output.

8. Nahw (EACL 2026) shows that Arabic grammar remains difficult even for strong LLMs and that high-quality natural data remains more effective than synthetic-only supervision. M2 must therefore be a falsification test, not a presumption that frontier reasoning solves Arabic.

## References

- https://aclanthology.org/2024.bea-1.6/
- https://aclanthology.org/2024.tacl-1.47/
- https://aclanthology.org/2025.acl-short.20/
- https://aclanthology.org/2025.acl-long.470/
- https://aclanthology.org/2025.acl-long.335/
- https://aclanthology.org/2024.lrec-main.584/
- https://aclanthology.org/2025.emnlp-main.138/
- https://aclanthology.org/2025.acl-long.970/
- https://aclanthology.org/2026.eacl-long.296/

## Guardrails

- One verifier architecture first; no multi-agent ensemble before single-verifier value is demonstrated.
- No A7'ta reserved examples are visible during prompt development.
- No QALB14 TEST, QALB15, ZAEBUC DEV/TEST, reserved Nahw or sealed ACAD_PASS benchmark.
- Expert reference/case family/model identity are hidden from the verifier.
- No threshold/prompt tuning after reserved confirmation labels are opened.
