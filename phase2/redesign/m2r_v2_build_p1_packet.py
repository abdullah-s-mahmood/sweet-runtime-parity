#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,urllib.request
from collections import Counter
from pathlib import Path

REV="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
BASE=f"https://raw.githubusercontent.com/CAMeL-Lab/arabic-gec/{REV}/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2014"
SALT0="M2R-V2-P0-DEV-A"
SALT1="M2R-V2-P1-DEV-B"
AR=re.compile(r"[\u0600-\u06ff]")

def norm(s): return " ".join(s.strip().split())
def H(s): return hashlib.sha256(str(s).encode()).hexdigest()
def rank(*x): return H("|".join(map(str,x)))
def partition(uid):
    v=int(H(f"M2R-V2|{uid}")[:8],16)%100
    return "DEVELOPMENT" if v<70 else ("CONFIRMATION" if v<85 else "HOLDOUT")

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
        and bool(AR.search(s)) and bool(AR.search(r))
        and s!=r
    )

def overlaps(e,other):
    return not (e["end"]<=other["start"] or other["end"]<=e["start"])

def build_records():
    work=Path("upstream/qalb14v2p1");work.mkdir(parents=True,exist_ok=True)
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
                strict_pool.append((r,wi,e,ss,cand))
                break
    strict_pool.sort(key=lambda x:rank(salt,"STRICT",x[0]["uid"]))
    sel_s=strict_pool[:30]
    if len(sel_s)<30: raise SystemExit(f"insufficient strict pool: {len(sel_s)}")
    used=set(excluded)|{x[0]["uid"] for x in sel_s}

    nat=[r for r in records if r["uid"] not in used and r["detectable"]]
    nat.sort(key=lambda r:rank(salt,"NAT",r["uid"]))
    sel_n=nat[:60]
    if len(sel_n)<60: raise SystemExit(f"insufficient natural: {len(sel_n)}")
    used.update(r["uid"] for r in sel_n)

    clean=[r for r in records if r["uid"] not in used]
    clean.sort(key=lambda r:rank(salt,"CLEAN",r["uid"]))
    sel_c=clean[:30]
    if len(sel_c)<30: raise SystemExit(f"insufficient clean: {len(sel_c)}")

    packet_uids={x[0]["uid"] for x in sel_s}|{r["uid"] for r in sel_n}|{r["uid"] for r in sel_c}
    return sel_s,sel_n,sel_c,packet_uids,len(strict_pool)

records=build_records()

# Reconstruct P0 exactly.
p0_s,p0_n,p0_c,p0_uids,p0_strict_pool=choose_packet(records,SALT0,set())
if len(p0_uids)!=120:
    raise SystemExit(f"P0 reconstruction failed: {len(p0_uids)}")

# Build P1 only after excluding every P0 UID.
p1_s,p1_n,p1_c,p1_uids,p1_strict_pool=choose_packet(records,SALT1,p0_uids)
overlap=p0_uids & p1_uids
if overlap:
    raise SystemExit(f"P0/P1 overlap detected: {sorted(overlap)[:10]}")
if len(p1_uids)!=120:
    raise SystemExit(f"P1 unique uid failure: {len(p1_uids)}")
if any(partition(uid)!="DEVELOPMENT" for uid in p1_uids):
    raise SystemExit("partition leak")

rows=[]
for r in p1_n:
    gold=[{
        "surface":ss,
        "replacement":norm(e["replacement"]),
        "m2_type":e["type"],
        "source_span":[e["start"],e["end"]]
    } for i,e,ss in r["detectable"]]
    rows.append(("NATURAL_QALB_SOURCE",r,r["source"],gold,False))

for r in p1_c:
    rows.append(("CLEAN_QALB_REFERENCE",r,r["reference"],[],False))

for r,wi,e,ss,cand in p1_s:
    gold=[{
        "surface":ss,
        "replacement":norm(e["replacement"]),
        "m2_type":e["type"],
        "source_span":[e["start"],e["end"]]
    }]
    rows.append(("QALB_ALL_BUT_ONE_STRICT",r,cand,gold,True))

rows.sort(key=lambda x:rank(SALT1,"SHUFFLE",x[1]["uid"],x[0]))

blind=[];key=[];gold_count=0
for i,(fam,r,cand,gold,controlled) in enumerate(rows,1):
    cid=f"M2RV2-P1-{i:03d}"
    gold_count+=len(gold)
    blind.append({"case_id":cid,"candidate":cand})
    key.append({
        "case_id":cid,
        "uid":r["uid"],
        "split":r["split"],
        "line_no":r["line_no"],
        "family":fam,
        "gold_errors":gold,
        "controlled_counterfactual":controlled
    })

fc=Counter(x["family"] for x in key)
expected={"NATURAL_QALB_SOURCE":60,"CLEAN_QALB_REFERENCE":30,"QALB_ALL_BUT_ONE_STRICT":30}
if len(blind)!=120 or len(key)!=120: raise SystemExit("size failure")
if len({x["uid"] for x in key})!=120: raise SystemExit("P1 uid uniqueness failure")
if fc!=expected: raise SystemExit(f"family count failure: {fc}")
if set(x["uid"] for x in key)&p0_uids: raise SystemExit("final overlap failure")

Path("M2RV2_P1_DEV_BLIND.jsonl").write_text(
    "\n".join(json.dumps(x,ensure_ascii=False) for x in blind)+"\n",encoding="utf-8"
)
Path("M2RV2_P1_DEV_KEY.jsonl").write_text(
    "\n".join(json.dumps(x,ensure_ascii=False) for x in key)+"\n",encoding="utf-8"
)
summary={
    "status":"M2R_V2_P1_PACKET_READY",
    "cases":120,
    "family_counts":dict(fc),
    "unique_p1_uids":120,
    "reconstructed_p0_uids":120,
    "p0_p1_overlap":0,
    "gold_error_instances":gold_count,
    "p1_strict_pool_after_p0_exclusion":p1_strict_pool,
    "development_reconstructable_records":len(records),
    "confirmation_exposed":False,
    "holdout_exposed":False,
    "forbidden_source_read":False,
    "p0_salt":SALT0,
    "p1_salt":SALT1
}
Path("M2RV2_P1_PACKET_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
