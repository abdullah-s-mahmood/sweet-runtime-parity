#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SALT = "ACAD_PASS|MPSEF|V3|SPLIT1"


class DSU:
    def __init__(self, items):
        self.p = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def nfc_ws(s: str) -> str:
    return " ".join(unicodedata.normalize("NFC", s).strip().split())


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def token_set(s: str):
    return frozenset(nfc_ws(s).split())


def length_bin(n: float) -> str:
    if n <= 20:
        return "LE20"
    if n <= 40:
        return "21_40"
    if n <= 80:
        return "41_80"
    return "GT80"


def median(vals):
    xs = sorted(vals)
    n = len(xs)
    if n % 2:
        return float(xs[n // 2])
    return (xs[n // 2 - 1] + xs[n // 2]) / 2.0


def near_duplicate_pairs(records):
    # Exact candidate generation for Jaccard >=0.90 using a prefix filter.
    # Tokens are globally ordered by frequency (rare first).
    token_freq = Counter()
    sets = {}
    lengths = {}
    for uid, rec in records.items():
        s = token_set(rec["source"])
        sets[uid] = s
        lengths[uid] = len(nfc_ws(rec["source"]).split())
        token_freq.update(s)

    ordered = {
        uid: sorted(s, key=lambda t: (token_freq[t], t))
        for uid, s in sets.items()
    }

    inv = defaultdict(list)
    candidates = set()

    for uid in sorted(records):
        toks = ordered[uid]
        n = len(toks)
        if n == 0:
            continue
        # Prefix length for all-pairs threshold filtering at t=.90.
        prefix_len = n - math.ceil(0.90 * n) + 1
        prefix = toks[:max(1, prefix_len)]
        for tok in prefix:
            for other in inv[tok]:
                a, b = sorted((uid, other))
                candidates.add((a, b))
            inv[tok].append(uid)

    out = []
    for a, b in sorted(candidates):
        la, lb = lengths[a], lengths[b]
        if min(la, lb) / max(la, lb) < 0.90:
            continue
        sa, sb = sets[a], sets[b]
        union = len(sa | sb)
        j = 1.0 if union == 0 else len(sa & sb) / union
        if j >= 0.90:
            out.append((a, b, j))
    return out


def cluster_id(uids):
    joined = "\n".join(sorted(set(uids)))
    return sha(joined)


def assignment_hash(cid):
    return sha(SALT + "\n" + cid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--out-prefix", default="MPSEF_ROLE_SPLIT_V1")
    args = ap.parse_args()

    cal = {
        r["uid"]: r
        for r in (
            json.loads(x)
            for x in Path(args.calibration).read_text(encoding="utf-8").splitlines()
            if x.strip()
        )
    }
    ledger = {
        r["uid"]: r
        for r in (
            json.loads(x)
            for x in Path(args.ledger).read_text(encoding="utf-8").splitlines()
            if x.strip()
        )
    }

    if set(cal) != set(ledger) or len(cal) != 6888:
        raise RuntimeError("CALIBRATION/ledger UID mismatch")

    dsu = DSU(cal.keys())

    # Same document.
    docs = defaultdict(list)
    for uid, x in ledger.items():
        docs[x["document_id"]].append(uid)
    same_doc_edges = 0
    for uids in docs.values():
        first = uids[0]
        for u in uids[1:]:
            dsu.union(first, u)
            same_doc_edges += 1

    # Exact duplicate source.
    exact = defaultdict(list)
    for uid, r in cal.items():
        exact[sha(nfc_ws(r["source"]))].append(uid)
    exact_edges = 0
    for uids in exact.values():
        if len(uids) > 1:
            first = uids[0]
            for u in uids[1:]:
                dsu.union(first, u)
                exact_edges += 1

    # Near duplicates according to the frozen review rule.
    near_pairs = near_duplicate_pairs(cal)
    for a, b, _ in near_pairs:
        dsu.union(a, b)

    components = defaultdict(list)
    for uid in cal:
        components[dsu.find(uid)].append(uid)

    clusters = []
    for members in components.values():
        members = sorted(members)
        cid = cluster_id(members)
        lengths = [len(nfc_ws(cal[u]["source"]).split()) for u in members]
        origins = sorted({ledger[u]["origin_split"] for u in members})
        corpus = "QALB14"
        level = "L1"
        med = median(lengths)
        lb = length_bin(med)
        stratum = f"{corpus}|{level}|{lb}"
        clusters.append({
            "cluster_id": cid,
            "uids": members,
            "record_count": len(members),
            "document_ids": sorted({ledger[u]["document_id"] for u in members}),
            "origin_splits": origins,
            "median_source_words": med,
            "length_bin": lb,
            "corpus": corpus,
            "level": level,
            "stratum": stratum,
            "assignment_hash": assignment_hash(cid),
        })

    by_stratum = defaultdict(list)
    for c in clusters:
        by_stratum[c["stratum"]].append(c)

    role_by_cluster = {}
    for stratum, cs in sorted(by_stratum.items()):
        cs = sorted(cs, key=lambda x: (x["assignment_hash"], x["cluster_id"]))
        m = len(cs)
        if m >= 10:
            n_f = math.floor(0.30 * m)
            n_t = math.floor(0.40 * m)
            for i, c in enumerate(cs):
                if i < n_f:
                    role = "C_F"
                elif i < n_f + n_t:
                    role = "C_T"
                else:
                    role = "C_R"
                role_by_cluster[c["cluster_id"]] = role
        else:
            for c in cs:
                bucket = int(c["assignment_hash"], 16) % 10
                role = "C_F" if bucket <= 2 else ("C_T" if bucket <= 6 else "C_R")
                role_by_cluster[c["cluster_id"]] = role

    rows = []
    seen = set()
    for c in sorted(clusters, key=lambda x: x["cluster_id"]):
        role = role_by_cluster[c["cluster_id"]]
        for uid in c["uids"]:
            if uid in seen:
                raise RuntimeError("duplicate role assignment")
            seen.add(uid)
            e = ledger[uid]
            r = cal[uid]
            rows.append({
                "case_id": r["case_id"],
                "uid": uid,
                "cluster_id": c["cluster_id"],
                "role": role,
                "stratum": c["stratum"],
                "document_id": e["document_id"],
                "author_id": e["author_id"],
                "origin_split": e["origin_split"],
                "source_word_count": e["source_word_count"],
                "cluster_record_count": c["record_count"],
                "cluster_median_source_words": c["median_source_words"],
                "historically_independent": False,
                "future_role_only": True,
            })

    if seen != set(cal):
        raise RuntimeError("not every CALIBRATION record assigned")

    # Cluster disjointness.
    roles_by_cluster = defaultdict(set)
    for x in rows:
        roles_by_cluster[x["cluster_id"]].add(x["role"])
    bad = {k: v for k, v in roles_by_cluster.items() if len(v) != 1}
    if bad:
        raise RuntimeError(f"cluster role leakage: {list(bad.items())[:5]}")

    out = Path(args.out_prefix + ".jsonl")
    out.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n",
        encoding="utf-8",
    )

    role_records = Counter(x["role"] for x in rows)
    role_clusters = Counter(role_by_cluster.values())
    stratum_summary = {}
    for s, cs in sorted(by_stratum.items()):
        stratum_summary[s] = {
            "clusters": len(cs),
            "records": sum(c["record_count"] for c in cs),
            "role_clusters": dict(Counter(role_by_cluster[c["cluster_id"]] for c in cs)),
            "role_records": dict(Counter(
                role_by_cluster[c["cluster_id"]]
                for c in cs
                for _ in c["uids"]
            )),
        }

    uid_role_digest = sha(
        "\n".join(f'{x["uid"]}\t{x["role"]}\t{x["cluster_id"]}' for x in sorted(rows, key=lambda z:z["uid"])) + "\n"
    )

    summary = {
        "record_id": "MPSEF_ROLE_SPLIT_V1",
        "status": "PASS",
        "cases": len(rows),
        "clusters": len(clusters),
        "document_ids": len(docs),
        "same_document_union_edges": same_doc_edges,
        "exact_duplicate_union_edges": exact_edges,
        "near_duplicate_pairs_jaccard_ge_0_90": len(near_pairs),
        "roles_records": dict(role_records),
        "roles_clusters": dict(role_clusters),
        "role_record_fractions": {
            k: role_records[k] / len(rows) for k in ("C_F","C_T","C_R")
        },
        "role_cluster_fractions": {
            k: role_clusters[k] / len(clusters) for k in ("C_F","C_T","C_R")
        },
        "strata": stratum_summary,
        "salt": SALT,
        "historical_independence_restored": False,
        "interpretation": "FUTURE_ROLE_SEPARATION_ONLY",
        "uid_role_cluster_sha256": uid_role_digest,
        "integrity": {
            "every_calibration_record_assigned_once": len(rows) == 6888,
            "cluster_role_overlap": 0,
            "internal_evaluation_opened": False,
            "stress_diagnostic_opened": False,
            "confirmation_opened": False,
            "holdout_opened": False,
            "a7ta_reserved_opened": False,
            "qalb15_test_opened": False,
            "feasibility_metric_computed": False,
        },
    }

    Path(args.out_prefix + "_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
