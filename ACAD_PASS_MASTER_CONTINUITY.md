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
`FINAL EXECUTION AUTHORIZATION REVIEW`

Higher-model verdict:
`B. READY_WITH_FINAL_EXECUTION_CONTROL_CHANGE`

Both remaining gaps are now closed:
- true priority-conflict fixture;
- durable GitHub attempt ledger.

Final regression:
- run `37312305371`
- head `659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`
- artifact `11345959688`
- artifact ZIP SHA-256 `f3510bd4cacdb40a70d6b37d6d9f6fac24a9d77285462723f1e0738eb374a701`

Durable real claim:
`ABSENT / UNCONSUMED`

Synthetic durable claim:
`PRESENT / RETAINED AS EVIDENCE`

Current implementation verdict:
`READY_FOR_FINAL_EXECUTION_AUTHORIZATION_REVIEW`

Quality delta:
`IMPROVED`

FactPICO:
`NOT_RUN`

Still not authorized until independent final authorization:
- FactPICO prediction;
- scoring;
- gold join;
- rerun/adaptive retry;
- runtime/matcher modification;
- threshold/gold changes;
- custom Gate C;
- Arabic work.

Exact next action:
send the narrowly scoped final authorization prompt based on
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_5_FINAL_EXECUTION_AUTHORIZATION_REVIEW_PACKET.txt`

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


---

# 44. FACTPICO H1 CONTRACT V5 — FROZEN AFTER FOCUSED INDEPENDENT REVIEW

Date: 2026-10-04

V4 focused review decision:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_V4_FOCUSED_REVIEW_DECISION_V1.md`

Commit:
`d6804d096b648e259f3cd37b943f1a522d0e03c9`

Final V5 contract:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/H1_FACTPICO_HARD_GOLD_CONTRACT_V5.md`

Commit:
`26235ace57b68b1e93f78728c885d33c1806c24e`

Manifest metadata:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_HARD_GOLD_ELIGIBILITY_MANIFEST_V5_METADATA.md`

Commit:
`5852485cda8f4b75df5f573391b5dd3cff34da81`

Readiness update:
`7576fb11ee1fff86b0591f9571139b3f4386234a`

Quality delta:
`IMPROVED`

Independent verdict:
`B. ACCEPT_WITH_ESSENTIAL_CHANGES`

Final incorporated review changes:
1. all 3 N/A source clusters remain outside hard H1;
2. double-PICO hard-error cutoff <=1.5 retained;
3. Results<=2 REMOVED as independent hard-error trigger because released Results is an aggregate and raw per-finding human numeric ratings are not available;
4. Results=4 retained only for strict positive controls;
5. Added Information absence is accepted for safe-control only under complete annotation-framework + exact identity + no-span + no unresolved-source safeguards;
6. limited positive safe-control remains mandatory anti-degeneracy gate despite model skew;
7. >=75% pair-micro AND source-macro retained for positive and negative utility.

Primary-source FactPICO validation:
- all generated summaries were evaluated for PICO and Added Information;
- annotators highlighted addition spans;
- all 75 double-annotated texts received Added Information evaluation independently;
- Added Information is stored/released as span events.

Final V5 classes:
- SAFE_STRICT_CONTROL = 34 records / 33 sources
- ERROR_STRICT = 149 records / 83 sources
- INTERMEDIATE = 153 records / 84 sources represented
- N_A_SOURCE_DIAGNOSTIC = 9 records / 3 sources

Model distribution of SAFE_STRICT_CONTROL:
- ALPACA 33
- GPT-4 1
- LLAMA-2 0

Therefore positive-gate claim remains:
`LIMITED SOURCE-BOUNDED SAFE-CONTROL USABILITY`
not broad transformation acceptance.

Model distribution of ERROR_STRICT:
- ALPACA 35
- GPT-4 45
- LLAMA-2 69

Final V5 eligibility-manifest SHA-256:
`d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`

Superseded V4 proposal manifest SHA-256:
`72ece44c2d23b8c6ce667f5f1ff0856fb28900a412a0b14ed192ce329b8a9d91`

Safety rule:
`149 ERROR_STRICT -> PASS_CANDIDATE must be 0`

Eligible safety source clusters:
`83`

If zero unsafe source events:
one-sided exact 95% simple binomial upper bound ≈
`3.54496%`

Negative utility:
- pair-micro REJECT >=75%
- source-macro REJECT >=75%

Limited positive utility:
- pair-micro PASS >=75%
- source-macro PASS >=75%

No V2.4 prediction.
No H1 scoring.
No adapter implementation yet.
No runtime change.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`FACTPICO H1 ADAPTER + INPUT/GOLD MANIFEST IMPLEMENTATION FREEZE`


---

# 45. SCIENTIFIC VERIFICATION LANDSCAPE RESET + FACTPICO ADAPTER FREEZE

Date: 2026-10-04

Landscape reset:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/SCIENTIFIC_VERIFICATION_LANDSCAPE_RESET_V1.md`

Commit:
`f723cb718dc7451c2b484df43cb13a34e3603348`

Core diagnosis:
`RESOURCE SCARCITY = FALSE`

Actual issue:
`CONSTRUCT MATCHING + EVALUATION INTEGRITY`

Fresh research found strong modern resources across separate constructs:
- scientific revision/evaluation: ACL 2025 revision metrics, ParaRev, XtraGPT, Mr Dre
- long scientific factuality: LongSciVerify, FENICE, ACL 2026 factuality stress testing, LLM-Oasis
- claim/evidence: SciVer, CLAIM-BENCH, SciClaimEval, SciTab extensions, ClimateViz, Matter-of-Fact
- citation verification: SciCiteVal, CiteAudit, SciTrue
- biomedical quality: FactPICO, RoBBR, BioPulse-QA, ReFACT
- products/systems: Scite, Elicit, Paperpal, SciSpace, IPPOLIS Write

Strategy correction:
`REUSE MORE / FORCE LESS`

ACAD_PASS should use strongest matched evidence per construct rather than one benchmark per whole pipeline.

Current FactPICO role remains valid:
`H1 source-bounded critical RCT-element fidelity/preservation`

PLABA:
diagnostic/authentic transformation evidence.

Future H2/H3 resource selections are reopened before execution and must compare modern candidates against the older frozen candidates.

FactPICO adapter implementation freeze:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_H1_ADAPTER_IMPLEMENTATION_FREEZE_V1.md`

Commit:
`ee41d5908c5f703aa6738c4a6a3078e69f0e0f25`

Adapter:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/factpico_h1_adapter_v5.py`

Commit:
`c36aef499fe28c83b80f1d7a9f296deefa309d2d`

SHA-256:
`ab128309261eeffdb734464f2a2fef52cef4ce37bdb3b9654317d6b5bba0b7e1`

Build manifest:
`FACTPICO_H1_V5_BUILD_MANIFEST.json`

Commit:
`8450003be24db1b101cb7a8be663431a934dbd76`

Frozen artifacts:
- prediction input: 345 records
  SHA-256 `ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`
- separate gold: 345 records
  SHA-256 `6b0028e0180609d04c9f9b9dd62304fbcfd23f0606f4651a662a18a196a83e48`
- eligibility manifest:
  SHA-256 `d7c4999734f76179a576df4f35f87b981d694dd40615a0ede28ca7d4c61ab255`
- build manifest:
  SHA-256 `67bfbd4302f66d2248009c8a6fe9cef658a6f202d278450b73e942c68cb6f16b`

No-gold-leak:
`PASS`

Deterministic rebuild:
`PASS — two sequential independent builds, identical hashes`

Prediction keys only:
- record_id
- source_text
- candidate_text

Prediction/gold record-ID exact match:
`PASS`

Tooling negative evidence:
Python startup emitted an unrelated artifact_tool spreadsheet runtime warmup error, but adapter completed with return code 0; second sequential build reproduced all hashes.
Classified tooling/environment only.

Current H1 performance:
`NOT YET MEASURED`

No V2.4 external prediction.
No H1 scoring.
No runtime change.
No human recruitment.
No Arabic work.

Exact next checkpoint:
`H1 FACTPICO PRE-PREDICTION INTEGRITY GATE`


---

# 46. STRATEGIC LANDSCAPE REVIEW INCORPORATED + FACTPICO PRE-PREDICTION BLOCKER

Date: 2026-10-05

Higher-model review:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/STRATEGIC_LANDSCAPE_HIGHER_MODEL_REVIEW_DECISION_V1.md`

Commit:
`a1a9975797a6e3879ed8174c82e4ffbacd4dea7e`

Review verdict:
`B. PROCEED WITH MAJOR STRATEGIC MODIFICATIONS`

User-supplied review emphasized:
- candidate support != required-information preservation;
- component passes != end-to-end revision safety;
- expert labels are construct-specific;
- architecture claims require execution/generalization evidence;
- novelty cannot rest on component aggregation alone.

Permanent strategic correction:
`CONSTRUCT-MODULAR EXTERNAL VALIDATION`

H1 is now interpreted as:
- H1-A candidate support/factuality;
- H1-B required-information preservation;
- H1-C revision usefulness.

FactPICO covers bounded critical-RCT parts of H1-A/H1-B only.

Future primary complements:
- InfoLossQA for omission/information loss;
- ParaReval/ParaRev for revision usefulness;
- SciFact/SciVer for claim support;
- QASemConsistency + NLI4CT for relation/numeric/comparison reasoning.

Capability map:
`ACAD_PASS_CAPABILITY_CLAIM_MAP_V1.md`

Commit:
`bba139f93af7b5b0be95ce6de1dde593cf77ffc6`

Added Information completeness decision:
`FACTPICO_ADDED_INFORMATION_COMPLETENESS_DECISION_V1.md`

Commit:
`99372a2e67594f17eaf67ddf5b2a00a84ea9c189`

Decision:
`PASS_WITH_NARROW_CLAIM`

Meaning:
absence of an exact span-event row may support only:
`NO_HIGHLIGHTED_ADDED_INFORMATION_SPAN_IN_THE_RELEASE`
under exact identity and unresolved-source exclusions.

Readiness supersession:
`PRE_GATE_C_READINESS_SUPERSESSION_INDEX_V1.md`

Commit:
`8ef29c7c00d46ade02f6b1c358bba9a58d879532`

FactPICO pre-prediction integrity gate:
`FACTPICO_H1_PRE_PREDICTION_INTEGRITY_GATE_V1.md`

Commit:
`160a823c4712815c364a30b9bcce42c4c9d03d93`

Readiness update:
`e4e2feb4d82cf10a0e584a66d93d7e9eaa9c962a`

Pre-prediction checks passed:
- claim boundary
- Added Information interpretation
- readiness authority
- FactPICO hashes
- adapter determinism
- no gold leakage
- prediction/gold IDs
- frozen runtime unchanged

Git compare from canonical freeze trigger
`c0193aa3f578cc32b454a031ead73ff7e56c8918`
to gate-time HEAD showed:
`0 frozen runtime component changes`.

New blocker found by implementation audit:
`FACTORIAL ALIGNER SCALABILITY`

Frozen B1.1 code enumerates permutations for assertion matching.

Complexity examples:
- 10 assertions: 3,628,800 permutations
- 12 assertions: 479,001,600
- 15 assertions: 1,307,674,368,000

Development B2 used a deliberately small mechanics set; full-document scalability was never measured.

Therefore:
`NOT_READY_FOR_FACTPICO_PREDICTION`

This is an execution-validity blocker, not a FactPICO scientific result.

Quality delta:
`IMPROVED SIGNIFICANTLY / NEW REAL BLOCKER FOUND BEFORE ONE-SHOT`

No FactPICO prediction.
No H1 scoring.
No frozen runtime modification.
No Arabic work.

Exact next checkpoint:
`V2.4 SYNTHETIC SCALABILITY PREFLIGHT + EXECUTION-POLICY DECISION`


---

# 47. FULL LANDSCAPE RECONCILIATION + V2.4 SYNTHETIC SCALABILITY PREFLIGHT

Date: 2026-10-05

User supplied:
- `ACAD_PASS_LANDSCAPE_STRATEGIC_REVIEW_2026-10-04.md`
- `ACAD_PASS_REVIEWER_HANDOFF.md`

Conclusion:
`NO ADDITIONAL FILE REQUIRED FOR CURRENT CHECKPOINT`

Original historical reviewer attachments may be requested later only if a specific unresolved historical claim requires exact provenance.

Full-report reconciliation:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FULL_STRATEGIC_LANDSCAPE_RECONCILIATION_V1.md`

Commit:
`b724f618eb8067e44edd7ac3ae823b52f292ae01`

Important newly incorporated roadmap details:
- validation hierarchy:
  artifact/conformance -> construct-level capability -> complete editing transaction;
- later task contract PRESERVE/SIMPLIFY/CORRECT;
- original native document authority;
- read-only context separated from obligations;
- independent coverage ledger;
- dependency-aware bounded repair;
- scoped delivery certificate;
- integration candidates Docling, GROBID, academic-refchecker, MiniCheck-family, W3C PROV/Web Annotation;
- baseline/benchmark candidates InfoLossQA, FaReBio, ParaReval, XtraGPT, MrDre, EditPropBench, SciFact, SciVer, QASemConsistency, NLI4CT, SciCiteVal;
- code/license/scorer caveats preserved.

Explicit later failure-mode ledger expanded with:
- shared extraction blindness
- benchmark packaging leakage
- multiplicity collapse
- context laundering
- evidence cherry-picking
- stale verification
- compensatory repair
- hidden document layers
- scientific-state confusion
- authoritative-source drift

No current FactPICO V5 rule changed.

Synthetic scalability preflight:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_4_SYNTHETIC_SCALABILITY_PREFLIGHT_V1.md`

Commit:
`03609245bab8d22e4c164708fd8ed2d9ded36803`

Method:
reproduced exact frozen best_one_to_one helper logic on synthetic assertion dictionaries only.

Measured:
- n3 0.00140s
- n4 0.00410s
- n5 0.02483s
- n6 0.17669s
- n7 1.41590s
- n8 12.94802s

Measured n8 throughput:
~3114 permutations/sec.

Optimistic n8-rate extrapolation:
- n9 ~1.94m
- n10 ~19.42m
- n11 ~3.56h
- n12 ~42.73h
- n13 ~23.14d
- n14 ~324.02d
- n15 ~13.31y

Measured throughput decreases with n, so these are optimistic.

Mathematical diagnosis:
frozen global objective is additive over source/candidate pair assignments with lexicographic priorities:
1. hard-owner mismatches
2. owner similarity
3. semantic similarity

Therefore factorial permutation enumeration is an implementation choice, not an intrinsic requirement of the matching problem.

But replacing it changes frozen executable identity.

Preflight verdict:
`FAIL_SCALABILITY`

FactPICO exposure:
`NONE`

No FactPICO assertion counts measured.
No FactPICO source/candidate passed through V2.4.

