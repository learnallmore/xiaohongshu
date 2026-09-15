"""品味打分：对照 ReferenceMaterial，判定候选是否够得上素材表品味。"""

from __future__ import annotations

import json
import re
import statistics
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CandidatePost, ReferenceMaterial

AI_TASTE_PENALTY_PHRASES = (
    "材质在呼吸",
    "岁月静好",
    "治愈心灵",
    "氛围感拉满",
    "高级感满满",
    "绝绝子",
    "封神了",
    "必看合集",
    "震惊",
)

PROVENANCE_MARKERS = ("图源", "来源", "Unsplash", "授权", "License", "摄影师", "图库")
HONESTY_MARKERS = ("不是我家", "不是我的", "不是实拍", "图库", "气氛板", "别当攻略", "先说清楚")

CITY_HINTS = (
    "上海",
    "北京",
    "深圳",
    "广州",
    "杭州",
    "成都",
    "重庆",
    "武汉",
    "南京",
    "苏州",
    "天津",
    "西安",
    "青岛",
    "厦门",
    "香港",
    "澳门",
    "台北",
    "陆家嘴",
    "外滩",
    "浦东",
)

INTERIOR_HINTS = ("包豪斯", "巴洛克", "折衷", "野兽派", "北欧", "日式", "现代主义", "材质", "比例")
MUSIC_HINTS = ("厂牌", "listening bar", "地下", "爵士", "R&B", "电子", "专辑", "制作人")
POLAR_HINTS = ("极地", "冰原", "极光", "极昼", "极夜", "苔原", "南极", "北极")

def _affirmative_phrase_hit(text: str, phrase: str) -> bool:
    idx = text.find(phrase)
    if idx < 0:
        return False
    window = text[max(0, idx - 8) : idx]
    if any(n in window for n in ("别", "不要", "忌", "禁止", "避免", "并非")):
        return False
    return True


CLICKBAIT = ("必看", "绝了", "封神", "跪了", "速看", "千万别")


@dataclass
class TasteResult:
    score: int
    passed: bool
    benchmark: int
    features: dict = field(default_factory=dict)

    def features_json(self) -> str:
        payload = {
            **self.features,
            "benchmark": self.benchmark,
            "passed": self.passed,
        }
        return json.dumps(payload, ensure_ascii=False)


def _tags(post: CandidatePost) -> list[str]:
    try:
        data = json.loads(post.tags_json or "[]")
        return [str(x) for x in data] if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _domain_materials(db: Session, domain: str) -> list[ReferenceMaterial]:
    stmt = select(ReferenceMaterial).where(ReferenceMaterial.domain == domain)
    rows = list(db.scalars(stmt).all())
    if rows:
        return rows
    # meta / 审美积累 作为跨域品味底线
    stmt = select(ReferenceMaterial).where(
        ReferenceMaterial.domain.in_(("meta", "extended"))
    )
    return list(db.scalars(stmt).all())


def domain_benchmark(db: Session, domain: str) -> int:
    mats = _domain_materials(db, domain)
    if not mats:
        return 72
    scores = sorted(m.quality_score for m in mats)
    return max(72, int(statistics.median(scores)))


def _material_tag_set(mats: list[ReferenceMaterial]) -> set[str]:
    tags: set[str] = set()
    for m in mats:
        try:
            data = json.loads(m.taste_tags_json or "[]")
            if isinstance(data, list):
                tags.update(str(x) for x in data)
        except json.JSONDecodeError:
            continue
    return tags


