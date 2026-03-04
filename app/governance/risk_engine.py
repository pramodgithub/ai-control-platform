from app.db import get_db
from sqlalchemy import text


def compute_risk(violated_clauses):
    if not violated_clauses:
        return "LOW"

    db = get_db()
    total_score = 0

    for clause_id in violated_clauses:
        result = db.execute(
            text("""
                SELECT criticality_weight 
                FROM policy_chunks
                WHERE clause_id = :clause_id
            """),
            {"clause_id": clause_id}
        ).fetchone()

        if result:
            total_score += result.criticality_weight

    db.close()

    # Normalize if needed
    if total_score >= 0.8:
        return "CRITICAL"
    elif total_score >= 0.5:
        return "HIGH"
    elif total_score >= 0.2:
        return "MEDIUM"
    else:
        return "LOW"