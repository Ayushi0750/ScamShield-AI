
from typing import Dict, Any

from app.services.rule_engine import analyze_job_text
from app.services.email_risk_service import email_risk_service
from app.services.domain_reputation_service import domain_reputation_service
from app.services.trust_score_service import trust_score_service

from app.core.singletons import fraud_graph_service
from app.services.fraud_ring_service import FraudRingService


class MasterRiskEngine:

    def __init__(self):
        self.fraud_ring_service = FraudRingService()

    def analyze(self, recruiter: Dict[str, Any], ml_score: float = None) -> Dict[str, Any]:

        email = recruiter.get("email")
        domain = recruiter.get("domain")
        job_id = recruiter.get("job_id", "unknown")

        # email risk 
        email_result = email_risk_service.analyze_email(
            email,
            company=recruiter.get("company", "")
        )
        email_score = email_result["risk_score"]

        # domain risk
        domain_result = domain_reputation_service.get_reputation(domain)
        domain_score = domain_result["risk_score"]

        #trust score
        trust_result = trust_score_service.calculate_score(recruiter)
        raw_trust_score = trust_result["trust_score"]
        trust_risk_score = 100 - raw_trust_score

        # graph risk
        clusters = []
        ring_scores = []
        max_ring_score = 0

        try:
            fraud_graph_service.build_relationship(
                recruiter_id=str(recruiter.get("id")),
                email=email,
                domain=domain,
                job_id=job_id
            )

            clusters = fraud_graph_service.get_cluster_summary().get("clusters", [])

            ring_scores = [
                self.fraud_ring_service.analyze_cluster(c)
                for c in clusters
            ]

            max_ring_score = max(
                [r["risk_score"] for r in ring_scores],
                default=0
            )

        except Exception:
            clusters = []
            ring_scores = []
            max_ring_score = 0

        # rule engine
        rule_result = analyze_job_text(recruiter.get("job_text", ""))
        rule_score = rule_result["confidence"] * 100
        rule_matched_indicators = rule_result.get("matched_rules", [])

        # rule override 
        rule_override_applied = False
        if rule_score >= 75 and len(rule_matched_indicators) >= 2:
            rule_override_applied = True
            email_score = max(email_score, 60)
            domain_score = max(domain_score, 60)
            trust_risk_score = max(trust_risk_score, 55)

        # final score
        if rule_override_applied:
            final_score = (
                rule_score * 0.60 +
                email_score * 0.15 +
                domain_score * 0.15 +
                trust_risk_score * 0.05 +
                max_ring_score * 0.05
            )
        else:
            final_score = (
                rule_score * 0.40 +
                email_score * 0.20 +
                domain_score * 0.15 +
                trust_risk_score * 0.15 +
                max_ring_score * 0.10
            )

        # label 
        if rule_override_applied and rule_score >= 75:
            label = "HIGH_RISK"
        elif final_score >= 60:
            label = "HIGH_RISK"
        elif final_score >= 30:
            label = "SUSPICIOUS"
        else:
            label = "SAFE"

        if rule_score >= 60 and label == "SAFE":
            label = "SUSPICIOUS"

        if rule_score >= 80 and label in ("SAFE", "SUSPICIOUS"):
            label = "HIGH_RISK"

        
        if ml_score is not None:
            final_score = round(final_score * 0.65 + ml_score * 0.35, 2)

            if ml_score >= 85:
                label = "HIGH_RISK"
            elif ml_score >= 70 and label == "SAFE":
                label = "SUSPICIOUS"

        

        def normalize(l):
            return "SCAM" if l in ("HIGH_RISK", "SUSPICIOUS") else "GENUINE"

        # FIX: use pure rule engine signal (not blended label)
        rule_label = "SCAM" if rule_score >= 60 else "GENUINE"

        ml_label = (
            "SCAM"
            if (ml_score is not None and ml_score >= 70)
            else "GENUINE"
        )

        agreement_status = (
            "AGREE"
            if normalize(rule_label) == normalize(ml_label)
            else "CONFLICT"
        )

        return {
            "final_score": round(final_score, 2),
            "final_label": label,
            "agreement_status": agreement_status,
            "breakdown": {
                "rule_score": rule_score,
                "email_score": email_score,
                "domain_score": domain_score,
                "trust_score": raw_trust_score,
                "trust_risk_score": trust_risk_score,
                "fraud_ring_score": max_ring_score,
                "rule_override_applied": rule_override_applied
            },
            "details": {
                "email": email_result,
                "domain": domain_result,
                "rings": ring_scores
            }
        }


master_risk_engine = MasterRiskEngine()