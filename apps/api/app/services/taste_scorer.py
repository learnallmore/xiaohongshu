"""品味打分 v2：素材库 P75 + 人声硬过滤；图源认元数据，不认正文说明书。"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CandidatePost, ReferenceMaterial
from app.services.voice_filter import scan_voice
from app.source_registry import source_text_allowed, url_host_allowed
from app.theme_packs import THEME_PACKS

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

# 正文里的地点/对象事实（不是版权说明书）
PLACE_FACT_MARKERS = (
    "上海",
    "浦西",
    "外滩",
    "黄浦江",
    "陆家嘴",
    "延安高架",
    "乍浦",
    "内透",
    "蓝调",
)

# 极短诚实口吻即可；禁止长篇「先说这不是我家」辩护
HONESTY_MARKERS = ("参考图", "不是我家", "气氛板", "别当攻略", "不是实拍")

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
    "浦西",
    "钱塘",
)

INTERIOR_HINTS = (
    "包豪斯",
    "巴洛克",
    "折衷",
    "野兽派",
    "北欧",
    "日式",
    "现代主义",
    "线脚",
    "中古",
    "材质",
    "比例",
)
MUSIC_HINTS = (
    "厂牌",
    "listening bar",
    "Listening Bar",
    "地下",
    "爵士",
    "R&B",
    "电子",
    "专辑",
    "制作人",
    "黑胶",
    "House",
    "house",
    "Breakbot",
    "Stardust",
    "Cassius",
)
LOW_QUALITY_SIGNALS = (
    "必打卡",
    "绝美夜景",
    "保姆级",
    "封神",
    "跪了",
    "速看",
    "千万别",
    "不看后悔",
    "震惊",
    "全网最全",
    "热歌推荐",
    "洗脑神曲",
)

CLICKBAIT = ("必看", "绝了", "封神", "跪了", "速看", "千万别")

CURATION_TAGS = frozenset(
    {
        "atmosphere-title",
        "collage",
        "visual-board",
        "curator-voice",
        "series-day",
        "low-sat",
        "named-artist",
        "provenance-stated",
        "honest-framing",
        "style-named",
        "china-place",
        "listening-space",
        "niche-label",
        "material-talk",
        "skyline",
    }
)


def _affirmative_phrase_hit(text: str, phrase: str) -> bool:
    idx = text.find(phrase)
    if idx < 0:
        return False
    window = text[max(0, idx - 8) : idx]
    if any(n in window for n in ("别", "不要", "忌", "禁止", "避免", "并非")):
        return False
    return True


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
    stmt = select(ReferenceMaterial).where(
        ReferenceMaterial.domain.in_(("meta", "extended"))
    )
    return list(db.scalars(stmt).all())


def _percentile(sorted_vals: list[int], p: float) -> int:
    if not sorted_vals:
        return 85
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return int(sorted_vals[int(k)])
    return int(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f))


def domain_benchmark(db: Session, domain: str) -> int:
    """同领域真实素材 quality_score 的 P75，下限 85。"""
    mats = _domain_materials(db, domain)
    if not mats:
        return 85
    scores = sorted(m.quality_score for m in mats)
    return max(85, _percentile(scores, 0.75))


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


def _infer_tags(
    post: CandidatePost,
    domain_s: float,
    honest: bool,
    body: str,
    title: str,
    meta_ok: bool,
) -> set[str]:
    inferred: set[str] = set()
    if re.search(r"Day\.?\s*\d+|第\s*\d+\s*天|系列", title + body, re.I):
        inferred.add("series-day")
    if any(x in body for x in ("拼贴", "collage", "图组")):
        inferred.add("collage")
        inferred.add("visual-board")
    if any(x in body or x in title for x in ("低饱和", "冷调", "雾", "蓝色", "蓝调")):
        inferred.add("low-sat")
    if post.domain == "cityscape" and domain_s >= 1.0:
        inferred.add("china-place")
        inferred.add("skyline")
    if meta_ok:
        inferred.add("provenance-stated")
    if honest:
        inferred.add("honest-framing")
    if any(x in body or x in title for x in INTERIOR_HINTS):
        inferred.add("style-named")
        inferred.add("material-talk")
    if any(x in body or x in title for x in MUSIC_HINTS):
        inferred.add("listening-space")
        inferred.add("niche-label")
        if any(
            x in body or x in title
            for x in ("Breakbot", "Stardust", "Cassius", "制作人", "专辑")
        ):
            inferred.add("named-artist")
    if any(x in body for x in ("策展", "厂牌", "值得收藏", "合集")):
        inferred.add("curator-voice")
    if 4 <= len(title.strip()) <= 18 and not any(b in title for b in CLICKBAIT):
        inferred.add("atmosphere-title")
    return inferred


def _material_keyword_overlap(
    post: CandidatePost, mats: list[ReferenceMaterial]
) -> tuple[float, list[str]]:
    blob = f"{post.title} {post.body}".lower()
    top = sorted(mats, key=lambda m: ((m.likes_hint or 0), m.quality_score), reverse=True)[
        :6
    ]
    hits: list[str] = []
    score_bits: list[float] = []
    for m in top:
        tokens: list[str] = []
        for raw in (m.title_observed, m.body_excerpt or ""):
            for tok in re.findall(r"[\u4e00-\u9fff]{2,6}|[A-Za-z]{3,}", raw or ""):
                if tok.lower() in ("the", "and", "for", "with", "http", "https"):
                    continue
                tokens.append(tok)
        tokens = list(dict.fromkeys(tokens))[:12]
        matched = [t for t in tokens if t.lower() in blob or t in blob]
        if matched:
            hits.append(f"{m.note_id or m.id}:{','.join(matched[:4])}")
            score_bits.append(min(1.0, len(matched) / 3.0))
        else:
            score_bits.append(0.0)
    if not score_bits:
        return 0.35, []
    return sum(score_bits) / len(score_bits), hits[:6]


def _meta_provenance(images: list) -> float:
    """合法图源写在图片 source/license 元数据；正文不再要求说明书。"""
    if not images:
        return 0.0
    ok = sum(1 for img in images if (img.source or "").strip() and (img.license or "").strip())
    return ok / max(1, len(images))


def _body_density(body: str) -> float:
    """短句、具体物：惩罚过长说明书与形容词堆砌。"""
    text = (body or "").strip()
    if not text:
        return 0.0
    n = len(text)
    # 真人笔记常见 60–280 字；过长易变成说明书
    if 50 <= n <= 320:
        length_s = 1.0
    elif n < 50:
        length_s = 0.45
    elif n <= 480:
        length_s = 0.55
    else:
        length_s = 0.2
    sentences = [s for s in re.split(r"[。！？\n]+", text) if s.strip()]
    short_ratio = (
        sum(1 for s in sentences if len(s.strip()) <= 40) / max(1, len(sentences))
    )
    return min(1.0, 0.55 * length_s + 0.45 * short_ratio)


def _entity_alignment(post: CandidatePost, images: list) -> tuple[float, list[str]]:
    """正文实体须与图 source / theme pack 交集；防耳机图配 Breakbot。"""
    blob = f"{post.title or ''} {post.body or ''}"
    theme_key = getattr(post, "theme_key", None) or ""
    entities: list[str] = []
    if theme_key and theme_key in THEME_PACKS:
        entities = list(THEME_PACKS[theme_key].get("entities") or [])
    if not entities and theme_key and ":" in theme_key:
        # 日更动态 theme：domain:keyword
        tail = theme_key.split(":", 1)[1]
        entities = [tail] + [p for p in tail.replace("-", " ").split() if len(p) >= 2]
    if not entities:
        # 回退：从标签抽
        try:
            import json

            tags = json.loads(post.tags_json or "[]")
            entities = [str(t) for t in tags] if isinstance(tags, list) else []
        except Exception:
            entities = []
    if not entities:
        return 0.2, ["无 theme entities"]

    body_hits = [e for e in entities if e.lower() in blob.lower() or e in blob]
    src_blob = " ".join(
        f"{getattr(img, 'source', '')} {getattr(img, 'url', '')}" for img in images
    ).lower()
    src_hits = [e for e in entities if e.lower() in src_blob]
    # 正文至少命中 2 个实体；图 source/url 至少命中 1 个（备援图也要带 theme 词）
    body_s = min(1.0, len(body_hits) / 2.0)
    src_s = 1.0 if src_hits else 0.0
    # 负例：通用库存关键词
    stock = ("headphones", "concert lights", "music performance", "耳机", "演唱会灯")
    stock_hit = any(s in src_blob for s in stock) and not src_hits
    if stock_hit:
        return 0.0, ["图源像通用库存且未命中主题实体"]
    score = 0.55 * body_s + 0.45 * src_s
    detail = [f"body:{','.join(body_hits[:5])}", f"src:{','.join(src_hits[:5])}"]
    return score, detail


def _source_whitelist_score(images: list) -> tuple[float, list[str]]:
    if not images:
        return 0.0, ["无图"]
    fails: list[str] = []
    ok = 0
    for img in images:
        src = (getattr(img, "source", None) or "").strip()
        url = (getattr(img, "url", None) or "").strip()
        good = source_text_allowed(src) or url_host_allowed(url)
        if good:
            ok += 1
        else:
            fails.append((src or url or "?")[:80])
    return ok / max(1, len(images)), fails


def score_candidate(db: Session, post: CandidatePost) -> TasteResult:
    body = post.body or ""
    title = post.title or ""
    tags = _tags(post)
    images = list(post.images or [])
    mats = _domain_materials(db, post.domain)
    benchmark = domain_benchmark(db, post.domain)
    mat_tags = _material_tag_set(mats)
    top_mats = sorted(
        mats, key=lambda m: ((m.likes_hint or 0), m.quality_score), reverse=True
    )[:5]

    voice = scan_voice(title, body)

    features: dict = {
        "model": "taste_v3_source_theme",
        "theme_key": getattr(post, "theme_key", None),
        "material_sample": [
            {
                "note_id": m.note_id,
                "title": m.title_observed,
                "likes": m.likes_hint,
                "quality_score": m.quality_score,
                "source_url": m.source_url,
                "source_site": getattr(m, "source_site", None),
            }
            for m in top_mats
        ],
        "fail_reasons": [],
        **voice.as_features(),
    }
    parts: list[tuple[str, float, float]] = []

    # 0. 人声硬过滤（阻塞）
    voice_s = 1.0 if voice.passed else 0.0
    features["voice"] = round(voice_s, 3)
    parts.append(("voice", 0.16, voice_s))
    if not voice.passed:
        features["fail_reasons"].append(
            "人声硬过滤未过: " + "; ".join(voice.hits[:5])
        )

    # 0b. 白名单宿主
    wl_s, wl_fails = _source_whitelist_score(images)
    features["source_whitelist"] = round(wl_s, 3)
    features["source_whitelist_fails"] = wl_fails[:4]
    parts.append(("source_whitelist", 0.10, wl_s))
    if wl_s < 0.99:
        features["fail_reasons"].append("图片来源不在数据源白名单/授权备援")

    # 0c. 图文实体对齐
    ent_s, ent_detail = _entity_alignment(post, images)
    features["entity_alignment"] = round(ent_s, 3)
    features["entity_detail"] = ent_detail
    parts.append(("entity_alignment", 0.12, ent_s))
    if ent_s < 0.5:
        features["fail_reasons"].append("图文主题实体未对齐（疑似拼凑）")

    # 1. 图源可追溯 → 图片元数据（非正文说明书）
    prov_s = _meta_provenance(images)
    features["provenance"] = round(prov_s, 3)
    parts.append(("provenance", 0.08, prov_s))
    if prov_s < 0.5:
        features["fail_reasons"].append("图片元数据缺少 source/license")

    # 城市帖：正文要有可指认地点事实（不是版权段）
    if post.domain == "cityscape":
        place_ok = any(m in body or m in title for m in PLACE_FACT_MARKERS) or any(
            h in body or h in title for h in CITY_HINTS
        )
        if not place_ok:
            features["fail_reasons"].append("城市帖正文缺少可指认地点")

    # 2. 诚实人设（极短即可；室内建议有一句）
    honest = any(m in body or m in title for m in HONESTY_MARKERS)
    if post.domain == "interior":
        honest_s = 1.0 if honest else 0.4
    else:
        honest_s = 1.0 if honest else 0.75
    features["honesty"] = round(honest_s, 3)
    parts.append(("honesty", 0.06, honest_s))
    if post.domain == "interior" and honest_s < 0.5:
        features["fail_reasons"].append("室内帖缺少极短诚实口吻（如参考图）")

    # 3. 领域特异
    blob = body + title + "".join(tags)
    if post.domain == "cityscape":
        domain_s = 1.0 if any(h in blob for h in CITY_HINTS) else 0.15
    elif post.domain == "interior":
        domain_s = 1.0 if any(h in blob for h in INTERIOR_HINTS) else 0.15
    elif post.domain == "music":
        domain_s = 1.0 if any(h in blob for h in MUSIC_HINTS) else 0.15
    else:
        domain_s = 0.6
    features["domain_specificity"] = round(domain_s, 3)
    parts.append(("domain_specificity", 0.10, domain_s))
    if domain_s < 0.5:
        features["fail_reasons"].append("领域关键词不足以对齐同域真实素材")

    # 4. 标题克制
    tlen = len(title.strip())
    length_ok = 6 <= tlen <= 28
    bait = any(b in title for b in CLICKBAIT)
    title_s = (0.9 if length_ok else 0.35) * (0.2 if bait else 1.0)
    features["title_craft"] = round(title_s, 3)
    parts.append(("title_craft", 0.06, title_s))
    if bait:
        features["fail_reasons"].append("标题含攻略/封神等低质信号")

    # 5. 标签卫生
    n_tags = len(tags)
    tag_s = 1.0 if 3 <= n_tags <= 8 else (0.45 if 1 <= n_tags <= 10 else 0.15)
    features["tag_hygiene"] = round(tag_s, 3)
    parts.append(("tag_hygiene", 0.04, tag_s))

    # 6. 图组完整
    if len(images) >= 3 and all(img.source and img.license for img in images):
        img_s = 1.0
    elif len(images) >= 2:
        img_s = 0.45
    else:
        img_s = 0.1
    features["image_completeness"] = round(img_s, 3)
    parts.append(("image_completeness", 0.08, img_s))
    if img_s < 0.5:
        features["fail_reasons"].append("图组不足或缺少 source/license 元数据")

    # 7. 去 AI 味短语
    hits = [
        p
        for p in AI_TASTE_PENALTY_PHRASES
        if _affirmative_phrase_hit(body, p) or _affirmative_phrase_hit(title, p)
    ]
    ai_s = max(0.0, 1.0 - 0.3 * len(hits))
    features["anti_ai"] = round(ai_s, 3)
    features["ai_hits"] = hits
    parts.append(("anti_ai", 0.06, ai_s))
    if hits:
        features["fail_reasons"].append(f"命中 AI 味短语: {','.join(hits)}")

    # 8. 信息密度（对标真实短帖）
    dens_s = _body_density(body)
    features["body_density"] = round(dens_s, 3)
    parts.append(("body_density", 0.05, dens_s))

    # 9. 与真实高互动素材 taste_tags 对齐
    meta_ok = prov_s >= 0.99
    inferred = _infer_tags(post, domain_s, honest, body, title, meta_ok)
    top_tags = _material_tag_set(top_mats) if top_mats else mat_tags
    relevant = (top_tags | mat_tags) & CURATION_TAGS
    if relevant:
        overlap = len(inferred & relevant) / max(3, min(5, len(relevant)))
    else:
        overlap = 0.25
    align_s = min(1.0, overlap)
    features["material_alignment"] = round(align_s, 3)
    features["inferred_tags"] = sorted(inferred)
    features["material_tag_sample"] = sorted(relevant)[:14]
    parts.append(("material_alignment", 0.05, align_s))
    if align_s < 0.45:
        features["fail_reasons"].append(
            "与同域高互动素材 taste_tags 重叠不足（缺策展/诚实/领域气质）"
        )

    # 10. 关键词级对齐
    kw_s, kw_hits = _material_keyword_overlap(post, mats)
    features["material_keyword_overlap"] = round(kw_s, 3)
    features["material_keyword_hits"] = kw_hits
    parts.append(("material_keyword_overlap", 0.04, kw_s))

    # 11. 低质惩罚
    lq = [s for s in LOW_QUALITY_SIGNALS if _affirmative_phrase_hit(body, s) or s in title]
    lq_s = max(0.0, 1.0 - 0.35 * len(lq))
    features["low_quality_penalty"] = round(lq_s, 3)
    features["low_quality_hits"] = lq
    parts.append(("low_quality_penalty", 0.06, lq_s))
    if lq:
        features["fail_reasons"].append(f"低质信号: {','.join(lq)}")

    total_w = sum(w for _, w, _ in parts)
    raw = sum(w * s for _, w, s in parts) / total_w
    score = int(round(100 * raw))
    score = max(0, min(100, score))
    # voice / 白名单 / 图文对齐 硬过滤未过 → 强制未过线
    hard_ok = voice.passed and wl_s >= 0.99 and ent_s >= 0.5
    passed = score >= benchmark and hard_ok
    features["weights"] = {n: w for n, w, _ in parts}
    if passed:
        features["fail_reasons"] = []
    else:
        features["fail_reasons"] = features["fail_reasons"][:8]
        if score < benchmark:
            features["fail_reasons"].append(
                f"taste_score={score} < benchmark(P75)={benchmark}"
            )

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
