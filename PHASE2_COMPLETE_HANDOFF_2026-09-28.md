# COMPLETE HANDOFF — Academic Research & Document Intelligence Platform
## Phase 2 Arabic GEC / SWEET / Safety Architecture

**State date:** 2026-09-28  
**Purpose:** transfer this conversation to a new ChatGPT conversation without losing technical context, decisions, evidence, or next actions.

> **Instruction to the next conversation:** Read this file completely before doing anything. Do not restart or repeat closed Phase 2 work. Inspect the current GitHub branch and the canonical successful runs/commits listed below. Continue from the active **Independent Candidate Acceptance Gate**. Perform fresh deep research + maximum-effort brainstorming before and after every major gate, and whenever surprising evidence appears.

---

# 1. Product objective

We are building a bilingual **Academic Research & Document Intelligence Platform** for EN/AR academic writing, proofreading, controlled rewriting, semantic-fidelity protection, scientific-integrity protection, document preservation, and review.

Target transformation flow:

`UNDERSTAND → PROTECT → PROOFREAD/POLISH/TRANSFORM → INDEPENDENTLY VERIFY MEANING → DETECT SEMANTIC RISK → SELECTIVELY REPAIR → RE-VERIFY → ESCALATE → REVIEW → PRESERVE DOCUMENT → DELIVER`

Core principles:

- Strict Fidelity Engine prevents unintended semantic change during transformation.
- Semantic Equivalence Engine must be independent of the rewrite generator.
- “No warning” is not proof of equivalence.
- Risk states:
  - CRITICAL SEMANTIC RISK
  - POTENTIAL SEMANTIC RISK
  - REVIEW REQUIRED / UNKNOWN
  - NO DETECTED MATERIAL CHANGE
  - later VERIFIED WITH HIGH CONFIDENCE after validation.
- Scientific Integrity Guard protects:
  numbers, p-values, confidence intervals, citations, equations, units, dates, entities, technical terms, method parameters, research questions, etc.
- Source preservation is a first-class invariant.
- Direct Text Workspace and DOCX are both first-class.
- DOCX target includes OOXML/layout/styles/tables/images/captions/hyperlinks/headers/footers/notes/equations/fields/crossrefs/comments/RTL-LTR.
- Word→LaTeX is a later goal.
- AI-detector evasion is **not** a product objective. The product optimizes naturalness, fidelity and voice consistency, not “undetectability”.

---

# 2. Permanent user methodology rule

For **every major phase/gate**:

1. Fresh rigorous technical/research investigation at the start.
2. Maximum-effort brainstorming.
3. Challenge the current architecture rather than justify it.
4. Search for contradictory evidence, alternative models, failure modes and pivots.
5. If a surprising result appears, do not mutate architecture immediately; analyze and brainstorm first.
6. Fresh research + brainstorming again at the end.
7. Always report:
   - what improved;
   - what worsened;
   - expectation for the next step.
8. Do not repeat closed heavy work without a concrete scientific reason.

The user prefers:
- Arabic responses by default.
- Exact next action.
- No unnecessary questions.
- ChatGPT/GitHub/Work should execute instead of asking the user to run terminal commands.
- One complete paste-ready Work prompt when Work is needed.

---

# 3. English track note

Current work is intentionally concentrated on Arabic because it was the hardest blocking path.

English showed materially better early semantic/safety behavior, but the English neural GEC track has **not** yet undergone the same strict sequence now used for Arabic:
real model execution → source-local rendering → selectivity → candidate verification.

After Arabic reaches a stable Development Freeze:
1. return to English correction model evaluation (GECToR or the best current alternative);
2. run the same evidence pipeline;
3. unify EN/AR;
4. test mixed Arabic-English paragraphs.

Do **not** claim English is already completely closed.

---

# 4. Repository

Repository:

`abdullah-s-mahmood/sweet-runtime-parity`

Active branch:

`phase2-arabic-eval`

Repo id:

`1392251096`

Public repository. Never commit:
- model weights;
- private/sealed material;
- sensitive evidence packages.

---

# 5. SWEET official models

Official upstream:

`CAMeL-Lab/text-editing`

Pinned commit:

`4d552ca3ae98029550f27fc52aa1b22883e16e61`

## NoPnx

Model:
`CAMeL-Lab/text-editing-zaebuc-nopnx`

