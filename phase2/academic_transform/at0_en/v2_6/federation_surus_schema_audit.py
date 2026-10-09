#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import pathlib
import sys


PINNED_SURUS_COMMIT = "3a61790d5c304dea95fb278f76cc3b1a0ca07564"
EXPECTED_LABEL_IDS = list(range(1, 26))
EXPECTED_CLASS_IDS = list(range(1, 8))
EXPECTED_ARTICLES = 523
EXPECTED_ANNOTATIONS = 48833
PAPER_ANNOTATION_TOTAL = 49538


def sha(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_semicolon(path: pathlib.Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    if not rows:
        raise RuntimeError(f"empty table: {path}")
    return rows


def find_col(cols, candidates, required=False):
    exact = {c.casefold(): c for c in cols}
    for x in candidates:
        if x.casefold() in exact:
            return exact[x.casefold()]
    for c in cols:
        low = c.casefold()
        if any(x.casefold() in low for x in candidates):
            return c
    if required:
        raise RuntimeError(f"missing required column; candidates={candidates}; columns={cols}")
    return None


def parse_int(value, field, errors, row_id):
    try:
        return int(str(value).strip())
    except Exception:
        errors.append(f"{row_id}: invalid integer {field}={value!r}")
        return None


def unique_id_map(rows, id_col, table_name, errors):
    out = {}
    for i, row in enumerate(rows, start=2):
        rid = str(row.get(id_col, "")).strip()
        if not rid:
            errors.append(f"{table_name}: blank ID at CSV line {i}")
            continue
        if rid in out:
            errors.append(f"{table_name}: duplicate ID {rid}")
            continue
        out[rid] = row
    return out


def candidate_text_fields(article_cols):
    wanted = []
    for name in ("Title", "Abstract"):
        for c in article_cols:
            if c.casefold() == name.casefold():
                wanted.append(c)
    return wanted


def slice_matches(text, start, end, annotated, inclusive):
    if start is None or end is None:
        return False
    if start < 0:
        return False
    stop = end + 1 if inclusive else end
    if stop <= start or stop > len(text):
        return False
    return text[start:stop] == annotated


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    args = ap.parse_args()

    base = args.root / "data/dataset"
    label_path = base / "label.csv"
    class_path = base / "label_class.csv"
    article_path = base / "article.csv"
    annotation_path = base / "annotation.csv"

    labels = read_semicolon(label_path)
    classes = read_semicolon(class_path)
    articles = read_semicolon(article_path)
    anns = read_semicolon(annotation_path)

    lcols = list(labels[0].keys())
    ccols = list(classes[0].keys())
    acols = list(articles[0].keys())
    ncols = list(anns[0].keys())

    label_id = find_col(lcols, ["ID"], required=True)
    label_name = find_col(lcols, ["Name"], required=True)
    label_class = find_col(lcols, ["ClassID"], required=True)
    class_id = find_col(ccols, ["ID"], required=True)
    class_name = find_col(ccols, ["Name"], required=True)

    article_id = find_col(acols, ["ID", "ArticleID"], required=True)
    pmid_col = find_col(acols, ["PMID", "PubMed"])
    domain_col = find_col(acols, ["Dataset", "Domain", "RecordDomain", "Set", "Type"])

    ann_id = find_col(ncols, ["ID"], required=True)
    ann_article = find_col(ncols, ["ArticleID", "article_id", "Article"], required=True)
    ann_label = find_col(ncols, ["LabelID", "label_id", "Label"], required=True)
    ann_text = find_col(ncols, ["Text"], required=True)
    start_col = find_col(ncols, ["Start", "StartIndex", "StartPos"], required=True)
    end_col = find_col(ncols, ["End", "EndIndex", "EndPos"], required=True)
    token_start_col = find_col(ncols, ["TokenStart"], required=False)
    token_end_col = find_col(ncols, ["TokenEnd"], required=False)

    errors = []

    label_by_id = unique_id_map(labels, label_id, "label", errors)
    class_by_id = unique_id_map(classes, class_id, "label_class", errors)
    article_by_id = unique_id_map(articles, article_id, "article", errors)
    ann_by_id = unique_id_map(anns, ann_id, "annotation", errors)

    label_ids_int = []
    for lid in label_by_id:
        v = parse_int(lid, "LabelID", errors, f"label:{lid}")
        if v is not None:
            label_ids_int.append(v)
    class_ids_int = []
    for cid in class_by_id:
        v = parse_int(cid, "ClassID", errors, f"class:{cid}")
        if v is not None:
            class_ids_int.append(v)

    if sorted(label_ids_int) != EXPECTED_LABEL_IDS:
        errors.append(f"released LabelID set mismatch: {sorted(label_ids_int)}")
    if sorted(class_ids_int) != EXPECTED_CLASS_IDS:
        errors.append(f"released ClassID set mismatch: {sorted(class_ids_int)}")

    ontology = []
    for lid in sorted(label_by_id, key=lambda x: int(x)):
        row = label_by_id[lid]
        cid = str(row.get(label_class, "")).strip()
        crow = class_by_id.get(cid)
        if crow is None:
            errors.append(f"label {lid}: unknown ClassID {cid!r}")
            cname = "UNKNOWN"
        else:
            cname = str(crow.get(class_name, "")).strip()
        ontology.append(
            {
                "label_id": int(lid),
                "label_class_id": int(cid) if cid.isdigit() else cid,
                "class_name": cname,
                "label_name": str(row.get(label_name, "")).strip(),
                "channel_index_zero_based": int(lid) - 1,
            }
        )

    pmids = set()
    if pmid_col:
        for r in articles:
            v = str(r.get(pmid_col, "") or "").strip()
            if v:
                pmids.add(v)

    domains = collections.Counter()
    if domain_col:
        domains.update(str(r.get(domain_col, "") or "").strip() for r in articles)

    text_fields = candidate_text_fields(acols)
    if not text_fields:
        errors.append("no released Title/Abstract text field found")

    coord_models = {}
    for field in text_fields:
        coord_models[f"{field}:half_open"] = 0
        coord_models[f"{field}:inclusive_end"] = 0

    ann_counts_by_id = collections.Counter()
    ann_counts_by_domain_and_id = collections.Counter()
    missing_article = 0
    missing_label = 0
    blank_annotation_text = 0
    invalid_numeric_coordinate = 0
    invalid_token_index = 0
    duplicate_coordinate_label_rows = 0
    exact_tuple_seen = set()

    per_annotation_cache = []

    for r in anns:
        aid = str(r.get(ann_id, "")).strip()
        art_id = str(r.get(ann_article, "")).strip()
        lid = str(r.get(ann_label, "")).strip()
        annotated = str(r.get(ann_text, "") or "")

        art = article_by_id.get(art_id)
        if art is None:
            missing_article += 1
        if lid not in label_by_id:
            missing_label += 1
        if not annotated:
            blank_annotation_text += 1

        s = parse_int(r.get(start_col), start_col, errors, f"annotation:{aid}")
        e = parse_int(r.get(end_col), end_col, errors, f"annotation:{aid}")
        if s is None or e is None or s < 0 or e <= s:
            invalid_numeric_coordinate += 1

        ts = te = None
        if token_start_col is not None and token_end_col is not None:
            ts = parse_int(r.get(token_start_col), token_start_col, errors, f"annotation:{aid}")
            te = parse_int(r.get(token_end_col), token_end_col, errors, f"annotation:{aid}")
            if ts is None or te is None or ts < 0 or te < ts:
                invalid_token_index += 1

        if lid in label_by_id:
            ann_counts_by_id[int(lid)] += 1

        if art is not None and lid in label_by_id and domain_col:
            dom = str(art.get(domain_col, "") or "").strip()
            ann_counts_by_domain_and_id[(dom, int(lid))] += 1

        if art is not None and s is not None and e is not None:
            for field in text_fields:
                source = str(art.get(field, "") or "")
                if slice_matches(source, s, e, annotated, inclusive=False):
                    coord_models[f"{field}:half_open"] += 1
                if slice_matches(source, s, e, annotated, inclusive=True):
                    coord_models[f"{field}:inclusive_end"] += 1

        key = (art_id, lid, s, e, annotated)
        if key in exact_tuple_seen:
            duplicate_coordinate_label_rows += 1
        exact_tuple_seen.add(key)
        per_annotation_cache.append((aid, art_id, lid, annotated, s, e, ts, te))

    total_annotations = len(anns)
    full_match_models = [k for k, v in coord_models.items() if v == total_annotations]
    if len(full_match_models) != 1:
        errors.append(
            "coordinate origin/serialization not uniquely certified; "
            f"full_match_models={full_match_models}; match_counts={coord_models}"
        )
        resolved_model = None
    else:
        resolved_model = full_match_models[0]

    exact_roundtrip_failures = 0
    coordinate_oob_rows = 0
    resolved_text_field = None
    resolved_inclusive = None

    if resolved_model:
        resolved_text_field, mode = resolved_model.split(":", 1)
        resolved_inclusive = mode == "inclusive_end"
        for aid, art_id, lid, annotated, s, e, ts, te in per_annotation_cache:
            art = article_by_id.get(art_id)
            if art is None or s is None or e is None:
                exact_roundtrip_failures += 1
                continue
            source = str(art.get(resolved_text_field, "") or "")
            stop = e + 1 if resolved_inclusive else e
            if s < 0 or stop <= s or stop > len(source):
                coordinate_oob_rows += 1
                exact_roundtrip_failures += 1
                continue
            if source[s:stop] != annotated:
                exact_roundtrip_failures += 1

    if missing_article:
        errors.append(f"annotation rows with missing article FK: {missing_article}")
    if missing_label:
        errors.append(f"annotation rows with missing label FK: {missing_label}")
    if blank_annotation_text:
        errors.append(f"blank annotation Text rows: {blank_annotation_text}")
    if invalid_numeric_coordinate:
        errors.append(f"invalid numeric character-coordinate rows: {invalid_numeric_coordinate}")
    if invalid_token_index:
        errors.append(f"invalid token-index rows: {invalid_token_index}")
    if coordinate_oob_rows:
        errors.append(f"out-of-bounds coordinate rows: {coordinate_oob_rows}")
    if exact_roundtrip_failures:
        errors.append(f"exact text/coordinate round-trip failures: {exact_roundtrip_failures}")

    if len(articles) != EXPECTED_ARTICLES:
        errors.append(f"article row count changed: {len(articles)} != {EXPECTED_ARTICLES}")
    if len(anns) != EXPECTED_ANNOTATIONS:
        errors.append(f"annotation row count changed: {len(anns)} != {EXPECTED_ANNOTATIONS}")
    if len(label_by_id) != 25:
        errors.append(f"label count changed: {len(label_by_id)} != 25")
    if len(class_by_id) != 7:
        errors.append(f"label class count changed: {len(class_by_id)} != 7")

    annotation_counts_by_label_id = []
    for item in ontology:
        lid = item["label_id"]
        annotation_counts_by_label_id.append(
            {
                **item,
                "annotation_count": int(ann_counts_by_id.get(lid, 0)),
            }
        )

    domain_label_counts = []
    for (dom, lid), count in sorted(ann_counts_by_domain_and_id.items(), key=lambda x: (x[0][0], x[0][1])):
        domain_label_counts.append(
            {
                "domain": dom,
                "label_id": lid,
                "annotation_count": int(count),
            }
        )

    state = "FEDERATION_SURUS_SCHEMA_COORDINATE_AUDIT_PASS" if not errors else "FEDERATION_SURUS_SCHEMA_COORDINATE_AUDIT_FAIL"

    out = {
        "state": state,
        "source_commit": PINNED_SURUS_COMMIT,
        "license": "CC-BY-NC-4.0",
        "license_sha256": sha(args.root / "LICENSE"),
        "article_file_sha256": sha(article_path),
        "annotation_file_sha256": sha(annotation_path),
        "label_file_sha256": sha(label_path),
        "label_class_file_sha256": sha(class_path),
        "article_rows": len(articles),
        "annotation_rows": len(anns),
        "publication_reported_annotation_total": PAPER_ANNOTATION_TOTAL,
        "release_vs_publication_annotation_delta": PAPER_ANNOTATION_TOTAL - len(anns),
        "release_vs_publication_equivalence_claimed": False,
        "label_count": len(label_by_id),
        "label_class_count": len(class_by_id),
        "article_columns": acols,
        "annotation_columns": ncols,
        "pmid_column_detected": pmid_col,
        "unique_pmids": len(pmids),
        "domain_column_detected": domain_col,
        "domain_counts": dict(sorted(domains.items())),
        "ontology_primary_key": ["source_commit", "released_LabelID"],
        "ontology_channel_order": "numeric LabelID ascending 1..25",
        "labels_by_id": annotation_counts_by_label_id,
        "annotation_counts_by_domain_and_label_id": domain_label_counts,
        "foreign_key_missing_article": missing_article,
        "foreign_key_missing_label": missing_label,
        "duplicate_exact_annotation_rows": duplicate_coordinate_label_rows,
        "blank_annotation_text_rows": blank_annotation_text,
        "invalid_numeric_coordinate_rows": invalid_numeric_coordinate,
        "invalid_token_index_rows": invalid_token_index,
        "coordinate_candidate_match_counts": coord_models,
        "coordinate_model_full_match_candidates": full_match_models,
        "coordinate_model_resolved": resolved_model,
        "coordinate_text_field_resolved": resolved_text_field,
        "coordinate_end_semantics": (
            "inclusive" if resolved_inclusive else "half_open"
        ) if resolved_model else None,
        "coordinate_out_of_bounds_rows": coordinate_oob_rows,
        "exact_text_coordinate_roundtrip_failures": exact_roundtrip_failures,
        "coordinate_roundtrip_certified": bool(resolved_model and exact_roundtrip_failures == 0),
        "token_index_numeric_invariants_certified": invalid_token_index == 0,
        "token_to_model_representability_certified": False,
        "raw_article_text_emitted": False,
        "pmid_values_emitted": False,
        "scientific_metric_computed": False,
        "native_pico_mapping_authorized": False,
        "surus_scientific_fit_performed": False,
        "errors": errors,
        "interpretation": (
            "Corrected release-identity/schema/coordinate audit only. "
            "Model-tokenizer representability remains a separate adapter preflight. "
            "No native P/I/C/O mapping or scientific fit is authorized."
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))

    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
