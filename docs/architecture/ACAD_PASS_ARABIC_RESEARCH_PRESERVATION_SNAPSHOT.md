# ACAD_PASS — Arabic Research Preservation Snapshot

Snapshot: AR-FREEZE-2026-10-03 / 1.0.0 · Parent architecture: ENGLISH_FIRST 2.0.0

**ACTIVE ARABIC RESEARCH: FROZEN. HISTORICAL EVIDENCE: RETAINED.** This is an evidence-preservation record, not a new experiment, a restart instruction, or an Arabic product validation claim. It freezes knowledge and exposure decisions; it does not claim that every remote artifact has already been backed up.

## 1. Authority, scope and source integrity

Repository: `abdullah-s-mahmood/sweet-runtime-parity`; inspected branch: `phase2-arabic-eval`. On 2026-10-03 the two remote continuity files still matched the supplied Git blob IDs:

| File | Git blob SHA-1 | Local supplied-file SHA-256 |
|---|---|---|
| RESUME_HERE.md | `7a0963f477426e6c711aa747e46dfe1be4e3b989` | `d368dc797e29f9c7cd2ed96e528d3a88d2f13d2a9347c719d5cae2d67ad045b3` |
| ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md | `753fcf49627fe42cde0cf09aa2e2eb32c1c388d7` | `c7eea67ceeb16336b0e54b705d26f032143ee2994bbc32640eeab9648f55ca40` |

These two identifiers are **blob IDs, not commit SHAs**. Supplied files were copied byte-for-byte into [evidence/2026-10-03](evidence/2026-10-03/RESUME_HERE.md); the [ledger copy](evidence/2026-10-03/ACAD_PASS_SYSTEM_EVOLUTION_LEDGER.md) preserves the full chronology. Selected contracts and V4.2 closure documents are also mirrored there; the [evidence manifest](ACAD_PASS_EVIDENCE_MANIFEST.json) names every mirrored item and its verification state.

Earlier headings in the continuity files describe earlier current states; the final 2026-10-02 V4.2 closure governs the historical Arabic outcome. The 2026-10-03 English-first decision supersedes historical next-action instructions. The mirrored documents remain historical evidence, including their instructions to rerun or continue earlier stages; those instructions are not active authorization.

No new Arabic input/reference dataset was read, no Arabic generation was performed, and no historical experiment was rerun to create this snapshot. Claims below are derived from the continuity records and named closure documents, not independent recomputation of their data. `metadata_index.json` preserves all hash/run/path-bearing source lines with line numbers to aid later recovery; it is a lexical index, not a validated mapping of every number to an artifact.

## 2. Classification vocabulary

| Classification | Meaning now |
|---|---|
| REUSABLE | Established contract, evidence or methodological lesson can be reused in its stated scope. This does not confer language-quality approval on an implementation. |
| REQUIRES_REVALIDATION | Potentially useful model, linguistic component or implementation whose use in a new pack/task/version requires local validation. |
| HISTORICAL_ONLY | Keep for provenance and interpretation; not a current deployable result. |
| FAILED_DO_NOT_REPEAT | Closed approach or invalid execution must not be repeated unchanged or silently relabelled. A genuinely new hypothesis requires a new future protocol. |
| UNOPENED_RESERVED | Preserve access boundary; metadata knowledge is not permission to inspect text. |
| FUTURE_ARABIC_CANDIDATE | Research direction, not an approved model, experiment or dependency. |

Classify an item's facets separately where needed: a failed model hypothesis can yield a REUSABLE testing method and HISTORICAL_ONLY outputs. `KEEP` for a proposer means retained research value, not permission to deploy it.

## 3. Historical phases and established conclusions

