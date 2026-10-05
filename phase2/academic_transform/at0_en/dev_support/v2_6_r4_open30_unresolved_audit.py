#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, pathlib, urllib.request, collections, re

HERE=pathlib.Path(__file__).resolve().parent
AT0=HERE.parent
V26=AT0/"v2_6"
SRC_COMMIT="482b7d8f135fe6ea424961c2812e8d214c3f4a5f"
BASE=f"https://raw.githubusercontent.com/sociocom/PICO-Corpus/{SRC_COMMIT}/pico_corpus_brat_annotated_files"
PMIDS=[
"10459028","10547391","11136837","11283119","12374678","12377957","12393819","12425756","12439707","12540501",
"12598347","12609560","12621740","12637464","12697850","12721239","12775735","12796608","12812657","12839848",
"12840087","12904519","12919237","12926095","12957243","14525573","14556922","14637388","14722733","15014181",
]

def loadmod(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
ra=loadmod("v26_ra_audit",V26/"gate_b2"/"relation_aware_extractor.py")

RULES=[
("objective",r"\b(?:aim|objective|purpose|determin|assess|evaluate|compare|investigate|examine|test)\b"),
("population",r"\b(?:patients?|participants?|women|men|children|subjects?|survivors?|volunteers?)\b"),
("randomization",r"\b(?:random|assign|allocat)\w*\b"),
("intervention",r"\b(?:receive|undergo|treat|therapy|dose|drug|placebo|surgery|radiation|chemotherapy|exercise)\w*\b"),
("outcome",r"\b(?:outcome|endpoint|end point|response|recurrence|survival|mortality|quality of life|qol)\b"),
("result_direction",r"\b(?:increase|decrease|reduce|improve|higher|lower|greater|less|difference|similar|benefit|effect)\w*\b"),
("statistics",r"\b(?:hazard ratio|odds ratio|confidence interval|p\s*[<=>]|significant|mean|median|rate|risk)\b"),
("followup",r"\b(?:follow|month|week|year|time to|duration)\w*\b"),
("safety",r"\b(?:adverse|toxicity|death|tolerat)\w*\b"),
("conclusion",r"\b(?:conclude|effective|efficacy|appears|suggest|support|justify)\w*\b"),
]

def classify(ev):
    l=ev.lower()
    cats=[name for name,pat in RULES if re.search(pat,l,re.I)]
    return cats or ["other"]

rows=[]
cat_counter=collections.Counter()
pred_counter=collections.Counter()
for pmid in PMIDS:
    with urllib.request.urlopen(f"{BASE}/{pmid}.txt",timeout=30) as resp:
        text=resp.read().decode("utf-8")
    g=ra.relation_aware_extract(text,f"AUDIT-{pmid}")
    for a in g["assertions"]:
        if a["confidence_status"]!="CERTAIN" or a["predicate"]=="UNRESOLVED":
            cats=classify(a["evidence"])
            for c in cats: cat_counter[c]+=1
            pred_counter[a["predicate"]]+=1
            rows.append({
                "pmid":pmid,
                "predicate":a["predicate"],
                "confidence":a["confidence_status"],
                "criticality":a["criticality"],
                "categories":cats,
                "evidence":a["evidence"],
            })

rows_sorted=sorted(rows,key=lambda x:(x["categories"][0],x["pmid"],x["evidence"]))
summary={
    "audit_id":"AT0_EN_V26_R4_OPEN30_UNRESOLVED_AUDIT_V1",
    "source_commit":SRC_COMMIT,
    "documents":len(PMIDS),
    "factpico_used":False,
    "holdout_opened":False,
    "unresolved_or_noncertain_count":len(rows),
    "category_counts":dict(cat_counter.most_common()),
    "predicate_counts":dict(pred_counter.most_common()),
    "examples":rows_sorted[:160],
}
print(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2))