def score_candidate(db: Session, post: CandidatePost) -> TasteResult:
    """确定性规则打分；足够对标素材表中位线，不依赖 LLM。"""
    body = post.body or ""
    title = post.title or ""
    tags = _tags(post)
    images = list(post.images or [])
    mats = _domain_materials(db, post.domain)
    benchmark = domain_benchmark(db, post.domain)
    mat_tags = _material_tag_set(mats)

    features: dict = {}
    parts: list[tuple[str, float, float]] = []  # name, weight, 0..1

    # 1. 正文图源可追溯（读者可见）
    prov = sum(1 for m in PROVENANCE_MARKERS if m in body)
    prov_s = min(1.0, prov / 2.0)
    features["provenance"] = round(prov_s, 3)
    parts.append(("provenance", 0.18, prov_s))

    # 2. 诚实人设（室内/极地更重）
    honest = any(m in body or m in title for m in HONESTY_MARKERS)
    honest_s = 1.0 if honest else (0.55 if post.domain in ("interior", "polar") else 0.75)
    features["honesty"] = round(honest_s, 3)
    parts.append(("honesty", 0.12, honest_s))

    # 3. 领域特异
    if post.domain == "cityscape":
        domain_s = 1.0 if any(h in body or h in title or h in "".join(tags) for h in CITY_HINTS) else 0.2
    elif post.domain == "interior":
        domain_s = 1.0 if any(h in body or h in title for h in INTERIOR_HINTS) else 0.25
    elif post.domain == "music":
        domain_s = 1.0 if any(h in body or h in title for h in MUSIC_HINTS) else 0.25
    elif post.domain == "polar":
        domain_s = 1.0 if any(h in body or h in title for h in POLAR_HINTS) else 0.25
    else:
        domain_s = 0.7
    features["domain_specificity"] = round(domain_s, 3)
    parts.append(("domain_specificity", 0.16, domain_s))

    # 4. 标题克制
    tlen = len(title.strip())
    length_ok = 6 <= tlen <= 32
    bait = any(b in title for b in CLICKBAIT)
    title_s = (0.85 if length_ok else 0.4) * (0.3 if bait else 1.0)
    features["title_craft"] = round(title_s, 3)
    parts.append(("title_craft", 0.10, title_s))

    # 5. 标签卫生
    n_tags = len(tags)
    tag_s = 1.0 if 3 <= n_tags <= 8 else (0.5 if 1 <= n_tags <= 10 else 0.2)
    features["tag_hygiene"] = round(tag_s, 3)
    parts.append(("tag_hygiene", 0.08, tag_s))

    # 6. 图组完整 + 元数据
    if len(images) >= 3 and all(img.source and img.license for img in images):
        img_s = 1.0
    elif len(images) >= 2:
        img_s = 0.55
    else:
        img_s = 0.15
    features["image_completeness"] = round(img_s, 3)
    parts.append(("image_completeness", 0.14, img_s))

    # 7. 去 AI 味（反例引用「别…」不扣分）
    hits = [
        p
        for p in AI_TASTE_PENALTY_PHRASES
        if _affirmative_phrase_hit(body, p) or _affirmative_phrase_hit(title, p)
    ]
    ai_s = max(0.0, 1.0 - 0.25 * len(hits))
    features["anti_ai"] = round(ai_s, 3)
    features["ai_hits"] = hits
    parts.append(("anti_ai", 0.12, ai_s))

    # 8. 与高分素材 taste_tags 对齐（结构层，非搬文）
    inferred: set[str] = set()
    if re.search(r"Day\.?\s*\d+|第\s*\d+\s*天|系列", title + body, re.I):
        inferred.add("series-day")
    if any(x in body for x in ("拼贴", "collage", "图组")):
        inferred.add("collage")
    if any(x in body or x in title for x in ("低饱和", "冷调", "雾", "蓝色")):
        inferred.add("low-sat")
    if post.domain == "cityscape" and domain_s >= 1.0:
        inferred.add("china-place")
    if any(x in body for x in PROVENANCE_MARKERS):
        inferred.add("provenance-stated")
    if honest:
        inferred.add("honest-framing")
    if mats:
        top = sorted(mats, key=lambda m: m.quality_score, reverse=True)[:5]
        top_tags = _material_tag_set(top)
        if top_tags:
            overlap = len(inferred & top_tags) / max(1, min(4, len(top_tags)))
        else:
            overlap = 0.5
    else:
        overlap = 0.5
        top_tags = set()
    align_s = min(1.0, 0.35 + overlap)
    features["material_alignment"] = round(align_s, 3)
    features["inferred_tags"] = sorted(inferred)
    features["material_tag_sample"] = sorted(list(top_tags | mat_tags))[:12]
    parts.append(("material_alignment", 0.10, align_s))

    total_w = sum(w for _, w, _ in parts)
    raw = sum(w * s for _, w, s in parts) / total_w
    score = int(round(100 * raw))
    score = max(0, min(100, score))
    passed = score >= benchmark
    features["weights"] = {n: w for n, w, _ in parts}
    features["model"] = "taste_v0_rule"

    return TasteResult(score=score, passed=passed, benchmark=benchmark, features=features)


def apply_taste_to_post(db: Session, post: CandidatePost) -> TasteResult:
    result = score_candidate(db, post)
    post.taste_score = result.score
    post.taste_pass = result.passed
    post.taste_features_json = result.features_json()
    return result


def rescore_all_candidates(db: Session) -> list[dict]:
    from sqlalchemy.orm import selectinload

    stmt = select(CandidatePost).options(selectinload(CandidatePost.images))
    out: list[dict] = []
    for post in db.scalars(stmt).all():
        r = apply_taste_to_post(db, post)
        out.append(
            {
                "id": post.id,
                "domain": post.domain,
                "taste_score": r.score,
                "taste_pass": r.passed,
                "benchmark": r.benchmark,
            }
        )
    db.commit()
    return out
