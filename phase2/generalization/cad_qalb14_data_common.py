"""Frozen QALB14 external example construction for CAD feasibility."""
from __future__ import annotations
import hashlib
from difflib import SequenceMatcher

ALIF=set("ا أ إ آ ٱ".split())
YA={"ي","ى"}
TA={"ه","ة"}
WINDOW_RADIUS=12

def sha(s:str)->str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def target_window(words,target_i):
    lo=max(0,target_i-WINDOW_RADIUS)
    hi=min(len(words),target_i+WINDOW_RADIUS+1)
    return " ".join(words[lo:hi])

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
    last=len(src)-1;orth=[];other=[]
    for i,(a,b) in enumerate(zip(src,gold)):
        if a==b:continue
        (orth if ortho_pair(a,b,i,last) else other).append(i)
    if not orth or not other:return None
    chars=list(src)
    for i in orth:chars[i]=gold[i]
    cand="".join(chars)
    return None if cand in {src,gold} else cand

def locus(op):
    _,i1,i2,_,_=op
    return (i1,i1) if i1==i2 else (i1,i2-1)

def nearby(target_i,op,radius=2):
    a,b=locus(op)
    return not (b<target_i-radius or a>target_i+radius)

def examples_for_split(src_path,gold_path,split):
    s_lines=[x.strip() for x in src_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    g_lines=[x.strip() for x in gold_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(s_lines)==len(g_lines)>0
    out=[]
    for line_no,(sl,gl) in enumerate(zip(s_lines,g_lines),1):
        src=sl.split();gold=gl.split()
        ops=[x for x in SequenceMatcher(a=src,b=gold,autojunk=False).get_opcodes() if x[0]!="equal"]
        for oi,op in enumerate(ops):
            tag,i1,i2,j1,j2=op
            if tag!="replace" or i2-i1!=1 or j2-j1!=1:continue
            s,g=src[i1],gold[j1]
            other=[x for k,x in enumerate(ops) if k!=oi]
            near=any(nearby(i1,x,2) for x in other)
            if ortho_only(s,g):
                cls="NEG_NEARBY_RESIDUAL" if near else "POS_ISOLATED_ORTHO"
                cand=list(src);cand[i1]=g
                eid=sha(f"{split}|{line_no}|{i1}|{cls}|{sha(s)}|{sha(g)}")
                out.append({
                    "id":eid,"class":cls,"label":0 if near else 1,
                    "source":target_window(src,i1),"candidate":target_window(cand,i1)
                })
            sub=ortho_subedit(s,g)
            if sub is not None:
                cand=list(src);cand[i1]=sub
                cls="NEG_ORTHO_SUBEDIT"
                eid=sha(f"{split}|{line_no}|{i1}|{cls}|{sha(s)}|{sha(g)}|{sha(sub)}")
                out.append({
                    "id":eid,"class":cls,"label":0,
                    "source":target_window(src,i1),"candidate":target_window(cand,i1)
                })
    return out

def select_train(rows):
    pos=sorted([x for x in rows if x["class"]=="POS_ISOLATED_ORTHO"],key=lambda x:x["id"])[:4000]
    sub=sorted([x for x in rows if x["class"]=="NEG_ORTHO_SUBEDIT"],key=lambda x:x["id"])[:2000]
    need=4000-len(sub)
    near=sorted([x for x in rows if x["class"]=="NEG_NEARBY_RESIDUAL"],key=lambda x:x["id"])[:need]
    neg=sub+near
    assert len(pos)==4000 and len(neg)==4000,(len(pos),len(neg))
    return pos+neg

def select_dev(rows):
    pos=sorted([x for x in rows if x["class"]=="POS_ISOLATED_ORTHO"],key=lambda x:x["id"])
    sub=sorted([x for x in rows if x["class"]=="NEG_ORTHO_SUBEDIT"],key=lambda x:x["id"])
    need=len(pos)-len(sub)
    near=sorted([x for x in rows if x["class"]=="NEG_NEARBY_RESIDUAL"],key=lambda x:x["id"])[:need]
    neg=sub+near
    assert len(pos)==1209 and len(neg)==1209,(len(pos),len(neg))
    return pos+neg

def rows_hash(rows):
    return sha("\n".join(sorted(x["id"] for x in rows)))
