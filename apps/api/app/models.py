from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class CandidatePost(Base):
    __tablename__ = "candidate_posts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    date_batch: Mapped[date] = mapped_column(Date, index=True)
    domain: Mapped[str] = mapped_column(String(32))
    domain_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text)
    tags_json: Mapped[str] = mapped_column(Text)  # JSON array as text
    cover_index: Mapped[int] = mapped_column(Integer, default=0)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    niche_score: Mapped[int] = mapped_column(Integer, default=0)
    taste_score: Mapped[int] = mapped_column(Integer, default=0)
    taste_pass: Mapped[bool] = mapped_column(Boolean, default=False)
    taste_features_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    reject_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    images: Mapped[list[PostImage]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="PostImage.sort_order",
    )


class PostImage(Base):
    __tablename__ = "post_images"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    post_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("candidate_posts.id", ondelete="CASCADE"), index=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    url: Mapped[str] = mapped_column(String(1024))
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    mime_type: Mapped[str] = mapped_column(String(64), default="image/jpeg")
    source: Mapped[str] = mapped_column(String(255))
    license: Mapped[str] = mapped_column(String(128))

    post: Mapped[CandidatePost] = relationship(back_populates="images")


class ReferenceMaterial(Base):
    """调研参照素材：只存结构/审美特征，禁止未授权原文原图。"""

    __tablename__ = "reference_materials"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    domain: Mapped[str] = mapped_column(String(32), index=True)
    keyword: Mapped[str] = mapped_column(String(128))
    title_observed: Mapped[str] = mapped_column(String(300))
    author_hint: Mapped[str | None] = mapped_column(String(128), nullable=True)
    likes_hint: Mapped[int | None] = mapped_column(Integer, nullable=True)
    structure_notes: Mapped[str] = mapped_column(Text)
    taste_tags_json: Mapped[str] = mapped_column(Text)  # JSON array
    quality_score: Mapped[int] = mapped_column(Integer, default=70)
    source_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    license_ok: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    collected_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
