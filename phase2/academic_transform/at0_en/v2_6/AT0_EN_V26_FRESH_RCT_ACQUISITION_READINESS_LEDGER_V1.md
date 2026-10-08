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
| Annotation manual pin | Exact source manual revision + local immutable copy/hash | NOT_YET_FROZEN |
| Prospective annotation addendum | Decisions 17–21 converted into immutable operational manual | NOT_YET_FROZEN |
| Statistical implementation | Clopper-Pearson/HMAC audit code validated on synthetic data only | NOT_YET_IMPLEMENTED |
| Retrieval archive tooling | Must archive exact query, timestamps, QueryTranslation, warnings, full PMIDs/XML/pagination/hashes without sampling | NOT_YET_IMPLEMENTED |
| Trial-family provenance tooling | Deterministic exact/fuzzy triggers + registry alias ledger; no learned model required | NOT_YET_IMPLEMENTED |
| Seed commitment procedure | Independent custodian procedure documented; actual secret NOT generated yet | PROCEDURE_PENDING |
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
