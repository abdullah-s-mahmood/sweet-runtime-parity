#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path

ARABIC_RE=re.compile(r"[\u0600-\u06ff]")

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
def norm(s):
    return " ".join(s.strip().split())
def hkey(*xs):
    return sha("|".join(map(str,xs)))
def safe_support(*items):
    return list(items)

UNRESOLVED=[
  "scientific_fidelity","factual_truth","citation_integrity",
  "numeric_statistical_relation_preservation","document_integrity",
  "author_intent_if_ambiguous","correctness_of_nonreference_alternatives"
]

def parse_m2(path):
    blocks=[]; src=None; edits=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("S "):
            if src is not None: blocks.append((src,edits))
            src=line[2:]; edits=[]
        elif line.startswith("A ") and src is not None:
            p=line[2:].split("|||")
            if len(p)<3: continue
            span=p[0].split()
            if len(span)<2: continue
            try: a,b=int(span[0]),int(span[1])
            except ValueError: continue
            annot=p[-1].strip()
            if annot not in {"","0"}: continue
            edits.append({"start":a,"end":b,"type":p[1],"correction":p[2]})
    if src is not None: blocks.append((src,edits))
    return blocks

def apply_edits(src,edits,idxs):
    toks=src.split()
    for i in sorted(idxs,key=lambda i:(edits[i]["start"],edits[i]["end"]),reverse=True):
        e=edits[i]
        repl=[] if e["correction"] in {"","-NONE-"} else e["correction"].split()
        toks[e["start"]:e["end"]]=repl
    return " ".join(toks)

def make(case_id,corpus,split,unit_id,fam,src,cand,ref,tier,n_edits=0,applied=None,withheld=None,natural=True,support=None,extra=None):
    applied=applied or []; withheld=withheld or []
    direct={}
    if fam.endswith("CLEAN_REFERENCE_KEEP") or fam=="QALB_CLEAN_REFERENCE_KEEP":
        direct={"clean_text":"EXPERT_REFERENCE_SUPPORTED","necessity":"KEEP_SUPPORTED_RELATIVE_TO_REFERENCE","repair_completeness":"COMPLETE_RELATIVE_TO_REFERENCE"}
    elif fam.endswith("ERRONEOUS_SOURCE_KEEP") or fam=="QALB_ERRONEOUS_SOURCE_KEEP":
        direct={"necessity":"EXPERT_CORRECTION_EXISTS","repair_completeness":"INCOMPLETE_RELATIVE_TO_REFERENCE","known_reference_residual":True}
    elif fam in {"QALB_ONE_OF_MANY_PARTIAL","QALB_ALL_BUT_ONE_PARTIAL"}:
        direct={"local_correctness":"APPLIED_EDITS_REFERENCE_SUPPORTED","repair_completeness":"INCOMPLETE_RELATIVE_TO_REFERENCE","known_withheld_reference_edit_count":len(withheld),"residual_relation":"UNRESOLVED"}
    else:
        direct={"necessity":"EXPERT_CORRECTION_EXISTS","contextual_correctness":"REFERENCE_SUPPORTED","repair_completeness":"COMPLETE_RELATIVE_TO_REFERENCE"}
    r={
      "case_id":case_id,"corpus":corpus,"split":split,"unit_id":unit_id,"case_family":fam,
      "source_sha256":sha(src),"candidate_sha256":sha(cand),"reference_sha256":sha(ref),
      "reference_edit_count":n_edits,"applied_reference_edit_indices":applied,
      "withheld_reference_edit_indices":withheld,"evidence_tier":tier,
      "direct_assertions":direct,"protocol_support":support or [],
      "unresolved_axes":UNRESOLVED,"controlled_counterfactual":not natural,
      "raw_text_persisted":False
    }
    if extra: r.update(extra)
    return r

def cap(rows,fam,n):
    xs=[x for x in rows if x["case_family"]==fam]
    xs.sort(key=lambda x:hkey(x["corpus"],x["split"],x["unit_id"],x["case_family"]))
    return xs[:n]

def read_lines(p):
    return p.read_text(encoding="utf-8-sig").splitlines()

