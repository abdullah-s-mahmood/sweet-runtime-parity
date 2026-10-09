# ACAD_PASS — Adapted PICOX Executable Mechanics Preflight Freeze V1

Date: 2026-10-09

State:
`FEDERATION_PICOX_EXECUTABLE_MECHANICS_PREFLIGHT_PASS`

Run:
`37897788557`

Artifact:
`11601460910`

Digest:
`sha256:633707b4da39d90d2bcd6bee83db65343eefe09f34381c95c3d5909d2b7f6e6c`

Scientific training:
false

Benchmark TEST used:
false

Verified prospectively:
- upstream-compatible five-way boundary decoding;
- immutable boundary grid {.20,.25,.30,.35,.40,.45,.50};
- START/END Cartesian candidate generation with start<=end;
- four-way multi-label span decision at fixed sigmoid threshold .50;
- same-class NMS exactly follows upstream implementation: IoU > 0 and the longer overlapping span is dropped;
- different-class overlaps are preserved;
- checkpoint policy = FINAL_EPOCH_ONLY;
- no TEST-time threshold tuning;
- adapted boundary train batch = 8;
- span train batch = 16.

The boundary batch size 8 is a prospective adaptation that makes explicit the upstream TrainingArguments default because the upstream notebook did not set it explicitly.

Remaining before scientific PICOX fitting:
- per-fit matched data manifest binding;
- GPU/VRAM runtime qualification;
- full model-weight/runtime availability on the selected execution backend.

No scientific comparator fit is authorized by this file alone.
