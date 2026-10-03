# ACAD_PASS MASTER CONTINUITY

Last updated: 2026-10-03
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `phase2-arabic-eval`

> THIS IS THE CANONICAL CROSS-CONVERSATION CONTINUITY FILE.
>
> Any new ChatGPT conversation continuing ACAD_PASS must read this file first, then read `RESUME_HERE.md` for the most recent appended checkpoint details.
>
> Update this file whenever a material result, failure, decision, agreement, protocol change, architecture change, consultation result, or exact-next-step changes.
>
> Do not restart completed stages unless this file explicitly says they are open.

---

# 1. PROJECT IDENTITY

Project:
`ACAD_PASS — Academic Document Intelligence & Transformation Platform`

Canonical architecture:

`UNDERSTAND → PROTECT → TRANSFORM/PROOFREAD → INDEPENDENTLY VERIFY → DETECT RISK → REPAIR → RE-VERIFY → ESCALATE/REVIEW → PRESERVE DOCUMENT → DELIVER`

Current strategy:
`ENGLISH_FIRST / MULTILINGUAL_READY_CORE`

Arabic research is preserved/frozen as research evidence; it is not discarded.

Core scientific principle:
**A transformation is not trusted because it sounds better. It is trusted only when protected facts, relations, scope, evidence, document structure, and scientific meaning remain verifiably correct.**

Primary architecture files:
- `phase2/academic_transform/at0_en/v2_4/AT0_EN_V2_4_FROZEN_ARCHITECTURE_V2.md`
- `docs/architecture/ACAD_PASS_MASTER_PRODUCT_ARCHITECTURE.md`
- `docs/architecture/ACAD_PASS_LANGUAGE_EXTENSION_CONTRACT.md`
- `docs/architecture/ACAD_PASS_ARABIC_RESEARCH_PRESERVATION_SNAPSHOT.md`
- `docs/architecture/ACAD_PASS_ARCHITECTURE_CHANGELOG.md`
- `docs/architecture/ACAD_PASS_EVIDENCE_MANIFEST.json`
- `docs/architecture/ACAD_PASS_HIGHER_MODEL_DELEGATION_PROTOCOL.md`

---

# 2. PERMANENT EXECUTION AGREEMENTS

## 2.1 Strict sequential execution

User requires strict sequential-only execution.

Rules:
1. Never run tool calls in parallel.
2. Multiple operations are allowed only one after another.
3. Long/fragile work is divided into coherent checkpoints.
4. Finish one checkpoint, freeze evidence/state, report, then STOP until user says `أكمل`.
5. Do not duplicate one-shot experiments.
6. If UI/network/tooling fails, resume from last verified checkpoint; do not restart completed scientific work.
7. Distinguish UI/tooling failures from scientific failures.

Initial persistence commit:
`f191445125431d7bac96423526d942050a605aa6`

## 2.2 Quantitative reporting

At every meaningful checkpoint report:
- quality delta: `IMPROVED / WORSENED / MIXED / NOT COMPARABLE`
- only scientifically valid numeric deltas
- current stage completion
- coarse whole-project completion
- blockers/unfinished work
- fresh research + brainstorming/red-team at start/end of substantive phases

Agreement commit:
`a2f01aa7dd6942e8db2b167fbc5bbb653cd8070`

## 2.3 Error-resilient mode

Known recurring UI/platform issues:
- “Our systems are thinking a bit more about this request before responding.”
- “ChatGPT stream recovery polling timed out”
- “A network error occurred. Please check your connection and try again.”

Rules:
- use shorter checkpoints
- freeze evidence early
- avoid duplicate polling/triggers
- verify external state before corrective action
- do not interpret UI/network interruption as research failure

Agreement commit:
`a2c8a92b796fe40cfb30fe1c093376661a4e3caf`

## 2.4 Higher-model consultation

Higher model is consultant/reviewer only.

Use only for:
- architecture review
- benchmark/experiment design
- construct validity
- high-stakes go/no-go decisions
- difficult research synthesis/red-team

Do NOT delegate:
- coding
- repo edits
- tests
- hashes/freezing
- routine data inspection
- standard documentation

Before consultation:
- current implementation agent completes all reasonable analysis
- sends one focused packet
- user manually forwards prompt
- higher model returns findings/risks/decision only
- implementation agent critically evaluates response

Agreement commit:
`9bef0b4dd3464d4fddec56fc64530ea4067c8b0a`

## 2.5 Reporting style

Permanent user preference:
- concise outputs
- summarize rather than repeat full technical history
- show the essential metrics in this fixed form:

`Metric | Current measured result | Strong-adoption target | Gap`

When metric is not yet measured end-to-end, report:
`NOT YET MEASURED`

Do not substitute component results for end-to-end results.

## 2.6 Arabic/English formatting

For Arabic responses:
- RTL-friendly prose
- isolate English identifiers with backticks
- avoid mixed-direction disorder

## 2.7 Continuity-file rule

This file:
`ACAD_PASS_MASTER_CONTINUITY.md`

is the canonical cross-chat reference.

`RESUME_HERE.md` remains the append-heavy operational log.

Update BOTH when any of these materially change:
- architecture
- result
- failure
- frozen evidence
- agreement
- consultation
- exact next checkpoint
- major blocker
- strong-adoption target
- current progress estimate

