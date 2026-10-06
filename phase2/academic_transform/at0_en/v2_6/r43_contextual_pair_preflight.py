#!/usr/bin/env python3
from __future__ import annotations

import argparse, collections, hashlib, json, math, pathlib
from typing import Any

from transformers import AutoTokenizer

SEED=42
LABELS=["P","I","C","O"]
VALID_BIO={"O","B-P","I-P","B-I","I-I","B-C","I-C","B-O","I-O"}
EXPECTED_TRAIN_SHA="6491a57e5c8639e5bfc3c0326b8501869fccab655a1ed571b75a772dc1c70a5e"
EXPECTED_EMPTY={"O":5,"I-I":5,"I-P":6,"I-O":1}
MAX_WIDTH=64

def sha_bytes(b:bytes)->str:
    return hashlib.sha256(b).hexdigest()

def sha_text(s:str)->str:
    return sha_bytes(s.encode("utf-8"))

def file_sha(p:pathlib.Path)->str:
    return sha_bytes(p.read_bytes())

def dump(path:pathlib.Path,obj:Any):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def parse_train(path:pathlib.Path):
    docs=[]; doc=[]; toks=[]; tags=[]; empty=collections.Counter()
    malformed_lines=[]
    def flush_sent():
        nonlocal toks,tags,doc
        if toks:
            doc.append((toks,tags))
            toks=[]; tags=[]
    def flush_doc():
        nonlocal doc,docs
        flush_sent()
        if doc:
            docs.append(doc); doc=[]
    for ln,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if raw.startswith("-DOCSTART-"):
            flush_doc()
            continue
        # Important: a literal empty-surface row begins with TAB and must NOT
        # be mistaken for a sentence separator.
        if raw=="":
            flush_sent()
            continue
        if "\t" in raw:
            tok,tag=raw.split("\t",1)
        else:
            parts=raw.rsplit(None,1)
            if len(parts)!=2:
                malformed_lines.append({"line":ln,"raw":raw})
                continue
            tok,tag=parts
        if tag not in VALID_BIO:
            malformed_lines.append({"line":ln,"raw":raw,"reason":"unknown_tag"})
            continue
        if tok=="":
            empty[tag]+=1
            continue
        toks.append(tok); tags.append(tag)
    flush_doc()
    return docs,dict(sorted(empty.items())),malformed_lines

def bio_spans(tags,initial_continuation_type=None):
    spans=[]; malformed=[]; cur=None
    prev="O"
    for i,tag in enumerate(tags):
        if tag=="O":
            if cur is not None:
                typ,s=cur; spans.append((typ,s,i)); cur=None
            prev=tag; continue
        pref,typ=tag.split("-",1)
        if pref=="B":
            if cur is not None:
                ctyp,s=cur; spans.append((ctyp,s,i))
            cur=(typ,i)
        elif pref=="I":
            if i==0 and initial_continuation_type==typ:
                # Source continuation segment: raw label remains I-X.
                cur=(typ,0)
            else:
                valid_prev=(prev==f"B-{typ}" or prev==f"I-{typ}")
                if not valid_prev:
                    malformed.append({"index":i,"tag":tag,"previous":prev})
                    if cur is not None:
                        ctyp,s=cur; spans.append((ctyp,s,i))
                    cur=(typ,i)
                elif cur is None:
                    malformed.append({"index":i,"tag":tag,"previous":prev,"reason":"missing_active_span"})
                    cur=(typ,i)
        prev=tag
    if cur is not None:
        typ,s=cur; spans.append((typ,s,len(tags)))
    return spans,malformed

def spans_for_sentence(doc,si):
    tokens,tags=doc[si]
    initial_type=None
    continuation=None
    prefix_bad=[]
    if tags and tags[0].startswith("I-"):
        typ=tags[0][2:]
        prev_last=None
        if si>0 and doc[si-1][1]:
            prev_last=doc[si-1][1][-1]
        if prev_last in (f"B-{typ}",f"I-{typ}"):
            initial_type=typ
            continuation={"sentence":si,"tag":tags[0],"previous_sentence_last_tag":prev_last}
        else:
            prefix_bad.append({"index":0,"tag":tags[0],"previous_sentence_last_tag":prev_last,
                               "reason":"invalid_cross_example_continuation"})
    spans,bad=bio_spans(tags,initial_type)
    return spans,prefix_bad+bad,continuation

