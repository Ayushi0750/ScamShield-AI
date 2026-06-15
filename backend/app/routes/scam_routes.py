


from fastapi import APIRouter
from app.models.request_models import JobAnalysisRequest
from app.services.rule_engine import analyze_job_text
from app.ml.classifier import predict_probability

from app.database.db import SessionLocal
from app.models.analysis import Analysis

from app.rag.retriever import retriever
from app.utils.evaluation_logger import log_evaluation

from app.services.master_risk_engine import master_risk_engine

import re

router = APIRouter()



def extract_email_from_text(text: str) -> str:
    match = re.search(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        text
    )
    if match:
        return match.group(0)

    mention = re.search(
        r"@([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})",
        text
    )
    if mention:
        return "careers@" + mention.group(1)

    return "unknown@unverified.com"


def extract_domain_from_email(email: str) -> str:
    return email.split("@")[-1].lower() if "@" in email else "unverified.com"


def extract_company_from_text(text: str) -> str:
    first_line = text.strip().split("\n")[0]
    if "—" in first_line:
        return first_line.split("—")[0].strip().lower()
    if "-" in first_line:
        return first_line.split("-")[0].strip().lower()
    return ""



@router.post("/analyze")
def analyze(request: JobAnalysisRequest):

    db = SessionLocal()

    try:
        job_text = request.job_text
        actual_label = request.actual_label

        #rule engine
        rule_result = analyze_job_text(job_text)
        rule_score = rule_result["confidence"]

        # ml model
        ml_result = predict_probability(job_text)
        ml_score = min(max(ml_result["scam_probability"], 0.05), 0.95)

        # rag
        retrieved_cases = retriever.search_similar_cases(
            job_text,
            top_k=3
        )

        rag_score = 0.0
        rag_top_matches = []
        rag_explanations = []

        if retrieved_cases:

            rag_score = sum(
                r["similarity"] for r in retrieved_cases
            ) / len(retrieved_cases)

            for r in retrieved_cases:
                rag_top_matches.append({
                    "text": r.get("text", ""),
                    "label": r.get("label", ""),
                    "similarity": float(r.get("similarity", 0))
                })

                rag_explanations.append(
                    f"Matched case ({r.get('label')}): "
                    f"{r.get('text', '')[:120]}..."
                )

        #master risk 
        extracted_email = extract_email_from_text(job_text)
        extracted_domain = extract_domain_from_email(extracted_email)
        extracted_company = extract_company_from_text(job_text)

        ml_score_scaled = ml_score * 100

        master_result = master_risk_engine.analyze({
            "id": actual_label or 0,
            "email": extracted_email,
            "domain": extracted_domain,
            "company": extracted_company,
            "job_text": job_text,
            "verified_status": False,
            "job_count": 0,
            "scam_flags": 0
        }, ml_score=ml_score_scaled)

        # hybrid score
        hybrid_score = (
            rule_score * 0.30 +
            ml_score * 0.55 +
            rag_score * 0.15
        )

        # risk level
        risk_level = (
            "HIGH" if hybrid_score >= 0.80
            else "MEDIUM" if hybrid_score >= 0.50
            else "LOW"
        )

        # db 
        analysis_record = Analysis(
            job_text=job_text,
            is_scam=hybrid_score >= 0.5,
            confidence=int(hybrid_score * 100),
            risk_level=risk_level,
            matched_rules=rule_result["matched_rules"]
        )

        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)

        log_evaluation({
            "rule_score": rule_score,
            "ml_score": ml_score,
            "rag_score": rag_score,
            "final_score": hybrid_score,
            "master_score": master_result["final_score"],
        })

        # response
        return {
            "id": analysis_record.id,
            "is_scam": analysis_record.is_scam,
            "confidence": hybrid_score,
            "risk_level": risk_level,

            "rule_prediction": "SCAM" if rule_result["is_scam"] else "GENUINE",
            "ml_prediction": ml_result["label"],
            "ml_score": ml_score,

            
            "agreement_status": master_result.get("agreement_status", "CONFLICT"),

            "matched_rules": rule_result["matched_rules"],

            "rag": {
                "score": rag_score,
                "top_matches": rag_top_matches,
                "explanations": rag_explanations
            },

            "master_risk": master_result
        }

    finally:
        db.close()