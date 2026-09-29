"""Contextual morphological identity diagnostic for tri-model targets.

Reads source/corrected ephemeral text only. Writes feature-equality/hash evidence,
never QALB text.
"""
from __future__ import annotations
import hashlib,json,unicodedata
from pathlib import Path
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator

from phase2.arabart_audit.build_full_arabart_edit_queue import units

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"artifacts"
CONS=ART/"consensus"/"POSTEDIT_CONSENSUS_LINES.jsonl"
OUT=ART/"POSTEDIT_MORPH_IDENTITY.jsonl"

FIELDS=("lex","pos","per","asp","vox","gen","num","prc0","prc1","prc2","prc3","enc0")

def jl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]

def norm_lex(v):
    if v is None:return None
    return "".join(ch for ch in unicodedata.normalize("NFC",str(v))
                   if unicodedata.category(ch)!="Mn" and ch!="ـ")

def h(v):
    if v is None:return None
    return hashlib.sha256(str(v).encode("utf-8")).hexdigest()

def top_analysis(d):
    if not d.analyses:return None
    return d.analyses[0].analysis

def main():
    dis=BERTUnfactoredDisambiguator.pretrained()
    out=[]
    for x in jl(CONS):
        src=x["source_text"]; cor=x["corrected_text"]
        sw=src.split(); cw=cor.split()
        sd=dis.disambiguate(sw); cd=dis.disambiguate(cw)
        su=units(src); cu=units(cor)
        assert len(su)==len(cu)
        for t in x["targets"]:
            i=int(t["source_lexical_span"][0])
            swi=su[i]["whitespace_word_index"]; cwi=cu[i]["whitespace_word_index"]
            sa=top_analysis(sd[swi]); ca=top_analysis(cd[cwi])
            available=(sa is not None and ca is not None)
            eq={}
            hashes={}
            if available:
                for f in FIELDS:
                    sv=norm_lex(sa.get(f)) if f=="lex" else sa.get(f)
                    cv=norm_lex(ca.get(f)) if f=="lex" else ca.get(f)
                    eq[f]=(sv==cv)
                    hashes[f]={"source":h(sv),"candidate":h(cv)}
            safe=bool(available and all(eq.values()))
            out.append({
                "vote_id":t["vote_id"],
                "line_id":x["line_id"],
                "line_hash":x["line_hash"],
                "source_lexical_span":t["source_lexical_span"],
                "source_hash":t["source_hash"],
                "candidate_hash":t["candidate_hash"],
                "analysis_available":available,
                "field_equal":eq,
                "field_value_hashes":hashes,
                "morph_identity_safe":safe,
            })
    assert len(out)==142,len(out)
    OUT.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf-8")
    dumped=OUT.read_text(encoding="utf-8")
    assert not any("\u0600"<=ch<="\u06ff" for ch in dumped),"Arabic text leaked"
    print(json.dumps({"status":"POSTEDIT_MORPH_IDENTITY_COMPLETE","rows":len(out),
                      "safe":sum(x["morph_identity_safe"] for x in out),
                      "unavailable":sum(not x["analysis_available"] for x in out)}))

if __name__=="__main__":
    main()
