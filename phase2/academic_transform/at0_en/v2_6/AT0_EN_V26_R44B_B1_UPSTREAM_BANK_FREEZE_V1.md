# ACAD_PASS — R44-B B1 Upstream Nested-Bank Freeze V1

Date: 2026-10-08
Status: R44-B B1 UPSTREAM COMPLETE / VERIFIED / STOP BEFORE J0-J1 HEAD TRAINING UNTIL SEPARATE AUTHORIZATION

## 1. Official execution

Workflow run:
- `37683637815`
- workflow: `R44-B B1 parallel pair-exclusion upstream`
- head SHA: `2b39d3549cbaeefe3865e8d289a6a8894f81d21d`

Frozen precheck:
- SUCCESS

All 10 unordered pair-exclusion upstream jobs:
- `0-1` SUCCESS — artifact `11515420365` — digest `sha256:c12d0a5ba5ce0f2b4156f2aff89d9992d68c291e203e69cc995051e8abee229d`
- `0-2` SUCCESS — artifact `11516345519` — digest `sha256:5a45d35d182d7e0ee48aa82aa38c0540bde542ddc0dff4e7705c90db3014d6f8`
- `0-3` SUCCESS — artifact `11514979175` — digest `sha256:ca76d0664fd9e8f3e950bc908a650a993a5d39124b48ce0eb5575ecce4f9e6d0`
- `0-4` SUCCESS — artifact `11515213736` — digest `sha256:d25589a18f90511e166e00d129860f768d585c066c7e27ff8334e0ca25b6c850`
- `1-2` SUCCESS — artifact `11512599487` — digest `sha256:d0db8ec0b12048993e721967999cc1b59385984ee45a3decda70e1f3a21e811d`
- `1-3` SUCCESS — artifact `11514774316` — digest `sha256:28d265e6ed18521c3a30e65e744a8148cd7eede62ee5981715b0e37a200c5722`
- `1-4` SUCCESS — artifact `11514343182` — digest `sha256:2649a8cfa94b3068a0a9ff322586af2ff1b285a7d1a8b144075fd608e1d3abeb`
- `2-3` SUCCESS — artifact `11514937307` — digest `sha256:160f5dd01ec15d98ee305f55cbfa84170c163e24dc5f613b651f0301e9567108`
- `2-4` SUCCESS — artifact `11516505701` — digest `sha256:ac94bf5be43a9a5243dff8f2c4d0f9cd796f5f609a6fd740d49be7fb9c352b65`
- `3-4` SUCCESS — artifact `11515154030` — digest `sha256:d4d2e10893a25ef69c11e05d6978b6783382d10f5af74973031fda87d97794ea`

Failures: 0.
Queued at terminal state: 0.

## 2. Nested-bank aggregate

Aggregate job:
- `R44-B pair-bank nested assembly audit`
- SUCCESS
- state: `R44B_PAIR_AGGREGATE_PASS`

Artifact:
- `11515434193`
- digest: `sha256:98383b4bec040f19d6e4076fea1a70dcb406366dfd4bd724d1ad2fac6d2018fb`

Pair count:
- 10 / 10

Outer-fold meta rows:
- outer 0: 1567
- outer 1: 1519
- outer 2: 1499
- outer 3: 1535
- outer 4: 1551

Outer-fold C support:
- outer 0: 68
- outer 1: 66
- outer 2: 71
- outer 3: 69
- outer 4: 71

Interpretation:
- the nested leakage-safe meta-training banks required by the frozen B1 protocol were assembled successfully;
- every outer fold has substantial C support;
- no candidate-ceiling or assembly guard stopped the experiment.

## 3. Immutable label-independent context cache

Context-cache job:
- SUCCESS
- state: `R44B_BASE_CONTEXT_CACHE_PASS`

Artifact:
- `11510422862`
- digest: `sha256:4fdceb511c2067cf81a1ad6c64c039febf99e3c11b9d8baa32b2d73569faa91c`

Verified identities:
- base model SHA256: `3a6d0b156c45ccd8093af83a9ad3d388808eba5a9e15f0032fc0fe068bb92b68`
- DESIGN source SHA256: `f8b49420cb17a5cb3f67f3120f9362b5e6b15fbb148176eab20105790bab1e18`
- context NPY SHA256: `6bb548884cafb2a14e19b7d691b393dcf0ab9b5cc6add14e6ab0a873be33361b`
- index SHA256: `db9a6bae51a4db38d244e9e0a98f44b5dbfb246f694db5397c6e204cd58881dd`

Shape:
- 26,595 tokens x 768
- dtype: float32
- documents: 256
- sentences: 1034

Guards:
- labels_used = false
- VERIFY_INTERNAL used = false
- old SELECT used = false
- protected data used = false

## 4. Scientific meaning

Quality delta:
`IMPROVED — LEAKAGE-SAFE NESTED UPSTREAM SUPERVISION IS NOW PHYSICALLY AVAILABLE AND VERIFIED`

This stage does NOT yet measure J0/J1 final precision/recall or gate passage.
No head training has occurred.
No threshold has been selected.
No protected evaluation has been opened.

R44-A OOF evidence remains frozen and unchanged.

## 5. Frozen boundaries

Still closed:
- VERIFY_INTERNAL 64 docs
- old R4.3 SELECT
- historical DEV/test
- external EBM/COVID/AD tests
- FactPICO
- consumed 60-RCT holdout

No threshold/seed/model-family shopping is authorized.

## 6. Exact checkpoint

`R44B_B1_UPSTREAM_NESTED_BANKS_COMPLETE_AND_VERIFIED`

Next decision boundary:
- perform final adversarial protocol review using the complete upstream evidence;
- if no disqualifying leakage/construct-validity defect is found, issue a separate authorization for the already-frozen J0-vs-J1 nested head experiment;
- J0 remains the preferred simpler model if it passes the frozen gates;
- J1 is escalation only if J0 fails and J1 passes;
- boundary repair remains outside the primary B1 comparison.

Do NOT access VERIFY_INTERNAL or any protected test before the J0/J1 nested result is frozen.
