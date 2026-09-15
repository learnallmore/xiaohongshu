"""CLI: python -m app.jobs.ingest_candidates [path.json]

默认读取 apps/api/data/agent_daily.json（由 Cursor Agent 写好后落库）。
"""

from __future__ import annotations

import sys
from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.schema_migrate import ensure_schema
from app.services.candidate_ingest import ingest_from_json_file

import app.models  # noqa: F401


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    default = root / "data" / "agent_daily.json"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    if not path.is_file():
        print(f"找不到候选文件: {path}")
        print("请先让 Cursor Agent 按 daily-agent-generate Skill 写好 JSON。")
        return 1

    Base.metadata.create_all(bind=engine)
    ensure_schema(engine)
    db = SessionLocal()
    try:
        result = ingest_from_json_file(db, path)
        print(result.message)
        print("post_ids:", result.post_ids)
        return 0 if result.ok else 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
