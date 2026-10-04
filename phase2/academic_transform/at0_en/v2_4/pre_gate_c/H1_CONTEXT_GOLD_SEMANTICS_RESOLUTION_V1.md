# ACAD_PASS — H1 Context + Gold-Semantics Resolution V1

Date: 2026-10-04
Status: RESOLVED AT DESIGN LEVEL / FACTPICO ARTIFACT FREEZE REQUIRED / NO V2.4 EXECUTION

Parent:
- H1_CONTRACT_V3_INDEPENDENT_REVIEW_DECISION_V1.md
- GATE_C_EXT_META_PROTOCOL_AMENDMENT_V2.md

## 1. Problem being resolved

H1 Contract V3 was blocked because PLABA's sentence-level expert judgments are not automatically equivalent to ACAD_PASS strict protected-content preservation.

Two independent incompatibilities were verified:

1. PLABA annotators/judges may rely on broader abstract context.
2. PLABA adaptation policy intentionally permits omission/generalization of some source details.

Frozen V2.4 has no separate non-protected context channel.

Therefore a PLABA-only hard H1 preservation gate would overstate construct equivalence.

## 2. Primary-source PLABA context findings

Official PLABA/TREC 2024 and retrospective publications establish:

- output is sentence-aligned;
- each source sentence maps to one target cell, possibly containing multiple target sentences;
- source sentences may not be merged;
- output for a source sentence should not contain information from other source sentences;
- the whole rewritten abstract is nevertheless expected to read fluently as a document;
- PLABA explicitly recognizes the importance of document context.

Official annotation guidelines further permit:
- carrying already understandable text over unchanged;
- ignoring source sentences not relevant to consumer understanding;
- resolving pronouns/anaphora using the previous source sentence;
- omitting confidence intervals, p-values and similar measurements;
- using context or outside publication information to interpret ambiguous jargon;
- explaining named entities/jargon with added explanatory text.

Conclusion:

`PLABA SAFE/ACC/COM GOLD IS TASK-VALID BUT NOT IDENTICAL TO ACAD_PASS STRICT-PRESERVATION GOLD`

## 3. Why a surface-filtered PLABA hard subset is rejected

A possible rescue would be to keep only sentences that appear:
- non-anaphoric;
- non-quantitative;
- non-omissible;
- context-independent.

This is rejected as the primary hard solution because:
- surface rules cannot prove annotator context independence;
- PLABA's permissibility of omission is semantic/task-dependent;
- filtering by patterns risks construct cherry-picking;
- filtering by V2.4 extractor capability would be circular;
- no published PLABA field directly marks “ACAD_PASS-strict-preservation eligible”.

Therefore:

`NO HARD PLABA SUBSET WILL BE CREATED BY POST-HOC SEMANTIC/SURFACE FILTERING`

before prediction.

## 4. Revised role of PLABA

PLABA remains valuable because it provides:
- authentic biomedical plain-language transformations;
- expert accuracy/completeness judgments;
- broad system diversity;
- large source coverage.

But its preferred role is narrowed to:

### PLABA-H1-DIAGNOSTIC / TRANSFORMATION-UTILITY

Allowed uses:
- external human agreement diagnostics;
- identity-control diagnostics;
- authentic transformation acceptance/abstention analysis;
- native ACC/COM cross-tabs;
- sentence-level limited-context behavior.

Not allowed from PLABA alone:
- universal strict-preservation PASS gold;
- claim that all omitted scientific details should have been preserved;
- full ACAD_PASS H1 hard-pass equivalence.

PLABA remains a scientifically important secondary H1 track, not discarded.

## 5. Smallest stronger hard-H1 companion: FactPICO

Resource:
`FactPICO: Factuality Evaluation for Plain Language Summarization of Medical Evidence`

ACL 2024:
`10.18653/v1/2024.acl-long.459`

Official repository:
`lilywchen/FactPICO`

Observed repository main HEAD:
`2e16993a000aedb15cb348b7bcd61070d26bab14`

Repository license:
`MIT`

Dataset download route:
official repository points to a UT Austin Box artifact.

Dataset bytes/license terms for the separately hosted data are NOT yet frozen.

## 6. Why FactPICO closes the specific H1 gap better

FactPICO evaluates whole plain-language summaries against whole RCT abstracts.

This matches frozen V2.4's existing interface better:
- source can be the full RCT abstract;
- candidate can be the full plain-language summary;
- no separate hidden/non-obligatory context channel is required.

Expert annotation evaluates critical RCT elements:

- Population
- Intervention
- Comparator
- Outcome

and evidence-inference / reported findings.

PICO rating semantics:
- 4: mentioned and described accurately;
- 3: mentioned but somewhat inaccurate or vague;
- 2: severe inaccuracies and/or missing critical descriptors;
- 1: missing.

