"""Build a complete base-letter AraBART edit-event queue.

Development-only audit of the persisted AraBART second-generator output.
This script does not run a model and does not use human/gold labels in
alignment. It represents substitutions, deletions, insertions, and contiguous
complex word-level events for later linguistic adjudication.

Diacritics and punctuation are ignored for alignment identity because the
AraBART pipeline uses morphology/dediacritized model input; full surface
correctness is judged later against the original source.
"""
from __future__ import annotations
import json, re, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
GEN=ROOT/"PHASE2_ARABART_SECOND_GENERATOR.json"
DEV=ROOT/"phase2"/"arabic_eval"/"DEVELOPMENT_TARGETS.jsonl"
OUT=ROOT/"PHASE2_ARABART_FULL_EDIT_ADJUDICATION_QUEUE.jsonl"
SUM=ROOT/"PHASE2_ARABART_FULL_EDIT_ADJUDICATION_QUEUE_SUMMARY.json"


def read_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def strip_marks(s):
    return "".join(ch for ch in unicodedata.normalize("NFC",s)
                   if unicodedata.category(ch)!="Mn" and ch!="ـ")


def is_punc_or_symbol(ch):
    return unicodedata.category(ch)[0] in {"P","S"}


def base(s):
    return "".join(ch for ch in strip_marks(s)
                   if not is_punc_or_symbol(ch) and not ch.isspace())


def units(text):
    out=[]
    for wi,m in enumerate(re.finditer(r"\S+",text)):
        b=base(m.group(0))
        if b:
            out.append({
                "lexical_index":len(out),
                "whitespace_word_index":wi,
                "surface":m.group(0),
                "base":b,
                "span":[m.start(),m.end()]
            })
    return out


def lev(a,b):
    if a==b:return 0
    if not a:return len(b)
    if not b:return len(a)
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1):
            cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]


def sub_cost(a,b):
    if a==b:return 0.0
    return min(1.0,lev(a,b)/max(len(a),len(b),1))


def align(src_text,out_text):
    s=units(src_text); o=units(out_text); n=len(s);m=len(o)
    dp=[[0.0]*(m+1) for _ in range(n+1)]
    back=[[None]*(m+1) for _ in range(n+1)]
    for i in range(1,n+1):dp[i][0]=i;back[i][0]="DEL"
    for j in range(1,m+1):dp[0][j]=j;back[0][j]="INS"
    for i in range(1,n+1):
        for j in range(1,m+1):
            c=sub_cost(s[i-1]["base"],o[j-1]["base"])
            opts=[
                (dp[i-1][j-1]+c,"KEEP" if c==0 else "SUB"),
                (dp[i-1][j]+1.0,"DEL"),
                (dp[i][j-1]+1.0,"INS"),
            ]
            dp[i][j],back[i][j]=min(opts,key=lambda z:z[0])
    ops=[];i=n;j=m
    while i or j:
        op=back[i][j]
        if op in {"KEEP","SUB"}:
            ops.append({"op":op,"src":s[i-1],"out":o[j-1],
                        "cost":sub_cost(s[i-1]["base"],o[j-1]["base"])})
            i-=1;j-=1
        elif op=="DEL":
            ops.append({"op":"DEL","src":s[i-1],"out":None,"cost":1.0});i-=1
        elif op=="INS":
            ops.append({"op":"INS","src":None,"out":o[j-1],"cost":1.0});j-=1
        else:
            raise RuntimeError((i,j,op))
    ops.reverse()
    return ops,dp[n][m]


def group_nonkeep(ops):
    groups=[];cur=[]
    for op in ops:
        if op["op"]=="KEEP":
            if cur:groups.append(cur);cur=[]
        else:
            cur.append(op)
    if cur:groups.append(cur)
    return groups