Focused independent review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_4_SCALABILITY_HIGHER_MODEL_REVIEW_PACKET.txt`

Commit:
`481c45c8a77f2446f9f2759c46c620c55054c1f2`

Readiness update:
`aa43910aa5d97528521cce253397404dcab827fe`

Implementation-agent recommendation:
`PREFER VERSION-BUMP SCALABLE MATCHER, SUBJECT TO INDEPENDENT REVIEW`

Reason:
a known execution defect should not be allowed to dominate a prospective external scientific measurement if it can be resolved cleanly before exposure.

No FactPICO prediction.
No scoring.
No frozen-runtime modification.
No Arabic work.

Exact next checkpoint:
`FOCUSED HIGHER-MODEL DECISION ON V2.4 SCALABILITY BLOCKER`


---

# 48. AT0-EN V2.5 SCALABLE MATCHER — REGRESSION + RUNTIME FREEZE COMPLETE

Date: 2026-10-05

Higher-model decision:
`B. VERSION_BUMP_BEFORE_FACTPICO`

Decision evidence:
user-supplied focused review and reviewer handoff revision 7.

V2.4 status:
`NOT_RUN — PRE-PREDICTION SCALABILITY BLOCKER`

No FactPICO semantic score exists for V2.4.

V2.5 specification:
`phase2/academic_transform/at0_en/v2_5/AT0_EN_V2_5_EXACT_SCALABLE_MATCHER_SPEC_V1.md`

V2.5 runtime freeze:
`phase2/academic_transform/at0_en/v2_5/AT0_EN_V2_5_RUNTIME_FREEZE_V1.md`

Freeze commit:
`d8282a13d9ba215117f1dd52c80088ccdb972a15`

FactPICO execution identity amendment:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V5_EXECUTION_IDENTITY_AMENDMENT_V1.md`

Commit:
`2301367d918501dbbe875ebf8bf9c4eb0e6e35ec`

GitHub Actions run:
`37279532576`

Workflow head:
`05e200461c1067c120e73acf4a6055383eb350b2`

Run:
`SUCCESS`

Artifact:
`11331840770`

Artifact ZIP digest:
`sha256:ec012324b265b5e6be5e1aff5f5dd670547692fc9f8bb6a3f58c993ccbb2cba1`

Frozen hashes:
- spec `8fe6203b266f86e2e147cf65b4e55d15b8dc25b344b466ac5d0f75ca461f888f`
- aligner `ac36409cd32c9a759a3e962ee6a86aa30d0a52299f2a19ccc8206d7b54e248ea`
- runner `ad2e996f0e76e8d6b80285d7059b072c53914f32d9d48fbf9af8f8076282b807`
- regression test `6633db047be337df27d1fad61eb8b33a473a6d69c60b73e35ec2611b1552a47a`
- report `2b0861f904448663b1eaff675ed79034bdccdb4c6ccee3ba08e7986fa5eb4b20`

Algorithm:
`HUNGARIAN_EXACT_INTEGER_LEXICOGRAPHIC_V1`

Numeric policy:
`EXACT_RATIONAL_FORMULA_V1`

Regression:
- B1 12 canonical pairs, exact differences 0
- B2 all GG/GE/EG/EE, exact differences 0
- GG 12/12
- GE 11/12, safe 4/5, unsafe PASS 0
- EG 11/12, safe 4/5, unsafe PASS 0
- EE 12/12, safe 5/5, unsafe PASS 0/6, REVIEW 1/1
- 205 synthetic brute-force equivalence cases, 0 differences
- downstream tie-sensitive case PASS
- grouping boundaries preserve legacy behavior

Scalability:
- n9 ~0.032 s
- n10 ~0.039 s
- n12 ~0.056 s
- n16 ~0.099 s
- n32 ~0.395 s
- n64 ~1.58 s
- n128 ~6.31–6.73 s
- n128 peak ~5.35 MB

Guardrails:
- timeout PASS
- crash PASS
- valid child PASS
- empty input PASS
- out-of-envelope PASS
- retries 0

Operational envelope:
- max assertions/side 128
- 60 s/record
- strictly sequential
- no retries
- timeout/crash/out-of-envelope -> INVALID_VERIFICATION

Numeric qualification:
exact-rational V2.5 is not claimed universally bitwise identical to legacy floating V2.4.
No differences were observed in canonical development or the 205 oracle cases.

FactPICO:
`NOT USED / NOT PREDICTED / NOT SCORED`

FactPICO V5:
scientific contract and frozen input/gold/eligibility hashes unchanged.

Pre-prediction review packet:
`phase2/academic_transform/at0_en/v2_5/V2_5_PRE_PREDICTION_HIGHER_MODEL_REVIEW_PACKET.txt`

Commit:
`274d9bbd107779618a894445d83e1ec050d84973`

Readiness update:
`3b7c89c6593c57462cf4e2f8376c32313c15ab6b`

Quality delta:
`MAJOR IMPROVEMENT — SCALABILITY BLOCKER REMOVED WITHOUT OBSERVED REGRESSION`

Exact next checkpoint:
`V2.5 PRE-PREDICTION HIGHER-MODEL REVIEW`


---

# 48. V2.5 IMPLEMENTATION-AGENT PRE-REVIEW AUDIT

Date: 2026-10-05

Audit:
`phase2/academic_transform/at0_en/v2_5/V2_5_IMPLEMENTATION_AGENT_PRE_REVIEW_AUDIT_V1.md`

Commit:
`21ece496e825ada155a9d44f11c8146b07391425`

Verdict:
`PASS_FOR_HIGHER_MODEL_PRE_PREDICTION_REVIEW`

Quality delta:
`IMPROVED`

Verified:
- V2.5 runtime freeze PASS
- zero B1/B2 exact regression differences
- 205 synthetic exhaustive-equivalence cases
- tie/grouping/failure-path checks PASS
- scalable envelope to n=128 PASS
- 60s per-record guardrail
- max 128 assertions/side
- zero retries
- INVALID on timeout/crash/out-of-envelope
- FactPICO V5 hashes/eligibility/thresholds unchanged
- FactPICO NOT_RUN

No new risk identified by implementation-agent consistency audit.

Numeric caveat remains explicit:
exact-rational V2.5 is not universally claimed bitwise-identical to every possible V2.4 floating near-tie.

Current mandatory gate:
`V2.5 PRE-PREDICTION HIGHER-MODEL REVIEW`

No FactPICO prediction authorized.


---

# 49. V2.5 ESSENTIAL PRE-EXECUTION CLOSURE

Date: 2026-10-05

Higher-model pre-prediction verdict:
`B. READY_WITH_ESSENTIAL_PRE_EXECUTION_CHANGES`

Implementation closure:
`phase2/academic_transform/at0_en/v2_5/V2_5_ESSENTIAL_PRE_EXECUTION_CLOSURE_V1.md`

Runtime freeze:
`phase2/academic_transform/at0_en/v2_5/AT0_EN_V2_5_RUNTIME_FREEZE_V2.md`

Execution identity:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V5_EXECUTION_IDENTITY_AMENDMENT_V2.md`

Final run:
`37289569561`

Head:
`29e3abe5ccb708cb88d94ae00630eaa0fdc2b123`

Artifact:
`11335647986`

Artifact digest:
`61d82aa30de89e84aa5bc0433bdfa528259269c0b3630648df5c0d4c95573b63`

Key closure:
- exact objective checked on all 205 oracle cases
- no observed float-vs-exact selected-mapping discrepancy
- characterized priority/partial-tie/near-tie/full-tie PASS
- fresh-process reproducibility PASS
- mixed-batch failure accounting PASS
- output overwrite refusal PASS
- one-shot guard PASS
- max-shape/unequal near-envelope PASS
- no canonical B1/B2 regression

Preserved negative:
run `37289060156` failed new 128 full-tie <=10s synthetic criterion.
This revealed synthetic runtime variability, not semantic failure.
Criterion refrozen to 30s using synthetic-only evidence.
External record timeout remains 60s.

FactPICO exposure:
`NONE`

Net:
`IMPROVED / NO NEW SCIENTIFIC REGRESSION OBSERVED`

Current checkpoint:
`FINAL HIGHER-MODEL PRE-PREDICTION RE-REVIEW`


---

# 50. FINAL V2.5 EXECUTION-CONTROL CLOSURE

Date: 2026-10-05

Higher-model verdict:
`B. READY_WITH_FINAL_EXECUTION_CONTROL_CHANGE`

Remaining gaps:
1. priority-conflict fixture
2. durable attempt ledger

Both closed.

Priority fixture:
selected assignment now wins owner priorities while losing semantic score.
Matcher unchanged.

Final regression:
`37312305371`

Head:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

Artifact:
`11345959688`

Artifact SHA:
`f3510bd4cacdb40a70d6b37d6d9f6fac24a9d77285462723f1e0738eb374a701`

Durable ledger:
provider `GitHub repository contents`
branch `factpico-v25-one-shot-ledger`

Authorization:
`FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

Real canonical key:
`claims/real/FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001/ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82/ATTEMPT_CLAIM.json`

Synthetic durability test:
- creation commit `f687cedcb82c543d8d21552db79a2d25a93f7a4e`
- later blob `cf03473f29ab3ce3452d133302ccc27672c1278f`
- survived first launcher interruption
- fresh launcher refused restart
- PASS

Current tree:
real claim FALSE
synthetic evidence claim TRUE

FactPICO real attempt remains:
`UNCONSUMED`

Files:
- `V2_5_FINAL_EXECUTION_CONTROL_CLOSURE_V1.md`
- `FACTPICO_V5_EXECUTION_IDENTITY_AMENDMENT_V3.md`
- `V2_5_FINAL_EXECUTION_AUTHORIZATION_REVIEW_PACKET.txt`

Net:
`IMPROVED / NO NEW SCIENTIFIC REGRESSION OBSERVED`

Current stop:
`FINAL EXECUTION AUTHORIZATION REVIEW`


---

# 51. FINAL FACTPICO V2.5 EXECUTION AUTHORIZATION

Date: 2026-10-05

Independent higher-model verdict:
`A. AUTHORIZE_ONE_PROSPECTIVE_FACTPICO_PREDICTION_RUN`

Decision record:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/V2_5_FINAL_EXECUTION_AUTHORIZATION_DECISION_V1.md`

Decision-record commit:
`af6c877295684c2028fe5e72948723c2f31d899c`

Two-gap status:
- priority-conflict fixture: CLOSED
- durable attempt ledger: CLOSED
- concrete unresolved execution defect: NONE

Authorized maximum:
`ONE PROSPECTIVE AT0-EN V2.5 FACTPICO PREDICTION RUN + IMMUTABLE PREDICTION ARTIFACT FREEZE ONLY`

Immutable execution checkout:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

Authorization ID:
`FACTPICO-V5-V25-ONE-PROSPECTIVE-PREDICTION-001`

Frozen prediction-input SHA-256:
`ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`

Real attempt:
`UNCONSUMED`

FactPICO:
- prediction: NOT_RUN
- gold join: NOT_RUN
- scoring: NOT_RUN
- profiling: NOT_RUN

Mandatory order:
1. verify exact frozen input bytes/hash and 345 unique IDs/order;
2. verify canonical real durable claim absent;
3. atomically create/read back canonical remote claim;
4. invoke bound local guard exactly once;
5. strictly sequential, zero retries, 60 s/record, max128 assertions/side;
6. retain all INVALID outcomes;
7. freeze prediction SHA/artifact/evidence;
8. STOP before gold join.

Still forbidden:
scoring, gold join, rerun, adaptive retry, runtime/matcher changes, threshold/gold changes, pre-run FactPICO profiling, H1/H2/H3/H4 redesign, custom Gate C, Arabic work.

Quality delta:
`IMPROVED — FINAL EXECUTION AUTHORIZATION OBTAINED / NO NEW SCIENTIFIC REGRESSION`

Current exact checkpoint:
`AUTHORIZED ONE-SHOT EXECUTION PREFLIGHT`


---

# 52. AUTHORIZED FACTPICO PREFLIGHT COMPLETE + ADAPTER PROVENANCE RECONCILIATION

Date: 2026-10-05

Authorized preflight workflow:
`37317413838`

Head:
`fa1ffb4f37e44dec04d29061ba95c5091ee3a46a`

Artifact:
`11348064811`

Artifact digest:
`sha256:c3786ba8c6516d959e0f22f075e289868b9765b7aa72c49fe5607a547b4e69e4`

Immutable execution checkout verified:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

PASS:
- matcher SHA
- batch runner SHA
- one-shot guard SHA
- exact public FactPICO ZIP SHA
- 345-record prediction-input rebuild
- prediction-input SHA
- gold SHA
- eligibility SHA
- unique IDs/order/schema
- no real claim created
- no inference started

Provenance mismatch found:
historically documented adapter SHA
`ab128309...`
does not match the bytes actually committed in Git.

Actual committed adapter SHA:
`3b0698772630a17d6d05fdf7197f5faa79b22212332ae785b069318bda4cd5b0`

Git compare from adapter implementation commit `c36aef...` to execution checkout `659b61...` shows no adapter-file modification.

Therefore:
`HISTORICAL DOCUMENTED-HASH MISMATCH / NOT POST-FREEZE CODE MUTATION`

Reconciliation file:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_ADAPTER_COMMITTED_IDENTITY_RECONCILIATION_V1.md`

Commit:
`c22f027fb879a8092fa129f45c238d07f9a25ffd`

Scientific contract/runtime/thresholds/gold/population:
`UNCHANGED`

Real attempt:
`UNCONSUMED`

FactPICO prediction:
`NOT_RUN`

Exact next checkpoint:
`VERIFY REAL CLAIM ABSENT -> ATOMIC REMOTE CLAIM -> ONE AUTHORIZED PREDICTION RUN -> IMMUTABLE FREEZE -> STOP BEFORE GOLD JOIN`


---

# 53. FACTPICO V2.5 ONE PROSPECTIVE PREDICTION — COMPLETE AND FROZEN

Date: 2026-10-05

