#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

EXPECTED_CASES = 1918
EXPECTED_CLUSTERS = 764
EXPECTED_SOURCE_SHA = "051516cdce384c5fe50afb2ce80fe12d8cd8fb65b06ba31c3209301f91a7e193"
EXPECTED_P1_SHA = "2ff2ff6ed837e902eeea93856ce4753966e9ecec6b497b681ecc185b260e300d"
EXPECTED_P2_SHA = "f91ab2be10909851d16bc8139fcf6987259de627447c948c45c31c33449cf99b"

POLICY_VERSION = "MPSEF_EXECUTABLE_ACTION_LEGALIZER_V1"
PROTECTION_VERSION = "MPSEF_DERIVED_PROTECTION_V2"

DIGITS = "0-9٠-٩۰-۹"
NUMBER_CORE = rf"[+\-−]?[{DIGITS}]+(?:[.,٫٬][{DIGITS}]+)*(?:[eE][+\-]?[{DIGITS}]+)?"
LATIN_UNITS = r"(?:kg|g|mg|ug|µg|km|cm|mm|um|µm|nm|m|L|mL|ml|uL|µL|Hz|kHz|MHz|GHz|V|mV|kV|A|mA|W|kW|MW|J|kJ|Pa|kPa|MPa|bar|mol|mmol|s|ms|min|h|K|°C|°F)"
AR_UNITS = r"(?:كغ|كغم|غم|غ|ملغ|مغ|ميكروغرام|كم|سم|مم|متر|م|لتر|مل|ثانية|ث|دقيقة|د|ساعة|س|هرتز|كيلوهرتز|ميغاهرتز|غيغاهرتز|فولت|أمبير|واط|جول|باسكال|مول)"
UNITS = rf"(?:{LATIN_UNITS}|{AR_UNITS})"
PERCENT = r"(?:%|٪)"

PROTECTED_PATTERNS = [
    ("URL_EMAIL", re.compile(r"https?://[^\s]+|www\.[^\s]+|[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")),
    ("CITATION_DOI", re.compile(r"\b10\.\d{4,9}/[^\s]+|\[(?:\s*[0-9٠-٩۰-۹]+\s*(?:[-–,،]\s*[0-9٠-٩۰-۹]+\s*)*)\]")),
    ("EQUATION_FORMULA", re.compile(r"\$[^$\n]+\$|\\\([^\n]+?\\\)|\\\[[^\n]+?\\\]")),
    ("DOCUMENT_STRUCTURE", re.compile(r"<(?:FIGURE|TABLE|EQUATION|COMMENT|BOOKMARK|FIELD)[^>]*>|\[\[(?:FIGURE|TABLE|EQUATION|COMMENT|BOOKMARK|FIELD)[^\]]*\]\]", re.I)),
    ("NUMBER_UNIT_COUPLED", re.compile(rf"{NUMBER_CORE}\s*{UNITS}\b", re.I)),
    ("PERCENT_COUPLED", re.compile(rf"{NUMBER_CORE}\s*{PERCENT}")),
    ("CODE_LATIN_TECHNICAL", re.compile(r"(?<![A-Za-z0-9_])[A-Za-z][A-Za-z0-9_.:+/#@\-]*(?![A-Za-z0-9_])")),
    ("NUMBER", re.compile(NUMBER_CORE + rf"(?:\s*{PERCENT})?")),
]

FINAL_STATE_ORDER = [
    "SOURCE_MISMATCH",
    "EMPTY_OUTPUT",
    "EXECUTION_FAILED",
    "TRUNCATED",
    "ALIGNMENT_FAILED",
    "NONREVERSIBLE",
    "PROTECTED_BLOCKED",
    "ALIGNMENT_AMBIGUOUS",
    "OK",
]

def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

def derived_spans(text: str):
    found = {}
    for category, pattern in PROTECTED_PATTERNS:
        for m in pattern.finditer(text):
            if m.start() == m.end():
                continue
            found[(m.start(), m.end(), category, m.group(0))] = True
    out = []
    for i, (s, e, cat, value) in enumerate(sorted(found), start=1):
        out.append({
            "protected_id": f"D{i:04d}",
            "category": cat,
            "source_start": s,
            "source_end": e,
            "text": value,
            "sha256": sha_text(value),
            "detector": PROTECTION_VERSION,
            "hard_protected": True,
        })
    return out

