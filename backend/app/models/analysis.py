from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from datetime import datetime, timezone
from app.database.base import Base



class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    job_text = Column(Text, nullable=False)

    is_scam = Column(Boolean, nullable=False)

    confidence = Column(Integer, nullable=False)  # 0–100 score

    risk_level = Column(String, nullable=False)  # LOW / MEDIUM / HIGH

   
    matched_rules = Column(JSON, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )