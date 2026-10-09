#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,csv,difflib,hashlib,json,pathlib,re,tarfile,time,unicodedata,urllib.parse,urllib.request

NCBI_BASE="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def norm_title(s):
    s=unicodedata.normalize("NFKC",s).casefold()
    return " ".join(re.findall(r"[a-z0-9]+",s))

def lexicalize_tokens(tokens):
    return re.findall(r"[a-z0-9]+",unicodedata.normalize("NFKC"," ".join(tokens)).casefold())

def parse_mod_docs(path):
    docs=[]; cur=[]; started=False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            if started: docs.append(cur)
            cur=[]; started=True; continue
        if not started or not line.strip(): continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"): continue
        cur.append(line.split("\t")[0])
    if started: docs.append(cur)
    return docs

def parse_bids_docs(path):
    docs=[]; blocks=[]; cur=[]; started=False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            if started:
                if cur: blocks.append(cur)
                docs.append(blocks)
            blocks=[]; cur=[]; started=True; continue
        if not started: continue
        if not line.strip():
            if cur: blocks.append(cur); cur=[]
            continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"): continue
        cur.append(line.split("\t")[0])
    if started:
        if cur: blocks.append(cur)
        docs.append(blocks)
    return docs

def canonical_doc(blocks):
    toks=[t for b in blocks for t in b]
    s=unicodedata.normalize("NFC"," ".join(toks))
    return " ".join(s.split())

def extract_title(blocks):
    for b in blocks:
        low=[x.casefold() for x in b]
        if low and low[0]=="title":
            start=1
            if len(b)>1 and b[1]==":": start=2
            t=" ".join(b[start:]).strip()
            if t: return t
    # fail closed: no heuristic title from arbitrary text
    return None

def find_original_tokens(root):
    out={}
    for p in root.rglob("*.tokens"):
        if p.stem.isdigit():
            lex=lexicalize_tokens(p.read_text(encoding="utf-8",errors="replace").split())
            if len(lex)>=7: out[p.stem]=lex
    return out

def ngrams(seq,n=7):
    return [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]

def map_mod_to_pmids(mod_docs,originals):
    inv=collections.defaultdict(set)
    for pmid,toks in originals.items():
        for g in set(ngrams(toks,7)): inv[g].add(pmid)
    mapped={}
    for di,doc in enumerate(mod_docs):
        grams=set(ngrams(lexicalize_tokens(doc),7))
        counts=collections.Counter()
        for g in grams:
            for pmid in inv.get(g,()): counts[pmid]+=1
        ranked=counts.most_common()
        best=ranked[0][1] if ranked else 0
        second=ranked[1][1] if len(ranked)>1 else 0
        best_ids=[p for p,v in ranked if v==best] if best else []
        coverage=best/max(1,len(grams))
        if len(best_ids)==1 and best>=12 and best-second>=6 and coverage>=.12:
            mapped[di]=best_ids[0]
    return mapped

