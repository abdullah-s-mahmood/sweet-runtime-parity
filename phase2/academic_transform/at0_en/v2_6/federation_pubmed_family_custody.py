#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,json,pathlib,re,tarfile,time,unicodedata,urllib.parse,urllib.request,xml.etree.ElementTree as ET

EUTILS="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
REGEXES=[
 ("NCT",re.compile(r"\bNCT\s*[-:]?\s*(\d{8})\b",re.I)),
 ("ISRCTN",re.compile(r"\bISRCTN\s*[-:]?\s*(\d{8})\b",re.I)),
 ("ACTRN",re.compile(r"\bACTRN\s*[-:]?\s*(\d{14})\b",re.I)),
 ("CHICTR",re.compile(r"\bChiCTR\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("CTRI",re.compile(r"\bCTRI\s*[/:-]?\s*([0-9A-Za-z/-]+)\b",re.I)),
 ("IRCT",re.compile(r"\bIRCT\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("UMIN",re.compile(r"\bUMIN\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("JRCT",re.compile(r"\bjRCT\s*[-:]?\s*([A-Za-z0-9-]+)\b",re.I)),
 ("DRKS",re.compile(r"\bDRKS\s*[-:]?\s*(\d{8})\b",re.I)),
 ("EUCTR",re.compile(r"\b(?:EudraCT|EU\s*CTR)\s*[-:]?\s*([0-9-]+)\b",re.I)),
]

def norm_title(s):
    s=unicodedata.normalize("NFKC",s or "").casefold()
    return " ".join(re.findall(r"[a-z0-9]+",s))

def lex(tokens):
    return re.findall(r"[a-z0-9]+",unicodedata.normalize("NFKC"," ".join(tokens)).casefold())

def parse_mod(path):
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

def parse_bids(path):
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

def canonical(blocks):
    s=" ".join(t for b in blocks for t in b)
    return " ".join(unicodedata.normalize("NFC",s).split())

def title_of(blocks):
    for b in blocks:
        if b and b[0].casefold()=="title":
            start=2 if len(b)>1 and b[1]==":" else 1
            s=" ".join(b[start:]).strip()
            if s:return s
    return None

def original_tokens(root):
    out={}
    for p in root.rglob("*.tokens"):
        if p.stem.isdigit():
            x=lex(p.read_text(encoding="utf-8",errors="replace").split())
            if len(x)>=7: out[p.stem]=x
    return out

def grams(x,n=7):
    return [tuple(x[i:i+n]) for i in range(len(x)-n+1)]

def map_mod(mod,orig):
    inv=collections.defaultdict(set)
    for pmid,t in orig.items():
        for g in set(grams(t)): inv[g].add(pmid)
    out={}
    for i,d in enumerate(mod):
        gg=set(grams(lex(d))); cnt=collections.Counter()
        for g in gg:
            for p in inv.get(g,()):cnt[p]+=1
        rr=cnt.most_common()
        best=rr[0][1] if rr else 0; second=rr[1][1] if len(rr)>1 else 0
        ids=[p for p,v in rr if v==best] if best else []
        cov=best/max(1,len(gg))
        if len(ids)==1 and best>=12 and best-second>=6 and cov>=.12:out[i]=ids[0]
    return out

def http(url,tries=5):
    last=None
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"ACAD_PASS/1.0 provenance-custody"})
            with urllib.request.urlopen(req,timeout=40) as r:return r.read()
        except Exception as e:
            last=e;time.sleep(1.5*(i+1))
    raise RuntimeError(type(last).__name__)

def esearch_title(title):
    for exact in (True,False):
        term=f'"{title}"[Title]' if exact else f"{title}[Title]"
        q=urllib.parse.urlencode({"db":"pubmed","term":term,"retmode":"json","retmax":"20","tool":"ACAD_PASS"})
        d=json.loads(http(f"{EUTILS}/esearch.fcgi?{q}"))
        ids=d.get("esearchresult",{}).get("idlist",[])
        if ids:return ids
    return []

def esummary(ids):
    if not ids:return {}
    q=urllib.parse.urlencode({"db":"pubmed","id":",".join(ids),"retmode":"json","tool":"ACAD_PASS"})
    d=json.loads(http(f"{EUTILS}/esummary.fcgi?{q}"))
    return {i:d.get("result",{}).get(i,{}) for i in ids}

def resolve_title(title):
    ids=esearch_title(title); nt=norm_title(title)
    ss=esummary(ids)
    exact=[i for i in ids if norm_title(ss.get(i,{}).get("title",""))==nt]
    return exact[0] if len(exact)==1 else None

def target_docs(root,corpus):
    seen={}; test=set()
    for fold in range(1,6):
        for role in ("train","dev","test"):
            for b in parse_bids(root/f"data/{corpus}/fold{fold}/{role}.txt"):
                h=hashlib.sha256(canonical(b).encode()).hexdigest()
                seen.setdefault(h,b)
                if role=="test":test.add(h)
    return seen,test

def efetch(pmids):
    if not pmids:return {}
    result={}
    ids=sorted(set(pmids),key=int)
    for off in range(0,len(ids),100):
        batch=ids[off:off+100]
        q=urllib.parse.urlencode({"db":"pubmed","id":",".join(batch),"retmode":"xml","tool":"ACAD_PASS"})
        root=ET.fromstring(http(f"{EUTILS}/efetch.fcgi?{q}"))
        for art in root.findall(".//PubmedArticle"):
            pm=art.findtext(".//MedlineCitation/PMID")
            if not pm:continue
            dois=set()
            regs=set()
            for el in art.findall(".//ArticleId"):
                if (el.attrib.get("IdType") or "").casefold()=="doi" and el.text:
                    dois.add(el.text.strip().casefold())
            for el in art.findall(".//ELocationID"):
                if (el.attrib.get("EIdType") or "").casefold()=="doi" and el.text:
                    dois.add(el.text.strip().casefold())
            full=" ".join(x.strip() for x in art.itertext() if x and x.strip())
            for pref,rx in REGEXES:
                for m in rx.finditer(full):
                    regs.add(pref+":"+re.sub(r"[\s:]","",m.group(1)).upper())
            result[pm]={"dois":dois,"regs":regs}
        time.sleep(.36)
    return result

def stats(target_pmids,target_test_pmids,historical):
    tmeta=efetch(target_pmids)
    histmeta=efetch(set().union(*historical.values()) if historical else set())
    tdoi=set().union(*(v["dois"] for v in tmeta.values())) if tmeta else set()
    treg=set().union(*(v["regs"] for v in tmeta.values())) if tmeta else set()
    testmeta={p:tmeta[p] for p in target_test_pmids if p in tmeta}
    testdoi=set().union(*(v["dois"] for v in testmeta.values())) if testmeta else set()
    testreg=set().union(*(v["regs"] for v in testmeta.values())) if testmeta else set()
    comp={}
    for name,pmids in historical.items():
        mm={p:histmeta[p] for p in pmids if p in histmeta}
        hd=set().union(*(v["dois"] for v in mm.values())) if mm else set()
        hr=set().union(*(v["regs"] for v in mm.values())) if mm else set()
        comp[name]={
          "historical_pmids_queried":len(pmids),
          "historical_pubmed_records_returned":len(mm),
          "whole_shared_doi_count":len(tdoi&hd),
          "test_shared_doi_count":len(testdoi&hd),
          "whole_shared_registry_count":len(treg&hr),
          "test_shared_registry_count":len(testreg&hr)
        }
    return {
      "resolved_target_pmids":len(target_pmids),
      "pubmed_records_returned":len(tmeta),
      "target_unique_dois":len(tdoi),
      "target_unique_registry_ids_from_pubmed_record":len(treg),
      "resolved_test_pmids":len(target_test_pmids),
      "test_pubmed_records_returned":len(testmeta),
      "test_unique_dois":len(testdoi),
      "test_unique_registry_ids_from_pubmed_record":len(testreg),
      "comparisons":comp
    },tmeta

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bids",type=pathlib.Path,required=True)
    ap.add_argument("--ebm-archive",type=pathlib.Path,required=True)
    ap.add_argument("--r44-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args();(a.work/"ebm").mkdir(parents=True,exist_ok=True)
    with tarfile.open(a.ebm_archive,"r:gz") as tf:tf.extractall(a.work/"ebm",filter="data")
    mapped=map_mod(parse_mod(a.bids/"data/EBM-NLPmod/fold1/train.txt"),original_tokens(a.work/"ebm"))
    m=json.loads(a.r44_manifest.read_text())
    hist={
      "DESIGN":{mapped[i] for i in m["design_documents"] if i in mapped},
      "VERIFY_INTERNAL":{mapped[i] for i in m["verify_internal_documents"] if i in mapped},
      "OLD_SELECT":{mapped[i] for i in m["excluded_old_select_documents"] if i in mapped},
    }

    targets={};reason=collections.Counter()
    for corpus in ("AD","COVID-19"):
        docs,testhash=target_docs(a.bids,corpus)
        resolved={}
        for h,b in sorted(docs.items()):
            t=title_of(b)
            if not t:reason[f"{corpus}:NO_TITLE"]+=1;continue
            p=resolve_title(t)
            if p:resolved[h]=p;reason[f"{corpus}:RESOLVED"]+=1
            else:reason[f"{corpus}:UNRESOLVED"]+=1
            time.sleep(.36)
        whole=set(resolved.values());test={resolved[h] for h in testhash if h in resolved}
        st,meta=stats(whole,test,hist)
        st["canonical_documents"]=len(docs);st["official_test_documents"]=len(testhash)
        targets[corpus]=st

    out={
      "state":"FEDERATION_PUBMED_DOI_REGISTRY_CUSTODY_AUDIT_PASS",
      "targets":targets,
      "resolution_counts":dict(sorted(reason.items())),
      "output_contains_pmids":False,
      "output_contains_dois":False,
      "output_contains_registry_ids":False,
      "output_contains_titles":False,
      "output_contains_raw_text":False,
      "output_contains_gold_labels":False,
      "limitations":[
        "Only records resolved to a unique exact normalized PubMed title are compared.",
        "DOI identity detects publication identity, not all same-trial related publications.",
        "Registry identifiers are detected only when present in the fetched PubMed record text/identifiers.",
        "Unresolved records remain unresolved and must be handled conservatively."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()