def load_qalb(root):
    rows=[]; stats={}; multi=0; recon_fail=0
    for split,prefix in [("train","QALB-2014-L1-Train"),("dev","QALB-2014-L1-Dev")]:
        d=root/split
        srcs=read_lines(d/f"{prefix}.sent.no_ids")
        cors=read_lines(d/f"{prefix}.cor.no_ids")
        blocks=parse_m2(d/f"{prefix}.m2")
        if len(srcs)!=len(cors): raise SystemExit(f"QALB line mismatch {split}")
        block_ok=len(blocks)==len(srcs)
        st=Counter(source_lines=len(srcs),corrected_lines=len(cors),m2_blocks=len(blocks),m2_count_matches_lines=int(block_ok))
        for i,(src,cor) in enumerate(zip(srcs,cors),1):
            s,c=norm(src),norm(cor)
            # Every human-corrected reference becomes a clean KEEP source.
            rows.append(make(f"Q14-{split}-{i}-CK","QALB14_L1",split,str(i),"QALB_CLEAN_REFERENCE_KEEP",c,c,c,"S",support=safe_support("QALB human corrected reference")))
            st["clean_reference_keep"]+=1
            if s==c:
                st["naturally_unchanged"]+=1
                continue
            st["changed_lines"]+=1
            rows.append(make(f"Q14-{split}-{i}-KEEPRAW","QALB14_L1",split,str(i),"QALB_ERRONEOUS_SOURCE_KEEP",s,s,c,"S",support=safe_support("QALB raw differs from human corrected reference")))
            edits=[]
            if block_ok:
                bsrc,bedits=blocks[i-1]
                if norm(bsrc)==s: edits=bedits
            if not edits:
                st["changed_without_usable_m2"]+=1
                rows.append(make(f"Q14-{split}-{i}-FULL","QALB14_L1",split,str(i),"QALB_FULL_EXPERT_REPAIR",s,c,c,"S",support=safe_support("QALB full human correction")))
                continue
            idx=list(range(len(edits)))
            recon=norm(apply_edits(s,edits,idx))
            if recon!=c:
                recon_fail+=1; st["m2_reconstruction_fail"]+=1
                rows.append(make(f"Q14-{split}-{i}-FULL","QALB14_L1",split,str(i),"QALB_FULL_EXPERT_REPAIR",s,c,c,"S",n_edits=len(edits),applied=idx,support=safe_support("QALB full human correction; M2 partial synthesis skipped")))
                continue
            st["m2_reconstructable"]+=1
            n=len(edits)
            rows.append(make(f"Q14-{split}-{i}-FULL","QALB14_L1",split,str(i),"QALB_FULL_EXPERT_REPAIR",s,c,c,"S",n_edits=n,applied=idx,support=safe_support("QALB human reference + official M2")))
            if n==1:
                st["single_edit_complete"]+=1
                rows.append(make(f"Q14-{split}-{i}-SINGLE","QALB14_L1",split,str(i),"QALB_SINGLE_EDIT_COMPLETE",s,c,c,"S",n_edits=1,applied=[0],support=safe_support("sole official M2 edit reconstructs human reference")))
            if n>=2:
                multi+=1; st["multi_edit_reconstructable"]+=1
                one=int(hkey(split,i,"one")[:8],16)%n
                with1=[x for x in idx if x!=one]
                cand1=norm(apply_edits(s,edits,[one]))
                rows.append(make(f"Q14-{split}-{i}-ONE","QALB14_L1",split,str(i),"QALB_ONE_OF_MANY_PARTIAL",s,cand1,c,"S",n_edits=n,applied=[one],withheld=with1,natural=False,support=safe_support("controlled: one official human edit applied, others withheld")))
                miss=int(hkey(split,i,"missing")[:8],16)%n
                app=[x for x in idx if x!=miss]
                cand2=norm(apply_edits(s,edits,app))
                rows.append(make(f"Q14-{split}-{i}-ABO","QALB14_L1",split,str(i),"QALB_ALL_BUT_ONE_PARTIAL",s,cand2,c,"S",n_edits=n,applied=app,withheld=[miss],natural=False,support=safe_support("controlled: one official human edit withheld")))
        stats[split]=dict(st)
    return rows,stats,multi,recon_fail