For a new conversation:
1. Read `ACAD_PASS_MASTER_CONTINUITY.md`.
2. Read the latest end of `RESUME_HERE.md`.
3. Verify branch HEAD.
4. Continue exact authorized next checkpoint.
5. Do not restart completed experiments.

---

# 3. PROJECT-DEFINED STRONG-ADOPTION TARGETS

These are ACAD_PASS project criteria, not claimed universal scientific standards.

## Safety — non-compensatory
- adversarial automatic acceptance: **0%**
- critical silent scientific errors: **0**
- critical uncertainty promotion to automatic PASS: **0**
- ambiguity preservation when evidence insufficient: **100%**

## Quality/usability
- automatic-PASS selective precision: **>=99%**
- authentic in-domain safe automatic acceptance: **>=90%**
- end-to-end / extracted-graph decision accuracy: **>=95%**
- controlled critical relation/ownership correctness: **100%**

## Structural
- deterministic anchor precision: **100%**
- deterministic anchor recall: **100%**
- critical evidence/provenance completeness: **100%**
- human-correct graph alignment hard gates: **100%**

Safety cannot be compensated by higher coverage.

---

# 4. CURRENT KEY METRIC LEDGER

As of 2026-10-03:

| Metric | Current measured result | Strong-adoption target | Gap / interpretation |
|---|---:|---:|---|
| Development extracted->extracted accuracy (B2.2 EE) | 100% | >=95% | exceeded on synthetic development only |
| Authentic in-domain safe auto acceptance | NOT YET MEASURED | >=90% | Gate C required |
| End-to-end automatic-PASS selective precision | NOT YET MEASURED | >=99% | later Gate C/strong-adoption validation |
| Adversarial automatic acceptance | 0% on measured B2 development | 0% | met on development evidence only |
| Critical silent scientific errors | 0 observed on measured development evidence | 0 | met on current evidence only |
| Human-correct alignment | 100% | 100% | met |
| REVIEW/ambiguity preservation | 100% development | 100% | met |
| Anchor precision / recall | 100% / 100% | 100% / 100% | met |

Do NOT present B2 development 100% as production/generalization performance.

---

# 5. ARABIC TRACK — CLOSED / PRESERVED EVIDENCE

Arabic work is NOT to be restarted unless explicitly authorized.

## Audit correction
Earlier causal comparison 88.73% -> 96.55% was invalidated because populations differed.

Same-population:
- 34/36 = 94.44%
- 28/29 = 96.55%
- delta = +2.1073 pp
- supported retention = 28/34 = 82.35%

Audit verdict:
`YES — STRONG REDESIGN OPPORTUNITY`

Arabic remains REVIEW-first.

## M1
CLOSED / DATA_READY
- QALB14 TRAIN 19,411; DEV 1,017
- reconstructable TRAIN 18,884; DEV 1,003
- failures 493
- calibration 3,829
- A7’ta parseable 463
- bootstrap 375
- reserve 88
- pilot 24:
  - 8 SUPPORTED_CORRECTION
  - 5 SUPPORTED_ALTERNATIVE
  - 7 WRONG_CORRECTION
  - 2 PARTIAL_CORRECTION
  - 2 UNNECESSARY_EDIT

## M2 monolithic
CLOSED FAIL
- P0 unsafe 4.17%, coverage 22.22%, review 37.5%
- P1 unsafe 18.75%, coverage 56.94%, review 20.83%
- no P2

## M2-R
CLOSED useful but not standalone
P0:
- CRR 82.22%
- GELR 29.14%
- CFPR 60%
- strict recall 63.33%
- precision 63.47%

P1:
- CRR 86.67%
- GELR 48.88%
- CFPR 33.33%
- strict recall 76.67%
- precision 65.50%

P1 vs P0:
- CRR +4.44 pp
- GELR +19.74 pp
- CFPR improved 26.67 pp
- strict recall +13.33 pp
- precision +2.03 pp

Closure:
`54129a5111d8d58a49e5e5f85a7a3c48bfd11251`

## M2-H / V4.2
H1 model:
`CAMeL-Lab/text-editing-qalb14-nopnx`
revision:
`21286e56ce98a86362db540863f91c083b8970f9`

H1 candidate run:
`36691616010`
artifact:
`11088155733`
46,811 candidates
- exact-reference supported 32,502
- unsupported 14,309
- availability 69.4324%

H2 lower bounds:
- HAMZA_ALIF_SEAT 85.57%
- ALIF_MAQSURA_YA 90.34%
- TA_MARBUTA_HA 94.01%
- ALIF_VARIANT 95.85%
- SINGLE_ARABIC_LETTER_ORTHOGRAPHIC 93.90%

V4.2:
- C_F 1,918 cases / 764 clusters
- one-shot run `36940844664`
- primary denominator 9,679
- ROSTER recovery 72.2285–72.2699%
- SWEET 66.9284–66.9697%
- SEQ2SEQ 58.6941%
- ROSTER over SWEET +5.26 to +5.34 pp / +509 to +517
- 95% candidate availability gate FAIL
- needed 9,196
- ROSTER upper 6,995
- deficit 2,201 / 22.7301 pp
- whole-action recovery 23.6491–23.6905%
- primary complete repair 21.8884–21.9421%

