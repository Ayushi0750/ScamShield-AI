from fastapi import APIRouter, HTTPException
from app.database.db import SessionLocal
from app.models.analysis import Analysis

router = APIRouter()



@router.get("/analysis")
def get_all_analysis():

    db = SessionLocal()

    try:
        records = db.query(Analysis).order_by(Analysis.id.desc()).all()

        return [
            {
                "id": r.id,
                "job_text": r.job_text,
                "is_scam": r.is_scam,
                "confidence": r.confidence,
                "risk_level": r.risk_level,
                "matched_rules": r.matched_rules,
                "created_at": r.created_at
            }
            for r in records
        ]

    finally:
        db.close()



@router.get("/analysis/{analysis_id}")
def get_analysis_by_id(analysis_id: int):

    db = SessionLocal()

    try:
        record = db.query(Analysis).filter(Analysis.id == analysis_id).first()

        if not record:
            raise HTTPException(status_code=404, detail="Analysis not found")

        return {
            "id": record.id,
            "job_text": record.job_text,
            "is_scam": record.is_scam,
            "confidence": record.confidence,
            "risk_level": record.risk_level,
            "matched_rules": record.matched_rules,
            "created_at": record.created_at
        }

    finally:
        db.close()