Raw `pytorch_model.bin`:
- size: 539,450,353 bytes
- SHA-256:
`584ccc089d143b1d7c72ea5b296652050359d163e57e4374b920fbac7925e8d6`

## Pnx

Model:
`CAMeL-Lab/text-editing-zaebuc-pnx`

Raw weight:
- size: 538,638,321 bytes
- SHA-256:
`195696eaf09a5b92d8141f473e0e3a0d5a710649114b3180afb25cf76cdaa4f3`

Published pipeline:
NoPnx ×2 → Pnx ×1.

Product architecture does **not** assume the published pipeline is the best product configuration.

---

# 6. Real-weight proof and official runtime parity

Known demo input:

`يجب الإهتمام ب الصحه و لا سيما ف ي الصحه النفسيه ياشباب المستقبل،،`

NoPnx iter1:
`يجب الاهتمام بالصحة ولا سيما في الصحة النفسية يا شباب المستقبل ،`

NoPnx iter2:
same.

Pnx final:
`يجب الاهتمام بالصحة ولا سيما في الصحة النفسية يا شباب المستقبل .`

Canonical official parity run:

- GitHub Actions run: `36400626837`
- head SHA: `05375c9fd368eebf568d72d077ea0393a481529c`

Environment:
- Ubuntu 22.04.5
- Python 3.10.21
- PyTorch 1.12.1+cpu
- Transformers 4.30.0
- NumPy 1.23.5

Result:
- NoPnx hash match PASS
- Pnx hash match PASS
- official NoPnx output matches NumPy/SciPy proof
- final output matches prior proof
- final output matches public model-card demo
- upstream rewrite commit pinned

Marker:

`OFFICIAL_REFERENCE_RUNTIME_PARITY: PASS`

Therefore:

`PHASE 2 MODEL EXECUTION GATE: CLOSED`

Runtime parity does **not** prove quality or semantic safety.

---

# 7. Phase 2 Arabic development data

Source:

Nahw Arabic Grammar Benchmark  
`https://github.com/qcri/nahw-arabic-grammar-benchmark`

Development set:
- 150 correction targets
- from only 41 passages
- therefore 150 target rows are **not independent observations**
- uncertainty/statistics must cluster by passage
- 59 prior sealed identifiers excluded
- 12 project-authored scientific stress cases, NON_HUMAN_GOLD
- narrow deterministic baseline = 0/150

Canonical transfer commit:

`3cd6939e346176cc3f1f024c126db8341dce2af0`

Nahw reference usually corrects one local location; it is **not whole-passage complete gold**.  
Collateral edits are not automatically wrong.

---

# 8. Raw official SWEET Arabic evaluation

Canonical run:

`36412018852`

Head:

`9295634cbb1ad4be6911e433f883bf5e4b28e98c`

## Target recovery

NoPnx1:
- 29/150 = 19.33%
- passage-cluster bootstrap roughly 14.0–24.83%
- hamza: 12/38 = 31.58%
- generic: 17/98 = 17.35%

NoPnx2:
- 29/150 = 19.33%
- gained one target, lost one target → net zero

Pnx-only:
- 3/150 = 2.0%

Full NoPnx2→Pnx:
- 29/150 = 19.33%
- Pnx added zero target gains on this metric.

Important:
19.33% is localized target exact recovery, **not overall Arabic GEC accuracy**.

---

# 9. Renderer corruption discovery

On 41 passages:

NoPnx1:
- changed 41/41
- 160 non-K labels
- 3 passages changed despite zero non-K labels

Pnx-only:
- changed 41/41
- 24 non-K labels
- 29 passages changed despite zero non-K labels

Cause:
official `rewrite()` reconstructs subwords and `detokenize_sent()` joins with spaces.

Conclusion:
official renderer is valid for reproduction, but not suitable as a Strict-Fidelity product renderer.

---

# 10. Raw scientific stress findings

12 project-authored scientific cases.

Raw full SWEET:
- exact protected spans: 4/12
- whitespace-insensitive protected preservation: 10/12
- whole source ws-insensitive unchanged: 4/12
- output changed exactly: 12/12
- [UNK] cases: 6/12

Examples:
- `5 mg/kg` corrupted to tokens containing `[UNK]`
- date spacing corruption
- variable splitting
- citation/English fragment changes
- vocalized Arabic → `[UNK]`

---

# 11. Protected-span prototype

File:

`phase2/arabic_eval/prototype_protected_span_sweet.py`