Permanent:
`C_F = ADAPTIVELY_CONSUMED DEVELOPMENT / NOT CLEAN HOLDOUT`

No silent rerun.
V4.2 CLOSED.

---

# 6. ENGLISH AT0 — V2.1

V2.1 established the initial English live feasibility boundary.

Models:
- MODEL_A Qwen3-4B-Instruct-2507 Q4_K_M
- MODEL_B SmolLM3-3B Q4_K_M
- llama.cpp commit `b92761a...`

Design:
12 cases x 2 models x DIRECT/PLANNED = 48 slots

Live run:
`37123963805`
artifact:
`11275534001`

Results:
- 48/48 recorded
- 71/72 calls
- COMPLETE_RAW 36/48 = 75%
- parse output fail 3
- parse plan fail 1
- schema output fail 8
- 35 structurally valid REVISE

Structural:
- A DIRECT 11/12 = 91.67%
- A PLANNED 12/12 = 100%
- B DIRECT 3/12 = 25%
- B PLANNED 10/12 = 83.33%

Observed semantic failures:
- evidential/causal strengthening
- claim-strength changes
- scope weakening
- misleading metric relation wording
- unsupported additions

Decision:
- ENGINEERING PASS_LIVE_WITH_ACCOUNTED_OUTPUT_FAILURES
- TRANSFORMATION FEASIBILITY MIXED
- SCIENTIFIC FIDELITY NOT ESTABLISHED
- MATERIAL DRIFT OBSERVED
- HUMAN WRITING NOT ASSESSED

V2.1 CLOSED.
HW1-EN NOT AUTHORIZED.

---

# 7. V2.2 — RULE-BASED VERIFIER FAILURE

Goal:
separate generation from packaging/verification.

Independent red-team:
run `37130259582`

12 SAFE controls + 24 attacks:
- caught 3/24
- escaped 21/24 = **87.5% escape**

Conclusion:
regex/rule approach unsafe/non-generalizable.

Key lesson:
lexical witness presence does not prove correct relation binding.

Need:
`(subject,predicate,object,qualifiers,polarity,scope)`
plus contradiction/binding logic.

Do NOT return to V2.2 patch-by-patch rules.

---

# 8. V2.3 — KNOWN REGRESSION PASS / UNSEEN FAIL

Known-external gate:
run `37134559401`
36/36 PASS

Second unseen holdout:
36 total
- 12 SAFE
- 24 ADV

Frozen hashes:
- inputs `b1633df5...`
- labels `99363773...`
- verifier `d82af97d...`
- source cases `d91fae32...`

One-shot:
run `37136722184`
artifact `11278888488`

Result:
`BOTH_FAIL`

- adversarial caught 15/24 = 62.5%
- adversarial escaped 9/24 = 37.5%
- SAFE accepted 3/12 = 25%
- safe non-pass 9/12 = 75%
- exact binary correct 18/36 = 50%
- balanced accuracy 43.75%

Dominant FN:
**relation rebinding under lexical preservation**

Dominant FP:
- paraphrase brittleness
- regex-window contamination
- negation-scope confusion
- word-order dependence
- narrow templates

Holdout consumed development evidence.
Do NOT reopen.

Closure:
`46aeaad...`

---

# 9. V2.4 ARCHITECTURE

Higher-model architecture review verdict:
`PROCEED_WITH_CHANGES`

Chosen design:
**Hybrid Scientific Assertion Frame (SAF) + Assertion Relation Graph (ARG)**

Core:
- small relation-justified graph
- explicit ownership relations
- quantity kinds / denominator / precision
- operator scope/procedure structure
- deterministic vs semantic boundary
- source extraction frozen separately
- coverage independent from confidence
- bidirectional many-to-many alignment
- outcomes:
  - PASS_CANDIDATE
  - REJECT
  - REVIEW
  - INVALID_VERIFICATION

Frozen architecture:
`phase2/academic_transform/at0_en/v2_4/AT0_EN_V2_4_FROZEN_ARCHITECTURE_V2.md`
commit:
`14db09677fb6df90e6aa688601cfe071e8138ee6`

Architecture review closure:
`4063174aa6919f0072189193203819aef6b7feb2`

---

# 10. V2.4 GATE 0

Initial contract defect found during A1:
1. anchors were assertion-local only
2. no global evidence-span inventory

Repaired:
- top-level `evidence_spans`
- top-level `anchors`
- assertion `anchor_refs`
- EXTRACT_BEFORE_OWNERSHIP
- GLOBAL_EVIDENCE_SPANS_ARE_CANONICAL
- FRAME_AND_GRAPH_MUST_AGREE
- critical frame/graph disagreement -> INVALID_VERIFICATION

Canonical validation:
run `37142006598`
artifact `11280702653`
**326/326 PASS**

Key hashes:
- schema `df986f759a114bd86525b84f00f8d2f362d71bb31546441992291d21c5ebd69f`
- criticality `1599bf6bdb10afd462ba45a422b3e276a4ddbb47656d3d6047a0ff9b39acc48d`
- outcome contract `aeff55ec0d5c10a949afc2f86a5eae46e610043f3885497643561b17aa669905`

Outcome precedence:
1. INVALID_VERIFICATION
2. REJECT
3. REVIEW
4. PASS_CANDIDATE

---

# 11. GATE A1 — DETERMINISTIC ANCHORS

Run:
`37142176334`
artifact:
`11280995699`

Development:
35 gold anchors

Results:
- predicted 35
- TP35 FP0 FN0
- precision 100%
- recall 100%
- F1 100%
- provenance 35/35

Interpretation:
PASS WITH NARROW DEVELOPMENT SCOPE

Do not claim regex catalog generalization.

Closure:
`d6c8d396b19be4b6cfb1768eb86e2ef8bcf3ac01`

---

# 12. GATE A2 — CONSERVATIVE SOURCE EXTRACTION

Purpose:
source assertion decomposition + abstention.

Important failed first run:
workflow green but manual red-team found decimal sentence-splitting bug:
42.0, 51.5, 46.2, 49.8, 4.2 split incorrectly.

This negative evidence is permanent.

Repair:
decimal-safe splitting + conservative abstention.

Final run:
`37142951015`
artifact:
`11281086502`

12 frozen synthetic cases:
- source sentences 47
- assertion candidates 50
- structural representation 47/47 =100%
- exact evidence/provenance checks 140
- relations emitted 0
- semantic ownership NOT assessed
- coverage UNKNOWN_BY_DESIGN

Statuses:
- CERTAIN 19/50 =38%
- UNCERTAIN 13/50 =26%
- AMBIGUOUS 18/50 =36%
- non-CERTAIN 62%

Classification:
`PASS AS A CONSERVATIVE STRUCTURAL SOURCE-EXTRACTION PROTOTYPE / SEMANTIC ACCURACY NOT ESTABLISHED`

Closure:
`0f8050f37ffd492d27cd732833eba1a194c90e5e`

---

# 13. GATE A3 — FIRST SEMANTIC SOURCE-EXTRACTOR SCORE

Development cases:
EN04, EN05, EN06, EN07, EN09, EN12

Gold:
28 assertions, 27 critical

Frozen thresholds:
- critical gold coverage >=95%
- overall coverage >=90%
- false-addition <=10%
- atomic 1:1 >=75%
- certain precision >=90%
- error-abstention recall >=80%
- critical silent errors =0

First score:
run `37143592151`
result initially:
`FAIL_CRITICAL_SILENT_ERROR`

Manual red-team found evaluator defect:
EN12-AS-001 assertion type RELATIONAL vs SCOPE was incorrectly classified as a critical semantic failure.

This was evaluator-contract mismatch, not extractor failure.

First score frozen:
commit `674aaf2131ecef25870e91fe249f7dffa7035db6`

Evaluator repaired WITHOUT changing extractor/gold/thresholds.

Canonical rerun:
run `37143729167`
artifact `11281706053`

Result:
`PASS_DEVELOPMENT`

Metrics:
- coverage 28/28 =100%
- critical coverage 27/27 =100%
- false additions 0%
- atomic one-to-one 22/25 =88%
- certain precision 13/14 =92.8571%
- error-abstention recall 87.5%
- unnecessary abstention 23.5294%
- context dependency detection recall 100%
- critical silent errors 0

Field diagnostics:
- assertion type 86.36%
- predicate 95.45%
- subject 90.91%
- object 100%
- polarity 100%
- modality 100%
- causality 100%

Closure:
`202395a973db9af6fc09f06017d5600df8e4e821`

---

# 14. GATE A4 — READINESS DECISION

Higher-model verdict:
`ACCEPT_AND_PROCEED_TO_ALIGNMENT`

Key rationale:
- 12% overmerge not automatically blocking
- all material observed semantic/atomicity failures were UNCERTAIN
- avoid dev-specific patching
- relation/ownership stage is the architecture's intended next component
- proceed to limited offline alignment research only

No production/generalization claim.

---

# 15. GATE B1 — HUMAN-CORRECT ALIGNMENT

First aligner score:
run `37145678669`

Result:
`FAIL_B1_HUMAN_CORRECT`

Metrics:
- pair outcome 10/12 =83.33%
- critical coverage 20/22 =90.91%
- critical status accuracy 95%
- adversarial acceptance 1
- faithful false rejection 1
- uncertainty preservation 100%
- evidence trace 100%

Failures:
B1-P03:
faithful many-to-one merge falsely rejected

B1-P04:
Group A/B values swapped but aligner cross-matched by value and falsely accepted

Repair principles:
- owner/entity-first assignment
- canonical split/merge binding facts
- non-compensation: equal value cannot compensate wrong owner
- relation-aware assignment

B1.1 final:
run `37146333162`
artifact `11282215627`

Result:
`PASS_B1_HUMAN_CORRECT`

- pair outcomes 12/12 =100%
- critical alignment coverage 22/22 =100%
- critical status accuracy 100%
- adversarial acceptance 0
- false rejection 0
- uncertainty preservation 100%
- evidence trace completeness 100%
- repair regressions 3/3 PASS

Improvement:
- accuracy +16.67 pp
- critical coverage +9.09 pp
- critical status +5 pp
- adversarial acceptance 1 ->0
- false rejection 1 ->0

Closure:
`c170e2053158d7cdb3032be1ab7f4faff1102ed8`

---

# 16. GATE B2 — EXTRACTED-GRAPH DEGRADATION

Four-arm design:
- GG = gold source -> gold candidate
- GE = gold source -> extracted candidate
- EG = extracted source -> gold candidate
- EE = extracted source -> extracted candidate

Canonical first B2:
- GG 100%
- GE 41.67%
- EG 50%
- EE 33.33%
- EE safe acceptance 0%
- EE adversarial acceptance 0%
- REVIEW preservation 100%

Verdict:
`MIXED_B2_REPAIR_REQUIRED`

Important:
safety remained conservative, usability collapsed.

Diagnosis of 8 wrong EE pairs:
- predicate/paraphrase/scope/decomposition: 4/8 =50%
- split/merge owner/value or meaning binding: 2/8 =25%
- missing explicit semantic relation: 1/8 =12.5%
- equation/symbol structured ownership: 1/8 =12.5%

Bridge invalid records: 0.
GG aligner: 100%.
Therefore extraction/representation is primary target.

Higher-model B2.1 verdict:
`HYBRID_RELATION_AWARE_EXTRACTION_REPAIR`

Keep A2.
Add relation-aware structured layer.
Do not tune aligner to compensate.

Mandatory capabilities:
1. predicate/paraphrase normalization
2. negation/scope ownership
3. owner/value and owner/meaning split/merge binding
4. citation-to-claim binding
5. equation/symbol/coefficient binding

Deferred:
- generic procedural parser
- generic local coreference resolver
- broad semantic parser
- general algebraic equivalence

---

# 17. B2.2 HYBRID RELATION-AWARE REPAIR

A2 and B1.1 aligner remained frozen.

Prototype added:
- deterministic-first relation-aware layer
- scientific predicate normalization
- explicit modality preservation
- explicit negation handling
- canonical group/value ownership
- explicit citation binding
- explicit equation coefficient/symbol binding
- ambiguity preservation

Important authentic-text blind spot found:
initial authentic qualitative check:
- 5/5 authentic excerpts AMBIGUOUS
- 0 invented relations

Repair:
explicit scientific predicates:
DEFINE, AIM_TO, TREAT, USE_FOR, INTRODUCE
plus modality/negation red-team.

Final:
- 17/17 principle/red-team regressions PASS
- authentic qualitative check 5/5 CERTAIN
- unsupported invented relations 0

Canonical B2.2 revalidation:
run `37150199075`
artifact `11283159352`

Results:
GG:
- accuracy 100%
- safe acceptance 100%
- adversarial acceptance 0

GE:
- accuracy 91.67%
- safe acceptance 80%
- adversarial acceptance 0

EG:
- accuracy 91.67%
- safe acceptance 80%
- adversarial acceptance 0

EE:
- accuracy 100%
- safe acceptance 100%
- adversarial acceptance 0
- REVIEW preservation 100%
- false rejection 0
- uncertainty promotion 0

Representation audit:
- 24 sides
- 102 checks
- 0 failures

Improvement vs first B2:
- EE accuracy 33.33% ->100% = +66.67 pp
- EE safe acceptance 0% ->100% = +100 pp
- GE +50 pp accuracy
- EG +41.67 pp accuracy
- no adversarial regression

Shared-error safeguard triggered because EE=100% while GE/EG=91.67%.

P01 review:
classification:
`CANONICALIZATION_FIXTURE_MISMATCH / NOT_SHARED_SEMANTIC_ERROR`

Cause:
relation evidence sentence creates one redundant but text-supported MATERIAL assertion in extracted graph, while gold encodes same material only as relation evidence.

No repair performed.
GE/EG intentionally remain 91.67%.

Gate B2 final:
`PASS_B2_EXTRACTED_DEVELOPMENT`

Final closure:
`ff56323d1c9a75211eaf33dc753d2a6a642166f9`

---

# 18. PRE-GATE-C PIPELINE FREEZE

Purpose:
freeze complete verifier before untouched authentic evaluation.

Canonical pipeline-freeze run:
`37150864483`

Artifact:
`11284520199`

Artifact SHA-256:
`74f765f614b616da2eb101c30d669de0c0931b304a377944be2a4039fe5a844c`

Frozen core:
- schema
- criticality rules
- outcome contract
- A1
- A2
- B2.2 relation-aware layer
- B1.1 aligner
- architecture identity

First freeze run failed because checker repo root path was one directory too high.
This was tooling-only.
Runtime unchanged.
Second run passed.

Freeze rule:
**Any runtime change after final Gate C protocol freeze creates a new pipeline version.**

---

# 19. FINAL GATE C PROTOCOL

Higher-model verdict:
`ACCEPT_WITH_ESSENTIAL_PROTOCOL_AMENDMENTS`

Higher model explicitly performed deep research and red-team methodology review.

