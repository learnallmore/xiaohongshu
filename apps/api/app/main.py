from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.db import Base, SessionLocal, engine
from app.routers import materials, review
from app.schema_migrate import ensure_schema
from app.seed import seed_if_empty

# ensure models registered
import app.models  # noqa: F401

app = FastAPI(title="棱镜", version="0.1.0")

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.include_router(review.router)
app.include_router(materials.router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_schema(engine)
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        seed_if_empty(db)
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "ok": True,
        "review": "/review",
        "materials": "/api/materials",
        "taste_rescore": "/api/taste/rescore",
    }
