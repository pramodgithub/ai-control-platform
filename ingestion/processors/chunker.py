import re

def chunk_text(section, max_chars=800):
    sentences = re.split(r'(?<=[.!?]) +', section)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_chars:
            current += " " + sentence
        else:
            chunks.append(current.strip())
            current = sentence

    if current:
        chunks.append(current.strip())

    return chunks


    import re

def semantic_chunk_section(text, section_name, max_words=220, min_words=60):
    """
    Creates semantic chunks from section text.
    Splits by paragraphs, bullets, and definitions.
    """

    # Split into logical blocks
    blocks = re.split(r'\n\s*\n|(?<=\.)\s+(?=[A-Z])', text)

    chunks = []
    current = []

    for block in blocks:
        words = block.split()

        if not words:
            continue

        current.extend(words)

        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []

    # Add remaining
    if current:
        if chunks and len(current) < min_words:
            chunks[-1] += " " + " ".join(current)
        else:
            chunks.append(" ".join(current))

    return [
        {
            "section": section_name,
            "text": chunk.strip()
        }
        for chunk in chunks
    ]


def chunk_definitions(text, section_name):
    items = re.split(r'##\s+', text)
    chunks = []

    for item in items:
        item = item.strip()
        if len(item.split()) > 5:
            chunks.append({
                "section": section_name,
                "text": item
            })

    return chunks


def is_table_noise(text):
    """
    Detect table-like metadata blocks
    """
    pipe_ratio = text.count("|") / max(len(text), 1)

    # many pipes OR typical metadata keywords
    if pipe_ratio > 0.02:
        return True

    keywords = [
        "document name",
        "version",
        "date of approval",
        "approving authority",
        "data classification",
        "review history",
        "code |",
        "scope of application",
    ]

    lowered = text.lower()

    return any(k in lowered for k in keywords)