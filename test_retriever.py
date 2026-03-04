from dotenv import load_dotenv
load_dotenv()

from app.retrieval.retriever import retrieve_similar_clauses

query = "Vendor stores EU customer data in US data centers"

results = retrieve_similar_clauses(query, top_k=3)

for r in results:
    print("------")
    print("Policy:", r.policy_id)
    print("Clause:", r.clause_id)
    print("Text:", r.clause_text)
    print("Distance:", r.distance)