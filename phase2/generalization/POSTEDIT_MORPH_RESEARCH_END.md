# Post-Edit Stability & Morphological Identity — Research End

Date: 2026-09-29

The repaired diagnostic confirms that fixed-point stability is not a correctness oracle: only 1/16 unsafe events was captured by target/window stability. Contextual morphological identity is more informative but still captured only 4/16 unsafe and 2/4 wrong events.

Fresh external research is consistent with this outcome:
- edit-level voting can mitigate over-correction but cannot guarantee correctness;
- Arabic GEC remains highly context- and morphology-sensitive;
- CamelParser2.0 exposes dependency relations, POS and rich morphology across Arabic genres, providing a structurally different signal from model agreement or token morphology;
- current Arabic grammar benchmarks continue to show substantial deficits, so held-out validation and review remain mandatory.

Research conclusion:
the next experiment should target syntactic governor/dependent compatibility and repair completeness rather than add voters, increase fixed-point radius, or tighten morphology identity.

CamelParser2.0 is preferred for a consumed-slice diagnostic because it is open source and can produce CATiB/UD dependency parses from raw/preprocessed Arabic text. Any policy derived from that diagnostic must still be frozen before a new disjoint slice.
