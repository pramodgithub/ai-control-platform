from app.db import get_db
from sqlalchemy import text
import json

def log_decision(
    user_input,
    retrieved,
    filtered,
    prompt,
    raw_response,
    decision,
    model_name,
    embedding_provider
):
    db = get_db()

    db.execute(
        text("""
        INSERT INTO decision_logs
        (user_input, retrieved_clauses, filtered_clauses,
         llm_prompt, raw_response, decision,
         confidence_score, model_name, embedding_provider)
        VALUES
        (:user_input, :retrieved, :filtered,
         :prompt, :raw_response, :decision,
         :confidence, :model_name, :embedding_provider)
        """),
        {
            "user_input": user_input,
            "retrieved": json.dumps(retrieved),
            "filtered": json.dumps(filtered),
            "prompt": prompt,
            "raw_response": json.dumps(raw_response),
            "decision": json.dumps(decision),
            "confidence": decision["confidence_score"],
            "model_name": model_name,
            "embedding_provider": embedding_provider
        }
    )

    db.commit()