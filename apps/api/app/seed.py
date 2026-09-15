from __future__ import annotations

import json
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import CandidatePost, PostImage

# 文案与图源须符合 .cursor/skills/authentic-xhs-voice/SKILL.md
SEED: list[dict] = [
    {
        "id": "cand-city-01",
        "domain": "cityscape",
        "domain_label": "顶级城市景观 · 中国",
        "title": "陆家嘴江岸，雨停之后",
        "body": (
            "昨天傍晚雨停，从东昌路地铁站走到滨江。\n"
            "不是去打卡那块「最经典机位」石板，就顺着栏杆往北走了一点，"
            "对面楼玻璃还在滴水，倒影比晴天乱，反而好看。\n\n"
            "图都是上海浦东陆家嘴滨江一带。\n"
            "图1–3来源：Unsplash（摄影师见各图文件页），授权按 Unsplash License。"
            "我没用别人小红书原图。\n\n"
            "如果你也去，记得看开盘时间；江风大，手机别只顾怼天际线。"
        ),
        "tags": ["上海", "陆家嘴", "滨江", "城市天际线"],
        "rationale": "中国可指认地点+正文写明图源；克制升华腔。",
        "niche_score": 76,
        "images": [
            {
                "id": "img-c1-1",
                "sort_order": 0,
                "url": "https://images.unsplash.com/photo-1538426455732-8efd34c9b5c3?w=1200&q=80",
                "width": 1200,
                "height": 1600,
                "source": "Unsplash/Shanghai skyline photo-1538426455732-8efd34c9b5c3",
                "license": "Unsplash License",
            },
            {
                "id": "img-c1-2",
                "sort_order": 1,
                "url": "https://images.unsplash.com/photo-1548919973-5cef591cdbc9?w=1200&q=80",
                "width": 1200,
                "height": 1600,
                "source": "Unsplash/Shanghai photo-1548919973-5cef591cdbc9",
                "license": "Unsplash License",
            },
            {
                "id": "img-c1-3",
                "sort_order": 2,
                "url": "https://images.unsplash.com/photo-1474181487882-5abf3f12bbf8?w=1200&q=80",
                "width": 1200,
                "height": 1500,
                "source": "Unsplash/Shanghai photo-1474181487882-5abf3f12bbf8",
                "license": "Unsplash License",
            },
        ],
    },
    {
        "id": "cand-interior-01",
        "domain": "interior",
        "domain_label": "室内设计 · 包豪斯参考",
        "title": "先说清楚：这不是我家实拍",
        "body": (
            "想聊包豪斯，别上来就「材质在呼吸」。\n"
            "我最近在翻的是管状金属椅 + 直角柜体那一套：线很硬，颜色少，空地留得多。\n\n"
            "下面三张图来自 Unsplash，风格接近包豪斯/现代主义室内，"
            "不是国内某小区改造案例，也不是我住的地方——避免误会成探店。\n"
            "图源与授权：Unsplash License，具体摄影师见原页。\n\n"
            "真要在国内找可参观样本，还得另查展览或开放日；这组只当造型参考。"
        ),
        "tags": ["包豪斯", "室内设计", "图源说明", "现代主义"],
        "rationale": "诚实标注非实拍；风格可追溯，禁止假装探店。",
        "niche_score": 80,
        "images": [
            {
                "id": "img-i1-1",
                "sort_order": 0,
                "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=1200&q=80",
                "width": 1200,
                "height": 1500,
                "source": "Unsplash/interior photo-1586023492125-27b2c045efd7",
                "license": "Unsplash License",
            },
            {
                "id": "img-i1-2",
                "sort_order": 1,
                "url": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1200&q=80",
                "width": 1200,
                "height": 1500,
                "source": "Unsplash/interior photo-1618221195710-dd6b41faaea6",
                "license": "Unsplash License",
            },
            {
                "id": "img-i1-3",
                "sort_order": 2,
                "url": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=1200&q=80",
                "width": 1200,
                "height": 1500,
                "source": "Unsplash/interior photo-1616486338812-3dadae4b4ace",
                "license": "Unsplash License",
            },
        ],
    },
    {
        "id": "cand-polar-01",
        "domain": "polar",
        "domain_label": "极地风景",
        "title": "冰原照片，别当成我去过南极",
        "body": (
            "极地这组我用来练「少写故事」。\n"
            "雪面高光很容易拍成糖水，所以选了偏冷、几乎没人的画面。\n\n"
            "图1–3：Unsplash 极地/高山冰雪题材，授权 Unsplash License；"
            "不是我的航拍，也不是某次科考随行记录。\n"
            "正文不写假路线、假日期。你要是收藏，当气氛板就行，别当攻略。"
        ),
        "tags": ["极地", "冰原", "图源说明", "风景"],
        "rationale": "极地允许非中国；必须诚实图源，禁止伪科考人设。",
        "niche_score": 83,
        "images": [
            {
                "id": "img-p1-1",
                "sort_order": 0,
                "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
                "width": 1200,
                "height": 1600,
                "source": "Unsplash/mountain-ice photo-1464822759023-fed622ff2c3b",
                "license": "Unsplash License",
            },
            {
                "id": "img-p1-2",
                "sort_order": 1,
                "url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1200&q=80",
                "width": 1200,
                "height": 1600,
                "source": "Unsplash/snow peak photo-1519681393784-d120267933ba",
                "license": "Unsplash License",
            },
            {
                "id": "img-p1-3",
                "sort_order": 2,
                "url": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=1200&q=80",
                "width": 1200,
                "height": 1500,
                "source": "Unsplash/alpine photo-1483728642387-6c3bdd6c93e5",
                "license": "Unsplash License",
            },
        ],
    },
]


