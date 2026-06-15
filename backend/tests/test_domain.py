from app.services.trust_score_service import trust_score_service

print(
    trust_score_service.extract_domain(
        "recruiter@microsoft.com"
    )
)

print(
    trust_score_service.extract_domain(
        "hr@google.com"
    )
)

print(
    trust_score_service.extract_domain(
        "jobs@amazon.com"
    )
)