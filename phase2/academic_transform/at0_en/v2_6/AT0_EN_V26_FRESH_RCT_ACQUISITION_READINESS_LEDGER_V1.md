# ACAD_PASS — Fresh RCT Acquisition Readiness Ledger V1

Date: 2026-10-08

State:
`READINESS_INCOMPLETE_ACQUISITION_BLOCKED`

Governing protocol:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_PROTOCOL_FREEZE_V1.md`

Governing independent review:
`FRESH_RCT_INDEPENDENT_ACQUISITION_REVIEW_V1.md`

## Readiness gates

| Gate | Required evidence | Current state |
|---|---|---|
| Human annotator A | Qualified medical/allied-health or graduate clinical epidemiology/evidence-synthesis background; English RCT competence; later protocol qualification | NOT_ESTABLISHED |
| Human annotator B | Same requirements; independent of A until lock | NOT_ESTABLISHED |
| Senior adjudicator | Qualified senior clinical/evidence-synthesis reviewer | NOT_ESTABLISHED |
| Independent custodian | Separate from model development; holds seed/split/EVAL custody | NOT_ESTABLISHED |
| Resource/funding feasibility | Must cover 80 qualification + 400 DEV + 5,000 EVAL under dual annotation + adjudication/audit | NOT_ESTABLISHED |
| Prior-exposure inventory | Complete versioned inventory across all prior ACAD_PASS corpora/artifacts/prompts/attachments/translations/manual examples | INCOMPLETE |
| Protected-corpus fingerprint custody | Ability to deduplicate against protected sources without developer opening VERIFY_INTERNAL | NOT_ESTABLISHED |
| Access control | EVAL text/IDs/labels/scope/embeddings/discussions inaccessible to developers before final freeze | NOT_ESTABLISHED |
| Annotation manual pin | Exact source manual revision + local immutable copy/hash | UPSTREAM_PIN_FROZEN — commit bc4b878773192f38b2600ec830ca4208b82f7dc0 / blob f67df5da9507c562cbeab7ad497e816bde58a02a; local binary copy still pending |
| Prospective annotation addendum | Decisions 17–21 converted into immutable operational manual | FROZEN — AT0_EN_V26_FRESH_RCT_ANNOTATION_ADDENDUM_V1.md / commit 26cd1573a1fc410f1209d1a5f5c38dec5ac54ce4 |
| Statistical implementation | Clopper-Pearson/HMAC audit code validated on synthetic data only | SYNTHETIC_PREFLIGHT_PASS — run 37828307955 / artifact 11572557395 |
| Retrieval archive tooling | Must archive exact query, timestamps, QueryTranslation, warnings, full PMIDs/XML/pagination/hashes without sampling | SYNTHETIC_MECHANICS_PASS — run 37828800778; live PubMed execution still blocked |
| Trial-family provenance tooling | Deterministic exact/fuzzy triggers + registry alias ledger; no learned model required | SYNTHETIC_TRIGGER_PASS — run 37828800778; real documentary/family adjudication still blocked |
| Seed commitment procedure | Independent custodian procedure documented; actual secret NOT generated yet | PROCEDURE_FROZEN — actual secret generation remains forbidden until custodian readiness/sign-off |
| Acquisition sign-off | Readiness evidence independently reviewed and explicitly authorized | NOT_AUTHORIZED |

## Hard rule

No acquisition action may convert any NOT_ESTABLISHED / INCOMPLETE / NOT_YET_FROZEN / NOT_YET_IMPLEMENTED row into an assumption.

No real retrieval is authorized until every required BEFORE_ACQUISITION gate is closed and a new explicit acquisition authorization file is committed.

## Next allowed package

Build:
`FRESH_RCT_ACQUISITION_READINESS_PACKAGE_V1`

It may contain only:
- provenance inventory and fingerprints/identifiers;
- staffing/custody declarations;
- access-control design;
- resource feasibility;
- pinned annotation manual/addendum;
- synthetic-only statistical/tooling tests.

It must contain zero:
- new RCT records;
- new split memberships;
- real allocation seed;
- annotations;
- model outputs.


## 2026-10-08 statistical readiness update

Synthetic statistical preflight:
`PASS`

Run:
`37828307955`

Artifact digest:
`sha256:f9f8f5cd80b0936f8183aacfe008525949428a1f5b310f401c6b233838668926`

Frozen evidence:
`AT0_EN_V26_FRESH_RCT_STATS_SYNTHETIC_PREFLIGHT_FREEZE_V1.md`

This closes only the statistical synthetic-mechanics row.

Overall state remains:
`READINESS_INCOMPLETE_ACQUISITION_BLOCKED`.


## 2026-10-08 annotation/readiness update

Pinned manual identity:
- repository `BIDS-Xu-Lab/section_specific_annotation_of_PICO`;
- commit `bc4b878773192f38b2600ec830ca4208b82f7dc0`;
- manual Git blob `f67df5da9507c562cbeab7ad497e816bde58a02a`;
- blob size 204547 bytes.

Frozen prospective addendum:
`AT0_EN_V26_FRESH_RCT_ANNOTATION_ADDENDUM_V1.md`

Actual qualification/main-corpus annotation remains forbidden.

Seed-commitment logic is frozen, but no real 256-bit secret may be generated before an independent custodian exists and acquisition is explicitly authorized.


## 2026-10-08 acquisition-tooling readiness update

Synthetic acquisition-tooling preflight:
`PASS`

Run:
`37828800778`

Artifact:
`11572806239`

Artifact digest:
`sha256:c5bf089d064987692fa4b8780252c7e6283531a47b0dc47a71f19b0a8be36dbc`

Frozen evidence:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_TOOLING_SYNTHETIC_PREFLIGHT_FREEZE_V1.md`

No PubMed request was issued.
No RCT record was retrieved.
No protected corpus was opened.

These tooling rows are mechanically closed only at the synthetic level.

Overall state remains:
`READINESS_INCOMPLETE_ACQUISITION_BLOCKED`.
