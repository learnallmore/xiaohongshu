"""轻量列补齐：create_all 不会 ALTER 已有表。"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


_CANDIDATE_EXTRA_COLUMNS: list[tuple[str, str]] = [
    ("taste_score", "INT NOT NULL DEFAULT 0"),
    ("taste_pass", "TINYINT(1) NOT NULL DEFAULT 0"),
    ("taste_features_json", "TEXT NULL"),
    ("theme_key", "VARCHAR(128) NULL"),
]

_MATERIAL_EXTRA_COLUMNS: list[tuple[str, str]] = [
    ("note_id", "VARCHAR(64) NULL"),
    ("collects_hint", "INT NULL"),
    ("comments_hint", "INT NULL"),
    ("cover_url", "VARCHAR(1024) NULL"),
    ("images_json", "TEXT NULL"),
    ("body_excerpt", "TEXT NULL"),
    ("source_site", "VARCHAR(32) NULL"),
    ("theme_key", "VARCHAR(128) NULL"),
]


def _ensure_columns(
    conn, table: str, columns: list[tuple[str, str]]
) -> None:
    rows = conn.execute(
        text(
            "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t"
        ),
        {"t": table},
    ).fetchall()
    existing = {r[0] for r in rows}
    if not existing:
        return
    for name, ddl in columns:
        if name not in existing:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))


def ensure_schema(engine: Engine) -> None:
    with engine.begin() as conn:
        _ensure_columns(conn, "candidate_posts", _CANDIDATE_EXTRA_COLUMNS)
        _ensure_columns(conn, "reference_materials", _MATERIAL_EXTRA_COLUMNS)
        # note_id 索引（若不存在）
        idx = conn.execute(
            text(
                "SELECT COUNT(1) FROM information_schema.STATISTICS "
                "WHERE TABLE_SCHEMA = DATABASE() "
                "AND TABLE_NAME = 'reference_materials' "
                "AND INDEX_NAME = 'ix_reference_materials_note_id'"
            )
        ).scalar()
        if idx == 0:
            try:
                conn.execute(
                    text(
                        "CREATE INDEX ix_reference_materials_note_id "
                        "ON reference_materials (note_id)"
                    )
                )
            except Exception:
                pass
