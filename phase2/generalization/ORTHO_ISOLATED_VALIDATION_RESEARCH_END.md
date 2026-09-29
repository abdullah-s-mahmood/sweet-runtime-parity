# ORTHO_ISOLATED Fresh Validation — Research End

Date: 2026-09-29

The fresh validation falsified the zero-unsafe auto-accept claim for ORTHO_ISOLATED_COMMON_NOUN_V1. End-of-gate research supports interpreting this as a contextual-completeness problem rather than a simple voting problem.

Relevant evidence:
1. Alhafni & Habash, ACL 2025, "Enhancing Text Editing for Grammatical Error Correction: Arabic as a Case Study" — Arabic text-editing and ensembles improve performance, but the task remains morphologically rich and contextual.
   DOI: 10.18653/v1/2025.acl-long.875
2. Goto, Sakai & Watanabe, BEA 2026, "Edit-level Majority Voting Mitigates Over-Correction in LLM-based Grammatical Error Correction" — edit-level voting can mitigate over-correction, but does not constitute a correctness proof.
   DOI: 10.18653/v1/2026.bea-1.60
3. Elshabrawy et al., ArabicNLP 2023, "CamelParser2.0: A State-of-the-Art Dependency Parser for Arabic" — Arabic dependency parsing can expose syntactic relations and rich morphology that local orthographic identity cannot represent.
   DOI: 10.18653/v1/2023.arabicnlp-1.15
4. Mubarak, Hawasly & Mohamed, EACL 2026, "Nahw: A Comprehensive Benchmark of Arabic Grammar Understanding, Error Detection, Correction, and Explanation" — current Arabic grammar systems still show substantial gaps, reinforcing the need for systematic held-out evaluation and human validation.
   DOI: 10.18653/v1/2026.eacl-long.296

Research implication:
- do not add a fourth voter merely to raise agreement;
- do not reinterpret morphology identity as contextual correctness;
- test a separate context/repair-completeness signal;
- dependency/governor evidence and post-edit fixed-point stability are justified candidates;
- any V2 must be pre-registered before a fourth untouched slice is evaluated.
