# M2-H Environment Architecture Decision

Date: 2026-09-30
Status: FROZEN BEFORE PREFLIGHT V2

## Decision

**Use dual-environment isolation. Do not legacy-pin CAMeL Tools merely to force H1 and H3 into one Python environment.**

## Evidence

H1 / SWEET official text-editing repository documents:
- Python >=3.10
- PyTorch 1.12.1
- Transformers 4.30.0

Current CAMeL Tools documentation/package metadata requires:
- Python >=3.11

The failed preflight confirmed the practical incompatibility:
- H1 stack installed under Python 3.10.
- current frozen CAMeL Tools resolved to 1.6.0.
- CAMeL Tools required scikit-learn >=1.8.0.
- the Python 3.10 environment could not satisfy that dependency.
- failure occurred before CAMeL data installation or inference.

Older CAMeL Tools releases (e.g. 1.5.x) support Python 3.10, but selecting them solely to share an environment would introduce an unnecessary legacy constraint.

## Architecture

### Environment H1
Purpose:
- SWEET explicit-edit candidate generation.

Runtime:
- Python 3.10
- PyTorch 1.12.1
- Transformers 4.30.0
- Hugging Face checkpoint: CAMeL-Lab/text-editing-qalb14-nopnx

Output contract:
- JSON/JSONL structured edit candidates only.

### Environment H3/H4
Purpose:
- CAMeL morphology;
- deterministic orthographic/boundary validation;
- H4 evidence generation.

Runtime:
- Python 3.11+
- current frozen CAMeL Tools source revision where reproducible.

Output contract:
- JSON/JSONL evidence records only.

### Fusion boundary
The two environments may communicate only through explicit serialized artifacts:
- case_id
- exact span
- proposed operation/replacement
- evidence fields
- component version/hash
- decision/confidence fields where applicable.

No Python object sharing and no hidden shared model state.

## Why this is preferred

1. Preserves H1's published reproduction environment.
2. Preserves current CAMeL compatibility instead of forcing legacy dependencies.
3. Improves component independence.
4. Reduces dependency coupling.
5. Makes provenance clearer: each component has its own lockfile and hashes.
6. Better matches the scientific hypothesis that heterogeneous evidence should be independently reproducible.

## Rejected alternative: legacy CAMeL pin

Rejected as the default path because:
- older CAMeL versions can support Python 3.10, but this is an engineering workaround rather than a scientific requirement;
- it increases maintenance debt;
- it risks silently changing morphology behavior relative to current data/tooling;
- it weakens long-term product architecture.

Legacy pin remains only an emergency fallback if current CAMeL cannot be reproduced independently.

## No scientific result change

This decision changes execution architecture only.

Measured Arabic verification performance: UNCHANGED.
Deployment status: REVIEW-first.
