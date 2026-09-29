# M1-A — Adversarial Brainstorming Before Implementation

Date: 2026-09-30  
Status: FROZEN BEFORE RESULTS

## Candidate strategies considered

### A. Stop until two human reviewers are available
Strength: cleanest independence.
Weakness: blocks measurement research unnecessarily even though expert-corrected corpora exist.
Decision: reject as the only path; retain human confirmation as a later gate.

### B. Let the current agent label the 24-case pilot
Strength: immediate.
Weakness: repeats the exact provenance weakness identified by the audit.
Decision: reject as human gold.

### C. Use a frontier LLM as surrogate gold immediately
Strength: scalable and context-sensitive.
Weakness: LLM judge reliability is task-dependent; scientific correctness remains difficult; circular if the judge later evaluates itself.
Decision: reject as gold; permit later as a system under test.

### D. Treat QALB reference mismatch as wrong
Strength: simple.
Weakness: contradicted by QALB multi-annotator evidence and GEC multi-reference literature.
Decision: reject.

### E. Expert-grounded partial-label bootstrap
Use human corrected source→reference pairs only for claims directly entailed by them, synthesize controlled incomplete candidates by withholding known expert edits, and leave semantic/scientific/document dimensions unresolved when they are not directly established.
Decision: SELECTED.

## Evidence tiers

### TIER_A_DIRECT
Directly derivable from the human-corrected pair or published local correction:
- source differs from expert reference;
- a particular expert reference edit is applied;
- candidate equals the full expert reference;
- known expert-reference edits remain unapplied;
- KEEP is expert-supported on a source==reference line.

### TIER_B_PROTOCOL_SUPPORTED
Supported by the corpus annotation protocol but not independently adjudicated per item:
- annotations aimed for grammatical correctness, semantic coherence, minimal intrusion and style preservation.

These are contextual evidence, not automatic per-item labels.

### TIER_C_UNESTABLISHED
Not established by QALB/Nahw alone:
- scientific-claim fidelity;
- factual truth;
- author intent in ambiguous cases;
- document/DOCX structural integrity;
- correctness of a candidate that differs from all available references;
- whether two remaining errors are causally/grammatically related.

These dimensions remain null/unknown or REVIEW_REQUIRED.

## Controlled case families

1. FULL_EXPERT_REPAIR
   source → full human corrected line.
   Strong for full-reference completion.

2. EXPERT_KEEP
   source == human corrected line.
   Strong evidence that no correction was annotated under that corpus protocol; not proof that no possible stylistic rewrite exists.

3. SINGLE_EDIT_COMPLETE
   exactly one official reference edit and candidate equals full corrected line.
   Separates a one-edit complete reference case from multi-edit cases.

4. ONE_OF_MANY_PARTIAL
   on a line with >=2 official edits, apply exactly one expert edit and leave the others.
   This produces a controlled candidate with a human-supported local edit and known residual reference edits.

5. ALL_BUT_ONE_PARTIAL
   apply all official edits except one.
   This creates a hard near-complete negative for sentence-completeness testing without fabricating an incorrect edit.

6. NAHW_LOCAL_REFERENCE
   apply one published Nahw target correction to the frozen development passage.
   Strong local support; never claim full-passage completion because Nahw targets are one-location references.

## Important non-cases

M1-A will NOT synthesize arbitrary WRONG or UNNECESSARY edits by:
- reversing a gold edit;
- replacing with random tokens;
- treating a non-reference alternative as wrong.

Those may be generated later only for a separately declared robustness task and never called human gold.

## Expected value

If successful, M1-A removes the immediate human-reviewer availability blocker for:
- contract calibration;
- completeness/residual detection research;
- future verifier pretesting.

It does NOT remove the need for independent human confirmation before claims about real Arabic academic documents.