| Phase | Evidence and conclusion | Disposition |
|---|---|---|
| Early NoPnx/Nahw audit | 150 targets / 41 passages: 29 recovered (19.33%), 65 preserved (43.33%), 56 changed-other (37.33%). Audit covered 21 sections / 64 experiments. | HISTORICAL_ONLY; retain denominators |
| Population correction | The old 88.73→96.55 causal comparison crossed populations. Comparable figures were 34/36=94.44% versus 28/29=96.55%, +2.1073 pp; supported retention 28/34=82.35%. | REUSABLE lesson; invalid original inference FAILED_DO_NOT_REPEAT |
| M1 | Closed edit-contract/pilot phase. 24 pilot items: 8 supported corrections, 5 alternatives, 7 wrong, 2 partial, 2 unnecessary. Necessity/local correctness/group completeness/residual errors/meaning/protection separated. | Contract REUSABLE; labels HISTORICAL_ONLY |
| M1-A | QALB14 Train 19,411 / Dev 1,017; reconstructable 18,884+1,003; ledger-reported reconstruction failures 493. These totals do not reconcile by simple subtraction; retain the historical figures and flag the accounting scope for metadata reconciliation, not a rerun. Persisted calibration 3,829. A7'ta parseable 463: bootstrap 375, reserve 88. | Exposure and reconstruction records REUSABLE within scope; learner-text quality not academic product proof |
| M2 | Monolithic verifier: safe acceptance coverage 22.22→56.94%, review 37.5→20.83%, but unsafe approval 4.17→18.75%. Closed FAIL; no P2/M3 continuation from that phase. | FAILED_DO_NOT_REPEAT as standalone route |
| M2-R | ArabiGEE selective annotations unsuitable as complete-error gold; moved to complete QALB references. P0→P1 CRR 82.22→86.67%; GELR 29.14→48.88%; CFPR 60→33.33%; strict residual recall 63.33→76.67%; claim precision 63.47→65.50%. Improved but insufficient. | Closed FAIL; no P2. Gold semantics REUSABLE |
| M2-H | H1 candidate generator; H2 orthography, H3 morphology, H4 boundaries; H5 fusion/H6 completeness depend on upstream gates. H1 recall failed, so no integrated safe-verifier claim. | H5/H6 blocked; design lessons REUSABLE |
| H1-v1 | Frozen one-pass top-1 NoPnx; initial exact-transaction proxy 30.02% superseded by official-alignment measurement. 256/256 cross-path parity; final P=71.53, R=69.39, F1=70.44, F0.5=71.09. Recall gate 80% failed by 10.61 pp. | CLOSED FAIL; do not rerun unchanged |
| H2-v1 | Best ALIF lower bound 95.85% below 98%; no activation. Planned 250-item blinded expert packet had not been completed. | Hypothesis unapproved; qualified review not invented |
| H2-v2 | CALIMA analyzability hypothesis accepted 0/19,338. Source-analyzable 18,998; candidate-unanalyzable 339; hygiene 1. No narrower post-hoc salvage loop. | FAILED_DO_NOT_REPEAT |
| H3 | 2,597 MI/MT targets, 2,529 mapped; 169 candidates, 85 exact-supported nominations. H3 supported 3, exact 1; recall proxy 1.18% below 70%. Precision proxy 33.33% on n=3 is not a global estimate. | Disabled; morphology diagnostics REQUIRES_REVALIDATION |
| H4 split | Gold 2,633: accepted 0; H1 pure stream 1,920: accepted 0. Adversarial non-pure 0/1,143 and general 0/1,000 accepted. | FAILED_DO_NOT_REPEAT unchanged |
| H4 merge | Gold 5,505: accepted 2,612, recall 47.45% below 70%. H1 stream 3,792: accepted 1,853, exact-supported 1,779, unsupported 74; precision lower bound 96.01% >90% but recall gate fails. | No activation; high precision cannot cancel low recall |
| MP-SEF | Separate proposal generation from authorization. Source-anchored whole actions KEEP/P1/P2, later P3; no editwise oracle presented as an executable selector. | Separation principle REUSABLE |
| P1 | Same SWEET weights as H1, but separately versioned two-pass NoPnx. 64-case parity and frozen 1,918-source outputs. | Retain research anchor; REQUIRES_REVALIDATION for new Arabic product |
| P2 old | GED subword predictions zipped as words; 1,918/1,918 affected, 30,341 predictions dropped. Reproducibility of old outputs did not make them valid. | HISTORICAL_ONLY / FAILED_DO_NOT_REPEAT |
| P2_V2 | Repaired published GED-conditioned path, Stage0/Stage1/Stage2 with frozen source outputs. Completeness fails closed where needed. | Current independent-family research evidence; REQUIRES_REVALIDATION |
| P3_V1 | P1 NoPnx×2 followed by one SWEET Pnx pass; same family, not independent consensus. | Diagnostic alternate only; production route DEFER |
| V4 → V4.2 | Source-only preflights, atomic action legality, canonical identity/projection, scorer adversaries and runtime identity hardening. Preflight PASS is software evidence, not measured quality. | Engineering lessons REUSABLE; revisions stay traceable |
| V4.2 measurement | One authorized DEVELOPMENT measurement completed successfully; candidate-availability gate failed. Full details below. | Closed measurement REUSABLE evidence; no silent rerun |

