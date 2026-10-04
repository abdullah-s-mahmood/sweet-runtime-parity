# ACAD_PASS MASTER CONTINUITY

Last updated: 2026-10-04
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

Current authorized path:
`PRE-GATE-C EXT/META — USER-MEDIATED FOCUSED INDEPENDENT REVIEW OF FACTPICO H1 CONTRACT V4`

FactPICO physical artifact is fully frozen.
H1 Contract V4 is now frozen for focused methodological review.

Preferred contract:
`H1_FACTPICO_HARD_GOLD_CONTRACT_V4.md`

Focused review packet:
`H1_FACTPICO_V4_FOCUSED_REVIEW_PACKET.txt`

Review scope is deliberately narrow to conserve higher-model usage:
- N/A policy;
- double-annotation cutoff;
- Results aggregate error rule;
- source-bounded safe-control rule;
- severe Alpaca skew / safe-control status;
- 75% micro+source-macro thresholds.

Still not authorized:
- H1 adapter implementation;
- V2.4 FactPICO predictions;
- H1 scoring;
- V2.4 modification;
- threshold changes after prediction;
- original custom Gate C opening;
- new-human recruitment;
- Arabic-track work.

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

Original custom Gate C protocol:
**FINAL / FROZEN / INTEGRITY PASS / PRESERVED**

Original custom Gate C holdout:
**UNOPENED**

Human reviewer pool:
**NOT RECRUITED / RECRUITMENT DEFERRED**

Current preferred research-progression route:
**Gate C-EXT + Gate C-META**

First no-new-human consultation:
`YES_WITH_ESSENTIAL_CHANGES`

Second independent pre-execution review:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Protocol:
`GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`

Readiness:
`GATE_C_EXT_META_READINESS_V2.md`

Condition 1 of 10:
`PASS`

Conditions 2-10:
`NOT YET PASS`

Current overall readiness:
`NOT_READY_GATE_C_EXT_META`

Current authorization:
`DATASET / VERSION / SPLIT / ADAPTER / METRIC / OVERLAP FREEZING ONLY`

External verifier execution:
**NOT AUTHORIZED**

Exact next work:
**Freeze external dataset identities, label contracts, measurable-output adapters, denominators/statistics, overlap/source clusters, and independent META oracles.**

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



---

# 30. NO-NEW-HUMAN HIGHER-MODEL CONSULTATION — RECEIVED / ACCEPTED WITH CHANGES

Date: 2026-10-04

Independent verdict:
`B — YES_WITH_ESSENTIAL_CHANGES`

Core decision:
- `Gate C-EXT + Gate C-META` may replace the custom newly-human-adjudicated Gate C for the next research-progression decision.
- do not recruit new human reviewers now;
- original 80-study Gate C remains frozen, preserved and unopened;
- residual human validation becomes:
  `DEFERRED — CONDITIONALLY REQUIRED FOR UNCOVERED CLAIMS`.

Consultation corrections accepted:
- PLABA is not automatically PASS gold;
- PlainFact stays secondary unless exact human-validation semantics justify use;
- CLEF SimpleText external human gold must use genuinely human-annotated real-system material, not synthetic distortions;
- QASemConsistency is relation-level, not complete-source preservation;
- metamorphic testing is complementary and needs anti-degenerate controls;
- support and completeness are separate constructs;
- native dataset semantics must be retained unless exact mapping is justified;
- no weighted aggregate may compensate safety failure.

New prioritized benchmarks:
- FactPICO (ACL 2024);
- FaReBio (EMNLP Findings 2024);
- LongSciVerify (LREC-COLING 2024).

Fresh implementation-agent source verification confirmed:
- FactPICO provides expert fine-grained PICO/finding factuality judgments;
- FaReBio provides expert faithfulness + supporting-evidence annotations;
- LongSciVerify provides human fine-grained factual-consistency annotations for long scientific summaries;
- CLEF SimpleText 2026 officially states that manual 2025 annotations are reusable as ground truth for distortion classification.

Decision record:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/NO_NEW_HUMAN_HIGHER_MODEL_CONSULTATION_DECISION_V1.md`

Decision record commit:
`d6dbb95053a2d95a1d273eeff9a71e00afbfa988`

Quality delta:
`IMPROVED`
because the replacement is now independently reviewed, construct boundaries are tighter, and three stronger scientific fidelity resources were added to priority audit.

No runtime change.
No benchmark execution.
No custom holdout opening.

---

# 31. GATE C EXT/META PROTOCOL AMENDMENT + READINESS — FROZEN FOR REVIEW

Date: 2026-10-04

Protocol amendment:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PROTOCOL_AMENDMENT_V1.md`

Commit:
`7ad010a95373ecb7626bf1bea5a3b68979a08385`

