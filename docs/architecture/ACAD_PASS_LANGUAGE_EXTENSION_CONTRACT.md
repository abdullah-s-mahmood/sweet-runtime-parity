# ACAD_PASS Language Extension Contract

Version: 1.0.0
Date: 2026-10-03

## Principle
A language is added as a Language Pack over the same Core, never as a forked product.

## LanguageAdapter capabilities
- detect_language
- segment_document
- segment_paragraph
- segment_sentence
- analyze_morphology
- analyze_syntax
- extract_discourse_features
- extract_stylometric_features
- transform_academic_text
- verify_language_quality
- validate_punctuation
- compute_length_metrics
- build_voice_profile
- evaluate_voice_similarity
- get_detector_protocol
- get_language_specific_constraints

Unsupported capabilities return explicit `NOT_IMPLEMENTED`, `UNSUPPORTED`, or `UNCERTAIN`. Core must never silently fall back to English.

## Core portability invariants
- explicit language field and UNKNOWN path;
- explicit Unicode coordinate units;
- tested UTF-8/code-point/UTF-16 conversion;
- direction metadata independent of stored logical text order;
- tokenizers, prompts, grammar, detector thresholds, and language length rules outside Core;
- extensible VoiceProfile;
- capability-based interfaces, not English grammatical tags.

## Future ADD ARABIC
Read the master architecture, this contract, Arabic snapshot, and architecture changelog. Classify each component as `REUSE_UNCHANGED`, `ADAPT_INTERFACE`, `ARABIC_IMPLEMENTATION_REQUIRED`, or `ARABIC_REVALIDATION_REQUIRED`. Reuse preserved evidence and do not rerun closed experiments without scientific justification.
