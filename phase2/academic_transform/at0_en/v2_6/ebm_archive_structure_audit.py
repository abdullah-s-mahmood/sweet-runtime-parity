#!/usr/bin/env python3
import argparse,collections,json,pathlib,tarfile
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--archive",type=pathlib.Path,required=True); ap.add_argument("--out",type=pathlib.Path,required=True); a=ap.parse_args()
    top=collections.Counter(); depths=collections.Counter(); keyword=collections.Counter(); samples=[]
    with tarfile.open(a.archive,"r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile(): continue
            p=pathlib.PurePosixPath(m.name); parts=p.parts
            if parts: top[parts[0]]+=1
            depths[len(parts)]+=1
            low=[x.casefold() for x in parts]
            for k in ["annotations","aggregated","starting_spans","hierarchical_labels","participants","interventions","outcomes","train","test","gold"]:
                if k in low: keyword[k]+=1
            if ("starting_spans" in low or "phase1" in low) and len(samples)<80:
                # structural path only; filename stem redacted
                red=list(parts)
                if red:
                    suffix=pathlib.PurePosixPath(red[-1]).suffix
                    red[-1]="<FILE>"+suffix
                samples.append("/".join(red))
    d={"state":"EBM_ARCHIVE_STRUCTURE_AUDIT_PASS","top_components":dict(top),"depths":dict(depths),"keyword_counts":dict(keyword),"structural_samples":samples,"content_read":False}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps(d,indent=2,sort_keys=True))
if __name__=="__main__": main()
