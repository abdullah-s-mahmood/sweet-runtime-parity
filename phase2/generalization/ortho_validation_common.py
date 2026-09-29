"""Raw-only selector for the third disjoint QALB15 TRAIN validation slice."""
from __future__ import annotations
from pathlib import Path
from phase2.generalization.cross_model_common import sha_text, read_nonempty_lines

CROSS_SEED="phase2-cross-model-agreement-v1"
TRI_SEED="phase2-trimodel-vote-v1"
VALIDATION_SEED="phase2-ortho-isolated-validation-v1"
SLICE_N=50

def select_validation_raw_lines(path:Path):
    lines=read_nonempty_lines(path)

    cross=[(sha_text(CROSS_SEED+"|"+s),i,s) for i,s in enumerate(lines,1)]
    cross.sort(key=lambda x:x[0])
    cross_ids={i for _,i,_ in cross[:min(SLICE_N,len(cross))]}

    tri=[(sha_text(TRI_SEED+"|"+s),i,s) for i,s in enumerate(lines,1) if i not in cross_ids]
    tri.sort(key=lambda x:x[0])
    tri_ids={i for _,i,_ in tri[:min(SLICE_N,len(tri))]}

    fresh=[(sha_text(VALIDATION_SEED+"|"+s),i,s) for i,s in enumerate(lines,1)
           if i not in cross_ids and i not in tri_ids]
    fresh.sort(key=lambda x:x[0])
    selected=fresh[:min(SLICE_N,len(fresh))]

    selected_ids={i for _,i,_ in selected}
    assert not selected_ids & cross_ids
    assert not selected_ids & tri_ids
    assert not cross_ids & tri_ids
    return selected,len(lines),sorted(cross_ids),sorted(tri_ids)