Final protocol:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_PROTOCOL_FINAL_V1.md`

Protocol commit:
`2f9286614741c8168c6e45b8f9fb7a7366e4a18a`

Protocol SHA-256:
`f41fdc9aa6c574447779858cdbd5a2dec83a9851c81408cc415be58c8eda1d1e`

Final integrity run:
`37153113766`

Artifact:
`11284443202`

Artifact digest:
`7a1bfbdd09cf51c5d8ad0e71bff7db0853d26eff47b6742558005ca3e70b5a3f`

Integrity:
- 19 protocol checks PASS
- 9 pipeline identities PASS
- holdout_opened = false
- source_sampling_authorized = false

## Gate C design

80 independent original studies/papers.

5 domains x 16:
1. CS/Engineering
2. Biomedical/Life Sciences
3. Physical/Materials Sciences
4. Environmental/Earth Sciences
5. Social/Behavioral Sciences

Temporal mix per domain:
- target 8 first publicly available in 2026
- target 8 older unseen

Transactions:
- 80 faithful PASS
- 80 material-drift REJECT
- 40 ambiguity REVIEW
- 200 total

Primary statistical independence unit:
**original study/paper**

## Gate C hard progression gates

Safety:
- Gold REJECT -> automatic PASS: 0/80
- Gold REVIEW -> automatic PASS: 0/40
- critical silent scientific errors: 0
- unsupported critical evidence used for auto decision: 0

Usability:
- faithful safe acceptance >=60/80 =75%
- decisive material-drift REJECT >=60/80 =75%
- REVIEW preservation >=36/40 =90%

Evidence:
- reference completeness 100%
- semantic support 100%
- decision-path linkage 100% where recorded

INVALID_VERIFICATION:
- separate
- never success
- remains in denominators

## Statistical plan

- source study = independence unit
- cluster bootstrap whole source clusters within domain
- exact one-sided binomial bounds for zero-event safety
- do not interpret 0/80 as 0 true risk
- simple 0/80 upper 95% bound ≈3.68%
- simple 0/40 upper 95% bound ≈7.22%

Strong-adoption <1% simple zero-error boundary:
**299 appropriately independent decisions**, for the relevant claim.

Do NOT count correlated sibling transactions as independent.

---

# 20. HUMAN REVIEWER PROBLEM AND INTERNET SOLUTION

User has NO pre-existing human reviewers.

This must NOT automatically force the protocol to weaken.

Preferred non-provisional solution:
`INTERNET_RECRUITED_QUALIFIED_HUMAN_ADJUDICATION`

Plan file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_INTERNET_EXPERT_ADJUDICATION_PLAN_V1.md`

Plan commit:
`710367d45b5cb2b8b2138da29ad1118230e851d1`

## Primary recruitment options

### Kolabtree
Use for domain-specific scientists / peer-review consultants.
Good for:
- subject-specific academic expertise
- private projects
- peer-review consulting
- NDA/confidentiality

### Prolific Domain Experts
Use for verified specialist recruitment.
Verification can include:
- skills assessments
- academic/professional credentials
- publication history
- work experience

Prolific supports expert pools including STEM, healthcare, senior professionals and AI/fact-checking-related expertise.

## Reviewer structure

Per domain:
- Reviewer A
- Reviewer B
- reserve/adjudicator C

Target:
- 10 primary reviewers total
- up to 5 reserve/adjudicators

Two independent judgments per Gate C transaction.
Third only for unresolved material disagreement.

## Reviewer qualification

Platform verification alone is not enough.

Freeze a qualification pack containing:
- scientific-fidelity judgments
- evidence span selection
- ambiguity vs difficulty
- critical relation ownership
- materiality

Public expert-annotated scientific verification data can be used for calibration/qualification.

Example:
**SciFact**
- expert-written scientific claims
- SUPPORT/CONTRADICT labels
- evidence/rationales

SciFact is calibration material only.
It does NOT replace Gate C because its construct differs from academic transformation fidelity.

## Low-budget fallback

If qualified humans cannot be recruited:
Gate C may run as:
`PROVISIONAL_RESEARCH_EVIDENCE`

Fallback can combine:
- multiple independent model judges
- deterministic evidence checks
- expert-labeled public calibration data
- disagreement escalation

But:
- do not call it independent human gold
- do not claim non-provisional Gate C
- do not use it for Strong-Adoption claims

---

# 21. CURRENT HOLDOUT-OPENING CONDITIONS

Final eight conditions:

1. scope/context freeze
2. 80-study sampling/temporal/de-duplication/exposure rules freeze
3. family/REVIEW/replacement policy freeze
4. qualified adjudicators + adjudication guide
5. role/access separation + neutral IDs + sealed-gold mechanism
6. full pipeline/runtime/settings re-verification
7. metrics/statistics/evidence-audit/report-weight freeze
8. one-shot failure/exclusion/gold-correction/full-report policy freeze

Current:
- conditions 1,2,3,6,7,8 substantially specified
- conditions 4 and 5 require operational setup

Therefore:
`SOURCE_SAMPLING_NOT_YET_AUTHORIZED`

Do NOT select/open the 80 Gate C sources yet.

---

# 22. CURRENT EXACT NEXT CHECKPOINT

`AT0-EN V2.4 PRE-GATE-C — HOLDOUT-OPENING READINESS SETUP`

Scope:
1. finalize reviewer qualification pack
2. finalize reviewer qualification thresholds
3. define recruitment brief for each domain
4. determine practical reviewer recruitment route (Kolabtree / Prolific Domain Experts / hybrid)
5. define reviewer neutral IDs/assignment
6. define gold access separation
7. define constructor vs gold vs prediction-runner role separation
8. verify all eight opening conditions

Only after this checkpoint passes:
`SOURCE_SAMPLING_AUTHORIZED`

Not authorized now:
- selecting Gate C source papers
- opening source passages
- candidate construction
- Gate C gold labeling
- Gate C predictions
- live generation
- HW1-EN
- production claims

---

# 23. WHOLE-PROJECT PROGRESS

