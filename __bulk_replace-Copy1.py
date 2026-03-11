## I just use this one manually!!! BE CAREFUL!!!


#!/usr/bin/env python3
"""
Bulk string replace across Markdown + Jupyter notebooks.

- Markdown: replaces in entire file text.
- Notebooks (.ipynb): replaces in cell sources (markdown/code/raw) and optionally metadata fields.

Author: Silvia Mazzoni (silviamazzoni@yahoo.com)
"""




from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple, Dict, Any


@dataclass(frozen=True)
class ReplacePair:
    old: str
    new: str



# =========================
# USER FLAGS (edit these)
# =========================
PROCESS_MD = True
PROCESS_IPYNB = False

# Notebook-only options (used only if PROCESS_IPYNB is True)
NB_INCLUDE_CODE = False
NB_INCLUDE_MARKDOWN = True
NB_INCLUDE_RAW = False
NB_INCLUDE_METADATA = True

# If True, the script will error if both PROCESS_MD and PROCESS_IPYNB are False
REQUIRE_SOMETHING_TO_DO = True

# =========================
# REPLACEMENTS (edit these)
# =========================
REPLACE_PAIRS = [
    # ("old", "new"),
    # ("../../shared/../Examples", "../../../shared/Examples"),
    ('"../static/_images/'},"../../../shared/images"),
    ]

# =========================





DEFAULT_NOTEBOOK_METADATA_PATHS = [
    # Common spots where text appears
    ("metadata", "title"),
    ("metadata", "authors"),
    ("metadata", "kernelspec", "display_name"),
    ("metadata", "language_info", "name"),
]

def iter_files(root: Path, exts: Iterable[str], exclude_dirs: Iterable[str]) -> Iterable[Path]:
    exts_lc = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in exts}
    exclude = set(exclude_dirs)

    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded directories in-place
        dirnames[:] = [d for d in dirnames if d not in exclude and not d.startswith(".")]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in exts_lc:
                yield p


def apply_replacements(text: str, pairs: List[ReplacePair]) -> Tuple[str, int]:
    """Return (new_text, num_replacements_total)."""
    total = 0
    out = text
    for pair in pairs:
        if not pair.old:
            continue
        count = out.count(pair.old)
        if count:
            out = out.replace(pair.old, pair.new)
            total += count
    return out, total


def replace_in_markdown(path: Path, pairs: List[ReplacePair]) -> Tuple[bool, int]:
    original = path.read_text(encoding="utf-8")
    updated, n = apply_replacements(original, pairs)
    if n == 0:
        return False, 0
    path.write_text(updated, encoding="utf-8")
    return True, n


def _get_nested(obj: Dict[str, Any], keys: Tuple[str, ...]) -> Tuple[bool, Any]:
    cur: Any = obj
    for k in keys[:-1]:
        if not isinstance(cur, dict) or k not in cur:
            return False, None
        cur = cur[k]
    last = keys[-1]
    if not isinstance(cur, dict) or last not in cur:
        return False, None
    return True, cur[last]


def _set_nested(obj: Dict[str, Any], keys: Tuple[str, ...], value: Any) -> bool:
    cur: Any = obj
    for k in keys[:-1]:
        if not isinstance(cur, dict) or k not in cur:
            return False
        cur = cur[k]
    last = keys[-1]
    if not isinstance(cur, dict) or last not in cur:
        return False
    cur[last] = value
    return True


