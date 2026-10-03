# ACAD_PASS — Language Extension Contract

Contract version: 1.0.0 · Architecture baseline: 2.0.0 · Date: 2026-10-03

Status: normative design for implementation; not a claim that an adapter or language has passed validation. Initial active pack: `LANG_EN`. Future pack: `LANG_AR`. See [master architecture](ACAD_PASS_MASTER_PRODUCT_ARCHITECTURE.md).

## 1. Contract principles and compatibility

A Language Pack provides linguistic outcomes under versioned contracts. It need not share English grammatical internals, tokenizer units, punctuation conventions or rhetorical targets. Core schemas express text, document relationships, findings and provenance; language-specific taxonomies live in namespaced extensions.

Pack manifest fields: `pack_id`, BCP-47 language tags, script/direction support, pack version, compatible Core range, contract version, capabilities, supported modes/domains/document scopes, resource/model identities, licenses, policy versions, benchmark versions, limitations and release status. `en` is mandatory in English runs; omission is an error. A declaration and a detector can disagree; preserve that finding rather than silently overriding it.

Core and pack versions use semantic versioning. Breaking schema/meaning changes require a major version and migration/conformance evidence. Additive optional capabilities require negotiation and cannot silently alter existing results. Replays use the original schema and stored proposal; a newer pack cannot re-interpret historical offsets or hashes. Do not load a pack outside its declared Core range.

Capability states: `AVAILABLE`, `NOT_IMPLEMENTED`, `UNSUPPORTED`. Individual results use `OK`, `UNCERTAIN`, `ERROR`; checks additionally return `PASS`, `FAIL`, `REVIEW`, `NOT_ASSESSED` as appropriate. These are not interchangeable. An unsupported morphology capability is acceptable if the released task does not depend on it. An unavailable required scientific check cannot be converted into PASS.

## 2. Shared call envelope

Each call accepts a versioned request with document/source identity, exact text or allowed source spans, language, read-only context, task/mode, constraints, policy versions and permitted capabilities. Sensitive text remains tenant-scoped. Calls cannot grant themselves broader access.

Each response records method/pack/resource versions, capability status, outcome, input/output hashes, evidence spans, warnings, uncertainty and timing/usage where applicable. Feature values identify units and denominators. Null plus a reason replaces fabricated values. All offsets name the coordinate space and source version. Pack-private token or morphology indices must map back to Core spans or be explicitly unresolved.

Transformers return proposals, never mutations. Extracted facts and generator-declared mappings are hypotheses until verified. A scientific relation can remain unknown even when a surface term is unchanged.

## 3. LanguageAdapter capabilities

| Method | Required outcome and constraints |
|---|---|
| `detect_language()` | Language distribution and/or span tags, confidence and UNKNOWN/unsupported result; short text and mixed scripts may be ambiguous. Dispatcher may combine registered detectors. |
| `segment_document()` | Linguistic section/block annotations linked to existing structural nodes; must not reparse away tables, equations or source structure. |
| `segment_paragraph()` | Paragraph boundaries or within-paragraph units with explicit semantics and source mapping; no silent scope expansion. |
| `segment_sentence()` | Sentence/unit spans, segmenter version and ambiguity; abbreviations, decimals and quotations handled or flagged. |
| `analyze_morphology()` | Language-defined analyses, ambiguity and optional feature namespace; no required English inflection/POS taxonomy. |
| `analyze_syntax()` | Language-defined syntax representation and span links with confidence; formalism/version named. |
| `extract_discourse_features()` | Rhetorical/discourse annotations with evidence, section/domain and local taxonomy; no universal IMRaD move sequence required. |
| `extract_stylometric_features()` | Versioned feature vector, counts/denominators, sample adequacy and confounds; not an authorship verdict. |
| `transform_academic_text()` | Bounded source-anchored KEEP or revision proposal with content mappings, declared model/prompt settings and failure states. |
| `verify_language_quality()` | Separate quality findings, evidence and uncertainty; language quality cannot certify scientific truth. |
| `validate_punctuation()` | Locale-aware punctuation findings with protected spans respected; no destructive normalization. |
| `compute_length_metrics()` | Words or declared language-appropriate units, raw/adjusted counts, sentences, comparable token ratio if available, policy version and null reasons. |
| `build_voice_profile()` | Authorized corpus provenance, tenant/author/language scope, feature schema and uncertainty; no scientific fact ingestion. |
| `evaluate_voice_similarity()` | Content-controlled style comparison and limits; distinct from authorship attribution, fluency and detector scores. |
| `get_detector_protocol()` | Current language-specific eligible documents, detectors, versions/date, scoring/abstention handling and freeze requirements. |
| `get_language_specific_constraints()` | Orthographic, scientific-expression, punctuation, terminology, direction and normalization rules with versions and severity. |

Additional capabilities can provide scientific-relation extraction, citation-support interpretation or domain lexicons. Their evidence schema is shared; their linguistic effectiveness must be validated locally. Core invokes a required capability through its interface rather than importing the English implementation.

