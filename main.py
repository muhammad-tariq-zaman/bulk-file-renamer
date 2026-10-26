"""Bulk file renamer: safe bulk rename with preview/dry-run and undo mapping."""
import argparse
import json
import os
import sys


def build_mapping(directory, find="", replace="", prefix="", suffix=""):
    mapping = {}
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        new = name
        if find:
            new = new.replace(find, replace)
        stem, ext = os.path.splitext(new)
        new = prefix + stem + suffix + ext
        if new != name and new:
            mapping[name] = new
    return mapping


def apply_mapping(directory, mapping, undo_file):
    applied = {}
    for old, new in mapping.items():
        src, dst = os.path.join(directory, old), os.path.join(directory, new)
        if os.path.exists(dst):
            raise FileExistsError(f"target already exists: {dst}")
        os.rename(src, dst)
        applied[old] = new
    with open(undo_file, "w", encoding="utf-8") as fh:
        json.dump(applied, fh, indent=2)
    return applied


def undo_rename(directory, undo_file):
    with open(undo_file, encoding="utf-8") as fh:
        mapping = json.load(fh)
    for old, new in mapping.items():
        os.rename(os.path.join(directory, new), os.path.join(directory, old))
    return mapping


def main(argv=None):
    p = argparse.ArgumentParser(description="Bulk rename files safely.")
    p.add_argument("--dir", required=True)
    p.add_argument("--find", default="")
    p.add_argument("--replace", default="")
    p.add_argument("--prefix", default="")
    p.add_argument("--suffix", default="")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--undo-file", default="undo.json")
    p.add_argument("--undo", action="store_true")
    args = p.parse_args(argv)
    if args.undo:
        done = undo_rename(args.dir, args.undo_file)
        print(f"Restored {len(done)} file(s).")
        return 0
    mapping = build_mapping(args.dir, args.find, args.replace, args.prefix, args.suffix)
    for old, new in mapping.items():
        print(f"{old} -> {new}")
    if args.dry_run or not mapping:
        print(f"Dry run: {len(mapping)} file(s) would be renamed. No changes made." if args.dry_run else "No files to rename.")
        return 0
    apply_mapping(args.dir, mapping, args.undo_file)
    print(f"Renamed {len(mapping)} file(s). Undo mapping saved to {args.undo_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