Current coarse planning estimate:
**approximately 35% ±5%**

This is a planning estimate, not a scientific metric.

PRE-GATE-C final protocol freeze:
100% complete.

PRE-GATE-C overall:
approximately 85% complete.

---

# 24. IMPORTANT NEGATIVE EVIDENCE — NEVER ERASE

Keep all these visible:

- Arabic causal comparison invalid due population mismatch
- M2 monolithic FAIL
- V4.2 candidate availability FAIL
- V2.1 material semantic drift despite structural success
- V2.2 adversarial escape 87.5%
- V2.3 unseen holdout BOTH_FAIL
- A2 first run decimal segmentation bug
- A3 first score false critical error due evaluator defect
- B1 first aligner 83.33% FAIL with owner/value rebinding acceptance
- B1.1 first regression attempt failed coordinated-owner normalization
- B2 first EE 33.33%, safe acceptance 0%
- B2 duplicate post-UI run must not be double-counted
- authentic B2.2 first qualitative check 5/5 AMBIGUOUS
- B2.2 red-team caught positive parsing of “does not treat”
- B2.2 GE/EG stayed 91.67% while EE 100%; P01 reviewed as canonicalization fixture mismatch
- PRE-GATE-C first freeze checker failed due repo-root path, tooling only

These failures are part of the research evidence and must not be overwritten.

---

# 25. NEW-CONVERSATION BOOTSTRAP

When this conversation reaches its limit, user can open a new conversation and say:

`Continue ACAD_PASS from the canonical continuity files in repository abdullah-s-mahmood/sweet-runtime-parity, branch phase2-arabic-eval. Read ACAD_PASS_MASTER_CONTINUITY.md first, then the latest end of RESUME_HERE.md, verify branch HEAD, and continue only the exact authorized next checkpoint. Do not restart completed stages, do not rerun consumed one-shot experiments, preserve all permanent execution agreements, use sequential-only tool execution, and update both continuity files after every material result/failure/decision.`

The new conversation should not need the user to restate the full project history if repository access is available.

---

# 26. DO-NOT-DO LIST

Do NOT:
- restart Arabic track
- reopen consumed V2.3 holdout
- silently rerun one-shot evaluations
- claim development 100% = production 100%
- open Gate C before all 8 opening conditions pass
- replace qualified human adjudication silently with LLM consensus
- tune frozen Gate C verifier after predictions
- change gold after reveal without preserving original result
- drop INVALID cases from denominators
- use aggregate usability to compensate safety
- use pair-ID-specific repairs
- modify aligner to hide extraction defects
- create new architecture unless evidence demands it
- use higher model as implementation agent
- run tools in parallel
- duplicate runs after UI errors without verifying external state

---

# 27. FINAL CURRENT STATE

Pipeline:
**FROZEN**

Gate B:
**COMPLETE / DEVELOPMENT PASS**

Gate C protocol:
**FINAL / FROZEN / INTEGRITY PASS**

Gate C holdout:
**UNOPENED**

Human reviewer pool:
**NOT YET RECRUITED**

Reviewer problem:
**SOLVABLE VIA INTERNET-RECRUITED QUALIFIED EXPERTS**

Current authorization:
`PRE-GATE-C HOLDOUT-OPENING READINESS SETUP ONLY`

Exact next work:
**Reviewer qualification + recruitment/access-separation setup.**


---

# 28. NO-NEW-HUMAN GATE C ALTERNATIVE — RESEARCH UPDATE

Date: 2026-10-03

User requested aggressive deep research/brainstorming to avoid recruiting new human reviewers if scientifically defensible.

New researched conclusion:

`EXTERNAL_HUMAN_GOLD_COMPOSITE_VALIDATION`

is a plausible replacement for most or all newly-created Gate C human gold.

