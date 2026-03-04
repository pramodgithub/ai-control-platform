import re

def extract_section_number(section_title: str):
    match = re.match(r"(\d+)", section_title)
    return match.group(1) if match else "0"

def detect_domain(tags):
    priority = [
        "security-principle",
        "risk",
        "compliance",
        "privacy",
        "access-control",
        "business-continuity",
        "responsibilities",
        "asset-management",
        "definition",
    ]

    for p in priority:
        if p in tags:
            return p

    return "general"

def detect_risk_category(tags):
    if "risk" in tags:
        return "operational"

    if "security-principle" in tags:
        return "security"

    if "compliance" in tags:
        return "regulatory"

    if "privacy" in tags:
        return "privacy"

    if "business-continuity" in tags:
        return "operational"

    return "general"

def detect_severity(text):
    text = text.lower()

    if "must" in text or "shall" in text:
        return "high"

    if "should" in text:
        return "medium"

    return "low"

def detect_data_type(text):
    text = text.lower()

    if "personal data" in text or "privacy" in text:
        return "personal"

    if "financial" in text:
        return "financial"

    return "organizational"


def detect_regulatory_scope(text):
    text = text.lower()

    if "iso 27001" in text:
        return "ISO27001"

    if "gdpr" in text:
        return "GDPR"

    if "sox" in text:
        return "SOX"

    return "internal"


def compute_criticality(tags, severity, score):
    weight = score or 5

    if "risk" in tags:
        weight += 2

    if severity == "high":
        weight += 2

    if "security-principle" in tags:
        weight += 1

    return min(weight, 10)