Logic:
- exact protected locks
- preflight [UNK] → preserve source
- postflight [UNK] → preserve source
- zero non-K → preserve exact source
- protected spans reinsert exactly

NoPnx1:
- protected 12/12
- UNK 0
- source exact unchanged 9/12

Full + Pnx:
- protected 12/12
- UNK 0
- source unchanged only 3/12

This supported NoPnx1 as conservative base and Pnx as selective-only candidate.

---

# 12. Raw SWEET adjudication

Work reviewed:
- 41/41 passages
- 150/150 targets
- 56/56 TARGET_CHANGED_OTHER
- 1541 collateral edits

Commit:

`2d72cef18a6de2c306dfdb320b84f58dfda2f672`

Results:
- supported alternatives: 10
- wrong corrections: 50
- partial: 2
- review required: 88

Crucial finding:
~1395/1541 collateral changes were `SURFACE_RENDERER_CHANGE`.

Most apparent collateral damage was renderer noise, not model linguistic edits.

---

# 13. Source-Preserving Surgical Renderer

Initial commit:

`5eaa579773e52b0946c2ee824db31fd29e508133`

Architecture:

Original source  
→ SWEET non-K edits  
→ map edit to exact source span  
→ apply only that edit  
→ untouched characters remain byte-for-byte original.

Safety:
- [UNK] → abstain
- unsafe map → abstain
- protected span → lock
- unsafe merge → abstain
- no edit → exact source

Canonical run:

`36436857686`

Results:

NoPnx1 surgical:
- exact recovery 32/150 = 21.33%
- changed passages 33/41
- applied model edits 60
- suppressed hazards 100

NoPnx2:
- 31/150

Full:
- 31/150
- more changes with no target gain

Scientific:
- protected 12/12
- UNK 0
- source unchanged 11/12

---

# 14. Surgical adjudication

Commit:

`b621cad48b89af8dc0ae37977a8170e2571607d4`

Results:
- applied edits adjudicated: 60/60
- supported: 49
- unnecessary: 2
- wrong: 7
- partial: 2
- review required: 0
- suppressed hazards audited: 100/100
- confirmed useful corrections lost: 0
- AUTO_ACCEPT_CANDIDATE passages: 22/41
- REVIEW: 4/41
- REJECT: 7/41
- UNCHANGED: 8/41

NoPnx2 decision: TEST_SELECTIVELY  
Pnx decision: TEST_SELECTIVELY

Applied-edit supported precision:
49/60 = 81.67%

Operation families:
- INSERT: 18/19 supported = 94.7%
- REPLACE: 26/32 = 81.25%
- DELETE: 5/9 = 55.56%

DELETE is the riskiest family.

---

# 15. Selectivity sweep and Selective Surgical Gate

Retrospective rule discovered on development:
- non-space INSERT → allow
- REPLACE if confidence ≥ 0.80 → allow
- DELETE → abstain

On same dev:
- retained 38
- supported 37
- wrong 0
- partial 1
- precision 97.37%

This is **not a sealed estimate** because the rule was discovered on the same dev evidence.

Files:
- `phase2/selectivity/PHASE2_SELECTIVITY_POLICY_SWEEP.json`
- `phase2/selectivity/PHASE2_SELECTIVITY_NEXT_GATE.md`

Canonical Selective Surgical Gate run:

`36445652931`

Results:
- retained 38
- supported 37
- wrong 0
- partial 1
- unnecessary 0
- precision proxy 97.37%
- changed passages 26/41
- automated exact target recovery 28/150

Burden proxy:
- 25 AUTO_ACCEPT_CANDIDATE
- 15 UNCHANGED
- 1 REVIEW
- 0 REJECT

Scientific:
- protected 12/12
- source unchanged 12/12
- UNK 0

Tradeoff:
precision/safety ↑ substantially, target coverage ↓.

---

# 16. GED experiment

Public GED-13 models:
- ZAEBUC
- QALB14

ZAEBUC:
- target locations detected: 99/150 = 66%

QALB14:
- 79/150 = 52.67%

GED hard gating did not improve the already 0-wrong operation-aware stream and reduced useful coverage.

Decision:
- GED hard gate: DROP
- GED soft feature/ranking: WATCH / TEST

---

# 17. Reversible normalization feasibility

98 NoPnx hazards were caused by tokenizer [UNK].

