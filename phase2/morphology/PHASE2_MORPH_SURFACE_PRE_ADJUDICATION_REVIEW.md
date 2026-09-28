# Phase 2 — Morphology-Aware Surface Realization Gate: Pre-Adjudication Review

Date: 2026-09-28

Status: DEVELOPMENT v3 executed successfully. Surface proposals are ready for linguistic adjudication. No source corpus has been modified, no sealed benchmark has been created, and Phase 3 has not started.

## Canonical v3 execution

GitHub Actions run:
- 36453279349
- conclusion: SUCCESS

Architecture:
- CAMeL Tools 1.5.2
- CALIMA MSA r13 morphology lattice
- CAMeL MLE MSA prior
- CAMeL BERTUnfactoredDisambiguator MSA contextual morphology
- exact source-preserving realization layer
- Unicode punctuation separated from morphology core
- fathatan+terminal-alif serialization equivalence used for evaluation only

## v3 evidence

Across the 19 normalized candidates:
- morphologically analyzable: 18/19
- multiple possible source-preserving morphological surfaces: 17/19
- unique morphology surface: 1/19

This is an important falsification result: morphology generation alone does **not** solve contextual surface realization. Arabic case/mood/state ambiguity remains dominant.

For the 13 candidates touching selected Nahw targets:
- some compatible surface exists in morphology lattice: 11/13
- out-of-context MLE top-1 compatible: 7/13
- contextual BERT top-1 compatible: 10/13
- contextual BERT top-2 surface consensus compatible: 7/13
- current selected/proposed runtime surface compatible under evaluation comparator: 9/13

Contextual morphology therefore materially outperforms the word-only MLE prior on this small development population, but it is not grammatical proof.

## Development surface proposal set

The bounded gate emits:
- 9 DEVELOPMENT direct/contextual-consensus surface proposals
- 3 REVIEW surface proposals
- 7 explicit abstentions with no surface proposal

The 9 development proposals all originate from normalized candidates previously adjudicated as supported/alternative:
- supported/alternative candidate directions: 9/9
- prior wrong candidate directions: 0/9
- prior partial candidate directions: 0/9
- target-overlapping proposals: 8
- target-compatible surfaces by automated evaluator: 8/8

This is not yet a surface accuracy result because the final Unicode forms still require linguistic adjudication.

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

Some proposals contain additional explicit case/mood marks compared with the published minimally vocalized correction. Adjudication must distinguish grammatical correctness from editorial over-diacritization.

## Important implementation correction during the gate

An earlier v2 comparator incorrectly treated Arabic punctuation as morphology core and undercounted forms that differed only in the Unicode placement of fathatan relative to terminal alif.

v3 fixes:
1. Unicode-category punctuation separation.
2. Evaluation-only equivalence for common Arabic tanween-alif serializations (ًا / اً).
3. No silent source rewriting; the equivalence exists only in evaluation.

Therefore v3, not v1/v2, is the canonical morphology-surface evidence.

## Fresh research synthesis

- Arabic diacritics are morphosyntactically meaningful, and modern work explicitly separates core-word diacritics from case endings. This matches the observed surface ambiguity around nominative/accusative endings.
  - https://aclanthology.org/2024.lrec-main.128/

- A 2025 Arabic diacritization system explicitly preserves user-provided marks, supporting our invariant that correct source diacritics should remain authoritative rather than globally re-diacritizing the word.
  - https://aclanthology.org/2025.emnlp-main.846/

- Camel Morph MSA is a very large MSA analyzer/generator and provides the case/mood/number/gender/state features needed to enumerate possible surfaces; however, the observed 17/19 ambiguity shows enumeration is not selection.
  - https://aclanthology.org/2024.lrec-main.240/

- SWEET remains useful as an efficient edit candidate generator, but its text-editing architecture does not itself solve Arabic morphosyntactic surface selection.
  - https://aclanthology.org/2025.acl-long.875/

- ZAEBUC* (LREC 2026) provides a broader future Arabic GEC/morphology benchmark for independent validation after the development architecture is frozen.
  - https://aclanthology.org/2026.lrec-1.137/

## Maximum-effort brainstorming before adjudication

### Keep contextual morphology after normalized recovery
Decision: **PROTOTYPE SUCCESSFUL / KEEP**

BERT morphology improved target-surface compatibility over word-only MLE (10/13 vs 7/13 top-1 in this development slice).

### Treat morphology consensus as proof
Decision: **REJECT**

Even contextual morphology can produce a grammatically possible form that is wrong for the intended correction. Final surface adjudication remains mandatory.

### Preserve source marks outside the edited morpheme
Decision: **INTEGRATE AS INVARIANT**

This remains the strongest defense against unnecessary re-vocalization.

### Case/mood mark generation
Decision: **PROTOTYPE WITH REVIEW**

Explicitly generated case/mood endings are useful but need contextual verification.

### Automatic application before surface adjudication
Decision: **DROP**

The current labels are DEVELOPMENT proposals only.

### Add a second Arabic GEC model now
Decision: **WAIT**

The present bottleneck is surface verification, not lack of candidate generators. First determine how many of the 12 proposed surfaces survive adjudication.

### Dedicated syntactic verifier after morphology
Decision: **WATCH / LIKELY NEXT TEST**

If morphology surfaces are often linguistically plausible but contextually wrong, a dependency/syntactic or LLM verifier constrained to the local edit may be higher value than another generator.

### Strict Scientific mode
Decision: **INTEGRATE**

Morphology/normalization must remain behind protected-span and citation/technical-term firewalls.

## Next required gate

Adjudicate the 12 explicit surface proposals and audit the 7 abstentions.

Primary questions:
1. How many of the 9 development direct/contextual-consensus proposals are actually correct Unicode surface realizations?
2. Are extra case/mood marks correct, merely over-diacritized, or harmful?
3. Do any of the 3 REVIEW proposals deserve promotion?
4. Did any of the 7 abstentions miss a surface that the morphology lattice already contained?
5. Can a deployable acceptance policy be expressed without Nahw gold or prior human candidate labels?

Only after this adjudication should the architecture decide whether to:
- implement a constrained surface verifier,
- test CAMeL contextual morphology as a soft/ranking feature,
- or move to a second Arabic GEC generator.
