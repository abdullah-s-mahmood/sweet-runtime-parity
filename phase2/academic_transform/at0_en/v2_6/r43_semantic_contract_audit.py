#!/usr/bin/env python3
"""Read-only semantic contract audit against actual repository functions.

No training data, weights, SELECT/DEV/TEST, network or model inference.
AST extraction ensures tests execute the real checked-in functions, not copies.
"""
from __future__ import annotations
import ast, collections, json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parent
STAGE=ROOT/"r43_stage_b_h0_h1_diagnostic.py"
ANC=ROOT/"r43_fit_ancestors_train.py"
PREF=ROOT/"r43_contextual_pair_preflight.py"

def extract_fn(path,name,env=None):
    tree=ast.parse(path.read_text(encoding="utf-8"))
    node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name)
    mod=ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[]))
    scope={} if env is None else dict(env)
    exec(compile(mod,str(path),"exec"),scope)
    return scope[name]

def require(a,b,why):
    if a!=b: raise AssertionError(f"{why}: expected {b!r}; observed {a!r}")

def run():
    decode=extract_fn(STAGE,"decode_pred_entities")
    boundary=extract_fn(ANC,"boundary_tags")
    bio=extract_fn(PREF,"bio_spans")
    out={}
    # Invalid IOB2 transition from O is converted to an entity.
    q=decode(["O","I-P","I-P","O"],[.99,.99,.99,.99])
    require([(x["type"],x["start"],x["end"]) for x in q],[("P",1,3)],"invalid I-after-O")
    g,_=bio(["O","I-P","I-P","O"])
    require(g,[("P",1,3)],"gold BIO parser also normalizes invalid I")
    out["invalid_I_after_O"]={"input":["O","I-P","I-P","O"],"decoder_output":q,
      "interpretation":"Model invalid BIO is converted to a valid-looking entity; count occurrence before attributing SELECT FPs."}
    # Cross-type I transition is also converted.
    q=decode(["B-P","I-I","I-I"],[.98,.99,.99])
    require([(x["type"],x["start"],x["end"]) for x in q],[("P",0,1),("I",1,3)],"cross-type I")
    out["invalid_cross_type_I"]={"input":["B-P","I-I","I-I"],"decoder_output":q}

    q=decode(["B-P","I-P","O"],[.94,.93,.99])
    require([(x["type"],x["start"],x["end"]) for x in q],[("P",0,2)],"valid BIO")
    out["valid_BIO_control"]="PASS"

    # Boundaries collide for nested/overlapping entities, if any are supplied.
    ov=boundary(3,[("P",0,2),("I",1,3)])
    require(ov,["START","START","END"],"overlap overwrites prior END")
    out["overlap_boundary_loss"]={"gold_spans":[["P",0,2],["I",1,3]],"boundary_tags":ov,
      "expected_for_P_at_token1":"END","actual":"START",
      "scope":"architecture-level hazard only; current BIO source is flat."}

    # Confirm metric duplicate guard is absent in actual function AST.
    tree=ast.parse(STAGE.read_text(encoding="utf-8"))
    metric=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="metric_counts")
    src=ast.get_source_segment(STAGE.read_text(encoding="utf-8"),metric)
    out["metric_duplicate_guard_static"]={
      "counts_accepted_increment":'counts[typ]["accepted"]+=1' in src,
      "recall_tracks_accepted_in_set":'accepted[(r["document"],r["sentence"])].add(k)' in src,
      "caution":"Potential double-counting if later candidate generators produce duplicate spans; native BIO proposals are currently unique."}

    result={"state":"R43_SEMANTIC_CONTRACT_AUDIT_COMPLETED",
        "tests":out,
        "guards":{"real_data_loaded":False,"models_loaded":False,"historical_dev":False,
            "SELECT":False,"test":False,"other_folds":False,"training":False},
        "conclusion":"BIO illegal transitions are silently normalized; proposed fix requires prospective schema and real-data frequency audit, not posthoc SELECT selection."}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__": run()
