from typing import Dict, List, Any
import networkx as nx


class FraudGraphService:

    def __init__(self):
        self.graph = nx.Graph()

    # ---------------- NODE ----------------
    def add_recruiter(self, recruiter_id: str, data: Dict[str, Any] = None):
        self.graph.add_node(f"recruiter_{recruiter_id}", type="recruiter", **(data or {}))

    def add_email(self, email: str):
        self.graph.add_node(f"email_{email}", type="email", email=email)

    def add_domain(self, domain: str):
        self.graph.add_node(f"domain_{domain}", type="domain", domain=domain)

    def add_job_post(self, job_id: str, data: Dict[str, Any] = None):
        self.graph.add_node(f"job_{job_id}", type="job_post", **(data or {}))

    # ---------------- EDGE ----------------
    def link_recruiter_email(self, recruiter_id: str, email: str):
        self.graph.add_edge(f"recruiter_{recruiter_id}", f"email_{email}", relation="USES_EMAIL")

    def link_email_domain(self, email: str, domain: str):
        self.graph.add_edge(f"email_{email}", f"domain_{domain}", relation="BELONGS_TO")

    def link_recruiter_job(self, recruiter_id: str, job_id: str):
        self.graph.add_edge(f"recruiter_{recruiter_id}", f"job_{job_id}", relation="POSTED")

    def link_domain_job(self, domain: str, job_id: str):
        self.graph.add_edge(f"domain_{domain}", f"job_{job_id}", relation="HOSTS")

    # ---------------- PIPELINE ----------------
    def build_relationship(self, recruiter_id, email, domain, job_id=None):

        self.add_recruiter(recruiter_id)
        self.add_email(email)
        self.add_domain(domain)

        self.link_recruiter_email(recruiter_id, email)
        self.link_email_domain(email, domain)

        if job_id:
            self.add_job_post(job_id)
            self.link_recruiter_job(recruiter_id, job_id)
            self.link_domain_job(domain, job_id)

        return {"status": "success"}

    # ---------------- GRAPH ----------------
    def get_nodes(self):
        return list(self.graph.nodes(data=True))

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def detect_clusters(self):
        clusters = []
        components = list(nx.connected_components(self.graph))

        for idx, component in enumerate(components):

            recruiters, emails, domains, jobs = [], [], [], []

            for node in component:
                node_type = self.graph.nodes[node].get("type")

                if node_type == "recruiter":
                    recruiters.append(node)
                elif node_type == "email":
                    emails.append(node)
                elif node_type == "domain":
                    domains.append(node)
                elif node_type == "job_post":
                    jobs.append(node)

            clusters.append({
                "cluster_id": idx,
                "size": len(component),
                "recruiters": recruiters,
                "emails": emails,
                "domains": domains,
                "jobs": jobs
            })

        return clusters

    def get_cluster_summary(self):
        clusters = self.detect_clusters()

        return {
            "total_clusters": len(clusters),
            "largest_cluster_size": max((c["size"] for c in clusters), default=0),
            "clusters": clusters
        }

    
    def get_fraud_rings(self, fraud_ring_service):

        clusters = self.detect_clusters()

        return [
            fraud_ring_service.analyze_cluster(c)
            for c in clusters
        ]

