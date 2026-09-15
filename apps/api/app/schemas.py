from __future__ import annotations

import json
from datetime import date, datetime

from pydantic import BaseModel, Field


class ImageOut(BaseModel):
    id: str
    sort_order: int
    url: str
    width: int
    height: int
    source: str
    license: str


class CandidateOut(BaseModel):
    id: str
    domain: str
    domain_label: str | None
    status: str
    title: str
    body: str
    tags: list[str]
    cover_index: int
    rationale: str | None
    niche_score: int
    taste_score: int
    taste_pass: bool
    taste_features: dict | None = None
    theme_key: str | None = None
    images: list[ImageOut]


class ReviewBody(BaseModel):
    action: str = Field(pattern="^(publish|draft|reject)$")
    reject_reason: str | None = None


class MaterialIn(BaseModel):
    id: str | None = None
    domain: str
    keyword: str
    note_id: str | None = None
    title_observed: str
    author_hint: str | None = None
    likes_hint: int | None = None
    collects_hint: int | None = None
    comments_hint: int | None = None
    cover_url: str | None = None
    images: list[str] = Field(default_factory=list)
    body_excerpt: str | None = None
    structure_notes: str | None = None  # 策展备注，可选
    taste_tags: list[str] = Field(default_factory=list)
    quality_score: int = Field(ge=0, le=100, default=75)
    source_url: str | None = None
    source_site: str | None = "xhs"
    theme_key: str | None = None
    notes: str | None = None


class MaterialOut(BaseModel):
    id: str
    domain: str
    keyword: str
    note_id: str | None = None
    title_observed: str
    author_hint: str | None
    likes_hint: int | None
    collects_hint: int | None = None
    comments_hint: int | None = None
    cover_url: str | None = None
    images: list[str] = Field(default_factory=list)
    body_excerpt: str | None = None
    structure_notes: str
    taste_tags: list[str]
    quality_score: int
    source_url: str | None
    source_site: str | None = None
    theme_key: str | None = None
    license_ok: bool
    notes: str | None
    collected_at: datetime | None = None


def tags_from_json(raw: str) -> list[str]:
    try:
        data = json.loads(raw)
        return [str(x) for x in data] if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def features_from_json(raw: str | None) -> dict | None:
    if not raw:
        return None
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        return None


def candidate_to_out(post) -> CandidateOut:
    return CandidateOut(
        id=post.id,
        domain=post.domain,
        domain_label=post.domain_label,
        status=post.status,
        title=post.title,
        body=post.body,
        tags=tags_from_json(post.tags_json),
        cover_index=post.cover_index,
        rationale=post.rationale,
        niche_score=post.niche_score,
        taste_score=getattr(post, "taste_score", 0) or 0,
        taste_pass=bool(getattr(post, "taste_pass", False)),
        taste_features=features_from_json(
            getattr(post, "taste_features_json", None)
        ),
        theme_key=getattr(post, "theme_key", None),
        images=[
            ImageOut(
                id=img.id,
                sort_order=img.sort_order,
                url=img.url,
                width=img.width,
                height=img.height,
                source=img.source,
                license=img.license,
            )
            for img in sorted(post.images, key=lambda i: i.sort_order)
        ],
    )


def material_to_out(row) -> MaterialOut:
    images: list[str] = []
    raw_imgs = getattr(row, "images_json", None)
    if raw_imgs:
        try:
            data = json.loads(raw_imgs)
            if isinstance(data, list):
                images = [str(x) for x in data]
        except json.JSONDecodeError:
            images = []
    cover = getattr(row, "cover_url", None)
    if cover and cover not in images:
        images = [cover] + images
    return MaterialOut(
        id=row.id,
        domain=row.domain,
        keyword=row.keyword,
        note_id=getattr(row, "note_id", None),
        title_observed=row.title_observed,
        author_hint=row.author_hint,
        likes_hint=row.likes_hint,
        collects_hint=getattr(row, "collects_hint", None),
        comments_hint=getattr(row, "comments_hint", None),
        cover_url=cover,
        images=images,
        body_excerpt=getattr(row, "body_excerpt", None),
        structure_notes=row.structure_notes or "",
        taste_tags=tags_from_json(row.taste_tags_json),
        quality_score=row.quality_score,
        source_url=row.source_url,
        source_site=getattr(row, "source_site", None),
        theme_key=getattr(row, "theme_key", None),
        license_ok=row.license_ok,
        notes=row.notes,
        collected_at=row.collected_at,
    )


TODAY = date.today
