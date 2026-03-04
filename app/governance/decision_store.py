from app.db import get_connection

def save_decision(decision):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO compliance_decisions
        (decision, risk_level, violated_clauses, explanation, confidence_score, needs_human_review)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            decision.decision,
            decision.risk_level,
            decision.violated_clauses,
            decision.explanation,
            decision.confidence_score,
            decision.needs_human_review,
        ),
    )

    decision_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return decision_id