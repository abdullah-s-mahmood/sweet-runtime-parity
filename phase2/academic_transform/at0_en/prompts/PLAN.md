# AT0-EN PLAN prompt v1

Create a short visible editorial plan for the target English academic paragraph. Use only supplied content-unit IDs and allowed operations such as KEEP, REORDER_WITHIN_PARAGRAPH, SPLIT, MERGE, CLARIFY, or REMOVE_REDUNDANCY. Do not write private chain-of-thought.

The plan must preserve every scientific relation and protected element. It must not introduce new facts, references, novelty claims, causal strengthening, or generalization. If a requested improvement conflicts with preservation constraints, mark the item REVIEW rather than resolving it by invention.

Return only the structured plan and uncertainty flags.