def protected_signature(spans):
    return [(x["category"], x["text"]) for x in spans]

def boundary_guard(text: str, s: int, e: int):
    left = text[:s]
    right = text[e:]
    left_gap = left[len(left.rstrip()):] if left else ""
    right_gap = right[:len(right)-len(right.lstrip())] if right else ""
    return {
        "left_gap": left_gap,
        "right_gap": right_gap,
        "left_token_count": len(left.split()),
        "right_token_count": len(right.split()),
    }

def _levenshtein_forward(a: str, b: str):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        ca = a[i - 1]
        row = d[i]
        prev = d[i - 1]
        for j in range(1, m + 1):
            row[j] = min(
                prev[j] + 1,
                row[j - 1] + 1,
                prev[j - 1] + (0 if ca == b[j - 1] else 1),
            )
    return d

def _levenshtein_backward(a: str, b: str):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        d[i][m] = n - i
    for j in range(m, -1, -1):
        d[n][j] = m - j
    for i in range(n - 1, -1, -1):
        ca = a[i]
        row = d[i]
        nxt = d[i + 1]
        for j in range(m - 1, -1, -1):
            row[j] = min(
                nxt[j] + 1,
                row[j + 1] + 1,
                nxt[j + 1] + (0 if ca == b[j] else 1),
            )
    return d

def optimal_alignment_protection_audit(source: str, output: str, spans):
    if not spans:
        return {
            "status":"PASS",
            "optimal_distance":None,
            "ambiguity_affects_legality":False,
            "reasons":[],
            "mapped_spans":[],
        }

    fwd = _levenshtein_forward(source, output)
    bwd = _levenshtein_backward(source, output)
    n, m = len(source), len(output)
    optimum = fwd[n][m]

    protected_chars = set()
    insertion_cursors = set()
    for span in spans:
        s, e = span["source_start"], span["source_end"]
        protected_chars.update(range(s, e))
        insertion_cursors.update(range(s, e + 1))

    possible_match_positions = {i:set() for i in protected_chars}
    bad_reasons = set()
    ambiguity_reasons = set()

    def edge_optimal(i, j, ni, nj, cost):
        return fwd[i][j] + cost + bwd[ni][nj] == optimum

    for i in range(n + 1):
        for j in range(m + 1):
            if i < n:
                if edge_optimal(i, j, i + 1, j, 1) and i in protected_chars:
                    bad_reasons.add(f"OPTIMAL_PATH_CAN_DELETE_PROTECTED_CHAR:{i}")
            if j < m:
                if edge_optimal(i, j, i, j + 1, 1) and i in insertion_cursors:
                    bad_reasons.add(f"OPTIMAL_PATH_CAN_INSERT_AT_PROTECTED_BOUNDARY:{i}")
            if i < n and j < m:
                cost = 0 if source[i] == output[j] else 1
                if edge_optimal(i, j, i + 1, j + 1, cost) and i in protected_chars:
                    if cost != 0:
                        bad_reasons.add(f"OPTIMAL_PATH_CAN_SUBSTITUTE_PROTECTED_CHAR:{i}")
                    else:
                        possible_match_positions[i].add(j)

    for i in sorted(protected_chars):
        poss = possible_match_positions[i]
        if len(poss) == 0:
            bad_reasons.add(f"NO_OPTIMAL_EXACT_MATCH_FOR_PROTECTED_CHAR:{i}")
        elif len(poss) > 1:
            ambiguity_reasons.add(
                f"PROTECTED_CHAR_HAS_MULTIPLE_OPTIMAL_OUTPUT_POSITIONS:{i}:{','.join(map(str,sorted(poss)))}"
            )

    mapped_spans = []
    for idx, span in enumerate(spans):
        s, e = span["source_start"], span["source_end"]
        mapped = []
        mapping_ok = True
        for i in range(s, e):
            poss = possible_match_positions.get(i, set())
            if len(poss) != 1:
                mapping_ok = False
                break
            mapped.append(next(iter(poss)))
        if mapping_ok and mapped:
            expected = list(range(mapped[0], mapped[0] + len(mapped)))
            if mapped != expected:
                ambiguity_reasons.add(f"PROTECTED_SPAN_NONCONTIGUOUS_MAPPING:{idx}")
                mapping_ok = False
        mapped_spans.append({
            "source_span_index":idx,
            "output_start":mapped[0] if mapping_ok and mapped else None,
            "output_end":mapped[-1] + 1 if mapping_ok and mapped else None,
            "mapping_unique_contiguous":bool(mapping_ok and mapped),
        })

    reasons = sorted(bad_reasons | ambiguity_reasons)
    return {
        "status":"PASS" if not reasons else "FAIL",
        "optimal_distance":optimum,
        "ambiguity_affects_legality":bool(ambiguity_reasons),
        "reasons":reasons,
        "mapped_spans":mapped_spans,
    }

