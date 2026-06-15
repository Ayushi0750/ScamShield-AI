from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from datetime import datetime, timezone

from app.database.base import Base


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    company = Column(String, nullable=False)

    email = Column(String, nullable=False, unique=True)

    domain = Column(String, nullable=False)

    job_count = Column(Integer, default=0)

    scam_flags = Column(Integer, default=0)

    verified_status = Column(Boolean, default=False)

  
    trust_score = Column(Integer, default=50)

    risk_label = Column(
        String,
        default="SUSPICIOUS"
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )