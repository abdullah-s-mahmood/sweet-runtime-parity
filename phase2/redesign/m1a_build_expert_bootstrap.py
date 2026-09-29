#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path

ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
UPSTREAM_REV = "8c7fb84f3ed84d1d30beb7080b02d0f6bfe1c5bf"

def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def norm(s: str) -> str:
    return " ".join(s.strip().split())

def hkey(*xs) -> str:
    return sha("|".join(map(str,xs)))

def parse_m2(path: Path):
    blocks=[]
    cur_src=None
    cur=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("S "):
            if cur_src is not None:
                blocks.append((cur_src,cur))
            cur_src=line[2:]
            cur=[]
        elif line.startswith("A ") and cur_src is not None:
            parts=line[2:].split("|||")
            if len(parts) < 3:
                continue
            span=parts[0].split()
            if len(span) < 2:
                continue
            start,end=int(span[0]),int(span[1])
            typ=parts[1]
            corr=parts[2]
            annotator=parts[-1].strip() if parts else "0"
            # QALB gold is normally annotator 0; ignore other encodings if present.
            if annotator not in {"0",""}:
                continue
            cur.append({"start":start,"end":end,"type":typ,"correction":corr})
    if cur_src is not None:
        blocks.append((cur_src,cur))
    return blocks

def apply_edits(src: str, edits, indices):
    toks=src.split()
    chosen=[(i,edits[i]) for i in indices]
    for _,e in sorted(chosen,key=lambda z:(z[1]["start"],z[1]["end"]),reverse=True):
        repl=[] if e["correction"] in {"","-NONE-"} else e["correction"].split()
        toks[e["start"]:e["end"]]=repl
    return " ".join(toks)

def direct_for(fam, remaining):
    if fam=="EXPERT_KEEP":
        return {
          "necessity":"EXPERT_SUPPORTED_NO_CHANGE",
          "local_correctness":"NOT_APPLICABLE",
          "repair_completeness":"COMPLETE_RELATIVE_TO_REFERENCE"
        }
    if fam in {"FULL_EXPERT_REPAIR","SINGLE_EDIT_COMPLETE"}:
        return {
          "necessity":"EXPERT_CORRECTION_EXISTS",
          "local_correctness":"REFERENCE_SUPPORTED",
          "contextual_correctness":"REFERENCE_SUPPORTED",
          "repair_completeness":"COMPLETE_RELATIVE_TO_REFERENCE",
          "known_reference_residual_count":0
        }
    if fam in {"ONE_OF_MANY_PARTIAL","ALL_BUT_ONE_PARTIAL"}:
        return {
          "necessity":"EXPERT_CORRECTION_EXISTS",
          "local_correctness":"APPLIED_EDITS_REFERENCE_SUPPORTED",
          "repair_completeness":"INCOMPLETE_RELATIVE_TO_REFERENCE",
          "known_reference_residual_count":remaining,
          "residual_relation":"UNRESOLVED"
        }
    if fam=="NAHW_LOCAL_REFERENCE":
        return {
          "necessity":"PUBLISHED_LOCAL_CORRECTION_EXISTS",
          "local_correctness":"REFERENCE_SUPPORTED",
          "repair_completeness":"NOT_ESTABLISHED_FOR_PASSAGE"
        }
    return {}

UNRESOLVED=[
  "scientific_fidelity","factual_truth","author_intent_if_ambiguous",
  "document_integrity","correctness_of_nonreference_alternatives"
]

def rec(case_id, corpus, split, unit_id, fam, src, cand, ref, n_edits, applied, withheld, support):
    remaining=len(withheld)
    return {
      "case_id":case_id,
      "corpus":corpus,
      "split":split,
      "unit_id":unit_id,
      "case_family":fam,
      "source_sha256":sha(src),
      "candidate_sha256":sha(cand),
      "reference_sha256":sha(ref),
      "reference_edit_count":n_edits,
      "applied_reference_edit_indices":applied,
      "withheld_reference_edit_indices":withheld,
      "evidence_tier":"TIER_A_DIRECT",
      "direct_assertions":direct_for(fam,remaining),
      "protocol_support":support,
      "unresolved_axes":UNRESOLVED,
      "raw_text_persisted":False
    }