Readiness contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_READINESS_V1.md`

Commit:
`99803dee149e8c5f8ba6d30e830d27556f4766b9`

Independent pre-execution review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PREEXECUTION_REVIEW_PACKET_V1.txt`

Commit:
`5e18d6e71e7a4d2720d81c4d53d117a4bdb11b8f`

Hard-gate functions frozen for review:
- H1 scientific transformation fidelity;
- H2 scientific claim/evidence fidelity;
- H3 fine-grained relation fidelity;
- H4 ACAD_PASS deterministic metamorphic validation.

Diagnostic-by-default:
- DeFacto;
- USB;
- PlainFact;
- QASPER;
- FENICE;
- TRUE or AggreFact;
- expert-edited 2026 simplification corpus;
- other long-document tracks unless promoted before results.

Readiness:
`NOT_READY_GATE_C_EXT_META`

Ten mandatory conditions must pass before any external-suite verifier execution.

Exact next action:
`USER-MEDIATED HIGHER-MODEL PRE-EXECUTION REVIEW`

Until response:
- no external benchmark execution;
- no custom 80-study holdout opening;
- no new-human recruitment;
- no V2.4 runtime change.


---

# 32. SECOND EXT/META PRE-EXECUTION REVIEW — ACCEPTED WITH ESSENTIAL CHANGES

Date: 2026-10-04

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

The reviewer explicitly authorized progression to:
`dataset / version / split / adapter / metric / overlap freezing`

with:
`ZERO NEW-HUMAN RECRUITMENT AT THIS STAGE`

No benchmark execution is authorized yet.

Five accepted methodological changes:
1. H1 is defined by two required functions, not dataset count:
   - output-content support/factuality;
   - preservation/completeness of required source content.
2. H2/H3 must be measurable from actual frozen V2.4 outputs without a new semantic inference layer.
3. evidence-location correctness and semantic-support correctness are separate audits.
4. META oracle must be independent from both verifier output and extractor semantic assumptions/rules.
5. per-track denominators/sample targets/success rules/missing-output handling must be frozen before prediction.

H1 resource classification:
- FactPICO = `CONDITIONAL SUBSTITUTE`
- FaReBio = `CONDITIONAL SUBSTITUTE`
- LongSciVerify = `DIAGNOSTIC ONLY`

Current preferred H1 freeze candidates:
- human-annotated real-system CLEF SimpleText material;
- eligible PLABA/TREC judgments that actually establish the required preservation/completeness function.

FactPICO/FaReBio are added only if they close a documented H1 construct gap.

No diagnostic dataset is promoted to hard now.

Review decision:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PREEXECUTION_REVIEW_DECISION_V2.md`
commit:
`41f518392a6aab3af4e1c0f0d2834a5736e02377`

Revised protocol:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md`
commit:
`a8cd52bb731a53e1a72de6984a2eb3308fad7966`

Revised readiness:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/GATE_C_EXT_META_READINESS_V2.md`
commit:
`73c7e5673b4bbcc708e2eb69eb745c91d3e713e6`

Quality delta:
`IMPROVED`

Reason:
- stronger construct separation;
- stronger adapter boundary;
- independent META oracle requirement;
- no empty denominators;
- explicit source-cluster/sample-target precommitment;
- public-gold independence claim narrowed correctly.

No runtime change.
No external prediction.
No custom holdout opening.
No human recruitment.

Exact next checkpoint:
`PRE-GATE-C EXT/META — DATASET / VERSION / SPLIT / ADAPTER / METRIC / OVERLAP FREEZE`


---

# 33. H1 DATASET / VERSION / ACCESS / LABEL AUDIT V1 — FROZEN

Date: 2026-10-04

Audit:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_DATASET_VERSION_ACCESS_LABEL_AUDIT_V1.md`

Commit:
`87485c350c148668fcba85fc6d6bca802b1c5001`

Readiness update commit:
`4025a5a295228e47ba7509d3acbb03027638daba`

Quality delta:
`IMPROVED / ACCESS-BLOCKED`

Key findings:

### CLEF SimpleText 2025
- official track identity verified;
- official 2026 documentation confirms manual 2025 annotations are reused as ground truth for information-distortion classification;
- current public Codabench remains operational;
- official site says data are available to registered participants;
- actual annotation artifact bytes/IDs are not yet frozen;
- repository has no declared top-level license metadata;
- H1-S = strong candidate;
- H1-C = unresolved until exact human annotation coverage is inspected.

### PLABA original dataset
- version-of-record DOI:
  `10.1038/s41597-022-01920-3`
- 750 manually adapted biomedical abstracts;
- 7,643 sentence pairs;
- public OSF identity confirmed;
- canonical public artifact named `data.json`;
- direct OSF artifact retrieval failed through current tooling;
- article is CC BY 4.0, but dataset-specific license is not separately verified;
- PLABA references allow omission and therefore are NOT automatic full-content PASS gold.

