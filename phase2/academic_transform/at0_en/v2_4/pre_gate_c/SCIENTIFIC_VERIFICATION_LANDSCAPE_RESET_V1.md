# ACAD_PASS — Scientific Verification / Revision Landscape Reset V1

Date: 2026-10-04
Status: STRATEGY CORRECTION / NO EXTERNAL V2.4 EXECUTION

## 1. Why this reset was necessary

The difficulty encountered in H1 was not caused by a shortage of related research, benchmarks, or applications.

The actual problem was methodological overloading:
we were repeatedly asking a single external resource to prove several different ACAD_PASS constructs at once.

Modern literature treats these as distinct tasks:
- scientific text revision;
- meaning preservation;
- factual consistency;
- claim/evidence verification;
- citation verification;
- document-level comprehension;
- multimodal scientific evidence;
- abstention/uncertainty;
- preservation across iterative revision.

Therefore ACAD_PASS should reuse the strongest external resource for EACH construct rather than force one benchmark to validate the entire system.

## 2. Strong recent research resources identified

### Scientific revision / preservation

1. Identifying Reliable Evaluation Metrics for Scientific Text Revision
   ACL 2025
   DOI: 10.18653/v1/2025.acl-long.335

Key implication:
scientific revision correctness remains difficult; hybrid task-specific evaluation is stronger than generic similarity or LLM-as-judge alone.

2. ParaRev
   Scientific paragraph revision dataset with manually annotated revision instructions.
   2025.

3. XtraGPT
   ACL 2026.
   Context-aware academic paper revision.
   7,000 papers / ~140,000 instruction-response pairs.
   Explicitly targets section-level conceptual coherence during revision.

4. Mr Dre
   ACL 2026.
   Multi-turn research-report revision.
   Shows 16–27% regression in previously covered content/citation quality during iterative revision.

5. TACL 2024 meaning-preservation via reading comprehension.
   Human evaluation explicitly tests whether simplification preserves information needed to answer comprehension questions.

### Long-document/scientific factuality

6. LongSciVerify / LongDocFACTScore
   LREC-COLING 2024.
   Human fine-grained factual consistency for long scientific summaries.

7. FENICE
   Findings ACL 2024.
   Claim extraction + NLI alignment; human factuality annotations for long-form summarization.

8. Stress Testing Factual Consistency Metrics for Long-Document Summarization
   ACL 2026.
   Seven meaning-preserving perturbation families.
   Demonstrates instability of current factuality metrics under semantically equivalent rewrites.

9. LLM-Oasis
   Computational Linguistics 2026.
   Large end-to-end factuality-evaluation resource with a human gold test set.

### Scientific claim / evidence verification

10. SciVer
    ACL 2025.
    3,000 expert-annotated examples / 1,113 papers.
    Expert supporting evidence.
    Multimodal scientific claim verification.

11. CLAIM-BENCH
    IJCNLP-AACL 2025.
    Scientific claim-evidence extraction and validation.

12. SciClaimEval
    LREC 2026.
    1,664 expert-validated samples / 180 papers.
    Authentic scientific claims with support/refute evidence and multimodal evidence.

13. Table-Text Alignment / SciTab extension
    Findings EMNLP 2025.
    Human cell-level rationales for scientific table claim verification.

14. ClimateViz
    EMNLP 2025.
    49,862 scientific claims over 2,896 expert-curated visualizations.
    Support/refute/NEI with structured explanations.

15. Matter-of-Fact
    EMNLP 2025.
    8.4k scientific/materials claims with expert feasibility verification.

### Citation verification

16. SciCiteVal
    LREC 2026.
    >1,000 manually annotated citations.
    Correct / Incorrect / Unrelated with fine-grained error taxonomy.

17. CiteAudit
    2026.
    Human-validated scientific citation verification framework.
    Claim extraction, evidence retrieval, passage matching, reasoning, calibrated judgment.

18. SciTrue
    EACL 2026 system demo.
    Explicit claim-component-to-source traceability.
    Human evaluation over 300 attributions.

### Biomedical/document quality beyond factuality

19. FactPICO
    ACL 2024.
    Expert critical RCT fidelity/preservation.
    Current H1 hard resource.

20. RoBBR
    2024/2025.
    >500 biomedical papers / ~2,000 expert risk-of-bias annotations.
    Important future evidence-quality construct, not rewrite fidelity.

21. BioPulse-QA
    2026.
    2,280 expert-verified biomedical QA pairs from recent drug labels, trials, guidelines.
    Strong robustness/freshness diagnostic candidate.

22. ReFACT
    EACL 2026.
    1,001 expert-annotated scientific QA pairs with span-level confabulation errors.
    Important scientific unsupported-content diagnostic.

## 3. Existing applications / systems show the same decomposition

### Scite
Strong in:
- citation-statement verification;
- supporting / contrasting / mentioning classifications;
- traceability to source sentences.

### Elicit
Strong in:
- evidence search;
- screening;
- extraction;
- systematic review;
- sentence-level supporting quotes/citations;
- auditable review workflows.

