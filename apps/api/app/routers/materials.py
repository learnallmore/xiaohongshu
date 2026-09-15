from __future__ import annotations

import json
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models import CandidatePost, ReferenceMaterial
from app.schemas import MaterialIn, MaterialOut, candidate_to_out, material_to_out
from app.services.material_gates import material_reject_reason
from app.services.taste_scorer import apply_taste_to_post, domain_benchmark, rescore_all_candidates

router = APIRouter(prefix="/api", tags=["materials-taste"])


@router.get("/materials", response_model=list[MaterialOut])
def list_materials(
    domain: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(ReferenceMaterial).order_by(
        ReferenceMaterial.quality_score.desc(),
        ReferenceMaterial.collected_at.desc(),
    )
    if domain:
        stmt = stmt.where(ReferenceMaterial.domain == domain)
    rows = list(db.scalars(stmt).all())
    return [material_to_out(r) for r in rows]


@router.post("/materials", response_model=MaterialOut)
def create_material(body: MaterialIn, db: Session = Depends(get_db)):
    """入库真实笔记公开元数据；license_ok 强制 false。"""
    reject = material_reject_reason(
        domain=body.domain,
        title=body.title_observed,
        body_excerpt=body.body_excerpt,
        keyword=body.keyword,
        notes=body.notes,
    )
    if reject:
        raise HTTPException(status_code=400, detail=reject)
    mid = body.id or (
        f"xhs-{body.note_id}" if body.note_id else f"mat-{uuid.uuid4().hex[:12]}"
    )
    row = db.get(ReferenceMaterial, mid)
    if row is None:
        row = ReferenceMaterial(id=mid)
        db.add(row)
    row.domain = body.domain
    row.keyword = body.keyword
    row.note_id = body.note_id
    row.title_observed = body.title_observed
    row.author_hint = body.author_hint
    row.likes_hint = body.likes_hint
    row.collects_hint = body.collects_hint
    row.comments_hint = body.comments_hint
    row.cover_url = body.cover_url
    images = list(body.images or [])
    if body.cover_url and body.cover_url not in images:
        images = [body.cover_url] + images
    row.images_json = json.dumps(images, ensure_ascii=False) if images else None
    row.body_excerpt = body.body_excerpt
    row.structure_notes = body.structure_notes or body.notes or (
        f"真实笔记 {body.note_id or mid}"
    )
    row.taste_tags_json = json.dumps(body.taste_tags, ensure_ascii=False)
    row.quality_score = body.quality_score
    row.source_url = body.source_url
    row.source_site = body.source_site or "xhs"
    row.theme_key = body.theme_key
    row.license_ok = False
    row.notes = body.notes
    row.collected_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return material_to_out(row)


@router.post("/taste/rescore")
def taste_rescore(db: Session = Depends(get_db)):
    results = rescore_all_candidates(db)
    return {"ok": True, "count": len(results), "results": results}


@router.post("/taste/score/{post_id}")
def taste_score_one(post_id: str, db: Session = Depends(get_db)):
    stmt = (
        select(CandidatePost)
        .where(CandidatePost.id == post_id)
        .options(selectinload(CandidatePost.images))
    )
    post = db.scalar(stmt)
    if not post:
        raise HTTPException(status_code=404, detail="not found")
    result = apply_taste_to_post(db, post)
    db.commit()
    db.refresh(post)
    out = candidate_to_out(post)
    return {
        "candidate": out,
        "benchmark": result.benchmark,
        "taste_score": result.score,
        "taste_pass": result.passed,
    }


@router.get("/taste/benchmark/{domain}")
def taste_benchmark(domain: str, db: Session = Depends(get_db)):
    return {"domain": domain, "benchmark": domain_benchmark(db, domain)}
