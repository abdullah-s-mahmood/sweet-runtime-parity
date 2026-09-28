# Phase 2 — Morphology-Aware Surface Realization Gate: Result Review

Date: 2026-09-28

Status: DEVELOPMENT GATE COMPLETED. Not sealed. No production auto-application policy is frozen. Phase 3 not started.

## Canonical execution reviewed

Canonical successful workflow:
- Phase 2 Morphology-Aware Surface Gate
- run: 36453279349
- conclusion: SUCCESS

Runtime:
- camel_tools 1.5.2
- morphology DB: calima-msa-r13
- MLE MSA disambiguator
- contextual CAMeL BERTUnfactoredDisambiguator MSA

Inputs:
- 19 adjudicated normalized candidates
- 14 passages
- 13 candidates overlap published Nahw targets

No source corpus was modified.

## Main morphology result

Of 19 normalized candidates:
- 18/19 were morphologically analyzable
- 17/19 still had multiple source-preserving morphology surfaces
- only 1/19 had a unique morphology surface before contextual ranking

For 13 target-overlapping candidates:
- a compatible form existed somewhere in the morphology lattice for 11/13
- MLE top-1 matched the published target surface for 7/13
- contextual BERT top-1 matched for 10/13
- contextual BERT top-2 surface consensus matched for 7/13
- the bounded development gate produced a target-compatible runtime surface for 9/13

This establishes that contextual morphology is materially more useful than an out-of-context morphology prior for surface realization on this small development population.

## Development surface proposals

The bounded gate emitted 9 development surface proposals:
- 9 supported/alternative according to the prior candidate adjudication
- 0 partial
- 0 wrong
- 0 unnecessary
- 8 overlap a published target and are target-compatible
- 1 is a supported collateral correction without a local published target

Examples include:
- إشتدادًا، → اشتدادًا،
- نَفْس → نَفْساً
- إستشعِر → استشعِر
- خَطر → خَطراً
- يقدِّموا → يقدِّمونَ
- المصريِّين → المصريُّونَ
- الإرهابيُّون → الإرهابيِّينَ
- حبًّ → حبّاً
- يرضَ → يرضَى

The runtime proposals preserve unaffected source marks and introduce morphology-derived marks only in the edit neighborhood.

## Critical limitation: this is NOT yet a deployable acceptor

The current surface gate is explicitly bounded by the **previous candidate adjudication class**. In other words, it is testing:

> “If a normalized candidate is already known to be linguistically supported, can morphology realize it safely?”

It is **not** yet testing:

> “Can the runtime independently know that the candidate is supported?”

Therefore the observed 9/9 supported development proposals and 0 wrong proposals must not be reported as production precision.

This is the most important architectural limitation after this gate.

## Gold-independent morphology signals

Looking at morphology signals without using the prior candidate label:

### Direct local patch
- candidates with direct patch: 2
- supported: 2
- wrong: 0

This is the cleanest independent surface mechanism, but it has very low coverage.

### Contextual BERT top-2 surface consensus
- candidates with consensus: 9
- supported: 7
- partial: 1
- wrong: 1

The known wrong defective-noun candidate:
- وساعٍ → وساعا
also receives BERT top-2 surface consensus.

Therefore morphology consensus **cannot serve as an independent correctness verifier**.

### Contextual BERT top-1
Available for 18/19 candidates:
- 12 supported
- 4 partial
- 1 wrong
- 1 unnecessary

This is useful as a surface ranker, not as a correction acceptor.

## Known wrong candidate is not repaired by morphology

NORM-38-24-0:
- source: وساعٍ
- normalized candidate: وساعا
- correct published form: وساعيًا
- CAMeL morphology analyzes/ranks وساعا as a possible proper-noun-like form
- contextual BERT top-2 agrees on وساعا

This falsifies a tempting assumption:

**Morphological analyzability or morphology-model consensus is not proof that the upstream correction direction is grammatically correct in context.**

A separate correction-quality verifier is still necessary.

## Partial candidates show the opposite opportunity

Morphology can improve some incomplete normalized candidates even when the normalized candidate itself was only partial.

Example:
- كريمًا → normalized كريم
- contextual BERT top-1 proposes كريمٌ
- morphology lattice contains exactly one target-compatible source-preserving surface

Likewise:
- واقعًا → normalized واقع
- BERT top-1/top-2 can produce واقِعٌ / related nominative realization compatible with the needed case direction

These cases show that morphology is valuable as a **surface completion/ranking layer**, but only after candidate correctness has been independently established.

## Fresh end-of-gate research

### Morphological generation is not reducible to tokenizer alignment

LREC 2026 reports that morphological alignment of tokenizers is neither necessary nor sufficient for productive Arabic root-pattern generation. This matches our current evidence: normalization solved tokenizer [UNK], but morphology and contextual grammatical correctness remained separate problems.
- https://aclanthology.org/2026.lrec-1.923/

### Case endings and vowel ambiguity remain major bottlenecks

Recent Arabic diacritization shared-task analyses continue to report case endings and vowel ambiguity as major error sources. This supports explicit abstention rather than deterministic tanween/case heuristics.
- https://aclanthology.org/2026.osact-1.28/

