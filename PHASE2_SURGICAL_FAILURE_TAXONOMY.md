# Surgical failure taxonomy

1. **Wrong model-supported edit (7/60).** Examples: وانشر→وأنشر changes imperative polarity/actor cues; أولي→أولى changes the intended noun; a single deleted opening parenthesis damages a quotation; فيها→فيه changes referent; شئنها→شؤنها and جاني→جانئ are orthographically wrong; الدؤب→الدوب damages the word.
2. **Partial local edit (2/60).** يبطيء→يبطي omits a required hamza seat; إحتمله→احتمله fixes hamza but leaves the conditional answer without فاء.
3. **Unnecessary edit (2/60).** Removing a defensible comma and splitting لولا add no correction value.
4. **Unresolved target error (108/150).** Source preservation prevents corruption but does not solve all agreement, case, hamza and weak-verb cases.
5. **False exact-match flags (5/32).** Queue flags for ITEM-143, 387, 433, 435 and 439 have no applied edit at the target; the source error remains. The adjudicated exact supported count is 27.
6. **Suppressed unknown-token hazards (98/100).** The gate prevented destructive decoding; 51 hazards are clearly harmful and 47 unsafe, with two plausible but unproven recovery opportunities across all suppression reasons.
7. **Second-pass tradeoff.** NoPnx2 adds two useful repairs, regresses وامنح to وأمنح, removes another parenthesis and adds an unresolved lexical change.
8. **Pnx review burden.** Of 26 incremental punctuation edits, 14 are supported, six unnecessary, one wrong and five unresolved. None adds a target recovery in the supplied queue.

Severity is attached to every applied edit in the JSONL. These are passage-clustered development observations; no claim of scientific semantic safety or production auto-accept follows.
