# Residual GED Completeness — Research Start

Date: 2026-09-29

Fresh literature review supports testing a post-correction acceptability signal rather than adding more voters.

- Arabic text-editing ensembles improve GEC but do not establish zero-error local acceptance (Alhafni & Habash, ACL 2025).
- Edit-level voting mitigates over-correction but correlated errors remain possible (Goto et al., BEA 2026).
- Multi-pass decoding shows that residual correction demand after an edit is a meaningful GEC signal (Wang et al., EMNLP 2024).
- Correction Acceptability Discrimination explicitly argues that sentence-level syntax/semantics after correction must be assessed rather than trusting a locally plausible edit (Cao et al., LREC-COLING 2024).
- Nahw (EACL 2026) shows Arabic grammar understanding remains difficult, motivating conservative review-first architecture.

The immediate hypothesis is therefore residual GED cleanliness around the candidate, tested only as a consumed-population diagnostic.
