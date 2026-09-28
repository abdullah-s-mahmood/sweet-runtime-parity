"""Gold-blind lexical continuity diagnostic over frozen cross-model agreement events.

No QALB corrected text, no manual labels, no QALB TEST.
No lexical strings are persisted; only counts, set hashes and boolean relations.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path

from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.utils import strip_lex
from camel_tools.utils.dediac import dediac_ar

ROOT=Path(__file__).resolve().parents[2]
AG=ROOT/"artifacts"/"agreement"/"artifacts"/"CROSS_MODEL_AGREEMENT_FEATURES.jsonl"
OUT=ROOT/"artifacts"/"LEXICAL_CONTINUITY_FEATURES.jsonl"
SUM=ROOT/"artifacts"/"LEXICAL_CONTINUITY_RUNTIME.json"
EXPECTED_AGREEMENT_SHA="d66a5ab3c6b9e1527b7a1a59ddce0f843a864281e70106cacd58d00315741c4c"

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def sha_set(values):
    return hashlib.sha256("\u241f".join(sorted(values)).encode("utf-8")).hexdigest()

def read_jsonl(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def norm_lex(value):
    if not value:return None
    try:value=strip_lex(value)
    except Exception:pass
    value=dediac_ar(str(value)).strip()
    return value or None

def analysis_sets(analyses):
    lex=set();roots=set();pos=set()
    for a in analyses:
        lx=norm_lex(a.get("lex"))
        if lx:lex.add(lx)
        rt=str(a.get("root") or "").strip()
        if rt not in ("","0","-","na","None"):roots.add(rt)
        ps=str(a.get("pos") or "").strip()
        if ps not in ("","-","na","None"):pos.add(ps)
    return lex,roots,pos

def main():
    if sha_file(AG)!=EXPECTED_AGREEMENT_SHA:
        raise RuntimeError("Frozen agreement features SHA mismatch")
    events=[x for x in read_jsonl(AG) if x["runtime_decisions"]["EXACT_SINGLE_SUB_AGREEMENT"]=="ACCEPT"]
    assert len(events)==159,len(events)

    db=MorphologyDB.builtin_db("calima-msa-r13",flags="a")
    analyzer=Analyzer(db,backoff="NONE")

    rows=[]
    for e in events:
        ss=e.get("source_surfaces") or []
        oo=e.get("output_surfaces") or []
        assert len(ss)==len(oo)==1,(e["agreement_id"],ss,oo)
        src=ss[0];cand=oo[0]
        sa=analyzer.analyze(src)
        ca=analyzer.analyze(cand)
        sl,sr,sp=analysis_sets(sa)
        cl,cr,cp=analysis_sets(ca)

        source_ok=bool(sa);candidate_ok=bool(ca)
        lex_overlap=bool(sl & cl)
        root_overlap=bool(sr & cr)
        pos_overlap=bool(sp & cp)

        candidate_unanalyzable=not candidate_ok
        lex_disjoint=source_ok and candidate_ok and not lex_overlap
        lex_root_disjoint=lex_disjoint and bool(sr) and bool(cr) and not root_overlap

        rows.append({
            "agreement_id":e["agreement_id"],
            "line_id":e["line_id"],
            "line_hash":e["line_hash"],
            "source_lexical_span":e["source_lexical_span"],
            "source_hash":e["source_hash"],
            "candidate_hash":e["output_hash"],
            "analysis_counts":{"source":len(sa),"candidate":len(ca)},
            "set_counts":{
                "source_lexemes":len(sl),"candidate_lexemes":len(cl),
                "source_roots":len(sr),"candidate_roots":len(cr),
                "source_pos":len(sp),"candidate_pos":len(cp),
            },
            "set_hashes":{
                "source_lexemes":sha_set(sl),"candidate_lexemes":sha_set(cl),
                "source_roots":sha_set(sr),"candidate_roots":sha_set(cr),
                "source_pos":sha_set(sp),"candidate_pos":sha_set(cp),
            },
            "features":{
                "source_analyzable":source_ok,
                "candidate_analyzable":candidate_ok,
                "candidate_unanalyzable":candidate_unanalyzable,
                "lexeme_overlap":lex_overlap,
                "root_overlap":root_overlap,
                "pos_overlap":pos_overlap,
                "lexeme_disjoint":lex_disjoint,
                "lexeme_and_root_disjoint":lex_root_disjoint,
            },
            "runtime_decisions":{
                "LEXEME_DISJOINT_VETO":"REVIEW" if (candidate_unanalyzable or lex_disjoint) else "KEEP_ACCEPT",
                "LEXEME_AND_ROOT_DISJOINT_VETO":"REVIEW" if (candidate_unanalyzable or lex_root_disjoint) else "KEEP_ACCEPT",
                "CANDIDATE_UNANALYZABLE_ONLY":"REVIEW" if candidate_unanalyzable else "KEEP_ACCEPT",
            }
        })

    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
    policies=("LEXEME_DISJOINT_VETO","LEXEME_AND_ROOT_DISJOINT_VETO","CANDIDATE_UNANALYZABLE_ONLY")
    summary={
        "status":"LEXICAL_CONTINUITY_RUNTIME_FROZEN",
        "diagnostic_only":True,
        "gold_or_manual_labels_read":False,
        "agreement_features_sha256":sha_file(AG),
        "rows":len(rows),
        "feature_counts":{
            "source_unanalyzable":sum(not x["features"]["source_analyzable"] for x in rows),
            "candidate_unanalyzable":sum(x["features"]["candidate_unanalyzable"] for x in rows),
            "lexeme_disjoint":sum(x["features"]["lexeme_disjoint"] for x in rows),
            "lexeme_and_root_disjoint":sum(x["features"]["lexeme_and_root_disjoint"] for x in rows),
            "no_pos_overlap":sum(not x["features"]["pos_overlap"] for x in rows),
        },
        "decision_counts":{
            p:{
                "KEEP_ACCEPT":sum(x["runtime_decisions"][p]=="KEEP_ACCEPT" for x in rows),
                "REVIEW":sum(x["runtime_decisions"][p]=="REVIEW" for x in rows),
            } for p in policies
        },
        "qalb15_test_read":False,
        "lexical_strings_persisted":False,
    }
    SUM.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False))

if __name__=="__main__":
    main()
