from fastapi import APIRouter

from app.core.singletons import fraud_graph_service

router = APIRouter()


@router.get("/fraud/graph")
def get_graph():

    nodes = fraud_graph_service.get_nodes()
    edges = fraud_graph_service.get_edges()

    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }


#fraud clusters
@router.get("/fraud/clusters")
def get_clusters():

    return fraud_graph_service.get_cluster_summary()


# fraud rings
@router.get("/fraud/rings")
def get_fraud_rings():

    return fraud_graph_service.get_fraud_rings()


#ingest
@router.post("/fraud/ingest")
def ingest_data(payload: dict):

    recruiter_id = payload.get("recruiter_id")
    email = payload.get("email")
    domain = payload.get("domain")
    job_id = payload.get("job_id")

    result = fraud_graph_service.build_relationship(
        recruiter_id=recruiter_id,
        email=email,
        domain=domain,
        job_id=job_id
    )

    return {
        "message": "Data ingested successfully",
        "result": result
    }