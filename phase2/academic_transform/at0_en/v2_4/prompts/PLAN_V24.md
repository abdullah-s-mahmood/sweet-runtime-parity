# AT0-EN V2.4 PLAN

Create a short visible editorial plan for the target English academic paragraph.

Use only supplied source content and protected content units. Allowed operations include KEEP, CLARIFY, REMOVE_REDUNDANCY, MERGE, SPLIT, and REORDER_WITHIN_PARAGRAPH.

The plan must not introduce new facts, interpretations, causal claims, novelty claims, significance claims, references, mechanisms, benefits, or generalizations. It must not weaken or strengthen scientific claims, restrictions, negation, uncertainty, comparison direction, or methodological conditions.

If the requested revision cannot be planned safely, return REVIEW.

Return only one JSON object with exactly these fields:
{"status":"PLAN|REVIEW","operations":[],"uncertainty":[]}

For REVIEW, operations must be empty.
Do not provide private chain-of-thought or explanatory prose.