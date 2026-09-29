# Dependency/Governor Completeness — Brainstorm Start

Date: 2026-09-29

| Idea | Decision | Reason |
|---|---|---|
| Parse source/candidate with CATiB | TEST | Arabic-focused dependency formalism and current parser support. |
| Parse source/candidate with UD simultaneously | DEFER | Add only if CATiB mapping is inadequate or as later robustness check. |
| preprocessed_text mode | TEST | Gives POS/morphology but may split clitics. |
| tokenized mode | TEST | Preserves supplied tokens but uses UNK POS; useful mapping baseline. |
| Hard-code rules from the two known partials | PROHIBITED | Would overfit consumed labels. |
| Compare target relation/head/dependents | TEST AFTER MAPPING | Direct structural evidence. |
| Treat parser agreement as correctness proof | DROP | Parser itself can err. |
| Use dependency signal as REVIEW gate | CANDIDATE | Appropriate safety role if diagnostics are informative. |

The first gate is runtime/tokenization feasibility only.