def canonical_doc_tokens(doc):
    return json.dumps([s[0] for s in doc],ensure_ascii=False,separators=(",",":"))

def canonical_doc_tags(doc):
    return json.dumps([s[1] for s in doc],ensure_ascii=False,separators=(",",":"))

def gold_inventory(docs):
    doc_rows=[]; all_gold=[]; malformed_bio=[]; continuations=[]
    coord_conflicts=[]
    maxw=0
    class_tot=collections.Counter()
    for di,doc in enumerate(docs):
        cc=collections.Counter(); ntok=0
        for si,(tokens,tags) in enumerate(doc):
            ntok+=len(tokens)
            spans,bad,cont=spans_for_sentence(doc,si)
            if cont is not None:
                continuations.append({"document":di,**cont})
            for x in bad:
                malformed_bio.append({"document":di,"sentence":si,**x})
            seen={}
            for typ,s,e in spans:
                key=(s,e)
                if key in seen and seen[key]!=typ:
                    coord_conflicts.append({"document":di,"sentence":si,"start":s,"end":e,
                                            "classes":sorted({seen[key],typ})})
                seen[key]=typ
                w=e-s; maxw=max(maxw,w)
                cc[typ]+=1; class_tot[typ]+=1
                all_gold.append({"document":di,"sentence":si,"type":typ,"start":s,"end":e,
                                 "tokens":tokens[s:e]})
        token_canon=canonical_doc_tokens(doc)
        tag_canon=canonical_doc_tags(doc)
        doc_rows.append({
            "document":di,
            "token_sha256":sha_text(token_canon),
            "token_tag_sha256":sha_text(token_canon+"\n"+tag_canon),
            "sentences":len(doc),
            "tokens":ntok,
            "gold_counts":{c:int(cc[c]) for c in LABELS},
        })
    return doc_rows,all_gold,malformed_bio,continuations,coord_conflicts,maxw,dict(class_tot)

def build_groups(doc_rows):
    by=collections.defaultdict(list)
    for r in doc_rows:
        by[r["token_sha256"]].append(r)
    groups=[]
    tag_conflicts=[]
    for h,rows in sorted(by.items()):
        tag_hashes=sorted({r["token_tag_sha256"] for r in rows})
        if len(tag_hashes)>1:
            tag_conflicts.append({"token_sha256":h,"documents":[r["document"] for r in rows],
                                  "token_tag_sha256":tag_hashes})
        cc=collections.Counter()
        for r in rows:
            cc.update(r["gold_counts"])
        groups.append({
            "group_token_sha256":h,
            "documents":[r["document"] for r in rows],
            "document_count":len(rows),
            "gold_counts":{c:int(cc[c]) for c in LABELS},
            "tie_sha256":sha_text(f"{SEED}|{h}")
        })
    return groups,tag_conflicts

def split_groups(groups,total_docs,class_tot):
    target_docs=round(.20*total_docs)
    target={c:.20*class_tot[c] for c in LABELS}
    selected=[]
    remain=list(groups)
    cur_docs=0; cur=collections.Counter()
    def objective(g):
        nd=cur_docs+g["document_count"]
        val=((nd-target_docs)/max(1.0,target_docs))**2
        for c in LABELS:
            nv=cur[c]+g["gold_counts"][c]
            val+=((nv-target[c])/max(1.0,target[c]))**2
        return val
    while remain and cur_docs<target_docs:
        remain.sort(key=lambda g:(objective(g),g["tie_sha256"]))
        g=remain.pop(0)
        selected.append(g)
        cur_docs+=g["document_count"]
        cur.update(g["gold_counts"])
    sel_groups={g["group_token_sha256"] for g in selected}
    manifest=[]
    for g in groups:
        part="SELECT" if g["group_token_sha256"] in sel_groups else "FIT"
        manifest.append({
            "group_token_sha256":g["group_token_sha256"],
            "documents":g["documents"],
            "partition":part,
            "document_count":g["document_count"],
            "gold_counts":g["gold_counts"],
        })
    fit_docs=set(); sel_docs=set()
    for m in manifest:
        (sel_docs if m["partition"]=="SELECT" else fit_docs).update(m["documents"])
    return manifest,fit_docs,sel_docs,target_docs,target