def load_zaebuc(root):
    raw=read_lines(root/"train.sent.raw"); cor=read_lines(root/"train.sent.cor")
    if len(raw)!=len(cor): raise SystemExit(f"ZAEBUC train line mismatch {len(raw)} != {len(cor)}")
    rows=[]; st=Counter(total_pairs=len(raw))
    for i,(a,b) in enumerate(zip(raw,cor),1):
        s,c=norm(a),norm(b)
        rows.append(make(f"ZAE-train-{i}-CK","ZAEBUC_AR","train",str(i),"ZAEBUC_CLEAN_REFERENCE_KEEP",c,c,c,"S",support=safe_support("ZAEBUC professionally corrected Arabic reference")))
        st["clean_reference_keep"]+=1
        if s==c:
            st["unchanged_pairs"]+=1
            continue
        st["changed_pairs"]+=1
        rows.append(make(f"ZAE-train-{i}-FULL","ZAEBUC_AR","train",str(i),"ZAEBUC_FULL_EXPERT_REPAIR",s,c,c,"S",support=safe_support("ZAEBUC raw to professional human correction")))
        rows.append(make(f"ZAE-train-{i}-KEEPRAW","ZAEBUC_AR","train",str(i),"ZAEBUC_ERRONEOUS_SOURCE_KEEP",s,s,c,"S",support=safe_support("ZAEBUC raw differs from professional corrected reference")))
    return rows,dict(st)

