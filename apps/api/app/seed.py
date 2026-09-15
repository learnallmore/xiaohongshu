from __future__ import annotations

import json
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import CandidatePost
from app.seed_materials import upsert_materials

# 负例仅供本地回归 taste；不是日更候选。日更由 app.jobs.daily_generate 落库。
_NEGATIVES: list[dict] = [
    {
        "id": "cand-neg-city-clickbait",
        "domain": "cityscape",
        "domain_label": "负例 · 攻略腔城市",
        "title": "必看！绝美夜景封神机位速看",
        "body": (
            "全网最全打卡攻略来了！氛围感拉满高级感满满，"
            "不去后悔一辈子。热门景点必打卡，绝美夜景随便拍都出片。"
        ),
        "tags": ["必打卡", "夜景"],
        "rationale": "故意低质负例",
        "niche_score": 20,
    },
]


def seed_if_empty(db: Session) -> None:
    """启动只同步素材库；不覆盖今日候选（日更走 daily_generate）。"""
    upsert_materials(db)


def list_today_candidates(db: Session) -> list[CandidatePost]:
    """今日审阅：最多 3 条 pending/draft/published（排除 neg）。"""
    today = date.today()
    stmt = (
        select(CandidatePost)
        .where(CandidatePost.date_batch == today)
        .where(CandidatePost.status.in_(("pending", "draft", "published")))
        .options(selectinload(CandidatePost.images))
        .order_by(CandidatePost.created_at.desc())
    )
    posts = [
        p
        for p in db.scalars(stmt).all()
        if not p.id.startswith("cand-neg-")
    ][:3]
    return posts
