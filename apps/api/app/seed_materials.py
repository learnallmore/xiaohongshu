"""参照素材种子：来自官方网页观察「审美积累」+ 四大领域结构笔记（无原文原图）。"""

from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import ReferenceMaterial

# 仅结构/审美特征；license_ok=False 表示不可搬运原作
MATERIALS: list[dict] = [
    # —— 审美积累（跨域 meta）——
    {
        "id": "mat-meta-misty-forest",
        "domain": "meta",
        "keyword": "审美积累",
        "title_observed": "𝓶𝓲𝓼𝓽𝔂 𝓯𝓸𝓻𝓮𝓼𝓽",
        "author_hint": "Externalsunshine:)",
        "likes_hint": 16000,
        "structure_notes": (
            "拼贴封面多图并置；标题用氛围词而非攻略句；"
            "视觉偏雾感/冷调/童话废墟混搭，适合当「封面密度」参照。"
        ),
        "taste_tags": ["collage", "low-sat", "atmosphere-title", "visual-board"],
        "quality_score": 88,
        "source_url": "https://www.xiaohongshu.com/search_result?keyword=%E5%AE%A1%E7%BE%8E%E7%A7%AF%E7%B4%AF",
        "notes": "搜索「审美积累」高赞拼贴板；只学结构。",
    },
    {
        "id": "mat-meta-blue-obsession",
        "domain": "meta",
        "keyword": "审美积累",
        "title_observed": "“人类为何迷恋蓝色”",
        "author_hint": "不药",
        "likes_hint": 93000,
        "structure_notes": (
            "单色母题提问式标题；封面大风景冷静；"
            "正文宜短、留白，忌鸡汤升华——作「主题一色」参照。"
        ),
        "taste_tags": ["low-sat", "mono-theme", "question-title", "landscape"],
        "quality_score": 92,
        "source_url": None,
        "notes": "高赞审美母题帖；学习提问标题+单色。",
    },
    {
        "id": "mat-meta-series-day",
        "domain": "meta",
        "keyword": "审美积累",
        "title_observed": "审美提升|Day.744|Ezgi Polat",
        "author_hint": "nRs（审美分享）",
        "likes_hint": None,
        "structure_notes": (
            "强系列感：Day.N + 作者/作品名；账号靠连载建立品味信任；"
            "适合「棱镜」日更编号结构，但禁止抄作品。"
        ),
        "taste_tags": ["series-day", "named-artist", "provenance-stated"],
        "quality_score": 86,
        "source_url": None,
        "notes": "连载编号是可学结构，非可抄内容。",
    },
    {
        "id": "mat-meta-ins-photographer",
        "domain": "meta",
        "keyword": "审美积累",
        "title_observed": "📷「INS值得收藏的摄影师」 | 审美积累",
        "author_hint": "📷Mr.飯忒稀",
        "likes_hint": None,
        "structure_notes": (
            "策展口吻：点名外部作者；标签「审美积累」作栏目；"
            "强调收藏/参照而非「我拍的」。"
        ),
        "taste_tags": ["curator-voice", "named-artist", "provenance-stated", "series-day"],
        "quality_score": 85,
        "source_url": None,
        "notes": "策展人设与图源诚实是核心。",
    },
    {
        "id": "mat-meta-cn-architecture",
        "domain": "cityscape",
        "keyword": "审美积累",
        "title_observed": "中式美学之京派巨构",
        "author_hint": "设计师陈欢",
        "likes_hint": None,
        "structure_notes": (
            "中国可指认建筑母题；标题点风格流派；"
            "封面建筑立面/屋顶线，避免网红机位土味滤镜。"
        ),
        "taste_tags": ["china-place", "architecture", "style-named", "low-sat"],
        "quality_score": 87,
        "source_url": None,
        "notes": "对齐 002 城市景观=中国。",
    },
    # —— 城市 ——
    {
        "id": "mat-city-skyline-struct",
        "domain": "cityscape",
        "keyword": "城市建筑美学",
        "title_observed": "结构参照：中国城市天际线克制机位",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "标题含城市名；正文写片区/机位；图源写给读者；"
            "忌「必打卡」「绝美夜景」堆砌；雨后/阴天冷调更贴审美积累高赞气质。"
        ),
        "taste_tags": ["china-place", "provenance-stated", "low-sat", "honest-framing"],
        "quality_score": 84,
        "source_url": None,
        "notes": "领域标尺：可指认中国地点+图源。",
    },
    {
        "id": "mat-city-waterfront",
        "domain": "cityscape",
        "keyword": "滨江天际线",
        "title_observed": "结构参照：滨水天际线少人叙事",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "一段真实路径细节即可；不写攻略体；"
            "3 图以上同一地点不同距离，封面选倒影/立面而非自拍。"
        ),
        "taste_tags": ["china-place", "waterfront", "multi-distance", "provenance-stated"],
        "quality_score": 82,
        "source_url": None,
        "notes": "路径细节=去AI味关键。",
    },
    # —— 室内 ——
    {
        "id": "mat-interior-bauhaus",
        "domain": "interior",
        "keyword": "室内美学 包豪斯",
        "title_observed": "结构参照：包豪斯线硬色少",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "开篇诚实「非我家实拍」；点名流派；谈材质/比例/留白；"
            "封面家具与空间关系清晰，忌软装拼贴土味。"
        ),
        "taste_tags": ["honest-framing", "style-named", "provenance-stated", "material-talk"],
        "quality_score": 86,
        "source_url": None,
        "notes": "室内必须防假探店。",
    },
    {
        "id": "mat-interior-eclectic",
        "domain": "interior",
        "keyword": "折衷主义室内",
        "title_observed": "结构参照：折衷主义材质对照",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "用对照句（金属vs织物）代替形容词堆砌；"
            "每张图注明图库/展览来源。"
        ),
        "taste_tags": ["honest-framing", "style-named", "provenance-stated", "contrast"],
        "quality_score": 83,
        "source_url": None,
        "notes": "对照句结构可学。",
    },
    # —— 音乐 ——
    {
        "id": "mat-music-listening-bar",
        "domain": "music",
        "keyword": "小众爵士 listening bar",
        "title_observed": "结构参照：听音空间+小众厂牌",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "点名真实厂牌/制作人/专辑；可连听觉与封面美学；"
            "避免洗脑神曲榜单搬运；不传侵权音频。"
        ),
        "taste_tags": ["named-artist", "niche-label", "listening-space", "curator-voice"],
        "quality_score": 84,
        "source_url": None,
        "notes": "小众可核验艺人是硬门槛。",
    },
    {
        "id": "mat-music-album-cover",
        "domain": "music",
        "keyword": "电子音乐 专辑封面美学",
        "title_observed": "结构参照：专辑封面与听觉联动",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "标题含作品名；正文一句听感+一句视觉；"
            "标签含厂牌/风格而非「热歌推荐」。"
        ),
        "taste_tags": ["named-artist", "cover-aesthetic", "niche-label"],
        "quality_score": 81,
        "source_url": None,
        "notes": "封面美学联动是扩展点。",
    },
    # —— 极地 ——
    {
        "id": "mat-polar-ice-quiet",
        "domain": "polar",
        "keyword": "极地风光",
        "title_observed": "结构参照：冰原静谧少叙事",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "少写故事；诚实图源；禁止伪科考人设；"
            "冷调高纬度画面，忌糖水滤镜。"
        ),
        "taste_tags": ["honest-framing", "provenance-stated", "low-sat", "vast-scale"],
        "quality_score": 85,
        "source_url": None,
        "notes": "极地允许非中国，但必须诚实。",
    },
    {
        "id": "mat-polar-aurora-struct",
        "domain": "polar",
        "keyword": "极光 美学",
        "title_observed": "结构参照：极光气氛板非攻略",
        "author_hint": None,
        "likes_hint": None,
        "structure_notes": (
            "标题不写「攻略」；正文标明非亲历时可当气氛板；"
            "地点或航线可核验时再写具体。"
        ),
        "taste_tags": ["honest-framing", "atmosphere-title", "provenance-stated"],
        "quality_score": 82,
        "source_url": None,
        "notes": "气氛板话术防假经历。",
    },
]


def upsert_materials(db: Session) -> int:
    now = datetime.utcnow()
    for item in MATERIALS:
        row = db.get(ReferenceMaterial, item["id"])
        if row is None:
            row = ReferenceMaterial(id=item["id"])
            db.add(row)
        row.domain = item["domain"]
        row.keyword = item["keyword"]
        row.title_observed = item["title_observed"]
        row.author_hint = item.get("author_hint")
        row.likes_hint = item.get("likes_hint")
        row.structure_notes = item["structure_notes"]
        row.taste_tags_json = json.dumps(item["taste_tags"], ensure_ascii=False)
        row.quality_score = item["quality_score"]
        row.source_url = item.get("source_url")
        row.license_ok = False
        row.notes = item.get("notes")
        row.collected_at = now
    db.commit()
    return len(MATERIALS)
