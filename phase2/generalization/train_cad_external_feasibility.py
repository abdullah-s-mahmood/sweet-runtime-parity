"""Train/calibrate frozen-encoder CAD feasibility classifier on QALB14 only."""
from __future__ import annotations
import hashlib,json,math
from difflib import SequenceMatcher
from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

from phase2.generalization.cad_feasibility_common import (
    MODEL_ID,MODEL_REVISION,target_window,load_encoder,pair_feature_matrix
)

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"upstream/arabic-gec/data/gec/QALB-0.9.1-Dec03-2021-SharedTasks/data/2014"
TRAIN_SRC=BASE/"train/QALB-2014-L1-Train.sent.no_ids"
TRAIN_GOLD=BASE/"train/QALB-2014-L1-Train.cor.no_ids"
DEV_SRC=BASE/"dev/QALB-2014-L1-Dev.sent.no_ids"
DEV_GOLD=BASE/"dev/QALB-2014-L1-Dev.cor.no_ids"
OUT=ROOT/"PHASE2_CAD_EXTERNAL_TRAINING_SUMMARY.json"
MODEL_OUT=ROOT/"CAD_FEASIBILITY_MODEL.joblib"

ALIF=set("ا أ إ آ ٱ".split());YA={"ي","ى"};TA={"ه","ة"}

def sha(s):return hashlib.sha256(s.encode("utf-8")).hexdigest()
def file_sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

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
    assert len(pos)==4000 and len(neg)==4000,(len(pos),len(neg),len(sub),len(near))
    return pos+neg

def select_dev(rows):
    pos=sorted([x for x in rows if x["class"]=="POS_ISOLATED_ORTHO"],key=lambda x:x["id"])
    sub=sorted([x for x in rows if x["class"]=="NEG_ORTHO_SUBEDIT"],key=lambda x:x["id"])
    need=len(pos)-len(sub)
    near=sorted([x for x in rows if x["class"]=="NEG_NEARBY_RESIDUAL"],key=lambda x:x["id"])[:need]
    neg=sub+near
    assert len(pos)==1209 and len(neg)==1209,(len(pos),len(neg),len(sub),len(near))
    return pos+neg

def rows_hash(rows):
    return sha("\n".join(sorted(x["id"] for x in rows)))

def main():
    train_all=examples_for_split(TRAIN_SRC,TRAIN_GOLD,"train")
    dev_all=examples_for_split(DEV_SRC,DEV_GOLD,"dev")
    tr=select_train(train_all);dv=select_dev(dev_all)

    tok,enc=load_encoder()
    Xtr=pair_feature_matrix([(x["source"],x["candidate"]) for x in tr],tok,enc)
    ytr=np.array([x["label"] for x in tr],dtype=np.int64)
    Xdv=pair_feature_matrix([(x["source"],x["candidate"]) for x in dv],tok,enc)
    ydv=np.array([x["label"] for x in dv],dtype=np.int64)

    pipe=Pipeline([
      ("scale",StandardScaler()),
      ("clf",LogisticRegression(C=1.0,class_weight="balanced",random_state=0,max_iter=2000,solver="lbfgs"))
    ])
    pipe.fit(Xtr,ytr)
    probs=pipe.predict_proba(Xdv)[:,1]
    neg_probs=probs[ydv==0]
    max_neg=float(np.max(neg_probs))
    threshold=float(np.nextafter(np.float64(max_neg),np.float64(2.0)))
    pred=probs>=threshold
    neg_false=int(np.sum(pred & (ydv==0)))
    pos_pass=int(np.sum(pred & (ydv==1)))
    pos_total=int(np.sum(ydv==1))
    feasible=neg_false==0 and pos_pass>=300 and pos_pass/pos_total>=0.25
    auc=float(roc_auc_score(ydv,probs))

    payload={
      "pipeline":pipe,
      "threshold":threshold,
      "encoder_model_id":MODEL_ID,
      "encoder_revision":MODEL_REVISION,
      "feature_dim":int(Xtr.shape[1]),
      "rule_version":"CAD_QALB14_LOCAL_COMPLETENESS_V1",
    }
    joblib.dump(payload,MODEL_OUT,compress=3)

    summary={
      "status":"PHASE2_CAD_EXTERNAL_MODEL_TRAINED",
      "training_source":"QALB14_EXTERNAL_ONLY",
      "current_phase_labels_read":False,
      "qalb15_corrected_read":False,
      "qalb15_test_read":False,
      "qalb_text_persisted":False,
      "encoder_model_id":MODEL_ID,
      "encoder_revision":MODEL_REVISION,
      "training_examples":len(tr),
      "training_positive":int(np.sum(ytr==1)),
      "training_negative":int(np.sum(ytr==0)),
      "dev_examples":len(dv),
      "dev_positive":pos_total,
      "dev_negative":int(np.sum(ydv==0)),
      "train_selection_ids_sha256":rows_hash(tr),
      "dev_selection_ids_sha256":rows_hash(dv),
      "feature_dim":int(Xtr.shape[1]),
      "dev_auc":auc,
      "max_dev_negative_probability":max_neg,
      "acceptance_threshold":threshold,
      "dev_negative_false_accepts":neg_false,
      "dev_positive_pass":pos_pass,
      "dev_positive_retention":pos_pass/pos_total,
      "external_feasibility_criterion_met":feasible,
      "model_sha256":file_sha(MODEL_OUT),
      "next_action":"SCORE_CONSUMED_QALB15" if feasible else "STOP_EXTERNAL_CAD_FEASIBILITY_FAILED",
    }
    OUT.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=c<="\u06ff" for c in dumped)
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":main()