def replace_in_notebook(
    path: Path,
    pairs: List[ReplacePair],
    include_code: bool,
    include_markdown: bool,
    include_raw: bool,
    metadata_paths: List[Tuple[str, ...]],
) -> Tuple[bool, int]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    total_changes = 0

    # Cells
    for cell in nb.get("cells", []):
        ctype = cell.get("cell_type", "")
        if ctype == "code" and not include_code:
            continue
        if ctype == "markdown" and not include_markdown:
            continue
        if ctype == "raw" and not include_raw:
            continue

        src = cell.get("source", "")
        # In notebooks, "source" can be list[str] or str
        if isinstance(src, list):
            joined = "".join(src)
            updated, n = apply_replacements(joined, pairs)
            if n:
                # keep list-of-lines style
                cell["source"] = updated.splitlines(keepends=True)
                total_changes += n
        elif isinstance(src, str):
            updated, n = apply_replacements(src, pairs)
            if n:
                cell["source"] = updated
                total_changes += n

    # Metadata (optional)
    for keys in metadata_paths:
        ok, val = _get_nested(nb, keys)
        if not ok:
            continue
        if isinstance(val, str):
            updated, n = apply_replacements(val, pairs)
            if n:
                _set_nested(nb, keys, updated)
                total_changes += n
        elif isinstance(val, list):
            # Sometimes authors is a list of strings/dicts; replace in string elements
            changed_any = False
            new_list = []
            for item in val:
                if isinstance(item, str):
                    updated, n = apply_replacements(item, pairs)
                    if n:
                        total_changes += n
                        changed_any = True
                    new_list.append(updated)
                else:
                    new_list.append(item)
            if changed_any:
                _set_nested(nb, keys, new_list)

    if total_changes == 0:
        return False, 0

    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return True, total_changes

def load_pairs_inline() -> List[ReplacePair]:
    return [ReplacePair(old, new) for (old, new) in REPLACE_PAIRS]