M1 contract explicitly separates a locally correct edit from complete repair, and independent residual errors from damage introduced by an edit. Reference mismatch does not prove an error; a reference match does not prove complete repair. This survives the move from micro-edits to paragraph transformations.

## 4. Data populations and irreversible exposure

| Population | Count / identity | Exposure state and future use |
|---|---|---|
| M2-R P0 and P1 | 120 UIDs each, disjoint | Consumed development; not fresh validation |
| Reconstructable development frame | 14,017; exclude P0/P1 →13,777 | Frame/split metadata; do not equate entire frame with untouched data |
| CALIBRATION | 6,888; UID SHA-256 `3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9` | Materialized/used; 6,867 changed references +21 unchanged. Development exposure persists. |
| C_F | 1,918 UIDs /764 clusters | Permanently ADAPTIVELY_CONSUMED DEVELOPMENT / NOT CLEAN HOLDOUT |
| C_T | 2,898 UIDs /1,020 clusters | Subset of already exposed CALIBRATION; role name does not create a clean holdout |
| C_R | 2,072 UIDs /768 clusters | Same exposure caveat; no independent confirmation claim by renaming |
| INTERNAL_EVALUATION | 5,510; UID SHA-256 `55a07608bd4ffd88f9d443aa877cae0830a20f4e797621853fb5bd096c276255` | UNOPENED_RESERVED per continuity record |
| STRESS_DIAGNOSTIC | 1,379; UID SHA-256 `aa0c341451adca4bf861a0758c36f6b6629e3c3af65b5f8c9f73da2997752587` | UNOPENED_RESERVED |
| Confirmation / Holdout | Sizes not established in this snapshot | UNOPENED_RESERVED; no invented counts |
| A7'ta reserve | 88 | UNOPENED_RESERVED |
| Reserved Nahw IDs | 59; distinct from frozen 150 targets/41 passages | UNOPENED_RESERVED |
| QALB15 TEST | Count not needed here | UNOPENED_RESERVED |

C_F/C_T/C_R total 6,888 UIDs /2,552 clusters; the recorded partition has no overlap across these subroles. The remaining 13,777 UID digest is `0a03e6f5a5a7c46ef917630a9fd8fc69fea1d651141c163ed55751564c6b375c`. Split-lock commit: `40545c5150a0831ee5d0d320da6049047693ff68`.

Training overlap is separate from local access: QALB-trained model performance on QALB-derived development text is not independent generalization. A cancelled gold-aware run still creates exposure. Runs `36775239051` (failed) and `36775748058` (cancelled after at least 500/1,918 gold-aware rows) must not disappear from contamination history. V4.2 adds final adaptive consumption, not a fresh split.

## 5. Models, revisions and environments