def _upsert_seed(db: Session) -> None:
    today = date.today()
    for item in SEED:
        post = db.get(CandidatePost, item["id"])
        if post is None:
            post = CandidatePost(id=item["id"])
            db.add(post)
            for img in item["images"]:
                post.images.append(
                    PostImage(
                        id=img["id"],
                        post_id=item["id"],
                        sort_order=img["sort_order"],
                        url=img["url"],
                        width=img["width"],
                        height=img["height"],
                        source=img["source"],
                        license=img["license"],
                    )
                )
        else:
            # refresh text/images on existing seed rows
            post.images.clear()
            for img in item["images"]:
                post.images.append(
                    PostImage(
                        id=img["id"],
                        post_id=item["id"],
                        sort_order=img["sort_order"],
                        url=img["url"],
                        width=img["width"],
                        height=img["height"],
                        source=img["source"],
                        license=img["license"],
                    )
                )

        post.date_batch = today
        post.domain = item["domain"]
        post.domain_label = item["domain_label"]
        post.status = "pending"
        post.title = item["title"]
        post.body = item["body"]
        post.tags_json = json.dumps(item["tags"], ensure_ascii=False)
        post.cover_index = 0
        post.rationale = item["rationale"]
        post.niche_score = item["niche_score"]
        post.reject_reason = None

    db.commit()


def seed_if_empty(db: Session) -> None:
    """启动时同步种子内容（可覆盖同 id），保证文案规范迭代能进库。"""
    _upsert_seed(db)


def list_today_candidates(db: Session) -> list[CandidatePost]:
    today = date.today()
    stmt = (
        select(CandidatePost)
        .where(CandidatePost.date_batch == today)
        .options(selectinload(CandidatePost.images))
        .order_by(CandidatePost.created_at.asc())
        .limit(3)
    )
    posts = list(db.scalars(stmt).all())
    if len(posts) < 3:
        stmt = (
            select(CandidatePost)
            .options(selectinload(CandidatePost.images))
            .order_by(CandidatePost.created_at.asc())
            .limit(3)
        )
        posts = list(db.scalars(stmt).all())
    return posts
