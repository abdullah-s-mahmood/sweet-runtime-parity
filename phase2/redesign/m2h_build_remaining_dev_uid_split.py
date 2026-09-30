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
    work=Path("upstream/qalb14_m2h_uid_scan");work.mkdir(parents=True,exist_ok=True)
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
            records.append({"uid":uid,"source":s,"edits":ed,"detectable":det,"stricts":stricts})
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
    if len(sel_s)<30: raise SystemExit("insufficient strict pool")
    used=set(excluded)|{x[0]["uid"] for x in sel_s}

    nat=[r for r in records if r["uid"] not in used and r["detectable"]]
    nat.sort(key=lambda r:rank(salt,"NAT",r["uid"]))
    sel_n=nat[:60]
    if len(sel_n)<60: raise SystemExit("insufficient natural")
    used.update(r["uid"] for r in sel_n)

    clean=[r for r in records if r["uid"] not in used]
    clean.sort(key=lambda r:rank(salt,"CLEAN",r["uid"]))
    sel_c=clean[:30]
    if len(sel_c)<30: raise SystemExit("insufficient clean")

    return {x[0]["uid"] for x in sel_s}|{r["uid"] for r in sel_n}|{r["uid"] for r in sel_c}

records=build_records()
all_dev={r["uid"] for r in records}

p0=choose_packet(records,P0_SALT,set())
p1=choose_packet(records,P1_SALT,p0)
if len(p0)!=120 or len(p1)!=120 or p0&p1:
    raise SystemExit("P0/P1 reconstruction mismatch")

remaining=sorted(all_dev-p0-p1)
if len(remaining)!=len(all_dev)-240:
    raise SystemExit("remaining-count mismatch")
if any(partition(uid)!="DEVELOPMENT" for uid in remaining):
    raise SystemExit("non-development UID leaked")

ranked=sorted(remaining,key=lambda uid:(H(M2H_SALT+"|"+uid),uid))
n=len(ranked)
n_cal=n//2
n_eval=(4*n)//10
cal=ranked[:n_cal]
internal=ranked[n_cal:n_cal+n_eval]
stress=ranked[n_cal+n_eval:]

assert not (set(cal)&set(internal) or set(cal)&set(stress) or set(internal)&set(stress))
assert not ((set(cal)|set(internal)|set(stress)) & (p0|p1))
assert len(cal)+len(internal)+len(stress)==n

def digest_uids(xs):
    return hashlib.sha256(("\n".join(xs)+"\n").encode()).hexdigest()

manifest={
  "record_id":"M2H_REMAINING_DEVELOPMENT_UID_SPLIT_V1",
  "status":"UID_ONLY_SPLIT_READY",
  "source_revision":REV,
  "partition_rule":"existing M2-R v2 DEVELOPMENT partition",
  "split_salt":M2H_SALT,
  "development_reconstructable_records":len(all_dev),
  "excluded":{
    "m2r_p0_uids":len(p0),
    "m2r_p1_uids":len(p1),
    "p0_p1_overlap":len(p0&p1)
  },
  "remaining_uids":n,
  "counts":{
    "CALIBRATION":len(cal),
    "INTERNAL_EVALUATION":len(internal),
    "STRESS_DIAGNOSTIC":len(stress)
  },
  "uid_list_sha256":{
    "CALIBRATION":digest_uids(cal),
    "INTERNAL_EVALUATION":digest_uids(internal),
    "STRESS_DIAGNOSTIC":digest_uids(stress),
    "ALL_REMAINING":digest_uids(ranked)
  },
  "split_origin_counts":{
    "CALIBRATION":dict(Counter(x.split(":")[0] for x in cal)),
    "INTERNAL_EVALUATION":dict(Counter(x.split(":")[0] for x in internal)),
    "STRESS_DIAGNOSTIC":dict(Counter(x.split(":")[0] for x in stress))
  },
  "uids":{
    "CALIBRATION":cal,
    "INTERNAL_EVALUATION":internal,
    "STRESS_DIAGNOSTIC":stress
  },
  "integrity":{
    "text_persisted":False,
    "source_text_in_manifest":False,
    "reference_text_in_manifest":False,
    "gold_edits_in_manifest":False,
    "candidate_text_in_manifest":False,
    "confirmation_opened":False,
    "holdout_opened":False,
    "a7ta_reserved_opened":False,
    "qalb15_test_opened":False
  }
}
Path("M2H_REMAINING_DEV_UID_SPLIT_V1.json").write_text(
    json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
summary={k:manifest[k] for k in [
    "status","development_reconstructable_records","excluded",
    "remaining_uids","counts","uid_list_sha256","split_origin_counts","integrity"
]}
Path("M2H_REMAINING_DEV_UID_SPLIT_SUMMARY_V1.json").write_text(
    json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
print(json.dumps(summary,ensure_ascii=False,indent=2))