def span_maps(docs,docset):
    # gold coordinate maps + positive rows using frozen continuation-segment semantics
    gold_by_sent={}
    positives=[]
    for di in sorted(docset):
        doc=docs[di]
        for si,(tokens,tags) in enumerate(doc):
            spans,bad,_=spans_for_sentence(doc,si)
            if bad:
                raise RuntimeError(f"unexpected BIO violation in span_maps: doc={di} sent={si} {bad[:3]}")
            gm={(s,e):typ for typ,s,e in spans}
            gold_by_sent[(di,si)]=gm
            for typ,s,e in spans:
                positives.append({"document":di,"sentence":si,"start":s,"end":e,
                                  "label":typ,"tokens":tokens[s:e],"kind":"GOLD"})
    return gold_by_sent,positives

def keyhash(*parts):
    return sha_text("|".join(map(str,parts)))

def overlap(a,b,c,d):
    return max(a,c)<min(b,d)

def static_negative_candidates(docs,fit_docs,gold_by_sent,positives):
    local_raw=[]; comp_raw=[]; bg_reserved=[]
    comp_same=0; comp_diff=0
    bg_available=0

    # index gold per sentence
    bysent=collections.defaultdict(list)
    for p in positives: bysent[(p["document"],p["sentence"])].append(p)

    for p in positives:
        di,si,s,e,typ=p["document"],p["sentence"],p["start"],p["end"],p["label"]
        tokens=docs[di][si][0]; n=len(tokens)
        golds=gold_by_sent[(di,si)]
        # Up to two local perturbations.
        pool=[]
        for ds in (-2,-1,0,1,2):
            for de in (-2,-1,0,1,2):
                if ds==0 and de==0: continue
                a=s+ds; b=e+de
                if a<0 or b>n or b<=a or b-a>MAX_WIDTH: continue
                if (a,b) in golds: continue
                h=keyhash(SEED,di,si,typ,s,e,a,b,"LOCAL")
                pool.append((h,a,b))
        pool.sort()
        for h,a,b in pool[:2]:
            local_raw.append({"document":di,"sentence":si,"start":a,"end":b,
                              "label":"NONE","kind":"LOCAL","source":(s,e,typ)})

        # At most one composite, preferring same/different class by frozen hash parity.
        same=[]; diff=[]
        for q in bysent[(di,si)]:
            if q is p: continue
            qtyp,qs,qe=q["label"],q["start"],q["end"]
            for a,b in ((s,qe),(qs,e)):
                if a<0 or b>n or b<=a or b-a>MAX_WIDTH: continue
                if (a,b) in golds: continue
                h=keyhash(SEED,di,si,typ,s,e,qtyp,qs,qe,a,b,"COMPOSITE")
                row=(h,a,b,qtyp)
                (same if qtyp==typ else diff).append(row)
        same.sort(); diff.sort()
        prefer_same=(int(keyhash(SEED,di,si,typ,s,e,"PREF")[-1],16)%2==0)
        chosen=(same if prefer_same else diff) or (diff if prefer_same else same)
        if chosen:
            h,a,b,qtyp=chosen[0]
            k="COMPOSITE_SAME" if qtyp==typ else "COMPOSITE_DIFFERENT"
            comp_raw.append({"document":di,"sentence":si,"start":a,"end":b,
                             "label":"NONE","kind":k,"source":(s,e,typ)})
            if qtyp==typ: comp_same+=1
            else: comp_diff+=1

        # Reserve one deterministic length-matched background fallback candidate.
        w=e-s
        bpool=[]
        for a in range(0,n-w+1):
            b=a+w
            if (a,b) in golds: continue
            if any(overlap(a,b,gs,ge) for (gs,ge) in golds): continue
            h=keyhash(SEED,di,si,typ,s,e,a,b,"BACKGROUND_FALLBACK")
            bpool.append((h,a,b))
        bpool.sort()
        if bpool:
            bg_available+=1
            h,a,b=bpool[0]
            bg_reserved.append({"document":di,"sentence":si,"start":a,"end":b,
                                "label":"NONE","kind":"BACKGROUND_FALLBACK","source":(s,e,typ)})

    # Deduplicate static local+composite with gold precedence. Background is RESERVED
    # separately because it is used only when future native FIT-error slot is absent.
    bycoord={}
    provenance=collections.defaultdict(set)
    for row in local_raw+comp_raw:
        k=(row["document"],row["sentence"],row["start"],row["end"])
        if k in gold_by_sent[(row["document"],row["sentence"])]:
            continue
        provenance[k].add(row["kind"])
        bycoord[k]=row
    static=[]
    for k in sorted(bycoord):
        row=dict(bycoord[k])
        row["provenance"]=sorted(provenance[k])
        static.append(row)

    bg_bycoord={}
    for row in bg_reserved:
        k=(row["document"],row["sentence"],row["start"],row["end"])
        if k in gold_by_sent[(row["document"],row["sentence"])]:
            continue
        bg_bycoord[k]=row
    bg_unique=[bg_bycoord[k] for k in sorted(bg_bycoord)]

    return {
        "local_raw":local_raw,
        "composite_raw":comp_raw,
        "background_reserved_raw":bg_reserved,
        "static_unique":static,
        "background_reserved_unique":bg_unique,
        "composite_same_raw":comp_same,
        "composite_different_raw":comp_diff,
        "background_available_source_gold":bg_available,
    }