| Component | Frozen identity |
|---|---|
| H1/P1 weights | `CAMeL-Lab/text-editing-qalb14-nopnx`; revision `21286e56ce98a86362db540863f91c083b8970f9`; weight SHA-256 `9324bd3e8bcbfd5a45d5562979cccd4279f0a7946c25a13abb10aba9cc42364d` |
| Official text-editing implementation | `4d552ca3ae98029550f27fc52aa1b22883e16e61`; H1 one pass, P1 two passes; never collapse these identities |
| P2 GEC | `CAMeL-Lab/arabart-qalb14-gec-ged-13`; revision `410588a318d988cdcfdbf64cf5745ed4adea0f6a`; weight SHA-256 `5eadbd894d7ba21e18ca53e118af20858b2e87a4d0b02f41d75e91e33919bb5f` |
| P2 GED | `CAMeL-Lab/camelbert-msa-qalb14-ged-13`; revision `447179dc63d186e4bff09a993e90e73ad622d571`; weight SHA-256 `23385ffe560860a8f5e9e46e05b66a31c33a4b0bd58e9a718933fdab8161f50f` |
| Official arabic-gec / enhanced ARETA | Revision `8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf` |
| Modified Transformers for P2 | `bc21aaca789f1a366c05e8b5e111632944886393`; replacing GED-conditioned inference with ordinary seq2seq is not equivalent |
| CAMeL Tools lock | `be79ca9fc493f0df795375a7255bafef246a802d`; morphology DB SHA-256 `195bc25a333237a2126470da888d7936b59ed3729f9210e0a4194ba43497dd70` |
| P3 | `CAMeL-Lab/text-editing-qalb14-pnx`, one punctuation-stage pass on frozen P1 final outputs; exact Pnx revision and weight/config/tokenizer hashes must be recovered from its runtime lock, not guessed from the NoPnx identity |

The proposer identity contract is mirrored as `MPSEF_PROPOSER_IDENTITY_FREEZE_V1.md`, Git blob `8b7deff8107a90ab8450af3f49bce329211faf34`. Its initial parity settings are historical; later P2_V2 source-length and completeness contracts govern the repaired full run.

Use separate reproducible environments where required. H1 stack used Python 3.10 / torch 1.12.1 / transformers 4.30; H3/H4 used Python 3.11 plus frozen CAMeL resources. Exchange JSON/JSONL rather than pickled Python objects. Environment decision commit `1f6c36d104d5d8e3d0a9746bbca2c7ec07783c97`; preflight `36653526757`; reproducibility lock `228d37d8ff525a9c597a716dbc44a1a4b063f2a7`. Future portability does not justify upgrading a historical environment and claiming identical evidence.

## 6. Normalization, ARETA and evaluation lessons

Enhanced ARETA is diagnostic stratification, nomination and coverage analysis, **not independent human gold or an authorization oracle**. MI/MT H3 strata are development proxies; boundary labels do not replace a pure-whitespace contract.

ARETA run `36656461533` failed dependency installation under Python 3.9; historical sklearn/numpy build compatibility was an operational issue. Python 3.8 fix commit `3fccd966016a832c34f7cbdae1732adb0e7664da`. Run `36657211515` then failed for missing morphology resources; corrected historical CAMeL data acquisition commit `90eb4e3dd0b36106493376efc7221422aa91a067`. Successful preflight `36657724871`, artifact `11073405357`, SHA-256 `9623141a4fb21ffaa8ff893ea6fb187610611ef854d055870c157ec86e4acfed`; pip-freeze `56b9a3964f149eeab9db64ff118287b23a63bf05eb52c6599e9b4af859a12704`. Do not reinterpret installation failures as linguistic results.