Evidence-inference rating similarly distinguishes:
- accurate;
- vague/slightly inaccurate;
- inaccurate;
- not mentioned.

FactPICO also annotates:
- added information spans;
- correctness of added information;
- free-text expert rationales.

Thus it directly exposes both H1 functions at a critical scientific-content level:

### H1-S — support/factuality
covered by:
- PICO factuality;
- evidence-inference factuality;
- added-information correctness.

### H1-C — preservation/completeness
covered by:
- “missing” PICO elements;
- “missing critical descriptors”;
- evidence-inference “not mentioned”;
- documented overgeneralization/omission of critical RCT elements.

This is not full-document exhaustive preservation.
It is:
`CRITICAL RCT-ELEMENT FIDELITY/PRESERVATION`

which is a defensible narrow H1 hard claim.

## 7. Expert provenance

FactPICO contains:
- 115 RCT abstracts;
- 345 plain-language summaries;
- outputs from three LLMs.

Annotation:
- two fifth-year medical students with relevant annotation experience;
- 75 summaries were doubly annotated;
- 60 of those involved discussion to resolve conceptual PICO differences;
- 15 were independently evaluated for held-out agreement;
- evidence-inference and added-information questions on the 75 double-annotated texts were not resolved through discussion.

Reported agreement is moderate-to-high and must be preserved in future interpretation.

No new human recruitment is required.

## 8. H1 architecture after resolution

Preferred hard H1 design:

### H1-HARD — FactPICO critical scientific transformation fidelity

Purpose:
test whether frozen V2.4:
- automatically accepts expert-supported critical scientific transformations;
- rejects/abstains on critical omissions/inaccuracies/additions;
- preserves PICO/findings at whole-abstract context.

Exact hard mappings/thresholds are NOT yet frozen.

### H1-PLABA — diagnostic / authentic-transformation utility

Purpose:
measure behavior on large authentic sentence-aligned biomedical simplifications under PLABA's native human judgment semantics.

PLABA does NOT determine full H1 PASS alone.

### Optional completeness diagnostic
`InfoLossQA`

ACL 2024:
1,000 linguist-curated QA pairs from 104 LLM simplifications of medical study abstracts.

Potential role:
information-loss characterization.

Default:
`DIAGNOSTIC ONLY`

Reason:
its QA representation is not automatically an exact V2.4 PASS/REJECT oracle and would otherwise require semantic adapter logic.

### Other resources
- FaReBio: conditional/diagnostic H1-S corroboration;
- SimpleText: optional transformation/diversity evidence;
- LongSciVerify: diagnostic long-scientific consistency.

No benchmark is added merely to increase count.

## 9. Construct sufficiency decision

For the next H1 hard-gate design:

`FACTPICO IS THE MINIMUM REQUIRED REPLACEMENT/COMPANION RESOURCE`

PLABA remains secondary.

This decision is made because FactPICO directly closes the verified mismatch:
- whole-source context;
- expert critical-element preservation;
- explicit missing/inaccurate categories;
- added-information factuality.

InfoLossQA/FaReBio are not mandatory at this stage.

## 10. Claim boundary

A future combined H1 pass may support only a claim of the form:

“Frozen AT0-EN V2.4 met preregistered external-human/expert research-progression criteria for critical biomedical scientific-content fidelity on FactPICO, with complementary authentic-transformation diagnostics on PLABA.”

It must NOT imply:
- universal academic-domain preservation;
- exhaustive preservation of every fact;
- production readiness;
- human-level writing quality;
- external medical truth verification;
- natural deployment prevalence.

## 11. Current readiness

H1 context/gold semantics:
`RESOLVED AT DESIGN LEVEL`

PLABA-only hard H1:
`REJECTED`

FactPICO hard-H1 candidacy:
`ACCEPTED FOR ARTIFACT/SCHEMA FREEZE`

FactPICO dataset bytes:
`NOT YET FROZEN`

FactPICO exact data license:
`NOT YET VERIFIED SEPARATELY FROM REPOSITORY MIT LICENSE`

FactPICO adapter/metric contract:
`NOT READY`

V2.4 external prediction:
`NOT AUTHORIZED`

## 12. Exact next checkpoint

`FACTPICO ARTIFACT + SCHEMA + LICENSE FREEZE`

Tasks:
1. obtain/freeze exact FactPICO data artifact;
2. compute hashes;
3. inspect exact source/summary/annotation schema;
4. verify annotation counts and provenance;
5. freeze data-license/reuse terms;
6. map dataset records to source abstracts/PubMed identifiers;
7. audit overlap with other H1/H2/H3 resources;
8. only then draft H1 Contract V4.

Still prohibited:
- V2.4 external predictions;
- H1 scoring;
- V2.4 modification;
- new-human recruitment;
- original custom Gate C opening;
- Arabic-track work.
