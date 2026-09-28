# Phase 2 — Full AraBART Edit Event Adjudication

Date: 2026-09-28

## Scope
106 full AraBART edit events across 36 passages: 96 SUB and 10 COMPLEX. 56 judgments were safely reused from the already completed 67-row one-to-one adjudication; 50 events were adjudicated in full-event context. PASS 2 was a same-agent consistency recheck, not independent human validation.

## Results
- Supported correction: 57
- Supported alternative: 5
- Partial correction: 7
- Unnecessary edit: 2
- Wrong correction: 35
- Overall supported/alternative rate: 58.49%

Target-overlap: 46/56 supported/alternative (82.14%).
Non-target: 16/50 supported/alternative (32.00%), with 31/50 wrong (62.00%).

## Complex-event finding
Complex alignment is not optional. Some events must be judged jointly:
- `داعي المسلمون -> دعا المسلمين` is grammatical and meaning-compatible as a whole, but the isolated `داعي -> دعا` edit leaves incompatible syntax.
- `يعرفوا أبناؤهم -> يعرفون أبناءهم`, `بيت واحد -> بيتا واحدا`, and `موعد مناسب -> موعدا مناسبا` are coherent multiword corrections.
- `فأجابهما: أتسألا -> فاجابهما اسألاه` and `ولأمتهم؛ فاعمل -> ولامتهم فأعمل` are jointly unsafe.
- `ولا بد -> ولابد` is a boundary merge and must never be represented as a patch-safe one-word substitution.

## Interpretation
AraBART is a valuable recall-expanding generator, but not an acceptance oracle. The next gate must be target-agnostic and operate on complete edit events, with typed Arabic validators, alignment quality, independent evidence, source-fidelity, and abstention.
