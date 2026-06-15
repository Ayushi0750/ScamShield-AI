from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.db import SessionLocal
from app.models.recruiter import Recruiter

from app.services.email_risk_service import (
    email_risk_service
)

router = APIRouter()


class EmailAnalysisRequest(BaseModel):
    email: str
    company: str

#recruiter trust score
@router.get("/recruiter/{recruiter_id}/trust-score")
def get_recruiter_trust_score(recruiter_id: int):

    db = SessionLocal()

    try:

        recruiter = (
            db.query(Recruiter)
            .filter(Recruiter.id == recruiter_id)
            .first()
        )

        if not recruiter:
            raise HTTPException(
                status_code=404,
                detail="Recruiter not found"
            )

        return {
            "id": recruiter.id,
            "name": recruiter.name,
            "company": recruiter.company,
            "email": recruiter.email,
            "trust_score": recruiter.trust_score,
            "risk_label": recruiter.risk_label,
            "verified_status": recruiter.verified_status,
            "updated_at": recruiter.updated_at
        }

    finally:
        db.close()


#email analysis api 
@router.post("/email/analyze")
def analyze_email(
    request: EmailAnalysisRequest
):

    result = (
        email_risk_service
        .analyze_email(
            email=request.email,
            company=request.company
        )
    )

    return result