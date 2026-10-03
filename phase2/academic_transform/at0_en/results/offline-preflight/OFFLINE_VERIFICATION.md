# AT0-EN Offline Verification

Run from `phase2/academic_transform/at0_en`:

```bash
python tests/run_preflight.py
python tests/run_portability_audit.py
```

Expected results for this checkpoint:

- frozen engineering fixtures: `30/30 PASS`;
- language portability audit: `10/10 PASS`;
- live experiment: `NOT_RUN` until two authorized distinct model identities and an explicit cost ceiling are frozen.

The first preflight attempt was `29/30` because source matching did not independently enforce the pre-authorized paragraph scope. The implementation was repaired by adding an independent `authorized_scope` invariant; the complete suite then passed `30/30`.