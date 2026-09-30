#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,urllib.request
from pathlib import Path
from collections import Counter

REV="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
BASE=f"https://raw.githubusercontent.com/CAMeL-Lab/arabic-gec/{REV}/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2014"
P0_SALT="M2R-V2-P0-DEV-A"
P1_SALT="M2R-V2-P1-DEV-B"
M2H_SALT="M2H-REMAINING-DEV-SPLIT-V1-20260930-A"
EXPECTED_CAL_SHA="3b6c1128f412531223b3c2e5346082d3290f40daac706eb13bbafa1db10a09c9"
AR=re.compile(r"[\u0600-\u06ff]")

def norm(s): return " ".join(s.strip().split())
def H(s): return hashlib.sha256(str(s).encode()).hexdigest()
def rank(*x): return H("|".join(map(str,x)))
def partition(uid):
    v=int(H(f"M2R-V2|{uid}")[:8],16)%100
    return "DEVELOPMENT" if v<70 else ("CONFIRMATION" if v<85 else "HOLDOUT")
def uid_digest(xs): return hashlib.sha256(("\n".join(xs)+"\n").encode()).hexdigest()

def dl(split,prefix,suf,out):
    urllib.request.urlretrieve(f"{BASE}/{split}/{prefix}.{suf}",out)
    if out.stat().st_size<20: raise RuntimeError(out)

def parse_m2(path):
    blocks=[];src=None;ed=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("S "):
            if src is not None: blocks.append((src,ed))
            src=line[2:];ed=[]
        elif line.startswith("A ") and src is not None:
            p=line[2:].split("|||");sp=p[0].split() if p else []
            if len(p)<3 or len(sp)<2 or p[-1].strip() not in {"","0"}: continue
            try:a,b=int(sp[0]),int(sp[1])
            except: continue
            ed.append({"start":a,"end":b,"type":p[1],"replacement":p[2]})
    if src is not None: blocks.append((src,ed))
    return blocks

def surf(src,e):
    t=src.split()
    return norm(" ".join(t[e["start"]:e["end"]]))

def apply(src,edits,skip=None):
    t=src.split()
    for i,e in sorted(enumerate(edits),key=lambda z:(z[1]["start"],z[1]["end"]),reverse=True):
        if i==skip: continue
        rr=[] if e["replacement"] in {"","-NONE-"} else e["replacement"].split()
        t[e["start"]:e["end"]]=rr
    return norm(" ".join(t))

def detectable(src,e):
    s=surf(src,e)
    return bool(s and AR.search(s))

def strict(src,e):
    s=surf(src,e);r=norm(e["replacement"])
    return (
        e["end"]-e["start"]==1 and bool(s) and bool(r)
        and " " not in s and " " not in r
        and bool(AR.search(s)) and bool(AR.search(r)) and s!=r
    )

def overlaps(e,other):
    return not (e["end"]<=other["start"] or other["end"]<=e["start"])

def build_records():
    work=Path("upstream/qalb14_m2h_calibration");work.mkdir(parents=True,exist_ok=True)
    records=[]
    for split,prefix in [("train","QALB-2014-L1-Train"),("dev","QALB-2014-L1-Dev")]:
        d=work/split;d.mkdir(exist_ok=True)
        for suf in ["sent.no_ids","cor.no_ids","m2"]:
            dl(split,prefix,suf,d/f"{prefix}.{suf}")
        srcs=(d/f"{prefix}.sent.no_ids").read_text(encoding="utf-8").splitlines()
        cors=(d/f"{prefix}.cor.no_ids").read_text(encoding="utf-8").splitlines()
        blocks=parse_m2(d/f"{prefix}.m2")
        if not(len(srcs)==len(cors)==len(blocks)): raise SystemExit("line count mismatch")
        for line_no,(s0,c0,(bs,ed)) in enumerate(zip(srcs,cors,blocks),1):
            uid=f"{split}:{line_no}"
            if partition(uid)!="DEVELOPMENT": continue
            s=norm(s0);c=norm(c0)
            if norm(bs)!=s or apply(s,ed)!=c: continue
            det=[]
            for i,e in enumerate(ed):
                ss=surf(s,e)
                if detectable(s,e) and s.count(ss)==1:
                    det.append((i,e,ss))
            stricts=[]
            for i,e,ss in det:
                if not strict(s,e): continue
                if any(j!=i and overlaps(e,oe) for j,oe in enumerate(ed)): continue
                stricts.append((i,e,ss))
            records.append({
                "uid":uid,"split":split,"line_no":line_no,
                "source":s,"reference":c,"edits":ed,
                "detectable":det,"stricts":stricts
            })
    return records

