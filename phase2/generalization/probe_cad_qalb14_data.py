"""QALB14 CAD-inspired local-completeness data feasibility probe.

External-data only. Persists counts/hashes, never Arabic text.
"""
from __future__ import annotations
import hashlib,json
from difflib import SequenceMatcher
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"upstream/arabic-gec/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2014"
SPLITS={
 "train":(
   BASE/"train/QALB-2014-L1-Train.sent.no_ids",
   BASE/"train/QALB-2014-L1-Train.cor.no_ids",
 ),
 "dev":(
   BASE/"dev/QALB-2014-L1-Dev.sent.no_ids",
   BASE/"dev/QALB-2014-L1-Dev.cor.no_ids",
 ),
}
OUT=ROOT/"PHASE2_CAD_DATA_FEASIBILITY.json"

ALIF=set("ا أ إ آ ٱ".split())
YA={"ي","ى"}
TA={"ه","ة"}

def file_sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def ortho_pair(a,b,pos,last):
    if a==b:return False
    if a in ALIF and b in ALIF:return True
    if pos==last and a in YA and b in YA:return True
    if pos==last and a in TA and b in TA:return True
    return False

def ortho_only(src,gold):
    if len(src)!=len(gold) or src==gold:return False
    diffs=[i for i,(a,b) in enumerate(zip(src,gold)) if a!=b]
    if not diffs:return False
    last=len(src)-1
    return all(ortho_pair(src[i],gold[i],i,last) for i in diffs)

def ortho_subedit(src,gold):
    if len(src)!=len(gold) or src==gold:return None
    last=len(src)-1
    orth=[];other=[]
    for i,(a,b) in enumerate(zip(src,gold)):
        if a==b:continue
        (orth if ortho_pair(a,b,i,last) else other).append(i)
    if not orth or not other:return None
    chars=list(src)
    for i in orth:chars[i]=gold[i]
    cand="".join(chars)
    if cand in {src,gold}:return None
    return cand

def locus(op):
    tag,i1,i2,j1,j2=op
    if i1==i2:return (i1,i1)
    return (i1,i2-1)

def nearby(target_i,op,radius=2):
    a,b=locus(op)
    return not (b < target_i-radius or a > target_i+radius)

def derive(src_line,gold_line,line_no,split):
    src=src_line.split();gold=gold_line.split()
    sm=SequenceMatcher(a=src,b=gold,autojunk=False)
    ops=[x for x in sm.get_opcodes() if x[0]!="equal"]
    out=[]
    for oi,op in enumerate(ops):
        tag,i1,i2,j1,j2=op
        if tag!="replace" or (i2-i1)!=1 or (j2-j1)!=1:continue
        s,g=src[i1],gold[j1]
        other=[x for k,x in enumerate(ops) if k!=oi]
        near=any(nearby(i1,x,2) for x in other)
        if ortho_only(s,g):
            cls="NEG_NEARBY_RESIDUAL" if near else "POS_ISOLATED_ORTHO"
            out.append((cls,sha(f"{split}|{line_no}|{i1}|{cls}|{sha(s)}|{sha(g)}")))
        sub=ortho_subedit(s,g)
        if sub is not None:
            out.append(("NEG_ORTHO_SUBEDIT",sha(f"{split}|{line_no}|{i1}|NEG_ORTHO_SUBEDIT|{sha(s)}|{sha(g)}|{sha(sub)}")))
    return out

def main():
    result={
      "status":"PHASE2_CAD_DATA_FEASIBILITY_FROZEN",
      "rule_version":"CAD_QALB14_LOCAL_COMPLETENESS_V1",
      "splits":{},
      "current_phase_labels_read":False,
      "qalb15_corrected_read":False,
      "qalb15_test_read":False,
      "qalb_text_persisted":False,
    }
    all_ids=[]
    for split,(sp,gp) in SPLITS.items():
        s_lines=[x.strip() for x in sp.read_text(encoding="utf-8").splitlines() if x.strip()]
        g_lines=[x.strip() for x in gp.read_text(encoding="utf-8").splitlines() if x.strip()]
        assert len(s_lines)==len(g_lines) and len(s_lines)>0,(split,len(s_lines),len(g_lines))
        counts={"POS_ISOLATED_ORTHO":0,"NEG_NEARBY_RESIDUAL":0,"NEG_ORTHO_SUBEDIT":0}
        ids=[]
        for n,(s,g) in enumerate(zip(s_lines,g_lines),1):
            for cls,eid in derive(s,g,n,split):
                counts[cls]+=1;ids.append(eid)
        ids=sorted(ids);all_ids.extend(ids)
        result["splits"][split]={
          "lines":len(s_lines),
          "counts":counts,
          "positive":counts["POS_ISOLATED_ORTHO"],
          "negative":counts["NEG_NEARBY_RESIDUAL"]+counts["NEG_ORTHO_SUBEDIT"],
          "source_sha256":file_sha(sp),
          "gold_sha256":file_sha(gp),
          "example_ids_sha256":sha("\n".join(ids)),
        }
    tr=result["splits"]["train"];dv=result["splits"]["dev"]
    feasible=tr["positive"]>=500 and tr["negative"]>=500 and dv["positive"]>=50 and dv["negative"]>=50
    result["pre_registered_feasibility_criterion_met"]=feasible
    result["next_action"]="TRAIN_EXTERNAL_CAD_FEASIBILITY_MODEL" if feasible else "STOP_CAD_DATA_INSUFFICIENT"
    result["all_example_ids_sha256"]=sha("\n".join(sorted(all_ids)))
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in dumped)
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":main()