Final freeze record:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_ONE_PROSPECTIVE_PREDICTION_FREEZE_V1.md`

Freeze-record commit:
`cdabc233c77cad2dace15233ccbc179ee5fa2dac`

Authorized execution:
- run `37318062175`
- workflow head `066d606e311136c5020ba800c3872b054c11e6da`
- job `111789731999`
- conclusion `SUCCESS`

Immutable runtime checkout:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

Input:
- count `345`
- SHA-256 `ce7f796b13aacc2a4d3792cd3f037e77f340fb077398847c6402d9aba8776c82`
- unique IDs/order `PASS`

Durable real claim:
- state `CONSUMED_BEFORE_INFERENCE`
- creation commit `6387516d84e9ba1109d387dcc4bde715ce2ac16b`
- blob SHA `a1d7bb2df60e55db8f914550858c2accadad1390`
- read-back `PASS`

Prediction:
- state `PREDICTIONS_FROZEN`
- count `345`
- SHA-256 `925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b`
- retry count `0`

Frozen artifact:
- ID `11348646367`
- size `358556 bytes`
- digest `sha256:eb68ab179bc17af1105a63ae1ff2f3fc76a4449bffd74a40a76a775319743daa`
- independently downloaded ZIP SHA matches the GitHub artifact digest exactly
- private preservation copy stored in ACAD_PASS Library

Preserved preflight negative:
- run `37317221936` failed BEFORE CLAIM because historical adapter SHA metadata did not match committed bytes
- no inference and no claim occurred in that failed preflight
- provenance was reconciled before execution

Successful preflight:
- run `37317413838`
- artifact `11348064811`
- digest `sha256:c3786ba8c6516d959e0f22f075e289868b9765b7aa72c49fe5607a547b4e69e4`

Current FactPICO boundary:
- prediction `COMPLETE / FROZEN`
- real one-shot authorization `CONSUMED / NO RERUN`
- gold join `NOT_RUN`
- scoring `NOT_RUN`
- eligibility join `NOT_RUN`
- scientific H1 result `NOT YET MEASURED`

Quality delta:
`IMPROVED — AUTHORIZED ONE-SHOT EXECUTION COMPLETED WITH EXACT ID/ORDER AND IMMUTABLE ARTIFACT`

New irreversible state:
`ONE-SHOT AUTHORIZATION CONSUMED AS DESIGNED`

Exact current checkpoint:
`FACTPICO PREDICTION FROZEN / STOP BEFORE GOLD JOIN`

Do NOT:
- rerun prediction;
- join gold;
- score;
- inspect results adaptively;
- modify runtime/matcher;
- change thresholds/gold;
- open custom Gate C;
- resume Arabic work.

Gold join/scoring requires a separate explicit authorization checkpoint.


---

# 52. UI-RESILIENT EXECUTION AGREEMENT

Date: 2026-10-05

Persistent working rule added by explicit user request:

`MINIMIZE_UI_STALL_RISK`

Operational policy:
- strictly sequential tool execution only;
- minimize total tool calls where safely possible;
- combine related read-only checks into one bounded step;
- avoid unnecessary polling; poll only when a state transition must be verified;
- keep checkpoint messages short;
- never repeat completed scientific work merely because the UI displays:
  `Our systems are thinking a bit more about this request before responding.`
- treat that phrase as a UI/stream interruption, not scientific failure;
- resume from the last verified durable state;
- preserve all successful and negative evidence;
- never sacrifice one-shot integrity, scientific controls, hashes, or auditability merely to reduce tool calls.

Current scientific/execution state remains unchanged:
- final authorization: GRANTED
- real FactPICO attempt: UNCONSUMED
- prediction: NOT_RUN
- gold join: NOT_RUN
- scoring: NOT_RUN

Exact next checkpoint:
`VERIFY REAL CLAIM ABSENT -> CREATE REMOTE CLAIM -> ONE AUTHORIZED PREDICTION RUN -> IMMUTABLE FREEZE -> STOP BEFORE GOLD JOIN`


---

# 53. FACTPICO V2.5 ONE-SHOT PREDICTION COMPLETE / FROZEN

Date: 2026-10-05

Canonical execution freeze:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_PROSPECTIVE_PREDICTION_EXECUTION_FREEZE_V1.md`

Freeze commit:
`97e35b9d8375a67fb58861b4f87b611f31e5f499`

Successful one-shot run:
`37318062175`

Execution checkout:
`659b61b6e1784bb8159f2bb1d36b41c0fb3de7ee`

Remote real claim:
- commit: `6387516d84e9ba1109d387dcc4bde715ce2ac16b`
- blob: `a1d7bb2df60e55db8f914550858c2accadad1390`
- state: `CONSUMED_BEFORE_INFERENCE`

Prediction:
- count: `345`
- exact ID order: PASS
- SHA-256: `925c8a073f4304fe751af072c1d1b8fc64455104e8ed2f23a88c3fc3e6ad496b`
- retry count: `0`
- INVALID: `0`

Unscored runtime outcomes:
- PASS_CANDIDATE: 0
- REJECT: 37
- REVIEW: 308
- INVALID_VERIFICATION: 0

These counts are NOT gold-based performance metrics.

Frozen artifact:
- ID: `11348646367`
- digest: `eb68ab179bc17af1105a63ae1ff2f3fc76a4449bffd74a40a76a775319743daa`
- ZIP size: `358556` bytes

Stop boundary:
- gold join: NOT_RUN
- scoring: NOT_RUN
- rerun: FORBIDDEN
- adaptive changes: FORBIDDEN

Quality delta:
`IMPROVED — AUTHORIZED PROSPECTIVE PREDICTION COMPLETED AND IMMUTABLY FROZEN`

New risk/status:
- real one-shot authorization is permanently CONSUMED;
- therefore no replacement/rerun is allowed;
- no scientific performance interpretation is allowed before a separate gold/scoring authorization.

Current exact checkpoint:
`FACTPICO V2.5 POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`


---

# 54. POST-PREDICTION / PRE-GOLD REVIEW PACKET READY

Review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_POST_PREDICTION_PRE_GOLD_REVIEW_PACKET.txt`

Packet commit:
`5a72c16de204fc787fbd9fc6e6232033439779a1`

Purpose:
request exactly one independent decision:
- `A. AUTHORIZE_ONE_DETERMINISTIC_FACTPICO_GOLD_JOIN_AND_FROZEN_SCORING_RUN`
or
- `B. BLOCK_BEFORE_GOLD_JOIN`

Current stop remains:
- prediction frozen
- attempt consumed
- gold join NOT_RUN
- scoring NOT_RUN
- no rerun/adaptation permitted

Exact next checkpoint:
`INDEPENDENT POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`


---

# 55. FACTPICO V2.5 PROGRESS / MATURITY SCORECARD

Scorecard:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_STAGE_PROGRESS_SCORECARD_V1.md`

Scorecard commit:
`f056eb2391e57076f7b3159186d3fb9b78887196`

Engineering progress indicators (NOT benchmark metrics):
- authorized prediction-execution checkpoint: `100%`
- FactPICO V2.5 validation subphase: `70%`
- execution-integrity maturity: `96/100`
- scientific-validation completeness: `70/100`
- current FactPICO-stage quality satisfaction: `90/100`
- overall ACAD_PASS English-track maturity: `78/100`

Improvement since the previous major checkpoint:
- completion: approximately `+20 percentage points`
- execution-integrity maturity: approximately `+8 points`
- scientific-performance delta: `NOT YET COMPARABLE` until frozen gold scoring is authorized and executed.

Target for `EXCELLENT / REVIEW-READY` system maturity:
`>=90/100`

Main remaining gap:
external/gold-based validation evidence and frozen interpretation, not runtime stability.

Current exact checkpoint remains:
`INDEPENDENT POST-PREDICTION / PRE-GOLD AUTHORIZATION REVIEW`


---

# 56. FACTPICO V2.5 GOLD JOIN / SCORING COMPLETE AND FROZEN

Date: 2026-10-05

Canonical scoring freeze:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_GOLD_SCORING_EXECUTION_FREEZE_V1.md`

Freeze commit:
`7f5a717c549696d91eef2ace7f16a6d8e783ca4e`

Pre-gold code/config freeze run:
`37324968724`

Scorer SHA:
`00df8950ffb3d0ee48925c98ad976e1a940e68069a937396d4b28fdd5923d7fb`

Config SHA:
`bf2c47d0d2b7121c64168d62fc8f51669c22579f5827b6d3e4d0a4f20d304322`

Authorized scoring run:
`37325138336`

Scoring artifact:
- ID `11351451888`
- digest `105534207a4566c38d76174e9cd263244b87e37358b6007c76502bc250d67e77`

Exact join:
`345/345 PASS`

Hard safety:
`PASS`
- unsafe PASS records = 0
- unsafe PASS sources = 0
- one-sided exact 95% source upper bound = 3.5449568%

Negative utility:
`FAIL`
- pair-micro REJECT = 10.7383%
- CI = [5.7971%, 16.2338%]
- source-macro REJECT = 9.4378%
- CI = [4.8193%, 14.8594%]
- threshold = 75%

Positive anti-degeneracy:
`FAIL`
- pair-micro PASS = 0%
- source-macro PASS = 0%
- both CIs = [0%, 0%]
- threshold = 75%

Mechanical decision:
`H1_FULL_PASS_NOT_ACHIEVED`

No interpretation or repair has yet been authorized.

Progress scorecard V2:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_STAGE_PROGRESS_SCORECARD_V2.md`

Scorecard commit:
`37d1287ba7d61668a02ba2a0f52c26eb5829dd46`

Current engineering indicators:
- FactPICO V2.5 completion = 95%
- experimental-integrity maturity = 98/100
- scientific-validation completeness = 95/100
- process rigor satisfaction = 98/100
- benchmark-outcome satisfaction = 30/100
- overall English-track maturity = 74/100

Interpretation review packet:
`phase2/academic_transform/at0_en/v2_4/pre_gate_c/FACTPICO_V25_POST_SCORING_INTERPRETATION_REVIEW_PACKET.txt`

Packet commit:
`42af380148c790162572ba335a2a817a85d1565a`

Current exact checkpoint:
`FACTPICO V2.5 POST-SCORING INDEPENDENT INTERPRETATION / NEXT-DECISION REVIEW`

STOP:
- no prediction rerun
- no scoring rerun
- no threshold/gold/population changes
- no adaptive repair before independent interpretation


Rerun-prevention closure:
- one-shot scoring workflow removed after successful immutable freeze
- removal commit: `1fa410c417f4e718f7213fe431ad04534ae90940`
- purpose: prevent accidental second gold/scoring execution


---

# 57. FACTPICO FAILURE ANALYSIS + V2.6 REPAIR DESIGN FROZEN

Date: 2026-10-05

Independent interpretation verdict:
`A. AUTHORIZE_BOUNDED_FACTPICO_FAILURE_ANALYSIS_AND_REPAIR_DESIGN`

Taxonomy:
`FACTPICO_V25_FAILURE_ANALYSIS_TAXONOMY_V1.md`
commit `ecc458d9f46a51f5cc9f6e10b51b6d5caacc1ce7`

Failure analysis:
`FACTPICO_V25_FAILURE_ANALYSIS_REPORT_V1.md`
commit `3a96a19105f2c732c8ba62d2daef4a1957718b6d`

Repair design:
`AT0_EN_V26_DEV_REPAIR_DESIGN_V1.md`
commit `f7b329baa42225353e20895fc15f4a1ef8e50593`

Key frozen localization:
- 345/345 contain assertion uncertainty
- 2773/2824 alignments UNCERTAIN
- 308 REVIEW explained by uncertainty gate
- 37 REJECT explained by critical mismatch overriding uncertainty
- relation alignments 0
- 339/345 non-1:1 assertion groups
- 331/345 source assertion count > candidate count
- median source:candidate ratio 4.83
- current unequal-count code appends all leftovers to last group

Most defensible mechanism:
`EXTRACTION/REPRESENTATION UNCERTAINTY + UNEQUAL-COUNT GROUPING AMPLIFICATION + FAIL-CLOSED REVIEW GATE`

Decision-rule-only relaxation:
`NOT JUSTIFIED`

Proposed V2.6-DEV design only:
- R1 boundary/markup normalization
- R2 localized assertion confidence
- R3 partial exact alignment with explicit unmatched nodes
- R4 independent extraction-coverage extension only if still needed

NO IMPLEMENTATION performed.

FactPICO V2.5 experiment:
`100% COMPLETE`

Scientific performance improvement:
`0%` because runtime is unchanged.

Current indicators:
- diagnostic localization completeness 92/100
- evidence/reproducibility 99/100
- process rigor 99/100
- repair-direction confidence 88/100
- validated benchmark satisfaction 30/100
- overall English-track maturity 74/100

Next review packet:
`FACTPICO_V25_FAILURE_ANALYSIS_AND_REPAIR_DESIGN_REVIEW_PACKET.txt`
commit `731160384e89a6d28c2b892b8b05697fc6d4e2f5`

Current exact checkpoint:
`FAILURE_ANALYSIS_AND_REPAIR_DESIGN_REVIEW`

Still forbidden:
- FactPICO rerun/rescoring
- threshold/gold/population changes
- repair implementation until independent approval
- custom Gate C
- Arabic work


---

# 58. CONSULTATION MINIMIZATION + DEEP-REASONING RULE

Date: 2026-10-05

Explicit user governance update:

## A. Consultation policy

Higher-model / external consultation is now an EXCEPTION, not a default.

Use it only when at least one condition holds:
1. the next action is irreversible or one-shot and a wrong decision could permanently invalidate evidence;
2. construct validity, preregistration, benchmark integrity, or a major architecture boundary is genuinely ambiguous;
3. there are two or more technically credible paths with materially different scientific consequences that cannot be resolved from available evidence;
4. the user explicitly requests an independent review.

Do NOT request higher-model consultation for:
- routine debugging;
- code inspection;
- deterministic implementation;
- ordinary experimental design details;
- evidence aggregation;
- descriptive failure analysis;
- repair implementation that is already bounded by an accepted design;
- documentation or continuity updates;
- decisions that can be resolved by direct evidence, deep analysis, literature, or controlled development tests.

Before recommending a consultation, ChatGPT must first:
- perform its own deep analysis;
- inspect all available project evidence;
- conduct deep research when external evidence can materially improve the decision;
- perform genuine multi-hypothesis brainstorming;
- narrow the issue to a specific unresolved question;
- state why it cannot be responsibly resolved internally.

## B. Mandatory deep-reasoning rule

For every material ACAD_PASS decision:
- perform a real deep-analysis pass;
- actively generate competing hypotheses, not a single preferred explanation;
- search for disconfirming evidence;
- compare alternatives on scientific validity, safety, utility, reproducibility, implementation cost, and risk of overfitting;
- use deep web/literature research whenever current external evidence can materially improve the result;
- prefer the narrowest evidence-supported intervention;
- preserve negative findings and failed paths;
- do not optimize for agreement with prior assumptions.

The objective is:
`BEST DEFENSIBLE RESULT, NOT FASTEST AGREEMENT`

## C. Credit/cost conservation rule

Minimize unnecessary model escalations and repeated reviews.
Reuse already-established evidence and previous reviews.
Do not ask the user to spend additional model quota when the task can be completed to a high standard internally.

## D. Current application

The current FactPICO failure analysis and V2.6 repair-design problem is considered technically resolvable internally.
Further higher-model review is NOT automatically required unless a future irreversible scientific boundary is reached or the user requests it.



---

# 59. AT0-EN V2.6-DEV R1-R3 IMPLEMENTED / MECHANICS PASS

Date: 2026-10-05

Development branch:
`at0-en-v2.6-dev`

