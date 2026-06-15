import re
from typing import Dict, List, Any


class RuleEngine:

    def __init__(self):

        self.rules = [
            # PAYMENT SCAMS
            {
                "rule_name": "Payment Requirement",
                "category": "PAYMENT_SCAM",
                "weight": 0.35,
                "patterns": [
                    "processing fee",
                    "registration fee",
                    "pay to apply",
                    "advance payment",
                    "security deposit",
                    "training fee",
                    "program fee",
                    "one-time fee",
                    "one time fee",
                    "enrollment fee",
                    "enrolment fee",
                    "starter deposit",
                    "refundable deposit",
                    "activation fee",
                    "tool access fee",
                    "onboarding fee",
                    "pay a fee",
                    "fee of ₹",
                    "fee of rs",
                    "usdt",
                    "bitcoin deposit",
                    "crypto deposit",
                    "pay in crypto"
                ],
                "reason": "Requests upfront payment"
            },

            # FAKE SALARY PROMISE
            {
                "rule_name": "Unrealistic Salary",
                "category": "FAKE_JOB_PROMISE",
                "weight": 0.30,
                "patterns": [
                    "earn money fast",
                    "guaranteed income",
                    "lakh per day",
                    "high income no skills",
                    "quick money",
                    "earn ₹",
                    "earn up to ₹",
                    "earn per hour",
                    "per article",
                    "unlimited income",
                    "no cap on earnings",
                    "top performers earned",
                    "earn lakhs",
                    "₹ per month easily",
                    "guaranteed income of",
                    "guaranteed ₹",
                    "earn without limits"
                ],
                "reason": "Promises unrealistic earnings"
            },

            # URGENCY MANIPULATION
            {
                "rule_name": "Urgency Manipulation",
                "category": "URGENT_PRESSURE",
                "weight": 0.20,
                "patterns": [
                    "urgent",
                    "immediately",
                    "hurry",
                    "limited time",
                    "last chance",
                    "limited seats",
                    "slots are filling",
                    "register before",
                    "closes this",
                    "closes when",
                    "batch closes",
                    "only 47 slots",
                    "last few hours",
                    "before midnight",
                    "act now",
                    "don't miss",
                    "do not miss",
                    "right now",
                    "seats close"
                ],
                "reason": "Uses urgency pressure tactics"
            },

            # FAKE IDENTITY / NO INTERVIEW
            {
                "rule_name": "Missing Company Identity",
                "category": "FAKE_IDENTITY",
                "weight": 0.25,
                "patterns": [
                    "no company name",
                    "anonymous hiring",
                    "no interview",
                    "direct selection without interview",
                    "whatsapp only",
                    "contact us only on whatsapp",
                    "message on whatsapp",
                    "whatsapp at +91",
                    "telegram only",
                    "contact on telegram",
                    "message our coordinator",
                    "t.me/",
                    "@gmail.com",
                    "no resume required",
                    "no interviews",
                    "no paperwork",
                    "no interview needed",
                    "no interview required",   # FIX: added — covers "No interview required"
                    "direct selection",        # FIX: added — covers "Direct selection based on"
                    "direct joining",
                    "send your name",          # FIX: added — asking for personal info via chat
                    "send your whatsapp",
                    "whatsapp number"          # FIX: added — scam job asked for WhatsApp number
                ],
                "reason": "Lacks verified company identity"
            },

            # FAKE PLACEMENT GUARANTEE
            {
                "rule_name": "Fake Placement Guarantee",
                "category": "FAKE_GUARANTEE",
                "weight": 0.30,
                "patterns": [
                    "guaranteed job",
                    "guaranteed placement",
                    "100% placement",
                    "100 percent placement",
                    "placement guarantee",
                    "guaranteed selection",
                    "guaranteed a job",
                    "guaranteed a high",
                    "guaranteed offer",
                    "instant selection",
                    "direct joining without interview",
                    "offer letter immediately",
                    "100% selection"
                ],
                "reason": "Makes fake job placement guarantees"
            },

            # CRYPTO / INVESTMENT SCAM
            {
                "rule_name": "Crypto or Investment Scam",
                "category": "CRYPTO_SCAM",
                "weight": 0.35,
                "patterns": [
                    "crypto investment",
                    "bitcoin trading",
                    "cryptocurrency trading",
                    "defi investing",
                    "double your money",
                    "guaranteed returns",
                    "passive income",
                    "investment opportunity",
                    "live trading",
                    "trading wallet",
                    "altcoin",
                    "usdt",
                    "profit sharing",
                    "starter deposit",
                    "training wallet"
                ],
                "reason": "Promotes crypto or investment-based job scam"
            },

            # COMMISSION SCAM WITH DEPOSIT
            {
                "rule_name": "Commission Scam with Deposit",
                "category": "COMMISSION_SCAM",
                "weight": 0.25,
                "patterns": [
                    "pure commission",
                    "no salary",
                    "commission only",
                    "30% commission",
                    "flat commission",
                    "security deposit",
                    "refundable security",
                    "upi deposit",
                    "pay via upi",
                    "verification deposit",
                    "onboarding verification",
                    "deposit returned after"
                ],
                "reason": "Commission-only role requiring upfront deposit"
            },

            # GENUINE INDICATORS (negative weight — reduces scam score)
            # FIX: Removed "hr team" — too broad, scam jobs also use this phrase
            #      e.g. "Our HR team will contact you shortly"
            # FIX: Capped legitimate signal reduction using min() in analyze_job_text
            {
                "rule_name": "Legitimate Job Signals",
                "category": "GENUINE_SIGNALS",
                "weight": -0.15,
                "patterns": [
                    "no fees required",
                    "no registration fee",
                    "interview process",
                    "structured interview",
                    "apply through",
                    "careers portal",
                    "apply on our website",
                    "linkedin",
                    "official website",
                    # REMOVED: "hr team" — too generic, matches scam postings
                    "does not charge",
                    "does not request payment",
                    "free to apply",
                    "no payment required",
                    "background verification",
                    "offer letter from",
                    "official email",
                    "@accenture.com",
                    "@razorpay.com",
                    "@deloitte.com",
                    "@swiggy.in",
                    "@paloaltonetworks.com"
                ],
                "reason": "Shows legitimate hiring process"
            }
        ]

    def analyze_job_text(self, text: str) -> Dict[str, Any]:

        text_lower = text.lower()

        total_score = 0.0
        matched_rules = []
        category_scores = {}

        for rule in self.rules:

            rule_hits = 0

            for pattern in rule["patterns"]:
                if pattern in text_lower:
                    rule_hits += 1

            if rule_hits > 0:

                # FIX: Cap score contribution per rule at 1x weight (not hits * weight).
                # Previously, 3 hits in one rule tripled the weight, skewing scores.
                # Now each rule contributes at most its defined weight, regardless of
                # how many patterns matched. Multiple hits still confirm the rule fired,
                # but don't multiply the risk score.
                score = rule["weight"]  # was: rule["weight"] * rule_hits
                total_score += score

                matched_rules.append({
                    "rule_name": rule["rule_name"],
                    "category": rule["category"],
                    "reason": rule["reason"],
                    "hits": rule_hits
                })

                category_scores[rule["category"]] = (
                    category_scores.get(rule["category"], 0) + score
                )

        # -------------------------
        # NORMALIZATION
        # FIX: Clamp to [0, 1] — genuine signals (negative weight) can push
        # total below 0, which should resolve to 0, not a negative confidence.
        # -------------------------
        confidence = min(max(total_score, 0.0), 1.0)

        # -------------------------
        # RISK LEVEL
        # -------------------------
        if confidence < 0.3:
            risk_level = "LOW"
        elif confidence < 0.6:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        # -------------------------
        # DEFAULT CASE
        # -------------------------
        if not matched_rules:
            matched_rules = [{
                "rule_name": "No Strong Scam Signals",
                "category": "SAFE",
                "reason": "No suspicious patterns detected",
                "hits": 0
            }]

        explanation = self._generate_explanation(matched_rules)

        return {
            "is_scam": confidence >= 0.4,  # FIX: lowered from 0.5; scores 0.40–0.49 were falsely GENUINE
            "confidence": round(confidence, 2),
            "risk_level": risk_level,
            "matched_rules": matched_rules,
            "category_scores": category_scores,
            "explanation": explanation
        }

    def _generate_explanation(self, matched_rules: List[Dict]) -> str:

        if len(matched_rules) == 1 and matched_rules[0]["category"] == "SAFE":
            return "No strong scam indicators detected in this job posting."

        reasons = [r["reason"] for r in matched_rules if r["category"] != "SAFE"]

        return (
            "This job posting appears suspicious due to: "
            + ", ".join(reasons)
            + "."
        )


rule_engine = RuleEngine()


def analyze_job_text(text: str):
    return rule_engine.analyze_job_text(text)