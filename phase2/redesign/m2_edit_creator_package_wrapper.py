#!/usr/bin/env python3
from __future__ import annotations

import importlib
import runpy
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(
            "Usage: m2_edit_creator_package_wrapper.py "
            "<upstream_root> <edit_creator_args...>"
        )

    upstream = Path(sys.argv[1]).resolve()
    args = sys.argv[2:]
    sys.path.insert(0, str(upstream))

    pkg = "gec.utils.m2scorer"

    # The frozen upstream edit_creator mixes package-relative imports
    # (inside levenshtein.py) with top-level imports (inside edit_creator.py).
    # Load the package modules first, then expose aliases expected by the
    # unchanged frozen edit_creator source.
    util = importlib.import_module(pkg + ".util")
    levenshtein = importlib.import_module(pkg + ".levenshtein")
    sys.modules["util"] = util
    sys.modules["levenshtein"] = levenshtein

    sys.argv = ["edit_creator.py", *args]
    runpy.run_module(pkg + ".edit_creator", run_name="__main__")


if __name__ == "__main__":
    main()