## 4. Minimum slice versus complete language support

AT0-EN needs explicit language routing, paragraph/sentence units, scoped transformation, constraints, deterministic protected checks, length measurement, provenance and truthful capability reporting. Its mock/deterministic verifiers exercise the mechanism. Full syntax, morphology, voice, detector execution and discourse scoring may remain unimplemented. A stub returning `NOT_IMPLEMENTED` is valid; a stub returning fabricated PASS is not.

A mature pack must have evaluated implementations for all advertised capabilities, and explicit unsupported states for others. Morphological analysis is required where the chosen language-specific protection design depends on it, not because English happened to expose a method. Publishing a language badge does not authorize every mode, domain or format.

## 5. Benchmark classes and data governance

Keep separate:

1. Synthetic engineering fixtures with known expected operations and relationships.
2. Authentic permitted academic transformation inputs across paper sections, domains and proficiency levels.
3. Provenance-labelled genuine human, weak human, AI-generated, AI-polished, professionally edited and human-edited AI material.
4. Scientific-preservation adversaries: quantities/groups/time/units, comparisons, negation, epistemic modality, causality, citations, equations and terminology.
5. Authorized author corpora for voice, separated by author/content/time where feasible.
6. Long-document and supported-format fidelity cases.
7. Frozen detector-eligible documents plus true human controls and EAL strata.

Document license/permission, origin, author/document cluster, model exposure/training-overlap knowledge, collection dates and split role. Development data remain development after tuning. Split by author/document/topic clusters, not randomly by adjacent paragraphs. Lock confirmation data before any tuning; do not call an already opened calibration subset a fresh holdout. A limited pilot does not prove generalization.

For Arabic, preserved exposure decisions govern even if a file is renamed, an experiment is cancelled or a new pack is created. Opening reserved Arabic data requires a future explicit protocol and authorization; a port request alone does not erase those restrictions.

## 6. Model comparison and transformation validation

Compare a strong direct model baseline with the proposed architecture under the same source, context, scope and policy. Record provider/model snapshot or opaque alias, observation date, settings, prompt hashes, resource budgets and all failures. Family diversity is useful when available; repeated calls to one model are not independent model families.

Retain original and human revision comparators when available. Predefine the experimental unit, randomization, failure treatment, primary question and uncertainty reporting. Track edit necessity, new claims, omissions and user revision burden. Never select a preferred variant using detector scores. A new model/version or major prompt/policy change triggers scoped revalidation before releasing old quality claims under the new identity.

## 7. Scientific and language-specific validation

Core conformance must establish exact-source protection, atomic scope, identity, replay, rollback, traceability and safe rejection of malformed/partial/stale requests. Language-local tests must establish how actual prose expresses protected relationships. Token preservation alone is insufficient.

For future Arabic add tests for hamza/alif variants, ya/alif maqsura, ta marbuta, diacritics, tatweel, clitics, inflection/agreement, whitespace boundaries, Arabic/Latin digits, units and mixed-script scientific symbols. Normalization must retain a source alignment. Arabic punctuation and bidi behavior must not inherit English assumptions. These are future validation categories, not permission to execute Arabic research now.

Qualified domain reviewers assess scientific and semantic fidelity; language/academic reviewers assess writing. Missing support, uncertain interpretation or reviewer disagreement remains visible. Any confirmed critical scientific corruption blocks release of the affected capability until explained, repaired and revalidated on a preregistered independent set.

## 8. Human-writing, length and voice validation

Use blinded and randomized pairwise comparison plus separate rubric dimensions. Evaluate naturalness, register, clarity, discourse, rhythm, formulaic phrasing and verbosity without encouraging artificial variation. Keep source and necessary scientific context available to fidelity reviewers. Report ties, disagreements, rater qualifications, reliability and limitations.

Calibrate length policies on genuine revision needs. A soft rewrite band is not a quality threshold. Report information-unit preservation separately, including uncertain units. Voice experiments isolate style retrieval from evidence retrieval, use only authorized examples, and include checks for copied content, topic leakage and cross-user access. Do not make a stronger style match at the expense of hedging, citation meaning or required details.

## 9. Detector and document validation

DR begins only after transformation outputs and selections are frozen. Record actual language eligibility and full-document requirements. Unsupported or too-short documents are ineligible, not zero-scored; do not concatenate unrelated paragraphs to obtain a score. Vendor score bands/abstentions stay bands/abstentions. Include human/EAL false positives, hybrid-writing categories, disagreement and update drift. Keep each detector's claim scope narrow.

Round-trip document suites test run/paragraph boundaries, citations, cross-references, tables, equations, footnotes, comments, tracked changes, style/direction metadata, unsupported objects and source bytes where exact retention is required. English format success does not establish Arabic RTL success. Test the same Core document services with pack-specific suites. No model may rewrite document package XML or LaTeX macros outside a controlled service and transaction.

## 10. LANGUAGE_PORTABILITY_AUDIT

