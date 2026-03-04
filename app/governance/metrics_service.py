from app.db import get_db

def get_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM compliance_decisions")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(confidence_score) FROM compliance_decisions")
    avg_conf = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM compliance_decisions WHERE needs_human_review = TRUE")
    review_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_evaluations": total,
        "average_confidence": round(avg_conf or 0, 3),
        "human_review_rate": round((review_count / total), 3) if total > 0 else 0
    }