# Public human-gold federation review — COMPLETE

Finalized 2026-10-09 (Asia/Baghdad). Canonical deliverable: `FINAL_PUBLIC_HUMAN_GOLD_FEDERATION_REVIEW_V1.md` in this directory. Verdict: **PROCEED_FEDERATION_WITH_CHANGES**. The complete review answers all 40 required decisions and specifies dataset roles, architecture/losses, sequence, benchmark/metric rules, reset, finite budget, stopping and claim limits. Evidence copies and SHA256 manifest are saved locally.

**Do not restart this review or execute training automatically.** Next project action, if separately requested: materialize and review the protocol/provenance closure before the first fit. No model training, GitHub changes, gold generation, new RCT collection, VERIFY_INTERNAL access, or historical reruns were performed. R44C remains consumed/frozen. No candidate benchmark was falsely certified eligible.

The checkpoints below record the completed review's progression; preliminary wording is superseded by the canonical final file.

Read-only consultation. No local qualified annotators available. Do not collect new RCTs, generate gold, train, rerun R44B/R44C, open VERIFY_INTERNAL or modify GitHub. Prior R44C remains consumed/frozen. New objective is comparable public benchmark performance, not fresh prospective clinical validation.

Repository branch at0-en-v2.6-dev pinned for review at 5f584c5a21a0639bf9d5929166e2eaf69ce6d521. Four requested documents read and saved under evidence/. Need complete source-code/provenance audit and 2024–2026 literature review. Exposure inventory incomplete; potential critical source misattribution: R44 source is EBM-NLP_mod but inventory groups it under PICO-Corpus and calls EBM-NLP_mod unresolved. Verify without protected row access.

Do not assert any benchmark test remains eligible until documentary split/exposure audit. Need final verdict, dataset/benchmark matrices, concrete minimal architecture/loss/training/attempt limits, 40 decisions and reset protocol. User wants progress saved at stages.

## Verified material findings (second checkpoint)

- R43 source contract explicitly pins EBM-NLP_mod fold1/train.txt at BIDS-Xu-Lab/section_specific_annotation_of_PICO commit bc4b878773192f38b2600ec830ca4208b82f7dc0. Its 400 documents feed R43/R44; R44 FIT 320 becomes DESIGN 256 + protected VERIFY_INTERNAL 64. The new exposure inventory misattributes this lineage to PICO-Corpus. EBM-NLP_mod is definitely exposed. Do not open protected rows to repair the inventory.
- AlpaPICO repository commit 54904417d9d9ab436eb8525f2112b6ea13fa385d: metric.py uses sets of extracted strings, collapses repeated mentions, and increments TP when both lists are empty. prediction.py evaluates OUT/INT/PAR. This code path is not strict occurrence-level exact P/I/C/O span evaluation. Do not assume every published paper number came from that path.
- Original EBM-NLP uses P/I/O; hierarchical control subtype does not make it equivalent to native separate-C flat annotation. Preserve its schema in an auxiliary head.
- TrialSieve has rich human types; NonStudyDrug is not a valid universal C label. C-TrO arm relations do not automatically distinguish experimental from comparator roles. No automatic flat-PICO conversion.
- EvidenceOutcomes covers Results/Conclusions and includes 140 EBM-NLP abstracts. It is not independent of that parent corpus, and its O construct/scope differs from Title/Methods native core.
- DISTANT-CTO semantic intervention annotations are weak labels, not proven independent human experimental/control roles. Large counts do not establish direct C supervision.
- Modern/PICO systems use incompatible schemas/metrics. PICOX merges I/C; FinePICO is fine-grained semi-supervision; AlpaPICO scorer needs reconciliation; GPT-4o 342/350 semantic verification is not exact-span precision.
- Do not certify all five published folds as independent/cross-trial: audit fold construction, repetition and trial-family overlap from manifests without opening protected text/gold. Preserve official test populations; decontaminate training sides, or label any changed protocol distinctly.

Research covered primary 2024-2026 sources for PICOX, FinePICO, AlpaPICO, TrialSieve, EvidenceOutcomes, OpenBioNER/v2, GLiNER-BioMed, BioClinical ModernBERT; older primary EBM-NLP/native section-specific corpus/C-TrO/DISTANT-CTO sources are necessary provenance. Still investigating a 2026 PICO LLM paper and a newly listed Zenodo corpus; no data collection or model execution.

Tentative verdict: PROCEED_FEDERATION_WITH_CHANGES. Existing public human annotation can support development and legitimate public-benchmark publication, conditional on provenance/split closure. It cannot restore unseen status or guarantee SOTA/clinical validation. Final architecture and finite attempt budget not yet frozen. Next: finish source checks, write complete 40-decision protocol and exact audit blockers, save final review and evidence index.

## Third checkpoint: research complete enough for decision

- DISTANT-CTO paper Section 4.3 explicitly merges Intervention and Comparator into one Intervention class, with semantic subtypes. Packet's direct weak I/C role-learning premise must be removed.
- Source Hu utils_ner.py update_data_to_max_len uses gold O/non-O labels to place chunk boundaries, and PICO_ner.py calls it on train/dev/test. Historical R43 audit proved zero inserted splits on its pinned training file; effect on future benchmark files is unverified. New preprocessing must be text-only. Paper's historical numbers remain intact; matched comparator adaptation must be disclosed.
- GLiNER-BioMed base config verified max_width=12 (max_len=2048); cannot assume unrestricted long PICO-span capacity. Paper's evaluation excludes discontinuous spans and uses entity-preserving chunking. Do not inherit gold-dependent preprocessing.
- BioClinical-ModernBERT-base pinned HF revision c3648aa87af95837c809e6f0c5f85d08160db437; MIT. ModernBERT-bio-base 2026 revision ee044b78afd30bfcb6dbb190c44d5472e535bce9; Apache-2.0. 2026 paper does not uniformly beat PubMedBERT on short-context NER; choose only one prespecified modern-encoder challenger, not an open search.
- Hao et al. JMIR 2026 DOI 10.2196/91215 uses three P/I/O classes and exact mention-text matching, not established occurrence-offset P/I/C/O scoring. Code repository zeyuanhao-cs/PICO. Treat as task-mismatched unless adapted and re-evaluated prospectively.
- Sundaram 2026 Zenodo 21918559 paper downloaded/read (paper only, no corpus collected). Labels explicitly derived from ClinicalTrials.gov fields without manual annotation; P/I/O token classification. Not new independent human gold. Exclude from first campaign.
- Primary evidence copies saved under evidence/, including R43/R44 contracts, Hu evaluation/preprocessing code, AlpaPICO metric code, corpus/model READMEs, model metadata and the 2026 Sundaram paper.

Final proposal being written: six fixed development arms (token/span x native/human federation, one modern encoder challenger, one strictly role-agnostic weak-label ablation); no LLM teacher, new pseudo-label generation, large verifier, stacking or relation module in first campaign. Test identities remain conditionally eligible pending custodian audit, not invented PASS.