# ACAD_PASS Master Product Architecture

Version: 2.0.0
Date: 2026-10-03
Status: English-first implementation with multilingual-ready Core

## Product objective
ACAD_PASS is an academic-document intelligence and transformation platform whose central product objective is **human-quality academic transformation** while preserving scientific meaning, claims, quantities, citations, uncertainty, causality, technical terminology, document provenance, and approximate information volume.

## Core workflow
Transform -> Protect -> Verify -> Drift -> Repair/Escalate -> Review -> Preserve -> Deliver

## Language strategy
English is the only active implementation language. English is the first Language Pack, not the architecture itself. Arabic active research is frozen and preserved as future `LANG_AR`.

## Core responsibilities
Document identity/versioning; transactions; provenance; claim/quantity/citation representation; verification orchestration; rollback/replay; plugin permissions; audit; source-intelligence contracts; document adapters; account/project/institution infrastructure.

## Language Pack responsibilities
Segmentation/tokenization; morphology; syntax; discourse conventions; academic style; transformation prompts/models; stylometry; voice features; language-specific validation and detector protocols.

## Human writing
Outputs should be natural academic prose without fake errors, arbitrary synonym replacement, deliberate grammatical damage, or noise injection.

## Length
For `ACADEMIC_REWRITE`, 0.85-1.15 source word ratio is an initial soft diagnostic band, always subordinate to scientific and semantic preservation.

## Detector robustness
Detector robustness, including Turnitin, is a major external evaluation dimension. Detector scores do not enter generation loss/ranking and do not trigger rewrite-until-low loops.

## Roadmap
AT0-EN -> HW1-EN / Research Beta -> English Academic Beta -> DOCX -> Paid SaaS -> Word -> API -> Institutional -> future LANG_AR port.

## Current authorization
Only AT0-EN is authorized. HW1-EN and detector work require higher-model review.
