from typing import Dict, Any

from app.services.domain_reputation_service import (
    domain_reputation_service
)


class TrustScoreService:
    """
    Recruiter Trust Score Engine

    Input:
        recruiter profile

    Output:
        trust score (0-100)
        risk label
        scoring breakdown
    """

    # email domain extraction
    def extract_domain(
        self,
        email: str
    ) -> str:

        if not email:
            return ""

        email = email.strip().lower()

        if "@" not in email:
            return ""

        return email.split("@")[-1]

    def calculate_score(
        self,
        recruiter: Dict[str, Any]
    ) -> Dict[str, Any]:

        score = 50

        breakdown = {}

        
        verification_score = (
            25 if recruiter.get("verified_status")
            else 0
        )

        score += verification_score

        breakdown["verification_score"] = verification_score

        
        domain = recruiter.get(
            "domain",
            ""
        ).lower()

        domain_score = 0

        reputation = (
            domain_reputation_service
            .get_reputation(domain)
        )

        if reputation["reputation"] == "TRUSTED":
            domain_score = 10

        elif reputation["reputation"] == "SUSPICIOUS":
            domain_score = -20

        elif reputation["reputation"] == "DISPOSABLE":
            domain_score = -30

        score += domain_score

        breakdown["domain_score"] = domain_score

        
        company = recruiter.get(
            "company",
            ""
        ).lower()

        company_match_score = 0

        if company and company in domain:
            company_match_score = 15

        score += company_match_score

        breakdown["company_match_score"] = company_match_score

        
        job_count = recruiter.get(
            "job_count",
            0
        )

        history_score = 0

        if job_count >= 10:
            history_score = 10

        elif job_count >= 5:
            history_score = 5

        score += history_score

        breakdown["history_score"] = history_score

        
        scam_flags = recruiter.get(
            "scam_flags",
            0
        )

        penalty = min(
            scam_flags * 10,
            40
        )

        score -= penalty

        breakdown["scam_penalty"] = penalty

        
        score = max(
            0,
            min(100, score)
        )

        
        if score >= 80:
            label = "SAFE"

        elif score >= 50:
            label = "SUSPICIOUS"

        else:
            label = "HIGH_RISK"

        return {
            "trust_score": score,
            "risk_label": label,
            "breakdown": breakdown
        }


trust_score_service = TrustScoreService()