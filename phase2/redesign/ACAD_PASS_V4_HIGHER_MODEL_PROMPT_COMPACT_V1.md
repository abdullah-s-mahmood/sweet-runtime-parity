# ACAD_PASS V4 — COMPACT HIGHER-MODEL REVIEW PROMPT V1

Use this exact prompt with the higher model:

Review ACAD_PASS V4 pre-gold measurement readiness.

Repository:
`abdullah-s-mahmood/sweet-runtime-parity`
Branch:
`phase2-arabic-eval`

Read ONLY these first:
1. `phase2/redesign/ACAD_PASS_V4_PRE_GOLD_HIGHER_MODEL_REVIEW_PACKET_V1.md`
2. files explicitly referenced by that packet, only as needed to verify a finding.

Task:
Act as an independent adversarial reviewer. Do NOT open or request project gold, do NOT estimate linguistic performance, and do NOT redesign unrelated parts of ACAD_PASS.

Return a concise verdict:
- `PROCEED`, `MODIFY`, or `BLOCK`
- only BLOCKER/MAJOR findings first; MINOR/NOTE only if materially useful
- answer the packet's 30 questions compactly
- for each required repair, name exact file/function/semantic rule
- state whether gold may be authorized after the listed repairs
- independently red-team denominator freezing, provenance/family semantics, P1+P3 same-family handling, M04, M05 whole-action semantics, punctuation separation, single-reference interpretation, historical C_F exposure, action-set identity, and hidden gold leakage to P4/selector/consensus
- challenge KEEP/REPAIR/REPLACE/ADD/DEFER assumptions only where evidence justifies it
- use fresh external research ONLY if a missing technical fact materially affects the verdict; otherwise conserve tokens and rely on the frozen packet/repo evidence

Output maximum: ~1200 words.
Do not restate the project history.
Do not praise the work.
Focus on actionable scientific/implementation defects and the minimum safe path forward.
