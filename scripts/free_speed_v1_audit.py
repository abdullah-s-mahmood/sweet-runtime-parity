#!/usr/bin/env python3
from __future__ import annotations
import json,re,pathlib,hashlib,collections

ROOT=pathlib.Path(__file__).resolve().parents[1]
WF=ROOT/".github/workflows"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def refs(text):
    out=[]
    for m in re.finditer(r"(?:python|python3)\s+(?:-m\s+)?([^\s\\]+\.py)",text):
        p=m.group(1).strip("'\"")
        q=ROOT/p
        if q.exists(): out.append(q)
    return sorted(set(out))

def main():
    rows=[]
    for p in sorted(list(WF.glob("*.yml"))+list(WF.glob("*.yaml"))):
        text=p.read_text(encoding="utf-8",errors="replace")
        low=(p.name+"\n"+text[:1000]).lower()
        py=refs(text)
        pytext="\n".join(x.read_text(encoding="utf-8",errors="replace") for x in py)

        matrix="matrix:" in text
        mp1=bool(re.search(r"max-parallel\s*:\s*1\b",text))
        has_concurrency="concurrency:" in text
        cancel_false=bool(re.search(r"cancel-in-progress\s*:\s*false\b",text,re.I))
        cancel_true=bool(re.search(r"cancel-in-progress\s*:\s*true\b",text,re.I))
        pip_install=bool(re.search(r"pip(?:3)?\s+install|python\s+-m\s+pip\s+install",text,re.I))
        setup_python="actions/setup-python@" in text
        hf=("snapshot_download" in text or "huggingface" in text.lower() or any("snapshot_download" in x.read_text(encoding="utf-8",errors="replace") for x in py))
        cache=("actions/cache@" in text or re.search(r"\bcache\s*:\s*['\"]?pip",text,re.I) is not None)
        threads=re.findall(r"torch\.set_num_threads\((\d+)\)",pytext)
        workers=re.findall(r"dataloader_num_workers\s*=\s*(\d+)",pytext)

        diagnostic=any(k in low for k in ["preflight","mechanics","diagnostic","smoke","audit","check"])
        scientific=any(k in low for k in ["train","training","fit-only","stage-b","stage-a","confirmatory","benchmark","oof upstream candidate bank","mitigation"])
        frozen=any(k in low for k in ["frozen","one-shot","confirmatory","protected"])

        flags=[]
        if scientific and not diagnostic: flags.append("DO_NOT_TOUCH_ACTIVE_OR_FROZEN_WITHOUT_VERSIONED_PROTOCOL")
        if (pip_install or setup_python or hf) and not cache: flags.append("CACHE_SAFE_CANDIDATE")
        if matrix and mp1: flags.append("PARALLEL_CANDIDATE_REQUIRES_INDEPENDENCE_PROOF")
        if threads or workers: flags.append("CPU_TUNING_CANDIDATE_REQUIRES_REPRO_BENCHMARK")
        if diagnostic and cancel_false: flags.append("CANCEL_SUPERSEDED_CANDIDATE")
        if not flags: flags.append("NO_OBVIOUS_FREE_SPEED_CHANGE")

        rows.append({
          "workflow":p.name,"workflow_sha256":sha(p),"flags":flags,
          "matrix":matrix,"max_parallel_1":mp1,
          "concurrency":has_concurrency,"cancel_in_progress_false":cancel_false,"cancel_in_progress_true":cancel_true,
          "pip_install":pip_install,"setup_python":setup_python,"hf_download_or_reference":hf,"cache_detected":cache,
          "referenced_python":[str(x.relative_to(ROOT)) for x in py],
          "torch_set_num_threads":threads,"dataloader_num_workers":workers,
          "scientific_sensitive_heuristic":scientific,"diagnostic_heuristic":diagnostic,"frozen_heuristic":frozen
        })

    counts=collections.Counter(f for r in rows for f in r["flags"])
    summary={"state":"FREE_SPEED_V1_STATIC_AUDIT_COMPLETE","workflow_count":len(rows),"flag_counts":dict(counts),
             "warning":"Flags are conservative static-analysis candidates, not automatic authorization to modify scientific workflows."}
    out=ROOT/"free_speed_v1"
    out.mkdir(exist_ok=True)
    (out/"FREE_SPEED_V1_WORKFLOW_INVENTORY.json").write_text(json.dumps({"summary":summary,"workflows":rows},indent=2,sort_keys=True)+"\n")
    md=["# FREE-SPEED V1 — Workflow Static Audit","",f"Workflows scanned: **{len(rows)}**","",
        "This is a conservative static classification. It does not modify any workflow and does not authorize changes to frozen scientific runs.","",
        "## Counts",""]
    for k,v in sorted(counts.items()): md.append(f"- {k}: **{v}**")
    md+=["","## Priority recommendations","",
         "1. Never change an active/frozen scientific run in place.",
         "2. Prefer dependency/model caching or immutable prepared artifacts before CPU/thread tuning.",
         "3. Parallelize only matrix jobs proven to have immutable inputs, disjoint outputs, no shared mutable state, and aggregate-after-all semantics.",
         "4. Treat thread/DataLoader changes as reproducibility benchmarks, not transparent optimizations.",
         "5. cancel-in-progress=true is only a candidate for superseded development diagnostics, never frozen one-shot science.","",
         "## Inventory","",
         "| Workflow | Flags | Cache | Matrix/max=1 | Threads | Workers |",
         "|---|---|---:|---:|---|---|"]
    for r in rows:
        md.append(f"| {r['workflow']} | {', '.join(r['flags'])} | {'yes' if r['cache_detected'] else 'no'} | {'yes' if r['matrix'] and r['max_parallel_1'] else 'no'} | {','.join(r['torch_set_num_threads']) or '-'} | {','.join(r['dataloader_num_workers']) or '-'} |")
    (out/"FREE_SPEED_V1_REPORT.md").write_text("\n".join(md)+"\n")
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__": main()