| ID | Cheap test at a major architecture gate | Failure consequence |
|---|---|---|
| LP01 | Language required; UNKNOWN/unsupported routing has no implicit English fallback | Block schema/interface acceptance |
| LP02 | Core dependency graph contains no English tokenizer, prompt, lexicon or detector threshold | Move dependency into pack before gate closes |
| LP03 | Explicit offset type; round-trip UTF-8/code-point/UTF-16 maps including non-BMP/combining characters | Block transformations on unsafe spans |
| LP04 | Direction and mixed-script metadata survive transaction and serialization using a nonlinguistic stub | Block claimed multilingual readiness |
| LP05 | Word/token/sentence units and thresholds externalized; zero/null cases supported | Block metric contract freeze |
| LP06 | No compulsory English grammar labels; unsupported capabilities exercise review behavior | Block adapter release |
| LP07 | Two stub packs with different feature namespaces/counting units share unchanged Core tests | Fix interface leakage; no language research required |
| LP08 | Voice feature namespaces, consent and tenant isolation remain extensible | Block voice/schema release |
| LP09 | Detector protocol selected by language/version, with unsupported eligibility preserved | Block DR/report compatibility |
| LP10 | Protected relation schemas and document services accept pack-local extraction/fidelity findings | Block relevant feature release |

Run at AT0 closure, benchmark/adapter schema freeze, long-document/DOCX freeze, public API freeze, and language-port entry/exit. Re-run only impacted tests after a relevant change. Do not turn this into a parallel Arabic evaluation program. Nonlinguistic Unicode/bidi fixtures are permitted; no Arabic generated prose or reserved text is needed.

## 11. Stop conditions and release gates

Stop affected execution for source corruption, scope escape, wrong hashes, ambiguous replay, prohibited data access, broken tenant isolation, unbounded cost or changed model identity. Record results already obtained and remaining slots. A single content failure is retained and rejected/reviewed; it need not stop independent cases if the harness is sound.

Language release gates: (G0) provenance, permissions, identity and compatibility frozen; (G1) Core/adapter conformance and portability pass; (G2) language-local scientific/semantic tests and qualified review; (G3) blinded human-writing confirmation in advertised scope; (G4) length and voice evidence for advertised modes; (G5) frozen-output DR measured or explicitly unavailable with no unsupported robustness claim; (G6) supported-document fidelity; (G7) useful, operationally viable beta with a release scope card. Detector scores do not override G2/G3. Voice can remain a disabled capability until validated.

Before opening confirmation data, freeze numeric/statistical criteria appropriate to sample size, risk and scope. At minimum require no unresolved critical source/scientific/document/tenant failure. A small pilot with zero observed errors is not a guarantee of zero error. If evidence is insufficient, narrow the release scope or collect an independently designed confirmation set.

## 12. Formal future ADD ARABIC procedure

Entry conditions: explicit Arabic resumption instruction, versioned mature English scope, stable Core contracts and a preservation integrity report. Then:

1. Read the four master files and evidence manifest; follow current decisions rather than historical next-step instructions.
2. Snapshot current Core and create a component inventory with exactly one initial disposition: `REUSE_UNCHANGED`, `ADAPT_INTERFACE`, `ARABIC_IMPLEMENTATION_REQUIRED`, or `ARABIC_REVALIDATION_REQUIRED`. Record evidence and owner for each; interface adaptation must preserve Core semantics.
3. Recover saved Arabic contracts, models, runtime locks, reports and exposure records. Verify hashes before use. Recover missing artifacts from existing copies; missing evidence does not authorize experiment reruns or opening reserved text.
4. Map preservation classifications to the port plan. Reuse engineering contracts, preserve failures, locally revalidate old linguistic components, and exclude development-exposed material from clean confirmation claims.
5. Implement `LANG_AR` capabilities needed for the first advertised scope: segmentation, scientific-expression constraints, morphology where needed, discourse, transformation, verification, length, stylometry and authorized voice. Additional advertised capabilities require their own evidence.
6. Design an Arabic equivalent of the proven English human-writing benchmark using locally appropriate discourse/rubrics and qualified reviewers. Freeze new dataset permissions and exposure roles. Do not translate the English benchmark and call that sufficient validation.
7. Run shared Core conformance plus Arabic scientific/semantic, normalization, RTL and mixed-script tests under a separately authorized port packet.
8. Evaluate frozen Arabic outputs against the then-current detector landscape, including then-current Turnitin support; do not transfer English scores or old vendor claims.
9. Integrate capability-scoped Arabic into the same projects, UI, API, billing, document services, Word integration and plugins. A schema defect discovered here is repaired through a versioned compatibility change, not an untracked Core fork.
10. Complete language gates, update all affected master records and release scope. If a gate fails, keep the pack experimental or restrict capability; do not reopen a closed Arabic experiment by default.

This procedure makes a Core redesign unnecessary by design, conditional on conformance and audits. It cannot promise that no future bug fix or additive schema evolution will ever be needed.