def capped(rows, fam, n):
    xs=[r for r in rows if r["case_family"]==fam]
    xs.sort(key=lambda r:hkey(r["corpus"],r["split"],r["unit_id"],r["case_family"]))
    return xs[:n]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--qalb-root",required=True)
    ap.add_argument("--repo-root",default=".")
    ap.add_argument("--out-dir",default=".")
    args=ap.parse_args()
    qroot=Path(args.qalb_root)
    repo=Path(args.repo_root)
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)

    allrows=[]
    stats={}
    forbidden_read=[]
    recon_fail=0
    multi_reconstructable=0

    splits=[
      ("train","QALB-2014-L1-Train"),
      ("dev","QALB-2014-L1-Dev")
    ]
    for split,prefix in splits:
        d=qroot/split
        srcp=d/f"{prefix}.sent.no_ids"
        corp=d/f"{prefix}.cor.no_ids"
        m2p=d/f"{prefix}.m2"
        srcs=srcp.read_text(encoding="utf-8").splitlines()
        cors=corp.read_text(encoding="utf-8").splitlines()
        blocks=parse_m2(m2p)
        if len(srcs)!=len(cors):
            raise SystemExit(f"line-count mismatch {split}: {len(srcs)} != {len(cors)}")
        # M2 may omit/alter segmentation in some distributions; align only by index when counts match.
        block_ok=(len(blocks)==len(srcs))
        st=Counter()
        st["source_lines"]=len(srcs)
        st["corrected_lines"]=len(cors)
        st["m2_blocks"]=len(blocks)
        st["m2_count_matches_lines"]=int(block_ok)
        for i,(src,cor) in enumerate(zip(srcs,cors),1):
            srcn,corn=norm(src),norm(cor)
            if srcn==corn:
                st["keep_lines"]+=1
                allrows.append(rec(
                  f"Q14-{split}-{i}-KEEP","QALB14_L1",split,str(i),"EXPERT_KEEP",
                  srcn,srcn,corn,0,[],[],
                  ["QALB human correction protocol; no edit annotated on this line."]
                ))
                continue
            st["changed_lines"]+=1
            edits=[]
            if block_ok:
                bsrc,bedits=blocks[i-1]
                if norm(bsrc)==srcn:
                    edits=bedits
            if not edits:
                st["changed_without_usable_m2"]+=1
                # Full human repair is still usable independent of M2.
                allrows.append(rec(
                  f"Q14-{split}-{i}-FULL","QALB14_L1",split,str(i),"FULL_EXPERT_REPAIR",
                  srcn,corn,corn,0,[],[],
                  ["QALB human-corrected reference line; full source→reference pair."]
                ))
                continue
            idx=list(range(len(edits)))
            recon=norm(apply_edits(srcn,edits,idx))
            if recon!=corn:
                recon_fail+=1
                st["m2_reconstruction_fail"]+=1
                allrows.append(rec(
                  f"Q14-{split}-{i}-FULL","QALB14_L1",split,str(i),"FULL_EXPERT_REPAIR",
                  srcn,corn,corn,len(edits),idx,[],
                  ["QALB human-corrected reference line; M2 reconstruction mismatch so no synthetic partials."]
                ))
                continue
            st["m2_reconstructable"]+=1
            n=len(edits)
            allrows.append(rec(
              f"Q14-{split}-{i}-FULL","QALB14_L1",split,str(i),"FULL_EXPERT_REPAIR",
              srcn,corn,corn,n,idx,[],
              ["QALB human-corrected reference line and official M2 edits."]
            ))
            if n==1:
                st["single_edit_complete"]+=1
                allrows.append(rec(
                  f"Q14-{split}-{i}-SINGLE","QALB14_L1",split,str(i),"SINGLE_EDIT_COMPLETE",
                  srcn,corn,corn,1,[0],[],
                  ["The sole official reference edit reconstructs the full human correction."]
                ))
            if n>=2:
                st["multi_edit_reconstructable"]+=1
                multi_reconstructable+=1
                # Deterministic edit index based on line identity.
                chosen=int(hkey(split,i,"one")[:8],16)%n
                cand1=norm(apply_edits(srcn,edits,[chosen]))
                withheld1=[x for x in idx if x!=chosen]
                allrows.append(rec(
                  f"Q14-{split}-{i}-ONE","QALB14_L1",split,str(i),"ONE_OF_MANY_PARTIAL",
                  srcn,cand1,corn,n,[chosen],withheld1,
                  ["Applied edit is an official human reference edit; other official edits are deliberately withheld."]
                ))
                missing=int(hkey(split,i,"missing")[:8],16)%n
                applied=[x for x in idx if x!=missing]
                cand2=norm(apply_edits(srcn,edits,applied))
                allrows.append(rec(
                  f"Q14-{split}-{i}-ABO","QALB14_L1",split,str(i),"ALL_BUT_ONE_PARTIAL",
                  srcn,cand2,corn,n,applied,[missing],
                  ["All but one official human reference edit are applied; one known reference correction remains."]
                ))
        stats[split]=dict(st)

    # Existing Nahw development targets: source/target correction are already in repository evidence.
    nahw_path=repo/"phase2/arabic_eval/DEVELOPMENT_TARGETS.jsonl"
    if nahw_path.exists():
        nrows=[json.loads(x) for x in nahw_path.read_text(encoding="utf-8").splitlines() if x.strip()]
        for j,x in enumerate(nrows,1):
            src=x.get("source_passage") or x.get("source") or x.get("passage_text")
            terr=x.get("target_error")
            tcorr=x.get("target_correction")
            span=x.get("target_span")
            if not (src and tcorr and span and isinstance(span,list) and len(span)==2):
                continue
            a,b=span
            cand=src[:a]+tcorr+src[b:]
            allrows.append(rec(
              f"NAHW-{x.get('target_id',j)}","NAHW_PHASE2_DEV","development",str(x.get("target_id",j)),
              "NAHW_LOCAL_REFERENCE",src,cand,cand,1,[0],[],
              ["Published/frozen Nahw local correction; reference scope is one target location, not full passage."]
            ))

    caps={
      "FULL_EXPERT_REPAIR":500,
      "EXPERT_KEEP":250,
      "SINGLE_EDIT_COMPLETE":250,
      "ONE_OF_MANY_PARTIAL":500,
      "ALL_BUT_ONE_PARTIAL":500,
      "NAHW_LOCAL_REFERENCE":150
    }
    sample=[]
    available=Counter(r["case_family"] for r in allrows)
    for fam,n in caps.items():
        sample.extend(capped(allrows,fam,n))
    sample.sort(key=lambda r:r["case_id"])

    # Criteria
    changed=sum(stats[s].get("changed_lines",0) for s in stats)
    keep=sum(stats[s].get("keep_lines",0) for s in stats)
    fam_avail=Counter(r["case_family"] for r in allrows)
    criteria={
      "qalb_line_counts_match":all(stats[s]["source_lines"]==stats[s]["corrected_lines"] for s in stats),
      "changed_lines_ge_1000":changed>=1000,
      "keep_lines_ge_100":keep>=100,
      "multi_edit_reconstructable_ge_300":multi_reconstructable>=300,
      "one_of_many_partial_ge_300":fam_avail["ONE_OF_MANY_PARTIAL"]>=300,
      "all_but_one_partial_ge_300":fam_avail["ALL_BUT_ONE_PARTIAL"]>=300,
      "forbidden_split_read":False,
      "raw_qalb_text_persisted":False,
      "provenance_present":all(r.get("evidence_tier") and r.get("corpus") for r in sample)
    }
    ready=all(v is True for k,v in criteria.items() if k!="forbidden_split_read") and criteria["forbidden_split_read"] is False

    manifest=out/"M1A_EXPERT_BOOTSTRAP_HASHED.jsonl"
    manifest.write_text("\n".join(json.dumps(r,ensure_ascii=False,sort_keys=True) for r in sample)+"\n",encoding="utf-8")

    summary={
      "status":"M1A_EXPERT_BOOTSTRAP_DATA_READY" if ready else "M1A_EXPERT_BOOTSTRAP_NOT_READY",
      "date":"2026-09-30",
      "upstream_revision":UPSTREAM_REV,
      "allowed_qalb_splits":["QALB14_L1_TRAIN","QALB14_L1_DEV"],
      "qalb15_read":False,
      "qalb_test_read":False,
      "raw_qalb_text_persisted":False,
      "split_stats":stats,
      "available_case_families":dict(available),
      "persisted_sample_counts":dict(Counter(r["case_family"] for r in sample)),
      "m2_reconstruction_failures":recon_fail,
      "criteria":criteria,
      "data_ready":ready,
      "interpretation":{
        "does_establish":[
          "expert-supported full corrections",
          "expert-supported unchanged lines under QALB protocol",
          "controlled incomplete candidates with known withheld expert edits",
          "local Nahw reference-supported edits"
        ],
        "does_not_establish":[
          "wrongness of non-reference alternatives",
          "scientific fidelity",
          "document integrity",
          "independent human validation of ACAD_PASS project cases",
          "Arabic auto-accept safety"
        ]
      }
    }
    (out/"M1A_EXPERT_BOOTSTRAP_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    # Leakage/persistence guard: no Arabic chars in persisted QALB-derived outputs.
    # Nahw hashes only are persisted too, so the complete manifest must be Arabic-free.
    persisted=manifest.read_text(encoding="utf-8")+(out/"M1A_EXPERT_BOOTSTRAP_SUMMARY.json").read_text(encoding="utf-8")
    if ARABIC_RE.search(persisted):
        raise SystemExit("raw Arabic detected in safe persisted outputs")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if not ready:
        raise SystemExit(2)

if __name__=="__main__":
    main()