Internal view:
- remove Unicode Mn combining marks
- remove tatweel
- source remains immutable
- exact index map retained

Result:
- 98/98 became tokenizable
- 0 remained [UNK]

Tokenizable ≠ correct.

---

# 18. Reversible Normalized Candidate View

Canonical run:

`36447653438`

Files:
- `PHASE2_NORMALIZED_CANDIDATE_QUEUE.jsonl`
- `PHASE2_NORMALIZED_CANDIDATE_QUEUE_SUMMARY.json`
- `PHASE2_NORMALIZED_CANDIDATE_MANIFEST.json`

Results:
- former-UNK locations: 98
- locations with non-K candidate: 19
- no candidate: 79
- 19 candidate rows
- 14 passages
- all 19 source spans identified
- unsafe projections: 0
- published targets overlapping hazard words: 32
- automated normalized target matches: 12
- all 12 were previously ERROR_PRESERVED

---

# 19. Normalized candidate adjudication

Commit:

`12b0c5cc44a1f827314959b9f438652492194718`

Results:
- candidates: 19/19
- supported corrections: 12
- supported alternatives: 1
- partial: 4
- unnecessary: 1
- wrong: 1
- review required: 0
- automated matches confirmed: 9/12
- new supported target recoveries: 9
- safe simple surface realization: 2
- ambiguous realization: 15

Fully supported/alternative:
13/19 = 68.42%

Including partial directional usefulness:
17/19 = 89.47%

Main bottleneck shifted to:
**morphology + case/mood + diacritic surface realization**

---

# 20. Morphology-Aware Surface Realization Gate

Runtime:
- CAMeL Tools 1.5.2
- CALIMA MSA R13
- MLE morphology disambiguator
- BERTUnfactoredDisambiguator contextual morphology

Canonical successful run:

`36453279349`

Results:
- 18/19 morphologically analyzable
- 17/19 have multiple source-preserving surfaces
- only 1/19 unique before contextual ranking

Among 13 target-overlapping candidates:
- target-compatible somewhere in morphology lattice: 11/13
- MLE top1 correct/equivalent: 7/13
- contextual BERT top1: 10/13
- BERT top2 consensus: 7/13

Bounded gate generated 9 proposals.

---

# 21. Morphology Surface Adjudication

Manifest commit:

`f2600b1a4df1ef934554f92ae6f47dc7cf165d92`

Evidence commit:

`bc15f8987f25d0ff11637268585f0e14f116d2ba`

Results:
- rows reviewed: 19/19
- runtime proposals reviewed: 9/9
- EXACT_SAFE_REALIZATIONS: 3
- CORRECT_ALTERNATIVE_SERIALIZATIONS: 5
- OVERDIACRITIZED_BUT_CORRECT: 4
- partial: 0
- wrong: 0
- review required: 0
- AUTO_APPLY_CANDIDATES: 3
- correct abstentions: 2/7
- safe surface missed by abstention: 2

Gold-independent surface policies:
- DIRECT_PATCH_ONLY: 2/2 = 100%
- BERT_TOP2: 8/9 = 88.9%
- BERT_TOP1: 13/18 = 72.2%
- MLE_TOP1: 9/18 = 50%
- DIRECT_PATCH_OR_BERT_TOP2: 10/11 = 90.9%

Critical counterexample:

`وساعٍ → وساعا`

Morphology + BERT consensus accepts it, but correct grammar requires:

`وساعيًا`

Therefore:

**Morphology is a surface ranker/realizer, NOT a candidate correctness verifier.**

Other observed failure modes:
- `باسمًا → باسْمٍ` lexical/case confusion
- `إستشعِر` imperative can be ranked as past
- unnecessary overdiacritization
- fathatan/alif Unicode serialization differences

Post-review commit:

`5673af03e83a5867c3339670c5bfe80e9f07b108`

New bottleneck:
**Independent Candidate Acceptance**

---

# 22. ACTIVE GATE — Independent Candidate Acceptance

The user explicitly requested:

**“ابدأ Independent Candidate Acceptance Gate ولا تنسى البحث المعمق والعصف الذهني”**

Goal:
build a verifier whose runtime decision uses **no Nahw gold and no previous human adjudication label**.

Candidate evidence:
- SWEET edit type/confidence
- GED soft signal
- morphology evidence
- deterministic Arabic grammar vetoes
- independent Arabic GEC source
- source fidelity
- later scientific/semantic safeguards

