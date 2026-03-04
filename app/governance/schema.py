from pydantic import BaseModel
from typing import List, Optional


class ComplianceDecision(BaseModel):
    decision: str  # COMPLIANT | NON_COMPLIANT | INSUFFICIENT_CONTEXT
    risk_level: str  # LOW | MEDIUM | HIGH | CRITICAL
    violated_clauses: Optional[List[str]] = []
    explanation: str
    confidence_score: float  # 0.0 - 1.0
    needs_human_review: bool