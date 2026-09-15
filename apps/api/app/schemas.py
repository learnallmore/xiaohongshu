from __future__ import annotations

import json
from datetime import date

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
    images: list[ImageOut]


class ReviewBody(BaseModel):
    action: str = Field(pattern="^(publish|draft|reject)$")
    reject_reason: str | None = None


def tags_from_json(raw: str) -> list[str]:
    try:
        data = json.loads(raw)
        return [str(x) for x in data] if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


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


TODAY = date.today
