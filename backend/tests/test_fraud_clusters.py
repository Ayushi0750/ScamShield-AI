from app.services.fraud_graph_service import fraud_graph_service


fraud_graph_service.build_relationship(
    recruiter_id="1",
    email="hr@microsoft.com",
    domain="microsoft.com",
    job_id="job_101"
)

fraud_graph_service.build_relationship(
    recruiter_id="2",
    email="fake@mailinator.com",
    domain="mailinator.com",
    job_id="job_102"
)

print("\nNODES:")
print(fraud_graph_service.get_nodes())

print("\nCLUSTERS:")
print(fraud_graph_service.get_cluster_summary())