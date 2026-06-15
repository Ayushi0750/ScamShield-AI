from typing import Dict


class DomainReputationService:
    """
    Domain Reputation Engine

    Responsible for:
    - Trusted domain detection
    - Suspicious domain detection
    - Disposable email detection
    """

    def __init__(self):

        self.trusted_domains = {
            "google.com",
            "microsoft.com",
            "amazon.com",
            "infosys.com",
            "tcs.com",
            "wipro.com",
            "accenture.com",
            "ibm.com",
            "oracle.com",
            "deloitte.com"
        }

        self.suspicious_domains = {
            "quickhire-now.com",
            "joboffer-fast.com",
            "instantjob-online.com",
            "easymoney-careers.com",
            "guaranteedjob.net"
        }

        self.disposable_domains = {
            "mailinator.com",
            "10minutemail.com",
            "tempmail.com",
            "guerrillamail.com",
            "yopmail.com"
        }

    # -------------------------
    # DOMAIN CHECKS
    # -------------------------
    def is_trusted(
        self,
        domain: str
    ) -> bool:

        return domain.lower() in self.trusted_domains

    def is_suspicious(
        self,
        domain: str
    ) -> bool:

        return domain.lower() in self.suspicious_domains

    def is_disposable(
        self,
        domain: str
    ) -> bool:

        return domain.lower() in self.disposable_domains

    # domain reputation
    def get_reputation(
        self,
        domain: str
    ) -> Dict:

        domain = domain.lower()

        if self.is_disposable(domain):
            return {
                "reputation": "DISPOSABLE",
                "risk_score": 90
            }

        if self.is_suspicious(domain):
            return {
                "reputation": "SUSPICIOUS",
                "risk_score": 70
            }

        if self.is_trusted(domain):
            return {
                "reputation": "TRUSTED",
                "risk_score": 10
            }

        return {
            "reputation": "UNKNOWN",
            "risk_score": 40
        }


domain_reputation_service = DomainReputationService()