### TREC PLABA 2023
- completeness/faithfulness manual judgments apply to selected question-relevant sentences;
- therefore H1-C coverage is partial/sampled only.

### TREC PLABA 2024
- complete abstract adaptation;
- expert manual evaluation includes:
  simplicity, accuracy, completeness, brevity;
- completeness explicitly targets information loss from the original;
- retrospective PLABA paper confirms extensive biomedical-expert manual evaluation;
- strongest current PLABA-family H1-C candidate;
- actual reusable judgment artifact and reuse terms remain unfrozen.

Current readiness:
- condition 1 = PASS;
- condition 2 = PARTIAL / NOT PASS;
- condition 3 = PARTIAL / NOT PASS;
- conditions 4-7,9 = NOT READY;
- condition 8 = PARTIAL;
- condition 10 = PARTIAL.

Overall:
`NOT_READY_GATE_C_EXT_META`

Important negative evidence:
- publication license cannot substitute silently for dataset license;
- public task descriptions cannot substitute for artifact bytes/hashes;
- sample human evaluation cannot be represented as exhaustive gold;
- no H1 adapter is authorized until exact record-level gold is frozen.

Exact next checkpoint:
`H1 ACCESS + ARTIFACT RESOLUTION`


---

# 34. H1 ACCESS + ARTIFACT RESOLUTION V1 — SUBSTANTIALLY RESOLVED

Date: 2026-10-04

Resolution file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_ACCESS_ARTIFACT_RESOLUTION_V1.md`

Commit:
`f88fe5b599ade9b85e6a301b350bc33c2163e331`

Readiness update:
`451c4a19b8b825d5de2df026152b19bff79fbe16`

Quality delta:
`IMPROVED`

Major finding:
a public Zenodo dataset now exposes raw PLABA manual judgments for TREC 2023-2024.

Zenodo DOI:
`10.5281/zenodo.18637045`

Key 2024 complete-rewrite artifact under the retrospective taxonomy:
`manual-judgments-task1-2024.zip`

Publisher-provided MD5:
`589ad66e0b9324592f0151cc67974015`

Critical naming ambiguity resolved:
- original TREC 2024 event page:
  `Task 2 = Complete Abstract Adaptation`
- retrospective paper/Zenodo normalization:
  `Task 1 = Rewriting abstracts`

Therefore for Zenodo manual judgments the complete-rewrite archive is:
`manual-judgments-task1-2024.zip`

Do not select the 2024 `task2` judgment ZIP for H1 complete-rewrite fidelity.

The retrospective peer-reviewed paper establishes 2024 rewrite manual axes:
- ACC = accuracy relative to source;
- COM = completeness / minimizing information loss;
- SIM = simplicity;
- BRV = brevity;
- FIN = aggregate.

It reports 19 complete-rewrite submissions and sentence-level evaluation across all 400 test abstracts.

Current H1 conceptual core:
- H1-S <- ACC
- H1-C <- COM

No binary PASS/REJECT adapter mapping has been authorized.

NIST/TREC public archive now exposes the original 2024 complete-adaptation corpus URL.

Rights/use:
- TREC research-use path is documented through its data-sharing framework;
- Zenodo record is publicly Open;
- Zenodo rendered metadata does not declare an explicit license;
- exact applicable reuse agreement must still be frozen before execution.

FaReBio:
- identity/version and expert faithfulness/evidence construct verified;
- public for research only;
- remains conditional H1-S corroboration, not mandatory H1-C.

SimpleText:
- remains useful/optional;
- participant/Codabench access remains;
- no longer a mandatory blocker for H1.

Readiness:
- condition 1 = PASS;
- condition 2 = SUBSTANTIAL PARTIAL / NOT PASS;
- condition 3 = SUBSTANTIAL PARTIAL / NOT PASS;
- condition 4 = NOT READY;
- overall = `NOT_READY_GATE_C_EXT_META`.

No V2.4 predictions.
No benchmark scoring.
No custom holdout opening.
No new-human recruitment.
No Arabic work.

Exact next checkpoint:
`H1 RAW ARTIFACT + SCHEMA + TERMS FREEZE`


---

# 35. H1 RAW ARTIFACT + SCHEMA + TERMS FREEZE V1 — PARTIAL PASS

Date: 2026-10-04

Freeze file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_RAW_ARTIFACT_SCHEMA_TERMS_FREEZE_V1.md`

Commit:
`a4e4d01a6f3b0ff2dba6360327c523e587e1c282`

Readiness update:
`3cb83a562fe96705c0c7b84de3a07e5089f26d31`