### Morphologically informed diacritization remains appropriate

LREC-COLING 2024 distinguishes core-word diacritics and case endings and shows that morphological information can support both.
- https://aclanthology.org/2024.lrec-main.128/

### User/source-specified mark preservation is supported by current research

EMNLP 2025 reports a diacritization model that can preserve user-specified diacritics while maintaining accuracy. This aligns directly with our source-authority invariant.
- https://aclanthology.org/2025.emnlp-main.846/

### CAMeL Morph remains valuable as an enumerator/generator

Camel Morph MSA is a large-scale open-source analyzer/generator with very broad inflectional coverage, but its existence does not solve contextual correction selection.
- https://aclanthology.org/2024.lrec-main.240/

## Maximum-effort architecture brainstorming

### 1. Morphology-aware surface realization
Decision: **INTEGRATE as a surface layer**

The gate clearly improves full Unicode realization for supported candidates.

### 2. Contextual BERT morphology as a correctness verifier
Decision: **DROP**

It ranks surfaces well but accepts the known wrong وساعا candidate. Use it only for ranking alternative surfaces after candidate acceptance.

### 3. Direct source-local patch
Decision: **INTEGRATE for a narrow safe class**

When:
- candidate correction is independently accepted;
- replacement does not cross diacritic boundaries;
- unaffected bytes remain identical.

### 4. Independent correction-quality verifier
Decision: **PROTOTYPE NEXT — highest priority**

This is now the missing production component.

It must decide whether a normalized candidate itself is linguistically justified **without using Nahw gold or prior human adjudication**.

Candidate evidence may include:
- SWEET edit type and confidence
- source context
- GED as soft evidence
- morphology features
- agreement/case/mood consistency
- deterministic Arabic grammar constraints where strong
- second independent Arabic GEC candidate
- semantic/fidelity safety checks

### 5. Morphology + candidate-consensus only
Decision: **REJECT as sole acceptor**

The wrong defective-noun form already survives morphology consensus.

### 6. Deterministic morphology constraints
Decision: **PROTOTYPE**

Especially:
- defective noun reconstruction
- sound masculine plural case suffixes
- five-verbs mood/nun retention
- hamzat al-wasl/qat
- tanween + terminal alif serialization

These should be validators, not broad rewrite rules.

### 7. Second Arabic GEC candidate generator
Decision: **TEST NEXT OR IN PARALLEL WITH VERIFIER**

Now it becomes more valuable: a second independent candidate source can provide agreement/disagreement evidence for acceptance, not merely more corrections.

AraT5/AraBART-family models remain suitable candidates based on Arabic GEC literature.

### 8. Multi-model edit selection
Decision: **PROTOTYPE after second generator is available**

Agreement across independently trained models plus morphology/safety constraints may be a stronger acceptance signal than confidence from one model.

### 9. Strict Scientific mode
Decision: **INTEGRATE**

Even a morphologically valid correction should not bypass protected spans, citation integrity, numeric/technical locks, or semantic verification.

### 10. Automatic full rediacritization
Decision: **DROP**

The product objective is minimal source-preserving correction, not global vocalization.

## What improved

- morphology lattice contains target-compatible forms for 11/13 target-overlapping normalized candidates;
- contextual BERT top-1 improves surface selection from MLE 7/13 to 10/13;
- the bounded realization gate can produce 9 supported development surface proposals;
- previously ambiguous case/mood/tanween forms can now often be realized as full Arabic surfaces;
- exact source-preservation architecture remains intact.

## What worsened / became clearer

- 17/19 morphology lattices remain ambiguous;
- morphology consensus alone accepts the known wrong وساعا candidate;
- the current 0-wrong development proposal result depends on prior candidate adjudication and therefore is not deployable evidence;
- one normalized candidate remains unanalyzable;
- the missing bottleneck is now **independent candidate acceptance**, not surface realization.

## Current interpretation

The project has progressed through four distinct bottlenecks:

1. raw renderer corruption → solved by source-preserving surgical rendering;
2. wrong/over-broad edits → strongly reduced by operation-aware selectivity;
3. tokenizer [UNK] coverage → partially recovered by reversible normalization;
4. Arabic surface realization → substantially improved by morphology/contextual ranking.

The next bottleneck is:

**Can the system independently decide whether a proposed correction is actually right before the morphology layer realizes it?**

## Next bounded gate

Before any sealed benchmark:

**Phase 2 — Independent Candidate Acceptance Gate**

Do not freeze morphology auto-application yet.

Use the existing development candidates and surface proposals. Evaluate gold-independent acceptance strategies, including:
- deterministic high-confidence grammar validators;
- morphology consistency;
- GED as a soft feature;
- second Arabic GEC generator agreement;
- source-fidelity / scientific locks;
- explicit abstention.

Primary success criterion:
- materially reduce wrong/partial/unnecessary candidate acceptance while retaining useful supported coverage;
- no use of prior adjudication labels or Nahw targets in runtime decisions.

Only after an independent acceptance rule is frozen should the architecture be evaluated on a new sealed Arabic set.
