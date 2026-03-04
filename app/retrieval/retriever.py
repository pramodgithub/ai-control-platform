from sqlalchemy import text
from app.database import SessionLocal
from app.embeddings.factory import get_embedding_provider


provider = get_embedding_provider()


def retrieve_similar_clauses(query_text: str, top_k: int = 5):
    query_embedding = provider.embed(query_text)

    # Convert list to pgvector string format
    vector_str = "[" + ",".join(map(str, query_embedding)) + "]"

    db = SessionLocal()

    similarity_query = text("""
        SELECT
            policy_id,
            section_title,
            clause_id,
            clause_text,
            risk_category,
            severity,
            embedding <-> CAST(:query_embedding AS vector) AS distance
        FROM policy_chunks
        ORDER BY embedding <-> CAST(:query_embedding AS vector)
        LIMIT :top_k
    """)

    results = db.execute(similarity_query, {
        "query_embedding": vector_str,
        "top_k": top_k
    }).fetchall()

    db.close()

    return results