Quality delta:
`IMPROVED / TOOLING-MATERIALIZATION BLOCKED`

Frozen artifact identity:
- Zenodo DOI `10.5281/zenodo.18637045`
- version `v2`
- `manual-judgments-task1-2024.zip`
- publisher MD5 `589ad66e0b9324592f0151cc67974015`
- size 7.1 MB

Frozen source/test route:
`https://trec.nist.gov/data/plaba/PLABA_2024-Task_2.zip`

2023 physical schema directly verified:
`Source, Output, Answer, Simp. sent, Simp. term, Simp. term acc., Simp. fluency, Acc. comp., Acc. faith., Team, Sent, Abst`

Observed source/abstract identifiers include:
`Q1_A4`, `Q2_A6`

2024 logical schema frozen from peer-reviewed retrospective:
- ACC accuracy relative to source;
- COM completeness / minimize information loss;
- SIM simplicity;
- BRV brevity;
- FIN mean score.

Current conceptual H1 mapping:
- H1-S <- ACC
- H1-C <- COM

No binary PASS/REJECT threshold has been frozen.

Usage/terms:
- TREC research-use framework permits research/NLP/document-understanding use and scientific reporting subject to restrictions;
- raw protected text must not be redistributed in the ACAD_PASS repo;
- store only IDs/hashes/protocol metadata/derived metrics publicly;
- Zenodo record is Open but explicit license value is not shown, so unrestricted redistribution is NOT assumed.

Independence rule:
`original biomedical abstract / PMID = source cluster`

The 400 test abstracts are the maximum candidate H1 source-cluster pool.

Still unresolved:
- local ZIP bytes;
- local SHA-256;
- exact 2024 TSV physical headers;
- exact PMID manifest;
- explicit Zenodo license;
- final H1 adapter and metric thresholds.

Current readiness:
- condition 1 PASS;
- conditions 2 and 3 substantial partial / not pass;
- condition 4 NOT READY;
- overall `NOT_READY_GATE_C_EXT_META`.

Exact next checkpoint:
`H1 PHYSICAL SCHEMA + SOURCE-CLUSTER FREEZE`

Preferred files if manual upload is required:
1. `manual-judgments-task1-2024.zip`
2. `PLABA_2024-Task_2.zip`

No V2.4 prediction.
No benchmark scoring.
No custom holdout opening.
No human recruitment.
No Arabic work.


---

# 36. H1 PHYSICAL SCHEMA + SOURCE-CLUSTER FREEZE V1 — COMPLETE

Date: 2026-10-04

Freeze file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_PHYSICAL_SCHEMA_SOURCE_CLUSTER_FREEZE_V1.md`

Commit:
`1cb73aa79658462d105be0de02f2e2acb6f16023`

Readiness update:
`4ed5de1969a889e88c0e8f25ca30305017c3ae7c`

Quality delta:
`IMPROVED`

User supplied the exact two public ZIPs.

Manual-judgment archive:
- size `7,054,073` bytes
- MD5 `589ad66e0b9324592f0151cc67974015`
- publisher MD5 match = YES
- SHA-256:
  `8256f7342c180e881e9c11244a7c24fe3e2fb4bdabf0fdfeb04892e4c8c722ce`

Source/test archive:
- size `231,126` bytes
- MD5 `daa454a5234161489fef52eab1ebec26`
- SHA-256:
  `f9416ee9ef5a051e79053b526ad7023237cb87d171e79d9623bda4dbd656991e`

Inner source file:
`test.json`
SHA-256:
`2d53f485082ea16571ac54d9f3bcbd56c1c199130d4b8542e93b678ed561e9a7`

Exact physical 2024 judgment schema:
- Abstract
- Sentence
- Source
- Target
- Accuracy
- Completeness
- Simplicity
- Brevity

Source corpus:
- 40 questions
- 400 abstract slots
- 4,060 source sentences
- 399 unique PMIDs

Duplicate PMID:
`15857353`

Slots:
- Q14_A3
- Q37_A5

Their 7-sentence sources are exactly identical.

Permanent independence rule:
`PMID = primary H1 source cluster`

Maximum independent source clusters:
`399`

Judgment archive:
- 19 runs
- 76,790 retained rows
- 14/19 full 4,060-row runs
- 5/19 incomplete runs
- 350 missing run×sentence rows
- 315 unique source-sentence pairs missing in >=1 run
- 0 extra source pairs
- 0 empty targets

All retained judgment rows:
- match a valid Abstract+Sentence source ID;
- match source text exactly against test.json.

Score alphabet:
`-1, 0, 1`

Gold descriptive counts:
Accuracy:
- -1: 2,084
- 0: 10,296
- 1: 64,410

Completeness:
- -1: 3,151
- 0: 16,992
- 1: 56,647

These are external gold properties, not ACAD_PASS results.

Current readiness:
- Condition 1 PASS
- Condition 2 substantial partial / not pass because rights documentation remains
- Condition 3 substantial partial / not pass because final eligible subset/metric contract remains
- Condition 5 H1-internal clustering frozen; cross-dataset overlap remains
- Conditions 4 and 6 NOT READY
- overall `NOT_READY_GATE_C_EXT_META`

No V2.4 prediction.
No external scoring.
No custom Gate C opening.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`H1 ADAPTER + NATIVE METRIC CONTRACT FREEZE`


---

# 37. H1 ADAPTER + NATIVE METRIC CONTRACT V2 — FROZEN FOR INDEPENDENT REVIEW

Date: 2026-10-04

Preferred contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_ADAPTER_NATIVE_METRIC_CONTRACT_V2.md`