Tatweel U+0640 exposed a coordinate bug: upstream normalization removed kashida before exact character reconstruction. The frozen repair preserved tatweel in character alignment while retaining punctuation/digit normalization and cross-validating against every originally successful case. It did not remove tatweel from source/reference or drop cases. The [char-alignment amendment](evidence/2026-10-03/M2H_H1_OFFICIAL_ALIGNMENT_TATWEEL_CHARALIGN_AMENDMENT_V1.md) preserves the procedure. Apply the general lesson to English combining characters, equations and future Arabic clitics: normalization needs explicit source alignment.

H1 official alignment reconstructed all 6,888 references without final construction errors; exact NoPnx sentences 1,540/6,888, source copies 283. Scoring-only continuation after an import issue reused frozen outputs rather than rerunning generation. The provisional 30.02% proxy must not compete with the final official 69.39% recall as though they measured the same construct.

## 7. V4/V4.2 exact closure

Stage2 source-only analysis: at least one legal family action for 1,843 cases, both independent families for 1,736, SWEET-only 67, seq2seq-only 40, neither 75. Agreement: 167 UIDs /144 clusters. P3 `MIXED_FROM_P1`: 1,800/1,918. P2 completeness failed closed on 22 cases. These are action/coverage diagnostics, not quality metrics.

V4.2 run `36940844664` is **CLOSED SUCCESSFULLY / CONSUMED**. Claim scope: `DEVELOPMENT / ADAPTIVELY_CONSUMED / REFERENCE_RELATIVE / NOT_INDEPENDENT_GENERALIZATION`.

Population: 1,918 UIDs /764 clusters; 9,679 primary +129 punctuation =9,808 reference targets; 1,864 primary-error, 48 all-reference-clean and 6 punctuation-only sentences.

| Quantity | Frozen result |
|---|---|
| P1 primary recovery | 66.8251–66.8664% |
| P2 primary recovery | 58.6941% |
| P3 primary recovery | 51.1520–51.1933% |
| SWEET family | 66.9284–66.9697% |
| ROSTER oracle availability | 72.2285–72.2699% |
| P2 complementary gain beyond SWEET | 509–517 targets; +5.26–5.34 percentage points |
| P3 marginal gain beyond P1 | 6–14 primary targets; +2 punctuation targets |
| 95% availability gate | Required 9,196; upper recovery 6,995; deficit 2,201 targets /22.7301 pp; FAIL |
| ROSTER clean whole-action recovery | 23.6491–23.6905% |
| Primary complete repair | 21.8884–21.9421% of 1,864 |
| All-reference complete repair | 21.1765–21.2299% of 1,870 |
| Scoring failures | 12 group records affecting 2 UIDs; bounds preserve uncertainty and denominators |

These ranges are **scoring-failure bounds, not confidence intervals**. ROSTER is a candidate-availability oracle diagnostic, not an executable selector. Reference-unsupported extras are not automatically linguistic errors. Clean-reference candidate activity was P1 3/48, P2 36/48, P3 43/48 and roster 45/48; this is not a deployed false-positive rate.

Disposition remains P1 KEEP, P2 KEEP, P3 diagnostic same-family alternate, selector DEFER, family consensus DEFER, generic judge DEFER as primary. Candidate generation/representation required a new design; selecting among absent corrections cannot close the 22.73 pp gap. That future Arabic redesign is now itself frozen while English product work proceeds. GEC is a future Verify/Repair component, not the product objective.

## 8. Recovery anchors: runs, artifacts, hashes and commits

The manifest provides structured selected anchors; the full mirrored continuity files and lexical metadata index retain additional runs and historical identities. The following are **recorded identities**, not claims that archive bytes were redownloaded and verified in this study.