def protection_proof(source: str, output: str):
    src = derived_spans(source)
    out = derived_spans(output)
    reasons = []

    # Detect deleted, changed, or newly created protected objects.
    if protected_signature(src) != protected_signature(out):
        reasons.append("PROTECTED_SIGNATURE_CHANGED")

    alignment = optimal_alignment_protection_audit(source, output, src)
    reasons.extend(alignment["reasons"])

    attachment_categories = {
        "CITATION_DOI","CODE_LATIN_TECHNICAL","NUMBER_UNIT_COUPLED",
        "PERCENT_COUPLED","URL_EMAIL","DOCUMENT_STRUCTURE","EQUATION_FORMULA"
    }

    # If optimal mapping is unique/contiguous, verify exact text and structural
    # attachment without freezing the lexical spelling of neighboring words.
    for idx, span in enumerate(src):
        mapped = alignment["mapped_spans"][idx] if idx < len(alignment["mapped_spans"]) else None
        if not mapped or not mapped["mapping_unique_contiguous"]:
            continue
        j, k = mapped["output_start"], mapped["output_end"]
        if output[j:k] != span["text"]:
            reasons.append(f"PROTECTED_TEXT_CHANGED:{idx}")
            continue

        sg = boundary_guard(source, span["source_start"], span["source_end"])
        og = boundary_guard(output, j, k)
        if sg["left_gap"] != og["left_gap"] or sg["right_gap"] != og["right_gap"]:
            reasons.append(f"PROTECTED_SEPARATOR_CHANGED:{idx}")

        if span["category"] in attachment_categories:
            if (
                sg["left_token_count"] != og["left_token_count"]
                or sg["right_token_count"] != og["right_token_count"]
            ):
                reasons.append(f"PROTECTED_ATTACHMENT_ORDINAL_CHANGED:{idx}")

    reasons = sorted(set(reasons))
    return {
        "status":"PASS" if not reasons else "FAIL",
        "derived_protection_version":PROTECTION_VERSION,
        "source_spans":src,
        "output_spans":out,
        "optimal_alignment_audit":alignment,
        "reasons":reasons,
    }

def alignment_ambiguity_status(source: str, output: str, protection):
    audit = protection.get("optimal_alignment_audit", {})
    if audit.get("ambiguity_affects_legality"):
        return {
            "status":"AFFECTS_LEGALITY",
            "reason":";".join(
                x for x in audit.get("reasons", [])
                if "MULTIPLE_OPTIMAL" in x or "NONCONTIGUOUS" in x
            ) or "PROTECTION_RELEVANT_OPTIMAL_ALIGNMENT_AMBIGUITY",
            "edit_distance":audit.get("optimal_distance"),
        }
    if protection.get("source_spans") and audit.get("status") == "FAIL":
        return {
            "status":"NO_AMBIGUITY_BUT_PROTECTION_UNSAFE",
            "reason":None,
            "edit_distance":audit.get("optimal_distance"),
        }
    return {
        "status":"NO_PROTECTION_RELEVANT_AMBIGUITY_PROVEN",
        "reason":None,
        "edit_distance":audit.get("optimal_distance"),
    }