### Paperpal
Strong in:
- academic writing/editing;
- reference integrity;
- DOI/metadata checking;
- retraction/reference relevance checks;
- hallucinated-reference detection.

### SciSpace
Strong in:
- literature search;
- document analysis;
- data extraction;
- writing / cited drafting;
- research agents.

### IPPOLIS Write
Open-source scientific-document formal-integrity checker:
- grammar;
- acronyms;
- bibliography/database checks;
- figure/table referential integrity;
- link consistency.

### SciTrue
Research prototype/system:
claim component -> explicit scientific source -> inspectable evidence traceability.

No reviewed product/resource found currently implements the full ACAD_PASS loop as one validated system:

`UNDERSTAND -> PROTECT -> TRANSFORM -> INDEPENDENTLY VERIFY -> DETECT RISK -> REPAIR -> RE-VERIFY -> ESCALATE -> PRESERVE -> DELIVER`

This is important:
ACAD_PASS should not reinvent mature components, but its contribution is the controlled integration, independent verification, preservation contract, repair loop, uncertainty handling, and auditability.

## 4. Strategy correction

Old tendency:
find one benchmark/resource that proves H1 broadly, then repeat for other tracks.

New strategy:

`CONSTRUCT-MODULAR EXTERNAL VALIDATION`

Each ACAD_PASS function gets the best-matched external evidence source.

### H1 — transformation fidelity / preservation

Hard:
`FactPICO`
for source-bounded critical RCT fidelity/preservation.

Complementary:
- PLABA authentic transformation diagnostics;
- scientific revision datasets/evaluations (Jourdan/ParaRev/XtraGPT) for broader revision utility;
- LongSciVerify for long scientific factual consistency;
- human meaning-preservation/reading-comprehension benchmark for content preservation.

No requirement that any one resource prove every H1 property.

### H2 — claim/evidence support

Preferred modern candidates to audit before execution:
1. SciVer
2. CLAIM-BENCH
3. SciCiteVal / CiteAudit for citation-specific support
4. SciFact retained as a clean established baseline

Do not automatically keep SciFact as the only primary resource merely because it was chosen earlier.

### H3 — relation/local evidence binding

Preferred modern candidates:
1. SciClaimEval
2. SciTab/Table-Text Alignment
3. CLAIM-BENCH
4. QASemConsistency retained where its exact relation contract is useful

### H4 — metamorphic / adversarial preservation

Use:
- ACAD_PASS controlled META oracle families;
- ACL 2026 long-document meaning-preserving perturbation research to improve family coverage;
- no external benchmark may replace the independent oracle requirement.

### Citation/reference integrity track

Future explicit subtrack:
- SciCiteVal
- CiteAudit
- Scite/Paperpal-like reference checks as product/engineering comparators

This should not be silently folded into H2 without preserving its distinct construct.

## 5. Why strong intelligence does not remove the benchmark problem

A smarter verifier may outperform existing published systems.

But evaluation quality cannot be created by intelligence alone.

The verifier must not:
- invent unavailable human gold;
- infer a benchmark label and then score itself against that inference;
- silently redefine task semantics;
- use semantic helper logic in the adapter that supplies capability being evaluated.

Recent literature itself confirms the problem:
- scientific-revision metrics struggle with correctness;
- long-document factuality metrics are unstable under meaning-preserving transformations;
- expert scientific claim verification remains substantially above current model performance;
- multi-turn research agents regress on previously preserved content;
- end-to-end medical fact-checking has construct-validity problems.

Thus the obstacles encountered are evidence that our evaluation discipline is appropriate, not evidence that relevant literature is absent.

## 6. Practical effect on current H1

Do NOT abandon FactPICO V5.

FactPICO remains well matched to:
`source-bounded critical RCT-element fidelity`

But do not describe it as the entire proof of transformation safety.

After H1 adapter/manifests are frozen, before opening broader Gate C claims:
perform a resource audit for:
- scientific revision benchmark(s);
- LongSciVerify;
- current 2025–2026 claim/citation benchmarks.

This can increase external validity without contaminating the current frozen FactPICO evaluation.

## 7. Product/novelty implication

ACAD_PASS novelty should NOT be framed as:
“the first AI tool that checks scientific text.”

That claim would be weak.

A stronger defensible direction is the integrated audited pipeline:

- protected scientific assertions/relations;
- transformation with explicit preservation obligations;
- verifier independent of transformation;
- evidence/source traceability;
- non-compensatory safety gates;
- deterministic/metamorphic drift checks;
- repair and re-verification loop;
- abstention/escalation;
- preservation of document structure/provenance;
- reproducible frozen evaluation artifacts.

Existing systems provide important partial capabilities, but the literature repeatedly treats these capabilities separately.

## 8. Current decision

Landscape finding:
`MANY STRONG RESOURCES EXIST`

Problem diagnosis:
`CONSTRUCT MATCHING + EVALUATION INTEGRITY, NOT RESOURCE SCARCITY`

Strategy:
`REUSE MORE / FORCE LESS`

Current execution path remains:
`FACTPICO H1 ADAPTER + INPUT/GOLD MANIFEST IMPLEMENTATION FREEZE`

No external prediction is authorized.