def load_pairs(pairs_path: Path) -> List[ReplacePair]:
    """
    Load replacements from JSON.
    Format:
      [
        ["old", "new"],
        ["old2", "new2"]
      ]
    """
    data = json.loads(pairs_path.read_text(encoding="utf-8"))
    out: List[ReplacePair] = []
    if not isinstance(data, list):
        raise ValueError("pairs JSON must be a list of [old,new] pairs.")
    for item in data:
        if not (isinstance(item, list) and len(item) == 2):
            raise ValueError("Each pair must be a 2-item list: [old, new].")
        out.append(ReplacePair(str(item[0]), str(item[1])))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Bulk replace strings in .md and .ipynb files.")
    ap.add_argument("--root", default=".", help="Root folder to search (default: current directory).")

    # Optional: only used if REPLACE_PAIRS is empty
    ap.add_argument("--pairs", default="", help="Path to JSON file containing [[old,new], ...] (used only if REPLACE_PAIRS is empty).")

    ap.add_argument(
        "--exclude-dir",
        nargs="*",
        default=[".git", "_build", "__pycache__", ".ipynb_checkpoints"],
        help="Directory names to skip (by name).",
    )
    ap.add_argument("--dry-run", action="store_true", help="Show what would change but do not write files.")
    ap.add_argument("--backup", action="store_true", help="Create a .bak copy of each file that changes.")

    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Root path does not exist: {root}")

    if REQUIRE_SOMETHING_TO_DO and not (PROCESS_MD or PROCESS_IPYNB):
        raise SystemExit("Nothing to do: PROCESS_MD and PROCESS_IPYNB are both False.")

    # Load pairs: inline first; fallback to JSON file if inline is empty
    if len(REPLACE_PAIRS) > 0:
        pairs = load_pairs_inline()
    else:
        if not args.pairs:
            raise SystemExit("REPLACE_PAIRS is empty. Provide --pairs path to a JSON file of replacements.")
        pairs = load_pairs(Path(args.pairs))

    if not pairs:
        print("No replacement pairs. Exiting.")
        return

    # Add a startup summary (so you don’t accidentally run on the wrong root)
    print("=== bulk_replace settings ===")
    print(f"root: {root}")
    print(f"PROCESS_MD: {PROCESS_MD}, PROCESS_IPYNB: {PROCESS_IPYNB}")
    print(f"NB_INCLUDE_CODE: {NB_INCLUDE_CODE}, NB_INCLUDE_MARKDOWN: {NB_INCLUDE_MARKDOWN}, NB_INCLUDE_RAW: {NB_INCLUDE_RAW}, NB_INCLUDE_METADATA: {NB_INCLUDE_METADATA}")
    print(f"pairs: {len(pairs)}")
    if args.dry_run:
        print("mode: DRY-RUN")
    else:
        print(f"mode: APPLY (backup={args.backup})")
    print("============================")


    
    # Decide extensions based on top-of-file flags
    exts: List[str] = []
    if PROCESS_MD:
        exts.append(".md")
    if PROCESS_IPYNB:
        exts.append(".ipynb")

    metadata_paths = [tuple(p) for p in DEFAULT_NOTEBOOK_METADATA_PATHS] if NB_INCLUDE_METADATA else []

    changed_files = 0
    total_repls = 0

    for p in iter_files(root, exts, args.exclude_dir):
        if not os.access(p, os.W_OK) and not args.dry_run:
            print(f"SKIP (not writable): {p}")
            continue

        suffix = p.suffix.lower()
        did_change = False
        nrepl = 0

        if suffix == ".md":
            txt = p.read_text(encoding="utf-8")
            updated, nrepl = apply_replacements(txt, pairs)
            if nrepl:
                did_change = True
                if args.dry_run:
                    print(f"DRY-RUN: {p}  ({nrepl} replacements)")
                else:
                    if args.backup:
                        p.with_suffix(p.suffix + ".bak").write_text(txt, encoding="utf-8")
                    p.write_text(updated, encoding="utf-8")

        elif suffix == ".ipynb":
            original = p.read_text(encoding="utf-8")

            if args.dry_run:
                nb_copy = json.loads(original)
                total_changes = 0

                for cell in nb_copy.get("cells", []):
                    ctype = cell.get("cell_type", "")
                    if ctype == "code" and not NB_INCLUDE_CODE:
                        continue
                    if ctype == "markdown" and not NB_INCLUDE_MARKDOWN:
                        continue
                    if ctype == "raw" and not NB_INCLUDE_RAW:
                        continue

                    src = cell.get("source", "")
                    if isinstance(src, list):
                        joined = "".join(src)
                        _, n = apply_replacements(joined, pairs)
                        total_changes += n
                    elif isinstance(src, str):
                        _, n = apply_replacements(src, pairs)
                        total_changes += n

                if metadata_paths:
                    for keys in metadata_paths:
                        ok, val = _get_nested(nb_copy, keys)
                        if ok and isinstance(val, str):
                            _, n = apply_replacements(val, pairs)
                            total_changes += n
                        elif ok and isinstance(val, list):
                            for item in val:
                                if isinstance(item, str):
                                    _, n = apply_replacements(item, pairs)
                                    total_changes += n

                nrepl = total_changes
                if nrepl:
                    did_change = True
                    print(f"DRY-RUN: {p}  ({nrepl} replacements)")

            else:
                if args.backup:
                    p.with_suffix(p.suffix + ".bak").write_text(original, encoding="utf-8")

                did_change, nrepl = replace_in_notebook(
                    p,
                    pairs,
                    include_code=NB_INCLUDE_CODE,
                    include_markdown=NB_INCLUDE_MARKDOWN,
                    include_raw=NB_INCLUDE_RAW,
                    metadata_paths=metadata_paths,
                )

                if did_change:
                    print(f"UPDATED: {p}  ({nrepl} replacements)")

        if did_change:
            changed_files += 1
            total_repls += nrepl

    print(f"\nDone. Changed files: {changed_files}, total replacements: {total_repls}")


if __name__ == "__main__":
    main()


# How you run it now

# If you keep REPLACE_PAIRS filled in:

# python bulk_replace.py --root . --dry-run
# python bulk_replace.py --root . --backup


# If you set REPLACE_PAIRS = [], then:

# python bulk_replace.py --root . --pairs replace_pairs.json --dry-run