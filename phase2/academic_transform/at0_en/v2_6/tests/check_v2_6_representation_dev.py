#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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

a2=loadmod("v26_a2",V26/"gate_a"/"source_assertion_extractor.py")
ra=loadmod("v26_ra",V26/"gate_b2"/"relation_aware_extractor.py")
al=loadmod("v26_al",V26/"gate_b1"/"b1_aligner.py")

def predict(source,candidate,case_id):
    sg=ra.relation_aware_extract(source,case_id+"-SRC")
    cg=ra.relation_aware_extract(candidate,case_id+"-CAND")
    if not sg["assertions"] or not cg["assertions"]:
        return {"predicted_outcome":"INVALID_VERIFICATION","assertion_alignment":[]}
    return al.align_pair({"pair_id":case_id,"source_graph":sg,"candidate_graph":cg})

def assertion(i,subject,obj,criticality="CRITICAL"):
    return {
        "id":f"A{i:03d}",
        "criticality":criticality,
        "subject":subject,
        "predicate":"REDUCE",
        "object":obj,
        "polarity":"POSITIVE",
        "modality":"ASSERTED",
        "causality":"NONE",
        "scope":[],
        "time":[],
        "population":[],
        "baseline":[],
        "bindings":{},
        "confidence_status":"CERTAIN",
        "evidence":f"{subject} reduced {obj}.",
    }

# A. 60 segmentation / normalization fixtures.
seg_templates=[
    ("The treatment reduced pain, e.g. headache burden. Adverse events were rare.",2),
    ("The outcome was stable, i.e. no clinically important change. Follow-up continued.",2),
    ("Dr. Smith reported improvement. Follow-up continued.",2),
    ("Jones et al. reported improvement. Follow-up continued.",2),
    ("The mean dose was 42.0 mg. Follow-up continued.",2),
    ("The p value was 0.05. Follow-up continued.",2),
    ("<s>Treatment reduced pain.</s> <s>Follow-up continued.</s>",2),
    ("&lt;s&gt;Treatment reduced pain.&lt;/s&gt; &lt;s&gt;Follow-up continued.&lt;/s&gt;",2),
    ("RESULTS:\nTreatment reduced pain. Follow-up continued.",3),
    ("METHODS:\nGroup A required 42.0 s. Group B required 43.0 s.",3),
]
seg_pass=0
seg_details=[]
for rep in range(6):
    for idx,(raw,expected) in enumerate(seg_templates):
        raw=raw.replace("42.0",f"{42+rep}.0").replace("43.0",f"{43+rep}.0")
        norm,mapping,events=ra.normalize_scientific_text(raw)
        spans=a2.sentence_spans(norm)
        ok=len(spans)==expected and len(mapping)==len(norm)
        if "<s>" in norm.lower() or "</s>" in norm.lower() or "&lt;s&gt;" in norm.lower():
            ok=False
        seg_pass+=int(ok)
        seg_details.append({"id":f"SEG-{rep:02d}-{idx:02d}","ok":ok,"span_count":len(spans),"expected":expected})

# B. 60 safe paraphrase fixtures.
safe_cases=[]
for i in range(10):
    safe_cases += [
        (f"Treatment{i} reduced pain{i}.",f"Treatment{i} lowered pain{i}."),
        (f"Marker_{i} is measured as level_{i}.",f"Marker_{i} is measured as level_{i}."),
        (f"X_{i} denotes outcome{i}.",f"X_{i} represents outcome{i}."),
        (f"Group A required {42+i}.0 s.",f"Group A required {42+i} s."),
        (f"Algorithm{i} runs for {100+i} iterations with seed {7+i}.",f"Algorithm{i} runs for {100+i} iterations with seed {7+i}."),
        (f"Therapy{i} treats hypertension{i}.",f"Therapy{i} typically treats hypertension{i}."),
    ]
safe_counts={"PASS_CANDIDATE":0,"REJECT":0,"REVIEW":0,"INVALID_VERIFICATION":0}
safe_examples=[]
for k,(s,c) in enumerate(safe_cases):
    p=predict(s,c,f"SAFE-{k:03d}")
    out=p["predicted_outcome"]
    safe_counts[out]=safe_counts.get(out,0)+1
    if out!="PASS_CANDIDATE" and len(safe_examples)<10:
        safe_examples.append({"id":f"SAFE-{k:03d}","outcome":out,"source":s,"candidate":c,"alignment":p["assertion_alignment"]})

# C. 80 critical-error fixtures.
critical_cases=[]
for i in range(10):
    critical_cases += [
        (f"Group A required {42+i}.0 s.",f"Group A required {43+i}.0 s.","quantity"),
        (f"Group A required {42+i}.0 s.",f"Group B required {42+i}.0 s.","owner"),
        (f"System{i} may aim to reduce pain{i}.",f"System{i} aims to reduce pain{i}.","modality"),
        (f"Drug{i} treats condition{i}.",f"Drug{i} is used for condition{i}.","predicate"),
        (f"Treatment{i} reduced severe neuropathic pain{i}.",f"Treatment{i} reduced nausea{i}.","concept"),
        (f"Association{i} does not establish that exposure{i} causes disease{i}.",f"Exposure{i} causes disease{i}.","causality"),
        (f"Method{i} was not evaluated outside cohort{i}.",f"Method{i} was evaluated outside cohort{i}.","scope"),
        (f"Treatment{i} reduced pain{i}. Treatment{i} reduced fatigue{i}.",f"Treatment{i} reduced pain{i}.","omission"),
    ]
