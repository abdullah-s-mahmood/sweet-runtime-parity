from __future__ import annotations
import hashlib,json,pathlib,re,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent

CAL_SHA="40f6c7aa6293b374d4d12d837ed96342d0a8e72d08cc014a115b0be3a54e5a65"

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def claim_units(text):
    parts=[]
    for sentence in re.split(r"(?<=[.!?;])\s+",text.strip()):
        if not sentence.strip(): continue
        chunks=re.split(r"\s+(?:but|whereas|however|nevertheless)\s+",sentence,flags=re.I)
        if len(chunks)==1 and re.match(r"(?i)^although\b",sentence):
            chunks=re.split(r",\s+",sentence,maxsplit=1)
        for c in chunks:
            c=c.strip(" ,;")
            if len(c.split())>=3: parts.append(c)
    return parts

# Rebuild frozen calibration deterministically and verify exact population identity.
subprocess.run([sys.executable,str(ROOT/"build_calibration_v1.py")],check=True)
cal_path=ROOT/"calibration/V2_4_SEMANTIC_CALIBRATION_V1.jsonl"
if sha256_bytes(cal_path.read_bytes())!=CAL_SHA:
    raise SystemExit("CALIBRATION_POPULATION_SHA_MISMATCH")
cal=[json.loads(x) for x in cal_path.read_text().splitlines() if x.strip()]
assert len(cal)==58

cases={}
for line in (ROOT.parent/"cases.jsonl").read_text().splitlines():
    if line.strip():
        c=json.loads(line); cases[c["case_id"]]=c
graph=json.loads((ROOT/"SOURCE_ASSERTIONS_V1.json").read_text())
assert set(graph["cases"])==set(cases)

pairs=[]
paragraphs=[]
for row in cal:
    cid=row["case_id"]; source=cases[cid]["source_text"]; candidate=row["candidate_text"]
    units=claim_units(candidate)
    paragraphs.append({
        "calibration_id":row["calibration_id"],
        "case_id":cid,
        "gold_label":row["label"],
        "source_sha256":row["source_sha256"],
        "candidate_sha256":row["candidate_sha256"],
        "candidate_claim_units":len(units)
    })
    for a in graph["cases"][cid]:
        pairs.append({
            "pair_id":f'{row["calibration_id"]}:S2C:{a["assertion_id"]}',
            "calibration_id":row["calibration_id"],
            "case_id":cid,
            "gold_paragraph_label":row["label"],
            "direction":"SOURCE_TO_CANDIDATE",
            "assertion_id":a["assertion_id"],
            "relation_family":a["relation_family"],
            "premise":candidate,
            "hypothesis":a["hypothesis"]
        })
    for i,u in enumerate(units,1):
        pairs.append({
            "pair_id":f'{row["calibration_id"]}:C2S:C{i:02d}',
            "calibration_id":row["calibration_id"],
            "case_id":cid,
            "gold_paragraph_label":row["label"],
            "direction":"CANDIDATE_TO_SOURCE",
            "candidate_unit_id":f"C{i:02d}",
            "premise":source,
            "hypothesis":u
        })

ids=[p["pair_id"] for p in pairs]
assert len(ids)==len(set(ids))
out=ROOT/"calibration"
pair_path=out/"V2_4_SEMANTIC_PAIR_MANIFEST_V1.jsonl"
pair_path.write_text("".join(json.dumps(p,ensure_ascii=False,sort_keys=True)+"\n" for p in pairs),encoding="utf-8")
para_path=out/"V2_4_SEMANTIC_PARAGRAPH_INDEX_V1.json"
para_path.write_text(json.dumps(paragraphs,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
manifest={
  "schema_version":"1.0.0",
  "status":"FROZEN_BEFORE_ANY_SEMANTIC_SCORE",
  "calibration_population_sha256":CAL_SHA,
  "source_assertions_sha256":sha256_bytes((ROOT/"SOURCE_ASSERTIONS_V1.json").read_bytes()),
  "paragraphs":len(paragraphs),
  "safe_paragraphs":sum(x["gold_label"]=="SAFE" for x in paragraphs),
  "adversarial_paragraphs":sum(x["gold_label"]=="ADVERSARIAL" for x in paragraphs),
  "pairs":len(pairs),
  "source_to_candidate_pairs":sum(x["direction"]=="SOURCE_TO_CANDIDATE" for x in pairs),
  "candidate_to_source_pairs":sum(x["direction"]=="CANDIDATE_TO_SOURCE" for x in pairs),
  "pair_manifest_sha256":sha256_bytes(pair_path.read_bytes()),
  "paragraph_index_sha256":sha256_bytes(para_path.read_bytes()),
  "semantic_scores_observed":False,
  "thresholds_observed":False
}
(out/"V2_4_SEMANTIC_PAIR_FREEZE_V1.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(manifest,indent=2))
