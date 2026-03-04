import re

def chunk_policy(text: str):
    """
    Splits policy text into clauses using clause IDs.
    """

    pattern = r"(SEC-\d{2}.*?)\n(.*?)(?=\nSEC-\d{2}|\Z)"
    matches = re.findall(pattern, text, re.S)

    chunks = []

    for title, body in matches:
        clause_id = title.split()[0]

        chunks.append({
            "clause_id": clause_id,
            "title": title.strip(),
            "text": body.strip()
        })

    return chunks