def choose_packet(records,salt,excluded):
    strict_pool=[]
    for r in records:
        if r["uid"] in excluded or not r["stricts"]: continue
        opts=sorted(r["stricts"],key=lambda x:rank(salt,r["uid"],x[0],x[2]))
        for wi,e,ss in opts:
            cand=apply(r["source"],r["edits"],skip=wi)
            if cand.count(ss)==1:
                strict_pool.append((r,wi,e,ss,cand));break
    strict_pool.sort(key=lambda x:rank(salt,"STRICT",x[0]["uid"]))
    sel_s=strict_pool[:30]
    used=set(excluded)|{x[0]["uid"] for x in sel_s}
    nat=[r for r in records if r["uid"] not in used and r["detectable"]]
    nat.sort(key=lambda r:rank(salt,"NAT",r["uid"]))
    sel_n=nat[:60]; used.update(r["uid"] for r in sel_n)
    clean=[r for r in records if r["uid"] not in used]
    clean.sort(key=lambda r:rank(salt,"CLEAN",r["uid"]))
    sel_c=clean[:30]
    if len(sel_s)!=30 or len(sel_n)!=60 or len(sel_c)!=30:
        raise SystemExit("packet reconstruction failure")
    return {x[0]["uid"] for x in sel_s}|{r["uid"] for r in sel_n}|{r["uid"] for r in sel_c}

records=build_records()
by_uid={r["uid"]:r for r in records}
all_dev=set(by_uid)

p0=choose_packet(records,P0_SALT,set())
p1=choose_packet(records,P1_SALT,p0)
if len(p0)!=120 or len(p1)!=120 or p0&p1: raise SystemExit("P0/P1 mismatch")

remaining=sorted(all_dev-p0-p1)
ranked=sorted(remaining,key=lambda uid:(H(M2H_SALT+"|"+uid),uid))
n=len(ranked); n_cal=n//2; n_eval=(4*n)//10
cal=ranked[:n_cal]
internal=set(ranked[n_cal:n_cal+n_eval])
stress=set(ranked[n_cal+n_eval:])

if uid_digest(cal)!=EXPECTED_CAL_SHA: raise SystemExit("CALIBRATION UID hash mismatch")
if set(cal)&internal or set(cal)&stress or internal&stress: raise SystemExit("split overlap")
if set(cal)&(p0|p1): raise SystemExit("consumed UID leak")

op_counts=Counter()
changed=unchanged=0
out=[]
for idx,uid in enumerate(cal,1):
    r=by_uid[uid]
    gold=[]
    for e in r["edits"]:
        s=surf(r["source"],e)
        gold.append({
            "surface":s,
            "replacement":norm(e["replacement"]),
            "m2_type":e["type"],
            "source_span":[e["start"],e["end"]]
        })
        op_counts[e["type"]]+=1
    changed += int(r["source"]!=r["reference"])
    unchanged += int(r["source"]==r["reference"])
    out.append({
        "case_id":f"M2H-CAL-{idx:05d}",
        "uid":uid,
        "split":r["split"],
        "line_no":r["line_no"],
        "source":r["source"],
        "reference":r["reference"],
        "gold_edits":gold
    })

Path("M2H_CALIBRATION_V1.jsonl").write_text(
    "\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8"
)
summary={
  "status":"M2H_CALIBRATION_MATERIALIZED",
  "source_revision":REV,
  "split_salt":M2H_SALT,
  "calibration_uid_sha256":EXPECTED_CAL_SHA,
  "cases":len(out),
  "changed_source_reference":changed,
  "unchanged_source_reference":unchanged,
  "m2_operation_counts":dict(op_counts),
  "origin_counts":dict(Counter(x["split"] for x in out)),
  "integrity":{
    "calibration_only":True,
    "internal_evaluation_text_materialized":False,
    "stress_diagnostic_text_materialized":False,
    "p0_p1_overlap":0,
    "confirmation_opened":False,
    "holdout_opened":False,
    "a7ta_reserved_opened":False,
    "qalb15_test_opened":False
  }
}
Path("M2H_CALIBRATION_SUMMARY_V1.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2))
