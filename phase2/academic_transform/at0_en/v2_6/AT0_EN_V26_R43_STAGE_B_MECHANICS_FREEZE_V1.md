# AT0 EN V2.6 — R4.3 Stage-B Mechanics Freeze V1

Date: 2026-10-07
Status: MECHANICS PASS; NO STAGE-B SCIENTIFIC RUN EXECUTED

## Identity

Run: `37540302867`
Conclusion: `success`
Head: `fb5091acc7d111d7e3d19f26ead46050eae99626`

Artifact:
- ID `11447889249`
- digest `sha256:d35ad79f82cb64d75f9e1f25a3367f1b329962945ec47e07bdac5d49e6647a9c`

## Mechanics result

State:
`R43_STAGE_B_MECHANICS_PASS`

Synthetic-only H0:
- parameters = 579461
- output shape = [8,5]
- finite forward/backward = true
- smoke loss = 1.5957911015

Synthetic-only H1:
- parameters = 662666
- output shape = [8,5]
- finite forward/backward = true
- smoke loss = 1.5101152658

Exact H1-H0 parameter difference:
- 83205

These match the frozen design/preflight parameter identities.

## Stage-B implementation safeguards

Prepared implementation:
`r43_stage_b_h0_h1_diagnostic.py`

Before any H0/H1 scientific training it must:
1. verify exact frozen source/split identities;
2. load only frozen FIT-only Stage-A ancestors;
3. generate native SELECT candidates from FIT-only B;
4. compute candidate ceiling FIRST;
5. STOP before H0/H1 fitting if any class has max candidate recall <0.20 or fewer than 10 exact candidate TPs;
6. materialize native FIT errors only from FIT;
7. preserve exact static-manifest parity and gold precedence;
8. feed H0/H1 identical examples and contextual features;
9. keep the encoder frozen;
10. use only the frozen threshold grid and scientific gate;
11. stop before historical DEV or external protected tests.

## Governance

This run used mechanics-only synthetic tensors. No TRAIN, SELECT, DEV or TEST scientific examples were evaluated by this mechanics run.

Stage B has NOT been launched.

Exact next dependency:
successful, frozen Stage-A ancestor completion.
