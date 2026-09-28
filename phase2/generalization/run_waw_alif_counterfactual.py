"""Counterfactual WAW-ALIF verifier challenge.

Authored project cases only; not a generalization benchmark.
Tests safety behavior of the morphosyntactic acceptance rule independent of
candidate-generator coverage.
"""
from __future__ import annotations
import json,re,unicodedata
from pathlib import Path
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

ROOT=Path(__file__).resolve().parents[2]
CASES=ROOT/"phase2/generalization/WAW_ALIF_COUNTERFACTUAL_CHALLENGE.jsonl"
OUT=ROOT/"PHASE2_WAW_ALIF_COUNTERFACTUAL_RESULTS.json"
NOMINAL_POS={"noun","noun_prop","noun_num","noun_quant","adj","adj_comp","adj_num"}

def jl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def norm(s):
    return "".join(ch for ch in s if unicodedata.category(ch)!="Mn" and unicodedata.category(ch)[0] not in {"P","S"})

def top_analysis(dw):
    if not dw or not dw.analyses:return None
    return dw.analyses[0].analysis

def lexical_flags(analyzer,token):
    ans=analyzer.analyze(token)
    return {
        "analysis_count":len(ans),
        "has_plural_verb":any(a.get("pos")=="verb" and a.get("num")=="p" for a in ans),
        "has_singular_verb":any(a.get("pos")=="verb" and a.get("num")=="s" for a in ans),
        "has_nominal":any(a.get("pos") in NOMINAL_POS for a in ans),
        "pos_set":sorted({str(a.get("pos")) for a in ans}),
        "verb_num_set":sorted({str(a.get("num")) for a in ans if a.get("pos")=="verb"}),
    }

def licensed(a):
    if not a:return False
    if a.get("pos")!="verb" or a.get("num")!="p":return False
    if a.get("source") in {"backoff","foreign","digit","punct"}:return False
    return a.get("asp") in {"p","c"} or (a.get("asp")=="i" and a.get("mod") in {"s","j"})

def safe(a):
    if not a:return None
    return {k:a.get(k) for k in ("pos","num","per","asp","mod","source","form_num","form_gen")}

def main():
    cases=jl(CASES)
    dis=BERTUnfactoredDisambiguator.pretrained()
    analyzer=Analyzer(MorphologyDB.builtin_db("calima-msa-r13","a"),"NONE")
    rows=[]
    for c in cases:
        sw=c["source"].split(); cw=c["candidate"].split()
        assert len(sw)==len(cw),(c["id"],sw,cw)
        dif=[i for i,(a,b) in enumerate(zip(sw,cw)) if norm(a)!=norm(b)]
        assert len(dif)==1,(c["id"],dif)
        i=dif[0]; s=norm(sw[i]); o=norm(cw[i])
        shape=s.endswith("و") and not s.endswith("وا") and o==s+"ا"
        sd=dis.disambiguate(sw); cd=dis.disambiguate(cw)
        st=top_analysis(sd[i]); ct=top_analysis(cd[i])
        sf=lexical_flags(analyzer,s); cf=lexical_flags(analyzer,o)
        cand_ok=shape and licensed(ct) and cf["has_plural_verb"]
        strict=cand_ok and sf["has_plural_verb"] and not sf["has_singular_verb"] and not sf["has_nominal"]
        recovery=cand_ok and not sf["has_singular_verb"] and not sf["has_nominal"]
        rows.append({
            "id":c["id"],"expected":c["expected"],"family":c["family"],
            "source_token":s,"candidate_token":o,
            "source_top":safe(st),"candidate_top":safe(ct),
            "source_flags":sf,"candidate_flags":cf,
            "decisions":{
                "WAW_ALIF_MORPH_STRICT":"ACCEPT" if strict else "REVIEW",
                "WAW_ALIF_MORPH_RECOVERY":"ACCEPT" if recovery else "REVIEW",
            }
        })
    negatives=[x for x in rows if x["expected"]=="MUST_NOT_ACCEPT"]
    unamb=[x for x in rows if x["expected"]=="SAFE_POSITIVE_UNAMBIGUOUS"]
    amb=[x for x in rows if x["expected"]=="POSITIVE_BUT_LOCALLY_AMBIGUOUS"]
    def stats(policy):
        return {
            "negative_false_accepts":sum(x["decisions"][policy]=="ACCEPT" for x in negatives),
            "negative_total":len(negatives),
            "unambiguous_positive_accepts":sum(x["decisions"][policy]=="ACCEPT" for x in unamb),
            "unambiguous_positive_total":len(unamb),
            "ambiguous_positive_accepts":sum(x["decisions"][policy]=="ACCEPT" for x in amb),
            "ambiguous_positive_total":len(amb),
        }
    result={
        "status":"WAW_ALIF_COUNTERFACTUAL_VERIFIER_COMPLETE",
        "authored_challenge_not_generalization_benchmark":True,
        "cases":len(rows),
        "policy_stats":{
            "WAW_ALIF_MORPH_STRICT":stats("WAW_ALIF_MORPH_STRICT"),
            "WAW_ALIF_MORPH_RECOVERY":stats("WAW_ALIF_MORPH_RECOVERY"),
        },
        "rows":rows,
        "interpretation":"Primary safety requirement is zero false accepts on MUST_NOT_ACCEPT cases. Ambiguous positives are allowed to abstain."
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="rows"},ensure_ascii=False))

if __name__=="__main__":
    main()