def main():
    gen=json.loads(GEN.read_text(encoding="utf-8"))
    dev=read_jsonl(DEV)
    bypid={}
    for r in dev:bypid.setdefault(int(r["passage_id"]),[]).append(r)

    rows=[];counter=0;passages_with_edits=set()
    stats={"SUB":0,"DEL":0,"INS":0,"COMPLEX":0}
    for spid,p in sorted(gen["passages"].items(),key=lambda z:int(z[0])):
        pid=int(spid);source=p["source"];output=p["generated_raw"]
        ops,cost=align(source,output)
        groups=group_nonkeep(ops)
        for g in groups:
            counter+=1;passages_with_edits.add(pid)
            srcs=[x["src"] for x in g if x["src"]]
            outs=[x["out"] for x in g if x["out"]]
            kinds=[x["op"] for x in g]
            if len(g)==1:k=kinds[0]
            else:k="COMPLEX"
            stats[k]=stats.get(k,0)+1
            if srcs:
                sa=min(x["span"][0] for x in srcs);sb=max(x["span"][1] for x in srcs)
                src_span=[sa,sb];src_text=source[sa:sb]
                ovs=[r for r in bypid.get(pid,[])
                     if sa<int(r["target_end"]) and sb>int(r["target_start"])]
            else:
                # Insert event: anchor after previous source op if possible.
                pos=None
                first_idx=ops.index(g[0])
                for prev in reversed(ops[:first_idx]):
                    if prev["src"]:
                        pos=prev["src"]["span"][1];break
                if pos is None:pos=0
                src_span=[pos,pos];src_text=""
                ovs=[]
            rows.append({
                "arabart_event_id":f"ABEV-{pid}-{counter}",
                "passage_id":pid,
                "source_passage":source,
                "arabart_generated_passage":output,
                "event_type":k,
                "primitive_ops":kinds,
                "source_span":src_span,
                "source_text":src_text,
                "source_words":[x["surface"] for x in srcs],
                "source_bases":[x["base"] for x in srcs],
                "arabart_words":[x["surface"] for x in outs],
                "arabart_bases":[x["base"] for x in outs],
                "event_cost":sum(float(x["cost"]) for x in g),
                "passage_alignment_cost":cost,
                "overlapping_published_targets":[{
                    "case_id":r["case_id"],"target_id":r["target_id"],
                    "category_hint":r["category_hint"],
                    "target_error":r["target_error"],
                    "target_correction":r["target_correction"],
                    "target_span":[r["target_start"],r["target_end"]],
                    "single_target_reference":r["reference"],
                } for r in ovs],
                "adjudication_contract":{
                    "event_class":[
                        "SUPPORTED_CORRECTION","SUPPORTED_ALTERNATIVE",
                        "PARTIAL_CORRECTION","UNNECESSARY_EDIT",
                        "WRONG_CORRECTION","ALIGNMENT_UNCERTAIN","REVIEW_REQUIRED"
                    ],
                    "severity":["LOW","MEDIUM","HIGH","CRITICAL"],
                    "note":"Judge the local AraBART event in full original passage context. Nahw targets are local and non-overlap is not evidence of wrongness."
                }
            })

    summary={
        "status":"READY_FOR_FULL_ARABART_EDIT_EVENT_ADJUDICATION",
        "event_rows":len(rows),
        "passages_with_events":len(passages_with_edits),
        "event_types":stats,
        "events_overlapping_published_target":sum(bool(x["overlapping_published_targets"]) for x in rows),
        "unique_published_targets_touched":len({z["target_id"] for x in rows for z in x["overlapping_published_targets"]}),
        "scope":"Base-letter word-alignment events from full persisted AraBART output, including substitutions, insertions, deletions, and contiguous complex events.",
        "alignment_identity":"Arabic combining marks/tatweel/punctuation ignored for word identity; original full surfaces retained for adjudication.",
        "important_limitations":[
            "Dynamic-programming word alignment is a development representation, not ground truth.",
            "Complex events may need human alignment judgment.",
            "Full AraBART output is evidence only and is never product output.",
            "Published Nahw references are local corrections, not exhaustive passage gold."
        ],
        "development_only":True,"not_sealed":True
    }
    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    SUM.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))


if __name__=="__main__":
    main()
