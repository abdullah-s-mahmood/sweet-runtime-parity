#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,csv,hashlib,json,pathlib,re,tarfile,time,unicodedata,urllib.parse,urllib.request,xml.etree.ElementTree as ET

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

def sha_lines(lines):
    return hashlib.sha256(("\n".join(sorted(lines))+"\n").encode()).hexdigest()

def lex(tokens):
    return re.findall(r"[a-z0-9]+",unicodedata.normalize("NFKC"," ".join(tokens)).casefold())

def parse_mod(path):
    docs=[]; toks=[]; labs=[]; started=False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("-DOCSTART-"):
            if started: docs.append((toks,labs))
            toks=[];labs=[];started=True;continue
        if not started or not line.strip(): continue
        if line.strip().startswith("###") and line.strip().endswith("$$$"): continue
        cols=line.split("\t"); toks.append(cols[0]); labs.append(cols[-1] if len(cols)>1 else "O")
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

def map_mod(mod,orig):
    inv=collections.defaultdict(set)
    for pmid,t in orig.items():
        for g in set(grams(t)): inv[g].add(pmid)
    out={}
    for i,(tokens,_) in enumerate(mod):
        gg=set(grams(lex(tokens))); cnt=collections.Counter()
        for g in gg:
            for p in inv.get(g,()):cnt[p]+=1
        rr=cnt.most_common(); best=rr[0][1] if rr else 0; second=rr[1][1] if len(rr)>1 else 0
        ids=[p for p,v in rr if v==best] if best else []; cov=best/max(1,len(gg))
        if len(ids)==1 and best>=12 and best-second>=6 and cov>=.12: out[i]=ids[0]
    return out

def http(url,tries=5):
    last=None
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"ACAD_PASS/1.0 fit-manifest-custody"})
            with urllib.request.urlopen(req,timeout=40) as r:return r.read()
        except Exception as e:last=e;time.sleep(1.5*(i+1))
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
            if not pm:continue
            dois=set();regs=set()
            for el in art.findall("./PubmedData/ArticleIdList/ArticleId"):
                if (el.attrib.get("IdType") or "").casefold()=="doi" and el.text:dois.add(el.text.strip().casefold())
            for el in art.findall("./MedlineCitation/Article/ELocationID"):
                if (el.attrib.get("EIdType") or "").casefold()=="doi" and el.text:dois.add(el.text.strip().casefold())
            article=art.find("./MedlineCitation/Article")
            full=" ".join(x.strip() for x in article.itertext() if x and x.strip()) if article is not None else ""
            for pref,rx in REGEXES:
                for m in rx.finditer(full):regs.add(pref+":"+re.sub(r"[\s:]","",m.group(1)).upper())
            result[pm]={"dois":dois,"regs":regs}
        time.sleep(.36)
    return result

class DSU:
    def __init__(self,xs):self.p={x:x for x in xs}
    def find(self,x):
        while self.p[x]!=x:self.p[x]=self.p[self.p[x]];x=self.p[x]
        return x
    def union(self,a,b):
        a=self.find(a);b=self.find(b)
        if a!=b:self.p[b]=a

def build_folds(design,mapped,meta):
    dsu=DSU(design);doi={};reg={}
    unresolved=[i for i in design if i not in mapped]
    for i,p in mapped.items():
        if i not in design:continue
        mm=meta.get(p,{"dois":set(),"regs":set()})
        for x in mm["dois"]:
            if x in doi:dsu.union(i,doi[x])
            else:doi[x]=i
        for x in mm["regs"]:
            if x in reg:dsu.union(i,reg[x])
            else:reg[x]=i
    if unresolved:
        for i in unresolved[1:]:dsu.union(unresolved[0],i)
    comps=collections.defaultdict(list)
    for i in design:comps[dsu.find(i)].append(i)
    ranked=[]
    for root,inds in comps.items():
        ps=sorted([mapped[i] for i in inds if i in mapped],key=int)
        key="PMID:"+ps[0] if ps else "UNRESOLVED_COMPONENT"
        rank=hashlib.sha256(("ACAD_PASS_FED_V1_DEV|"+key).encode()).hexdigest()
        ranked.append((rank,inds,key))
    ranked.sort()
    folds={0:[],1:[],2:[]};keys={0:[],1:[],2:[]}
    for pos,(_,inds,key) in enumerate(ranked):
        k=pos%3;folds[k]+=inds;keys[k].append(key)
    return folds,keys

def pmids_from_evidence(path):
    s=set()
    with open(path,encoding="utf-8",newline="") as f:
        for row in csv.reader(f,delimiter="\t"):
            if len(row)==5 and row[1].strip().isdigit():s.add(row[1].strip())
    return s

def pmids_from_trialsieve(path):
    d=json.loads(path.read_text(encoding="utf-8"))
    out={"train":set(),"validation":set(),"test":set()}
    for x in d:
        p=str(x.get("pmid","")).strip();sp=str(x.get("split",""))
        if p.isdigit() and sp in out:out[sp].add(p)
    return out

def pico_pmids(root):
    return {p.stem for p in (root/"pico_corpus_brat_annotated_files").glob("*.txt") if p.stem.isdigit()}

