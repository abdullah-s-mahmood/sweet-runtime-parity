# MP-SEF V4 STAGE1 PACKET LOCK V1

Date: 2026-10-01
Status: FROZEN / SOURCE-ONLY / PRE-INFERENCE
Gold/reference use: NONE
Proposer output used for selection: NONE

## Workflow evidence

Workflow:
`Phase 2 MP-SEF V4 Stage1 Packet Freeze`

Run:
`36871466394`

Head SHA:
`997790d77f8aa40f5721e3fd59f2ccd8130572ae`

Conclusion:
`SUCCESS`

Artifact:
- id: `11167360791`
- name: `mpsef-v4-stage1-packet-v1`
- digest:
  `sha256:64284a4187b1bda2e61dd1a2a5a20752f6791c14b8709a5ffb2aeee2e53dcaac`

## Frozen parent identities

C_F source manifest SHA256:
`051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193`

V4 registry SHA256:
`b448650c571f6c93dffe4825417e4f65d6a8cd02e33bd9551728ceac2b242b1a`

## Packet identities

Cases:
**128**

Clusters:
**128**

Packet SHA256:
`8460900d88656ff25fe4da05d156ba0b31980188e3d1135052ed1825f10087b1`

UID-list SHA256:
`e32b468f27653a1bbabfa5c355483c34ffe9b6e4cb2425c36e6c10b714c104ac`

Cluster-list SHA256:
`95b895d424d404d80a70b5acb8ac8b98fe8b461f8b03c2532a7535853f9a25ca`

Source-row-hashes SHA256:
`5b7f9abc05d4bbfb9a6a336aca1fadd6767fc0dc3a597fdcaed1ad01244a2b29`

## Selection algorithm

1. use only the frozen C_F source-only manifest;
2. rank clusters deterministically by SHA256 over the frozen Stage1 salt and cluster_id;
3. select the first 128 clusters;
4. within each selected cluster select the lowest deterministically ranked UID;
5. final artifact order sorted by UID.

Exactly one UID per selected cluster.

## Data-access assertions

- project_source_loaded: true
- project_source_scope: C_F_SOURCE_ONLY
- reference_content_used: false
- gold_edit_content_used: false
- project_gold_loaded: false
- quality_metric_computed: false
- r_joint_computed: false
- selector_trained: false
- proposer_output_consulted_for_selection: false
- internal_evaluation_opened: false
- stress_diagnostic_opened: false
- reserved_data_opened: false

## Scientific interpretation

The Stage1 packet is now immutable for V4 Stage1.

The packet is NOT:
- a correctness sample;
- an independent generalization set;
- a gold evaluation set;
- a quality-ranked sample.

It is a deterministic source-only engineering/diversity packet.

Any change in:
- UID list;
- cluster list;
- source row;
- registry SHA;
- source manifest SHA;
- selection salt/algorithm

requires a new packet version.

## Next allowed action

Run source-only proposer generation and diversity/provenance diagnostics on this exact packet only.

No gold/reference evaluation is authorized.
