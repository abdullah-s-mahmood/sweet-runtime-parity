# Phase 2 — Dependency/Governor Feature Diagnostic End Review

Date: 2026-09-29

## Canonical run

- Workflow: Phase 2 Dependency Governor Feature Diagnostic
- Run: 36523340807
- Conclusion: SUCCESS
- Population: 14 consumed fresh ORTHO_ISOLATED_COMMON_NOUN_V1 PASS events
- Features frozen before manual labels: yes
- Mapping reliable: 14/14
- QALB15 TEST read: no
- QALB text persisted: no

## Primary finding

Simple source-to-candidate dependency-structure change is not a useful unsafe detector on this population.

- supported events with any structural-category change: 10/12
- partial events with any structural-category change: 0/2

Both partial events were structurally unchanged under the recorded CATiB categories.

Therefore dependency-changed-implies-risk is falsified for this purpose.

## Exploratory absolute-context finding

Both partial events shared:
- source CATiB anchor POS = NOM
- candidate CATiB anchor POS = NOM
- anchor dependency relation = OBJ
- governing head POS = VRB
- no structural-category change.

Several equivalent pairwise predicates separate the two partials from the 12 supported events on this tiny consumed set, but these combinations are considered high overfitting risk and are NOT promoted as rules.

A more interpretable positive signal emerged:
- 10/12 supported events changed source CATiB anchor POS from PROP to candidate NOM;
- 0/2 partial events showed PROP to NOM.

Thus the next hypothesis is not a dependency-veto rule. It is independent CATiB lexical normalization evidence: source CATiB PROP to candidate CATiB NOM.

This signal is post-hoc on the 14 events and cannot be trusted without replication.

## Decision

MIXED: dependency-change hypothesis worsened; CATiB normalization hypothesis is worth retrospective cross-slice replication.

Do not consume a fresh fourth slice yet.