Internal bounded implementation review:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V2_6_INTERNAL_EVIDENCE_REVIEW_V1.md`
commit:
`a85fed42415a3e01492fac5d442913f6503927b4`

Implemented:
- R1 biomedical-aware boundary/markup normalization with provenance
- R2 atomic/local assertion confidence
- R3 exact partial Hungarian alignment with explicit unmatched OMITTED/NEW_INFORMATION nodes
- final fail-closed pair_outcome ordering unchanged

Independent development mechanics suite:
`phase2/academic_transform/at0_en/v2_6/tests/check_v2_6_representation_dev.py`

FactPICO records used:
`0`

First dev run:
`37334848280` — FAIL preserved as negative evidence.
Only failing family: segmentation 54/60 due to single-letter scientific unit `s.` being mistaken for a personal initial.
Safe 60/60 PASS; critical errors 80/80 REJECT; unsafe PASS 0; unequal-count 60/60.

Narrow code-only fix:
`6e6430fd5b669b0e27d75347dc7d2958154fb402`

Second dev run:
`37335021149` — SUCCESS

Successful artifact:
`11355512964`
digest:
`e3b5975c608901de8c53467fd7d47a9fbda5830df26fe2bacee2fc9c8866b272`

Successful result:
- segmentation 60/60
- safe paraphrase 60/60 PASS_CANDIDATE
- critical error 80/80 REJECT
- unsafe critical PASS 0
- safe REVIEW 0
- unequal-count explicit accounting 60/60
- INVALID 0
- two fresh-process outputs byte-identical

Canonical mechanics summary SHA:
`bdf54ee696e9841d927de46fb4a0d33ab26a43fe13380d34f9134cf941d02476`

This is development evidence only; it is NOT external validation.

Real-RCT stress diagnostic has now been frozen before observation:
`phase2/academic_transform/at0_en/dev_support/v2_6_real_rct_stress.py`
commit:
`e378b24140eb8159ce4d584e5aa8848922e7ce76`

Source:
`sociocom/PICO-Corpus`
source commit:
`482b7d8f135fe6ea424961c2812e8d214c3f4a5f`
30 deterministically selected RCT abstracts with frozen Git blob identities.

R4 decision thresholds were frozen before observing stress results.

Current exact checkpoint:
`V2.6 REAL-RCT STRESS / R4 NECESSITY DECISION`

No FactPICO rerun/rescoring.
No external validation.
No R4 implementation until development evidence justifies it.


## UI/STREAM INTERRUPTION RESILIENCE UPDATE — 2026-10-05

Observed UI symptoms:
- `Our systems are thinking a bit more about this request before responding.`
- `Connection interrupted. Waiting for the complete answer`

Permanent operating rule:
`DURABLE_STATE_BEFORE_RETRY`

When either UI/stream symptom appears:
1. Treat it as an interface/stream event, NOT as scientific or execution failure.
2. Before retrying any operation, inspect the durable state (GitHub branch head, commit history, workflow run, artifact/ledger as applicable).
3. If the intended step already committed or executed, continue from that durable checkpoint and DO NOT repeat it.
4. Preserve partial/failed runs as evidence; never erase them because the UI interrupted.
5. Minimize polling and tool-call count, but never weaken one-shot controls, frozen thresholds, holdout integrity, auditability, or scientific gates.
6. GitHub durable state outranks what was or was not visibly streamed in the chat UI.

Evidence motivating this rule:
During AT0-EN V2.6 R4 work, commits
`9d5e810e5c003950311d4ff8dda4e7e515f8521e`
and
`0ddd847cf660962b35cd6082259ca2da5b11d689`
were durably present even though the chat stream had been interrupted.

Current R4 checkpoint at the time of this update:
- legacy mechanics: 260/260 PASS
- frozen R4 surface suite: 120/120 PASS after bounded fixes
- critical unsafe PASS: 0
- open-30 real-RCT pre-holdout coverage after R4.1: unresolved 57.11%, non-CERTAIN 57.61%
- 60-RCT internal holdout: UNOPENED
- R4.1B generic coverage implementation commit: `60de7ff23150ffefe8936bfebb0db49f0be04463`
- R4.1B validation run: in progress at this checkpoint


# R4 INTERNAL HOLDOUT CONSUMED — R4.2 TRIGGERED

Date: 2026-10-05

One-time internal holdout run:
`37340581937`

Trigger head:
`e9e0b4aead491e02c9534980ab69c6f31b17e865`

Artifact:
`11358256711`
digest:
`sha256:808bce1258ccb2493385d81681b83bc2dbca010b0697f46909a84ab3db27f98c`

Canonical result SHA:
`750e0b11de8f1f4ceb88ef68b55a970d5a92a06957ae0ed77480130d802a63eb`

Holdout:
- 60 RCT documents
- FactPICO overlap = 0
- state = CONSUMED_INTERNAL_DEVELOPMENT_HOLDOUT
- rerun = FORBIDDEN
- R4.1B tuning against holdout = FORBIDDEN
- threshold relaxation = FORBIDDEN

Observed:
- total assertions 715
- unresolved 300 = 41.9580% (FAIL vs <=40%)
- non-CERTAIN 304 = 42.5175% (PASS vs <=45%)
- short evidence <=3 chars = 2 (FAIL vs 0)
- empty documents = 0 PASS
- over-128 documents = 0 PASS
- documents non-CERTAIN <=50% = 49/60 = 81.6667% PASS vs >=80%

Overall:
`FAIL_INTERNAL_HOLDOUT_GATE`

Next exact checkpoint:
`R4.2 AUXILIARY BIOMEDICAL EXTRACTION WITNESS / WEAK-SUPERVISION ARCHITECTURE DESIGN`

Do not inspect holdout text to patch R4.1B.
Do not rerun consumed holdout.
Do not touch FactPICO.


---

# PROCESS PROGRESS OBSERVABILITY RULE

Date: 2026-10-05

Permanent user-project agreement:

For every future execution process, experiment, workflow, training job, validation run, migration, build, or other long-running operation, the implementation SHOULD expose internal progress observability whenever technically feasible.

Minimum required status fields:

- `progress_percent`: estimated completion percentage from 0 to 100.
- `state`: one of `PENDING / RUNNING / COMPLETED / FAILED / STALLED / CANCELLED`.
- `current_stage`: human-readable current step/epoch/phase.
- `completed_units` and `total_units` when meaningful.
- `last_successful_checkpoint`: latest durable completed point.
- `last_progress_at`: timestamp of latest meaningful progress.
- `next_expected_step`: what should happen next.
- `failure_or_stall_reason`: populated when FAILED or STALLED.

For model training specifically, expose when feasible:
- current epoch / maximum epochs;
- current global step / estimated total steps;
- latest training loss;
- latest validation metric;
- best metric/checkpoint so far;
- elapsed time;
- progress percentage;
- heartbeat / last update timestamp.

For batch processing:
- processed records / total records;
- success / failure / skipped counts;
- current item or shard;
- progress percentage.

For GitHub Actions or remote workflows:
- periodically persist a machine-readable status artifact such as `PROCESS_STATUS.json` and/or append heartbeat/progress information to logs;
- do not rely only on the coarse GitHub job state when finer-grained progress can be exposed safely.

Stall rule:
If progress does not change for a predefined reasonable interval, mark the process `STALLED` rather than merely `RUNNING`, while preserving the last durable checkpoint.

This observability requirement must NOT weaken:
- scientific one-shot controls;
- determinism;
- frozen evidence;
- benchmark integrity;
- security;
- reproducibility.

Objective:
`AT ANY MOMENT, WE SHOULD BE ABLE TO TELL HOW FAR THE PROCESS HAS PROGRESSED AND WHETHER IT IS STILL MAKING PROGRESS OR HAS STOPPED.`


---

# R4.2 SAFE TRAIN RUN 4 — TIMEOUT / RECOVERY

Date: 2026-10-05

Run `37355935421` used the validated safe conversion path and was cancelled only by the GitHub Actions 120-minute timeout.

Evidence:
- safe base mapping succeeded;
- checkpoints `591` and `788` existed;
- at least 4 epochs completed;
- no final calibration result exists;
- test sets, FactPICO and consumed 60-RCT holdout stayed closed.

Classification:
`TECHNICAL_EXECUTION_TIMEOUT_AFTER_VALID_TRAINING_PROGRESS`

Execution-only recovery:
- job timeout raised to 360 minutes;
- scientific hyperparameters/data/gates unchanged;
- `PROCESS_STATUS.json` heartbeat added every 10 optimizer steps and at log/eval/save;
- status fields include epoch, step, total steps, progress %, best metric/checkpoint, last progress time and terminal state;
- unbuffered execution enabled;
- checkpoint trainer-state JSON included in always-upload evidence.

Next authorized step:
after the mechanics workflow for this patch succeeds, trigger exactly one V5 safe-path full train+calibration run.


---

# 2026-10-06 — R4.2 V5 VALID RESULT / R4.2B SOURCE-ALIGNED RECOVERY

V5 run `37372306905` attempt 2 completed valid training and calibration.
It is a scientific gate failure, not a technical failure.

Best exact entity macro-F1: 0.6841077577.
Exact micro-F1 of selected best model: 0.665.
Frozen calibration gate: FAIL.
At threshold 0.95, precision P/I/C/O = 0.7400 / 0.843137 / 0.941176 / 0.831325; macro precision 0.838910.

The dominant issue is high-confidence exact-entity false positives for P/I/O.
C passes precision at 0.90 and 0.95.
Recall and accepted-count floors are not the limiting factor.

A deep audit of the pinned source code found V5 training-protocol mismatches:
weight_decay 0.01 vs source 0.0; warmup_ratio 0.10 vs source warmup_steps 0; seed 20261005 vs source 42; eval batch 16 vs source 8; early stopping/best-model selection vs fixed 10-epoch source execution.

R4.2B preflight run `37408747717` proved truncation is not material on fold1:
0 train/dev sentences over budget, 0 gold entities lost, max sequence 139 wordpieces.

Authorized next experiment:
one source-code-hyperparameter-aligned dev-only training run, with all frozen test sets still closed.
No threshold relaxation.

PERMANENT TIME DISPLAY RULE:
Whenever user-facing messages mention a clock time, deadline, start/end time, or converted timestamp, display it in Iraq time `Asia/Baghdad (UTC+3)` unless the user explicitly requests another timezone. Internal GitHub UTC timestamps may be retained in evidence files, but user-facing reporting must convert them to Iraq time.


---

# 2026-10-06 — R4.2B SOURCE-ALIGNED FULL TRAINING RESULT

Run `37409097042` completed the full fixed 10-epoch source-aligned training and frozen-dev calibration.

User-facing Iraq-time milestones:
- training step started: 2026-10-06 06:29:58 Asia/Baghdad (UTC+3)
- epoch 10 / step 1970 reached: 2026-10-06 10:44:45 Asia/Baghdad
- calibration gate result emitted: 2026-10-06 10:45:52 Asia/Baghdad
- artifact upload completed: 2026-10-06 10:46:11 Asia/Baghdad

Execution evidence:
- epochs: 10/10
- global steps: 1970/1970
- progress: 100%
- train runtime: 15282.3433 s (~4 h 14 m 42 s)
- train loss: 0.1087133559
- final checkpoint: checkpoint-1970
- artifact id: 11397202598
- artifact digest: sha256:45d204d5f073aa5ecc5944dc49bee88be5bb677e0160b8c17720f2250de6fa71

Scientific outcome:
`R4_2B_SOURCE_ALIGNED_WITNESS_NOT_READY`

Failure classification:
`SCIENTIFIC_FROZEN_DEV_CALIBRATION_GATE_FAIL`

Exact failure reason recorded by PROCESS_STATUS:
`SOURCE_ALIGNED_FROZEN_DEV_CALIBRATION_GATE_NOT_MET`

This was NOT a timeout, queue failure, runner failure, NaN state, or model-loading failure.
Training completed validly and the evidence artifact was uploaded successfully.

Frozen next step from the run itself:
`STOP_AND_RUN_DEV_ONLY_BOUNDARY_ERROR_ANALYSIS`

Do NOT open EBM/COVID/AD test sets.
Do NOT rerun FactPICO.
Do NOT rerun the consumed 60-RCT holdout.
Do NOT relax calibration thresholds post hoc.

The automatic run watcher was disabled after completion because no automatic scientific rerun is authorized.


---

# 2026-10-06 — R4.2B DEV-ONLY BOUNDARY DIAGNOSTIC / R4.2C DECISION

Dev-only diagnostic run:
`37445035553`

Artifact:
`11402997860`

Artifact digest:
`sha256:6718d7007ed8b16f9644a33879e540ebadd26bcdbb248f98f21d5a74c8e0f5b1`

Canonical diagnostic pre-hash:
`dc5920c1d3148f4b78c7fcde36d25efe78cbf3471db406a5c51e79d36b2d8431`

Scope:
- frozen development split only
- no training
- no threshold changes
- no EBM/COVID/AD tests
- no FactPICO
- no consumed 60-RCT holdout
- no opened-30 diagnostic reuse

At threshold 0.95:
- accepted = 326
- exact TP = 249
- exact errors = 77
- same-type boundary = 47 = 61.039% of high-confidence errors
- overlap-related boundary/type = 59 = 76.623%
- spurious = 18 = 23.377%

Exact precision:
- P 0.769231
- I 0.780303
- C 0.933333
- O 0.724409

Diagnostic partial-overlap micro-F1:
`0.831658`
vs exact micro-F1:
`0.678392`
delta:
`+15.33 pp`

Partial scoring remains diagnostic only and does NOT replace the exact-span gate.

Mechanism:
`HIGH-CONFIDENCE BOUNDARY/TYPE DISAGREEMENT DOMINATES; INTERNAL-SPAN SOFTMAX CONFIDENCE IS NOT AN EXACT-BOUNDARY CONFIDENCE MEASURE`

Frozen next architecture:
`R4.2C SELECTIVE BOUNDARY-CONSENSUS VERIFIER`

Design:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2C_BOUNDARY_CONSENSUS_DESIGN_V1.md`

Next exact step:
`R4.2C DEVELOPMENT-ONLY PREFLIGHT`

No threshold relaxation.
No test-set opening.
No FactPICO/holdout reruns.


---

# R4.2B DEV-ONLY BOUNDARY DIAGNOSTIC — COMPLETE

Date: 2026-10-06

Permanent reporting rule added:
- every user-facing time must be converted to Iraq time `Asia/Baghdad (UTC+3)` unless the user explicitly requests another timezone.

Frozen diagnostic:
- run `37445035553`
- artifact `11402997860`
- digest `sha256:6718d7007ed8b16f9644a33879e540ebadd26bcdbb248f98f21d5a74c8e0f5b1`
- freeze file: `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2B_DEV_BOUNDARY_ERROR_DIAGNOSTIC_FREEZE_V1.md`

Key results:
- 404 predicted entities
- exact correct 270
- same-type boundary errors 70
- spurious 42
- exact-boundary type errors 13
- type+boundary errors 9
- token-level collapsed P/I/C/O micro F1 `0.8101347017`
- entity-level exact micro F1 remains `0.6783919598`
- at threshold 0.95: 326 accepted, 249 exact, 77 errors
- 47/77 high-confidence errors were same-type boundary errors
- 12/77 were type or type+boundary errors
- 59/77 = 76.62% of high-confidence errors are boundary/type-consistency failures
- dense dev-only threshold analysis found no single global threshold meeting all frozen class gates
- extreme class-specific thresholds can fit this dev, but sentence-cluster bootstrap stability was inadequate
- `REJECT_THRESHOLD_ONLY_RESCUE`

Architecture decision:
`R4_2C_INDEPENDENT_BOUNDARY_AND_TYPE_AGREEMENT_GUARD`

Keep R4.2B frozen as candidate generator. Add an independent span-oriented boundary/type verifier; exact span+type agreement is required for witness acceptance, otherwise REVIEW. Do not use dev-specific heuristics and do not relax existing gates.

Exact next authorized checkpoint:
`R4_2C_TRAIN_ONLY_SPAN_GUARD_DESIGN_AND_PREFLIGHT`

Before any new training:
1. inspect frozen TRAIN only for span length/type distributions
2. freeze candidate generation, negative sampling, losses and confidence rule
3. keep current dev for calibration/evaluation only
4. keep EBM/COVID/AD tests, FactPICO, consumed 60-RCT holdout and opened-30 diagnostic closed
5. mechanics/preflight first
6. then authorize exactly one R4.2C training run

Quality delta:
- measured model performance: unchanged
- diagnosis: IMPROVED materially
- dominant failure mechanism: now quantified
- architecture uncertainty: reduced


---

# 2026-10-06 — R4.2C PREFLIGHT PASS / TRAINING PROTOCOL FROZEN

R4.2C preflight:
- run `37447124232`
- artifact `11404450510`
- digest `sha256:f975a0f251bcfd392af49b7227678f7162ad55f7cd970d530083fdf5202868b1`
- canonical pre-hash `e27f70e2db357f289b00d174f1ac7a2d2685c2ad57ee02d841e3c850e3d2fbb5`
- state `R4_2C_PREFLIGHT_READY`

