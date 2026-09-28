# Failure taxonomy after adjudication

- **Unknown-token reconstruction / renderer corruption:** bracket fragments or [UNK] replace words, sometimes with no model non-K edit. This is a hard rejection for as-run passage output. See ITEM-022, 039, 095, 439.
- **Model-supported deletion or insertion with lexical loss:** D* can remove an unknown token or phrase; ITEM-105 and ITEM-199 lose text. Attribution may be mixed with prior [UNK].
- **Target under-correction:** 65 targets preserve the local published error in the full run.
- **Wrong local correction:** 50 changed targets fail the published grammatical rule or lose the target.
- **Valid unvowelled alternative:** 4 changed targets satisfy the rule without optional diacritics; exact-match-only scoring misses them.
- **Partial correction:** 2 changed targets fix one feature but leave a grammatical/orthographic requirement unmet.
- **Second-pass regression:** ITEM-077 is recovered in NoPnx iteration 1 and regresses to وأمنح in iteration 2; ITEM-467 is newly recovered.
- **Punctuation opportunity and over-edit risk:** Pnx adds commas in some clauses; no incremental target recoveries in the full run, and punctuation placement needs contextual judgment.
- **Renderer-only surface normalization:** whitespace around punctuation is not a linguistic correction; 1395 collateral diff rows include benign formatting and destructive unknown-token rendering, distinguished by severity and origin.
- **Domain safety unknown:** no inference from these passages proves scientific meaning preservation; the protected-span and safety stack remain unchanged.

Counts above are raw edit rows across four architectures, not unique errors or independent passages. For exact examples and decisions see the JSONL files.
