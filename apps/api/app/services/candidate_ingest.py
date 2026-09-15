"""把 Cursor Agent 写好的候选 JSON 落库（不调用外部 LLM API）。"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import CandidatePost, PostImage
from app.services.reject_store import is_rejected
from app.services.taste_scorer import apply_taste_to_post
from app.services.voice_filter import scan_voice


@dataclass
class IngestResult:
    ok: bool
    post_ids: list[str]
    message: str


def _clear_today_pending(db: Session, today: date) -> None:
    stmt = select(CandidatePost).where(
        CandidatePost.date_batch == today,
        CandidatePost.status == "pending",
    )
    for post in list(db.scalars(stmt).all()):
        if post.id.startswith("cand-neg-"):
            continue
        db.delete(post)
    db.commit()


def ingest_candidate_items(
    db: Session, items: list[dict], *, replace_today_pending: bool = True
) -> IngestResult:
    """
    items 每条字段：
      domain, title, body, tags[], images[{url,source,license,width?,height?}],
      theme_key?, domain_label?, rationale?, niche_score?
    """
    if len(items) != 3:
        return IngestResult(False, [], f"日更必须恰好 3 条，当前 {len(items)}")

    today = date.today()
    if replace_today_pending:
        _clear_today_pending(db, today)

    created: list[str] = []
    domains_seen: set[str] = set()

    for raw in items:
        domain = str(raw.get("domain") or "").strip()
        title = str(raw.get("title") or "").strip()
        body = str(raw.get("body") or "").strip()
        theme_key = (raw.get("theme_key") or f"agent:{domain}:{title[:24]}").strip()
        tags = raw.get("tags") or []
        if not isinstance(tags, list):
            tags = []
        tags = [str(t) for t in tags][:8]
        images = raw.get("images") or []
        if not domain or not title or not body:
            return IngestResult(False, created, "存在缺 domain/title/body 的条目")
        if not isinstance(images, list) or len(images) < 1:
            return IngestResult(False, created, f"「{title}」缺少 images")
        if is_rejected(db, theme_key=theme_key, title=title):
            return IngestResult(
                False, created, f"主题已被拒绝过，跳过：{theme_key} / {title}"
            )

        voice = scan_voice(title, body)
        if not voice.passed:
            return IngestResult(
                False,
                created,
                f"人声过滤未过「{title}」: " + "; ".join(voice.hits[:5]),
            )

        domains_seen.add(domain)
        post_id = str(raw.get("id") or f"agent-{today.isoformat()}-{uuid.uuid4().hex[:8]}")
        post = db.get(CandidatePost, post_id)
        if post is None:
            post = CandidatePost(id=post_id)
            db.add(post)
        else:
            post.images.clear()

        for i, img in enumerate(images[:6]):
            url = str(img.get("url") or "").strip()
            if not url:
                continue
            post.images.append(
                PostImage(
                    id=str(img.get("id") or f"img-{post_id}-{i}"),
                    post_id=post_id,
                    sort_order=int(img.get("sort_order", i)),
                    url=url,
                    width=int(img.get("width") or 1080),
                    height=int(img.get("height") or 1440),
                    source=str(img.get("source") or "agent"),
                    license=str(img.get("license") or "see-source"),
                )
            )
        if not post.images:
            return IngestResult(False, created, f"「{title}」图片 URL 无效")

        post.date_batch = today
        post.domain = domain
        post.domain_label = raw.get("domain_label") or domain
        post.status = "pending"
        post.title = title
        post.body = body
        post.tags_json = json.dumps(tags, ensure_ascii=False)
        post.cover_index = 0
        post.rationale = str(raw.get("rationale") or "Cursor Agent 日更落库")
        post.niche_score = int(raw.get("niche_score") or 80)
        post.theme_key = theme_key
        post.reject_reason = None
        db.commit()

        post = db.scalar(
            select(CandidatePost)
            .where(CandidatePost.id == post_id)
            .options(selectinload(CandidatePost.images))
        )
        assert post is not None
        apply_taste_to_post(db, post)
        db.commit()
        created.append(post_id)

    msg = f"已落库 {len(created)} 条 Agent 日更候选；领域 {sorted(domains_seen)}"
    return IngestResult(True, created, msg)


def ingest_from_json_file(db: Session, path: Path) -> IngestResult:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "candidates" in data:
        items = data["candidates"]
    elif isinstance(data, list):
        items = data
    else:
        return IngestResult(False, [], "JSON 须为数组或 {candidates:[...]}")
    if not isinstance(items, list):
        return IngestResult(False, [], "candidates 必须是数组")
    return ingest_candidate_items(db, items)
