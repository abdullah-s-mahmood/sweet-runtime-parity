# ACAD_PASS — SURUS Admission Higher-Model Review Packet V1

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `at0-en-v2.6-dev`

Review state:
`MANDATORY_INDEPENDENT_REVIEW_BEFORE_ANY_SURUS_PROTOCOL_ADMISSION`

This packet is advisory/review material only. It does not authorize training or a protocol amendment.

## 1. Decision to be reviewed

Determine whether SURUS should be admitted into the already-frozen ACAD_PASS public-human-gold federation as an additional native fine-grained auxiliary human-gold source for D2-D4.

Possible verdicts:
1. `REJECT_SURUS_ADMISSION`
2. `PROCEED_SURUS_ADMISSION_WITH_CHANGES`
3. `PROCEED_SURUS_ADMISSION_AS_SPECIFIED`

No other adaptive arm is allowed.

## 2. Current frozen scientific boundary

No successor federation model has been fit.

Current development campaign:
- D0: BiomedBERT + linear 9-way BIO native-only
- D1: BiomedBERT + four-channel span head native-only
- D2: BiomedBERT BIO + human auxiliary heads
- D3: BiomedBERT span + human auxiliary heads
- D4: BioClinical ModernBERT span + human auxiliary heads
- D5: prospectively canceled without replacement after official DISTANT-CTO source failed its semantic-type admission condition

Current fit budget:
`45 = 5 arms * 3 folds * 3 seeds`

No seventh arm.
No seed sweep.
No threshold shopping.
No VERIFY_INTERNAL access.
No AD/COVID external benchmark scoring during development.

Current process readiness:
- F01-F06 closure = 94.5%
- first-fit readiness = 89.7%

Latest actual scientific model result remains frozen/consumed R44C.

## 3. Existing frozen auxiliary architecture

Current human auxiliary sources:
- original EBM-NLP P/I/O: 3 channels
- TrialSieve: 20 released native types
- EvidenceOutcomes: native outcome type/scope
- PICO-Corpus: 26 released native BRAT types

Missing annotation in one source is not treated as a native negative.
Auxiliary heads are discarded at native P/I/C/O inference.

Frozen loss:
`L = L_native + 0.25 * L_aux`

Current implementation computes source-level auxiliary losses and then:
`L_aux = mean(source_auxiliary_losses)`

Therefore with four existing auxiliary source heads each source contributes 1/4 of the source-mean before the fixed 0.25 multiplier.

Adding SURUS as a fifth source without another rule would change every old source's share from 1/4 to 1/5 of `L_aux`.

This is a material protocol consequence and MUST be prospectively resolved. No loss-weight sweep is permitted.

## 4. SURUS durable source evidence

Pinned source:
`surus-ai/dataset@3a61790d5c304dea95fb278f76cc3b1a0ca07564`

Repository license:
`CC-BY-NC-4.0`

Schema audit:
- run `37900075427`: SUCCESS
- artifact `11602016518`
- digest `sha256:0549f36abf6d1cac39d87dec2206514c7a5a59a8ba2ca083d89c54d53ff26772`
- article rows: 523
- unique PMIDs: 523
- annotation rows: 48,833
- in-domain: 400
- indication OOD: 90
- study-type OOD: 33
- labels: 25
- label classes: 7
- missing article foreign keys: 0
- missing label foreign keys: 0
- invalid coordinate rows: 0
- raw text emitted by audit: false
- scientific metric computed by audit: false

Evidence freeze:
`AT0_EN_V26_SURUS_AUXILIARY_ADMISSION_EVIDENCE_FREEZE_V1.md`
commit `be5a2ee8cf66cec5d86d878aa9b5a558f78552cc`.

## 5. Human-gold quality evidence

Peer-reviewed source:
Peeters C, et al.
"Evaluation of SURUS: a named entity recognition NLP system to extract knowledge from interventional study records."
BMC Medical Research Methodology. 2025;25:184.
DOI: 10.1186/s12874-025-02624-z.
PMID: 40745274.