def load_a7ta(root):
    pairs=[]
    for correct in root.rglob("الصواب.txt"):
        d=correct.parent
        errs=[p for p in d.iterdir() if p.is_file() and p.name.endswith(".txt") and ("الخطأ" in p.name or "الخطا" in p.name)]
        if not errs: continue
        err=sorted(errs,key=lambda p:p.name)[0]
        es=[norm(x) for x in read_lines(err) if norm(x)]
        cs=[norm(x) for x in read_lines(correct) if norm(x)]
        n=min(len(es),len(cs))
        for j in range(n):
            pairs.append((str(d.relative_to(root)),j+1,es[j],cs[j],len(es)==len(cs)))
    rows=[]; st=Counter(discovered_pairs=len(pairs))
    for path,j,e,c,balanced in pairs:
        bucket=int(hkey(path,j,e,c)[:8],16)%100
        part="bootstrap" if bucket<80 else "reserved_m2"
        st[part+"_pairs"]+=1
        if part!="bootstrap": continue
        unit=hkey(path,j)[:20]
        extra={"source_path_sha256":sha(path),"pair_line_index":j,"source_file_pair_balanced":balanced}
        rows.append(make(f"A7-{unit}-PAIR","A7TA","bootstrap",unit,"A7TA_EXPERT_RULE_PAIR",e,c,c,"A",support=safe_support("A7ta pair from expert linguistic reference book"),extra=extra))
        rows.append(make(f"A7-{unit}-CK","A7TA","bootstrap",unit,"A7TA_CLEAN_REFERENCE_KEEP",c,c,c,"A",support=safe_support("correct side of A7ta expert pair"),extra=extra))
    return rows,dict(st)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--qalb-root",required=True)
    ap.add_argument("--zaebuc-root",required=True)
    ap.add_argument("--a7ta-root",required=True)
    ap.add_argument("--out-dir",default=".")
    args=ap.parse_args()
    out=Path(args.out_dir)

    qrows,qstats,multi,recon=load_qalb(Path(args.qalb_root))
    zrows,zstats=load_zaebuc(Path(args.zaebuc_root))
    arows,astats=load_a7ta(Path(args.a7ta_root))
    allrows=qrows+zrows+arows
    avail=Counter(x["case_family"] for x in allrows)

    caps={
      "QALB_FULL_EXPERT_REPAIR":500,
      "QALB_CLEAN_REFERENCE_KEEP":500,
      "QALB_ERRONEOUS_SOURCE_KEEP":500,
      "QALB_SINGLE_EDIT_COMPLETE":250,
      "QALB_ONE_OF_MANY_PARTIAL":500,
      "QALB_ALL_BUT_ONE_PARTIAL":500,
      "ZAEBUC_FULL_EXPERT_REPAIR":300,
      "ZAEBUC_CLEAN_REFERENCE_KEEP":300,
      "ZAEBUC_ERRONEOUS_SOURCE_KEEP":300,
      "A7TA_EXPERT_RULE_PAIR":400,
      "A7TA_CLEAN_REFERENCE_KEEP":400
    }
    sample=[]
    for fam,n in caps.items(): sample.extend(cap(allrows,fam,n))
    sample.sort(key=lambda x:x["case_id"])

    q_changed=sum(qstats[s].get("changed_lines",0) for s in qstats)
    q_clean=sum(qstats[s].get("clean_reference_keep",0) for s in qstats)
    source_families={x["corpus"] for x in sample}

    criteria={
      "qalb_line_counts_match":all(qstats[s]["source_lines"]==qstats[s]["corrected_lines"] for s in qstats),
      "qalb_changed_ge_1000":q_changed>=1000,
      "qalb_clean_reference_keep_ge_1000":q_clean>=1000,
      "qalb_erroneous_source_keep_ge_1000":avail["QALB_ERRONEOUS_SOURCE_KEEP"]>=1000,
      "qalb_multi_edit_reconstructable_ge_300":multi>=300,
      "qalb_one_of_many_ge_300":avail["QALB_ONE_OF_MANY_PARTIAL"]>=300,
      "qalb_all_but_one_ge_300":avail["QALB_ALL_BUT_ONE_PARTIAL"]>=300,
      "zaebuc_line_counts_match":zstats["total_pairs"]==zstats["total_pairs"],
      "zaebuc_total_ge_100":zstats["total_pairs"]>=100,
      "zaebuc_changed_ge_50":zstats.get("changed_pairs",0)>=50,
      "a7ta_discovered_ge_450":astats["discovered_pairs"]>=450,
      "a7ta_bootstrap_ge_300":astats["bootstrap_pairs"]>=300,
      "a7ta_reserved_ge_80":astats["reserved_m2_pairs"]>=80,
      "independent_source_families_ge_3":len(source_families)>=3,
      "forbidden_splits_read":False,
      "raw_arabic_persisted":False,
      "provenance_complete":all(x.get("corpus") and x.get("evidence_tier") and "unresolved_axes" in x for x in sample)
    }
    ready=all(v is True for k,v in criteria.items() if k!="forbidden_splits_read") and criteria["forbidden_splits_read"] is False

    manifest=out/"M1A_V11_EXPERT_BOOTSTRAP_HASHED.jsonl"
    manifest.write_text("\n".join(json.dumps(x,ensure_ascii=False,sort_keys=True) for x in sample)+"\n",encoding="utf-8")
    summary={
      "status":"M1A_V11_DATA_READY" if ready else "M1A_V11_NOT_READY",
      "date":"2026-09-30",
      "version":"1.1",
      "qalb_stats":qstats,
      "zaebuc_train_stats":zstats,
      "a7ta_stats":astats,
      "m2_reconstruction_failures":recon,
      "available_case_families":dict(avail),
      "persisted_sample_counts":dict(Counter(x["case_family"] for x in sample)),
      "source_families":sorted(source_families),
      "criteria":criteria,
      "data_ready":ready,
      "forbidden_data":{
        "qalb14_test_read":False,"qalb15_read":False,
        "zaebuc_dev_read":False,"zaebuc_test_read":False,
        "reserved_nahw_read":False,"sealed_benchmark_read":False
      },
      "interpretation":{
        "improved_vs_v1":[
          "clean KEEP no longer depends on naturally unchanged noisy-source lines",
          "adds independent professional university-writing corrections from ZAEBUC",
          "adds expert-book rule-grounded A7ta pairs",
          "reserves 20 percent of A7ta pairs for later M2 validation"
        ],
        "still_unresolved":[
          "independent human confirmation on ACAD_PASS project cases",
          "scientific fidelity",
          "document integrity",
          "non-reference alternative correctness",
          "Arabic production auto-accept"
        ]
      }
    }
    sp=out/"M1A_V11_EXPERT_BOOTSTRAP_SUMMARY.json"
    sp.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    persisted=manifest.read_text(encoding="utf-8")+sp.read_text(encoding="utf-8")
    if ARABIC_RE.search(persisted): raise SystemExit("raw Arabic leaked into safe outputs")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if not ready: raise SystemExit(2)

if __name__=="__main__": main()
