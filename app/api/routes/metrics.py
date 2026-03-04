from fastapi import APIRouter
from app.governance.metrics_service import get_metrics

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/")
def metrics():
    return get_metrics()