Relevant evidence:
- manual annotation;
- fine-grained 25-label ontology;
- 400 in-domain abstracts;
- 123 separately sampled out-of-domain abstracts;
- primary annotators had pharmaceutical/biomedical background;
- all annotations were reviewed by one of two expert annotators;
- detailed manual, training and consensus procedures;
- reported inter-annotator Cohen kappa 0.81;
- reported inter-annotator F1 0.88;
- reported model weighted F1 0.95 on the source task.

Scientific classification for ACAD_PASS:
`EXPERT_REVIEWED_HUMAN_GOLD`

Do NOT treat the reported SURUS model F1 as directly comparable to ACAD_PASS strict exact native P/I/C/O because task, ontology, split/training regime and output space differ.

## 6. Provenance / overlap custody

Run:
`37900288357` SUCCESS

Artifact:
`11602601668`

Digest:
`sha256:915be5e4fd758b90b959eae4700c774b441dda19f358310165ccfcd6a6517a5e`

SURUS exact-PMID overlaps:
- mapped DESIGN: 0
- mapped VERIFY_INTERNAL: 0
- mapped OLD_SELECT: 0
- resolved AD whole/test: 0 / 0
- resolved COVID-19 whole/test: 0 / 0
- EvidenceOutcomes: 7
- PICO-Corpus: 2
- TrialSieve train/validation: 1

In-domain SURUS exact-PMID overlaps:
- EvidenceOutcomes: 6
- PICO-Corpus: 2
- TrialSieve train/validation: 0
- mapped protected historical sets: 0

OOD SURUS exact-PMID overlaps:
- EvidenceOutcomes: 1
- PICO-Corpus: 0
- TrialSieve train/validation: 1
- mapped protected historical sets: 0

Limitations:
- PMID equality is not full trial-family identity.
- AD/COVID title-to-PMID resolution is incomplete.
- historical EBM identity mapping is incomplete.
- any SURUS admission still requires deterministic per-fold family decontamination.

## 7. Relevant external evidence on multi-source BioNER

The review must actively consider disconfirming evidence, not assume that adding more human-gold data helps.

Recent/relevant findings include:

1. Ruano et al., BioNLP 2025, "Effective Multi-Task Learning for Biomedical Named Entity Recognition":
multi-dataset biomedical NER can improve cross-domain generalization when missing annotations are handled explicitly rather than treated as negatives.

2. Yin et al., Journal of Biomedical Informatics 2024, "Augmenting biomedical named entity recognition with general-domain resources":
multi-task auxiliary data can help, but the authors explicitly note that multi-BioNER training is not consistently beneficial and can create label ambiguity; their staged target-specific fine-tuning was used to mitigate this.

3. Earlier multi-dataset BioNER ablation over 22 datasets found multitask learning generally did not improve performance, though it could match single-task models and aid low-data transfer.

4. Multiple-auxiliary NER work has shown that auxiliary datasets can help, but source composition/training strategy matters.

Implication:
SURUS must be admitted only if its information value outweighs negative transfer, ontology conflict and altered loss composition under a frozen prospective rule.

## 8. Critical ontology constraint

SURUS must NOT be mechanically collapsed into ACAD_PASS native P/I/C/O.

If admitted, the default safe representation is a separate auxiliary span head over the released fine-grained label identity.

Because some human-readable label names can recur under different label classes, the identity MUST be keyed by immutable released label ID or an equivalently collision-free `class::name` key, not label name alone.

No SURUS auxiliary head may be used at native P/I/C/O inference.

## 9. Candidate partition policy for adversarial review

Preliminary proposal ONLY; not authorized:

- use the 400 in-domain abstracts as the candidate SURUS auxiliary training pool;
- reserve all 123 original OOD abstracts (90 indication-OOD + 33 study-type-OOD) as untouched SURUS-specific auxiliary generalization evidence;
- do not use OOD labels for development selection, thresholding, source weighting, architecture choice or stopping;
- perform per-fold family decontamination before any training;
- deterministically remove any SURUS family colliding with native development/evaluation custody or another auxiliary source according to one prespecified precedence rule;
- emit only counts/hashes during custody audits, not protected identities.

Reason:
the original SURUS paper used the 400 in-domain set for 10-fold evaluation and the 123 OOD sets as cross-domain evaluation. Reserving the OOD data would preserve a stronger generalization check than consuming all 523 as training.

The independent reviewer MUST challenge this proposal and may reject it.

## 10. Loss-weighting problem that MUST be resolved

Current:
`L = L_native + 0.25 * mean(L_EBM, L_TrialSieve, L_EvidenceOutcomes, L_PICO)`

Naive SURUS addition would become:
`L = L_native + 0.25 * mean(L_EBM, L_TrialSieve, L_EvidenceOutcomes, L_PICO, L_SURUS)`

Consequences:
- SURUS receives 20% of auxiliary source weight;
- each existing auxiliary source drops from 25% to 20% of auxiliary source weight;
- any performance change then reflects BOTH additional information and changed source mixture.

The independent reviewer must specify ONE prospectively frozen mathematical rule.

Candidate families to assess:
A. equal-source mean over all five sources;
B. preserve the original four-source aggregate as one block and assign a fixed prespecified fraction of the existing 0.25 auxiliary budget to SURUS;
C. reject SURUS to preserve the already-frozen four-source loss exactly;
D. another single fixed rule justified from first principles and prior literature.

Forbidden:
- coefficient sweep;
- source-weight tuning on development outcomes;
- GradNorm/uncertainty/dynamic weighting introduced adaptively unless the entire campaign protocol is prospectively redesigned and independently justified;
- choosing a weighting rule after seeing comparative scientific fit results.

## 11. Fair-comparison constraint

If SURUS is added:
- D2, D3 and D4 would receive it because these are human-auxiliary arms;
- D0 and D1 must remain native-only by design;
- the interpretation of D2-vs-D0 and D3-vs-D1 becomes "human federation including SURUS" versus native-only, not a pure reproduction of the already-frozen four-source federation;
- no additional SURUS-specific arm may be created unless a new, independently reviewed campaign replaces the current protocol before any fit.

The reviewer must decide whether this remains a scientifically fair and sufficiently interpretable first campaign.

## 12. Fit-budget / manifest constraint

If SURUS is admitted before any successor scientific fit:
- retain the 45-fit ceiling unless the independent reviewer demonstrates that doing so is invalid;
- no seventh arm;
- all source/admission/decontamination manifests must be regenerated/rebound BEFORE first optimizer update;
- the 45 scientific attempt slots must bind the amended data/runtime/protocol hashes;
- previous implementation-only preflights do not consume scientific attempts;
- no fit occurs until the amended architecture/data preflight PASSes.

## 13. License / dissemination constraint

The pinned SURUS dataset repository is CC-BY-NC-4.0.

Any admission decision must:
- preserve attribution;
- treat the source as non-commercial under that license;
- avoid bundling/redistributing raw SURUS content in ACAD_PASS artifacts unless explicitly permitted;
- publish hashes, provenance and derived aggregate audit evidence where possible instead of third-party raw data.

The reviewer should flag any additional license issue but should not make unsupported legal conclusions.

## 14. Exact questions for the independent reviewer

Answer each explicitly:

1. Is SURUS scientifically worth admitting into D2-D4 before the first fit?
2. Does its expected information gain justify reopening the frozen auxiliary-source matrix?
3. Should the 400 in-domain / 123 OOD partition proposal be accepted, changed or rejected?
4. Is 123-OOD reservation scientifically stronger than training on all 523 for this campaign?
5. What exact deterministic family-decontamination precedence should be used for the 7 EvidenceOutcomes, 2 PICO-Corpus, 1 TrialSieve PMID overlaps and any newly discovered family aliases?
6. Should ontology identity use released label ID, `class::name`, or another collision-free representation?
7. What exact fixed mathematical definition of `L_aux` should be used after SURUS admission?
8. Would that weighting preserve interpretability/fairness of D2/D3/D4 versus D0/D1?
9. Should the 45-fit ceiling remain unchanged?
10. Which exact preflights/manifests must be redone before first fit?
11. What evidence must remain sealed?
12. What claim boundary should apply to SURUS-related results?
13. What evidence would falsify the hypothesis that SURUS is useful?
14. Is rejection of SURUS scientifically preferable because the current protocol is already near-complete?
15. Are there stronger public human-gold corpora published/updated through 2026 that should be considered instead or alongside SURUS BEFORE changing the protocol?

