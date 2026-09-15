"""轻量列补齐：create_all 不会 ALTER 已有表。"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


_CANDIDATE_EXTRA_COLUMNS: list[tuple[str, str]] = [
    ("taste_score", "INT NOT NULL DEFAULT 0"),
    ("taste_pass", "TINYINT(1) NOT NULL DEFAULT 0"),
    ("taste_features_json", "TEXT NULL"),
]


def ensure_schema(engine: Engine) -> None:
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'candidate_posts'"
            )
        ).fetchall()
        existing = {r[0] for r in rows}
        if not existing:
            return
        for name, ddl in _CANDIDATE_EXTRA_COLUMNS:
            if name not in existing:
                conn.execute(
                    text(f"ALTER TABLE candidate_posts ADD COLUMN {name} {ddl}")
                )