critical_counts={"PASS_CANDIDATE":0,"REJECT":0,"REVIEW":0,"INVALID_VERIFICATION":0}
critical_examples=[]
for k,(s,c,fam) in enumerate(critical_cases):
    p=predict(s,c,f"ERR-{k:03d}")
    out=p["predicted_outcome"]
    critical_counts[out]=critical_counts.get(out,0)+1
    if out!="REJECT" and len(critical_examples)<12:
        critical_examples.append({"id":f"ERR-{k:03d}","family":fam,"outcome":out,"source":s,"candidate":c,"alignment":p["assertion_alignment"]})

# D. 60 unequal-count mechanics fixtures.
unequal_pass=0
unequal_details=[]
for i in range(20):
    source=[assertion(1,f"S{i}A","pain"),assertion(2,f"S{i}B","fatigue"),assertion(3,f"S{i}C","nausea")]
    cand=[assertion(1,f"S{i}A","pain"),assertion(2,f"S{i}B","fatigue")]
    aa=al.align_assertions(source,cand)
    ok=all(len(x["source_ids"])<=1 and len(x["candidate_ids"])<=1 for x in aa) and sum(not x["candidate_ids"] for x in aa)==1
    unequal_pass+=int(ok); unequal_details.append({"id":f"UNEQ-S-{i:02d}","ok":ok,"alignments":aa})
for i in range(20):
    source=[assertion(1,f"T{i}A","pain"),assertion(2,f"T{i}B","fatigue")]
    cand=[assertion(1,f"T{i}A","pain"),assertion(2,f"T{i}B","fatigue"),assertion(3,f"T{i}C","nausea")]
    aa=al.align_assertions(source,cand)
    ok=all(len(x["source_ids"])<=1 and len(x["candidate_ids"])<=1 for x in aa) and sum(not x["source_ids"] for x in aa)==1
    unequal_pass+=int(ok); unequal_details.append({"id":f"UNEQ-C-{i:02d}","ok":ok,"alignments":aa})
for i in range(20):
    source=[assertion(j+1,f"U{i}-{j}",f"outcome{j}") for j in range(5)]
    cand=[assertion(1,f"U{i}-0","outcome0"),assertion(2,f"U{i}-1","outcome1")]
    aa=al.align_assertions(source,cand)
    ok=all(len(x["source_ids"])<=1 and len(x["candidate_ids"])<=1 for x in aa) and sum(not x["candidate_ids"] for x in aa)==3
    unequal_pass+=int(ok); unequal_details.append({"id":f"UNEQ-5-2-{i:02d}","ok":ok,"alignments":aa})

total=260
safe_pass=safe_counts["PASS_CANDIDATE"]
safe_review=safe_counts["REVIEW"]
critical_reject=critical_counts["REJECT"]
hard={
    "valid_fixture_invalid_zero":safe_counts["INVALID_VERIFICATION"]==0 and critical_counts["INVALID_VERIFICATION"]==0,
    "critical_error_unsafe_pass_zero":critical_counts["PASS_CANDIDATE"]==0,
    "segmentation_all_pass":seg_pass==60,
    "unequal_explicit_accounting_all_pass":unequal_pass==60,
}
utility={
    "safe_pass_rate":safe_pass/60,
    "critical_reject_rate":critical_reject/80,
    "safe_review_rate":safe_review/60,
    "safe_pass_ge_0_80":safe_pass/60>=0.80,
    "critical_reject_ge_0_90":critical_reject/80>=0.90,
    "safe_review_le_0_20":safe_review/60<=0.20,
}
summary={
    "suite_id":"AT0_EN_V26_REPRESENTATION_DEV_MECHANICS_V1",
    "fixture_count":total,
    "factpico_records_used":0,
    "segmentation":{"passed":seg_pass,"total":60,"details":seg_details},
    "safe":{"counts":safe_counts,"examples_nonpass":safe_examples},
    "critical_error":{"counts":critical_counts,"examples_nonreject":critical_examples},
    "unequal_count":{"passed":unequal_pass,"total":60},
    "hard_invariants":hard,
    "utility":utility,
    "overall_pass":all(hard.values()) and all(v for k,v in utility.items() if k.endswith(("_0_80","_0_90","_0_20"))),
}
raw=json.dumps(summary,ensure_ascii=False,sort_keys=True,separators=(",",":"))
summary["canonical_summary_sha256"]=hashlib.sha256(raw.encode()).hexdigest()
print(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2))
if not summary["overall_pass"]:
    raise SystemExit(2)
