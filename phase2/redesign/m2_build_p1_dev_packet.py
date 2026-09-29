#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def norm(s): return " ".join(s.strip().split())
def key(*x): return sha("|".join(map(str,x)))

def parse_m2(path):
    blocks=[]; src=None; edits=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("S "):
            if src is not None: blocks.append((src,edits))
            src=line[2:]; edits=[]
        elif line.startswith("A ") and src is not None:
            p=line[2:].split("|||"); sp=p[0].split() if p else []
            if len(p)<3 or len(sp)<2 or p[-1].strip() not in {"","0"}: continue
            try: a,b=int(sp[0]),int(sp[1])
            except ValueError: continue
            edits.append({"start":a,"end":b,"correction":p[2]})
    if src is not None: blocks.append((src,edits))
    return blocks

def apply(src,edits,idxs):
    t=src.split()
    for i in sorted(idxs,key=lambda i:(edits[i]["start"],edits[i]["end"]),reverse=True):
        e=edits[i]; repl=[] if e["correction"] in {"","-NONE-"} else e["correction"].split()
        t[e["start"]:e["end"]]=repl
    return " ".join(t)

def qalb(root,split,prefix):
    srcs=(root/split/f"{prefix}.sent.no_ids").read_text(encoding="utf-8").splitlines()
    cors=(root/split/f"{prefix}.cor.no_ids").read_text(encoding="utf-8").splitlines()
    blocks=parse_m2(root/split/f"{prefix}.m2")
    out=[]
    for i,(s0,c0) in enumerate(zip(srcs,cors),1):
        s,c=norm(s0),norm(c0)
        out.append({"case_id":f"Q-{split}-{i}-CK","source":c,"candidate":c,"gold_family":"CLEAN_REFERENCE_KEEP","source_family":"QALB"})
        if s==c: continue
        out.append({"case_id":f"Q-{split}-{i}-EK","source":s,"candidate":s,"gold_family":"ERRONEOUS_SOURCE_KEEP","source_family":"QALB"})
        out.append({"case_id":f"Q-{split}-{i}-FULL","source":s,"candidate":c,"gold_family":"FULL_EXPERT_REPAIR","source_family":"QALB"})
        if len(blocks)!=len(srcs): continue
        bs,ed=blocks[i-1]
        if norm(bs)!=s or len(ed)<2: continue
        idx=list(range(len(ed)))
        if norm(apply(s,ed,idx))!=c: continue
        one=int(key(split,i,"one")[:8],16)%len(ed)
        out.append({"case_id":f"Q-{split}-{i}-ONE","source":s,"candidate":norm(apply(s,ed,[one])),"gold_family":"ONE_OF_MANY_PARTIAL","source_family":"QALB"})
        miss=int(key(split,i,"miss")[:8],16)%len(ed)
        app=[x for x in idx if x!=miss]
        out.append({"case_id":f"Q-{split}-{i}-ABO","source":s,"candidate":norm(apply(s,ed,app)),"gold_family":"ALL_BUT_ONE_PARTIAL","source_family":"QALB"})
    return out

def zaebuc(root):
    raw=(root/"train.sent.raw").read_text(encoding="utf-8-sig").splitlines()
    cor=(root/"train.sent.cor").read_text(encoding="utf-8-sig").splitlines()
    if len(raw)!=len(cor): raise SystemExit("ZAEBUC line count mismatch")
    out=[]
    for i,(s0,c0) in enumerate(zip(raw,cor),1):
        s,c=norm(s0),norm(c0)
        out.append({"case_id":f"Z-{i}-CK","source":c,"candidate":c,"gold_family":"CLEAN_REFERENCE_KEEP","source_family":"ZAEBUC"})
        if s!=c:
            out.append({"case_id":f"Z-{i}-FULL","source":s,"candidate":c,"gold_family":"FULL_EXPERT_REPAIR","source_family":"ZAEBUC"})
    return out

SPEC=[
 (("QALB","CLEAN_REFERENCE_KEEP"),24),
 (("QALB","ERRONEOUS_SOURCE_KEEP"),24),
 (("QALB","FULL_EXPERT_REPAIR"),24),
 (("QALB","ONE_OF_MANY_PARTIAL"),12),
 (("QALB","ALL_BUT_ONE_PARTIAL"),12),
 (("ZAEBUC","CLEAN_REFERENCE_KEEP"),12),
 (("ZAEBUC","FULL_EXPERT_REPAIR"),12),
]

def select(groups,salt,exclude=None):
    exclude=exclude or set()
    picked=[]
    for g,n in SPEC:
        xs=[r for r in groups[g] if r["case_id"] not in exclude]
        xs.sort(key=lambda r:key(salt,g[0],g[1],r["case_id"]))
        if len(xs)<n: raise SystemExit(f"insufficient {g}: {len(xs)} < {n}")
        picked.extend(xs[:n])
    return picked

def emit(selected,salt,prefix,out):
    selected=sorted(selected,key=lambda r:key(salt,"shuffle",r["case_id"]))
    blind=[]; gold=[]
    for j,r in enumerate(selected,1):
        cid=f"{prefix}-{j:03d}"
        blind.append({"case_id":cid,"source":r["source"],"candidate":r["candidate"]})
        gold.append({
          "case_id":cid,
          "origin_case_id":r["case_id"],
          "gold_family":r["gold_family"],
          "source_family":r["source_family"],
          "safe_accept":r["gold_family"] in {"CLEAN_REFERENCE_KEEP","FULL_EXPERT_REPAIR","SINGLE_EDIT_COMPLETE"}
        })
    return blind,gold

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--qalb-root",required=True)
    ap.add_argument("--zaebuc-root",required=True)
    ap.add_argument("--out-dir",default=".")
    args=ap.parse_args(); out=Path(args.out_dir)

    rows=(qalb(Path(args.qalb_root),"dev","QALB-2014-L1-Dev")
          +qalb(Path(args.qalb_root),"train","QALB-2014-L1-Train")
          +zaebuc(Path(args.zaebuc_root)))
    groups={}
    for r in rows: groups.setdefault((r["source_family"],r["gold_family"]),[]).append(r)

    p0=select(groups,"M2-P0-DEV-A")
    p0_origins={r["case_id"] for r in p0}
    p1=select(groups,"M2-P1-DEV-B",exclude=p0_origins)
    p1_origins={r["case_id"] for r in p1}
    if p0_origins & p1_origins:
        raise SystemExit("P0/P1 overlap detected")

    blind,gold=emit(p1,"M2-P1-DEV-B","M2P1D",out)
    (out/"M2_P1_DEV_BLIND.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in blind)+"\n",encoding="utf-8")
    (out/"M2_P1_DEV_KEY.jsonl").write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in gold)+"\n",encoding="utf-8")
    summary={
      "cases":len(blind),
      "p0_origin_count":len(p0_origins),
      "p1_origin_count":len(p1_origins),
      "p0_p1_overlap":0,
      "salt":"M2-P1-DEV-B",
      "a7ta_reserved_used":False
    }
    (out/"M2_P1_PACKET_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
