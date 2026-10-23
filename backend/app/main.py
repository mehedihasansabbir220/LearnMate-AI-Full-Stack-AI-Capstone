import json, os
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()  # must run before .database reads DATABASE_URL

from .database import Base, engine, get_db
from .models import StudySession
from .schemas import GenerateRequest, StudyPack

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="LearnMate AI API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    # FRONTEND_ORIGIN may list several comma-separated origins, e.g. local dev plus the deployed site.
    allow_origins=[o.strip().rstrip("/") for o in os.getenv("FRONTEND_ORIGIN", "http://localhost:3000").split(",") if o.strip()],
    allow_credentials=False, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/")
def root():
    return {"name": "LearnMate AI API", "docs": "/docs", "status": "ok"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/study-packs", response_model=StudyPack)
def create_study_pack(payload: GenerateRequest, db: Session = Depends(get_db)):
    try:
        from .ai_service import AIUnavailableError, generate_study_pack
        result = generate_study_pack(payload.topic.strip(), payload.notes.strip(), payload.level)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except AIUnavailableError as exc:
        print(f"Study pack generation failed after retries: {exc}")
        raise HTTPException(status_code=503, detail="Gemini is busy or rate-limited right now. Please wait a minute and try again.")
    except Exception as exc:
        print(f"Study pack generation failed: {type(exc).__name__}: {exc}")
        raise HTTPException(status_code=502, detail="AI generation failed. Check API key, model access, quota, and backend logs.")
    row = StudySession(topic=payload.topic.strip(), level=payload.level,
        source_text=payload.notes.strip(), result_json=json.dumps(result, ensure_ascii=False))
    db.add(row); db.commit()
    return result

@app.get("/api/sessions")
def list_sessions(db: Session = Depends(get_db)):
    rows = db.query(StudySession).order_by(StudySession.id.desc()).limit(20).all()
    return [{"id": r.id, "topic": r.topic, "level": r.level,
             "created_at": r.created_at.isoformat() if r.created_at else ""} for r in rows]

@app.get("/api/sessions/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    row = db.get(StudySession, session_id)
    if not row:
        raise HTTPException(status_code=404, detail="Study session not found")
    return {"id": row.id, "topic": row.topic, "level": row.level,
            "created_at": row.created_at.isoformat() if row.created_at else "",
            "study_pack": json.loads(row.result_json)}
