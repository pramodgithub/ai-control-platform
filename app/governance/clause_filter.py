from typing import List
from app.ai.llm_gateway import LLMGateway


def filter_relevant_clauses(
    llm_gateway: LLMGateway,
    user_input: str,
    clauses: List
) -> List:
    """
    Filters retrieved policy clause OBJECTS using LLM.
    Always returns the same object type it received.
    """

    if not clauses:
        return []

    # Build clause list for prompt
    clause_list = "\n".join(
        [f"{c.policy_id}-{c.clause_id}: {c.clause_text}" for c in clauses]
    )

    prompt = f"""
You are a compliance relevance filter.

Return ONLY clause IDs separated by commas.
Format example:
ISO27001_2022-2.6,ISO27001_2022-2.10

If none apply, return:
NONE

User Input:
{user_input}

Policy Clauses:
{clause_list}
"""

    try:
        response = llm_gateway.generate(prompt)
    except Exception as e:
        print("Clause filter LLM error:", e)
        return clauses  # fail-safe

    print("Clause Filter Raw Response:", response)

    if not response or response.strip().upper() == "NONE":
        return []

    # Parse comma-separated IDs
    selected_ids = [r.strip() for r in response.split(",") if r.strip()]

    # Map back to ORIGINAL clause objects
    filtered_clauses = [
        clause for clause in clauses
        if f"{clause.policy_id}-{clause.clause_id}" in selected_ids
    ]

    return filtered_clauses