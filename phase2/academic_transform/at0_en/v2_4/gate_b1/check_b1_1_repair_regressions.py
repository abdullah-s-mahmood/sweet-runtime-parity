from __future__ import annotations
import importlib.util, pathlib

HERE=pathlib.Path(__file__).resolve().parent
ALIGNER=HERE/"b1_aligner.py"

spec=importlib.util.spec_from_file_location("b1",ALIGNER)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def A(i,subject,predicate,obj,bindings):
    return {
        "id":i,"criticality":"CRITICAL","subject":subject,"predicate":predicate,"object":obj,
        "polarity":"POSITIVE","modality":"ASSERTED","causality":"NONE",
        "scope":[],"time":[],"population":[],"baseline":[],
        "bindings":bindings,"confidence_status":"CERTAIN","evidence":i
    }

# Regression 1: owner-first assignment must not cross-match identical values to wrong owners.
src=[
    A("S1","Group X","REQUIRE","completion",{"value":10.0,"unit":"s"}),
    A("S2","Group Y","REQUIRE","completion",{"value":20.0,"unit":"s"}),
]
cand=[
    A("C1","Group X","REQUIRE","completion",{"value":20.0,"unit":"s"}),
    A("C2","Group Y","REQUIRE","completion",{"value":10.0,"unit":"s"}),
]
al=m.align_assertions(src,cand)
pairs={(tuple(x["source_ids"]),tuple(x["candidate_ids"])):x["status"] for x in al}
assert pairs[(("S1",),("C1",))]=="ALTERED", pairs
assert pairs[(("S2",),("C2",))]=="ALTERED", pairs

# Regression 2: split definitions and a faithful merged representation are binding-equivalent.
src=[
    A("S1","X_i","DEFINE","throughput",{"symbol":"X_i"}),
    A("S2","Y_i","DEFINE","normalized delay",{"symbol":"Y_i"}),
]
cand=[
    A("C1","X_i and Y_i","DEFINE","their respective quantities",{"X_i":"throughput","Y_i":"normalized delay"}),
]
al=m.align_assertions(src,cand)
assert len(al)==1 and al[0]["status"]=="PRESERVED", al

# Regression 3: owner-bound numeric facts remain equal across scalar+unit vs merged string representation.
src=[
    A("S1","Group X","REQUIRE","completion",{"value":46.2,"unit":"s"}),
    A("S2","Group Y","REQUIRE","completion",{"value":49.8,"unit":"s"}),
]
cand=[
    A("C1","Groups X and Y","REQUIRE","completion",{"Group_X":"46.2 s","Group_Y":"49.8 s"}),
]
al=m.align_assertions(src,cand)
assert len(al)==1 and al[0]["status"]=="PRESERVED", al

print("B1.1 repair regressions: 3/3 PASS")