def reversibility_proof(source: str, output: str, expected_source_sha: str, expected_output_sha: str):
    if sha_text(source) != expected_source_sha:
        return {"status":"FAIL","reason":"SOURCE_SHA_MISMATCH"}
    if sha_text(output) != expected_output_sha:
        return {"status":"FAIL","reason":"OUTPUT_SHA_MISMATCH"}

    action = {
        "expected_source_sha256": expected_source_sha,
        "expected_output_sha256": expected_output_sha,
        "replacement": output,
        "inverse_replacement": source,
    }

    def apply(current: str):
        if sha_text(current) != action["expected_source_sha256"]:
            raise ValueError("unexpected source")
        return action["replacement"]

    def inverse(current: str):
        if sha_text(current) != action["expected_output_sha256"]:
            raise ValueError("unexpected output")
        return action["inverse_replacement"]

    try:
        got = apply(source)
        back = inverse(got)
    except Exception as e:
        return {"status":"FAIL","reason":f"EXECUTION:{type(e).__name__}"}

    if got != output or back != source:
        return {"status":"FAIL","reason":"ROUNDTRIP_MISMATCH"}
    return {"status":"PASS","reason":None}

def p1_truncation_status(prop):
    # P1 is token-classification + rewrite, not seq2seq generation.
    # Frozen runner does not request tokenizer truncation. A too-long input would
    # fail execution rather than silently generate a ceiling-truncated sentence.
    for name in ("pass1_trace","pass2_trace"):
        trace = prop.get(name)
        if not isinstance(trace, dict):
            return {"status":"UNKNOWN","reason":f"MISSING_{name.upper()}"}
        if len(trace.get("subwords", [])) != len(trace.get("labels", [])):
            return {"status":"FAIL","reason":f"TOKEN_LABEL_MISMATCH_{name.upper()}"}
    return {"status":"PASS","reason":"GENERATION_FREE_NO_SILENT_TRUNCATION_ARGUMENT"}

def p2_ged_word_alignment_status(prop):
    morph = prop.get("morph_preprocessed_text")
    labels = prop.get("ged_labels")
    if not isinstance(morph, str) or not isinstance(labels, list):
        return {
            "status":"FAIL",
            "reason":"MISSING_P2_GED_PROVENANCE_FIELDS",
            "morph_word_count":None,
            "ged_label_count":None,
        }
    mw = len(morph.split())
    gl = len(labels)
    if mw != gl:
        return {
            "status":"FAIL",
            "reason":"GED_WORD_ALIGNMENT_MISMATCH",
            "morph_word_count":mw,
            "ged_label_count":gl,
            "excess_labels":gl-mw,
        }
    return {
        "status":"PASS",
        "reason":"GED_WORD_COUNT_MATCH",
        "morph_word_count":mw,
        "ged_label_count":gl,
        "excess_labels":0,
    }

