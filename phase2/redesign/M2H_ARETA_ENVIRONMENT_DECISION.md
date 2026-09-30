# M2-H ARETA Isolated Environment Decision

Date: 2026-09-30
Status: FROZEN BEFORE ARETA EXECUTION

ARETA is isolated from both H1 and H3 runtime environments.

Reason:
- the enhanced ARETA code is frozen in arabic-gec revision 8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf;
- its dependency file pins an older scientific Python stack;
- current CAMeL Tools 1.6.0 requires Python >=3.11;
- CAMeL Tools 1.5.0 supports Python >=3.7,<3.11 and is therefore selected for the ARETA diagnostic environment on Python 3.8.

Frozen diagnostic runtime:
- Python 3.8
- camel-tools==1.5.0
- exact ARETA requirements.txt from the frozen arabic-gec revision
- morphology-db-msa-r13

This environment is ONLY for ARETA diagnostic enrichment.

It must not replace:
- H1 SWEET environment;
- H3 current CAMeL morphology environment.

Scientific consequence:
ARETA labels remain development-only proxy/diagnostic evidence, never independent gold.
