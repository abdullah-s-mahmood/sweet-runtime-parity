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
CLASSES=("P","I","C","O")

def lex(tokens):
    return re.findall(r"[a-z0-9]+",unicodedata.normalize("NFKC"," ".join(tokens)).casefold())

def parse_docs_with_labels(path:pathlib.Path):
    docs=[]; toks=[]; labs=[]; started=False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            if started: docs.append((toks,labs))
            toks=[]; labs=[]; started=True; continue
        if not started or not line.strip(): continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"): continue
        cols=line.split("\t")
        toks.append(cols[0])
        labs.append(cols[-1] if len(cols)>1 else "O")
    if started: docs.append((toks,labs))
    return docs

def original_tokens(root):
    out={}
    for p in root.rglob("*.tokens"):
        if p.stem.isdigit():
            x=lex(p.read_text(encoding="utf-8",errors="replace").split())
            if len(x)>=7: out[p.stem]=x
    return out

def grams(x,n=7):
    return [tuple(x[i:i+n]) for i in range(len(x)-n+1)]

def map_mod(mod_docs,orig):
    inv=collections.defaultdict(set)
    for pmid,t in orig.items():
        for g in set(grams(t)): inv[g].add(pmid)
    out={}
    for i,(tokens,labels) in enumerate(mod_docs):
        gg=set(grams(lex(tokens))); cnt=collections.Counter()
        for g in gg:
            for p in inv.get(g,()): cnt[p]+=1
        rr=cnt.most_common()
        best=rr[0][1] if rr else 0
        second=rr[1][1] if len(rr)>1 else 0
        ids=[p for p,v in rr if v==best] if best else []
        cov=best/max(1,len(gg))
        if len(ids)==1 and best>=12 and best-second>=6 and cov>=.12:
            out[i]=ids[0]
    return out

def http(url,tries=5):
    last=None
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"ACAD_PASS/1.0 dev-family-fold-audit"})
            with urllib.request.urlopen(req,timeout=40) as r: return r.read()
        except Exception as e:
            last=e; time.sleep(1.5*(i+1))
    raise RuntimeError(type(last).__name__)

def efetch(pmids):
    result={}
    ids=sorted(set(pmids),key=int)
    for off in range(0,len(ids),100):
        batch=ids[off:off+100]
        q=urllib.parse.urlencode({"db":"pubmed","id":",".join(batch),"retmode":"xml","tool":"ACAD_PASS"})
        root=ET.fromstring(http(f"{EUTILS}/efetch.fcgi?{q}"))
        for art in root.findall(".//PubmedArticle"):
            pm=art.findtext(".//MedlineCitation/PMID")
            if not pm: continue
            dois=set(); regs=set()
            for el in art.findall("./PubmedData/ArticleIdList/ArticleId"):
                if (el.attrib.get("IdType") or "").casefold()=="doi" and el.text:
                    dois.add(el.text.strip().casefold())
            for el in art.findall("./MedlineCitation/Article/ELocationID"):
                if (el.attrib.get("EIdType") or "").casefold()=="doi" and el.text:
                    dois.add(el.text.strip().casefold())
            article=art.find("./MedlineCitation/Article")
            full=" ".join(x.strip() for x in article.itertext() if x and x.strip()) if article is not None else ""
            for pref,rx in REGEXES:
                for m in rx.finditer(full):
                    regs.add(pref+":"+re.sub(r"[\s:]","",m.group(1)).upper())
            result[pm]={"dois":dois,"regs":regs}
        time.sleep(.36)
    return result

class DSU:
    def __init__(self,xs):
        self.p={x:x for x in xs}
    def find(self,x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b):
        a=self.find(a); b=self.find(b)
        if a!=b: self.p[b]=a