Commit:
`23a613da183157c14ef5c1c82051a5014dbca18e`

Higher-model review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTRACT_V2_HIGHER_MODEL_REVIEW_PACKET.txt`

Packet commit:
`0f583d601f8d195797e597308887465864dd3c94`

Readiness update:
`5cc7f8c3339d4db3d67fdc51d1f19652c19f5e1b`

Quality delta:
`IMPROVED`

V2 strengthens V1:
1. confirmatory utility uses only 14 complete PLABA runs;
2. hard safety uses every observed extreme-negative gold row across all 19 runs;
3. exact Source==Target positive rows are excluded from primary transformed-positive acceptance and retained as identity controls.

Frozen gold strata:
- QUALIFIED_POSITIVE = ACC==1 AND COM==1
- QUALIFIED_NEGATIVE = ACC==-1 OR COM==-1
- other cells diagnostic only
- 0 is NOT mapped to REVIEW

All-run safety population:
- 4,275 qualified-negative rows
- 396 exposed PMID clusters
- any PASS_CANDIDATE is a hard safety failure

Confirmatory positive utility:
- 14 complete runs
- 33,660 non-identical qualified-positive rows
- 399 PMIDs
- PMID-macro PASS_CANDIDATE >=75%

Confirmatory negative utility:
- 14 complete runs
- 3,677 qualified-negative rows
- 394 PMIDs
- PMID-macro REJECT >=75%
- REVIEW is safe abstention but not decisive rejection
- INVALID is non-success

Statistics:
- PMID = independence unit
- 10,000 cluster bootstrap resamples
- seed 20261004
- 95% percentile interval
- exact one-sided zero-event upper bound for safety

Anti-degenerate behavior:
- PASS-all fails safety
- REJECT-all fails positive utility
- REVIEW-all fails positive utility and decisive-negative utility
- INVALID-all fails utility/integrity

No V2.4 external prediction.
No benchmark scoring.
No custom Gate C opening.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`USER-MEDIATED HIGHER-MODEL REVIEW OF H1 CONTRACT V2`


---

# 38. H1 ADAPTER + NATIVE METRIC CONTRACT V3 — FROZEN FOR INDEPENDENT REVIEW

Date: 2026-10-04

Preferred contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_ADAPTER_NATIVE_METRIC_CONTRACT_V3.md`

Commit:
`672bbc119eaa174e22365f5c4907bb47f9474a7d`

Higher-model review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTRACT_V3_HIGHER_MODEL_REVIEW_PACKET.txt`

Packet commit:
`78e5562cba86b99655acc5c54cec277e1196cbc4`

Readiness update:
`e20ea2544032fdc8c44eed6cc0c187d5ba2503fb`

Quality delta:
`IMPROVED`

Reason V2 was superseded before execution:
- it treated repeated row-level judgments as repeated prediction units;
- identical source/target pairs recur across runs;
- direct audit found human class conflict on repeated identical pairs;
- it restricted utility to complete runs, which is less principled than canonicalizing every pair with existing published gold;
- it excluded exact-copy positive pairs from primary gold rather than retaining them with explicit subgroup reporting.

No H1 prediction was ever run under V1 or V2.

Frozen V3 prediction unit:
`PMID + exact Source + exact Target`

Canonical-pair count:
`62,315`

Eligibility-manifest SHA-256:
`f0371da56290999d4786ce86ea319be15f994c8cc8075a8fddaaa81c12cf5dc9`

Canonical gold:
- SAFE_STRICT 40,609 / 399 PMIDs
- ERROR_STRICT 3,566 / 396 PMIDs
- INTERMEDIATE 16,800 / 399 PMIDs
- HUMAN_CONFLICT 1,340 / 320 PMIDs

Multi-rated sensitivity:
10,554 pairs:
- SAFE_STRICT 7,159
- ERROR_STRICT 455
- INTERMEDIATE 1,600
- HUMAN_CONFLICT 1,340

V3 preserves:
- 0 != REVIEW
- human disagreement != REVIEW
- INVALID remains in utility denominators
- PMID remains independence unit
- 10,000 PMID-cluster bootstrap, seed 20261004
- zero unsafe PASS non-compensatory
- no criticality claim from PLABA alone

Current status:
`H1 CONTRACT V3 FROZEN FOR INDEPENDENT REVIEW`

No V2.4 external prediction.
No scoring.
No adapter implementation.
No custom Gate C opening.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`USER-MEDIATED HIGHER-MODEL REVIEW OF H1 CONTRACT V3`


---

# 39. H1 CONTRACT V3 INDEPENDENT REVIEW — ACCEPTED WITH ESSENTIAL CHANGES

Date: 2026-10-04

Review decision:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTRACT_V3_INDEPENDENT_REVIEW_DECISION_V1.md`

