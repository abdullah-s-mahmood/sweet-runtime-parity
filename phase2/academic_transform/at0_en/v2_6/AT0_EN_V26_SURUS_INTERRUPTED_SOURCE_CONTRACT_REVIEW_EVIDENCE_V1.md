# ACAD_PASS — Interrupted Limited SURUS Source-Contract Review Evidence V1

Date: 2026-10-09
Timezone: Asia/Baghdad (UTC+3)

State:
`HIGHER_MODEL_REVIEW_INTERRUPTED_BEFORE_VERDICT`

User-reported higher-model session ended because the account usage limit was reached.

The higher model did NOT issue any of the authorized final verdicts:
- KEEP_SURUS_WITH_CHAR_COORDINATE_CONTRACT
- KEEP_SURUS_WITH_OTHER_CHANGES
- REJECT_OR_PAUSE_SURUS

Therefore:
`NO_GOVERNANCE_DECISION_WAS_PRODUCED`

No scientific fit authorization can be inferred.

## Durable repository check

At recovery, branch `at0-en-v2.6-dev` remained at:
`0ffe3746c2b40eac658e5b7ec34324fbe46e700a`

Thus the interrupted higher-model session left no durable GitHub commit in the project repository.

## Recoverable substantive finding from the interrupted review

The higher model stated that the observed 99.6048% structural alignment:
- demonstrates high structural coherence;
- does NOT by itself establish that those coordinates are exactly the boundaries intended by the human annotators;
- and that the 99.6048% check measures wordpiece boundaries on raw text, so it was verifying whether that matches the actual segment unit used by the frozen implementation.

This concern is scientifically valid and remains OPEN.

## Local follow-up inspection

The frozen ACAD_PASS protocol and implementation show:
- original words/characters and source offsets are preserved;
- original-to-model offset mapping is required;
- BiomedBERT windows are planned in wordpiece budgets but rounded to complete source-word boundaries;
- each source word is represented by the mean of its subword vectors;
- span endpoints are therefore not certified merely by arbitrary wordpiece-boundary agreement.

For SURUS, a trustworthy source-word/token unit has not yet been reconstructed from the public release.

## New source-paper evidence requiring diagnostic follow-up

The peer-reviewed SURUS paper states that dataset abstracts were tokenized using the BERT tokenizer and links the model to `bert-base-uncased`, whereas ACAD_PASS V4 tested the future scientific BiomedBERT tokenizer.

Therefore the V4 failure to recover released TokenStart/TokenEnd does NOT establish that SURUS token indices are unrecoverable.

Exact next non-scientific operation:
`SURUS_SOURCE_BERT_BASE_UNCASED_TOKEN_ALIGNMENT_DIAGNOSTIC_V5`

Restrictions:
- read-only;
- aggregate output only;
- no model fit;
- no protected evaluation;
- no source repair;
- no row dropping;
- no scientific attempt consumed.
