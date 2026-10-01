# POST-V4.2 EDIT TRANSACTION CONTRACT V1

Date: 2026-10-02

Status:
**FROZEN FOR SOURCE-ONLY IMPLEMENTATION PREFLIGHT**

Extends:
`phase2/redesign/ACAD_PASS_EDIT_CONTRACT_V1.md`

Governing gate:
`phase2/redesign/POST_V4_2_CANDIDATE_ARCHITECTURE_REDESIGN_GATE_V1.md`

This contract does NOT replace the historical M1 edit contract.
It operationalizes reversible candidate decomposition for post-V4.2 source-only architecture work.

---

## 1. Scope

Input:
- one frozen source sentence;
- one frozen proposer whole-sentence candidate action;
- frozen proposer/family/ancestry provenance.

Output:
- zero or more reversible atomic edit transactions;
- zero or more deterministic bundles;
- zero or more conflict components;
- exact deterministic reconstruction of the original whole-sentence candidate.

No gold/reference is allowed.

---

## 2. Raw source is authoritative

The exact raw UTF-8 source string is the only authoritative location space.

Required identities:
- source UTF-8 bytes;
- source SHA256;
- source Unicode code-point sequence;
- candidate UTF-8 bytes;
- candidate SHA256.

Offsets are stored in:
1. Unicode code-point offsets;
2. UTF-8 byte offsets.

Character offsets are half-open:
`[start, end)`

No normalized string may replace the authoritative source.

---

## 3. No lossy normalization in V1

V1 alignment operates on raw Unicode code points and deterministic token spans.

Forbidden in V1 alignment:
- alef unification;
- ya/alif-maqsura unification;
- ta-marbuta/ha normalization;
- hamza removal;
- diacritic stripping;
- tatweel stripping;
- Arabic/Persian digit mapping;
- punctuation canonicalization;
- whitespace collapsing before offset assignment.

A future shadow-normalization layer may be researched only if it preserves a complete reversible raw-span map and is versioned separately.

---

## 4. Deterministic segmentation

Define `RAW_SEGMENTER_V1`.

Each sentence is segmented into ordered spans:

- WHITESPACE
- LETTER_OR_MARK
- DIGIT
- PUNCTUATION
- SYMBOL
- OTHER

Rules:
- contiguous Unicode whitespace forms one WHITESPACE span;
- contiguous letters plus combining marks form one lexical span;
- contiguous digits form one numeric span;
- each punctuation code point is its own span;
- symbols are retained explicitly;
- no character is dropped.

Segmentation must satisfy:
`''.join(span.raw_text for span in spans) == original_raw_string`

---

## 5. Two-level alignment

### Level A — segment alignment

Use deterministic minimum-cost sequence alignment over raw segments.

Costs:
- exact same raw segment text: 0
- substitution: 1
- deletion: 1
- insertion: 1

Tie-breaking order:
1. maximize exact unchanged raw characters;
2. maximize exact unchanged segment count;
3. minimize number of edit blocks;
4. prefer earliest source anchor;
5. lexical compare of serialized operation sequence.

The tie-break is part of the algorithm and must be tested.

### Level B — local raw-code-point refinement

For each non-equal aligned block:
- run deterministic character-level alignment;
- split into smaller operations only when exact reconstruction remains unique;
- otherwise emit one `COMPLEX_LOCAL` transaction for the entire block.

No heuristic linguistic correctness judgment is used.

---

## 6. Atomic Edit Transaction schema

Required fields:

- `record_id`
- `contract_version`
- `uid`
- `cluster_id`
- `source_sha256`
- `parent_action_id`
- `parent_action_sha256`
- `proposer_id`
- `proposer_version`
- `family_id`
- `ancestry_id`
- `edit_id`
- `edit_type`
- `source_cp_start`
- `source_cp_end`
- `source_byte_start`
- `source_byte_end`
- `source_text`
- `replacement_text`
- `left_anchor_cp`
- `right_anchor_cp`
- `alignment_version`
- `protection_status`
- `transaction_sha256`

Optional:
- `bundle_id`
- `ambiguity_reason`
- `surface_class`

---

## 7. Edit types

Operational types:

### KEEP
No change.

### INSERT
- source span length = 0
- replacement non-empty

### DELETE
- source span length > 0
- replacement empty

### SUBSTITUTE
- source span length > 0
- replacement non-empty
- not classified as SPLIT/MERGE/PUNCTUATION

### SPLIT
A local source lexical span maps to multiple candidate lexical spans where:
- concatenating candidate lexical text after removing only raw whitespace equals the raw source lexical text;
- no other character normalization is used.

### MERGE
Multiple adjacent source lexical spans map to one candidate lexical span where:
- concatenating raw source lexical text after removing only raw whitespace equals candidate lexical text.

### PUNCTUATION
All changed non-whitespace characters in the transaction are Unicode punctuation characters.

### COMPLEX_LOCAL
A reversible local block that cannot be uniquely decomposed into the above without ambiguity.

### UNREPRESENTABLE
Used only as a terminal extraction failure record.
It never enters a candidate component.

---

## 8. Insert anchoring

Every zero-width INSERT has:
- `source_cp_start == source_cp_end`
- explicit left and right source anchors when available.

Multiple inserts at the same boundary are ordered by:
1. parent action;
2. candidate order;
3. edit_id.

Cross-family inserts at the same boundary are considered conflicting unless their exact replacement text is identical.

---

## 9. Transaction identity

Canonical transaction serialization:
- UTF-8 JSON;
- sorted keys;
- no insignificant whitespace;
- raw source/replacement preserved exactly.

`transaction_sha256 = SHA256(canonical_json_without_transaction_sha256)`