Commit:
`5488022080f2d55265f1e12e168c5efef5e6c59f`

Readiness update:
`1742ba46bd82b9a006aa1d05c85d7bf15b0c0ad8`

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Implementation-agent verification agreed with the core blocker:
- PLABA Task 1 is sentence-aligned but the whole rewritten abstract is expected to be coherent;
- PLABA discussion explicitly says sentence-level evaluation accounts for context of the entire abstract;
- official guidelines permit resolving anaphora from previous sentences;
- official guidelines permit ignoring some non-consumer-relevant sentences;
- official guidelines permit omitting confidence intervals, p-values and similar measurements;
- official guidelines permit explanations/generalizations that may add contextual material.

Therefore:
`PLABA SAFE_STRICT != AUTOMATIC ACAD_PASS STRICT-PRESERVATION PASS GOLD`

without a compatibility contract.

V2.4 context audit:
- frozen extractor receives one text string;
- no independent context field exists;
- prepending context would make that context part of source obligations and can create false omissions against a current-sentence target.

Current state:
`H1_NOT_READY_CONTEXT_GOLD_ALIGNMENT`

Retained V3 strengths:
- canonical PMID+Source+Target deduplication;
- human conflict diagnostic only;
- score 0 is not REVIEW;
- PMID cluster statistics;
- public-gold procedural separation;
- no new-human requirement now.

Required correction:
- Source==Target positives must be excluded from primary transformed-positive acceptance and reported as identity controls;
- final eligible denominators must be recalculated after context/gold compatibility is frozen.

Quality delta:
`MIXED / METHODOLOGICALLY IMPROVED`

Improved:
- detected a genuine construct mismatch before any prediction;
- prevented invalid H1 adapter implementation;
- preserved all negative protocol history.

Worsened/new blocker:
- PLABA alone is not yet proven compatible as a full hard H1 gate for frozen V2.4.

No V2.4 prediction.
No H1 scoring.
No runtime change.
No custom holdout opening.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`H1 CONTEXT + GOLD-SEMANTICS RESOLUTION`


---

# 40. H1 CONTEXT + GOLD-SEMANTICS RESOLUTION — DESIGN-LEVEL PASS

Date: 2026-10-04

Resolution file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_CONTEXT_GOLD_SEMANTICS_RESOLUTION_V1.md`

Commit:
`0db47c57fc012dd95cc7a147b27745e5d8356314`

Readiness update:
`7c948cc7704bbe27dbd95b11c19a0036921e45d8`

Quality delta:
`IMPROVED`

Primary-source PLABA resolution:
- sentence alignment does NOT imply context independence;
- whole rewritten abstract is expected to remain coherent;
- sentence-level evaluation accounts for broader abstract context;
- annotation guidelines permit context-dependent anaphora resolution;
- some sentences may be ignored for consumer relevance;
- confidence intervals, p-values and similar measurements may be omitted;
- explanatory additions/generalizations are permitted.

Therefore:
`PLABA SAFE_STRICT != ACAD_PASS STRICT-PRESERVATION PASS GOLD`

No hard PLABA subset will be created by post-hoc surface/semantic filtering.

Revised PLABA role:
`H1 DIAGNOSTIC / AUTHENTIC TRANSFORMATION UTILITY`

Minimum stronger hard-H1 companion selected:
`FactPICO`

FactPICO:
- ACL 2024 DOI `10.18653/v1/2024.acl-long.459`;
- 115 RCT abstracts;
- 345 whole plain-language summaries;
- expert fine-grained evaluation of PICO elements;
- PICO ratings explicitly distinguish accurate / vague-inaccurate / severe inaccuracies or missing critical descriptors / missing;
- evidence-inference ratings assess whether critical findings are accurately represented or omitted;
- added-information spans and correctness are annotated;
- whole abstract -> whole summary context is compatible in principle with the frozen V2.4 single-source/single-candidate interface.

FactPICO therefore covers:
- H1-S via critical factuality/support and added-information correctness;
- H1-C via missing PICO elements, missing critical descriptors, and omitted evidence inference.

Claim remains narrow:
`critical RCT-element fidelity/preservation`
not exhaustive document preservation.

Official repository:
`lilywchen/FactPICO`

Observed main HEAD:
`2e16993a000aedb15cb348b7bcd61070d26bab14`

Repository license:
`MIT`

Data files are hosted separately through UT Austin Box.
Their exact bytes and separate reuse/license terms are not yet frozen.

InfoLossQA:
`DIAGNOSTIC ONLY`
for information-loss characterization; not hard-gated because its QA representation is not an exact V2.4 outcome oracle without semantic adapter work.

No V2.4 prediction.
No H1 scoring.
No runtime change.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`FACTPICO ARTIFACT + SCHEMA + LICENSE FREEZE`


---

# 41. FACTPICO ARTIFACT + SCHEMA + LICENSE AUDIT — PARTIAL FREEZE

Date: 2026-10-04

Audit:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_ARTIFACT_SCHEMA_LICENSE_AUDIT_V1.md`

