#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, random
from collections import defaultdict
from pathlib import Path

CLASSES=("P","I","C","O")
THRESHOLDS=(0.80,0.85,0.90,0.95)

def _ident(x):
    return (str(x["document_id"]),int(x["start"]),int(x["end"]),str(x["class"]))

def validate_gold(gold, expected_docs):
    seen=set()
    for x in gold:
        d,s,e,c=_ident(x)
        if d not in expected_docs: raise ValueError("gold unknown document")
        if c not in CLASSES: raise ValueError("gold invalid class")
        if s<0 or e<=s: raise ValueError("gold invalid coordinate")
        k=(d,s,e,c)
        if k in seen: raise ValueError("duplicate gold")
        seen.add(k)
    return seen

def validate_predictions(preds, expected_docs):
    seen=set()
    for x in preds:
        d,s,e,c=_ident(x)
        if d not in expected_docs: raise ValueError("prediction unknown document")
        if c not in CLASSES: raise ValueError("prediction invalid class")
        if s<0 or e<=s: raise ValueError("prediction invalid coordinate")
        score=float(x.get("score",1.0))
        if not math.isfinite(score): raise ValueError("nonfinite score")
        k=(d,s,e,c)
        if k in seen: raise ValueError("duplicate prediction")
        seen.add(k)
    return seen

def exact_metrics(gold, preds, expected_docs):
    expected_docs=set(expected_docs)
    if not expected_docs: raise ValueError("empty expected document universe")
    g=validate_gold(gold,expected_docs)
    p=validate_predictions(preds,expected_docs)
    by_class={}
    TP=FP=FN=0
    for c in CLASSES:
        gc={x for x in g if x[3]==c}
        pc={x for x in p if x[3]==c}
        tp=len(gc&pc); fp=len(pc-gc); fn=len(gc-pc)
        pr=tp/(tp+fp) if tp+fp else 0.0
        rc=tp/(tp+fn) if tp+fn else 0.0
        f1=2*pr*rc/(pr+rc) if pr+rc else 0.0
        by_class[c]={"tp":tp,"fp":fp,"fn":fn,"precision":pr,"recall":rc,"f1":f1}
        TP+=tp; FP+=fp; FN+=fn
    pr=TP/(TP+FP) if TP+FP else 0.0
    rc=TP/(TP+FN) if TP+FN else 0.0
    f1=2*pr*rc/(pr+rc) if pr+rc else 0.0
    return {
      "micro":{"tp":TP,"fp":FP,"fn":FN,"precision":pr,"recall":rc,"f1":f1},
      "macro_f1":sum(by_class[c]["f1"] for c in CLASSES)/len(CLASSES),
      "per_class":by_class,
      "document_count":len(expected_docs)
    }

def select_threshold(gold,preds,expected_docs,family_of_doc):
    results={}
    for t in THRESHOLDS:
        q=[x for x in preds if float(x["score"])>=t]
        m=exact_metrics(gold,q,expected_docs)
        ok=True
        support={}
        for c in CLASSES:
            accepted=[x for x in q if x["class"]==c]
            fams={family_of_doc[str(x["document_id"])] for x in accepted}
            support[c]={"accepted":len(accepted),"families":len(fams)}
            pc=m["per_class"][c]
            if pc["precision"]<0.90 or pc["recall"]<0.33 or len(accepted)<30 or len(fams)<20:
                ok=False
        results[str(t)]={"metrics":m,"support":support,"passes":ok}
    passing=[t for t in THRESHOLDS if results[str(t)]["passes"]]
    if not passing:
        return {"decision":"NO_HIGH_PRECISION_MODE_NOMINATED","selected":None,"thresholds":results}
    # mean class-macro recall == average per-class recall
    ranked=[]
    for t in passing:
        rec=sum(results[str(t)]["metrics"]["per_class"][c]["recall"] for c in CLASSES)/4
        ranked.append((rec,t))
    ranked.sort(key=lambda z:(z[0],z[1]),reverse=True)
    return {"decision":"HIGH_PRECISION_MODE_NOMINATED","selected":ranked[0][1],"thresholds":results}

def cluster_bootstrap_difference(rows_a,rows_b,family_key="family_id",seed=4404,reps=200):
    # synthetic mechanics helper: rows are family-level (tp,fp,fn) records paired by family.
    a={str(x[family_key]):x for x in rows_a}
    b={str(x[family_key]):x for x in rows_b}
    fams=sorted(set(a)&set(b))
    if not fams: raise ValueError("no paired families")
    rng=random.Random(seed)
    diffs=[]
    def f1(rows):
        tp=sum(int(x["tp"]) for x in rows); fp=sum(int(x["fp"]) for x in rows); fn=sum(int(x["fn"]) for x in rows)
        return 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0
    for _ in range(reps):
        draw=[fams[rng.randrange(len(fams))] for __ in range(len(fams))]
        diffs.append(f1([a[x] for x in draw])-f1([b[x] for x in draw]))
    return diffs

