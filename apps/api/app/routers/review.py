from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config import get_settings
from app.db import get_db
from app.models import CandidatePost
from app.schemas import ReviewBody, candidate_to_out
from app.seed import list_today_candidates
from app.services.reject_store import hard_delete_candidate
from app.services.candidate_ingest import ingest_candidate_items

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/review", response_class=HTMLResponse)
def review_page(request: Request, db: Session = Depends(get_db)):
    posts = list_today_candidates(db)
    payload = [candidate_to_out(p).model_dump() for p in posts]
    settings = get_settings()
    return templates.TemplateResponse(
        request,
        "review.html",
        {
            "posts_json": payload,
            "account_name": settings.account_name,
            "count": len(payload),
        },
    )


@router.post("/api/review/{post_id}")
def review_action(
    post_id: str,
    body: ReviewBody,
    db: Session = Depends(get_db),
):
    stmt = (
        select(CandidatePost)
        .where(CandidatePost.id == post_id)
        .options(selectinload(CandidatePost.images))
    )
    post = db.scalar(stmt)
    if not post:
        raise HTTPException(status_code=404, detail="not found")

    if body.action == "publish":
        if not post.taste_pass:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"taste_score {post.taste_score} 未达素材品味门槛，"
                    "请改写后再发布"
                ),
            )
        post.status = "published"
        post.reviewed_at = datetime.utcnow()
        db.commit()
        db.refresh(post)
        return candidate_to_out(post)

    if body.action == "draft":
        post.status = "draft"
        post.reviewed_at = datetime.utcnow()
        db.commit()
        db.refresh(post)
        return candidate_to_out(post)

    # reject → 永久删除 + 指纹
    snapshot = candidate_to_out(post)
    hard_delete_candidate(
        db,
        post,
        reason=body.reject_reason or "user_rejected",
    )
    return {
        "deleted": True,
        "id": snapshot.id,
        "theme_key": snapshot.theme_key,
        "title": snapshot.title,
    }


@router.post("/api/jobs/ingest-candidates")
def api_ingest_candidates(body: dict, db: Session = Depends(get_db)):
    """Cursor Agent / 人工提交今日 3 条候选 JSON 落库（不调外部 LLM）。"""
    items = body.get("candidates") if isinstance(body, dict) else None
    if items is None and isinstance(body, list):
        items = body
    if not isinstance(items, list):
        raise HTTPException(status_code=400, detail="body 须含 candidates 数组")
    result = ingest_candidate_items(db, items)
    if not result.ok:
        raise HTTPException(status_code=400, detail=result.message)
    return {
        "ok": True,
        "message": result.message,
        "post_ids": result.post_ids,
    }
