# ACAD_PASS R4.3 Alternative Architecture Literature Matrix

Date: 2026-10-07
Purpose: independent literature evidence packet prepared while Stage A is running. No evaluation data used.

| Path | Primary evidence | Mechanism | Relevance to ACAD_PASS | Current priority |
|---|---|---|---|---|
| Biaffine start/end scoring | Yu, Bohnet & Poesio, ACL 2020, DOI 10.18653/v1/2020.acl-main.577 | Scores start/end token pairs globally with biaffine interaction | Directly tests whether endpoint interaction adds value beyond context | CURRENT H1 |
| Boundary Offset Prediction Network (BOPN) | Tang et al., Findings EMNLP 2023, DOI 10.18653/v1/2023.findings-emnlp.989 | Predicts offsets from candidate spans to nearest entity spans; uses non-entity spans as training signal | Strong fit if current bottleneck is wrong exact boundaries / recall | HIGH fallback |
| Locate-and-Label | Shen et al., ACL-IJCNLP 2021, DOI 10.18653/v1/2021.acl-long.216 | Filters seed spans and applies boundary regression before type labeling | Supports repair-before-classification hybrid | HIGH fallback |
| Triaffine span modeling | Yuan et al., Findings ACL 2022, DOI 10.18653/v1/2022.findings-acl.250 | Integrates boundaries, labels, inside tokens and related spans through triaffine attention/scoring | Candidate if H1 proves pair interaction useful but insufficient | MEDIUM-HIGH |
| GlobalPointer | Su et al., 2022, arXiv:2208.03054 | Global span scoring using head/tail interactions and imbalance-aware loss | Broader pair/grid alternative if verifier architecture underperforms | MEDIUM |
| MRC-style NER | Li et al., ACL 2020, DOI 10.18653/v1/2020.acl-main.519 | Reformulates each type as span extraction with start/end matching | Strong but larger reformulation; useful if type-conditioned queries help | MEDIUM |
| Context-rich modeling | Chen et al., AACL-IJCNLP 2020 | Uses richer context because ambiguous mentions can require context beyond local surface | Supports the missing-context hypothesis behind H0/H1 | SUPPORTING |

## Prospective interpretation

1. If H0 and H1 both improve substantially, context itself is validated as a core missing ingredient.
2. If H1 materially beats H0, explicit endpoint interaction is validated; triaffine/global pair models become more attractive.
3. If candidate ceiling or recall is the bottleneck, BOPN / Locate-and-Label style repair should outrank more aggressive rejection.
4. If contextual verification raises precision but sacrifices too much recall, a repair-then-verify hybrid is the most defensible next architecture.
5. MRC/GlobalPointer remain structurally credible alternatives but require larger reformulation and should not be introduced before the simpler hypotheses are resolved.

## Governance

This literature packet is non-adaptive and does not modify the frozen Stage-B protocol.
No protected data or Stage-A outputs were used to construct it.
