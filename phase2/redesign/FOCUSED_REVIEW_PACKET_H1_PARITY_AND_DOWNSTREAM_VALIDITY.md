# Focused Review Packet — H1 Parity, Official-Alignment Recall, and Downstream Validity

Date: 2026-09-30
Project: ACAD_PASS / Phase 2 Arabic GEC
Status: FROZEN REVIEW PACKET
Scope: H1 only + downstream validity implications

## 1. Decision issue

The frozen M2-H protocol requires H1 candidate edit-instance recall >= 80% on CALIBRATION before H5/H6 can be treated as scientifically viable.

The original direct exact-transaction audit produced a provisional 30.0205% value, but that measurement was later shown to be representation-sensitive and confounded by QALB edit decomposition, punctuation, and tatweel handling.

A representation-invariant official-alignment audit has now been completed.

## 2. Frozen H1 inference contract

Model:
CAMeL-Lab/text-editing-qalb14-nopnx

Frozen model revision:
21286e56ce98a86362db540863f91c083b8970f9

Frozen implementation revision:
4d552ca3ae98029550f27fc52aa1b22883e16e61

Frozen inference:
- one pass
- top-1
- NoPnx
- no confidence threshold
- no top-k expansion
- no punctuation model

## 3. Inference parity result

Public/model-card inference parity sample:
- deterministic CALIBRATION sample: 256
- subwords match: 256 / 256
- top-1 labels match: 256 / 256
- normalized rewrite match: 256 / 256
- all-field parity: 256 / 256
- mismatches: 0

Conclusion:
The frozen H1 candidate-generation stream is validated against the public/official inference path. There is no evidence that the H1 runner itself caused the recall deficit.

## 4. Official NoPnx gold-construction audit

CALIBRATION cases:
6,888

A frozen tatweel-preserving char-alignment amendment was required because the upstream character aligner normalizes/removes U+0640 kashida before attempting exact surface reconstruction, causing assertions on affected QALB rows.

The amendment was accepted only under strict cross-validation:
- official char-alignment successes were compared against the tatweel-preserving path;
- required mismatch count: 0;
- word/subword NoPnx target cross-path mismatch requirement: 0;
- no case could be silently excluded.

Final full loop:
- processed: 6,888 / 6,888
- gold-construction failures: 0
- char-alignment cross mismatches: 0
- word/subword cross-path mismatches: 0
- INTERNAL_EVALUATION opened: false
- STRESS_DIAGNOSTIC opened: false

Gold-construction source run:
36716848223

Source artifact:
11098030966

Source artifact digest:
sha256:ad476c7dfb8e194320a1a5d4b0a05ea016be5e4b012403854290fc86ca455fb1

## 5. Representation-invariant M2 result

Scoring-only continuation run:
36720612925

Continuation artifact:
11101562193

Continuation artifact digest:
sha256:5f3478162cb54034cb89a58a47db32f70e50573186b7df980215e56b3259e420

Official-alignment one-pass NoPnx M2:
- Precision: 0.7153
- Recall: 0.6939
- F1: 0.7044
- F0.5: 0.7109

Frozen H1 recall gate:
0.8000

Recall deficit:
-0.1061 absolute = -10.61 percentage points

Gate:
FAIL

Secondary:
- derived gold M2 edit lines: 35,559
- exact NoPnx reference sentences: 1,540 / 6,888 = 22.36%
- source-copy sentences: 283 / 6,888 = 4.11%

This is not a borderline miss. It is >10 pp below the frozen gate.

## 6. External/public sanity evidence

The public Hugging Face model card and current repository usage example apply the NoPnx model iteratively with decode_iter=2, then apply the Pnx model once.

This is relevant because the frozen H1 audit deliberately used one-pass decoding. Iterative decoding may improve coverage, but changing from one-pass to iterative decoding after observing the failed one-pass metric would be a new versioned diagnostic, not a valid rescue of H1-v1.