Output:
ACCEPT / REVIEW / REJECT.

---

# 23. Independent Arabic second generator

Official repo:

`CAMeL-Lab/arabic-gec`

Pinned upstream commit used in canonical successful acceptance run:

`8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf`

Models:

GED:
`CAMeL-Lab/camelbert-msa-qalb14-ged-13`

Resolved revision:

`447179dc63d186e4bff09a993e90e73ad622d571`

AraBART GEC:
`CAMeL-Lab/arabart-qalb14-gec-ged-13`

Resolved revision:

`410588a318d988cdcfdbf64cf5745ed4adea0f6a`

Official architecture:
contextual morphology preprocessing + GED + AraBART seq2seq.

AraBART output is never accepted as a full rewritten sentence; it must be aligned back into source-local edits.

---

# 24. CRITICAL CURRENT GITHUB STATE

At handoff creation, active branch HEAD is:

`bb1c74f4791cbe7b9c81286a63a687828c9cd327`

Message:

`Run independent candidate acceptance gate`

The latest run on that HEAD **failed**.

Several new/refactored workflow attempts after a successful acceptance run also failed.

This does **not** invalidate the scientific evidence from the earlier canonical successful run.

## Canonical successful acceptance run

Run:

`36459266906`

Workflow:

`Phase 2 Independent Candidate Acceptance Gate`

Head:

`2b032bb6aaeb9a6e7bb5953746791302684fa6fd`

Conclusion:

`success`

Persisted evidence commit:

`5d3f735`

Artifact:
- id: `10987145402`
- name: `phase2-independent-acceptance-gate-evidence`
- size: ~287 KB
- digest:
`sha256:c15446aa98ce7e9841373977760088c7a7652bc17591107470cb37ab1a91be02`

**The next conversation must use run 36459266906 / commit 5d3f735 as canonical first-pass acceptance evidence, then reconcile later failed workflow refactors.**

---

# 25. Acceptance Gate successful results

Population:
- runtime candidates: 79
- surgical candidates: 60
- normalized candidates: 19
- candidate passages: 37
- new AraBART unadjudicated edits: 67

Files at commit `5d3f735`:
- `PHASE2_ARABART_SECOND_GENERATOR.json`
- `PHASE2_ARABART_MODEL_REVISIONS.json`
- `PHASE2_ACCEPTANCE_RUNTIME_FEATURES.jsonl`
- `PHASE2_ACCEPTANCE_POLICY_RESULTS.json`
- `PHASE2_ACCEPTANCE_GATE_SUMMARY.json`
- `PHASE2_ARABART_NEW_EDIT_QUEUE.jsonl`
- `PHASE2_ACCEPTANCE_GATE_MANIFEST.json`

Manifest confirms:
- runtime decisions materialized before human labels
- sealed=false
- Phase3=false

---

# 26. Acceptance policy results

## ARABART_BASE_AGREEMENT
- accepted: 40
- review: 34
- reject: 5
- accepted supported: 37
- wrong: 1
- partial: 2
- unnecessary: 0
- supported precision: 92.5%
- supported coverage: 59.68%
- accepted high/critical wrong: 1

Too risky as automatic policy.

## ARABART_BASE_PLUS_GED
- accepted: 22
- review: 52
- reject: 5
- supported: 21
- wrong: 0
- partial: 1
- precision: 95.45%
- supported coverage: 33.87%
- high/critical wrong: 0

Safer, but low coverage and still one partial.

## REVIEW_FIRST
- accepted: 36
- review: 38
- reject: 5
- supported: 34
- wrong: 1
- partial: 1
- precision: 94.44%
- coverage: 54.84%
- high/critical wrong: 1

Still one serious wrong.

## STRICT_CONSENSUS
- accepted: 20
- review: 54
- reject: 5
- supported: 20
- wrong: 0
- partial: 0
- unnecessary: 0
- development precision: 100%
- supported coverage: 32.26%
- high/critical wrong: 0

This is **development evidence only**, not sealed or production precision.

---

# 27. Acceptance counterexamples

## NORM-38-24-0
Source:
`وساعٍ`

Candidate:
`وساعا`

Human evaluation:
WRONG_CORRECTION

AraBART base-level alignment agrees, but deterministic veto:

`DEFECTIVE_NOUN_YAA_RESTORATION_RISK`

All acceptance policies reject it.

This is an important success for deterministic grammar vetoes.