Preflight capacity:
- train P/I/C/O spans = 434/1328/181/1068
- train max gold span width = 54
- dev max gold span width = 30
- frozen max span width = 64
- exact-agreement scorer fixtures PASS
- no test/holdout access

Training protocol frozen:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2C_TRAINING_PROTOCOL_V1.md`

Architecture:
`FROZEN_R4_2B_BIO_CANDIDATE + CLASS_AGNOSTIC_BOUNDARY_LOCALIZER + INDEPENDENT P/I/C/O SPAN_CLASSIFIER`

Boundary module:
- 5 labels OUT/START/END/BOTH/IN
- lr 5e-5
- batch 8
- 3 epochs
- weight decay .01
- fixed boundary generation threshold .25

Span classifier:
- P/I/C/O independent sigmoid outputs; C remains separate
- lr 2e-5
- batch 16
- 3 epochs
- weight decay .01

Model identity remains the validated safe PubMedBERT-base path; no switch to large.

Final calibration grid unchanged:
`{0.80,0.85,0.90,0.95}`

Exact gate unchanged:
per-class precision >=.90, recall >=.20, accepted >=10; macro precision >=.90.

Next exact step:
`IMPLEMENT R4.2C TRAINER/EVALUATOR -> MECHANICS/SMOKE -> ONLY THEN ONE DEVELOPMENT TRAINING RUN`

Tests remain CLOSED.


---

# 2026-10-06 — R4.2C IMPLEMENTATION SMOKE PASS / DEVELOPMENT TRAINING AUTHORIZED

Smoke run:
`37451040508`

Artifact:
`11406382749`

Artifact digest:
`sha256:d51cd634ff242ef11805de77c57560259457572a64c30ebb97533477bb891eea`

Result:
`R4_2C_SMOKE_PASS`

Observed:
- boundary loss = `1.8232231140` finite
- span loss = `0.6865816712` finite
- exact scorer fixtures = PASS
- R4.2B model SHA = `3f1fbad22c6ab13256c142b6d90d13576e3c19b71d68a72598506a201dafca0c`
- safe base conversion remained valid
- boundary and span modules both produced finite gradients and one optimizer update
- no scientific full training occurred in smoke
- no EBM/COVID/AD tests, FactPICO, consumed 60-RCT holdout, or opened-30 diagnostic were used

Decision:
`AUTHORIZE_ONE_R4_2C_DEVELOPMENT_TRAINING_AND_FROZEN_DEV_CALIBRATION_RUN`

No hyperparameter, threshold, data, class, metric, or gate changes are authorized after this point.

Exact next step:
`TRIGGER ONE R4.2C DEVELOPMENT TRAINING RUN -> OBSERVE PROCESS_STATUS -> FREEZE RESULT -> STOP BEFORE ANY TEST INFERENCE`


---

# 60. CROSS-CHAT HANDOFF FILE AGREEMENT

Date: 2026-10-06

User explicitly requires a single portable continuity file that is kept current so a new conversation can resume without losing project state.

Canonical portable handoff:
`ACAD_PASS_CHAT_HANDOFF.md`

Rules:
- update it after every material checkpoint;
- include current branch, durable state, successes, failures, frozen decisions, forbidden actions, key runs/artifacts/hashes, and exact next authorized step;
- in a new chat, read it first, then the master continuity and latest RESUME_HERE tail;
- durable GitHub state outranks stale prose if any discrepancy exists.

Creation commit:
`07791961d45bec3045575c7201d2783dcf51d068`


---

## 2026-10-06 — R4.2C pre-training failure diagnosed; source-aligned recovery smoke PASS

Failed development-train run:
- run `37451685278`
- artifact `11406449018`
- digest `sha256:a515ebe81649f456f669b4da32679de4f6ebaa342388bc51978bc2cb33240ad5`
- failed before first training unit with `RuntimeError: boundary truncation: 54 != 55`
- completed_units = 0; no epoch, no calibration, no scientific result.

Read-only tokenizer-capacity audit:
- run `37454434658`
- artifact `11408961382`
- digest `sha256:fd43fccc9b7dc60664af21ac9178a2d59dea557462b2f99dc43a0a0be141da33`
- max train/dev encoded length = 141 wordpieces including specials;
- >256 = 0; >512 = 0.

Root cause:
17 literal zero-length train surface-token rows across 12 sentences, tags O=5, I-I=5, I-P=6, I-O=1. Pinned source preprocessing explicitly filters tokenized-empty rows.

Source-aligned correction:
commit `a74f064b473a5065886afb39926369305532b778`.
Frozen max_length 256 and all scientific hyperparameters/gates unchanged.

Recovery smoke:
- run `37455086281` SUCCESS
- artifact `11409796452`
- digest `sha256:fd53c2eac731e7eb023f83efb2a646c76052fd5f99e7868648e0d5485551aae9`
- trainer SHA `56b2d77d548c3980700664e58557b33bc0dbde66f99bdff529812fe301e95ca8`
- full train alignment 1576/1576 PASS
- full dev alignment 205/205 PASS
- boundary loss 1.8232231140 finite
- span loss 0.6865816712 finite
- exact scorer PASS
- no scientific full training or forbidden test/holdout access.

Freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2C_RECOVERY_SMOKE_FREEZE_V1.md`
commit `893122f344535850fa226358cdf763398a267ac3`.

Quality delta:
`IMPROVED — TECHNICAL ROOT CAUSE CLOSED / SCIENTIFIC PERFORMANCE NOT YET COMPARABLE`

Exact next checkpoint:
`ONE REPLACEMENT R4.2C DEVELOPMENT TRAINING + FROZEN-DEV CALIBRATION RUN`

STOP before any EBM/COVID/AD test inference.


---

## 2026-10-06 — R4.2C failure localized; R4.2D validity guard activated

R4.2C full replacement run `37464774424` completed all training/calibration and ended `COMPLETED_WITH_GATE_FAIL`, i.e. scientific frozen-dev failure rather than technical failure. Best macro precision was 0.8254464286 at t=0.90; P/I/C/O precision = 0.770833/0.812500/0.937500/0.780952.

Read-only dev FP decomposition run `37477106239` found at t=0.90:
- 225 TP, 56 FP;
- 48/56 FP (85.71%) = individually plausible but jointly invalid spans;
- 33/56 FP (58.93%) = same-class wrong-boundary overlap;
- TP vs FP type-confidence means nearly indistinguishable (0.96918 vs 0.97025).

Chosen architecture:
`R4_2D = FROZEN_R4_2C + TRAIN_ONLY_HARD_NEGATIVE_SPAN_VALIDITY_GUARD`

R4.2D design frozen in `AT0_EN_V26_R4_2D_SPAN_VALIDITY_DESIGN_V1.md`.

Preflight run `37479013072` PASS:
- 3011 positive spans;
- 5442 unique invalid spans;
- 8453 total examples;
- 0 collisions;
- deterministic dataset SHA `6038f5dd905271b27ad7be8f86118aa583f5adc06158b3adcbd9a7f02b724461`;
- max 58 wordpieces;
- smoke loss 0.761030376 finite; gradients valid;
- dev/test not read.

One authorized full R4.2D dev training + frozen-dev calibration run:
`37479970741`
trigger/head `fb3644e2f01189a0f5c0c676fa0f26d4d8ef2116`
started 2026-10-06 17:33:33 Asia/Baghdad.

Stop boundary remains before EBM/COVID/AD external test inference.


---

## 2026-10-06 — R4.2D result and next checkpoint

R4.2D one-shot dev train/calibration run `37479970741` completed all 3 epochs / 1587 steps and ended `COMPLETED_WITH_GATE_FAIL` (scientific, not technical).

Artifact `11422811514`, digest `sha256:7fd6cf920ff98bb19770a8a55efaae35ce73c11a5e4bf5a122b732238bc951e7`.

Best t=0.90 macro precision = `0.8239836029`, versus R4.2C `0.8254464286` (delta `-0.0014628257`, -0.1463 pp).

At t=0.90 accepted/TP/FP changed from R4.2C `281/225/56` to R4.2D `268/214/54`: the guard removed 11 TP but only 2 FP.

Mean P(VALID) among accepted TP = `0.9537864043`; among accepted FP = `0.9662910192`. Therefore the content-only validity guard is rejected and must not be retuned/repeated.

Frozen result:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R4_2D_DEV_GATE_RESULT_FREEZE_V1.md`

Current checkpoint:
`DESIGN_AND_PREFLIGHT_R4_2E_TRAIN_ONLY_JOINT_BOUNDARY_PAIR_VALIDATOR`

R4.2E should use contextual start/end representations from the frozen R4.2C boundary encoder and score the boundary pair jointly. External tests remain closed.


---

## 2026-10-07 — R4.3 contextual pair preflight PASS / STOP BEFORE TRAINING

Independent higher-model verdict:
`RUN_ONE_MORE_TRAIN_ONLY_DIAGNOSTIC_BEFORE_ARCHITECTURE_SELECTION`

Bounded future comparison:
- H0 contextual typed MLP
- H1 same contextual path + biaffine start/end interaction

Critical correction:
R4.2C `48/56 joint_invalid_fp` must not be read as 48 literal cross-entity pairs. Literal gold-boundary cross-pairs were only 3 across all 404 candidates. Competing explanations are missing context, negative mismatch, and endpoint interaction.

Design:
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V1.md`
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V2.md`

Initial preflight run `37533646474` stopped pre-training on 11 source sequence-initial I-* labels. TRAIN-only audit proved all 11 are valid same-type continuation segments across source example boundaries; zero invalid within-example I transitions. V2 freezes explicit continuation-segment semantics without rewriting raw labels.

Successful replacement preflight:
- run `37534110955` SUCCESS
- head `4ca858fcd8b632bc67748bfe1e8fdb0d9d6f8dbd`
- artifact `11446235369`
- digest `sha256:84f9688be55f46dfc6d05cee638c7552e12e6ed0ccae63e3b6f2fc99a4478c94`
- freeze file `AT0_EN_V26_R43_CONTEXTUAL_PAIR_PREFLIGHT_FREEZE_V1.md`
- freeze commit `fca998366cd246b68e13469e1a27d538a66eec88`

Source TRAIN:
- 400 documents, 1576 sequences, 41070 tokens
- gold P/I/C/O = 434/1328/181/1068; total 3011
- max gold width 54
- duplicate document groups 0
- tag-conflicting duplicate docs 0
- invalid BIO after frozen continuation semantics 0

Frozen FIT/SELECT:
- manifest SHA `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`
- FIT 320 docs; P/I/C/O = 342/1038/144/847; total 2371
- SELECT 80 docs; P/I/C/O = 92/290/37/221; total 640
- overlap 0
- SELECT deviations from exact 20% targets: P +5.99%, I +9.19%, C +2.21%, O +3.46%

TRAIN-only negative feasibility:
- local raw 4742
- composites raw 2042 = 1239 same-class + 803 different-class
- unique local+composite NONE 6157
- reserved background fallback unique 1908
- gold/synthetic coordinate collisions 0
- static manifest SHA `1ac4b4dd2ca3c1dbc42b5dc0530cafc93fb289f1646b518e305a3d7c20d5d8d2`
- native FIT-model errors intentionally deferred until a future FIT-only B replica exists

Critical context evidence:
- complete TRAIN: 14 identical cropped token strings/tokenizer sequences occur with multiple entity classes
- FIT prospective construction: 43 cropped token strings (48 tokenizer-ID sequences) can be both entity and synthetic NONE depending on context
This directly strengthens the missing-context hypothesis and explains why content-only R4.2D can fail. It does NOT prove biaffine necessity.

Head sizes:
- H0 trainable = 579,461
- H1 trainable = 662,666
- H1-H0 = 83,205 biaffine parameters

Access guards:
- TRAIN only
- historical DEV false
- fold1 TEST false
- other folds false
- external EBM/COVID/AD false
- FactPICO false
- consumed 60-RCT holdout false
- scientific training false

CURRENT EXACT CHECKPOINT:
`R43_CONTEXTUAL_PAIR_PREFLIGHT_PASS / REVIEW_FROZEN_PACKET_BEFORE_ANY_TRAINING_AUTHORIZATION`

Do NOT train FIT-only B/boundary/type/H0/H1 yet.


---

## 2026-10-07 — R4.3 Stage A FIT-only ancestors launched

Higher-model review + successful TRAIN-only preflight are now frozen.

Canonical R4.3 packet:
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V1.md`
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_DIAGNOSTIC_DESIGN_V2.md`
- `AT0_EN_V26_R43_CONTEXTUAL_PAIR_PREFLIGHT_FREEZE_V1.md`
- `AT0_EN_V26_R43_DIAGNOSTIC_TRAINING_AUTHORIZATION_V1.md`

Frozen split manifest:
`fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`

FIT = 320 documents; P/I/C/O = 342/1038/144/847.
SELECT = 80 documents; P/I/C/O = 92/290/37/221.

Stage A run:
- workflow `AT0 EN V2.6 R4.3 FIT-only ancestors`
- run `37535183682`
- head `ad058bc856c280914158e005b07ffe6a0834aa13`
- state at launch: IN_PROGRESS
- started 2026-10-07 00:37:25 Asia/Baghdad
- current observed step: frozen runtime installation; scientific training not yet entered.

Stage A trains ONLY FIT:
- B candidate generator 10 fixed epochs
- C boundary 3 fixed epochs
- C type 3 fixed epochs
- final fixed epoch only
- SELECT is not training/checkpoint-selection data.

Governance hardening:
generic `at0_en_v2_6_dev_representation.yml` no longer automatically runs real-RCT stress or the already-open 30-RCT audit. Those diagnostics now require separate explicit authorization. The hardening mechanics run `37535069562` passed.

Current exact checkpoint:
`R43_STAGE_A_RUN_37535183682_IN_PROGRESS`

Exact next operation:
monitor THIS SAME Stage-A run; do not relaunch. On success freeze ancestor hashes/evidence, then separately execute the already-authorized Stage B H0-vs-H1 comparison. On technical failure, root-cause and only scientifically neutral repair.

Do not access historical DEV, fold1 TEST, other folds, external EBM/COVID/AD tests, FactPICO, opened-30 diagnostic, or consumed 60-RCT holdout.


---

## 2026-10-07 — TEMPORARY PARALLEL WINDOW DURING R4.3 STAGE A

User explicitly authorized a temporary exception to the usual sequential-only rule UNTIL Stage A finishes:
independent, non-conflicting work may run in parallel while Stage A is active. As soon as Stage A terminates, revert immediately to sequential-only execution.

Canonical Stage A:
- run `37535183682`
- workflow `AT0 EN V2.6 R4.3 FIT-only ancestors`
- status at latest checkpoint: `IN_PROGRESS`
- active scientific step: FIT-only ancestor training
- no live logs available during run; do not infer failure from missing log blob.

Independent work completed during the temporary window:

### 1. Boundary-repair feasibility
Run `37539123038` SUCCESS.
Artifact `11448196366`.
Digest `sha256:f51f6490079bd50218e7e467a7853e5a5391261ce0a5303ced53f4648085da2c`.

Local perturbations:
- 105,766 candidates
- 101,487 unique nearest gold (~95.95%)
- 4,279 ambiguous (~4.05%)
- ~95.28% repairable within +/-4

Composite spans:
- 2,822 total
- 753 ambiguous (~26.68%)
- only 615 (~21.79%) repairable within +/-4

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_BOUNDARY_REPAIR_FEASIBILITY_FREEZE_V1.md`