Research plan:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_NO_NEW_HUMAN_ALTERNATIVE_RESEARCH_V1.md`

Commit:
`a8a613f28988046ccd37411760cbf8aa4c66a0cb`

Core idea:
replace bespoke new human adjudication with multiple independent published human/expert-labeled benchmarks + deterministic ACAD_PASS-specific metamorphic tests.

Candidate external human-gold tracks:

1. SciFact
   - expert-written scientific claims
   - SUPPORT/CONTRADICT labels
   - evidence rationales

2. SciFact-Open
   - open-domain scientific verification
   - large research-abstract corpus
   - annotated evidence

3. QASPER
   - 5,049 questions over 1,585 research papers
   - practitioner answers
   - supporting evidence paragraphs

4. DeFacto
   - human corrective instructions
   - human-edited corrected summaries
   - natural-language explanations

5. TRUE
   - standardized collection of 11 manually annotated factual-consistency datasets

6. SummaC / AGGREFACT / FRANK
   - multiple human-labeled factual-consistency benchmarks
   - error typologies and de-duplicated factuality cases

7. FENICE long-form annotations
   - human factuality annotations for long-form summarization

8. QASemConsistency 2026
   - >3K fine-grained human factual-consistency annotations
   - localized error evidence

9. Clinical-study summarization human factuality annotations

10. PlainFact / PlainQAFact
    - fine-grained human biomedical factual-consistency data

11. USB
    - six-domain human-labeled benchmark
    - evidence, factual accuracy, unsubstantiated spans, factual-error correction

12. Deterministic metamorphic ACAD_PASS track
    - oracle-free relation tests
    - owner/value swap
    - negation flip
    - modality strengthening
    - association->causation
    - citation-owner swap
    - equation coefficient-variable swap
    - baseline/denominator/time/scope mutations
    - faithful split/merge transformations

Scientific boundary:
- no single public dataset fully matches ACAD_PASS academic rewrite fidelity;
- composite triangulation can provide strong external validation;
- external labels require preregistered dataset-specific adapter contracts;
- do not naively map SUPPORT=PASS or NEI=REVIEW without construct validation;
- the strongest defensible claim would be:
  `NON_PROVISIONAL_EXTERNAL_BENCHMARK VALIDATION`
  for constructs represented by the selected benchmarks;
- do NOT call it `fresh bespoke human-adjudicated Gate C`.

Potential new structure:
- `Gate C-EXT`: published independent human-gold composite validation
- `Gate C-META`: deterministic metamorphic relation validation

Only if a journal/reviewer later demands bespoke fresh human labels:
run a small targeted residual human study instead of 200 new adjudications.

Immediate recommendation:
DO NOT recruit reviewers yet.
DO NOT open the custom 80-study holdout yet.

Exact next checkpoint proposed:
`PRE-GATE-C — EXTERNAL HUMAN-GOLD COMPOSITE FEASIBILITY AUDIT`

Audit tasks:
1. inventory candidate datasets;
2. verify licenses/downloadability;
3. inspect label schemas;
4. quantify usable public labeled examples;
5. detect overlap/deduplicate;
6. freeze dataset-specific ACAD_PASS adapter contracts;
7. map construct coverage/gaps;
8. decide whether new human adjudication can be removed entirely or reduced to a small residual study.

No V2.4 runtime changes.


---

# 29. EXTERNAL HUMAN-GOLD COMPOSITE FEASIBILITY AUDIT — CLOSED

Date: 2026-10-04

Audit:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/EXTERNAL_HUMAN_GOLD_COMPOSITE_FEASIBILITY_AUDIT_V1.md`

Commit:
`609d9ca39d5fbb333887c6f09b85a36b8d554b9d`

Verdict:
`FEASIBLE_WITHOUT_NEW_HUMAN_ADJUDICATORS_FOR_RESEARCH_PROGRESSION`

Primary core tracks identified:
- DeFacto
- PLABA
- CLEF SimpleText 2025 manually annotated real scientific simplifications if accessible
- SciFact
- QASemConsistency
- USB
- PlainFact positive biomedical fidelity track

Secondary/diagnostic:
- QASPER
- TRUE
- AggreFact
- FENICE
- optional non-overlapping SciFact-Open
- Cochrane-auto
- small 2026 expert-edited scientific simplification corpus

Important new discoveries:
- DeFacto official Microsoft repo is MIT licensed and contains 2561 examples, 1821 with errors, with human evidence/explanation/correction.
- QASemConsistency public repo is Apache-2.0 and includes raw multi-annotator predicate-argument support annotations.
- USB Hugging Face dataset is Apache-2.0 and includes evidence, factual accuracy, unsubstantiated spans and correction.
- PlainFact is CC BY-SA 3.0, 200 summary/abstract pairs and 2740 sentences.
- PLABA provides 750 PubMed abstracts and 7643 expert adaptation sentence pairs.
- TREC PLABA includes professional references and biomedical-expert manual faithfulness/completeness evaluations.
- CLEF SimpleText 2025 is extremely close to ACAD_PASS: scientific simplification + hallucination/information-distortion tasks, including manually annotated real system submissions; synthetic training distortions must not be counted as external human gold.
- CLEF 2026 explicitly reuses 2025 manual annotations as ground truth for distortion classification.

Proposed new structure:
- Gate C-EXT-1: direct scientific transformation fidelity
- Gate C-EXT-2: scientific claim/evidence fidelity
- Gate C-EXT-3: fine-grained relation fidelity
- Gate C-EXT-4: human correction/repair
- Gate C-EXT-5: biomedical stress
- Gate C-EXT-6: cross-domain transfer
- Gate C-META: deterministic ACAD_PASS-specific metamorphic relation testing

Adapter rule:
Do not force all datasets into PASS/REJECT/REVIEW.
Retain native labels unless an exact semantic adapter is preregistered.

Overlap control:
- SciFact-Open vs SciFact
- TRUE vs its component datasets
- AggreFact vs original components
- QASemConsistency underlying source datasets
- DeFacto derivatives
- PLABA/TREC source identity
must be deduplicated by source IDs/hashes.

Research progression:
new human adjudication is NOT currently judged necessary.

Strong-adoption boundary:
external composite can support non-provisional external-human-gold validation for represented constructs, but does not establish deployment prevalence, universal academic-domain coverage, or <1% production error.

High-stakes next decision:
final independent construct-validity review is required before replacing the already-frozen custom Gate C protocol.

Consultation packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/NO_NEW_HUMAN_HIGHER_MODEL_CONSULTATION_PACKET_V1.txt`

Commit:
`9d015241f52244448f7ccb9800e0a473f8a7f213`

Exact next action:
USER MEDIATES higher-model consultation.

Until response:
- do not recruit human reviewers;
- do not open custom 80-study holdout;
- do not execute external datasets;
- do not modify V2.4 runtime.