## NORM-63-11-0
Source:
`إستشعِر`

Candidate:
`استشعر`

Human class:
SUPPORTED_CORRECTION

Policies:
- BASE_AGREEMENT: ACCEPT
- PLUS_GED: REVIEW
- STRICT_CONSENSUS: REVIEW
- REVIEW_FIRST: REVIEW

Strict consensus may be too conservative for this valid hamzat-al-wasl correction.

## NORM-63-24-0
Source:
`باسمًا`

Candidate:
`باسم`

Human class:
PARTIAL_CORRECTION

Policies:
- BASE_AGREEMENT: ACCEPT
- PLUS_GED: ACCEPT
- STRICT_CONSENSUS: REVIEW
- REVIEW_FIRST: REVIEW

Important:
0 wrong does **not** mean all accepted edits are fully correct. Partial correction remains a distinct failure.

---

# 28. New AraBART edit queue

Canonical successful run produced:

`PHASE2_ARABART_NEW_EDIT_QUEUE.jsonl`

Count:

**67 new AraBART local edits not yet fully adjudicated.**

Examples include changes such as:
- `الطلبة → الطلبه`
- `وأطيعوا → واطيعوا`
- `الفاضلة → الفاضله`
- `أفئدتكم → افئدتكم`

This demonstrates that AraBART can introduce orthographic normalization/change and cannot be trusted as a full-sentence writer.

AraBART must remain:
**second candidate generator → local edit alignment → verifier**.

---

# 29. Full AraBART Edit Audit

A later dedicated workflow succeeded:

Run:

`36460634633`

Workflow title:

`Phase 2 AraBART Full Edit Audit`

Conclusion:

`success`

This run must be inspected by the next conversation before any new architecture change.

Do not assume the 67 new edits are all wrong or useful until the audit evidence is read.

---

# 30. Later workflow failures

After the successful acceptance run, multiple commits/refactors were added:
- `2e1704ae5aeaaff109b54228b585675d54a65e79`
- `f84d8b7c537b97b285bc419738e01b1f9e174971`
- `0718ae8831c4f46fb16f353f35b2d81d5e189b3f`
- `fbfd361350010945245e186f7bd625e26ed18883`
- `bb1c74f4791cbe7b9c81286a63a687828c9cd327`

Several runs failed.

Latest known run:

`36461982406`

on:

`bb1c74f4791cbe7b9c81286a63a687828c9cd327`

Conclusion:

`failure`

Do not treat this as a scientific failure of the gate.  
It is currently an orchestration/runtime/refactor state that must be reconciled.

---

# 31. Immediate required action in the NEW conversation

Before coding anything:

1. Inspect canonical successful acceptance run:
   - `36459266906`
2. Inspect evidence commit:
   - `5d3f735`
3. Inspect artifact:
   - `10987145402`
4. Inspect successful full AraBART edit audit:
   - `36460634633`
5. Inspect latest failed acceptance workflow:
   - `36461982406`
6. Determine why later workflow attempts failed.
7. Determine whether newer refactor:
   - duplicated an older working workflow;
   - introduced dependency/version regression;
   - changed paths/names;
   - deleted/replaced evidence files;
   - or intentionally superseded old behavior.
8. Restore one clean canonical acceptance workflow.
9. Preserve the scientific evidence from run `36459266906`.
10. Do **not** rerun any earlier Phase 2 stage.

Recommended exact opening instruction:

> **Continue Phase 2 — Independent Candidate Acceptance Gate from PHASE2_COMPLETE_HANDOFF_2026-09-28.md. First inspect GitHub state and reconcile canonical successful run 36459266906 / commit 5d3f735 with the later failed workflow attempts ending at branch HEAD bb1c74f4791cbe7b9c81286a63a687828c9cd327. Also inspect successful AraBART Full Edit Audit run 36460634633. Do not restart any earlier Phase 2 work. Perform fresh deep research + maximum-effort brainstorming before modifying architecture.**

---

# 32. What the Independent Candidate Acceptance Gate must ultimately prove

Can a gold-independent runtime acceptance policy achieve:

- no known HIGH/CRITICAL wrong corrections accepted;
- high supported-edit precision;
- materially better useful coverage than direct-patch-only;
- no Nahw target or previous human label in runtime;
- source fidelity;
- compatibility with Scientific Integrity Guard;
- explicit abstention/review when uncertain?

