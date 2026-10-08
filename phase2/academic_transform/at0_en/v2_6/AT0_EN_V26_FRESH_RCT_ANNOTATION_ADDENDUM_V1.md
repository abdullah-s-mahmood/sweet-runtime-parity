# ACAD_PASS — Fresh RCT PICO Annotation Addendum V1

Date: 2026-10-08

State:
`ANNOTATION_ADDENDUM_FROZEN_FOR_READINESS_ONLY`

Annotation is NOT authorized yet.

Governing protocol:
`AT0_EN_V26_FRESH_RCT_ACQUISITION_PROTOCOL_FREEZE_V1.md`

Governing independent review:
`FRESH_RCT_INDEPENDENT_ACQUISITION_REVIEW_V1.md`

## 1. Pinned source manual identity

Repository:
`BIDS-Xu-Lab/section_specific_annotation_of_PICO`

Pinned commit:
`bc4b878773192f38b2600ec830ca4208b82f7dc0`

Repository tree:
`aa10ba9a8a973129bd797f9a5946b35cb44efea5`

Manual path:
`Annotation guidelines.pdf`

Git blob SHA-1:
`f67df5da9507c562cbeab7ad497e816bde58a02a`

Blob size:
`204547 bytes`

This addendum adopts that pinned manual plus the prospective decisions below.
If source-manual text and this addendum conflict, STOP for protocol review rather than silently choosing a rule.

## 2. Annotation schema

Version:
`FRESH_PICO_TITLE_METHODS_V1`

Classes:
- P = explicit enrolled/recruited participant description.
- I = assigned experimental treatment/procedure.
- C = explicitly designated reference/control treatment, including placebo, sham, usual care or no treatment.
- O = measured endpoint/test used as an endpoint.

Outside is not Outcome.

Do not infer an entity absent from text.

A test used as the assigned treatment is I.

Stand-alone numeric results and statistical tests are not O.

## 3. Scope

Primary supplied scope:
`Title + Methods`

Title:
- P allowed;
- I allowed;
- C allowed;
- O NOT annotated in title.

Full abstract:
retained as role-disambiguation context only.

Structured abstracts:
prefer PubMed `NlmCategory=METHODS`.

Where NlmCategory is absent, map the following headings to Methods:
- Methods
- Materials and Methods
- Patients and Methods
- Design
- Setting
- Participants
- Interventions
- Main Outcome Measures

Other headings are outside primary annotation scope.

For unstructured/mixed abstracts:
- annotator A marks contiguous methods clauses;
- annotator B independently marks them;
- adjudicator resolves;
- observed-results clauses are excluded;
- no text may be invented.

A document with no in-scope methods clause is a valid empty Methods input and is NOT excluded.

## 4. Participant boundaries

P uses the complete participant noun phrase with attached descriptors.

Include attached articles.

Exclude:
- introductory prepositions;
- explicit eligibility-criteria lists that are not part of the participant noun phrase.

Do not shorten P to a disease dictionary term if the text expresses a fuller participant phrase.

## 5. Intervention/comparator boundaries

I/C include preceding:
- dose;
- formulation;
- frequency modifiers
when syntactically attached to the treatment mention.

Exclude trailing:
- dose;
- duration;
- following prepositional material
when the pinned manual excludes it.

Generic group labels are not treatment entities by themselves.

Coordinated treatments are separate mentions where text supports separate contiguous spans.

Abbreviation and full-form occurrences are separate mentions.

Prospective resolution:
if a postmodifier is required to complete a lexicalized treatment name, follow the pinned source-manual restriction and record omitted context in an annotation note rather than silently switching to clinical-concept boundaries.

## 6. Outcome boundaries

O retains:
- endpoint noun phrase;
- directly attached statistical modifier;
- one endpoint-defining prepositional attachment.

Exclude:
- change/difference introductions;
- measured values;
- comparison clauses;
- extrinsic measurement times.

Preserve intrinsic endpoint timing.

Numeric prefixes that are part of endpoint names are not automatically numerical results.

Composite endpoints:
- retain source-compatible summary mention;
- separately annotate explicitly expressed component mentions;
- subject all mentions to the flat projection defined below.

## 7. Trimming and punctuation

Use zero-based half-open Unicode-code-point offsets.

Trim only outside:
- whitespace;
- delimiter punctuation.

Preserve internal punctuation.

Do not normalize spelling, case or visible Unicode in annotation text.

## 8. Ellipsis/discontinuous meaning

For ellipsis:
- annotate the visible contiguous conjunct;
- store a shared-head link in auxiliary metadata;
- never insert absent words;
- never concatenate discontinuous text into a fabricated span.

No maximum gold-span token length.

## 9. Repetitions

Every in-scope occurrence is a distinct mention.

Title and Methods repetitions remain separate coordinates.

Abbreviation and expansion are separate mentions.

