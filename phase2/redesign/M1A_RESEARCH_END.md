# M1-A — Fresh Research End

Date: 2026-09-30  
Status: END-OF-ITERATION RESEARCH COMPLETE

## Question revisited

Can ACAD_PASS continue serious Arabic correction/verification research when the project owner cannot currently recruit qualified Arabic-language experts for direct adjudication?

**Answer: yes for calibration and feasibility research, but not by pretending that AI judgments are human gold.**

The best-supported workaround is to use multiple, independently produced traces of prior human/expert correction as external evidence, reserve some of that evidence for later confirmation, and explicitly leave dimensions unsupported by those corpora unresolved.

## Evidence confirmed at end

### QALB
The QALB correction work remains the strongest large-scale source for Arabic GEC source→human-corrected reference pairs and official edit structure. The published annotation work reports repeated quality-control/IAA procedures and also documents valid correction variation. Therefore QALB can ground reference-supported correction and completeness, but a non-reference alternative cannot automatically be labeled wrong.

### ZAEBUC
ZAEBUC provides an independent domain: university student writing, with raw and manually/professionally corrected Arabic. The published corpus describes a quality-controlled correction process and public raw/corrected versions. This reduces dependence on QALB and is closer to academic writing than social-media/native comment text, although it is still student essays rather than scientific manuscripts.

### A7'ta
A7'ta provides expert-book-derived MSA error/correction pairs organized by linguistic categories. The published data article reports 470 erroneous/error-free counterparts, manually extracted from a book intended as a guide to correct Arabic usage.

The pinned GitHub snapshot yielded **463 parseable non-empty aligned pairs**, seven fewer than the paper's 470. M1-A does not silently coerce the count to 470. The discrepancy is preserved as a QA issue (7/470 = 1.49%) before any use of the entire corpus as exhaustive evidence.

### Manual Arabic spelling-error correction corpus
The ISLRN resource “Manual Arabic spelling-errors correction for collected documents” records real spelling mistakes made by a group of users while editing Arabic documents and includes document/sentence/error-type structure. This is useful as future orthographic robustness evidence, but it is not promoted to Tier S because its provenance is human error collection rather than expert linguistic post-editing.

### Manually annotated 360-sentence syntactic reference corpus
The paper *An innovative approach to autocorrecting grammatical errors in Arabic texts* reports a manually annotated 360-sentence reference corpus: 30 syntactically correct and 330 ungrammatical learner sentences, including agreement, case-ending and definiteness errors. This is promising targeted syntax evidence, but the currently verified public evidence does not yet establish a reusable open paired correction artifact with provenance as strong as QALB/ZAEBUC/A7'ta. It remains a candidate secondary source pending data-access/provenance audit.

### Tibyan
Tibyan uses professional linguistic review and iterative correction, but its large corpus is ChatGPT-augmented. It is therefore useful for error-type coverage, adversarial/stress testing, and later generalization—not as the primary independent gold for M1.

### Arabic Learner Corpus thesis
Alfaifi's PhD work contributes a systematic Arabic learner corpus methodology and a 29-type error tagset across five broad categories, supported by a large multi-institution collection effort. This is valuable for taxonomy and annotation design, but not all ALC material constitutes full source→expert-corrected sentence pairs.

### Human evaluation of Arabic LLM corrections (Mohi et al., 2026)
A recent PeerJ study used four native-speaker experts to rate Arabic corrected sentences and explanations on grammatical correctness, fluency, meaning preservation, and explanation quality, with Fleiss' kappa reported. This is directly useful for **M2 rubric calibration**, particularly because it confirms that correctness, fluency and meaning preservation should be separate axes.

## End conclusion

A direct Arabic expert hired specifically for ACAD_PASS is no longer an immediate prerequisite for:
- M1 contract calibration;
- building controlled complete/incomplete Arabic correction cases;
- testing a strong verifier in M2;
- testing overcorrection/KEEP behavior.

A direct independent expert remains important later for:
- project-local ambiguous cases;
- scientific/academic Arabic fidelity;
- publication-grade external confirmation;
- final auto-apply claims.

The absence of such a reviewer is therefore downgraded from **blocking dependency** to **late-stage validation risk**.