Candidate features may include:
- SWEET operation family
- SWEET confidence
- AraBART local agreement
- GED soft evidence
- morphology rank
- deterministic grammar validators
- source-fidelity constraints
- semantic/scientific safeguards

Do not freeze STRICT_CONSENSUS yet despite 100% current dev precision because:
- same 41 passages
- development-tuned candidate pool
- 67 new AraBART edits still need characterization
- review burden is high
- no independent sealed set yet

---

# 33. Current best Arabic architecture hypothesis

```
Original Source
   │
   ├── NoPnx1 surgical candidates
   │
   ├── normalized fallback candidates after tokenizer hazard
   │
   └── AraBART independent local edit candidates
          │
          ▼
Gold-independent Candidate Acceptance
   ├── operation family
   ├── SWEET confidence
   ├── GED soft evidence
   ├── AraBART agreement/disagreement
   ├── deterministic Arabic grammar vetoes
   ├── morphology features
   └── source-fidelity constraints
          │
       ACCEPT / REVIEW / REJECT
          │
          ▼
Morphology Surface Realization
          │
          ▼
Scientific Integrity Guard
          │
          ▼
Semantic/Fidelity Verification
          │
          ▼
Surgical exact source patch
```

Strict Scientific mode:
- normalized candidates are highly conservative
- citations/technical terms/numbers/units/equations/entities protected
- linguistic correctness alone is insufficient.

---

# 34. Important research references

- SWEET ACL 2025:
  `https://aclanthology.org/2025.acl-long.875/`
- Arabic GED/GEC EMNLP 2023:
  `https://aclanthology.org/2023.emnlp-main.396/`
- Nahw EACL 2026:
  `https://aclanthology.org/2026.eacl-long.296/`
- CLEME2.0 ACL 2025:
  `https://aclanthology.org/2025.acl-long.10/`
- Minimal-edit GEC BEA 2025:
  `https://aclanthology.org/2025.bea-1.9/`
- CAMeL Morph LREC-COLING 2024:
  `https://aclanthology.org/2024.lrec-main.240/`
- Morphologically informed Arabic diacritization:
  `https://aclanthology.org/2024.lrec-main.128/`
- User/source-diacritic preservation EMNLP 2025:
  `https://aclanthology.org/2025.emnlp-main.846/`
- ArbESC+ preprint:
  `https://arxiv.org/abs/2511.14230`
- Edit-level voting BEA 2026:
  `https://aclanthology.org/2026.bea-1.60/`
- Edit verification/reranking EMNLP 2022:
  `https://aclanthology.org/2022.emnlp-main.785/`

Emerging research direction:
**multi-source candidate generation + source-local alignment + independent candidate acceptance + morphology realization + semantic/scientific safety + abstention/review**

not end-to-end rewriting.

---

# 35. Do NOT redo these closed items

Do not redo unless new evidence shows an actual defect:

- SWEET model acquisition
- NoPnx/Pnx weight verification
- official runtime parity
- 150 development target creation
- 41 passage extraction
- 59 sealed exclusions
- raw SWEET inference
- raw target recovery
- raw adjudication
- protected-span prototype
- surgical renderer proof
- surgical adjudication
- selective surgical gate
- GED hard-gate test
- reversible normalization feasibility
- normalized candidate generation
- normalized candidate adjudication
- morphology surface gate
- morphology surface adjudication

Do not create a sealed benchmark yet.  
Do not start Phase 3 yet.

---

# 36. Epistemic cautions

- 150 targets are clustered within 41 passages.
- never treat them as 150 independent statistical samples.
- Nahw references are local, not complete whole-passage gold.
- collateral edits can be valid.
- automated exact match is not linguistic adjudication.
- dediacritized equality can hide case/mood errors.
- morphology analyzability ≠ grammatical correctness.
- morphology consensus ≠ correction verifier.
- development 100% precision ≠ production precision.
- 12 scientific cases are project-authored NON_HUMAN_GOLD.
- Work PASS2 is same-agent unless genuinely independent adjudicator is explicitly available.
- runtime parity ≠ quality/safety.

---

# 37. One-line current status

**Arabic Phase 2 is not finished. The project has progressed from raw renderer corruption to a source-preserving, selective, normalized, morphology-aware, multi-source candidate architecture. The active unresolved problem is an independent candidate acceptance policy that preserves very high precision without collapsing useful coverage.**