def ebm_train_pmids(root):
    # Mirror the already-passed authoritative adapter preflight archive layout.
    ann_roots=[p for p in root.rglob("annotations") if p.is_dir()]
    top=None
    for p in ann_roots:
        if (p/"aggregated"/"starting_spans").exists():
            top=p.parent
            break
    if top is None:
        raise RuntimeError("EBM starting_spans root not found")
    out=set()
    for pio in ("participants","interventions","outcomes"):
        train_dir=top/"annotations"/"aggregated"/"starting_spans"/pio/"train"
        if not train_dir.exists():
            raise RuntimeError(f"missing EBM train dir for {pio}")
        for p in train_dir.glob("*.ann"):
            pmid=p.stem.split("_")[0]
            if pmid.isdigit(): out.add(pmid)
    if len(out)<4000:
        raise RuntimeError(f"unexpectedly small EBM training PMID union: {len(out)}")
    return out

def family_alias_set(pmids,meta):
    dois=set();regs=set()
    for p in pmids:
        mm=meta.get(p)
        if mm:
            dois|=mm["dois"];regs|=mm["regs"]
    return pmids,dois,regs

def decontam(source_pmids,source_meta,held):
    hpm,hdoi,hreg=held
    admitted=[];excluded=[]
    for p in sorted(source_pmids,key=int):
        mm=source_meta.get(p,{"dois":set(),"regs":set()})
        conflict=(p in hpm) or bool(mm["dois"]&hdoi) or bool(mm["regs"]&hreg)
        (excluded if conflict else admitted).append(p)
    return admitted,excluded

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bids",type=pathlib.Path,required=True)
    ap.add_argument("--r44",type=pathlib.Path,required=True)
    ap.add_argument("--ebm-archive",type=pathlib.Path,required=True)
    ap.add_argument("--pico",type=pathlib.Path,required=True)
    ap.add_argument("--evidence",type=pathlib.Path,required=True)
    ap.add_argument("--trialsieve",type=pathlib.Path,required=True)
    ap.add_argument("--work",type=pathlib.Path,required=True)
    ap.add_argument("--out",type=pathlib.Path,required=True)
    a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True)
    with tarfile.open(a.ebm_archive,"r:gz") as tf:tf.extractall(a.work/"ebm",filter="data")
    docs=parse_mod(a.bids/"data/EBM-NLPmod/fold1/train.txt")
    m=json.loads(a.r44.read_text());design=sorted(m["design_documents"])
    mapped=map_mod(docs,original_tokens(a.work/"ebm"))
    # Fetch metadata for mapped design first.
    meta=efetch({mapped[i] for i in design if i in mapped})
    folds,keys=build_folds(design,mapped,meta)

    sources={
      "EBM_ORIGINAL_PIO":ebm_train_pmids(a.work/"ebm"),
      "PICO_CORPUS_26":pico_pmids(a.pico),
      "EVIDENCE_OUTCOME_500":pmids_from_evidence(a.evidence/"500RCT-CoNLL.tsv"),
    }
    ts=pmids_from_trialsieve(a.trialsieve/"data/processed_for_modeling.json")
    sources["TRIALSIEVE_20_TRAIN_VALIDATION"]=ts["train"]|ts["validation"]

    # Fetch metadata for all auxiliary PMIDs once.
    all_aux=set().union(*sources.values())
    aux_meta=efetch(all_aux)

    manifests={}
    for fold in range(3):
        held_indices=folds[fold]
        held_pmids={mapped[i] for i in held_indices if i in mapped}
        held=family_alias_set(held_pmids,meta)
        source_summary={}
        for name,pmids in sources.items():
            adm,exc=decontam(pmids,aux_meta,held)
            source_summary[name]={
              "source_records":len(pmids),
              "admitted_records":len(adm),
              "excluded_known_family_alias_records":len(exc),
              "admitted_identity_digest_sha256":sha_lines([hashlib.sha256(("SRC|"+name+"|"+p).encode()).hexdigest() for p in adm]),
              "excluded_identity_digest_sha256":sha_lines([hashlib.sha256(("SRC|"+name+"|"+p).encode()).hexdigest() for p in exc]),
            }
        native_train=[i for i in design if i not in set(held_indices)]
        native_eval=held_indices
        manifest={
          "schema":"ACAD_PASS_FEDERATION_DEV_FOLD_DATA_MANIFEST_V1",
          "fold":fold,
          "native_train_documents":len(native_train),
          "native_eval_documents":len(native_eval),
          "native_train_index_digest_sha256":sha_lines([str(i) for i in native_train]),
          "native_eval_index_digest_sha256":sha_lines([str(i) for i in native_eval]),
          "heldout_mapped_pmids":len(held_pmids),
          "heldout_unresolved_documents":sum(i not in mapped for i in native_eval),
          "auxiliary_sources":source_summary,
          "D0_D1_auxiliary_use":"NONE",
          "D2_D3_D4_auxiliary_use":["EBM_ORIGINAL_PIO","PICO_CORPUS_26","EVIDENCE_OUTCOME_500","TRIALSIEVE_20_TRAIN_VALIDATION"],
          "D5":"CANCELED"
        }
        raw=json.dumps(manifest,sort_keys=True,separators=(",",":")).encode()
        manifest["manifest_sha256"]=hashlib.sha256(raw).hexdigest()
        manifests[str(fold)]=manifest

    out={
      "state":"FEDERATION_PER_FOLD_DATA_MANIFEST_CUSTODY_PASS",
      "source_documents":256,
      "folds":manifests,
      "output_contains_pmids":False,
      "output_contains_dois":False,
      "output_contains_registry_ids":False,
      "scientific_training_performed":False,
      "limitations":[
        "Decontamination removes known PMID/DOI/registry family aliases; unresolved family identity remains conservatively documented.",
        "Auxiliary source licensing/terms remain separate from identity decontamination.",
        "Manifest hashes bind counts/identity digests, not raw protected identifiers."
      ]
    }
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()