def synthetic_preflight():
    docs={"d1","d2","d3"}
    gold=[
      {"document_id":"d1","start":0,"end":2,"class":"P"},
      {"document_id":"d1","start":5,"end":7,"class":"I"},
      {"document_id":"d1","start":10,"end":12,"class":"I"}, # same surface could occur elsewhere; coords distinguish
      {"document_id":"d2","start":1,"end":3,"class":"C"},
      {"document_id":"d2","start":8,"end":11,"class":"O"},
    ]
    pred=[
      {"document_id":"d1","start":0,"end":2,"class":"P","score":.99}, # TP
      {"document_id":"d1","start":5,"end":7,"class":"C","score":.99}, # wrong type => C FP + I FN
      {"document_id":"d1","start":10,"end":12,"class":"I","score":.90}, # TP
      {"document_id":"d2","start":1,"end":4,"class":"C","score":.95}, # boundary error => FP+FN
      {"document_id":"d2","start":8,"end":11,"class":"O","score":.97}, # TP
    ]
    m=exact_metrics(gold,pred,docs)
    if m["micro"]!={"tp":3,"fp":2,"fn":2,"precision":0.6,"recall":0.6,"f1":0.6}:
        raise RuntimeError(m["micro"])
    # Both-empty document d3 contributes zero TP.
    if m["micro"]["tp"]!=3: raise RuntimeError("empty document inflated TP")

    # Guards
    def must_fail(xs,why):
        try:
            exact_metrics(gold,xs,docs)
        except ValueError:
            return
        raise RuntimeError(f"guard failed: {why}")
    must_fail(pred+[dict(pred[0])],"duplicate")
    bad=[dict(x) for x in pred]; bad[0]["score"]=float("nan"); must_fail(bad,"nonfinite")
    bad=[dict(x) for x in pred]; bad[0]["end"]=bad[0]["start"]; must_fail(bad,"coords")
    bad=[dict(x) for x in pred]; bad[0]["document_id"]="missing"; must_fail(bad,"unknown doc")

    # High-precision grid mechanics on synthetic support-rich data.
    hp_gold=[]; hp_pred=[]; fam={}
    for ci,c in enumerate(CLASSES):
        for i in range(40):
            d=f"{c}{i:02d}"; fam[d]=f"F{c}{i:02d}"
            hp_gold.append({"document_id":d,"start":0,"end":1,"class":c})
            # 36 TP at .96, 4 FN; plus 2 high-score FP => precision 36/38=.947, recall .90
            if i<36:
                hp_pred.append({"document_id":d,"start":0,"end":1,"class":c,"score":.96})
        for j in range(2):
            d=f"{c}FP{j}"; fam[d]=f"F{c}FP{j}"
            hp_pred.append({"document_id":d,"start":2,"end":3,"class":c,"score":.96})
    hp_docs=set(fam)
    hp=select_threshold(hp_gold,hp_pred,hp_docs,fam)
    if hp["decision"]!="HIGH_PRECISION_MODE_NOMINATED" or hp["selected"]!=0.95:
        raise RuntimeError("threshold selection fixture failed")

    # No-pass fixture by flooding FPs.
    badpred=list(hp_pred)
    for c in CLASSES:
        for j in range(20):
            d=f"{c}BAD{j}"; fam[d]=f"FB{c}{j}"
            hp_docs.add(d)
            badpred.append({"document_id":d,"start":3,"end":4,"class":c,"score":.99})
    no=select_threshold(hp_gold,badpred,hp_docs,fam)
    if no["decision"]!="NO_HIGH_PRECISION_MODE_NOMINATED":
        raise RuntimeError("no-pass threshold fixture failed")

    # Paired cluster bootstrap determinism.
    A=[{"family_id":f"F{i}","tp":8,"fp":1,"fn":1} for i in range(20)]
    B=[{"family_id":f"F{i}","tp":7,"fp":2,"fn":2} for i in range(20)]
    x=cluster_bootstrap_difference(A,B,reps=200)
    y=cluster_bootstrap_difference(A,B,reps=200)
    if x!=y or not all(v>0 for v in x):
        raise RuntimeError("bootstrap fixture failed")

    return {
      "state":"FEDERATION_STRICT_SCORER_SYNTHETIC_PREFLIGHT_PASS",
      "scientific_data_used":False,
      "benchmark_gold_used":False,
      "exact_fixture":m,
      "both_empty_tp_policy":"ZERO",
      "repeated_surface_policy":"COORDINATE_OCCURRENCE_DISTINCT",
      "wrong_type_policy":"FP_PLUS_FN",
      "boundary_error_policy":"FP_PLUS_FN",
      "guards":{"duplicate":True,"nonfinite":True,"invalid_coordinate":True,"unknown_document":True},
      "high_precision_pass_fixture_selected":hp["selected"],
      "high_precision_no_pass_fixture":no["decision"],
      "bootstrap_seed":4404,
      "bootstrap_deterministic":True
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--synthetic-preflight",action="store_true")
    ap.add_argument("--out",type=Path)
    a=ap.parse_args()
    if not a.synthetic_preflight:
        raise SystemExit("Only synthetic preflight authorized")
    d=synthetic_preflight()
    s=json.dumps(d,indent=2,sort_keys=True)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(s,encoding="utf-8")
    print(s,end="")
if __name__=="__main__":
    main()
