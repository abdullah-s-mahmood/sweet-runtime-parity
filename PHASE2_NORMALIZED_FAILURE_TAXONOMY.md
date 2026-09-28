# Normalized candidate failure taxonomy — development only

## Observed mechanisms

| Mechanism | Candidate IDs | Effect | Decision |
|---|---|---|---|
| Identity label/no-op | NORM-17-21-0 | R label changes `أن` to itself; no source correction | UNNECESSARY_EDIT; exclude from yield |
| Incomplete case-ending deletion | NORM-21-9-0, NORM-63-24-0, NORM-73-58-0, NORM-61-27-0 | Deletes wrong accusative ending but does not resolve required nominative diacritic | PARTIAL_CORRECTION; review |
| Incorrect defective-noun reconstruction | NORM-38-24-0 | `وساعٍ`→`وساعا` omits obligatory ي of `وساعيًا` | WRONG_CORRECTION; reject |
| Supported base edit, unresolved vocalized output | NORM-23-7-0, NORM-54-34-0, NORM-73-22-0, NORM-63-34-0, NORM-92-23-0 | Accusative alif direction is useful; tanween and source internal marks need explicit realization | No auto-application |
| Case-dependent suffix and mark change | NORM-76-31-0, NORM-81-9-0, NORM-81-18-0, NORM-85-21-0 | Correct base ending needs mood/case, shadda/vowel alignment | Morphological validation before source patch |
| Source-level scientific risk | SCI-DEV-03, SCI-DEV-12 in canonical run 36447653438 | Candidate corrupts `فاصل الثقة` or removes period from `al.` in citation | Strict Scientific remains REVIEW_ONLY |

All 19 candidate source spans were identified, but that geometric property does not establish grammatical or document safety. The 12 automated word matches resolve to nine linguistically supported base operations and three incomplete nominative realizations; only two supported candidates preserve existing diacritics by a simple local letter patch. No normalized candidate was applied. Severity: defective-noun wrong form MEDIUM (grammatical relation); scientific `فاصل` deletion HIGH (technical term); citation punctuation deletion HIGH (citation integrity). These severities describe proposed changes, not delivered errors.
