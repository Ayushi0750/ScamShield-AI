from typing import Dict

from app.services.trust_score_service import (
    trust_score_service
)

from app.services.domain_reputation_service import (
    domain_reputation_service
)


class EmailRiskService:
    """
    Email Risk Analysis Engine

    Responsibilities:
    - Extract domain
    - Check domain reputation
    - Detect disposable emails
    - Detect company/domain mismatch
    - Generate email risk score
    - Generate risk label
    """

    def is_company_domain_match(
        self,
        company: str,
        domain: str
    ) -> bool:

        if not company:
            return False

        company = company.lower().strip()
        domain = domain.lower().strip()

        return company in domain

    def analyze_email(
        self,
        email: str,
        company: str = ""
    ) -> Dict:

        # domain extraction
        domain = (
            trust_score_service
            .extract_domain(email)
        )

        # invalid email
        if not domain:

            return {
                "email": email,
                "domain": "",
                "reputation": "INVALID",
                "risk_score": 100,
                "risk_label": "HIGH_RISK",
                "company_match": False
            }

        
        reputation_data = (
            domain_reputation_service
            .get_reputation(domain)
        )

        reputation = reputation_data["reputation"]
        risk_score = reputation_data["risk_score"]

        
        company_match = (
            self.is_company_domain_match(
                company,
                domain
            )
        )

        if company and not company_match:
            risk_score += 20

        
        risk_score = min(
            risk_score,
            100
        )

        
        if risk_score <= 25:
            risk_label = "SAFE"

        elif risk_score <= 60:
            risk_label = "SUSPICIOUS"

        else:
            risk_label = "HIGH_RISK"

        return {
            "email": email,
            "company": company,
            "domain": domain,
            "reputation": reputation,
            "company_match": company_match,
            "risk_score": risk_score,
            "risk_label": risk_label
        }


email_risk_service = EmailRiskService()