Commit:
`4c55af156df1e0f67fd8ebe4f3a06f70b5c6a813`

Readiness update:
`b842e27001e26870ed7e9125c821692d50203f48`

Quality delta:
`IMPROVED / RAW-ARTIFACT BLOCKED`

Verified from primary sources:
- FactPICO ACL 2024 DOI `10.18653/v1/2024.acl-long.459`;
- 115 RCT abstracts;
- 345 plain-language summaries from GPT-4, Llama-2-Chat, Alpaca;
- expert PICO rating semantics:
  4 accurate,
  3 vague/slightly inaccurate,
  2 severe inaccuracies and/or missing critical descriptors,
  1 missing;
- Evidence Inference ratings:
  accurate / vague-slightly inaccurate / inaccurate / not mentioned;
- Added Information spans + factuality + rationale;
- separate exhaustive-outcome annotation exists;
- annotations released under CC BY 4.0;
- source articles from PubMed Open Access subset with reuse-compatible terms;
- repository code license MIT;
- official repo HEAD observed:
  `2e16993a000aedb15cb348b7bcd61070d26bab14`.

Official data route:
`https://utexas.box.com/s/mpe5idxrqrzs1wcakphng7xfi7h4g83j`

Current environment cannot access/materialize the Box payload.

Therefore NOT yet frozen:
- exact data filenames;
- raw bytes;
- local SHA-256;
- exact physical columns;
- PMID/source-ID manifest;
- annotator/provenance fields in the released artifact;
- exact duplicate/missing conventions.

Current FactPICO readiness:
`PARTIAL / NOT EXECUTION-READY`

Exact next checkpoint:
`FACTPICO PHYSICAL ARTIFACT + SCHEMA FREEZE`

Preferred user action:
download the complete Box shared folder/archive and upload it here unchanged.

No V2.4 prediction.
No H1 scoring.
No runtime change.
No human recruitment.
No Arabic work.


---

# 42. FACTPICO PHYSICAL ARTIFACT + SCHEMA FREEZE — COMPLETE

Date: 2026-10-04

