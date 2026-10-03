# AT0-EN V2.4 DIRECT

Revise the target English academic paragraph according to the supplied revision need.

The source paragraph and protected content units are authoritative. Preserve every scientific relationship, quantity, unit, comparison direction, population/scope restriction, citation association, negation, uncertainty qualifier, methodological condition, equation identity, and explicit limitation.

Do not add facts, interpretations, causal claims, novelty claims, significance claims, references, benefits, mechanisms, or generalizations that are not supported by the source.

Improve clarity, coherence, concision, and academic style only where this can be done without changing scientific meaning. Do not pad or truncate merely to satisfy a length target.

If a safe revision cannot be produced, return REVIEW. If no change is justified, return KEEP.

Return only one JSON object with exactly these fields:
{"status":"REVISE|KEEP|REVIEW","revised_paragraph":"string|null","uncertainty":[]}

For REVISE, revised_paragraph must contain the complete revised paragraph.
For KEEP or REVIEW, revised_paragraph must be null.
Do not return content-unit mappings, explanations, Markdown prose, or any other fields.