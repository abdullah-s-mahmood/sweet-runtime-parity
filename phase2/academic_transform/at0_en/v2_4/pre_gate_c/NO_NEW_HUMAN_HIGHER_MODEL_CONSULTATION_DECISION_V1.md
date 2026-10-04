# ACAD_PASS — No-New-Human Higher-Model Consultation Decision V1

Date: 2026-10-04
Status: ACCEPTED WITH ESSENTIAL CHANGES / PRE-EXECUTION ONLY
Repository: `abdullah-s-mahmood/sweet-runtime-parity`
Branch: `phase2-arabic-eval`

## 1. Consultation verdict

Independent higher-model verdict:

`B — YES_WITH_ESSENTIAL_CHANGES`

Interpretation:
- `Gate C-EXT + Gate C-META` may replace the custom newly-adjudicated 80-study Gate C **for the next research-progression decision only**.
- New human reviewer recruitment is **not required now**.
- The original custom 80-study Gate C remains preserved, frozen and unopened.
- The replacement must not be described as the original human-adjudicated Gate C.
- Residual human adjudication becomes:
  `DEFERRED — CONDITIONALLY REQUIRED FOR UNCOVERED CLAIMS`.

## 2. Critical methodological corrections accepted

The consultation identified and ACAD_PASS accepts these corrections:

1. `PLABA` is not automatically a PASS corpus. Only units/judgments whose human evaluation contract actually establishes the needed fidelity property are eligible.
2. `PlainFact` remains secondary unless the exact positive/negative label provenance supports the claim being measured; generated negatives are not independent human-gold negatives by default.
3. `CLEF SimpleText` may contribute only the genuinely human-annotated real-system material for external human gold. Synthetic distortion training data cannot be counted as independent human gold.
4. `QASemConsistency` is primarily a fine-grained relation-support benchmark; it does not alone establish preservation of all source claims.
5. Metamorphic testing is complementary evidence, not a substitute for absolute correctness. A reject-all system can satisfy some invariance tests.
6. Source support and source completeness are distinct constructs:
   - “everything stated is supported” !=
   - “everything that must be preserved was preserved”.
7. External tracks retain native semantics unless an exact ACAD_PASS adapter is frozen.
8. No aggregate score may compensate for a safety failure.

## 3. Independent implementation-agent verification

The implementation agent performed a fresh source check after receiving the consultation and found that the main benchmark recommendations are supported by primary/official sources:

- `FactPICO` (ACL 2024): 345 plain-language RCT summaries with fine-grained expert evaluation and natural-language rationales on PICO elements and reported findings.
- `FaReBio` (EMNLP Findings 2024): expert-annotated faithfulness and supporting evidence for biomedical plain summaries.
- `LongSciVerify` (LREC-COLING 2024): human-annotated fine-grained factual-consistency data for long scientific-document summaries.
- `CLEF SimpleText 2026`: official task documentation explicitly states that manual annotations from 2025 submissions are reused as ground truth for information-distortion classification.

These findings strengthen the external-human-gold strategy but do not remove the need for dataset-specific construct contracts.

## 4. Accepted hard-gate architecture

The replacement will use functional hard gates rather than a dataset-count vote.

### HARD GATE H1 — Scientific transformation fidelity

Must include:
- at least one direct scientific transformation dataset/unit with qualified human judgments; and
- at least one independent expert scientific factuality resource at a different granularity or construction process.

Priority candidates:
- CLEF SimpleText 2025 manually annotated real submissions;
- eligible PLABA/TREC human-faithfulness units;
- FactPICO;
- FaReBio;
- LongSciVerify.

Exact membership remains NOT READY until access, labels, licensing, overlap and adapter validity are frozen.

### HARD GATE H2 — Scientific claim/evidence fidelity

Primary:
- SciFact

Only exact claim/evidence semantics may be adapted.
No blanket rule such as SUPPORT = full-rewrite PASS.

### HARD GATE H3 — Fine-grained relation fidelity

Primary:
- QASemConsistency

Use relation-level support/hallucination semantics.
Do not reinterpret it as full-document preservation.

### HARD GATE H4 — ACAD_PASS-specific metamorphic safety

Deterministic, preregistered transformations with validity conditions.

Required families include:
- owner/value swap;
- group-label swap;
- negation flip;
- modality strengthening;
- association -> causation;
- citation-owner swap;
- equation coefficient/variable swap;
- denominator/baseline change;
- temporal/scope change;
- critical qualifier deletion;
- faithful split/merge;
- carefully constructed ambiguity/REVIEW cases.

Every metamorphic relation requires an explicit validity contract.

## 5. Diagnostic tracks

Diagnostic unless a later construct-gap audit promotes one before execution:
- DeFacto;
- USB;
- PlainFact;
- QASPER;
- FENICE;
- TRUE or AggreFact, deduplicated;
- expert-edited 2026 scientific simplification corpus;
- additional long-document tracks not already used as H1 hard evidence.

A confirmed critical safety failure found in a diagnostic track must still be reported and cannot be hidden merely because the track is diagnostic.

## 6. New benchmarks prioritized for adapter/access audit

Priority additions from consultation:
1. FactPICO — ACL 2024
2. FaReBio — EMNLP Findings 2024
3. LongSciVerify — LREC-COLING 2024

These are not automatically execution-authorized; they first undergo the same version/license/access/adapter/overlap freeze.

## 7. REVIEW strategy

Most engineered REVIEW validation may be supplied by `Gate C-META` at this stage, provided:
- the critical relation is genuinely unresolved under the allowed evidence;
- no stronger rule already implies REJECT or INVALID_VERIFICATION;
- matched resolvable controls are present to prevent reject/review-all gaming.

Do not map:
- missing evidence -> REVIEW automatically;
- annotator disagreement -> REVIEW automatically;
- truncation -> REVIEW automatically.

Natural real-world ambiguity performance remains an uncovered claim unless independently human-labeled evidence becomes available.

## 8. Global progression rule

`GO` only if **every hard gate passes its preregistered native/adapter contract** and all non-compensatory safety conditions pass.

No weighted average.

For mapped eligible cases:
- unsafe automatic acceptance = 0;
- critical silent scientific errors = 0;
- critical uncertainty promoted to automatic PASS = 0;
- critical evidence/provenance requirements = 100%.

The legacy 75% safe-acceptance / 75% decisive-reject / 90% REVIEW thresholds may be reused only where the external track has genuinely equivalent outcome semantics.

Unavailable required data -> `NOT_READY`.
Valid hard-gate failure -> `NO_GO`.

## 9. Claims boundary

If the composite later passes, permitted wording is limited to external benchmark validation of represented constructs using published human/expert judgments plus deterministic ACAD_PASS-specific metamorphic testing.

Still prohibited:
- claiming the original 80-study human Gate C was passed;
- claiming universal academic fidelity;
- claiming full-document meaning preservation unless directly tested;
- claiming production readiness or >=99% general precision;
- claiming all human references are PASS;
- treating repeated/derived datasets as independent evidence.

## 10. Current authorization

AUTHORIZED NOW:
- protocol amendment drafting;
- readiness-contract drafting;
- dataset/access/license/schema/overlap planning;
- independent pre-execution review.

NOT AUTHORIZED:
- executing external benchmarks;
- running verifier predictions on external evaluation cases;
- opening custom 80-study Gate C;
- recruiting new human reviewers;
- modifying frozen V2.4 runtime.

## 11. Exact next checkpoint

`PRE-GATE-C — EXT/META PROTOCOL AMENDMENT + PRE-EXECUTION READINESS FREEZE`

After that:
user-mediated independent review of the amendment/readiness packet before any external-suite execution.