| Evidence | Workflow run → artifact | Recorded archive SHA-256 |
|---|---|---|
| CALIBRATION materialization | 36654588477 →11070819539 | `ab5f303b4405162684d9a8ece23c0ed378b25e7863129a284f3e65ca0844058a` |
| H2-v2 | 36702245858 →11090183156 | `769bcd52f897868ebcb5b64b46f217d0b0ee63b047d1815174ca2c7d3ab38d2b` |
| H3 | 36703934748 →11091545756 | `82372c564d0f05dd16b3f7cc6d141c5eb77647a2c3a4277560ab6c6dc71d7f27` |
| H4 | 36705698086 →11092051414 | `060b5ee437feefae2031108c102ee408ffe61178a813b54396599b199970994e` |
| H1 official source result | 36716848223 →11098030966 | `ad476c7dfb8e194320a1a5d4b0a05ea016be5e4b012403854290fc86ca455fb1` |
| H1 scoring continuation | 36720612925 →11101562193 | `5f3478162cb54034cb89a58a47db32f70e50573186b7df980215e56b3259e420` |
| P1 source freeze | 36765798233 →11123050529 | `e4020418ca2f2793d4bb79bc766e26838398fb9affba6d0f1c704255cd5aed46` |
| Old invalid P2 | 36768378938 →11124303107 | `5209633d389db02054456a42710a96a1d6e573cefca308254747897969c7d41c` |
| P2_V2 Stage0 | 36868057043 →11165486137 | `9cdb16ad4f3606b2af158e296a7e59e24f3718aec18d8cbc174acfa4a2d50918` |
| P2_V2 Stage2 | 36899056538 →11186450279 | `c5c5d32c99ce216a5b93362748cfefa67de4ec1f5b2b1174c8d3caf0fcd914af` |
| P3_V1 Stage2 | 36920015935 →11192760024 | `9a31de6dcff43efb903212a7fe2e2ad378f24e177faba0ecbd46ba4dd05e4253` |
| Stage2 source analysis | 36923877787 →11192953283 | `d773c8b65f607e06ce811d44d7e18deaf49c0da0c17428122d2258b043f82c4b` |
| V4.2 final measurement | 36940844664 →11200024879 | `10ecdb75b5d80540d2c9ddf5e94672e8d64bbe3eb685ca3f53d63789c3d308af` |

Frozen output hashes: P1 proposal `2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d`; P2_V2 `87dd3600293b215172f5a75dc7485915013963aa3e661310ea1adac08b9ddba7`; P3_V1 `02f9bd2555b1b9f350665179dcd96dd6accf532355a269b38ef4d099ea25d4ec`. V4.2 summary `5a649c5e050b34679e27958814201d49a948e039c38961032ced263bdacddc91`; per-sentence `0e6c51435e978c1c917b9a37a361fad1a5fe4f65da6e18b17759ad2ecb67cc50`.

Key commits: M2-R closure `54129a5111d8d58a49e5e5f85a7a3c48bfd11251`; H2/H3/H4 component freeze `50794b34b224ac867f0cadde0d2c8facc2d83fa9`; MP-SEF architecture `730b9bb944a1967180e33401fa3836fed72cbc8a`; proposer identity `b453236cf5d80c0916a0c23fd167af14edaefc85`; Stage2 protocol completion `524e3e4e63bf58a3344b90b5795550f37497b3ee`; V4.2 activation `eabbd984744d3c5551e19b537d2b5b89d9cb5d8a`; evidence lock `fdad9788e152f1747a2a695973eb04a594e7b3cf`; analysis `fe130325130f073f5e97704a5f7eecd7b040c165`; closure `fa1cee35f3fdaa5aaade3efdc7e2c4621c5f928c`.

