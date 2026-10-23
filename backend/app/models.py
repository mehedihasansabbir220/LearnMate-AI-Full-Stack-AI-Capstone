from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class StudySession(Base):
    __tablename__ = "study_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    topic: Mapped[str] = mapped_column(String(250), nullable=False)
    level: Mapped[str] = mapped_column(String(40), nullable=False)
    source_text: Mapped[str] = mapped_column(Text, default="")
    result_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
