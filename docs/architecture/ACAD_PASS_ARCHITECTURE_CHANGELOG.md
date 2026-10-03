# ACAD_PASS — Architecture Changelog

Permanent decision history · Established 2026-10-03 · Current architecture 2.0.0

Each new entry must record date, decision, previous/new design, reason and evidence, benefits/costs/risks, English impact, Arabic portability impact, and whether the Arabic snapshot changes. Entries record decisions, not retroactive experimental success. Preserve prior entries and link superseded documents.

## 2026-10-02 — Initial platform architecture (retrospective index)

- **Decision:** retain transformation as the product core; protect it through transactions, scientific invariants, Verify/Repair and extensible tools.
- **Previous design:** Arabic GEC/proposer/verifier experiments dominated the active path.
- **New design:** paragraph-level academic transformation, bilingual feasibility slice, shared document/provenance platform and future commercial services.
- **Reason/evidence:** V4.2 completed but its roster availability gate failed; 72.23% oracle availability and 23.65% clean recovery are not a product-quality result. See [original study](ACAD_PASS_MASTER_ARCHITECTURE_2026-10-02.md).
- **Improved:** aligns research with writing usefulness; retains protection and evidence.
- **Worsened/cost:** simultaneous English/Arabic/mixed validation expands early experimental scope.
- **Risks:** infrastructure expansion, fluent scientific drift, premature generalization from synthetic tests.
- **English impact:** enters joint active research.
- **Arabic portability:** shared architecture proposed; Arabic remains active in that historical plan.
- **Snapshot impact:** historical rationale preserved; no change to experimental results or exposure.

## 2026-10-03 — V1.1 priority correction (retrospective index)

- **Decision:** formal HW/DR tracks, approximate length and authorial voice become explicit product concerns.
- **Previous design:** academic transformation present, but risks being crowded out by engineering/GEC.
- **New design:** human academic writing remains first; meaning precedes length; frozen-output detector evaluation and separate quality dimensions.
- **Reason/evidence:** user strategic correction and reviewed human/AI style, length and detector literature. See [V1.1 amendment](ACAD_PASS_ARCHITECTURE_AMENDMENT_V1_1_2026-10-03.md).
- **Improved:** clearer benchmark objectives, measured verbosity and style, no detector feedback loop.
- **Worsened/cost:** more evaluation dimensions and future qualified-review requirements.
- **Risks:** treating style proxies or a ±15% length band as proof of human quality.
- **English impact:** stronger writing evaluation within a still-bilingual plan.
- **Arabic portability:** local style/counting differences acknowledged; no new Arabic evidence.
- **Snapshot impact:** preserve earlier Arabic-specific research references; no new data exposure.

## 2026-10-03 — V2 English-first strategic rebaseline (current)

- **Decision:** ENGLISH_FIRST / MULTILINGUAL_READY_CORE; freeze active Arabic research. English is `LANG_EN`, not the Core.
- **Previous design:** bilingual AT0, 4 AR +4 EN +4 MIXED generation cases; 10×3 fixture design; parallel language research expectations.
- **New design:** one AT0-EN slice, 12 diverse English cases, 30 distinct engineering fixtures, two models × DIRECT/PLANNED =48 slots, nominal 72 logical calls. Follow with HW1-EN only after review. Arabic resumes later through the extension contract.
- **Reason/evidence:** explicit user rebaseline; lower experimental dimensionality; prior studies show language/domain/model specificity. V4.2 Arabic closure remains unchanged. See [V2 memo](ACAD_PASS_ENGLISH_FIRST_REBASELINE_V2.md).
- **Improved:** threefold English case coverage versus four English cases at the same nominal generation matrix size; focused human-writing validation; stable port boundary; permanent evidence memory. This is a design-efficiency gain, not a measured quality gain or guaranteed cost reduction.
- **Worsened/cost:** Arabic product availability delayed; contemporary Arabic quality/detector knowledge will age; preservation and interface audits add small costs.
- **New risks:** English tokenization/grammar/length assumptions in Core; accidental loss of expiring Arabic artifacts; mistaking English maturity for Arabic evidence; adapters becoming an overbuilt prerequisite.
- **Controls:** versioned outcome-based LanguageAdapter; explicit Unicode/source coordinates; externalized thresholds; capability-scoped release; cheap portability audits at major gates; verified evidence inventory and future Arabic-local validation.
- **English impact:** sole active language, immediate AT0-EN followed by authentic human assessment; no full GEC prerequisite.
- **Arabic portability impact:** future first-class port over shared platform; conditional confidence, not a promise of zero future schema evolution. Core services reused; linguistic implementations and validation local.
- **Snapshot impact:** YES. Create the canonical Arabic snapshot, retain source documents/hashes/exposure and selected closures, inventory remote backups separately. No Arabic experiment or reserved-data opening.
- **Artifacts established:** four permanent master Markdown files plus the recommended permanent evidence manifest; V2 decision memo and one superseding AT0-EN packet.
- **Execution state:** documents authored locally. No AT0-EN/HW1/DR experiment, repository promotion, branch deletion or new Arabic computation performed by this architecture study.

## Future entry template

Date / architecture version / decision ID / authoring or execution state / prior design / new design / reason / supporting evidence / what improves / what worsens / risks and mitigations / English impact / Arabic portability impact / snapshot update required and completed / affected compatibility versions / experiment authorization boundary.


## 2026-10-03 — AT0-EN implementation adoption checkpoint

- **Decision:** Adopt English-first architecture package and offline AT0-EN harness.
- **Previous state:** Architecture/design only; experiment not implemented.
- **New state:** Critical Arabic evidence byte-verified; 12 English synthetic cases frozen; 30/30 engineering fixtures PASS after one scope-protection repair; portability audit 10/10 PASS; live 48-slot matrix NOT_RUN due unavailable auditable two-model access/cost ceiling.
- **Improved:** Independent authorized-scope enforcement prevents context escape; multilingual boundary has executable checks.
- **Worsened/new risk:** Live transformation feasibility remains unmeasured until model access/budget are authorized.
- **Arabic impact:** Active Arabic research remains FROZEN; no reserved data opened and no V4.2 rerun.
- **Next gate:** Complete the authorized 48-slot live matrix or return blocker to architect; no HW1-EN/DR before review.


## 2026-10-03 — Higher-model delegation protocol adopted

- **Decision:** Higher model becomes architect/research director/red-team reviewer; routine work is delegated to the implementation agent.
- **Reason:** Higher-model access is limited and expensive; direct execution by it wastes scarce quota when the implementation agent can perform the work reliably.
- **Improved:** Lower higher-model consumption; clearer return gates; stronger separation of strategic review from implementation.
- **Risk:** Under-escalation could miss a high-level issue.
- **Mitigation:** Mandatory escalation for architecture changes, experiment-contract changes, safety-gate changes, protected-data boundary changes, critical evidence loss, or unexpected results threatening inference validity.
- **Arabic portability impact:** None directly; protocol applies to all future language packs.

## 2026-10-03 — Repository adoption recorded

- **Adoption commit:** `bca3a32791c6f2c1832403cbd751ea8c78cd6a43`
- **Scope:** English-first master records, Arabic preservation snapshot/evidence mirrors, higher-model delegation protocol, AT0-EN offline harness, 30/30 fixture result, 10/10 portability audit, and explicit 48-slot NOT_RUN accounting.
- **Live-model status:** no live model call; blocker remains authorized two-model access plus explicit cost ceiling.