## 15. Required review behavior

The independent reviewer MUST perform:
- Deep Research;
- Adversarial Review;
- Genuine Brainstorming;
- Alternative Hypotheses;
- Failure Analysis;
- Disconfirming Evidence Search;
- implementation-aware review, not papers alone;
- explicit degrees-of-freedom audit;
- publication/claim-validity audit.

Do not optimize for agreement with the preliminary proposal.

## 16. Required output

Return:

1. `VERDICT`: REJECT / PROCEED_WITH_CHANGES / PROCEED_AS_SPECIFIED.
2. Strongest arguments FOR admission.
3. Strongest arguments AGAINST admission.
4. Hidden failure modes / leakage / negative-transfer risks.
5. Exact accepted SURUS partition policy.
6. Exact admitted ontology and head definition.
7. Exact fixed `L_aux` equation.
8. Exact per-fold decontamination rule.
9. Exact fit budget and attempt-manifest consequence.
10. Required new preflights before optimizer update.
11. What remains sealed.
12. Claim boundaries.
13. Falsification criteria.
14. Whether a different corpus or design is superior.
15. Final GO/NO-GO for protocol amendment.
16. Exact next operation after the review.

## 17. Copy-ready higher-model prompt

Continue ACAD_PASS as an independent multidisciplinary scientific review board. Do NOT train anything and do NOT open protected benchmarks.

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`

Branch:
`at0-en-v2.6-dev`

Read first:
1. `ACAD_PASS_LATEST_STATE.md`
2. `ACAD_PASS_CHAT_HANDOFF.md`
3. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_FEDERATION_PROGRESS_SNAPSHOT_V4.md`
4. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_AUXILIARY_ADMISSION_EVIDENCE_FREEZE_V1.md`
5. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_SURUS_ADMISSION_HIGHER_MODEL_REVIEW_PACKET_V1.md`
6. `phase2/academic_transform/at0_en/v2_6/AT0_EN_V26_PUBLIC_HUMAN_GOLD_FEDERATION_PROTOCOL_V1.md`
7. `phase2/academic_transform/at0_en/v2_6/federation_architecture_preflight.py`

Perform Deep Research, Adversarial Review, Genuine Brainstorming, Alternative Hypotheses, Failure Analysis, Disconfirming Evidence Search, implementation-aware review, and a degrees-of-freedom audit.

The specific decision is whether SURUS should be prospectively admitted as an additional fine-grained auxiliary human-gold source in D2-D4 BEFORE any first federation scientific fit. The existing campaign is already frozen at D0-D4 / 45 fits after D5 cancellation. Current loss is `L_native + 0.25 * mean(four source-level auxiliary losses)`; therefore a naive fifth-source addition changes the old sources' relative auxiliary weights and is a material protocol change.

Do not assume more human-gold data is automatically better. Search the strongest relevant literature and implementations through 2026, including evidence for negative transfer and source/task weighting.

You MUST explicitly decide:
- admit or reject SURUS;
- 400 in-domain train-candidate vs 123 OOD sealed generalization policy;
- exact per-fold family decontamination;
- exact collision-free ontology identity;
- exact fixed mathematical `L_aux` after any admission;
- comparison fairness;
- whether the 45-fit budget remains valid;
- exact preflights/manifests that must be rebound;
- claim boundaries;
- falsification criteria;
- whether another public human-gold corpus/design is superior.

Preserve all existing scientific exposure constraints. VERIFY_INTERNAL stays CLOSED. AD/COVID external benchmark scoring stays CLOSED. R44C stays consumed. No threshold/seed/loss sweep. No seventh adaptive arm.

Output exactly the 16 review items specified in Section 16 of the review packet and give a final GO/NO-GO for the protocol amendment.
