# AT0-EN V2.3 — Second Unseen Adversarial Holdout V1 Construction Protocol

Date: 2026-10-03
Status: CONSTRUCTION/FREEZE ONLY
Scoring status: NOT_RUN

## Purpose

Create a temporally frozen second adversarial holdout for the already-frozen V2.3 assertion-graph verifier.

The holdout is constructed after the V2.3 known-failure regression gate and before any V2.3 scoring on these cases. Once the inputs and labels are frozen, V2.3 must not be modified before the one-shot holdout score.

## Independence boundary

This is **unseen-to-scoring / temporally held out**, but it is not claimed to be a perfectly designer-blind independent benchmark.

The same higher-level project context has seen the V2.3 architecture and the earlier V2.2 red-team history. To reduce adaptation bias:
- construction is based on the frozen source cases and an external error taxonomy, not on executing/probing V2.3;
- no V2.3 scoring is performed during construction;
- inputs and labels are frozen before scoring;
- V2.3 implementation may not change after holdout freeze and before the one-shot score;
- after scoring, any failure may motivate a later redesign, but this holdout then becomes consumed development evidence and cannot remain an untouched holdout.

No separate stronger-model consultation tool is available inside the current chat environment. This limitation is recorded rather than represented as an external consultation.

## Research basis

Construction follows principles from:
- TRUE (Honovich et al.): example-level factual-consistency meta-evaluation and complementary verification methods.
- VitaminC (Schuster et al.): contrastive examples with small factual changes that preserve surface similarity.
- ANLI (Nie et al.): adversarial examples designed to expose model blind spots rather than saturate a static benchmark.
- Jourdan et al., ACL 2025: scientific revision requires correctness-sensitive and task-specific evaluation; similarity and instruction-following are insufficient.

References:
- https://arxiv.org/abs/2204.04991
- https://arxiv.org/abs/2103.08541
- https://arxiv.org/abs/1910.14599
- https://aclanthology.org/2025.acl-long.335/

## Holdout composition

Total: 36
- 12 faithful contrastive SAFE_CONTROL paraphrases
- 24 ADVERSARIAL cases
- 2 adversarial cases per source case EN01–EN12

The new adversarial families intentionally emphasize relation rebinding and qualifier errors that are not exact copies of the known V2.2 attacks:
- scope binding shift
- exclusive-quantifier dilution
- agent/interval rebinding
- deployment-status invention
- percentage/metric rebinding
- condition rebinding
- subsystem/outcome swap
- condition-direction shift
- population generalization
- outside-population evidence invention
- unit-scale change
- baseline rebinding
- parameter-timing shift
- post-selection tuning invention
- density-qualifier swap
- manipulation-status shift
- adaptation-time weight change
- coefficient/variable swap
- grouping-interval rebinding
- metadata-scope reduction
- forwarding-scope expansion
- timestamp substitution
- metric-label swap
- partial retuning invention

## Gold construction rule

For SAFE_CONTROL:
- every source assertion, relation, quantity/unit, qualifier, scope, negation, and reproducibility condition must be preserved;
- stylistic compression/reordering is allowed only when relation identity remains intact.

For ADVERSARIAL:
- each text intentionally contains at least one material scientific-preservation violation;
- expected label is NOT_PASS;
- decoy terms may preserve the original words/numbers elsewhere to challenge positive-witness checking.

The authoritative reference is source_text, not the older frozen content_units list, because EN09 demonstrated that content_units can omit a source relation.

## Freeze and scoring rule

The holdout is stored as:
- inputs JSONL: texts only plus IDs/case IDs;
- labels JSONL: expected class, attack family, rationale;
- manifest: exact SHA-256 identities.

Labels are frozen before scoring. They are not secret; integrity is established by temporal freeze and hashes, not by secrecy.

The future one-shot scoring workflow must:
1. bind to the frozen V2.3 verifier hash;
2. read the frozen inputs without altering the verifier;
3. produce predictions before evaluation;
4. evaluate predictions against the already-frozen labels;
5. preserve all failures;
6. never tune V2.3 and re-score the same holdout as if it were untouched.

No model inference is involved.
