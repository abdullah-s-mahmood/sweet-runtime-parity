"""Gold-blind risk-family assignment for frozen exact cross-model agreements.

Uses only source/output base strings from the frozen runtime artifact.
No gold, human labels, QALB corrected text, or QALB TEST.
Persists only hashes + transformation family, not lexical strings.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
AG=ROOT/"artifacts"/"agreement"/"artifacts"/"CROSS_MODEL_AGREEMENT_FEATURES.jsonl"
OUT=ROOT/"artifacts"/"RISK_FAMILY_FEATURES.jsonl"
SUM=ROOT/"artifacts"/"RISK_FAMILY_RUNTIME.json"
EXPECTED_AGREEMENT_SHA="d66a5ab3c6b9e1527b7a1a59ddce0f843a864281e70106cacd58d00315741c4c"

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def read_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def hamza_norm(s):
    table={"أ":"ا","إ":"ا","آ":"ا","ؤ":"و","ئ":"ي","ء":""}
    return "".join(table.get(ch,ch) for ch in s)

def lev(a,b):
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1):
            cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]

def one_n_insert_delete(a,b):
    if abs(len(a)-len(b))!=1:return False
    short,long=(a,b) if len(a)<len(b) else (b,a)
    for i,ch in enumerate(long):
        if ch=="ن" and long[:i]+long[i+1:]==short:
            return True
    return False

def family(s,o):
    assert s!=o
    if hamza_norm(s)==hamza_norm(o):
        return "HAMZA_ONLY"
    if len(s)==len(o) and len(s)>0 and s[:-1]==o[:-1] and {s[-1],o[-1]}=={"ة","ه"}:
        return "TA_MARBUTA_HA_ONLY"
    if len(s)==len(o) and len(s)>0 and s[:-1]==o[:-1] and {s[-1],o[-1]}=={"ى","ي"}:
        return "ALIF_MAQSURA_YA_ONLY"
    if (o==s+"ا" and s.endswith("و")) or (s==o+"ا" and o.endswith("و")):
        return "WAW_ALIF_ONLY"
    if o==s+"ا" or s==o+"ا":
        return "FINAL_ALIF_OTHER"
    if one_n_insert_delete(s,o):
        return "NUN_ONLY"
    if (len(o)==len(s)+1 and o[1:]==s) or (len(s)==len(o)+1 and s[1:]==o):
        return "PREFIX_ONE_CHAR"
    if (len(o)==len(s)+1 and o[:-1]==s) or (len(s)==len(o)+1 and s[:-1]==o):
        return "SUFFIX_ONE_CHAR_OTHER"
    if len(s)==len(o) and sum(a!=b for a,b in zip(s,o))==1:
        return "SINGLE_CHAR_SUBSTITUTION_OTHER"
    return "MULTI_CHAR_OR_OTHER"

def main():
    if sha_file(AG)!=EXPECTED_AGREEMENT_SHA:
        raise RuntimeError("Frozen agreement features SHA mismatch")
    events=[x for x in read_jsonl(AG) if x["runtime_decisions"]["EXACT_SINGLE_SUB_AGREEMENT"]=="ACCEPT"]
    assert len(events)==159,len(events)
    rows=[]
    counts={}
    for e in events:
        sb=e.get("source_bases") or []
        ob=e.get("output_bases") or []
        assert len(sb)==len(ob)==1,(e["agreement_id"],sb,ob)
        fam=family(sb[0],ob[0])
        counts[fam]=counts.get(fam,0)+1
        rows.append({
            "agreement_id":e["agreement_id"],
            "line_id":e["line_id"],
            "line_hash":e["line_hash"],
            "source_lexical_span":e["source_lexical_span"],
            "source_hash":e["source_hash"],
            "candidate_hash":e["output_hash"],
            "risk_family":fam,
            "char_edit_distance":lev(sb[0],ob[0]),
            "length_delta":len(ob[0])-len(sb[0]),
        })
    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    summary={
        "status":"RISK_FAMILY_RUNTIME_FROZEN",
        "exploratory_only":True,
        "gold_or_manual_labels_read":False,
        "agreement_features_sha256":sha_file(AG),
        "rows":len(rows),
        "family_counts":dict(sorted(counts.items())),
        "qalb15_test_read":False,
        "lexical_strings_persisted":False,
    }
    SUM.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
