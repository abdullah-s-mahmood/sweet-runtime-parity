# AT0-EN V2.4 REALIZE

Using the original source paragraph, protected content units, revision need, and the previously generated visible editorial plan, produce the final revised English academic paragraph.

The source and protected content units are authoritative. The plan is advisory only and must be ignored if it conflicts with source meaning or protection constraints.

Preserve every scientific relationship, quantity, unit, comparison direction, population/scope restriction, citation association, negation, uncertainty qualifier, methodological condition, equation identity, and explicit limitation.

Do not add facts, interpretations, causal claims, novelty claims, significance claims, references, mechanisms, benefits, or generalizations that are not supported by the source.

If safe realization is not possible, return REVIEW. If the source should remain unchanged, return KEEP.

Return only one JSON object with exactly these fields:
{"status":"REVISE|KEEP|REVIEW","revised_paragraph":"string|null","uncertainty":[]}

For REVISE, revised_paragraph must contain the complete revised paragraph.
For KEEP or REVIEW, revised_paragraph must be null.
Do not return mappings, explanations, Markdown prose, or any other fields.