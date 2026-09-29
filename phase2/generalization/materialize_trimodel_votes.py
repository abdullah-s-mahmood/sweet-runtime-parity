"""Materialize frozen tri-model edit votes. Gold-blind."""
from __future__ import annotations
import json,hashlib
from pathlib import Path
from phase2.generalization.cross_model_common import read_jsonl,protected_risk,sha_text

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
FILES={
 "SWEET_Q14":ART/"sweet_q14"/"TRI_SWEET_Q14_EVENTS.jsonl",
 "SWEET_ZAEBUC":ART/"sweet_zaebuc"/"TRI_SWEET_ZAEBUC_EVENTS.jsonl",
 "ARABART_Q14":ART/"arabart_q14"/"TRI_ARABART_Q14_EVENTS.jsonl",
}
SUMS={
 "SWEET_Q14":ART/"sweet_q14"/"TRI_SWEET_Q14_SUMMARY.json",
 "SWEET_ZAEBUC":ART/"sweet_zaebuc"/"TRI_SWEET_ZAEBUC_SUMMARY.json",
 "ARABART_Q14":ART/"arabart_q14"/"TRI_ARABART_Q14_SUMMARY.json",
}
OUT=ART/"TRIMODEL_VOTE_FEATURES.jsonl"
SUMMARY=ART/"TRIMODEL_VOTE_RUNTIME.json"

def single_sub(e):
    sp=e.get("source_lexical_span") or [-1,-1]
    return e.get("primitive_ops")==["SUB"] and len(e.get("source_bases") or [])==1 and len(e.get("output_bases") or [])==1 and sp[0]>=0 and sp[1]-sp[0]==1

def key(e):
    return (int(e["line_id"]),tuple(map(int,e["source_lexical_span"])),tuple(e["source_bases"]),tuple(e["output_bases"]))

def main():
    sums={k:json.loads(p.read_text(encoding="utf-8")) for k,p in SUMS.items()}
    seeds={v["selection_seed"] for v in sums.values()}
    assert len(seeds)==1,seeds
    ids=[v["selected_line_ids"] for v in sums.values()]
    hashes=[v["selected_line_hashes"] for v in sums.values()]
    raws={v["raw_sha256"] for v in sums.values()}
    assert all(x==ids[0] for x in ids)
    assert all(x==hashes[0] for x in hashes)
    assert len(raws)==1
    assert all(v["gold_read"] is False for v in sums.values())

    events={k:read_jsonl(p) for k,p in FILES.items()}
    maps={}
    for voter,rows in events.items():
        m={}
        for e in rows:
            if not single_sub(e):continue
            m.setdefault(key(e),[]).append(e)
        maps[voter]=m

    allkeys=set().union(*[set(m.keys()) for m in maps.values()])
    rows=[]
    for k in sorted(allkeys):
        voters=[v for v,m in maps.items() if k in m]
        if not voters:continue
        line_id,span,sbases,obases=k
        source_hash=sha_text("\u241f".join(sbases)); output_hash=sha_text("\u241f".join(obases))
        sample=maps[voters[0]][k][0]
        veto=sorted(set(sum([protected_risk(maps[v][k][0]) for v in voters],[])))
        u3=(len(voters)==3 and not veto)
        ara_any=("ARABART_Q14" in voters and ("SWEET_Q14" in voters or "SWEET_ZAEBUC" in voters) and not veto)
        both_sweet=("SWEET_Q14" in voters and "SWEET_ZAEBUC" in voters and not veto)
        rows.append({
          "vote_id":"TRIV-"+sha_text("|".join([str(line_id),str(span),source_hash,output_hash]))[:20],
          "line_id":line_id,"line_hash":sample["line_hash"],"source_lexical_span":list(span),
          "source_hash":source_hash,"output_hash":output_hash,
          "voters":sorted(voters),"voter_count":len(voters),"veto_reasons":veto,
          "runtime_decisions":{
            "UNANIMOUS_3":"ACCEPT" if u3 else ("REJECT" if veto else "REVIEW"),
            "ARABART_PLUS_ANY_SWEET":"ACCEPT" if ara_any else ("REJECT" if veto else "REVIEW"),
            "BOTH_SWEETS":"DIAGNOSTIC" if both_sweet else "REVIEW",
          },
          "source_bases":list(sbases),"output_bases":list(obases),
        })
    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    pol=["UNANIMOUS_3","ARABART_PLUS_ANY_SWEET","BOTH_SWEETS"]
    counts={p:{} for p in pol}
    for p in pol:
      for d in ["ACCEPT","REVIEW","REJECT","DIAGNOSTIC"]:
        n=sum(x["runtime_decisions"][p]==d for x in rows)
        if n:counts[p][d]=n
    obj={"status":"TRIMODEL_VOTES_FROZEN","gold_read":False,"selection_seed":next(iter(seeds)),
         "selected_line_ids":ids[0],"selected_line_hashes":hashes[0],"raw_sha256":next(iter(raws)),
         "vote_rows":len(rows),"decision_counts":counts,"policy_frozen_before_gold":True,"qalb15_test_read":False}
    SUMMARY.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in obj.items() if k!="selected_line_hashes"},ensure_ascii=False))
if __name__=="__main__":main()
