"""Materialize label-free post-edit stability + morphology decisions."""
from __future__ import annotations
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
CONS=ART/"consensus"/"POSTEDIT_CONSENSUS_LINES.jsonl"
EVENTS={
    "SWEET_Q14":ART/"sweet_q14_post"/"TRI_SWEET_Q14_POSTEDIT_EVENTS.jsonl",
    "SWEET_ZAEBUC":ART/"sweet_zaebuc_post"/"TRI_SWEET_ZAEBUC_POSTEDIT_EVENTS.jsonl",
    "ARABART_Q14":ART/"arabart_post"/"TRI_ARABART_Q14_POSTEDIT_EVENTS.jsonl",
}
MORPH=ART/"morph"/"POSTEDIT_MORPH_IDENTITY.jsonl"
OUT=ROOT/"PHASE2_POSTEDIT_MORPH_FEATURES.jsonl"
SUMMARY=ROOT/"PHASE2_POSTEDIT_MORPH_RUNTIME.json"

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def overlaps(a,b):
    if a[0]<0 or b[0]<0:return False
    return max(a[0],b[0])<min(a[1],b[1])

def main():
    cons=jl(CONS)
    second={k:jl(p) for k,p in EVENTS.items()}
    morph={x["vote_id"]:x for x in jl(MORPH)}
    byline={v:{} for v in second}
    for voter,rows in second.items():
        for x in rows:byline[voter].setdefault(int(x["line_id"]),[]).append(x)

    out=[]
    for line in cons:
        lid=int(line["line_id"])
        for t in line["targets"]:
            span=list(map(int,t["source_lexical_span"]))
            i=span[0]
            window=[max(0,i-1),i+2]
            target_hits={}
            window_hits={}
            unanchored={}
            for voter in second:
                rows=byline[voter].get(lid,[])
                target_hits[voter]=sum(overlaps(x["source_lexical_span"],span) for x in rows)
                window_hits[voter]=sum(overlaps(x["source_lexical_span"],window) for x in rows)
                unanchored[voter]=sum((x["source_lexical_span"]==[-1,-1]) for x in rows)
            target_stable=all(target_hits[v]==0 for v in second)
            window_stable=all(window_hits[v]==0 for v in second)
            m=morph[t["vote_id"]]
            morph_safe=bool(m["morph_identity_safe"])
            out.append({
                "vote_id":t["vote_id"],
                "line_id":lid,
                "line_hash":line["line_hash"],
                "source_lexical_span":span,
                "source_hash":t["source_hash"],
                "candidate_hash":t["candidate_hash"],
                "second_pass_target_hits":target_hits,
                "second_pass_window1_hits":window_hits,
                "second_pass_unanchored_insertions_on_line":unanchored,
                "target_stable_all3":target_stable,
                "window1_stable_all3":window_stable,
                "morph_analysis_available":m["analysis_available"],
                "morph_field_equal":m["field_equal"],
                "morph_identity_safe":morph_safe,
                "runtime_decisions":{
                    "POST_EDIT_TARGET_STABLE_ALL3":"PASS" if target_stable else "REVIEW",
                    "POST_EDIT_WINDOW1_STABLE_ALL3":"PASS" if window_stable else "REVIEW",
                    "MORPH_IDENTITY_SAFE":"PASS" if morph_safe else "REVIEW",
                    "TARGET_STABLE_AND_MORPH_SAFE":"PASS" if (target_stable and morph_safe) else "REVIEW",
                },
            })
    assert len(out)==142,len(out)
    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    policies=list(out[0]["runtime_decisions"])
    counts={p:{
        "PASS":sum(x["runtime_decisions"][p]=="PASS" for x in out),
        "REVIEW":sum(x["runtime_decisions"][p]=="REVIEW" for x in out),
    } for p in policies}
    obj={
        "status":"PHASE2_POSTEDIT_MORPH_RUNTIME_FROZEN",
        "diagnostic_only":True,
        "labels_or_gold_read":False,
        "source_population":"142 consumed UNANIMOUS_3 events from run 36517205396",
        "rows":len(out),
        "decision_counts":counts,
        "target_unanchored_insertion_limitation":"Pure second-pass insertions use [-1,-1] in the established event representation and therefore do not count as target/window overlap. Their per-line counts are retained diagnostically.",
        "features_sha256":sha_file(OUT),
        "qalb_text_persisted":False,
        "qalb15_test_read":False,
        "policy_frozen_before_labels":True,
    }
    SUMMARY.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")+SUMMARY.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic text leaked"
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":
    main()
