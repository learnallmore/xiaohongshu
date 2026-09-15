#!/usr/bin/env python3
"""Merge browser-scraped note cards into collected_batch.json (dedupe by note_id)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collected_batch.json"


def main() -> None:
    incoming = json.loads(sys.stdin.read() or "[]")
    if not isinstance(incoming, list):
        raise SystemExit("stdin must be JSON list")
    existing: list[dict] = []
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8") or "[]")
    by_id = {x["note_id"]: x for x in existing if x.get("note_id")}
    for item in incoming:
        nid = item.get("note_id")
        if not nid:
            continue
        prev = by_id.get(nid, {})
        merged = {**prev, **{k: v for k, v in item.items() if v is not None}}
        by_id[nid] = merged
    rows = list(by_id.values())
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"total={len(rows)}")


if __name__ == "__main__":
    main()
