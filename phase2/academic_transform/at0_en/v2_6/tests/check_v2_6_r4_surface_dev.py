#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent
V26=HERE.parent

def loadmod(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ra=loadmod("r4_ra",V26/"gate_b2"/"relation_aware_extractor.py")
al=loadmod("r4_al",V26/"gate_b1"/"b1_aligner.py")

def graph(text,case):
    return ra.relation_aware_extract(text,case)

def predict(source,candidate,case):
    return al.align_pair({
        "pair_id":case,
        "source_graph":graph(source,case+"-S"),
        "candidate_graph":graph(candidate,case+"-C"),
    })

def statuses(g):
    return [(a["predicate"],a["confidence_status"],a["criticality"],a["subject"],a.get("object")) for a in g["assertions"]]

# 1) 30 explicit RCT surface extraction fixtures.
extract_cases=[]
for i in range(5):
    extract_cases += [
        (f"Randomized double-blind phase II trial {i}.","STUDY_DESIGN","MATERIAL"),
        (f"One hundred patients with condition{i} were enrolled.","POPULATION","CRITICAL"),
        (f"Patients were randomly assigned to treatment{i} or placebo{i}.","ASSIGN","CRITICAL"),
        (f"The primary outcome was symptom score{i} at 12 weeks.","DEFINE_OUTCOME","CRITICAL"),
        (f"Treatment{i} reduced symptom score{i} by {10+i}%.","REDUCE","CRITICAL"),
        (f"No serious adverse events were reported in either group{i}.","SAFETY_EVENT","CRITICAL"),
    ]

extract_pass=0
extract_fail=[]
for k,(text,expected_pred,expected_crit) in enumerate(extract_cases):
    g=graph(text,f"R4-EXT-{k:03d}")
    ok=(
        len(g["assertions"])>=1
        and any(a["predicate"]==expected_pred and a["confidence_status"]=="CERTAIN" and a["criticality"]==expected_crit
                for a in g["assertions"])
        and all(a["predicate"]!="UNRESOLVED" for a in g["assertions"])
    )
    extract_pass+=int(ok)
    if not ok:
        extract_fail.append({"id":f"R4-EXT-{k:03d}","text":text,"expected":[expected_pred,expected_crit],"actual":statuses(g)})

# 2) 30 safe biomedical paraphrase pairs.
safe=[]
for i in range(5):
    safe += [
        (f"One hundred patients with condition{i} were enrolled.",
         f"100 patients with condition{i} were enrolled."),
        (f"Patients were randomly assigned to treatment{i} or placebo{i}.",
         f"Patients were allocated at random to treatment{i} or placebo{i}."),
        (f"The primary outcome was symptom score{i} at 12 weeks.",
         f"The primary endpoint was symptom score{i} at 12 weeks."),
        (f"Treatment{i} reduced symptom score{i} by {10+i}%.",
         f"Treatment{i} decreased symptom score{i} by {10+i}%."),
        (f"No serious adverse events were reported in either group{i}.",
         f"No serious adverse events were observed in either group{i}."),
        (f"Overall quality of life improved in the treatment{i} group.",
         f"Overall quality of life increased in the treatment{i} group."),
    ]

safe_counts={"PASS_CANDIDATE":0,"REJECT":0,"REVIEW":0,"INVALID_VERIFICATION":0}
safe_fail=[]
for k,(s,c) in enumerate(safe):
    p=predict(s,c,f"R4-SAFE-{k:03d}")
    safe_counts[p["predicted_outcome"]]+=1
    if p["predicted_outcome"]!="PASS_CANDIDATE":
        safe_fail.append({"id":f"R4-SAFE-{k:03d}","source":s,"candidate":c,"outcome":p["predicted_outcome"],"aa":p["assertion_alignment"]})

# 3) 40 critical biomedical mutation pairs.
bad=[]
for i in range(5):
    bad += [
        (f"One hundred patients with condition{i} were enrolled.",
         f"One hundred healthy volunteers were enrolled.","population"),
        (f"Patients were randomly assigned to treatment{i} or placebo{i}.",
         f"Patients were randomly assigned to treatment{i} or surgery{i}.","comparator"),
        (f"The primary outcome was symptom score{i} at 12 weeks.",
         f"The primary outcome was mortality{i} at 12 weeks.","outcome"),
        (f"Treatment{i} reduced symptom score{i} by {10+i}%.",
         f"Treatment{i} increased symptom score{i} by {10+i}%.","direction"),
        (f"Treatment{i} reduced symptom score{i} by {10+i}%.",
         f"Treatment{i} reduced symptom score{i} by {20+i}%.","quantity"),
        (f"No serious adverse events were reported in either group{i}.",
         f"Serious adverse events were reported in both groups{i}.","safety"),
        (f"Treatment{i} may reduce recurrence{i}.",
         f"Treatment{i} reduces recurrence{i}.","modality"),
        (f"Exposure{i} was associated with outcome{i}.",
         f"Exposure{i} caused outcome{i}.","causality"),
    ]

bad_counts={"PASS_CANDIDATE":0,"REJECT":0,"REVIEW":0,"INVALID_VERIFICATION":0}
bad_fail=[]
for k,(s,c,fam) in enumerate(bad):
    p=predict(s,c,f"R4-BAD-{k:03d}")
    bad_counts[p["predicted_outcome"]]+=1
    if p["predicted_outcome"]!="REJECT":
        bad_fail.append({"id":f"R4-BAD-{k:03d}","family":fam,"source":s,"candidate":c,"outcome":p["predicted_outcome"],"aa":p["assertion_alignment"]})

# 4) 20 compression/material-omission fixtures.
compress=[]
for i in range(10):
    compress.append((
        f"Randomized prospective trial {i}. Tertiary university hospital. One hundred patients with disease{i} were enrolled. "
        f"Patients were randomly assigned to treatment{i} or placebo{i}. The primary outcome was pain score{i}. "
        f"Treatment{i} reduced pain score{i} by {10+i}%.",
        f"One hundred patients with disease{i} were enrolled. Patients were randomly assigned to treatment{i} or placebo{i}. "
        f"The primary outcome was pain score{i}. Treatment{i} reduced pain score{i} by {10+i}%.",
    ))
    compress.append((
        f"Background rationale for study{i}. Randomized controlled trial {i}. Two hundred participants with disease{i} were enrolled. "
        f"Participants received drug{i} or placebo{i}. The primary endpoint was recurrence{i}. No significant difference in recurrence{i} was observed.",
        f"Two hundred participants with disease{i} were enrolled. Participants received drug{i} or placebo{i}. "
        f"The primary endpoint was recurrence{i}. No significant difference in recurrence{i} was observed.",
    ))

compression_counts={"PASS_CANDIDATE":0,"REJECT":0,"REVIEW":0,"INVALID_VERIFICATION":0}
compression_fail=[]
for k,(s,c) in enumerate(compress):
    p=predict(s,c,f"R4-COMP-{k:03d}")
    compression_counts[p["predicted_outcome"]]+=1
    if p["predicted_outcome"]!="PASS_CANDIDATE":
        compression_fail.append({"id":f"R4-COMP-{k:03d}","outcome":p["predicted_outcome"],"aa":p["assertion_alignment"]})

summary={
    "suite_id":"AT0_EN_V26_R4_SURFACE_DEV_V1",
    "factpico_records_used":0,
    "fixture_count":120,
    "extraction":{"pass":extract_pass,"total":30,"failures":extract_fail[:10]},
    "safe":{"counts":safe_counts,"failures":safe_fail[:10]},
    "critical":{"counts":bad_counts,"failures":bad_fail[:10]},
    "compression":{"counts":compression_counts,"failures":compression_fail[:10]},
    "hard_invariants":{
        "extraction_30_of_30":extract_pass==30,
        "safe_no_reject_or_review":safe_counts["PASS_CANDIDATE"]==30,
        "critical_unsafe_pass_zero":bad_counts["PASS_CANDIDATE"]==0,
        "critical_reject_40_of_40":bad_counts["REJECT"]==40,
        "compression_20_of_20_pass":compression_counts["PASS_CANDIDATE"]==20,
        "invalid_zero":(
            safe_counts["INVALID_VERIFICATION"]==0 and
            bad_counts["INVALID_VERIFICATION"]==0 and
            compression_counts["INVALID_VERIFICATION"]==0
        ),
    }
}
summary["overall_pass"]=all(summary["hard_invariants"].values())
print(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2))
if not summary["overall_pass"]:
    raise SystemExit(2)