Interpretation:
near-boundary errors are suitable for gated offset repair; composite/far spans are better suited to contextual verification/review.

### 2. Frozen-base context-signal probe
Run `37539134852` SUCCESS.
Artifact `11447393744`.
Digest `sha256:ffdfee805e32a500403ef5a1fd1f219f96f799b675a1eaf037f1e1bd5607af76`.

FIT-only internal probe:
- cropped macro F1 = 0.563475
- contextual macro F1 = 0.641445
- delta = +0.077970 (+7.797 pp)
- ambiguous-surface subset delta = +0.191111 (+19.111 pp), n=14

Important risk:
- C precision fell 0.5652 -> 0.2687 in the simple contextual linear probe.

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_SIGNAL_PROBE_FREEZE_V1.md`

Interpretation:
context is materially useful, but C remains a stability risk.

### 3. Context-locality audit
Run `37539816534` SUCCESS.
Artifact `11448172538`.
Digest `sha256:f1a69ebce503b40bf598e4abeb4ec334098207a8684e37c52556568bfc1aa29a`.

Conflict keys:
- surface only: 42
- +/-1 context: 2
- +/-2 context: 1
- +/-4 context: 0
- full sentence + coordinates: 0

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_LOCALITY_AUDIT_FREEZE_V1.md`

Interpretation:
most cropped-surface ambiguity is contextual, not irreducible.

### 4. Stage-B mechanics
Run `37540302867` SUCCESS.
Artifact `11447889249`.
Digest `sha256:d35ad79f82cb64d75f9e1f25a3367f1b329962945ec47e07bdac5d49e6647a9c`.

H0:
- 579,461 params
- finite mechanics PASS

H1:
- 662,666 params
- finite mechanics PASS

Difference:
- 83,205 params

Prepared Stage-B implementation:
`r43_stage_b_h0_h1_diagnostic.py`

It has a mandatory candidate-ceiling STOP before H0/H1 scientific training if native SELECT proposals cannot meet recall/support floors.

Frozen mechanics:
`AT0_EN_V26_R43_STAGE_B_MECHANICS_FREEZE_V1.md`

Stage B has NOT been launched.

### 5. Additional independent probe currently running
Run `37540851386`:
`AT0 EN V2.6 R4.3 independent base H0-H1 probe`
FIT-only, frozen-base, no Stage-A outputs, SELECT/DEV/TEST/protected data.
Exploratory only; cannot modify frozen Stage B.

### Durable method registry
`ACAD_PASS_METHODS_REGISTRY.md`
records all tried/researched/retained methods including contextual MLP, biaffine, triaffine, PICOX composites, BOPN, Locate-and-Label, MRC, GlobalPointer/grid, hybrid repair+verification, stronger encoders, ensembles, and DiffusionNER as a retained lower-priority alternative.

### Source-code-audited repair fallback
`AT0_EN_V26_R43_BOUNDARY_REPAIR_SOURCE_AUDIT_V1.md`
documents official BOPN and Locate-and-Label mechanisms.

### Post-Stage-B prospective decision matrix
`AT0_EN_V26_R43_STAGE_B_READINESS_AND_FALLBACK_MATRIX_V1.md`

CURRENT GOVERNANCE:
- while Stage A active: temporary parallel independent work allowed by explicit user authorization;
- when Stage A reaches terminal state: STOP launching parallel work and revert immediately to sequential-only;
- first operation after Stage A terminal: inspect/freeze Stage-A identities and guards;
- only then consider the already-authorized Stage B sequentially.


---

## 2026-10-07 — Parallel exploratory evidence while R4.3 Stage A remains active

Temporary user-authorized exception allowed independent, non-conflicting exploratory work in parallel with Stage A. Scientific processing returns to strictly sequential after Stage A ends.

### Stage A current exact run

- run `37535183682`
- workflow `AT0 EN V2.6 R4.3 FIT-only ancestors`
- status `IN_PROGRESS`
- current step: `Train FIT-only frozen ancestors`
- all setup/acquisition/identity-freeze steps completed successfully
- live job log blob still unavailable while active; no fabricated epoch/step percentage
- automatic watch remains attached to this exact run

### Independent FIT-only boundary-repair feasibility

Run `37539123038` SUCCESS.
Artifact `11448196366`, digest `sha256:f51f6490079bd50218e7e467a7853e5a5391261ce0a5303ced53f4648085da2c`.

Local perturbations:
- candidates 105,766
- unique nearest gold target 101,487 (~95.95%)
- ambiguous nearest target 4,279 (~4.05%)
- repairable within +/-4 = 100,768 (~95.28%)

Composite spans:
- total 2,822
- ambiguous nearest target 753 (~26.68%)
- repairable within +/-4 = 615 (~21.79%)

Implication: future hybrid should preferentially repair local/near-boundary spans, while composite/far/ambiguous spans should be contextually scored/rejected rather than blindly repaired.

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_BOUNDARY_REPAIR_FEASIBILITY_FREEZE_V1.md`

### Independent FIT-only context signal probe

Run `37539134852` SUCCESS.
Artifact `11447393744`, digest `sha256:ffdfee805e32a500403ef5a1fd1f219f96f799b675a1eaf037f1e1bd5607af76`.

All eval:
- cropped accuracy 0.7586423755, macro-F1 0.5634747631
- contextual accuracy 0.7730987072, macro-F1 0.6414445653
- delta macro-F1 +0.0779698022

Ambiguous-surface subset:
- cropped macro-F1 0.3866666667
- contextual macro-F1 0.5777777778
- delta +0.1911111111

Implication: missing context is now directly supported by FIT-only evidence. This supports H0/H1 but does not prove biaffine necessity.

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_SIGNAL_FREEZE_V1.md`

### Independent FIT-only context locality audit

Run `37539816534` SUCCESS.
Artifact `11448172538`, digest `sha256:f1a69ebce503b40bf598e4abeb4ec334098207a8684e37c52556568bfc1aa29a`.

Representation conflicts:
- cropped surface only: 42
- +/-1 context: 2
- +/-2 context: 1
- +/-4 context: 0
- full sentence + coordinates: 0

Frozen file:
`AT0_EN_V26_R43_INDEPENDENT_CONTEXT_LOCALITY_FREEZE_V1.md`

### Stage-B mechanics/readiness

Mechanics run `37540302867` SUCCESS.
- H0 params = 579,461
- H1 params = 662,666
- H1-H0 = 83,205
- both forward/backward finite

Prepared but NOT TRIGGERED:
- trainer `r43_stage_b_h0_h1_diagnostic.py`
- workflow `.github/workflows/at0_en_v2_6_r43_stage_b_h0_h1.yml`

The Stage-B workflow is pinned to Stage-A run `37535183682`, verifies Stage-A summary/model hashes/guards, uses the frozen split, enforces candidate-ceiling stop, then performs only the authorized H0-vs-H1 diagnostic.

Do NOT create `.github/diagnostics/r43_stage_b_trigger_v1.txt` until Stage A is terminal SUCCESS and its artifact is fully verified.

CURRENT EXACT CHECKPOINT:
`R43_STAGE_A_IN_PROGRESS / INDEPENDENT_EVIDENCE_FROZEN / STAGE_B_READY_BUT_NOT_TRIGGERED`


---

## 2026-10-07 — R4.3 Stage A terminal verification and Stage B launch

CURRENT STATUS:
`R43_STAGE_A_100_PERCENT_PHYSICALLY_VERIFIED / R43_STAGE_B_H0_H1_RUNNING`

### Stage A — COMPLETE, SUCCESS, VERIFIED

- Source run: `37535183682`, final success at ~2026-10-07 01:50Z (04:50 Baghdad).
- Head `ad058bc856c280914158e005b07ffe6a0834aa13`.
- Main ancestor artifact `11455753005`; digest `sha256:f2a0352cc4668faf180c4486f496d5bf6ccfd0e39d57fe8144b1b55808d3c2b6`.
- Physical hash verification run `37566322559` SUCCESS, artifact `11458734036` digest `sha256:0b873b366b1267cc86d29b49d60d7982ad65914a78e4011d003abd651a3184c7`.
- Witness `R43_STAGE_A_COMPACT_IDENTITY_PASS`.
- TRAIN SHA `6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e`.
- Immutable split SHA `fbed5472eee4d0158626f438f5169f8767cb44dd65d8d89c74b8a3a573321226`.
- FIT docs320, sentences1292, gold2371 (P342/I1038/C144/O847).
- B_CANDIDATE: 10/10 epochs, steps1620, loss0.1110674603, SHA `4e4852b847be5bf64cd707ed62f770e13d64ee6becea3ce049f69bde220bfb05`.
- C_BOUNDARY: 3/3 epochs, steps486, loss0.2763030014, SHA `8c0848e798dd2b2409a81931b7bac496f88fceec2c8bd589e95a186d67dacebb`.
- C_TYPE: 3/3 epochs, steps447, loss0.1797347431, SHA `c7d5e4d2eb1632ac39c944e28232f8addff6c037b1ea80a09436a885101aed1a`.
- FIT-only and final-epoch-only guards confirmed; no SELECT training, historical DEV, test, other folds, FactPICO, consumed 60-RCT.
- Canonical freeze:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_STAGE_A_VERIFIED_RESULT_FREEZE_V1.md`.

### Independent FIT-only H0/H1 probes — terminal but NOT selection

- Probe A run `37540851386`: H0 macro-F1 0.8054956, H1 0.8211369, H1-H0 +0.0156413.
- Probe B run `37541116791`: H0 macro-F1 0.8457483, H1 0.8277176, H1-H0 -0.0180307.
- Different FIT-only inner partitions and candidate construction; opposite signs. Neither can be used to tune/select the main Stage B.
- Frozen details: `AT0_EN_V26_R43_INDEPENDENT_H0_H1_PROBES_FREEZE_V1.md`.

### Stage B — ONE RUN LAUNCHED

- Run `37566553994`
- Head SHA `a53cc67017d9973c4a76c4c99abdf34e2e329bb3`.
- Workflow `.github/workflows/at0_en_v2_6_r43_stage_b_h0_h1.yml`
- Trainer `phase2/academic_transform/at0_en/v2_6/r43_stage_b_h0_h1_diagnostic.py`
- Trigger `.github/diagnostics/r43_stage_b_trigger_v1.txt`.
- Last confirmed initial status `IN_PROGRESS`.
- Reads only pinned TRAIN and frozen 320-FIT/80-SELECT; uses exact Stage-A ancestor artifacts with SHA verification, makes native FIT-error negatives, computes candidate ceiling, and compares frozen H0 contextual typed MLP versus H1 identical+biaffine using frozen threshold grid `{0.80,0.85,0.90,0.95}`.
- Frozen scientific gate: precision>=0.90 each P/I/C/O, recall>=0.20 each, accepted>=10 each, macro precision>=0.90.
- Candidate ceiling can stop before head training; do not override.
- Stage B monitoring automation `6ac4142f5a1c8191aa1d615ea7e5bf81` updated to exact run `37566553994`, once hourly with state-change notifications.
- Strictly sequential scientific processing REINSTATED; temporary parallel permission expired once A finished.
- Do NOT relaunch Stage A, Stage B, independent probes or consume any closed tests.

NEXT_ACTION:
`WATCH_RUN_37566553994 -> ON_TERMINAL_VERIFY_ARTIFACT_AND_FREEZE_H0_VS_H1_RESULT -> APPLY_FROZEN_DECISION_RULES`.


---

## 2026-10-07 — R4.3 forensic causal review (supersedes tentative architecture escalation)

**CANONICAL REPORT:**
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R43_CAUSAL_FORENSIC_AUDIT_AND_RESEARCH_V1.md`
Commit `b72b013c17411e94dc0f61772684e3754c3c4853`.

**R4.3 STAGE B completed:** run `37566553994`, technical SUCCESS, scientific verdict `DIAGNOSTIC_NO_ARCHITECTURE_READY`. No additional scientific training or protected tests were run in this audit.

- Candidate ceiling: 697 proposals = 447 exact+type TP available / 250 FP; all P/I/C/O reachability floors possible.
- At t=.90, C-style pre-head 371 TP / 100 FP / macro P .8334036915.
- H0 348 TP / 85 FP / macro P .841786177.
- H1 362 TP / 87 FP / macro P .843930214.
- H1 FP taxonomy: 46 spurious/no-gold overlap; 34 same-type wrong-boundary overlap; 5 exact-boundary wrong-type; 2 overlap wrong-type.
- To pass every class precision >=.90 at fixed H1 t=.90 TPs, P must lose >=3 FP, I >=26 FP, O >=20 FP: >=49 P/I/O FPs total without TP loss.

**NEW ROOT FINDINGS:**
1. `native_slots=0` and 1982 fallback slots: no actual FIT B model errors were in head negative training. In-sample B mining plus code that seeds candidates only from gold-containing sentences creates a real training-distribution mismatch; exact relative contribution remains to be measured.
2. Cropped C-type head was trained on exact positive gold spans only, not invalid/NONE spans, but is used as a validity veto.
3. Actual-code synthetic unit test `37568400156` SUCCESS proves invalid predicted I-P after O becomes a candidate span without transition check; occurrence on real FIT remains unmeasured.
4. Current H0/H1 heads can only accept/reject frozen B coordinate/type; no boundary/type repair, no missing entity recovery.
5. A common t across unrelated sigmoid/softmax probabilities is not scientifically calibrated.
6. Full context here means one sentence, not an entire RCT abstract or section.
7. Some gold-absent spans may be annotation-incomplete, not necessarily clinically incorrect; EBM-NLP annotation noise/granularity is literature documented.
8. The current FP taxonomy is operational, not proof of one dominant pathology; R4.3 46 spurious FP differ from older R4.2C distributions.
9. Duplicate-count hazard is future only; current B spans unique. Overlap boundary label overwrite is future nested-entity hazard only.
10. SELECT now exposed; do not treat a further adaptive run on it as a fresh independent test.

**LITERATURE REVIEWED:** PICOX 2024, section-specific PICO 2023, NoiseBench 2024, CMiNER 2025, BEAN 2025, BGNER 2025, OpenBioNER-v2 2026, Multi-head Tri-Affine 2026, Trialstreamer operational workflow, Elicit and independent Elicit evaluation, GLiNER-biomed, BOPN and Locate-and-Label. Exact PICO gate outcomes are not directly comparable to vendor narrative extraction accuracy.

**IMPLEMENTED:** report freeze, methods registry update, `r43_semantic_contract_audit.py` tested SUCCESS, `r43_fit_b_native_error_causal_audit.py` prepared but NOT EXECUTED. A workflow creation attempt for the FIT-only replay was blocked, so no real-world B FIT error counts have been claimed.

**NEW NEXT_ACTION:**
`COMPLETE_FIT_ONLY_CAUSAL_REPLAY_AND_PROTOCOL_AUDIT -> FREEZE_RESULT -> ADVERSARIAL_HIGHER_MODEL_REVIEW -> DESIGN_OOF_NEGATIVE_MINING_WITH_GOLDLESS_COVERAGE -> PROSPECTIVE_TRAIN_ONLY_MODEL_COMPARISON`

