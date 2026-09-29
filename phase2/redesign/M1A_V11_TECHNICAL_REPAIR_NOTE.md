# M1-A v1.1 Technical Repair Note

Date: 2026-09-30

Run 36640832337 produced complete v1.1 feasibility counts but exited NOT_READY because two negative-polarity safety facts were placed inside an all-true criterion dictionary:

- `forbidden_splits_read = false`
- `raw_arabic_persisted = false`

The data state was safe, but the aggregator interpreted these desired false values as failed true-valued criteria.

Repair:
- rename to `no_forbidden_splits_read = true`;
- rename to `no_raw_arabic_persisted = true`;
- make ZAEBUC line-count equality explicit by recording raw_lines and corrected_lines separately.

No threshold, source, split, case family, sample cap, or scientific success criterion is changed. The counts from run 36640832337 are preserved as pre-repair evidence.