On 2026-10-03, the [V4.2 artifact metadata](https://github.com/abdullah-s-mahmood/sweet-runtime-parity/actions/runs/36940844664) reported 60,494 bytes, `expired=false`, and expiry **2026-12-30 23:26:48 UTC**. Its remote metadata matches the recorded digest. The archive itself is not mirrored by this study; GitHub retention is not a permanent backup.

## 9. Research already reviewed and future candidates

| Source | Preserved implication and limitation |
|---|---|
| [ArbESC+, 2025 preprint](https://arxiv.org/abs/2511.14230) | Arabic edit combination/conflict selection is a future candidate; cannot create unavailable candidate corrections. |
| [STAGEET, 2026 preprint](https://arxiv.org/abs/2608.28614) | Typed staged edits merit future evaluation; checkpoint/provenance and executable parity must be established. |
| [JELV, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/40761) | Finite references miss valid edits; supplemental judge evidence does not replace human gold. |
| [CLEME2.0, ACL 2025](https://aclanthology.org/2025.acl-long.10/) | Disentangled edit evaluation informs diagnosis; reference-dependent evaluation is not deployment verification. |
| [Arabic Authorship Attribution, LREC 2026](https://aclanthology.org/2026.lrec-1.576/) | Arabic style/author resources inform future voice work; literary MSA/Gulf material is not academic-writing validation. |
| [Arabic authorship repository](https://github.com/mbzuai-nlp/arabic-authorship-attribution) | Candidate feature implementation; data/resource availability and licenses require separate checks. Local SAMER resource assumptions are not a ready commercial dependency. |
| [AraGenEval, 2025](https://aclanthology.org/2025.arabicnlp-sharedtasks.1/) | Authorship/detection benchmarks are useful but books/news differ from scholarly transformation. |

Other previously considered candidates remain unapproved: MTAGEC, AraT5, ByT5/mT5, STAGEET and a third independent family require runnable identities, provenance and overlap audits. The 2026 ZAEBUC GED+AraBART lineage is not automatically independent of P2. Gemma-3-1B Arabic GEC remains a source-only candidate while training overlap is unresolved. Do not load these merely to fill a roster.

Arabic-specific future work: discourse and rhetorical moves, clitics/morphology, orthographic ambiguity, protected normalization, mixed Arabic/Latin scientific notation, RTL document fidelity, domain terminology, authorial style and then-current detector protocols. A language port must validate these locally rather than translating English rules.

## 10. Exact preservation operation for the implementation agent

1. Adopt this snapshot plus the other three master files and manifest in a versioned architecture directory. Add a current-strategy pointer to continuity files without rewriting history.
2. Record repository/branch HEAD, all relevant refs and existing uncommitted changes; preserve them. Create a recoverable repository backup/bundle containing the relevant commits and refs; do not delete or force-reset branches. Git history does not automatically include LFS objects, submodules, ignored data, model weights or Actions artifacts: inventory each separately.
3. Copy already-existing artifacts as opaque bytes to controlled durable storage with original names, sizes, SHA-256, source run IDs, retrieval time, rights and encryption/access policy. Do not parse reserved source/reference text. Hashing/copying a closed container is preservation, not permission to expose its contents.
4. Verify the critical V4.2 result archive and frozen P1/P2_V2/P3 outputs against their recorded hashes before claiming recoverability. Preserve failed/old artifacts under their own versions; do not overwrite them with repaired variants. Recover the exact P3 punctuation lock and missing dependency-resource identities from existing metadata.
5. Build a complete storage inventory from both continuity documents and repository locks. Track `MIRRORED_VERIFIED`, `REMOTE_METADATA_VERIFIED`, `RECORDED_NOT_RETRIEVED`, `MISSING`, and `ACCESS_RESTRICTED` separately. Link expired artifacts to existing local copies if found; missing artifacts do not authorize reruns.
6. Store an independent second copy and test restoration into an isolated location by hashes and file inventory only. Do not inspect reserved datasets during a restore test. Preserve license restrictions; do not commit restricted corpora/model weights to a public repository.
7. Report completeness honestly. The local package created by this study verifies continuity and selected document mirrors; comprehensive artifact/model backup remains an implementation task. If critical evidence is unavailable, return `PRESERVATION_BLOCKER` with the inventory; the offline English harness may be prepared, but do not claim the preservation gate passed.

No further Arabic scientific work is authorized. Future resumption follows [ADD ARABIC](ACAD_PASS_LANGUAGE_EXTENSION_CONTRACT.md), starts from this evidence and its unchanged exposure boundaries, and requires a new justified protocol before any new data opening or experiment.