def text_key(tokens):
    return "\u241f".join(tokens)

def collision_audit(docs,positives,none_rows,tokenizer):
    gold_text=collections.defaultdict(set)
    gold_ids=collections.defaultdict(set)
    none_text=collections.defaultdict(set)
    none_ids=collections.defaultdict(set)

    def ids(tokens):
        return tuple(tokenizer(tokens,is_split_into_words=True,truncation=False)["input_ids"])

    for p in positives:
        tk=text_key(p["tokens"]); gold_text[tk].add(p["label"]); gold_ids[ids(p["tokens"])].add(p["label"])
    for n in none_rows:
        tokens=docs[n["document"]][n["sentence"]][0][n["start"]:n["end"]]
        tk=text_key(tokens); none_text[tk].add("NONE"); none_ids[ids(tokens)].add("NONE")

    multi_gold_text=[{"tokens":k,"labels":sorted(v)} for k,v in gold_text.items() if len(v)>1]
    multi_gold_ids=[{"input_ids_sha256":sha_text(json.dumps(k)),"labels":sorted(v)} for k,v in gold_ids.items() if len(v)>1]
    gold_none_text=[]
    for k,gv in gold_text.items():
        if k in none_text:
            gold_none_text.append({"tokens":k,"gold_labels":sorted(gv),"also_none":True})
    gold_none_ids=[]
    for k,gv in gold_ids.items():
        if k in none_ids:
            gold_none_ids.append({"input_ids_sha256":sha_text(json.dumps(k)),"gold_labels":sorted(gv),"also_none":True})

    return {
        "gold_token_strings_with_multiple_entity_classes":len(multi_gold_text),
        "gold_tokenizer_ids_with_multiple_entity_classes":len(multi_gold_ids),
        "gold_token_strings_also_seen_as_synthetic_NONE":len(gold_none_text),
        "gold_tokenizer_ids_also_seen_as_synthetic_NONE":len(gold_none_ids),
        "examples":{
            "multi_gold_token_strings":multi_gold_text[:25],
            "gold_and_none_token_strings":gold_none_text[:25],
        }
    }

