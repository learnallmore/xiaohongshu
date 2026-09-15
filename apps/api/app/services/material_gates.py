"""素材入库门禁：领域白名单、禁题材、情感正向/平。"""

from __future__ import annotations

ALLOWED_MATERIAL_DOMAINS = frozenset(
    {"cityscape", "interior", "music", "meta", "extended"}
)

# 已下线极地域 + 南极相关一律拒
RETIRED_TOPIC_MARKERS = (
    "南极",
    "antarctica",
    "antarct",
    "极地风光",
    "南极冰原",
    "斯瓦尔巴",
    "冰岛极光",
    "极光 挪威",
    "极昼",
    "极夜",
    "苔原",
)

# 负向情绪主导（猎奇/惊悚/灾难等）；氛围克制的「平」与欣赏向「正向」可通过
NEGATIVE_EMOTION_MARKERS = (
    "诡异",
    "猎奇",
    "恐怖",
    "吓人",
    "血腥",
    "血瀑",
    "blood falls",
    "消融",
    "彻底消融",
    "无人能解释",
    "绝望",
    "崩溃",
    "灾难",
    "死亡",
    "阴暗",
    "恶心",
    "惊悚",
    "丧到",
    "哭瞎",
)


def _blob(*parts: str | None) -> str:
    return " ".join(p for p in parts if p).lower()


def material_reject_reason(
    *,
    domain: str,
    title: str,
    body_excerpt: str | None = None,
    keyword: str | None = None,
    notes: str | None = None,
    likes_hint: int | None = None,
    quality_score: int | None = None,
    min_likes: int | None = None,
    min_quality: int | None = None,
) -> str | None:
    """返回拒收原因；通过则 None。"""
    if domain == "polar" or domain not in ALLOWED_MATERIAL_DOMAINS:
        return f"领域不可用：{domain}（已下线 polar；允许 {sorted(ALLOWED_MATERIAL_DOMAINS)}）"

    text = _blob(title, body_excerpt, keyword, notes)
    for m in RETIRED_TOPIC_MARKERS:
        if m.lower() in text:
            return f"禁题材命中：{m}"

    raw = " ".join(p for p in (title, body_excerpt, keyword, notes) if p)
    raw_l = raw.lower()
    for m in NEGATIVE_EMOTION_MARKERS:
        if m.lower() in raw_l:
            return f"情感须正向或平，负向命中：{m}"

    # 互动/质量门槛（日更对照素材要够硬）
    if min_likes is not None and (likes_hint or 0) < min_likes:
        return f"互动过低：likes={likes_hint or 0} < {min_likes}"
    if min_quality is not None and (quality_score or 0) < min_quality:
        return f"质量分过低：quality={quality_score or 0} < {min_quality}"

    # 无封面的帖难以图文同源
    return None


def material_allowed(
    *,
    domain: str,
    title: str,
    body_excerpt: str | None = None,
    keyword: str | None = None,
    notes: str | None = None,
) -> bool:
    return (
        material_reject_reason(
            domain=domain,
            title=title,
            body_excerpt=body_excerpt,
            keyword=keyword,
            notes=notes,
        )
        is None
    )
