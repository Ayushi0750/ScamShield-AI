from fastapi import APIRouter, HTTPException
from app.database.db import SessionLocal
from app.models.recruiter import Recruiter

from app.services.trust_score_service import trust_score_service
from app.services.email_risk_service import email_risk_service
from app.services.domain_reputation_service import domain_reputation_service
from app.core.singletons import fraud_graph_service
from app.services.fraud_ring_service import fraud_ring_service

router = APIRouter()


@router.get("/recruiter/{recruiter_id}/analyze")
def analyze_recruiter(recruiter_id: int):

    db = SessionLocal()

    try:
        recruiter = db.query(Recruiter).filter(
            Recruiter.id == recruiter_id
        ).first()

        if not recruiter:
            raise HTTPException(
                status_code=404,
                detail="Recruiter not found"
            )

        # trust score
        trust_result = trust_score_service.calculate_score({
            "name": recruiter.name,
            "company": recruiter.company,
            "email": recruiter.email,
            "domain": recruiter.domain,
            "job_count": recruiter.job_count,
            "scam_flags": recruiter.scam_flags,
            "verified_status": recruiter.verified_status
        })

        
        email_result = email_risk_service.analyze_email(
            recruiter.email
        )

        
        clusters = fraud_graph_service.detect_clusters()

        related_cluster = None
        for c in clusters:
            if recruiter.email in str(c.get("emails", [])):
                related_cluster = c
                break

        fraud_ring_result = None
        if related_cluster:
            fraud_ring_result = fraud_ring_service.analyze_cluster(
                related_cluster
            )

        
        trust_score = trust_result["trust_score"]
        email_risk = email_result["risk_score"]

        graph_risk = (
            fraud_ring_result["risk_score"]
            if fraud_ring_result else 0
        )

        final_score = (
            trust_score * 0.5
            + (100 - email_risk) * 0.2
            + (100 - graph_risk) * 0.3
        )

        
        if final_score >= 75:
            label = "SAFE"
        elif final_score >= 45:
            label = "SUSPICIOUS"
        else:
            label = "HIGH_RISK"

        
        return {
            "recruiter_id": recruiter.id,
            "name": recruiter.name,
            "company": recruiter.company,
            "email": recruiter.email,

            "trust_score": trust_score,
            "email_risk": email_result,
            "fraud_cluster": related_cluster,
            "fraud_ring": fraud_ring_result,

            "final_score": final_score,
            "final_label": label
        }

    finally:
        db.close()