def partition_stats(docs,doc_rows,docset):
    rows=[r for r in doc_rows if r["document"] in docset]
    cc=collections.Counter()
    for r in rows: cc.update(r["gold_counts"])
    return {
        "documents":len(rows),
        "sentences":sum(r["sentences"] for r in rows),
        "tokens":sum(r["tokens"] for r in rows),
        "gold_counts":{c:int(cc[c]) for c in LABELS},
        "gold_total":int(sum(cc.values())),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--tokenizer-dir",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)

    if file_sha(args.train)!=EXPECTED_TRAIN_SHA:
        raise RuntimeError("TRAIN hash mismatch")

    docs,empty,bad_lines=parse_train(args.train)
    if bad_lines: raise RuntimeError(f"malformed source lines: {bad_lines[:5]}")
    if empty!=EXPECTED_EMPTY: raise RuntimeError(f"empty-surface mismatch: {empty}")

    doc_rows,all_gold,bad_bio,continuations,coord_conf,maxw,class_tot=gold_inventory(docs)
    if bad_bio: raise RuntimeError(f"malformed BIO continuity: {bad_bio[:10]}")
    cont_counts=dict(sorted(collections.Counter(x["tag"] for x in continuations).items()))
    expected_cont={"I-I":2,"I-O":1,"I-P":8}
    if len(continuations)!=11 or cont_counts!=expected_cont:
        raise RuntimeError(f"continuation inventory mismatch: n={len(continuations)} counts={cont_counts}")
    if coord_conf: raise RuntimeError(f"gold coordinate conflicts: {coord_conf[:10]}")
    if maxw>MAX_WIDTH: raise RuntimeError(f"gold width {maxw}>{MAX_WIDTH}")
    if len(docs)!=400: raise RuntimeError(f"document count changed: {len(docs)}")
    if sum(len(d) for d in docs)!=1576: raise RuntimeError("sentence count changed")
    if len(all_gold)!=3011: raise RuntimeError(f"gold segment count changed: {len(all_gold)}")

    groups,tag_conflicts=build_groups(doc_rows)
    manifest,fit_docs,sel_docs,target_docs,target=split_groups(groups,len(docs),class_tot)

    # Verify no group crosses partitions.
    docpart={}
    for m in manifest:
        for d in m["documents"]:
            if d in docpart and docpart[d]!=m["partition"]: raise RuntimeError("document crossed partitions")
            docpart[d]=m["partition"]
    if fit_docs & sel_docs: raise RuntimeError("FIT/SELECT overlap")

    fit_stats=partition_stats(docs,doc_rows,fit_docs)
    sel_stats=partition_stats(docs,doc_rows,sel_docs)
    for part,st in (("FIT",fit_stats),("SELECT",sel_stats)):
        for c in LABELS:
            if st["gold_counts"][c]<=0: raise RuntimeError(f"{part} lacks {c}")
    for c in LABELS:
        if sel_stats["gold_counts"][c]<20:
            raise RuntimeError(f"SELECT has <20 {c} spans: {sel_stats['gold_counts'][c]}")

    target_dev={
        "documents_target":target_docs,
        "class_target_20pct":{c:target[c] for c in LABELS},
        "select_class_relative_deviation":{
            c:(sel_stats["gold_counts"][c]-target[c])/target[c] if target[c] else None for c in LABELS
        }
    }

    fit_goldmap,fit_pos=span_maps(docs,fit_docs)
    neg=static_negative_candidates(docs,fit_docs,fit_goldmap,fit_pos)

    tokenizer=AutoTokenizer.from_pretrained(args.tokenizer_dir,local_files_only=True,use_fast=True)

    # Collision audit uses static local+composite plus the reserved background fallback
    # because these are all prospectively available NONE constructions.
    fit_none_for_audit=neg["static_unique"]+neg["background_reserved_unique"]
    fit_collisions=collision_audit(docs,fit_pos,fit_none_for_audit,tokenizer)

    # Whole-TRAIN gold-only ambiguity audit.
    _,all_pos=span_maps(docs,set(range(len(docs))))
    all_collisions=collision_audit(docs,all_pos,[],tokenizer)

    # Static synthetic coordinate collisions after gold precedence.
    static_coords={(r["document"],r["sentence"],r["start"],r["end"]) for r in neg["static_unique"]}
    gold_coords={(p["document"],p["sentence"],p["start"],p["end"]) for p in fit_pos}
    synthetic_gold_collision=len(static_coords & gold_coords)

    # Parameter counts frozen by design.
    projection=5*(768*128+128)
    edge_vectors=2*768
    width_embedding=64*16
    mlp=(656*128+128)+(128*5+5)
    h0=projection+edge_vectors+width_embedding+mlp
    biaffine=5*129*129
    h1=h0+biaffine

    # Deterministic manifests.
    split_payload={
        "seed":SEED,
        "algorithm":"frozen_greedy_grouped_multicount_objective_v1",
        "source_train_sha256":EXPECTED_TRAIN_SHA,
        "entries":sorted(manifest,key=lambda x:x["group_token_sha256"])
    }
    split_sha=sha_text(json.dumps(split_payload,sort_keys=True,separators=(",",":")))
    split_payload["manifest_sha256"]=split_sha
    dump(args.out/"R43_FIT_SELECT_MANIFEST.json",split_payload)

    synthetic_manifest={
        "fit_positive_coordinates":[
            {k:p[k] for k in ("document","sentence","start","end","label")} for p in
            sorted(fit_pos,key=lambda x:(x["document"],x["sentence"],x["start"],x["end"],x["label"]))
        ],
        "static_none_coordinates":[
            {k:r[k] for k in ("document","sentence","start","end","kind","provenance")} for r in neg["static_unique"]
        ],
        "reserved_background_fallback":[
            {k:r[k] for k in ("document","sentence","start","end","kind")} for r in neg["background_reserved_unique"]
        ],
        "native_fit_error_slot":"DEFERRED_UNTIL_FIT_ONLY_B_REPLICA_EXISTS; algorithm frozen in design V1"
    }
    syn_sha=sha_text(json.dumps(synthetic_manifest,sort_keys=True,separators=(",",":")))
    synthetic_manifest["manifest_sha256"]=syn_sha
    dump(args.out/"R43_STATIC_EXAMPLE_MANIFEST.json",synthetic_manifest)

    summary={
        "state":"R43_CONTEXTUAL_PAIR_PREFLIGHT_PASS",
        "source":{
            "train_sha256":EXPECTED_TRAIN_SHA,
            "documents":len(docs),
            "sentences":sum(len(d) for d in docs),
            "tokens":sum(len(s[0]) for d in docs for s in d),
            "empty_surface_removed":empty,
            "gold_counts":{c:int(class_tot.get(c,0)) for c in LABELS},
            "gold_total":len(all_gold),
            "max_gold_span_width_words":maxw,
        },
        "document_grouping":{
            "duplicate_groups_total":sum(1 for g in groups if g["document_count"]>1),
            "documents_in_duplicate_groups":sum(g["document_count"] for g in groups if g["document_count"]>1),
            "token_identical_tag_conflict_groups":len(tag_conflicts),
            "tag_conflict_examples":tag_conflicts[:20],
        },
        "split":{
            "manifest_sha256":split_sha,
            "target":target_dev,
            "FIT":fit_stats,
            "SELECT":sel_stats,
            "overlap_documents":len(fit_docs&sel_docs),
        },
        "flat_representation":{
            "within_or_cross_example_invalid_bio_continuations":len(bad_bio),
            "source_continuation_segments":len(continuations),
            "source_continuation_tag_counts":cont_counts,
            "source_continuation_inventory":continuations,
            "continuation_semantics":"RAW I-X PRESERVED; INITIAL I-X STARTS AN EXAMPLE-LOCAL CONTINUATION SEGMENT ONLY WHEN PREVIOUS EXAMPLE IN SAME DOCUMENT ENDS SAME TYPE",
            "gold_coordinate_class_conflicts":len(coord_conf),
            "max_width_ok":maxw<=MAX_WIDTH,
        },
        "static_negative_preflight":{
            "fit_gold_positives":len(fit_pos),
            "local_raw":len(neg["local_raw"]),
            "composite_raw":len(neg["composite_raw"]),
            "composite_same_raw":neg["composite_same_raw"],
            "composite_different_raw":neg["composite_different_raw"],
            "static_local_composite_unique":len(neg["static_unique"]),
            "background_fallback_source_gold_with_candidate":neg["background_available_source_gold"],
            "background_fallback_unique_reserved":len(neg["background_reserved_unique"]),
            "synthetic_gold_coordinate_collisions_after_precedence":synthetic_gold_collision,
            "static_example_manifest_sha256":syn_sha,
            "native_fit_error_examples_materialized":False,
        },
        "input_label_collision_audit":{
            "complete_train_gold_only":all_collisions,
            "fit_gold_vs_prospective_synthetic_none":fit_collisions,
        },
        "architecture_parameter_counts":{
            "shared_contextual_projection_plus_edges_plus_width":projection+edge_vectors+width_embedding,
            "H0_total_trainable_head_parameters":h0,
            "H1_biaffine_additional_parameters":biaffine,
            "H1_total_trainable_head_parameters":h1,
            "H1_minus_H0":biaffine,
        },
        "ancestry_plan":{
            "global_B_C_artifacts_allowed_for_SELECT":False,
            "future_fit_only_B_epochs":10,
            "future_fit_only_boundary_epochs":3,
            "future_fit_only_type_epochs":3,
            "ancestor_checkpoint_selection":"FINAL_FIXED_EPOCH_ONLY",
            "H0_H1_encoder":"FROZEN_FINAL_FIT_ONLY_BOUNDARY_ENCODER",
        },
        "access_guards":{
            "train_only":True,
            "historical_dev_read":False,
            "fold1_test_read":False,
            "other_folds_read":False,
            "external_EBM_COVID_AD_tests_read":False,
            "factpico_used":False,
            "consumed_60_rct_holdout_used":False,
            "scientific_training_performed":False,
        },
        "next_action":"FREEZE_PREFLIGHT_AND_STOP_BEFORE_ANY_FIT_SELECT_TRAINING"
    }
    dump(args.out/"R43_CONTEXTUAL_PAIR_PREFLIGHT.json",summary)
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
