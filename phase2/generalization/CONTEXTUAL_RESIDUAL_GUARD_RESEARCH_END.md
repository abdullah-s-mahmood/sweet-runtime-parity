# Contextual Residual-Risk Guard — Research End

Date: 2026-09-29

Fresh literature remains consistent with the observed result: edit-level voting can reduce over-correction but does not prove contextual correctness; counterfactual GEC work shows that context changes can flip edit validity; Arabic dependency parsing can supply structured syntax beyond morphology when needed.

The current diagnostic therefore supports a staged architecture: first validate the narrow morphology-preserving isolated orthographic lane; only escalate to dependency-aware guards if fresh validation fails or coverage is insufficient.

Key external anchors checked at phase end: Alhafni & Habash ACL 2025 Arabic text editing; Goto et al. BEA 2026 edit-level majority voting; Wang et al. Findings ACL 2026 COCOGEC; CamelParser2.0 Arabic dependency parsing.