Freeze file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_PHYSICAL_ARTIFACT_SCHEMA_FREEZE_V1.md`

Commit:
`117cd7c4b414aa77dab22db22423d2ce6bb319e1`

Readiness update:
`58bb72ed2e9da9b11c7aec771d3a55f1d03c4bba`

Quality delta:
`IMPROVED`

User supplied:
`FactPICO.zip`

Raw archive:
- size 2,232,398 bytes
- MD5 `7f14a2b793f0ee5bb03aadb0131768db`
- SHA-256 `ec260d7c69db9537f819fbdf728c997520e55de56b9f03b2980b017c91b9d4f4`
- ZIP integrity PASS

Primary numeric gold:
`data/all_evaluations.csv`

SHA-256:
`1035640d11dbe5fd28ad13385785638fca3c2f0632ba5e94480ed319b90992cd`

Reconciled:
- 115 RCT source abstracts
- 345 unique summaries
- 115 outputs/model for GPT-4, LLAMA-2, ALPACA
- exactly 3 summaries/source
- no duplicate Abstract+generation records

Primary expert fields:
- Population
- Intervention
- Comparator
- Outcome
- Results

Important physical semantics:
- 0 in relevant PICO fields = N/A encoding
- half-step PICO values occur in doubly annotated source group and are aggregate values, not native categorical labels
- Results is summary-level aggregate over 1–5 evidence inference spans
- Avg. PICO-R includes derived aggregation and is not hard gold
- holistic score has no hard role yet

Source-cluster ID:
`SHA256(exact Abstract)`

Unique source clusters:
`115`

Derived source-cluster manifest SHA-256:
`a5b26ad1bac4a80e6b158c251557383835e7c43772e25b084d4a4a2bf49fc831`

Derived record/gold manifest:
345 records

SHA-256:
`693f15c7eaaa6a4687cff04444a4096a076e71600bf240adcf1e5defafe534a5`

Rationale-layer defects preserved:
- `rest_270_annotated_rationales.csv` actually contains 240 rows
- single-rationale sources = 80 abstracts / 240 summaries
- double-rationale sources = 25 abstracts / 75 summaries
- rationale source sets disjoint
- 105/115 abstracts have PICO rationale files
- 30/345 summaries therefore have numeric expert ratings but no released PICO rationale row
- 15 released PICO rationale candidate strings remain corrupted/mismatched against canonical generation text after conservative formatting normalization
- canonical source/candidate text MUST always come from all_evaluations.csv

Evidence-inference rationale layer:
- 645 rows
- all 345 summaries represented
- 1–5 result spans per summary

Contradictions:
`DIAGNOSTIC ONLY`

LLM rationale files:
`pico_rationales.csv` and `llm_pico_rationales.csv`
are byte-identical and diagnostic only.

Artifact completeness decision:
- primary numeric gold = PASS
- rationale completeness = PARTIAL / NON-BLOCKING
- physical schema = PASS
- source clustering = PASS
- hard-gold eligibility/mapping = NOT READY

No V2.4 prediction.
No H1 scoring.
No runtime change.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`FACTPICO HARD-GOLD ELIGIBILITY + H1 CONTRACT V4 FREEZE`


---

# 43. FACTPICO HARD-GOLD ELIGIBILITY + H1 CONTRACT V4 — FROZEN FOR FOCUSED REVIEW

Date: 2026-10-04

Contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_HARD_GOLD_CONTRACT_V4.md`

Commit:
`d0891669fe21949439ee3d57f1e3e0a4c3659c70`

Focused review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_V4_FOCUSED_REVIEW_PACKET.txt`

Packet commit:
`d737db5d927eea17caa6c6cdbcbccfea840d0915`

Readiness update:
`86b123008baf1b389de0e0a7bcae3fb575725453`

Quality delta:
`IMPROVED / REVIEW PENDING`

V4 prediction universe:
`345 records / 115 source clusters`

Hard source eligibility:
- 3 sources / 9 summaries containing N/A PICO are diagnostic-only in the proposal;
- hard pool = 112 sources / 336 summaries.

Proposed V4 classes:
- SAFE_STRICT_CONTROL = 34 records / 33 sources
- ERROR_STRICT = 172 records / 91 sources
- INTERMEDIATE = 130 records / 79 sources
- N_A_SOURCE_DIAGNOSTIC = 9 records / 3 sources

SAFE_STRICT_CONTROL proposal:
- all PICO fields = 4
- Results = 4
- no identified Added Information span
- no unresolved Added Information identity source
- non-N/A source

Important limitation:
SAFE_STRICT_CONTROL model distribution:
- ALPACA 33
- GPT-4 1
- LLAMA-2 0

Therefore this cannot support a broad authentic-transformation claim without explicit narrowing.

ERROR_STRICT proposal:
- non-double PICO: any applicable <=2
- double-annotated averaged PICO: any <=1.5
- OR Results <=2

Why <=1.5 for double-PICO:
released half-step averages hide raw rater pairs; <=1.5 guarantees both integer underlying ratings lie in the hard-error range {1,2}. A released 2.0 may be (2,2) or disagreement such as (1,3), so V4 leaves it non-hard pending review.

Added Information:
not hard-mapped because FactPICO may mark externally factual explanatory additions as acceptable while frozen V2.4 is source-bounded.

Provisional metadata-only eligibility manifest:
345 rows
SHA-256:
`72ece44c2d23b8c6ce667f5f1ff0856fb28900a412a0b14ed192ce329b8a9d91`

Proposed gates:
- any ERROR_STRICT PASS_CANDIDATE = H1 safety FAIL
- ERROR_STRICT REJECT >=75% pair-micro AND source-macro
- SAFE_STRICT_CONTROL PASS >=75% pair-micro AND source-macro

Safety source clusters:
91
If zero unsafe source-cluster events:
simple one-sided 95% upper bound ≈ 3.2384%.
Benchmark-specific only.

Focused higher-model review is justified because these are construct/statistical decisions, not implementation tasks.

No V2.4 prediction.
No H1 scoring.
No adapter implementation.
No runtime change.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`USER-MEDIATED FOCUSED INDEPENDENT REVIEW OF FACTPICO H1 CONTRACT V4`
