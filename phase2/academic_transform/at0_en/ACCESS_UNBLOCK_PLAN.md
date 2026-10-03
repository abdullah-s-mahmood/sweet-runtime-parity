# AT0-EN — ACCESS UNBLOCK PLAN

Date: 2026-10-03
Status: PROPOSED / NOT YET AUTHORIZED

## Purpose

Provide an auditable, low-cost path to execute the frozen AT0-EN 48-slot live matrix without changing its scientific contract.

## Candidate independent model pair

1. OpenAI `gpt-5.6-terra`
   - provider: OpenAI API
   - official observed price on 2026-10-03: USD 2.00 / 1M input tokens; USD 12.00 / 1M output tokens
   - official source: https://developers.openai.com/api/docs/models/gpt-5.6-terra

2. Anthropic `claude-sonnet-5`
   - provider: Claude API
   - official observed price on 2026-10-03: USD 2.00 / 1M input tokens; USD 10.00 / 1M output tokens
   - official source: https://www.anthropic.com/research/claude-sonnet-5

These are candidate identities only. They become frozen experiment identities only after actual API access is confirmed and the provider-visible identity/version behavior is recorded. Do not silently substitute a different model.

## Workload evidence

Frozen AT0-EN inputs:
- 12 cases;
- source paragraphs: 38–73 whitespace words each;
- fixed prompt templates: DIRECT ~130 words, PLAN ~88 words, REALIZE ~114 words;
- two models × DIRECT/PLANNED = 48 slots;
- nominal maximum = 72 logical requests.

## Proposed authorization ceiling

This is a proposal, not authorization:

- `authorized_cost_ceiling_usd = 5.00`
- `max_total_tokens = 250000` provider-reported input + output tokens across the full two-model run
- retain the existing 72-logical-request ceiling
- reserve cost before each dispatch;
- stop before a request if its worst-case reservation would exceed the remaining ceiling.

The USD 5 ceiling intentionally includes a substantial margin above the expected cost for these short paragraphs. Actual cost must be reported from provider usage, not estimated after the fact.

## Preferred auditable execution environment

A repository-controlled runner or other environment that:
- receives provider credentials from a secret store;
- never commits or prints credentials;
- records exact provider/model identifiers, request IDs when exposed, timestamps, settings, token usage, and pricing snapshot;
- preserves raw responses and failures;
- cannot access Arabic/reserved datasets;
- uses the already-frozen cases/prompts/policies;
- enforces the independent `authorized_scope` invariant before generation and application.

GitHub Actions is a suitable candidate if the repository owner places API credentials in repository/environment secrets and explicitly authorizes the budget. Secrets must never be pasted into chat or committed to the repository.

## Required user authorization before any paid call

The live matrix remains blocked until BOTH are true:
1. auditable access to two distinct provider/model identities is confirmed;
2. the user explicitly approves a monetary/token ceiling.

No API call is authorized by this document.

## If access is unavailable

Retain `ACCEPT_BLOCKED_CHECKPOINT`. Do not replace missing providers with an untracked assistant, do not begin HW1-EN/DR, and do not weaken the experiment.