def http_json(url,tries=4):
    last=None
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"ACAD_PASS/1.0 provenance-audit"})
            with urllib.request.urlopen(req,timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last=e; time.sleep(1.5*(i+1))
    raise RuntimeError(f"NCBI request failed after retries: {type(last).__name__}")

def esearch_title(title):
    term=f'"{title}"[Title]'
    q=urllib.parse.urlencode({"db":"pubmed","term":term,"retmode":"json","retmax":"20","tool":"ACAD_PASS"})
    d=http_json(f"{NCBI_BASE}/esearch.fcgi?{q}")
    ids=d.get("esearchresult",{}).get("idlist",[])
    if not ids:
        # fallback remains title-field constrained; acceptance still requires exact normalized ESummary title
        q=urllib.parse.urlencode({"db":"pubmed","term":f"{title}[Title]","retmode":"json","retmax":"20","tool":"ACAD_PASS"})
        d=http_json(f"{NCBI_BASE}/esearch.fcgi?{q}")
        ids=d.get("esearchresult",{}).get("idlist",[])
    return ids

def esummary(ids):
    if not ids: return {}
    q=urllib.parse.urlencode({"db":"pubmed","id":",".join(ids),"retmode":"json","tool":"ACAD_PASS"})
    d=http_json(f"{NCBI_BASE}/esummary.fcgi?{q}")
    result=d.get("result",{})
    return {i:result.get(i,{}) for i in ids}

def resolve_title(title):
    ids=esearch_title(title)
    if not ids: return None,"NO_CANDIDATE"
    summaries=esummary(ids)
    nt=norm_title(title)
    exact=[]
    for i in ids:
        st=summaries.get(i,{}).get("title","")
        if norm_title(st)==nt:
            exact.append(i)
    if len(exact)==1: return exact[0],"EXACT_NORMALIZED_TITLE"
    if len(exact)>1: return None,"MULTIPLE_EXACT_TITLE"
    # no fuzzy acceptance; report unresolved
    return None,"NO_EXACT_TITLE"

def load_target_unique(root,corpus):
    docs_by_hash={}
    test_hashes=set()
    for fold in range(1,6):
        for role in ("train","dev","test"):
            for blocks in parse_bids_docs(root/f"data/{corpus}/fold{fold}/{role}.txt"):
                txt=canonical_doc(blocks)
                hh=hashlib.sha256(txt.encode()).hexdigest()
                docs_by_hash.setdefault(hh,blocks)
                if role=="test": test_hashes.add(hh)
    return docs_by_hash,test_hashes

def load_evidence_pmids(root):
    out={}
    for fn in ("500RCT-CoNLL.tsv","140EBMNLP-CoNLL.tsv"):
        s=set()
        with open(root/fn,encoding="utf-8",newline="") as f:
            r=csv.DictReader(f,delimiter="\t")
            for row in r:
                v=(row.get("PMID") or row.get("pmid") or "").strip()
                if v.isdigit(): s.add(v)
        out[fn]=s
    return out

def pico_pmids(root):
    return {p.stem for p in (root/"pico_corpus_brat_annotated_files").glob("*.txt") if p.stem.isdigit()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bids",type=pathlib.Path,required=True)
    ap.add_argument("--ebm-archive",type=pathlib.Path,required=True)
    ap.add_argument("--r44-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--pico",type=pathlib.Path,required=True)
    ap.add_argument("--evidence",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()
    a.work.mkdir(parents=True,exist_ok=True)
    with tarfile.open(a.ebm_archive,"r:gz") as tf: tf.extractall(a.work/"ebm",filter="data")
    originals=find_original_tokens(a.work/"ebm")
    mod_docs=parse_mod_docs(a.bids/"data/EBM-NLPmod/fold1/train.txt")
    mapped=map_mod_to_pmids(mod_docs,originals)
    m=json.loads(a.r44_manifest.read_text())
    hist_groups={
      "DESIGN":set(m["design_documents"]),
      "VERIFY_INTERNAL":set(m["verify_internal_documents"]),
      "OLD_SELECT":set(m["excluded_old_select_documents"])
    }
    protected_pmids={name:{mapped[i] for i in inds if i in mapped} for name,inds in hist_groups.items()}

    targets={}
    cache={}
    resolution_reasons=collections.Counter()
    for corpus in ("AD","COVID-19"):
        docs,test_hashes=load_target_unique(a.bids,corpus)
        if len(docs)!=150:
            raise RuntimeError(f"{corpus} expected 150 canonical docs got {len(docs)}")
        resolved={}
        no_title=0
        for k,(hh,blocks) in enumerate(sorted(docs.items())):
            title=extract_title(blocks)
            if not title:
                no_title+=1; resolution_reasons[f"{corpus}:NO_TITLE"]+=1; continue
            nt=norm_title(title)
            if nt in cache:
                pmid,reason=cache[nt]
            else:
                pmid,reason=resolve_title(title)
                cache[nt]=(pmid,reason)
                time.sleep(.36)  # <= 3 requests/s without API key
            resolution_reasons[f"{corpus}:{reason}"]+=1
            if pmid: resolved[hh]=pmid
        targets[corpus]={"docs":docs,"test_hashes":test_hashes,"resolved":resolved,"no_title":no_title}

    pico=pico_pmids(a.pico)
    ev=load_evidence_pmids(a.evidence)
    report_targets={}
    for corpus,x in targets.items():
        all_pm=set(x["resolved"].values())
        test_pm={x["resolved"][h] for h in x["test_hashes"] if h in x["resolved"]}
        comps={}
        for name,pp in protected_pmids.items():
            comps[name]={
              "whole_shared_pmid_count":len(all_pm&pp),
              "test_union_shared_pmid_count":len(test_pm&pp)
            }
        comps["PICO_CORPUS"]={
          "whole_shared_pmid_count":len(all_pm&pico),
          "test_union_shared_pmid_count":len(test_pm&pico)
        }
        for fn,s in ev.items():
            comps[f"EVIDENCEOUTCOMES_{fn}"]={
              "whole_shared_pmid_count":len(all_pm&s),
              "test_union_shared_pmid_count":len(test_pm&s)
            }
        report_targets[corpus]={
          "canonical_documents":150,
          "resolved_exact_title_pmids":len(x["resolved"]),
          "resolution_fraction":len(x["resolved"])/150,
          "official_test_union_documents":len(x["test_hashes"]),
          "resolved_test_union_pmids":len(test_pm),
          "test_resolution_fraction":len(test_pm)/len(x["test_hashes"]),
          "duplicate_resolved_pmid_assignments":len(x["resolved"])-len(all_pm),
          "overlap_counts":comps
        }

    adpm=set(targets["AD"]["resolved"].values())
    cvpm=set(targets["COVID-19"]["resolved"].values())
    out={
      "state":"FEDERATION_PUBLIC_TARGET_PMID_CUSTODY_AUDIT_PASS",
      "targets":report_targets,
      "ad_covid_shared_resolved_pmid_count":len(adpm&cvpm),
      "resolution_reason_counts":dict(sorted(resolution_reasons.items())),
      "historical_mapping_coverage":{k:{"mapped_pmids":len(v),"documents":len(hist_groups[k])} for k,v in protected_pmids.items()},
      "output_contains_pmids":False,
      "output_contains_titles":False,
      "output_contains_raw_text":False,
      "output_contains_gold_labels":False,
      "limitations":[
        "Only exact normalized PubMed-title matches are accepted; unresolved titles remain unresolved.",
        "Same PMID exclusion does not by itself prove absence of same-trial-family publications.",
        "Historical protected PMID coverage remains partial.",
        "Registry and exact-text audits remain complementary evidence."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