Do NOT:
- reinterpret R4.3 as a scientific PASS;
- tune R4.3 thresholds on exposed SELECT;
- train BOPN, triaffine, MRC, GlobalPointer or larger encoder now;
- open historical DEV, protected tests, FactPICO, 60-RCT consumed holdout;
- perform concurrent training.

Maintain strictly sequential scientific execution.


---

## 2026-10-07 — R4.4-A LAUNCHED AFTER FORENSIC/SOURCE-PARITY REVIEW

### Correct source protocol confirmation

Newest corrected source-parity run:
- run `37580279584` SUCCESS
- artifact `11464027321`
- digest `sha256:86ca5a0efa626df59261884e70b95eea7cee8ee0f196f05b35d222c9bd1bfabe`
- freeze: `AT0_EN_V26_R43_SOURCE_PROTOCOL_PARITY_V2_FREEZE.md`

It executes the original `update_data_to_max_len(256)` plus the actual combined-file `evaluate.py -lf` path.
Official/manually independent strict-B source inventory matches exactly:
- P426 / I1326 / C181 / O1067 = 3000 total.
Legacy local-continuation parser = P434 / I1328 / C181 / O1068 = 3011.
All +11 are example-initial continuation fragments (+8P/+2I/+1O).
17 raw tokenizer-empty rows are removed by source preprocessing; no additional max-length split is created.
Run `37570558785` remains superseded tooling error and must not be cited scientifically.

### R44 design state

Canonical files:
- `AT0_EN_V26_R44_OOF_SUPERVISION_REPAIR_DESIGN_V1.md`
- `AT0_EN_V26_R44_ADVERSARIAL_PROTOCOL_REVIEW_V1.md`
- `AT0_EN_V26_R44_PREFLIGHT_FREEZE_V1.md`
- `AT0_EN_V26_R44A_OOF_BANK_AUTHORIZATION_V1.md`
- `AT0_EN_V26_R44A_PRELAUNCH_FORENSIC_AUDIT_V1.md`

Read-only preflight:
- run `37572165532` SUCCESS
- R44 manifest SHA `799844f1bdd15792740333b2ad57c8aad7bb8f265566fece06f4a2ff61574720`
- parent = prior R4.3 FIT only; old R4.3 SELECT excluded.
- DESIGN = 256 docs / 1034 examples / 26,595 tokens / P271 I829 C115 O677.
- VERIFY_INTERNAL = 64 docs / P68 I207 C29 O169. It is INTERNAL only, not a pristine external benchmark, and remains unopened by R44-A.
- 5 OOF folds = 52/51/51/51/51 docs with balanced classes and C>=23 each.

DESIGN source-only package:
- run `37572893091` SUCCESS
- artifact `11461097651`
- design_source SHA `f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18`
- contains neither VERIFY_INTERNAL nor old SELECT.

### Adversarial correction

Ordinary head CV over one OOF bank is blocked due to second-order stacking leakage.
R44 is split:
- R44-A = OOF B + Boundary candidate/evidence bank ONLY.
- STOP.
- R44-B must later use leakage-safe nested outer/inner CV or a fully disjoint stack-development selection protocol.
No J0/J1/head selection is authorized during R44-A.

### Neutral code hardening before launch

- `r44a_oof_fold_train.py`: BIO diagnostics changed from token-level orphan-I overcount to contiguous run-level `INITIAL_I_RUN/O_TO_I_RUN/CROSS_TYPE_I_RUN`; initial-I additionally flags source-gold valid document continuation. Candidate generation semantics unchanged.
- `r44a_aggregate_bank.py`: exact DESIGN document/gold guards P271/I829/C115/O677, plus candidate-row and target-count consistency checks.
- final mechanics/invariants run `37581258498` SUCCESS at current prelaunch code lineage.

### R44-A live execution

Workflow:
`.github/workflows/r44a_oof_bank.yml`

Run:
`37581447046`

Head:
`67c91c0c0f0155ca443bdfef80133cd0700dec14`

State at launch checkpoint:
- fold 0 = IN_PROGRESS
- folds 1/2/3/4 = QUEUED
- max-parallel=1 confirmed operationally; no concurrent scientific fold.
- aggregate waits until all five fold jobs succeed.

Each fold:
- B_CANDIDATE fixed 10 epochs
- C_BOUNDARY fixed 3 epochs
- train = DESIGN minus that fold
- infer = held-out fold only
- gold labels assigned only AFTER inference to candidate targets/taxonomy
- no C_TYPE, no downstream head, no threshold selection
- temporary model weights are not uploaded
- frozen candidate bank / summary / model hashes / guards only.

Automation:
`6ac4142f5a1c8191aa1d615ea7e5bf81`
now watches run `37581447046` hourly for meaningful progress/terminal state and MUST NOT start follow-on work.

### Mandatory stop

After aggregate:
`STOP_BEFORE_R44B_HEAD_TRAINING_OR_VERIFY_INTERNAL_ACCESS`

NEXT:
`COMPLETE_R44A_OOF_BANK -> FREEZE_AND_AUDIT_REAL_OOF_ERROR_DISTRIBUTION -> SELECT/FREEZE_LEAKAGE_SAFE_R44B_PROTOCOL -> ONLY_THEN_CONSIDER_HEAD_TRAINING`.


---

## 2026-10-08 — EXECUTION GOVERNANCE SUPERSESSION: SAFE MAXIMAL CONCURRENCY

This supersedes the older blanket sequential-only execution rule.

Permanent execution policy:
1. Use the maximum safe GitHub Actions concurrency that preserves exact scientific semantics, determinism, auditability, and reproducibility.
2. Parallel jobs are allowed when they have immutable inputs, disjoint outputs, no shared mutable state, no cross-job dependency, and no possibility of data leakage or decision contamination.
3. Dependent scientific stages remain ordered: downstream work starts only after prerequisite artifacts are complete, verified, frozen, and authorized.
4. Serialize any operation that can race on the same branch/ref/file, consume one-shot state, alter another job's inputs/outputs, open protected data, or make scientific attribution ambiguous.
5. Never trade scientific exactness for speed. If parallelism can produce non-exact, confounded, or irreproducible values, do not use it.
6. Preserve hashes, artifacts, guards, model/data identities, per-job status, and provenance for every concurrent path.

The current R44-B B1 execution with 10 independent pair-exclusion upstream jobs plus one immutable label-independent context-cache job is compatible with this policy and should continue rather than be cancelled solely for being parallel.

Higher-model consultation remains selective: request it when evidence is ambiguous, architecture/protocol choice is consequential, failure is difficult, or a high-value alternative warrants independent review. Consultation packets should request deep research, adversarial critique, genuine brainstorming, alternative hypotheses, failure analysis, and best-possible next design.


---

## 2026-10-08 — R44-B B1 UPSTREAM COMPLETE / PRE-HEAD DECISION BOUNDARY

Durable state:
- official R44-B upstream run `37683637815` SUCCESS;
- all 10 pair-exclusion jobs SUCCESS;
- nested aggregate `R44B_PAIR_AGGREGATE_PASS`;
- nested-bank artifact `11515434193`, digest `sha256:98383b4bec040f19d6e4076fea1a70dcb406366dfd4bd724d1ad2fac6d2018fb`;
- outer meta rows 1567/1519/1499/1535/1551;
- C support 68/66/71/69/71;
- immutable context cache `R44B_BASE_CONTEXT_CACHE_PASS`;
- context artifact `11510422862`, digest `sha256:4fdceb511c2067cf81a1ad6c64c039febf99e3c11b9d8baa32b2d73569faa91c`;
- context 26,595 x 768 float32; no labels/protected/VERIFY_INTERNAL/old SELECT.

Canonical freeze:
`AT0_EN_V26_R44B_B1_UPSTREAM_BANK_FREEZE_V1.md`.

Independent pre-head adversarial review:
`AT0_EN_V26_R44B_PREHEAD_ADVERSARIAL_REVIEW_V1.md`.
No disqualifying leakage defect found.

Critical interpretation:
R44-B nested J0/J1 output is DEVELOPMENT MODEL-SELECTION EVIDENCE because the fixed architecture/threshold choice is made from DESIGN nested results. It is not a final unbiased generalization estimate. Freeze architecture + threshold before any future prospective VERIFY_INTERNAL use.

Higher-model packet:
`AT0_EN_V26_R44B_HIGHER_MODEL_REVIEW_PACKET_V1.md`.

A technical-only actual-data mechanics audit was launched as run `37702502662`; it cannot train a scientific head, evaluate thresholds, or access protected data.

NEXT:
`COMPLETE_ACTUAL_HEAD_MECHANICS -> HIGHER_MODEL_ADVERSARIAL_REVIEW -> RECONCILE -> IF_CLEAR AUTHORIZE FIRST FROZEN J0/J1 NESTED HEAD RUN -> FREEZE WINNER/THRESHOLD -> STOP BEFORE VERIFY_INTERNAL`.

Boundary-repair remains deferred as a separate prospective branch, especially if precision passes while recall/coverage remains operationally limited.


---

## 2026-10-08 — R44-B actual head mechanics PASS

Technical-only run:
- run `37702502662`
- conclusion: SUCCESS
- state: `R44B_HEAD_ACTUAL_MECHANICS_PASS`
- artifact: `11517764421`
- digest: `sha256:80d77e63701c9ff80b6b4fc7e571b7b089fbd2120c3bf00693a1c9c9ce570455`

Actual frozen-data audit:
- candidate rows audited across all outer meta/eval files: `9,613`
- context physical SHA: `6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b`
- context index SHA: `db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd`
- context shape: `26,595 x 768`, float32
- max observed candidate width: `45` (frozen embedding capacity =64)
- J0 parameters: `584,631`
- J1 parameters: `667,836`
- actual forward/backward finite on all five outer folds for both J0/J1
- scalar feature ranges valid and finite
- scientific head training performed: false
- threshold evaluation performed: false
- VERIFY_INTERNAL used: false
- old SELECT used: false
- protected data used: false

Quality delta:
`IMPROVED — ACTUAL FROZEN BANK/CACHE FEATURE MECHANICS FULLY VALIDATED`.

CURRENT EXACT CHECKPOINT:
`R44B_UPSTREAM_COMPLETE + ACTUAL_HEAD_MECHANICS_PASS -> HIGHER_MODEL_ADVERSARIAL_REVIEW -> RECONCILE -> IF CLEAR AUTHORIZE FIRST FROZEN J0/J1 NESTED SCIENTIFIC RUN`.

No J0/J1 scientific run has been consumed yet.


---

## 2026-10-08 — R44-B higher-model adjudication and executor closure

Verdict accepted:
`PROCEED_WITH_NONSCIENTIFIC_IMPLEMENTATION_FIXES_ONLY`.

Scientific design unchanged. I2 wording corrections are durable. I1 trainer/evaluator/synthetic closure are implemented.

Scientific attempt identity:
`R44B_B1_DEV_J0J1_ATTEMPT_1`.

Attempt consumption:
`0/1` — no real nested J0/J1 optimizer update has been authorized/executed yet.

Synthetic closure history:
- `37704956922` SUCCESS — superseded simpler closure;
- `37705160972` SUCCESS — superseded;
- `37705311699` FAILURE — synthetic fixture literal-backslash-n JSON bug;
- `37705508807` FAILURE — same non-scientific fixture lineage;
- fixture repaired without score/science-driven changes;
- authoritative candidate `37705640579` currently IN_PROGRESS on head `a20da0098d035a80219171b469033179830392a5`.

The two failures do NOT invalidate scientific evidence and do NOT consume J0/J1 because they used no scientific data/head fit.

Current next:
`37705640579 PASS -> freeze executor identities/artifacts -> pin one-shot scientific workflow -> run 5 folds x 2 heads safely in parallel -> aggregate complete 1942 rows/head -> freeze nomination/no-pass -> STOP before VERIFY_INTERNAL/final refit`.


---

## 2026-10-08 — R44-B one-shot consumed: NO_ARCHITECTURE_NOMINATED

Official DEVELOPMENT scientific run:
- `37706558889`
- attempt `R44B_B1_DEV_J0J1_ATTEMPT_1`
- precheck SUCCESS
- 10/10 J0/J1 outer-fold jobs SUCCESS
- aggregate SUCCESS
- reruns 0

Aggregate:
- artifact `11520076582`
- digest `sha256:f2375a772cc045b2aad6e207747cfec9724b6e84549b3987855ae78e3565e761`

Frozen result:
`AT0_EN_V26_R44B_B1_DEVELOPMENT_RESULT_FREEZE_V1.md`
commit `ce12eb09cec41b4d4eb7e22fa5584f8d5d590d89`.

Decision:
`NO_ARCHITECTURE_NOMINATED`.

Best frozen J0 is t=.95 with macro precision `0.845308610324185`; best frozen J1 t=.95 macro precision `0.8258277690482774`. Recall is not the blocking metric; precision is.

The one-shot J0/J1 attempt is CONSUMED and MUST NOT be repeated.

Read-only causal diagnosis:
`AT0_EN_V26_R44B_B1_FAILURE_CAUSAL_DIAGNOSIS_V1.md`
commit `f7893debaea87a2763963d57e8c9a4276d3d9170`.

Key causal findings:
- J0 t=.95: 171/189 accepted FPs (90.48%) are SAME_CLASS_WRONG_BOUNDARY or SPURIOUS_NO_OVERLAP.
- J0 validity AUROC ~.73284; J1 ~.72637.
- P/I/C/O-only accuracy on valid coordinates is ~.95092 J0 / ~.95164 J1, far above five-way accuracy.
- oracle-validity + existing J1 type-only predictions would pass all frozen class precision gates (diagnostic only).
- original B type + oracle validity still fails C precision, so type correction remains necessary.
- J1 final training CE ~.00067-.00102 yet DEVELOPMENT precision is worse than J0, strong evidence against adding unfocused capacity.

Current causal hypothesis:
`FACTORIZE_CANDIDATE_VALIDITY_FROM_PICO_TYPE_BEFORE_BOUNDARY_REPAIR_OR_CALIBRATION`.

No factorized model has been trained.

Higher-model review packet prepared:
`AT0_EN_V26_POST_R44B_FACTORIZED_REVIEW_PACKET_V1.md`
commit `aa5d4e85d25ce371c48b5839b6cf6b97fab9802e`.

NEXT:
`OBTAIN_HIGHER_MODEL_ADVERSARIAL_REVIEW_OF_ONE_PRIMARY_NEXT_PROTOCOL -> RECONCILE -> ONLY_THEN_CONSIDER_NEW_PROSPECTIVE_DEVELOPMENT_FIT`.

VERIFY_INTERNAL, final refit, calibration fitting, boundary repair, factorized training and all alternate training remain CLOSED.


---

## 2026-10-08 — Late original R44-B independent-review archive reconciled

The user supplied the original external-review deliverables after the R44-B one-shot result was already frozen:
- standalone review Markdown;
- complete independent-review ZIP.

Verification:
- standalone and ZIP-embedded review are byte-identical;
- review SHA-256 `ec18268fc33ee18d4546bdf5a0c3b4480e4578ab411c7ba401ab70d4f30c3f1e`;
- included `verify_frozen_artifacts.py` was re-executed and reproduced `INDEPENDENT_ARTIFACT_IDENTITY_AND_NESTED_ROW_AUDIT_PASS`;
- all four retained evidence ZIP hashes matched;
- no contradiction with I1/I2 implementation, scientific run `37706558889`, frozen no-pass result, or causal diagnosis was found.

