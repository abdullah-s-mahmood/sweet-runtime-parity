# Phase 2 — AraBART Edit Research Update

Date: 2026-09-28

## Fresh research considered

- Goto, Sakai & Watanabe, BEA 2026, **Edit-level Majority Voting Mitigates Over-Correction in LLM-based Grammatical Error Correction**: edit-level agreement is a more appropriate unit than whole-sentence voting for reducing over-correction. https://aclanthology.org/2026.bea-1.60/
- Goto, Sakai & Watanabe, TACL 2026, **Grammatical Error Correction Evaluation by Optimally Transporting Edit Representation**: reinforces edit-representation-centric evaluation rather than sentence similarity. https://aclanthology.org/2026.tacl-1.77/
- Ye et al., ACL 2025, **CLEME2.0**: separates hit-correction, wrong-correction, under-correction and over-correction; this matches the need to characterize AraBART collateral edits rather than collapse them into one score. https://aclanthology.org/2025.acl-long.10/
- Goto, Sakai & Watanabe, EMNLP 2025 Findings, **Reliability Crisis of Reference-free Metrics for GEC**: reference-free/LLM metrics can be exploited and should not become a sole runtime acceptance oracle. https://aclanthology.org/2025.findings-emnlp.1356/
- Rozovskaya & Roth, ACL 2026, **Toward Robust Evaluation for Multilingual GEC**: closest-gold evaluation better handles legitimate alternative corrections than a single fixed reference. https://aclanthology.org/2026.acl-long.2193/
- Mubarak, Hawasly & Mohamed, EACL 2026, **Nahw**: Arabic grammar detection/correction/explanation remains difficult and reference targets are local task instances. https://aclanthology.org/2026.eacl-long.296/
- Alhafni et al., LREC 2026, **ZAEBUC***: provides a bilingual Arabic-English benchmark direction useful later for transferring the same architecture to English and mixed-language evaluation. https://aclanthology.org/2026.lrec-1.137/

## Evidence after adjudication

The project data strongly supports an edit-level, abstention-first design. Of 67 new AraBART-only substitutions, 29 are supported/alternative while 33 are wrong. Published-target overlap is highly enriched for useful edits (19/23), but the runtime system cannot use target location as a feature. Outside target locations, only 10/44 edits are supported while 30/44 are wrong.

Therefore:
- AraBART is valuable as a recall-expanding second generator.
- AraBART-only generation is unsafe as an acceptance rule.
- reference-free scoring alone is not an adequate replacement for typed evidence and abstention.
- deterministic Arabic orthographic/grammar vetoes are unusually promising because many observed failures are structurally recognizable.
- edit-level model agreement should be tested only after generator independence and local alignment quality are verified.

No policy is frozen and no sealed benchmark is created.