`edit_id` is:
`sha256(uid + source_sha256 + parent_action_id + source_cp_start + source_cp_end + replacement_text + edit_type)`

No random identifier is permitted.

---

## 10. Exact parent reconstruction

For every parent candidate action:

1. sort transactions by source location;
2. apply non-overlapping transactions deterministically to the raw source;
3. reconstruct candidate string;
4. require exact byte-for-byte equality with the frozen parent candidate.

Required invariant:
`reconstructed_candidate_sha256 == parent_action_sha256`

If this fails:
`PARENT_RECONSTRUCTION_FAILURE`

The parent action is not admitted to V1 edit-level analysis.

---

## 11. Bundle semantics

A bundle may exist only if transactions from the SAME parent action must be accepted together.

Bundle eligibility:
- same parent_action_id;
- deterministic member order;
- explicit union source span;
- exact reconstruction test;
- reason code.

Allowed bundle reasons:
- `SPLIT_MERGE_COUPLING`
- `LOCAL_REWRITE_COUPLING`
- `RECONSTRUCTION_DEPENDENCY`

Forbidden:
- gold-based co-occurrence;
- combining edits merely because they are near each other;
- cross-proposer bundle synthesis in V1.

Bundle identity is a SHA256 over ordered member edit IDs.

---

## 12. Provenance-preserving deduplication

Two transactions may deduplicate only when all are equal:

- source_sha256
- source_cp_start
- source_cp_end
- source_text
- replacement_text
- edit_type

Deduplication output retains ALL provenance records.

Same-family provenance remains same-family.

P1 + P3 must never become two independent witnesses.

---

## 13. Conflict graph

Nodes:
- deduplicated transactions;
- deterministic bundles.

Edges are added when any of these holds:

1. overlapping non-zero source spans;
2. insertion occurs strictly inside another edit span;
3. incompatible inserts at same boundary;
4. different replacements for same source span;
5. SPLIT/MERGE boundary incompatibility;
6. bundle-member conflict;
7. protection incompatibility;
8. deterministic reconstruction would depend on application order.

Connected components are frozen as:
`CONFLICT_COMPONENT`

Every component includes:
`KEEP_COMPONENT`

---

## 14. Compatible-component composition

Transactions from different components may be composed only if:

- source spans are disjoint;
- insert anchors do not conflict;
- no shared bundle dependency;
- all protection checks pass;
- deterministic application order is unique.

Application order:
descending source_cp_start, then descending source_cp_end, then edit_id.

This prevents earlier edits from shifting later raw offsets.

---

## 15. Novel composed sentences

A sentence produced by combining compatible edits from different parent actions may never be described as a proposer output.

It must be marked:
`COMPOSED_FROM_PROVENANCE_PRESERVING_COMPONENTS`

Required lineage:
- all edit IDs;
- all parent action IDs;
- all proposer IDs;
- family set;
- reconstruction algorithm version.

No synthetic composition is allowed inside a conflict component.

---

## 16. Protection integration

Protection checks occur at three levels:

1. transaction;
2. bundle/component;
3. final composed sentence.

Any active frozen protection violation:
`FAIL_CLOSED_PROTECTION`

No protection weakening is authorized.

---

## 17. Failure taxonomy

Terminal extraction failures:

- `INVALID_SOURCE_IDENTITY`
- `INVALID_PARENT_ACTION_IDENTITY`
- `SEGMENTATION_RECONSTRUCTION_FAILURE`
- `ALIGNMENT_NONDETERMINISTIC`
- `RAW_OFFSET_MAPPING_FAILURE`
- `UNREPRESENTABLE_EDIT`
- `PARENT_RECONSTRUCTION_FAILURE`
- `PROTECTION_FAILURE`
- `PROVENANCE_FAILURE`

Failures remain in denominator accounting for source-only coverage diagnostics.

---

## 18. Source-only metrics

Allowed:

- parent actions processed
- extraction success rate
- failed parent-action rate
- transactions per parent
- transactions per UID
- edit-type frequencies
- bundle frequency
- conflict-component count
- component-size distribution
- cross-family exact-edit agreement
- same-family P1/P3 overlap
- unique edit contribution per family
- KEEP-only component rate
- protection failure rate
- exact parent reconstruction rate
- composed-action count
- runtime
- memory

Forbidden:
- correctness
- linguistic precision/recall
- gold recovery
- selector quality
- reference-supported rates

---

## 19. Required synthetic adversarial cases

At minimum:

1. exact KEEP
2. simple substitution
3. deletion
4. insertion at start
5. insertion at end
6. two inserts at same boundary
7. punctuation-only change
8. Arabic combining mark change
9. tatweel difference retained raw
10. whitespace split
11. whitespace merge
12. SPLIT
13. MERGE
14. adjacent substitutions
15. overlapping alternatives
16. same literal edit from P1/P3
17. same literal edit from SWEET/P2
18. different replacements same span
19. non-overlapping edits from different families
20. coupled same-parent bundle
21. reconstruction-dependent bundle
22. ambiguous alignment
23. multi-byte UTF-8 offset check
24. Arabic + English mixed text
25. Arabic + digit + punctuation
26. protected numeric span
27. protected citation-like span
28. action with no representable deterministic decomposition
29. exact parent reconstruction mismatch
30. deterministic composed reconstruction

All cases are synthetic/source-free.

---

## 20. V1 exit criteria

Before full source-only population execution:

- contract implemented exactly;
- 30/30 minimum synthetic tests PASS;
- raw/byte offset parity PASS;
- parent reconstruction parity PASS;
- provenance parity PASS;
- P1/P3 same-family invariant PASS;
- no gold/reference loader in implementation;
- protection stack unchanged;
- independent review of implementation packet.

No new gold is authorized by this contract.
