#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,difflib
from pathlib import Path

TARGETS=[
 ("M2P1D-015",19380,"ABO"),
 ("M2P1D-025",5380,"ABO"),
 ("M2P1D-041",16992,"ABO"),
 ("M2P1D-047",8273,"ABO"),
 ("M2P1D-054",10335,"ABO"),
 ("M2P1D-072",2533,"ABO"),
 ("M2P1D-103",15352,"ABO"),
 ("M2P1D-113",865,"ABO"),
 ("M2P1D-117",11570,"ONE"),
]
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def key(*x): return sha("|".join(map(str,x)))
def norm(s): return " ".join(s.strip().split())
def parse_m2(path):
    blocks=[]; src=None; edits=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("S "):
            if src is not None: blocks.append((src,edits))
            src=line[2:]; edits=[]
        elif line.startswith("A ") and src is not None:
            p=line[2:].split("|||"); sp=p[0].split() if p else []
            if len(p)<3 or len(sp)<2 or p[-1].strip() not in {"","0"}: continue
            try:a,b=int(sp[0]),int(sp[1])
            except:continue
            edits.append({"start":a,"end":b,"correction":p[2],"type":p[1]})
    if src is not None: blocks.append((src,edits))
    return blocks
def apply(src,edits,idxs):
    t=src.split()
    for i in sorted(idxs,key=lambda i:(edits[i]["start"],edits[i]["end"]),reverse=True):
        e=edits[i]; repl=[] if e["correction"] in {"","-NONE-"} else e["correction"].split()
        t[e["start"]:e["end"]]=repl
    return " ".join(t)

root=Path("upstream/qalb14/train")
prefix="QALB-2014-L1-Train"
srcs=(root/f"{prefix}.sent.no_ids").read_text(encoding="utf-8").splitlines()
cors=(root/f"{prefix}.cor.no_ids").read_text(encoding="utf-8").splitlines()
blocks=parse_m2(root/f"{prefix}.m2")
out=[]
for cid,line_no,kind in TARGETS:
    i=line_no-1
    src=norm(srcs[i]); ref=norm(cors[i]); bsrc,ed=blocks[i]
    assert norm(bsrc)==src
    idx=list(range(len(ed)))
    assert norm(apply(src,ed,idx))==ref
    if kind=="ABO":
        miss=int(key("train",line_no,"miss")[:8],16)%len(ed)
        applied=[x for x in idx if x!=miss]; withheld=[miss]
    else:
        one=int(key("train",line_no,"one")[:8],16)%len(ed)
        applied=[one]; withheld=[x for x in idx if x!=one]
    cand=norm(apply(src,ed,applied))
    sm=difflib.SequenceMatcher(a=cand.split(),b=ref.split())
    diffs=[]
    for tag,a0,a1,b0,b1 in sm.get_opcodes():
        if tag!="equal":
            diffs.append({"op":tag,"candidate":" ".join(cand.split()[a0:a1]),"reference":" ".join(ref.split()[b0:b1])})
    out.append({
      "case_id":cid,"line_no":line_no,"construction":kind,
      "withheld_edit_indices":withheld,
      "withheld_edit_types":[ed[x]["type"] for x in withheld],
      "withheld_edits":[ed[x] for x in withheld],
      "candidate":cand,"reference":ref,"diffs":diffs
    })
Path("M2_P1_UNSAFE_ACCEPT_AUDIT.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"cases":len(out),"all_reconstructed":True},indent=2))
