#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,urllib.request
from collections import Counter
from pathlib import Path

REV="8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"
BASE=f"https://raw.githubusercontent.com/CAMeL-Lab/arabic-gec/{REV}/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2014"
AR=re.compile(r"[\u0600-\u06ff]")

def norm(s):return " ".join(s.strip().split())
def download(split,prefix,suf,out):
    u=f"{BASE}/{split}/{prefix}.{suf}"
    urllib.request.urlretrieve(u,out)
    if out.stat().st_size<20:raise RuntimeError(u)
def parse_m2(path):
    blocks=[];src=None;ed=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("S "):
            if src is not None:blocks.append((src,ed))
            src=line[2:];ed=[]
        elif line.startswith("A ") and src is not None:
            p=line[2:].split("|||");sp=p[0].split() if p else []
            if len(p)<3 or len(sp)<2 or p[-1].strip() not in {"","0"}:continue
            try:a,b=int(sp[0]),int(sp[1])
            except:continue
            ed.append({"start":a,"end":b,"type":p[1],"replacement":p[2]})
    if src is not None:blocks.append((src,ed))
    return blocks
def apply(src,edits,skip=None):
    t=src.split()
    for i,e in sorted(enumerate(edits),key=lambda z:(z[1]["start"],z[1]["end"]),reverse=True):
        if i==skip:continue
        rr=[] if e["replacement"] in {"","-NONE-"} else e["replacement"].split()
        t[e["start"]:e["end"]]=rr
    return norm(" ".join(t))
def surface(src,e):
    toks=src.split();return norm(" ".join(toks[e["start"]:e["end"]]))
def detectable(src,e):
    s=surface(src,e)
    return bool(s and AR.search(s))
def strict(src,e):
    s=surface(src,e);r=norm(e["replacement"])
    return e["end"]-e["start"]==1 and bool(s) and bool(r) and " " not in s and " " not in r and bool(AR.search(s)) and bool(AR.search(r)) and s!=r

work=Path("upstream/qalb14v2");work.mkdir(parents=True,exist_ok=True)
tot=Counter();types=Counter()
for split,prefix in [("train","QALB-2014-L1-Train"),("dev","QALB-2014-L1-Dev")]:
    d=work/split;d.mkdir(exist_ok=True)
    for suf in ["sent.no_ids","cor.no_ids","m2"]:download(split,prefix,suf,d/f"{prefix}.{suf}")
    srcs=(d/f"{prefix}.sent.no_ids").read_text(encoding="utf-8").splitlines()
    cors=(d/f"{prefix}.cor.no_ids").read_text(encoding="utf-8").splitlines()
    blocks=parse_m2(d/f"{prefix}.m2")
    tot[f"{split}_source_lines"]=len(srcs);tot[f"{split}_corrected_lines"]=len(cors);tot[f"{split}_m2_blocks"]=len(blocks)
    if not(len(srcs)==len(cors)==len(blocks)):continue
    for s0,c0,(bs,ed) in zip(srcs,cors,blocks):
        s=norm(s0);c=norm(c0)
        if norm(bs)!=s:continue
        if apply(s,ed)!=c:
            tot["reconstruction_fail"]+=1;continue
        tot["reconstructable_lines"]+=1
        det=[e for e in ed if detectable(s,e)]
        st=[e for e in ed if strict(s,e)]
        tot["detectable_edit_instances"]+=len(det)
        tot["strict_single_token_edit_instances"]+=len(st)
        if det:tot["lines_with_detectable_edits"]+=1
        if st:tot["lines_with_strict_edit"]+=1
        if len(ed)>=2 and st:
            tot["all_but_one_strict_pool"]+=1
        for e in ed:types[e["type"]]+=1

criteria={
 "line_counts_match":tot["train_source_lines"]==tot["train_corrected_lines"]==tot["train_m2_blocks"] and tot["dev_source_lines"]==tot["dev_corrected_lines"]==tot["dev_m2_blocks"],
 "reconstructable_lines_ge_15000":tot["reconstructable_lines"]>=15000,
 "detectable_edits_ge_10000":tot["detectable_edit_instances"]>=10000,
 "lines_with_detectable_ge_5000":tot["lines_with_detectable_edits"]>=5000,
 "strict_edit_instances_ge_1000":tot["strict_single_token_edit_instances"]>=1000,
 "all_but_one_strict_pool_ge_500":tot["all_but_one_strict_pool"]>=500,
 "no_test_or_qalb15_read":True
}
summary={
 "status":"M2R_V2_DATA_READY" if all(criteria.values()) else "M2R_V2_DATA_NOT_READY",
 "date":"2026-09-30","revision":REV,"counts":dict(tot),
 "m2_type_top20":types.most_common(20),"criteria":criteria,
 "data_ready":all(criteria.values()),"raw_text_persisted":False,
 "qalb14_test_read":False,"qalb15_read":False
}
Path("M2R_V2_DATA_FEASIBILITY_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
if not summary["data_ready"]:raise SystemExit(2)
