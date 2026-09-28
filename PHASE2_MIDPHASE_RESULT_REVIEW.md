# Phase 2 Arabic Correction — Mid-Phase Result Review

Date: 2026-09-28

This is a DEVELOPMENT review, not a sealed result and not a Phase 2 final decision.

## Canonical execution

Latest canonical development run:
- GitHub Actions run: 36412018852
- branch: phase2-arabic-eval
- head commit: 9295634cbb1ad4be6911e433f883bf5e4b28e98c
- official Python/PyTorch/Transformers SWEET runtime: PASS
- transfer integrity: 150 targets / 41 passage clusters / 12 NON_HUMAN_GOLD scientific stress cases / 59 sealed passage IDs excluded

## What improved

The project moved from unknown real Arabic correction quality to measured official-runtime evidence.

On the 150 one-target Nahw development items:
- NoPnx iteration 1 recovered 29/150 = 19.33%.
- NoPnx iteration 2 recovered 29/150 = 19.33%.
- Full NoPnx×2→Pnx recovered 29/150 = 19.33%.
- Pnx-only recovered 3/150 = 2.00%.
- Narrow deterministic baseline had changed 0/150 in the earlier Work run.

Passage-clustered bootstrap 95% intervals:
- NoPnx iteration 1: 14.00%–24.83%
- NoPnx iteration 2: 13.82%–25.00%
- Full: 14.09%–24.34%
- Pnx-only: 0.00%–4.55%

The second NoPnx pass gained one target and lost one target: net zero recovery gain.
The Pnx stage added zero target gains and zero target losses over NoPnx×2 on this Nahw target metric.

## What worsened / newly exposed risks

The raw official-output path is substantially less fidelity-preserving than was apparent from the earlier single-sentence parity test.

Passage-level activity:
- NoPnx iteration 1 changed 41/41 passages.
- Pnx-only changed 41/41 passages.
- Pnx-only produced only 24 non-K edit labels across the 41 passages, yet 29 passages changed despite zero non-K labels.
- In the full pipeline Pnx changed 25/41 passage outputs; 14 of those changed despite zero non-K labels.
- NoPnx also showed a smaller version of this issue.

Cause confirmed in the pinned official source: gec.tag.rewrite reconstructs the full subword sequence and detokenize_sent returns a space-joined string. Therefore output reconstruction can normalize surface spacing even when the model predicts no actual edit. The earlier six punctuation sanity cases simply did not expose this broader behavior.

This means the official SWEET renderer is valid for reproducing the published model pipeline, but it is not automatically suitable as a Strict-Fidelity document renderer.

## Scientific stress evidence

The 12 scientific cases are project-authored NON_HUMAN_GOLD fidelity stress cases and do not enter GEC accuracy.

A metadata defect was found and transparently corrected for analysis:
- SCI-DEV-11 originally protected "المعادلة (3)", which was not an exact source substring because the source has the attached preposition "للمعادلة (3)".
- Original source data remains unchanged.
- SCIENTIFIC_STRESS_SPAN_CORRECTIONS.json records the development-only annotation correction.

Raw full SWEET:
- exact protected-span preservation: 4/12 = 33.3%
- whitespace-insensitive protected preservation: 10/12 = 83.3%
- whole-source equality after ignoring whitespace: 4/12 = 33.3%
- [UNK] appeared in 6/12 outputs
- all 12 raw outputs differed from source text exactly

Observed risks include:
- dose/unit slash corruption: 5 mg/kg -> tokens containing [UNK]
- vocalized Arabic words becoming [UNK]
- mixed citation damage
- lexical changes in otherwise clean scientific stress text
- systematic surface-spacing reconstruction

## Bounded strict-fidelity prototype

A DEVELOPMENT prototype was tested:
- lock source-exact protected spans before SWEET
- run SWEET only on unprotected segments
- if tokenizer input contains [UNK], keep the exact source segment
- if generated segment contains [UNK], keep the exact source segment
- if a stage predicts zero non-K edits, keep the exact source segment rather than detokenizing it

Results:

### Protected NoPnx iteration 1
- exact protected spans: 12/12 = 100%
- outputs containing [UNK]: 0/12
- exact whole-source unchanged: 9/12 = 75%
- whitespace-insensitive whole-source unchanged: 9/12 = 75%

