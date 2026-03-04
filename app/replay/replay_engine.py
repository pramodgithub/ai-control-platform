from app.db import get_db
from sqlalchemy import text
from app.governance.decision_engine import DecisionEngine
import json


class ReplayEngine:

    def __init__(self):
        self.engine = DecisionEngine()

    def replay_decision(self, decision_id: int):
        db = get_db()

        record = db.execute(
            text("SELECT * FROM decision_logs WHERE id = :id"),
            {"id": decision_id}
        ).fetchone()

        if not record:
            raise ValueError("Decision not found")

        original_decision = record.decision
        if isinstance(original_decision, str):
            original_decision = json.loads(original_decision)

        print("Re-running decision for input:")
        print(record.user_input)

        new_decision = self.engine.evaluate(record.user_input)

        # ---- Drift Detection ----

        classification_changed = (
            original_decision["decision"] != new_decision.decision
        )

        clauses_changed = (
            set(original_decision.get("violated_clauses", []))
            != set(new_decision.violated_clauses)
        )

        confidence_delta = abs(
            original_decision["confidence_score"]
            - new_decision.confidence_score
        )

        unstable = (
            classification_changed
            or clauses_changed
            or confidence_delta > 0.25
        )

        print("\n--- Drift Analysis ---")
        print("Classification Changed:", classification_changed)
        print("Clauses Changed:", clauses_changed)
        print("Confidence Delta:", round(confidence_delta, 3))
        print("Unstable:", unstable)

        return new_decision


# top‑level convenience wrapper so callers can just import a function
# instead of having to instantiate ReplayEngine themselves.
def replay_decision(decision_id: int):
    """Run a decision replay using a fresh ReplayEngine instance."""
    return ReplayEngine().replay_decision(decision_id)