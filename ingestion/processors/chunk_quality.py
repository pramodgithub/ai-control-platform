import re

# --- configuration ---
MIN_LENGTH = 40
MAX_LENGTH = 1200

POLICY_KEYWORDS = [
    "security", "policy", "risk", "control", "compliance",
    "data", "access", "system", "information", "management",
    "responsibility", "objective", "procedure"
]


def score_chunk(text: str) -> float:
    """
    Assign quality score to chunk.
    Higher = better.
    """

    if not text or not text.strip():
        return 0

    score = 0
    text = text.strip()

    # --- Length scoring ---
    length = len(text)

    if length < MIN_LENGTH:
        score -= 2
    elif MIN_LENGTH <= length <= MAX_LENGTH:
        score += 2

    # --- Sentence completeness ---
    if re.search(r'[.!?]$', text):
        score += 1

    # --- Word richness ---
    words = text.split()
    if len(words) > 8:
        score += 1

    # --- Keyword presence ---
    keyword_hits = sum(1 for kw in POLICY_KEYWORDS if kw in text.lower())
    score += min(keyword_hits, 3)

    # --- Penalize numeric/table noise ---
    if re.fullmatch(r'[\d\W\s]+', text):
        score -= 3

    if "|" in text and text.count("|") > 5:
        score -= 2

    # --- Penalize repeated dots/lines ---
    if "....." in text or "____" in text:
        score -= 1

    return score


def is_high_quality(text: str, threshold: float = 1.5) -> bool:
    """
    Decide if chunk should be kept.
    """
    return score_chunk(text) >= threshold