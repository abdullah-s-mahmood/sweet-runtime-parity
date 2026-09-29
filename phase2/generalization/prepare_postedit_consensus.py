"""Prepare jointly corrected tri-model lines for post-edit diagnostics.

Reads frozen first-pass voter artifacts + QALB RAW only.
No gold/manual labels are read.
Output contains QALB-derived text and is ephemeral CI evidence only.
"""
from __future__ import annotations
import json
from pathlib import Path

from phase2.arabart_audit.build_full_arabart_edit_queue import units
from phase2.generalization.cross_model_common import read_jsonl
from phase2.generalization.materialize_trimodel_votes import main as materialize_votes

ROOT=Path(__file__).resolve().parents[2]
UP=ROOT/"upstream"/"arabic-gec"
RAW=UP/"data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2015/train/QALB-2015-L2-Train.sent.no_ids"
ART=ROOT/"artifacts"
VOTES=ART/"TRIMODEL_VOTE_FEATURES.jsonl"
ARA=ART/"arabart_q14"/"TRI_ARABART_Q14_EVENTS.jsonl"
OUT=ART/"POSTEDIT_CONSENSUS_LINES.jsonl"
SUM=ART/"POSTEDIT_CONSENSUS_SUMMARY.json"

def read_lines(p):
    return [x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def event_key(e):
    return (
        int(e["line_id"]),
        tuple(map(int,e["source_lexical_span"])),
        tuple(e.get("source_bases") or []),
        tuple(e.get("output_bases") or []),
    )

def main():
    materialize_votes()
    votes=[
        x for x in read_jsonl(VOTES)
        if x["runtime_decisions"]["UNANIMOUS_3"]=="ACCEPT"
    ]
    assert len(votes)==142,len(votes)
    raw=read_lines(RAW)
    ara=read_jsonl(ARA)
    amap={}
    for e in ara:
        amap.setdefault(event_key(e),[]).append(e)

    byline={}
    for v in votes:
        byline.setdefault(int(v["line_id"]),[]).append(v)

    rows=[]
    for line_id,vs in sorted(byline.items()):
        source=raw[line_id-1]
        us=units(source)
        replacements=[]
        targets=[]
        for v in vs:
            span=list(map(int,v["source_lexical_span"]))
            assert span[1]-span[0]==1,span
            i=span[0]
            assert 0<=i<len(us),(line_id,i,len(us))
            u=us[i]
            k=(line_id,tuple(span),tuple(v["source_bases"]),tuple(v["output_bases"]))
            matches=amap.get(k) or []
            assert matches,(line_id,span,v["vote_id"])
            surf=(matches[0].get("output_surfaces") or [])
            assert len(surf)==1,(v["vote_id"],surf)
            assert u["base"]==v["source_bases"][0],(v["vote_id"],u["base"],v["source_bases"])
            replacements.append((u["span"][0],u["span"][1],surf[0],v["vote_id"]))
            targets.append({
                "vote_id":v["vote_id"],
                "source_lexical_span":span,
                "source_hash":v["source_hash"],
                "candidate_hash":v["output_hash"],
            })

        corrected=source
        for a,b,surf,_ in sorted(replacements,reverse=True):
            corrected=corrected[:a]+surf+corrected[b:]

        su=units(source); cu=units(corrected)
        assert len(su)==len(cu),(line_id,len(su),len(cu))
        rows.append({
            "line_id":line_id,
            "line_hash":vs[0]["line_hash"],
            "source_text":source,
            "corrected_text":corrected,
            "targets":targets,
        })

    assert sum(len(x["targets"]) for x in rows)==142
    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    obj={
        "status":"POSTEDIT_CONSENSUS_LINES_READY",
        "gold_or_manual_labels_read":False,
        "source_run_id":36517205396,
        "lines":len(rows),
        "targets":sum(len(x["targets"]) for x in rows),
        "qalb_text_ephemeral_only":True,
        "qalb15_test_read":False,
    }
    SUM.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(obj,ensure_ascii=False))

if __name__=="__main__":
    main()