Do not deduplicate semantically equivalent mentions across positions.

## 10. Nested/overlapping spans

Maintain two layers:

### FULL_ANNOTATION_LAYER
Store every independently justified source-schema span, including nested/crossing cases.

### PRIMARY_FLAT_LAYER
1. deduplicate identical `(document,start,end,class)`;
2. sort candidate spans by:
   - decreasing character length;
   - increasing start;
   - increasing end;
3. greedily retain nonoverlapping spans.

Same-coordinate class conflicts:
must be semantically adjudicated before flat projection.

No arbitrary class priority is allowed.

Suppressed nested/crossing spans remain in the immutable auxiliary layer.
Report suppression counts.

Model performance may never influence projection.

## 11. Multi-arm role rules

Each stated tested arm:
`I`

Each explicitly designated reference arm:
`C`

Multiple reference arms:
all may be C.

Role follows local textual arm context, not:
- outcome winner;
- first mention;
- drug dictionary;
- registry role absent from text.

Head-to-head trial with no expressed reference:
- both arms I;
- metadata `NO_EXPLICIT_REFERENCE=true`;
- do not manufacture C.

Intervention shared by all arms without contrastive role:
- I;
- metadata `SHARED_BACKGROUND=true`.

One occurrence jointly referring to tested and reference arms with no separable spans:
- class I;
- metadata `SHARED_ROLE=true`.

Registry metadata may support eligibility/trial-family identity but must not create hidden gold roles absent from model-visible text.

## 12. Annotation independence

Before submission lock, annotators must not see:
- each other's annotations;
- model candidates;
- model classes;
- confidence;
- B/Boundary/J0/J1/R44C outputs;
- split membership;
- target performance.

No semantic AI suggestions.

Mechanical tools may:
- validate offsets;
- validate schema;
- validate Unicode/code-point consistency;
- detect malformed records.

Mechanical tools may NOT suggest semantic span/class decisions.

## 13. Submission lock and adjudication

Annotator A submission is immutable after lock.
Annotator B submission is immutable after lock.

Before disagreement review, adjudicator independently annotates preselected audit samples:
- 40 DEV docs;
- 500 EVAL docs.

Then adjudicator:
- reviews all disagreements;
- reviews complete text for jointly missed spans;
- records resolution reason.

Do not synthesize a span by majority-character voting if nobody independently annotated it.

Unresolved semantic defect:
`GOLD_FREEZE_BLOCKED`

No difficult-document deletion.

## 14. Qualification

QUALIFICATION:
80 documents.

Training/discussion:
first 40.

Blind qualification:
next 40.

Adjudicator fixes blind reference before seeing submissions.

Per annotator require:
- exact typed-span macro F1 >= .85;
- every class F1 >= .80;
- >=10 reference entities/class.

Failure:
`ANNOTATOR_NOT_QUALIFIED_FOR_MAIN_CORPUS`

Do not:
- relax threshold;
- add opportunistic extra examples;
- recycle qualification docs into DEV/EVAL.

## 15. Main-corpus quality gate

Before adjudication report:
- exact typed-span micro F1;
- exact typed-span macro F1;
- per-class exact typed-span F1;
- exact boundary-only F1;
- same-coordinate type disagreement;
- omission/addition counts;
- section-boundary agreement;
- adjudication rate.

Overlap diagnostic:
maximum one-to-one interval matching at character IoU >= .5.

Never call the IoU diagnostic exact agreement.

Require separately on DEV and EVAL:
- exact typed-span micro F1 >= .85;
- each class F1 >= .80.

After adjudication:
- zero unresolved cases.

Failure halts release.

## 16. Immutable outputs per document

Freeze:
- source identity;
- raw text hash;
- scope map;
- annotator A file/hash;
- annotator B file/hash;
- adjudicator audit file/hash;
- adjudication log/hash;
- FULL_ANNOTATION_LAYER/hash;
- PRIMARY_FLAT_LAYER/hash;
- suppression metadata;
- annotation-tool version;
- addendum version.

Corrections:
append-only errata.

No silent replacement.

## 17. Claim boundary

This annotation protocol supports:
`SUPPLIED_TITLE_METHODS_SCOPE_PICO_EXTRACTION`

It does NOT by itself support:
- end-to-end section retrieval;
- full-abstract exhaustive PICO extraction;
- hidden registry-role recovery;
- clinical concept normalization;
- universal overlapping relation extraction.

## 18. Current authorization

Allowed:
- synthetic annotation-schema fixtures;
- offset/schema validators;
- independent review of this addendum.

Not allowed:
- annotating any acquired 2026 RCT;
- qualification annotation before acquisition readiness and split freeze;
- AI semantic preannotation;
- model-driven scope selection.

Checkpoint:
`ANNOTATION_CONTRACT_FROZEN_FOR_READINESS -> WAIT_FOR_ACQUISITION_READINESS`
