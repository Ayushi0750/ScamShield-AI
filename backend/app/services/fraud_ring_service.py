from typing import Dict, Any, List


class FraudRingService:
    """
    Fraud Ring Detection Engine
    """

    def analyze_cluster(self, cluster: Dict[str, Any]) -> Dict[str, Any]:

        score = 0
        reasons = []

        recruiters = cluster.get("recruiters", [])
        emails = cluster.get("emails", [])
        domains = cluster.get("domains", [])
        jobs = cluster.get("jobs", [])

        # 1. Multiple recruiters
        if len(recruiters) > 1:
            score += 35
            reasons.append("Multiple recruiters detected in same cluster")

        # 2. Suspicious domains
        suspicious_domains = {
            "mailinator.com",
            "10minutemail.com",
            "tempmail.com",
            "quickhire-now.com"
        }

        cleaned_domains = [d.replace("domain_", "") for d in domains]

        # COORDINATED PATTERN
        if len(recruiters) > 1 and len(set(cleaned_domains)) == 1:
            score += 35
            reasons.append("Coordinated recruiters using same domain (fraud pattern)")

        for d in cleaned_domains:
            if d in suspicious_domains:
                score += 45
                reasons.append(f"Suspicious domain detected: {d}")

        # 3. Email abuse
        if len(emails) >= 2:
            score += 20
            reasons.append("High email concentration detected")

        # 4. Job spam
        if len(jobs) >= 2:
            score += 15
            reasons.append("Multiple job postings from same cluster")

        # 5. Density
        total_nodes = len(recruiters) + len(emails) + len(domains) + len(jobs)

        if total_nodes >= 5:
            score += 10
            reasons.append("High cluster density")

        score = max(0, min(100, score))

        if score >= 75:
            label = "HIGH_RISK_RING"
        elif score >= 45:
            label = "SUSPICIOUS_RING"
        else:
            label = "SAFE"

        return {
            "cluster_id": cluster.get("cluster_id"),
            "risk_score": score,
            "label": label,
            "reasons": reasons,
            "size": cluster.get("size")
        }


fraud_ring_service = FraudRingService()
