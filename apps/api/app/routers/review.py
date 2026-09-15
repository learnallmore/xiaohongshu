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
        post.status = "published"
    elif body.action == "draft":
        post.status = "draft"
    else:
        post.status = "rejected"
        post.reject_reason = body.reject_reason or "rejected"

    post.reviewed_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return candidate_to_out(post)
