from app.services.trust_score_service import trust_score_service

recruiter = {
    "company": "Microsoft",
    "domain": "microsoft.com",
    "job_count": 12,
    "scam_flags": 0,
    "verified_status": True
}

print(
    trust_score_service.calculate_score(
        recruiter
    )
)