def p2_truncation_status(prop, trace):
    # P2 requires independent generation metadata because decoded text alone
    # cannot prove natural termination before max_length=100.
    if trace is None:
        return {"status":"UNKNOWN","reason":"MISSING_INDEPENDENT_GENERATION_TRACE"}
    required = [
        "uid","source_sha256","output_sha256","decoder_start_token_id",
        "eos_token_id","generated_token_ids","max_length",
        "ged_word_count","morph_word_count","ged_label_count",
    ]
    missing = [k for k in required if k not in trace]
    if missing:
        return {"status":"UNKNOWN","reason":"MISSING_TRACE_FIELDS:"+",".join(missing)}
    if trace["uid"] != prop["uid"] or trace["source_sha256"] != prop["source_version_hash"] or trace["output_sha256"] != prop["output_sha256"]:
        return {"status":"FAIL","reason":"TRACE_IDENTITY_MISMATCH"}
    ids = trace["generated_token_ids"]
    if not isinstance(ids, list) or not ids:
        return {"status":"UNKNOWN","reason":"EMPTY_GENERATION_TOKEN_TRACE"}
    if trace["ged_word_count"] != trace["morph_word_count"] or trace["ged_label_count"] != trace["morph_word_count"]:
        return {"status":"FAIL","reason":"GED_COVERAGE_MISMATCH"}

    start = 1 if ids and ids[0] == trace["decoder_start_token_id"] else 0
    eos = trace["eos_token_id"]
    eos_positions = [i for i in range(start, len(ids)) if ids[i] == eos]
    if not eos_positions:
        return {"status":"UNKNOWN","reason":"NO_TERMINATING_EOS_AFTER_DECODER_PREFIX"}
    end = eos_positions[0] + 1
    max_len = int(trace["max_length"])
    if end >= max_len:
        return {"status":"FAIL","reason":"GENERATION_REACHED_MAX_LENGTH"}
    if trace.get("input_truncated") is True:
        return {"status":"FAIL","reason":"INPUT_TRUNCATED"}
    if trace.get("input_truncated") is None:
        return {"status":"UNKNOWN","reason":"INPUT_TRUNCATION_NOT_PROVEN"}
    return {"status":"PASS","reason":"NATURAL_EOS_BEFORE_CEILING_AND_INPUT_COVERAGE_PROVEN"}

def choose_final_state(reasons):
    cats = {r.split(":",1)[0] for r in reasons}
    for state in FINAL_STATE_ORDER:
        if state == "OK":
            return "OK"
        if state in cats:
            return state
    return "OK"

def legalize_one(man, prop, proposer, p2_trace=None):
    reasons = []
    source = man["source"]
    output = prop.get("full_proposer_output","")

    if prop.get("uid") != man["uid"] or prop.get("cluster_id") != man["cluster_id"]:
        reasons.append("SOURCE_MISMATCH:IDENTITY")
    if prop.get("source") != source:
        reasons.append("SOURCE_MISMATCH:SOURCE_TEXT")
    if prop.get("source_version_hash") != man["source_sha256"]:
        reasons.append("SOURCE_MISMATCH:SOURCE_VERSION")
    if sha_text(source) != man["source_sha256"]:
        reasons.append("SOURCE_MISMATCH:MANIFEST_SOURCE_SHA")
    if prop.get("output_sha256") != sha_text(output):
        reasons.append("SOURCE_MISMATCH:OUTPUT_SHA")

    if output.strip() == "":
        reasons.append("EMPTY_OUTPUT:BLANK_OR_EMPTY")

    protection = protection_proof(source, output)
    if protection["status"] != "PASS":
        reasons.append("PROTECTED_BLOCKED:"+",".join(protection["reasons"]))

    ambiguity = alignment_ambiguity_status(source, output, protection)
    if ambiguity["status"] == "AFFECTS_LEGALITY":
        reasons.append("ALIGNMENT_AMBIGUOUS:"+str(ambiguity["reason"]))

    reversible = reversibility_proof(
        source, output, man["source_sha256"], prop.get("output_sha256","")
    )
    if reversible["status"] != "PASS":
        reasons.append("NONREVERSIBLE:"+str(reversible["reason"]))

    ged_alignment = None
    if proposer == "P2":
        ged_alignment = p2_ged_word_alignment_status(prop)
        if ged_alignment["status"] != "PASS":
            reasons.append("EXECUTION_FAILED:"+str(ged_alignment["reason"]))

    trunc = p1_truncation_status(prop) if proposer == "P1" else p2_truncation_status(prop, p2_trace)
    if trunc["status"] in {"FAIL","UNKNOWN"}:
        reasons.append("TRUNCATED:"+str(trunc["reason"]))

    final_state = choose_final_state(reasons)
    executable = final_state == "OK"

    action = {
        "uid": man["uid"],
        "case_id": man["case_id"],
        "cluster_id": man["cluster_id"],
        "proposer": proposer,
        "proposal_type": prop.get("proposal_type"),
        "source_sha256": man["source_sha256"],
        "output_sha256": prop.get("output_sha256"),
        "source": source,
        "output": output,
        "final_state": final_state,
        "reasons": reasons,
        "executable": executable,
        "alignment_status": ambiguity,
        "protection_status": protection,
        "truncation_status": trunc,
        "ged_word_alignment_status": ged_alignment,
        "reversibility_status": reversible,
        "legalizer_version": POLICY_VERSION,
        "gold_reference_consulted": False,
    }
    action["action_record_sha256"] = sha_text(json.dumps(action, ensure_ascii=False, sort_keys=True))
    return action

