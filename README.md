# bulk-file-renamer

Safe bulk rename with preview/dry-run and an undo mapping JSON.

## What it does

Renames files in a folder using find/replace, a prefix, and/or a suffix.
Dry-run prints the planned renames without changing anything. A real run
writes an undo JSON file so the renames can be reversed.

## How to run

```bash
python3 main.py --dir ./files --find old --replace new --dry-run
python3 main.py --dir ./files --prefix new_ --undo-file undo.json
python3 main.py --dir ./files --undo --undo-file undo.json
```

## Example output (sample from test fixture data)

```text
a.txt -> new_a.txt
b.txt -> new_b.txt
Renamed 2 file(s). Undo mapping saved to undo.json
```

Standard library only. No network access.
