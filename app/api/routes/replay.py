from fastapi import APIRouter
from app.replay.replay_service import get_decision_by_id

router = APIRouter(prefix="/replay", tags=["Replay"])

@router.get("/{decision_id}")
def replay(decision_id: int):
    return get_decision_by_id(decision_id)