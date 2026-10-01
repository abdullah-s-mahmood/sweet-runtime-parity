# MP-SEF P2 GED ALIGNMENT PROVENANCE DEFECT V1

Date: 2026-10-01
Status: FROZEN SOURCE-ONLY DEFECT RECORD

## Scope

This finding uses only the frozen P2 proposal artifact and the frozen Arabic-GEC implementation/documentation.
No gold/reference content and no R_joint result were read or computed.

## Frozen P2 artifact

- cases: 1,918
- proposal SHA256:
  `f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b`

## Observed defect

For every frozen P2 case:

`len(ged_labels) > len(morph_preprocessed_text.split())`

Counts:
- mismatch cases: **1,918 / 1,918**
- exact count matches: **0 / 1,918**
- difference minimum: **2**
- difference maximum: **87**
- median excess GED labels: **15**
- mean excess GED labels: **15.8191**
- all differences are positive.

Example:
- UID `dev:1003`
- morphology words: 50
- stored GED predictions: 58
- excess: 8

## Cause

The frozen P2 runner obtains GED predictions directly for every BERT subword after removing only special tokens:

`preds = ...[1:-1]`

and then passes that list to:

`for word, label in zip(morph.split(), ged_labels)`

The official Arabic-GEC `ErrorIdentifier` implementation instead creates one real label position for the **first wordpiece of each source word** and marks remaining wordpieces with the cross-entropy ignore index. Its prediction alignment retains only those first-wordpiece positions.

Therefore the frozen P2 runner does not implement a generally valid word-level GED alignment. Once any word splits into multiple BERT wordpieces, subsequent labels can be shifted relative to source words. Extra subword predictions are silently dropped by `zip`.

## Consequence

This is a proposer-generation provenance defect, not a gold-derived quality finding.

The frozen P2 proposals MUST NOT be regenerated, replaced, or corrected after discovery.

For the current V3 cycle, a P2 hypothesis cannot receive executable status unless the frozen legalizer policy explicitly proves acceptable GED word alignment. Under the independent review's fail-closed L09/C11 requirement, the observed mismatch is classified as:

`EXECUTION_FAILED:GED_WORD_LABEL_ALIGNMENT_MISMATCH`

for affected P2 hypotheses.

Because the mismatch is present in 1,918/1,918 frozen P2 records, the current frozen P2 route is expected to contribute **zero executable P2 whole-hypothesis actions** unless an independent methodological review explicitly concludes that this provenance defect does not invalidate executability under the frozen contract.

No such exemption is authorized by this record.

## Scientific interpretation

**WORSENED P2 PROVENANCE OUTLOOK / IMPROVED DEFECT DETECTION**

This record does not estimate linguistic accuracy and does not compute candidate availability.

Reserved/internal datasets remain closed.