def self_test():
    # Edge insertion / attachment tests required by the independent review.
    bad_pairs = [
        ("5 mg", "15 mg"),
        ("5 mg", "5 mg2"),
        ("النص", "النص [1]"),
        ("النص [1]", "النص[1]"),
        ("5 كغ", "6 كغ"),
        ("5٪", "6٪"),
    ]
    for src, out in bad_pairs:
        p = protection_proof(src, out)
        assert p["status"] == "FAIL", (src, out, p)

    # Round-trip proof.
    s, o = "النص 5 mg", "النص الصحيح 5 mg"
    r = reversibility_proof(s, o, sha_text(s), sha_text(o))
    assert r["status"] == "PASS"

    # P2 frozen inference requires one GED label per morphology word.
    bad_prop = {
        "morph_preprocessed_text":"كلمة أخرى",
        "ged_labels":["UC","UC","UC"],
    }
    good_prop = {
        "morph_preprocessed_text":"كلمة أخرى",
        "ged_labels":["UC","UC"],
    }
    assert p2_ged_word_alignment_status(bad_prop)["status"] == "FAIL"
    assert p2_ged_word_alignment_status(good_prop)["status"] == "PASS"

    # P2 decoder prefix == EOS must ignore the prefix.
    prop = {
        "uid":"U","source_version_hash":sha_text("x"),"output_sha256":sha_text("y")
    }
    trace = {
        "uid":"U","source_sha256":sha_text("x"),"output_sha256":sha_text("y"),
        "decoder_start_token_id":2,"eos_token_id":2,
        "generated_token_ids":[2,11,12,2,1],
        "max_length":100,"ged_word_count":1,"morph_word_count":1,
        "ged_label_count":1,"input_truncated":False,
    }
    assert p2_truncation_status(prop, trace)["status"] == "PASS"

    ceiling = dict(trace)
    ceiling["generated_token_ids"] = [2] + [11]*98 + [2]
    assert p2_truncation_status(prop, ceiling)["status"] == "FAIL"

    print(json.dumps({"self_test":"PASS","policy_version":POLICY_VERSION}, ensure_ascii=False))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--source-manifest")
    ap.add_argument("--p1-proposals")
    ap.add_argument("--p2-proposals")
    ap.add_argument("--p2-generation-trace")
    ap.add_argument("--out-prefix", default="MPSEF_EXECUTABLE_ACTIONS_V1")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return

    required = [args.source_manifest,args.p1_proposals,args.p2_proposals]
    if any(x is None for x in required):
        raise SystemExit("missing source-only legalizer input")

    manp,p1p,p2p = map(Path, required)
    if sha256_file(manp) != EXPECTED_SOURCE_SHA:
        raise RuntimeError("source manifest SHA mismatch")
    if sha256_file(p1p) != EXPECTED_P1_SHA:
        raise RuntimeError("P1 proposal SHA mismatch")
    if sha256_file(p2p) != EXPECTED_P2_SHA:
        raise RuntimeError("P2 proposal SHA mismatch")

    manifest = read_jsonl(manp)
    p1_rows = read_jsonl(p1p)
    p2_rows = read_jsonl(p2p)
    if len(manifest) != EXPECTED_CASES or len({x["uid"] for x in manifest}) != EXPECTED_CASES:
        raise RuntimeError("manifest population mismatch")
    if len({x["cluster_id"] for x in manifest}) != EXPECTED_CLUSTERS:
        raise RuntimeError("manifest cluster mismatch")
    if len(p1_rows) != EXPECTED_CASES or len(p2_rows) != EXPECTED_CASES:
        raise RuntimeError("proposal population mismatch")

    man = {x["uid"]:x for x in manifest}
    p1 = {x["uid"]:x for x in p1_rows}
    p2 = {x["uid"]:x for x in p2_rows}
    if set(man) != set(p1) or set(man) != set(p2):
        raise RuntimeError("UID-set mismatch")

    traces = {}
    if args.p2_generation_trace:
        trace_rows = read_jsonl(Path(args.p2_generation_trace))
        traces = {x["uid"]:x for x in trace_rows}
        if set(traces) != set(man):
            raise RuntimeError("P2 generation trace UID-set mismatch")

    records = []
    action_sets = []
    counts = Counter()

    for uid in sorted(man):
        a1 = legalize_one(man[uid], p1[uid], "P1", None)
        a2 = legalize_one(man[uid], p2[uid], "P2", traces.get(uid))
        records.extend([a1,a2])
        counts[f"P1_{a1['final_state']}"] += 1
        counts[f"P2_{a2['final_state']}"] += 1

        actions = [{
            "action_id": sha_text("KEEP\n"+uid+"\n"+man[uid]["source_sha256"]),
            "type":"KEEP",
            "output":man[uid]["source"],
            "output_sha256":man[uid]["source_sha256"],
            "provenance":["KEEP"],
        }]
        by_output = {man[uid]["source"]: actions[0]}
        for rec in (a1,a2):
            if not rec["executable"]:
                continue
            if rec["output"] in by_output:
                by_output[rec["output"]]["provenance"].append(rec["proposer"])
            else:
                item = {
                    "action_id":sha_text(rec["proposer"]+"\n"+uid+"\n"+rec["output_sha256"]),
                    "type":rec["proposal_type"],
                    "output":rec["output"],
                    "output_sha256":rec["output_sha256"],
                    "provenance":[rec["proposer"]],
                }
                actions.append(item)
                by_output[rec["output"]] = item

        action_sets.append({
            "uid":uid,
            "case_id":man[uid]["case_id"],
            "cluster_id":man[uid]["cluster_id"],
            "source_sha256":man[uid]["source_sha256"],
            "actions":actions,
            "unique_action_count":len(actions),
        })

    if len(records) != EXPECTED_CASES*2:
        raise RuntimeError("hypothesis record count mismatch")
    if any(x["unique_action_count"] < 1 or x["unique_action_count"] > 3 for x in action_sets):
        raise RuntimeError("primary action-set size violation")

    prefix = Path(args.out_prefix)
    rec_path = Path(str(prefix)+"_HYPOTHESES.jsonl")
    act_path = Path(str(prefix)+"_ACTION_SETS.jsonl")
    rec_path.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in records)+"\n",encoding="utf-8")
    act_path.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in action_sets)+"\n",encoding="utf-8")

    summary = {
        "record_id":"MPSEF_EXECUTABLE_ACTIONS_V1",
        "status":"LEGALIZER_COMPLETE",
        "legalizer_version":POLICY_VERSION,
        "cases":EXPECTED_CASES,
        "clusters":EXPECTED_CLUSTERS,
        "hypotheses":len(records),
        "expected_hypotheses":EXPECTED_CASES*2,
        "state_counts":dict(counts),
        "action_sets":len(action_sets),
        "action_count_min":min(x["unique_action_count"] for x in action_sets),
        "action_count_max":max(x["unique_action_count"] for x in action_sets),
        "source_manifest_sha256":sha256_file(manp),
        "P1_proposal_sha256":sha256_file(p1p),
        "P2_proposal_sha256":sha256_file(p2p),
        "P2_generation_trace_supplied":bool(args.p2_generation_trace),
        "gold_reference_consulted":False,
        "reference_content_used":False,
        "R_joint_computed":False,
        "selector_trained":False,
        "internal_evaluation_opened":False,
        "stress_diagnostic_opened":False,
        "reserved_data_opened":False,
    }
    summary["hypotheses_sha256"] = sha256_file(rec_path)
    summary["action_sets_sha256"] = sha256_file(act_path)
    Path(str(prefix)+"_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)

if __name__ == "__main__":
    main()
