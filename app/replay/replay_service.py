from app.db import get_db

def get_decision_by_id(decision_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM compliance_decisions WHERE id = %s",
        (decision_id,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return {"error": "Decision not found"}

    return {
        "id": row[0],
        "decision": row[1],
        "risk_level": row[2],
        "violated_clauses": row[3],
        "explanation": row[4],
        "confidence_score": row[5],
        "needs_human_review": row[6],
        "created_at": row[7],
    }