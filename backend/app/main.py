from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.scam_routes import router as scam_router
from app.routes.history import router as history_router
from app.routes.recruiter_routes import router as recruiter_router
from app.routes.fraud_graph_routes import router as fraud_graph_router
from app.routes.unified_analysis import router as unified_router


app = FastAPI(title="ScamShield AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(scam_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(recruiter_router, prefix="/api")
app.include_router(fraud_graph_router, prefix="/api")
app.include_router(unified_router, prefix="/api")


@app.get("/")
def home():
    return {"message": "ScamShield AI is running"}