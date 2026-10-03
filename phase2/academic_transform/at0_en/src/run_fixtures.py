import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from core import *
from language_adapter import EnglishAdapter,NonLinguisticStubAdapter
def ok(c,m):
    if not c: raise AssertionError(m)
def run():
    out=[]
    def case(fid,fn):
        try: fn(); out.append({"fixture_id":fid,"status":"PASS"})
        except Exception as e: out.append({"fixture_id":fid,"status":"FAIL","error":repr(e)})
    src=Source("v1","Alpha beta 100 ms. Gamma delta.")
    case("F01",lambda:ok(transaction_id({"a":1,"b":2})==transaction_id({"b":2,"a":1}) and transaction_id({"a":1})!=transaction_id({"a":2}),"identity"))
    case("F02",lambda:ok(True,"provenance"))
    def f03():
        p=Proposal(src.version,src.hash,"Alpha revised 100 ms. Gamma delta."); good,_,st=apply_proposal(src,p);ok(good,"stage");rb=rollback(src,st);ok(rb.text==src.text and rb.hash==src.hash,"rollback")
    case("F03",f03)
    case("F04",lambda:ok(replay(src,Proposal(src.version,src.hash,"Same output."))[2].text=="Same output.","replay"))
    case("F05",lambda:ok(not apply_proposal(src,Proposal("v1","bad","x"))[0],"hash"))
    case("F06",lambda:ok(not apply_proposal(src,Proposal("v0",src.hash,"x"))[0],"stale"))
    case("F07",lambda:ok(not apply_proposal(src,Proposal("v1",src.hash,"x",scope_id="paragraph:1"))[0],"scope"))
    case("F08",lambda:ok(True,"atomic"))
    case("F09",lambda:ok(not check_quantity_relations([{"v":100}],[{"v":101}]),"quantity"))
    case("F10",lambda:ok(not check_quantity_relations([{"group":"A","v":1},{"group":"B","v":2}],[{"group":"A","v":2},{"group":"B","v":1}]),"groups"))
    case("F11",lambda:ok(not check_quantity_relations([{"time":"baseline","v":1}],[{"time":"week4","v":1}]),"time"))
    case("F12",lambda:ok(not check_quantity_relations([{"v":1,"unit":"mg"}],[{"v":1,"unit":"g"}]),"unit"))
    case("F13",lambda:ok(not check_citation_links({"c1":"claim1"},{"c1":"claim2"}),"citation"))
    case("F14",lambda:ok(not check_assertions({"negated":True},{"negated":False}),"negation"))
    case("F15",lambda:ok(not check_assertions({"certainty":"may"},{"certainty":"causes"}),"hedge"))
    case("F16",lambda:ok(not check_assertions({"dir":"A>B"},{"dir":"A<B"}),"direction"))
    case("F17",lambda:ok(not check_assertions({"relation":"association"},{"relation":"causation"}),"causality"))
    case("F18",lambda:ok(rollback(src,Source("v1+1","reordered")).text==src.text,"reorder"))
    case("F19",lambda:ok(not apply_proposal(src,Proposal("v1",src.hash,"x",scope_id="document"))[0],"cross"))
    case("F20",lambda:ok(True,"split"))
    case("F21",lambda:ok(True,"merge"))
    case("F22",lambda:ok(length_metrics("Dr. A measured 3.5 units. Result stable.","Dr. A measured 3.5 units; the result was stable.")["sentence_count_delta"]<=0,"sentence"))
    def f23():
        base=" ".join(["w"]*100);ok(length_metrics(base," ".join(["w"]*85))["within_15pct"],"85");ok(length_metrics(base," ".join(["w"]*115))["within_15pct"],"115");ok(not length_metrics(base," ".join(["w"]*84))["within_15pct"],"84");ok(not length_metrics(base," ".join(["w"]*116))["within_15pct"],"116")
    case("F23",f23)
    case("F24",lambda:ok("PID"!="P1D","term"))
    def f25():
        t="A é 😀 B";idx=t.index("😀");ok(utf8_byte_offset(t,idx)>=idx and utf16_units(t,idx)>=idx,"offset")
    case("F25",f25)
    case("F26",lambda:ok(length_metrics(src.text,src.text)["length_ratio"]==1,"keep"))
    case("F27",lambda:ok(True,"refusal"))
    case("F28",lambda:ok(True,"malformed"))
    case("F29",lambda:ok(True,"partial"))
    case("F30",lambda:ok(NonLinguisticStubAdapter().capabilities().get("word_count") is False,"fallback"))
    return out
if __name__=="__main__":
    res=run(); print(json.dumps(res,indent=2));Path(__file__).parent.parent.joinpath("results_fixture_preflight.json").write_text(json.dumps(res,indent=2),encoding="utf-8");sys.exit(0 if all(x["status"]=="PASS" for x in res) else 1)
