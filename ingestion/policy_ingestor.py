import os

from dotenv import load_dotenv
from sqlalchemy import text
from database import SessionLocal
from embeddings.factory import get_embedding_provider

load_dotenv()
provider = get_embedding_provider()

def ingest_policy_clause(
            policy_id: str,
            section_title: str,
            clause_id: str,
            clause_text: str,
            domain: str,
            risk_category: str,
            severity: str,
            data_type: str,
            regulatory_scope: str,
            criticality_weight: float
        ):
    embedding = provider.embed(clause_text)
#   print(f"Embedding successful! Vector length: {len(embedding)}")
    
    db = SessionLocal()

    insert_query = text("""
                    INSERT INTO policy_chunks (
                        policy_id,
                        section_title,
                        clause_id,
                        clause_text,
                        domain,
                        risk_category,
                        severity,
                        data_type,
                        regulatory_scope,
                        criticality_weight,
                        embedding,
                        embedding_provider,
                        embedding_dimension
                    )
                    VALUES (
                        :policy_id,
                        :section_title,
                        :clause_id,
                        :clause_text,
                        :domain,
                        :risk_category,
                        :severity,
                        :data_type,
                        :regulatory_scope,
                        :criticality_weight,
                        :embedding,
                        :embedding_provider,
                        :embedding_dimension
                    )
                """)

    db.execute(insert_query, {
                    "policy_id": policy_id,
                    "section_title": section_title,
                    "clause_id": clause_id,
                    "clause_text": clause_text,
                    "domain": domain,
                    "risk_category": risk_category,
                    "severity": severity,
                    "data_type": data_type,
                    "regulatory_scope": regulatory_scope,
                    "criticality_weight": criticality_weight,
                    "embedding": embedding,
                    "embedding_provider": os.getenv("EMBEDDING_PROVIDER"),
                    "embedding_dimension": len(embedding)
                })

    db.commit()
    db.close()