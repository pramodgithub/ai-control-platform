from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.control_engine import evaluate_document
from app.governance.schema import ComplianceDecision

router = APIRouter(prefix="/evaluate", tags=["Evaluation"])

class EvaluationRequest(BaseModel):
    document: str

@router.post("/", response_model=ComplianceDecision)
def evaluate(request: EvaluationRequest):
    result = evaluate_document(request.document)
    return result