Durable audit:
`phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_R44B_LATE_INDEPENDENT_REVIEW_ARCHIVE_AUDIT_V1.md`
commit `e2aae5192100929393de7cd65b709fa16d28874b`.

The post-R44-B higher-model packet was updated to require reading this reconciliation before deciding the next experiment.

No scientific result was reopened and no new fit was authorized.


---

## 2026-10-08 — R44C LINEAR5 selected, preflight PASS, one-shot run active

Post-R44B higher-model verdict:
`PROCEED_OTHER_SINGLE_INTERVENTION`.

Factorization is NOT the next experiment.
Accepted next hypothesis:
`R44C_LINEAR5_L2_V1` — one 19,595-parameter regularized five-way linear estimator using the same frozen inputs/candidates and joint probability semantics.

Key reconciliation:
- five-way CE already contains validity + conditional type supervision;
- copy frozen B type on 1,406 valid coordinates = 96.37%, above J0/J1 type-only ~95.1%;
- near-zero nonlinear-head train losses plus worse J1 outer NLL/generalization justify a bounded capacity/regularization test.

Frozen protocol:
`AT0_EN_V26_R44C_LINEAR5_L2_PROTOCOL_FREEZE_V1.md`.

Authoritative non-scientific preflight:
- run `37725529491` SUCCESS;
- synthetic artifact `11527033325`, digest `sha256:0797f900bfc01f769098b945d3bf9968d26a19d78b696b6f0a163679a158480d`;
- frozen-input artifact `11527950745`, digest `sha256:4b7cc1eadac2989784af900c08502ca1f433b1084c8a8af33e3b37302cc990dd`;
- closure artifact `11527138040`, digest `sha256:b3286ec5308d413dbc8c1c6a1705688c09464a958b3793022d8a76e32499521d`;
- scientific attempt consumed=false;
- real META scaler/model/optimizer not created;
- VERIFY_INTERNAL=false.

Execution freeze:
`AT0_EN_V26_R44C_LINEAR5_EXECUTION_FREEZE_V1.md`.

One-shot authorization:
`AT0_EN_V26_R44C_LINEAR5_SCIENTIFIC_AUTHORIZATION_V1.md`.

Active scientific run:
`37726111765`
attempt `R44C_LINEAR5_L2_DEV_ATTEMPT_1`
trigger head `57790d0fedcc0f42707584ca44118bcbe2fba531`
run_number=1, run_attempt=1.

Immutable precheck SUCCESS.
Five outer-fold jobs dispatched with max safe parallelism=5.
No R44C aggregate result recorded at this checkpoint.

No automatic rerun/replacement is allowed after a real optimizer update.

NEXT:
`MONITOR_37726111765 -> ONE_AGGREGATE_IF_ALL_5_SUCCESS -> FREEZE_RESULT -> STOP`.

If R44C scientific gate fails, sole predeclared fallback:
`STOP_ADAPTING_DESIGN_AND_ACQUIRE_GENUINELY_FRESH_INDEPENDENTLY_ANNOTATED_DATA`.

VERIFY_INTERNAL remains CLOSED.


---

## 2026-10-08 — R44C one-shot frozen FAIL; stop adapting DESIGN

Official run `37726111765`:
- attempt `R44C_LINEAR5_L2_DEV_ATTEMPT_1`;
- immutable precheck SUCCESS;
- 5/5 folds SUCCESS;
- aggregate SUCCESS;
- reruns 0.

Aggregate artifact:
`11528185923`
digest `sha256:e2d1c4fec6106dd56c26e4f781428919dbef2e4e000565bb2563ec5800eee426`.

Frozen result:
`AT0_EN_V26_R44C_LINEAR5_DEVELOPMENT_RESULT_FREEZE_V1.md`
commit `ae5f3ea563fda14e6beb71212d0d2c10562de044`.

Decision:
`NO_ARCHITECTURE_NOMINATED`.
Scientific verdict:
`R44C_LINEAR5_L2_SCIENTIFIC_FAIL`.

Best t=.95:
- macro precision .8767348592080204;
- P .8918918918918919;
- I .8171091445427728;
- C .9318181818181818;
- O .8661202185792349;
- all recalls > .33;
- 897 accepted, 767 TP, 130 FP.

Versus frozen J0 t=.95:
- macro precision +3.1426 percentage points;
- FP 189 -> 130 (-31.22%);
- outer NLL 1.210236485360117 -> .9456049077876719;
- ECE .20785530979613684 -> .17694525120735866;
- validity AUROC only .7328427209613384 -> .7357526910256682.

The bounded low-capacity hypothesis improved generalization metrics but did NOT satisfy the frozen operational gate.

Attempt is consumed; no rerun.

Sole predeclared fallback now active:
`STOP_FURTHER_MODEL_THRESHOLD_LOSS_ADAPTATION_ON_DESIGN_AND_ACQUIRE_GENUINELY_FRESH_INDEPENDENTLY_ANNOTATED_DATA_UNDER_A_SEPARATELY_FROZEN_PLAN`.

No factorization/calibration/boundary repair/hard-negative/alternate model/lambda/seed/threshold work on DESIGN is authorized.

VERIFY_INTERNAL remains CLOSED.

NEXT:
`DESIGN_FRESH_DATA_ACQUISITION_PROTOCOL_ONLY -> INDEPENDENT_REVIEW/FREEZE -> THEN ACQUIRE NEW DATA`.


---

## 2026-10-08 — Fresh RCT acquisition review integrated / protocol frozen / acquisition still BLOCKED

Independent review archived:
`phase2/academic_transform/at0_en/v2_6/FRESH_RCT_INDEPENDENT_ACQUISITION_REVIEW_V1.md`
commit `a39e42faeafc44dcb5c78bc01fc4d008a60fa60b`.

Verdict:
`PROCEED_WITH_ACQUISITION_PROTOCOL_CHANGES`.

Frozen reviewed protocol:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_PROTOCOL_FREEZE_V1.md`
commit `5a98ad9e7723b457144bda4e3c47bc0332b45861`.

Core frozen design:
- exact PubMed candidate-frame query from review;
- earliest-public-results window 2026-01-01 through 2026-09-30;
- simple random family sampling without replacement;
- 80 QUALIFICATION + 400 FRESH_DEV + 5000 SEALED_FRESH_EVAL;
- no C-enriched stratum;
- Title+Methods supplied scope;
- no Outcome labels in titles;
- two independent qualified annotators + third adjudicator;
- semantic AI suggestions excluded from gold;
- EVAL text/IDs/labels/scope/derived representations sealed from developers;
- pooled precision/recall point gates retained;
- added separate trial-balanced one-sided CP lower-bound gate using alpha=.0125/class and >=200 contributing families/class.

Readiness ledger:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_READINESS_LEDGER_V1.md`
latest commit `35f4dc1783c92368f0535ced9acb627fd998f7e5`.

Prior-exposure inventory started:
`AT0_EN_V26_FRESH_RCT_PRIOR_EXPOSURE_INVENTORY_V1.md`
commit `0b4641100462bd646731a465acc445a7b0bd61da`.
State remains INCOMPLETE.

Annotation addendum:
`AT0_EN_V26_FRESH_RCT_ANNOTATION_ADDENDUM_V1.md`
commit `26cd1573a1fc410f1209d1a5f5c38dec5ac54ce4`.

Pinned source manual:
- BIDS-Xu-Lab commit `bc4b878773192f38b2600ec830ca4208b82f7dc0`;
- PDF Git blob `f67df5da9507c562cbeab7ad497e816bde58a02a`;
- size 204547 bytes.

Synthetic statistical preflight:
- run `37828307955` SUCCESS;
- artifact `11572557395`;
- digest `sha256:f9f8f5cd80b0936f8183aacfe008525949428a1f5b310f401c6b233838668926`;
- no EVAL/new RCT/model;
- CP fixtures exactly reproduced;
- HMAC selection verified label/confidence blind.

Synthetic retrieval/provenance tooling preflight:
- run `37828800778` SUCCESS;
- artifact `11572806239`;
- digest `sha256:c5bf089d064987692fa4b8780252c7e6283531a47b0dc47a71f19b0a8be36dbc`;
- no PubMed contact/new RCT/protected-data opening;
- frozen-query, pagination, partition reconciliation, DOI/PMID/title/5-gram/registry triggers tested.

Readiness package:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_READINESS_PACKAGE_V1.md`
commit `6f52306585bfc4f636ef941a892eaf715faa4253`.

HARD BLOCKERS still open:
- qualified human annotator A;
- qualified human annotator B;
- senior adjudicator;
- independent custodian;
- funding/resource feasibility for 5480 dual-annotated documents;
- complete prior-exposure inventory;
- protected-corpus fingerprint custody;
- access-control implementation;
- local immutable PDF copy/hash.

Therefore:
`READINESS_INCOMPLETE_ACQUISITION_BLOCKED`.

FORBIDDEN:
- live PubMed retrieval;
- real allocation seed;
- split membership generation;
- real annotation;
- model adaptation;
- VERIFY_INTERNAL.

NEXT:
`COMPLETE_HUMAN_CUSTODY_RESOURCE_AND_PROVENANCE_READINESS -> INDEPENDENT_READINESS_REVIEW -> EXPLICIT_ACQUISITION_AUTHORIZATION_ONLY_THEN_RETRIEVE`.


---

## 2026-10-08 — Public human-gold federation strategy prepared

User constraints clarified:
- no local expert annotators available;
- objective is best achievable system, ideally better than existing systems, otherwise at least matching strongest comparable system;
- user asked whether previous methods can be rebuilt from scratch while "forgetting" prior data.

Scientific answer frozen in:
`AT0_EN_V26_DATA_RESET_AND_EVIDENCE_POLICY_V1.md`
commit `abdc6b49602057eefe6e3a60af49bbf06cac07bc`.

Core rule:
- computational reset can erase weights/checkpoints/optimizer/calibrators/predictions;
- scientific exposure cannot be erased;
- previously exposed data can become TRAIN/DEVELOPMENT but cannot become genuinely untouched prospective evidence merely by retraining from scratch;
- valid final evidence requires prespecified external/public benchmark test sets not used for score-driven tuning.

New strategy packet:
`AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_PACKET_V1.md`
commit `0bf7d2831addaafd6475b1d482fc9690612cabba`.

Evidence assembled:
- Hu et al. section-specific public P/I/C/O corpora: 800 abstracts, 6821 P/I/C/O entities, explicit C;
- PICO-Corpus: 1011 human P/I/C/O abstracts, but project-exposed -> train/dev only;
- original EBM-NLP: 4993 abstracts; medical-professional test labels, but original schema not native separate-C;
- DISTANT-CTO: >300k trials / ~1m sentences / >977k weak I/C annotations;
- TrialSieve: 1609 abstracts, 52638 final spans, 20 categories, >=3 annotators per abstract, CC0 repository;
- C-TrO: 211 human-annotated randomized phase 3/4 trial abstracts with arm/intervention/outcome relations;
- EvidenceOutcomes: 640 RCT abstracts, three annotators, outcome-focused;
- FinePICO: semi-supervised 2511-abstract federation;
- PICOX: boundary/span architecture directly relevant to ACAD_PASS residual boundary/invalid-span errors;
- AlpaPICO / GPT-4o extraction: LLM comparators/teacher candidates; semantic metrics must not be equated to strict exact-span metrics.

Proposed new evidence hierarchy:
- exposed prior corpora -> TRAIN/DEV only;
- native explicit P/I/C/O human corpora -> core human-gold federation;
- TrialSieve/C-TrO/EvidenceOutcomes -> auxiliary human-gold tasks via frozen adapters;
- DISTANT-CTO/LLM outputs -> weak/silver only;
- official untouched public test splits / leave-one-corpus-out -> benchmark/generalization evidence;
- future truly prospective corpus remains strongest validation but is not required to continue development now.

No successor model training authorized yet.
Next checkpoint:
`INDEPENDENT_HIGHER_MODEL_REVIEW_OF_PUBLIC_HUMAN_GOLD_FEDERATION_PACKET`.


---

## 2026-10-09 — Final public human-gold federation review integrated

Canonical independent review:
`FINAL_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_V1.md`
archived commit `593702253c9cbcd8f62396b2471db51203769e03`.

Review resume:
`FINAL_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_RESUME_V1.md`
archived commit `cfb5dfe33683ece80d06ee9d3aa5c5a18f7c62ce`.

Verdict:
`PROCEED_FEDERATION_WITH_CHANGES`.

Critical corrections implemented:
1. R43/R44 source lineage corrected to EBM-NLP_mod fold1/train at BIDS-Xu-Lab commit `bc4b878773192f38b2600ec830ca4208b82f7dc0`, not PICO-Corpus.
2. DISTANT-CTO removed as direct I/C role supervision; allowed only as role-agnostic semantic intervention-type weak ablation.
3. TrialSieve NonStudyDrug and C-TrO arm membership are not mechanically mapped to C.
4. New preprocessing must be text-only/gold-independent.
5. AlpaPICO/FinePICO/PICOX/GPT-4o incompatible metrics cannot be headline-ranked directly against strict exact P/I/C/O.
6. Broad architecture proposal replaced by finite six-arm first campaign.

Corrected files:
- `AT0_EN_V26_FRESH_RCT_PRIOR_EXPOSURE_INVENTORY_V1.md` commit `0173150950e87376aaa84090b0ac03ba52d9de22`.
- `AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_PACKET_V1.md` commit `8fd7b1f68d54ff90aceec3cd44b086f9a05a103c`.
- `AT0_EN_V26_DATA_RESET_AND_EVIDENCE_POLICY_V1.md` commit `c51cd3437fa5469412e47831a39ed7d803624be4`.

New governing protocol:
`AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_V1.md`
commit `210c1b9f9849a50264945e82e7e3e3d692e90e02`.

Closure ledger:
`AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_AND_PROVENANCE_CLOSURE_V1.md`
commit `1bcdcac6a32b1c2dedb44181d7b4cd47260d5d1f`.

Current closure:
- F01 documentary lineage correction complete; protected/exposed alias custody still pending.
- F02 conceptual correction complete.
- F03 source defect verified; gold-independent preprocessor implementation/preflight pending.
- F04 benchmark eligibility OPEN.
- F05 incompatible-comparison finding verified.
- F06 finite six-arm protocol frozen; execution blocked.

Direct source-code verification completed:
- Hu `utils_ner.py::update_data_to_max_len` uses gold O/non-O state to select inserted chunk boundaries.
- Hu `PICO_ner.py` applies that preprocessing to train/dev/test.
- AlpaPICO `metric.py` uses mention-string sets and gives TP for both-empty sets.
- AlpaPICO `prediction.py` evaluates OUT/INT/PAR.

Public source Git metadata frozen without reading AD/COVID text/labels:
BIDS-Xu-Lab source tree `aa10ba9a8a973129bd797f9a5946b35cb44efea5` contains 5-fold AD/COVID train/dev/test files with immutable blob IDs. Full membership/trial-family audit remains isolated pre-fit work.

No successor training has occurred.
No AD/COVID metric has been released.
VERIFY_INTERNAL remains CLOSED.
R44C remains consumed/frozen.

Current checkpoint:
`PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_FROZEN_PENDING_PROVENANCE_CLOSURE -> IMPLEMENT_ISOLATED_SPLIT_PROVENANCE_AND_GOLD_INDEPENDENT_PREPROCESSING_PREFLIGHT -> NO_FIRST_FIT_YET`.