The ACL 2025 SWEET paper is:
Bashar Alhafni and Nizar Habash.
"Enhancing Text Editing for Grammatical Error Correction: Arabic as a Case Study."
ACL 2025, pages 17892-17914.
DOI: 10.18653/v1/2025.acl-long.875

Public model card:
https://huggingface.co/CAMeL-Lab/text-editing-qalb14-nopnx

Public repo:
https://github.com/CAMeL-Lab/text-editing

## 7. Downstream dependency impact

Because inference parity passed 256/256 and the frozen H1 stream did not change:

H2:
- no rerun required for candidate generation;
- H2-v1/v2 conclusions remain valid;
- 0 automatic families remain enabled.

H3:
- no rerun required solely due to the H1 audit;
- H3 remains CLOSED FAIL / not activated.

H4:
- gold structural recall calculations remain valid;
- H1 intersection diagnostics remain based on the same unchanged H1 stream;
- H4 remains not activated.

M1 / M2 / M2-R:
remain closed and unaffected.

H5/H6:
remain BLOCKED pending a scientific decision on how to interpret the failed H1-v1 gate.

INTERNAL_EVALUATION / STRESS_DIAGNOSTIC:
must remain unopened.

## 8. Core review questions

1. Is official-alignment one-pass NoPnx M2 recall a defensible operational realization of the preregistered H1 "candidate edit-instance recall >=80%" gate after exact-transaction matching was shown to be representation-sensitive?

2. Given Recall=69.39%, should H1-v1 be considered CLOSED FAIL under the frozen protocol?

3. Does the public intended usage of decode_iter=2 justify a separately versioned iterative H1 diagnostic, provided:
   - the current H1-v1 result remains frozen as FAIL;
   - no gate is weakened;
   - INTERNAL_EVALUATION remains closed;
   - the iterative diagnostic is explicitly labeled post-v1 and exploratory/diagnostic?

4. If iterative decoding is explored, what would constitute a scientifically defensible stopping rule that prevents a tuning loop?

5. If H1-v1 is closed and no iterative diagnostic is authorized, should H5/H6 be closed without execution because the candidate generator already violates its prerequisite gate?

6. Are any downstream H2/H3/H4 reruns scientifically necessary despite 100% H1 inference parity and an unchanged H1 candidate stream?

## 9. Decision options

Option A — Close H1-v1 and close M2-H before H5/H6.
Rationale:
the preregistered prerequisite failed substantially (-10.61 pp); proceeding may be scientifically incoherent.

Option B — Close H1-v1 as FAIL, but allow one separately versioned iterative-decoding diagnostic.
Constraints:
- exactly one preregistered diagnostic;
- no threshold/gate changes;
- no INTERNAL_EVALUATION;
- no reuse of the diagnostic result to rewrite H1-v1;
- predetermined stop rule before execution.

Option C — Proceed to H5/H6 despite H1-v1 failure.
This requires an explicit argument that the original 80% H1 gate was not actually a prerequisite for H5/H6. The current frozen protocol record appears inconsistent with such an interpretation, so this option requires strong justification.

## 10. Out of scope

Do not:
- tune SWEET weights;
- change H1 checkpoint;
- lower the 80% gate;
- change one-pass H1-v1 retroactively;
- open INTERNAL_EVALUATION;
- open STRESS_DIAGNOSTIC;
- open Confirmation, Holdout, A7'ta reserve, reserved Nahw IDs, or QALB15 TEST;
- restart H2/H3/H4 tuning;
- treat iterative decoding as if it were the preregistered H1-v1 run.

## 11. Current recommended interpretation for review

H1-v1 should be treated as a scientifically resolved one-pass FAIL unless a focused methodological review finds that the official-alignment M2 definition is not a valid realization of the frozen gate.

If a further diagnostic is permitted, the only clearly motivated one is a separately versioned iterative decoding check aligned with the public SWEET usage pattern. It must not erase or replace the failed H1-v1 result.