### Protected NoPnx iteration 2
- exact protected spans: 12/12 = 100%
- outputs containing [UNK]: 0/12
- exact whole-source unchanged: 9/12 = 75%
- no measured fidelity gain over one NoPnx pass

### Protected full pipeline including Pnx
- exact protected spans: 12/12 = 100%
- outputs containing [UNK]: 0/12
- exact whole-source unchanged: 3/12 = 25%

Therefore Pnx materially increases changes on these clean scientific stress cases without adding Nahw targeted-correction recovery.

## Evaluation interpretation

The 19.33% target recovery is NOT a full GEC accuracy score:
- 150 targets come from only 41 passages.
- References correct one published location, not the entire passage.
- collateral edits require adjudication.
- 56/150 full-pipeline targets were changed to another state rather than exact target recovery.
- 65/150 full-pipeline targets still locally preserved the original error.

The evaluation should follow an edit-decomposed framework:
- HIT / supported target correction
- UNDER-correction / target preserved
- WRONG or alternative target change / adjudication required
- OVER/collateral correction / adjudication required

This is consistent with the CLEME2.0 evaluation direction (ACL 2025), which separates hit-, wrong-, under-, and over-correction.

## Mid-phase architecture implications

Current classifications:

- INTEGRATE INTO EVALUATION: target-level hit/under/wrong/over decomposition with passage-clustered uncertainty.
- PROTOTYPE: Scientific Integrity Guard BEFORE SWEET with exact span locks and tokenizer hazard handling.
- TEST: a source-preserving surgical edit renderer that applies only model-supported edits to the original text instead of accepting full detokenized reconstruction.
- TEST: NoPnx iteration 1 as the conservative Proofread/Strict-Fidelity Arabic candidate generator.
- TEST: NoPnx iteration 2 only where an independently measured gain justifies it; current development evidence shows net-zero target gain.
- TEST / ROUTE SELECTIVELY: Pnx for explicit punctuation tasks rather than always-on strict proofreading.
- WATCH: multi-system edit selection (e.g. ArbESC+) after the single-system baseline is fully adjudicated.
- DO NOT INTEGRATE YET: raw full SWEET output as an auto-accepted scientific/document transformation.

## Research check

Relevant current evidence:
- SWEET / Arabic text editing, ACL 2025: https://aclanthology.org/2025.acl-long.875/
- CLEME2.0 edit-disentangled GEC evaluation, ACL 2025: https://aclanthology.org/2025.acl-long.10/
- Minimal-edit GEC, BEA 2025: https://aclanthology.org/2025.bea-1.9/
- Nahw Arabic grammar benchmark, EACL 2026: https://aclanthology.org/2026.eacl-long.296/
- ArbESC+ multi-system Arabic edit selection, 2025 preprint: https://arxiv.org/abs/2511.14230

## Current status versus previous checkpoint

MIXED, with a large increase in evidence quality.

Improved:
- real SWEET quality is now measurable;
- +19.33 percentage points exact targeted recovery versus the narrow deterministic baseline on this development slice;
- a bounded protection prototype raised exact protected-span preservation from 33.3% for raw full SWEET to 100%, and removed [UNK] from 6/12 cases to 0/12.

Worsened / risk:
- raw SWEET is too aggressive as a direct strict-fidelity renderer;
- full pipeline preserved clean source exactly in 0/12 raw scientific stress cases;
- Pnx adds no Nahw target gain here and sharply worsens clean scientific no-change behavior in the protected prototype (75% unchanged with NoPnx1 versus 25% with full).

## Forecast

Most likely viable product role:
SWEET is more promising as an Arabic edit/candidate generator inside a protected, selective, source-preserving architecture than as the final renderer.

Main blockers before freeze:
1. adjudicate the 56 TARGET_CHANGED_OTHER cases and collateral edits;
2. measure wrong/over-correction and review burden;
3. validate source-preserving edit application;
4. test a real punctuation slice before deciding Pnx routing;
5. broaden scientific-domain coverage beyond 12 authored stress cases.

Do not freeze and do not create a sealed final set yet.
