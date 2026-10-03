from __future__ import annotations
import importlib.util, pathlib

HERE=pathlib.Path(__file__).resolve().parent
EX=HERE/"b2_2_relation_aware_extractor.py"
B1=HERE.parent/"gate_b1"/"b1_aligner.py"

src=EX.read_text(encoding="utf-8")
for forbidden in ["B1-P01","B1-P02","B1-P03","B1-P04","B1-P05","B1-P06","B1-P07","B1-P08","B1-P09","B1-P10","B1-P11","B1-P12","expected_outcome","gold_alignment"]:
    assert forbidden not in src, forbidden

spec=importlib.util.spec_from_file_location("ex",EX)
ex=importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
spec=importlib.util.spec_from_file_location("b1",B1)
b1=importlib.util.module_from_spec(spec); spec.loader.exec_module(b1)

def graph(text,name):
    return ex.relation_aware_extract(text,name)

def outcome(a,b):
    return b1.align_pair({"pair_id":"REG","source_graph":a,"candidate_graph":b})["predicted_outcome"]

# 1. Predicate/paraphrase normalization.
g1=graph("Adaptive routing reduced mean delay.","R1S")
g2=graph("Adaptive routing lowered mean delay.","R1C")
assert outcome(g1,g2)=="PASS_CANDIDATE",(g1,g2,outcome(g1,g2))

# 2. Negation/scope ownership.
g1=graph("The finding was not evaluated outside the evening window.","R2S")
g2=graph("The finding was also evaluated outside the evening window.","R2C")
assert outcome(g1,g2)=="REJECT",(g1,g2,outcome(g1,g2))

# 3. Split/merge owner/value binding.
g1=graph("At 14:00, Group A required 46.2 s. At 14:00, Group B required 49.8 s.","R3S")
g2=graph("At 14:00, route completion required 46.2 s for Group A and 49.8 s for Group B.","R3C")
assert outcome(g1,g2)=="PASS_CANDIDATE",(g1,g2,outcome(g1,g2))

g3=graph("At 14:00, route completion required 49.8 s for Group A and 46.2 s for Group B.","R3X")
assert outcome(g1,g3)=="REJECT",(g1,g3,outcome(g1,g3))

# 4. Citation-to-claim binding.
s="Adaptive routing reduced mean delay. Packet loss increased when relay density was reduced. Delay claim -> CIT_SYN_A. Packet-loss claim -> CIT_SYN_B."
c_ok="Adaptive routing reduced mean delay. Packet loss increased when relay density was reduced. Delay claim -> CIT_SYN_A. Packet-loss claim -> CIT_SYN_B."
c_swap="Adaptive routing reduced mean delay. Packet loss increased when relay density was reduced. Delay claim -> CIT_SYN_B. Packet-loss claim -> CIT_SYN_A."
g1=graph(s,"R4S"); g2=graph(c_ok,"R4C"); g3=graph(c_swap,"R4X")
assert outcome(g1,g2)=="PASS_CANDIDATE",(g1,g2,outcome(g1,g2))
assert outcome(g1,g3)=="REJECT",(g1,g3,outcome(g1,g3))
assert len(g1["relations"])==2,g1["relations"]

# 5. Equation coefficient-to-symbol binding.
g1=graph("P_i = w_1U_i + w_2D_i.","R5S")
g2=graph("P_i = w_1U_i + w_2D_i.","R5C")
g3=graph("P_i = w_1D_i + w_2U_i.","R5X")
assert outcome(g1,g2)=="PASS_CANDIDATE",(g1,g2,outcome(g1,g2))
assert outcome(g1,g3)=="REJECT",(g1,g3,outcome(g1,g3))

# 6. Ambiguity must not be promoted.
g1=graph("The result may reflect improved neighbor awareness.","R6S")
g2=graph("This outcome may reflect better neighbor awareness.","R6C")
assert outcome(g1,g2)=="REVIEW",(g1,g2,outcome(g1,g2))

# 7-11. Explicit scientific predicate normalization on generic, non-benchmark sentences.
cases=[
    ("We define throughput as delivered packets per second.","DEFINE"),
    ("The scheduler aims to reduce deadline misses.","AIM_TO"),
    ("The analysis treats latency and throughput independently.","TREAT"),
    ("These measurements are used for estimating packet loss.","USE_FOR"),
    ("We introduce RouteGuard, a framework for validating paths.","INTRODUCE"),
]
for i,(text,pred) in enumerate(cases,7):
    g=graph(text,f"RX{i}")
    assert len(g["assertions"])==1,(text,g)
    a=g["assertions"][0]
    assert a["predicate"]==pred,(text,a)
    assert a["confidence_status"]=="CERTAIN",(text,a)

print("B2.2 relation-aware principle regressions: 13/13 PASS")