def count_b(labels):
    out={c:0 for c in CLASSES}
    for y in labels:
        if y.startswith("B-") and y[2:] in out:
            out[y[2:]]+=1
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=pathlib.Path,required=True)
    ap.add_argument("--r44-manifest",type=pathlib.Path,required=True)
    ap.add_argument("--ebm-archive",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args()

    docs=parse_docs_with_labels(a.train)
    if len(docs)!=400: raise RuntimeError(f"expected 400 docs got {len(docs)}")
    m=json.loads(a.r44_manifest.read_text())
    design=sorted(m["design_documents"])
    if len(design)!=256: raise RuntimeError("expected 256 DESIGN docs")

    a.work.mkdir(parents=True,exist_ok=True)
    with tarfile.open(a.ebm_archive,"r:gz") as tf: tf.extractall(a.work,filter="data")
    mapped=map_mod(docs,original_tokens(a.work))
    design_mapped={i:mapped[i] for i in design if i in mapped}
    design_unmapped=[i for i in design if i not in mapped]
    meta=efetch(set(design_mapped.values()))

    dsu=DSU(design)
    # Shared publication/trial identifiers create known family components.
    doi_owner={}; reg_owner={}
    for i,p in design_mapped.items():
        mm=meta.get(p,{"dois":set(),"regs":set()})
        for d in mm["dois"]:
            if d in doi_owner: dsu.union(i,doi_owner[d])
            else: doi_owner[d]=i
        for r in mm["regs"]:
            if r in reg_owner: dsu.union(i,reg_owner[r])
            else: reg_owner[r]=i

    # Conservative unresolved policy: put all unresolved DESIGN docs in one component.
    if design_unmapped:
        root=design_unmapped[0]
        for i in design_unmapped[1:]: dsu.union(root,i)

    comps=collections.defaultdict(list)
    for i in design: comps[dsu.find(i)].append(i)

    # Canonical internal family key. Never emitted.
    family_keys=[]
    for root,inds in comps.items():
        pmids=sorted([design_mapped[i] for i in inds if i in design_mapped],key=int)
        if pmids:
            key="PMID:"+pmids[0]
        else:
            key="UNRESOLVED_COMPONENT"
        rank=hashlib.sha256(("ACAD_PASS_FED_V1_DEV|"+key).encode()).hexdigest()
        family_keys.append((rank,root,inds))
    family_keys.sort()

    folds={0:[],1:[],2:[]}
    for pos,(_,root,inds) in enumerate(family_keys):
        folds[pos%3].extend(inds)

    fold_stats={}
    for k,inds in folds.items():
        cnt={c:0 for c in CLASSES}
        for i in inds:
            cc=count_b(docs[i][1])
            for c in CLASSES: cnt[c]+=cc[c]
        valid=all(cnt[c]>0 for c in CLASSES) and cnt["C"]>=20
        fold_stats[str(k)]={
          "documents":len(inds),
          "source_compatible_B_entity_counts":cnt,
          "all_classes_present":all(cnt[c]>0 for c in CLASSES),
          "C_at_least_20":cnt["C"]>=20,
          "fold_gate_pass":valid
        }

    comp_sizes=[len(v) for v in comps.values()]
    out={
      "state":"FEDERATION_DEVELOPMENT_FAMILY_FOLD_CUSTODY_PASS" if all(x["fold_gate_pass"] for x in fold_stats.values()) else "FEDERATION_DEVELOPMENT_FAMILY_FOLD_CUSTODY_FAIL",
      "design_documents":256,
      "mapped_design_pmids":len(design_mapped),
      "unresolved_design_documents":len(design_unmapped),
      "pubmed_records_returned":len(meta),
      "known_shared_doi_edge_keys":sum(1 for d in doi_owner),
      "known_shared_registry_edge_keys":sum(1 for r in reg_owner),
      "family_components":len(comps),
      "largest_component_size":max(comp_sizes),
      "multi_document_components":sum(1 for x in comp_sizes if x>1),
      "unresolved_docs_forced_single_component":len(design_unmapped),
      "fold_assignment_rule":"sort SHA256('ACAD_PASS_FED_V1_DEV|'+canonical_family_key), positions modulo 3",
      "folds":fold_stats,
      "output_contains_pmids":False,
      "output_contains_dois":False,
      "output_contains_registry_ids":False,
      "output_contains_raw_text":False,
      "limitations":[
        "Known-family components use shared DOI/registry evidence plus conservative grouping of unresolved records.",
        "Absence of a shared registry/DOI does not prove distinct trials.",
        "This is a development leakage-reduction graph, not a claim of perfect clinical trial-family reconstruction."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
    if out["state"].endswith("_FAIL"):
        raise SystemExit(2)

if __name__=="__main__": main()
