"""拒绝指纹：拒绝候选后永久跳过同主题。"""

from __future__ import annotations

import hashlib
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CandidatePost, RejectedFingerprint


def title_hash(title: str) -> str:
    return hashlib.sha256((title or "").strip().encode("utf-8")).hexdigest()[:32]


def is_rejected(
    db: Session, *, theme_key: str | None, title: str | None = None
) -> bool:
    checks: list[tuple[str, str]] = []
    if theme_key:
        checks.append(("theme_key", theme_key))
    if title:
        checks.append(("title_hash", title_hash(title)))
    for kind, val in checks:
        row = db.scalar(
            select(RejectedFingerprint).where(
                RejectedFingerprint.kind == kind,
                RejectedFingerprint.value == val,
            )
        )
        if row:
            return True
    return False


def record_rejection(
    db: Session,
    *,
    theme_key: str | None,
    title: str | None,
    note_ids: list[str] | None = None,
    reason: str = "user_rejected",
) -> None:
    rows: list[RejectedFingerprint] = []
    if theme_key:
        rows.append(
            RejectedFingerprint(
                id=f"rej-{uuid.uuid4().hex[:12]}",
                kind="theme_key",
                value=theme_key,
                reason=reason,
            )
        )
    if title:
        rows.append(
            RejectedFingerprint(
                id=f"rej-{uuid.uuid4().hex[:12]}",
                kind="title_hash",
                value=title_hash(title),
                reason=reason,
            )
        )
    for nid in note_ids or []:
        if nid:
            rows.append(
                RejectedFingerprint(
                    id=f"rej-{uuid.uuid4().hex[:12]}",
                    kind="note_id",
                    value=nid,
                    reason=reason,
                )
            )
    for row in rows:
        exists = db.scalar(
            select(RejectedFingerprint).where(
                RejectedFingerprint.kind == row.kind,
                RejectedFingerprint.value == row.value,
            )
        )
        if exists is None:
            db.add(row)


def hard_delete_candidate(
    db: Session, post: CandidatePost, reason: str = "user_rejected"
) -> None:
    record_rejection(
        db,
        theme_key=post.theme_key,
        title=post.title,
        reason=reason,
    )
    db.delete(post)
    db.commit()
