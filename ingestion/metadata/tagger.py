import re

# use package-relative import so that the module can be imported regardless of
# the working directory or pythonpath. `tag_rules` lives in the same
# package (`ingestion.metadata`) as this module.
from .tag_rules import TAG_RULES

def detect_tags(text):
    text_lower = text.lower()
    tags = set()

    for tag, patterns in TAG_RULES.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                tags.add(tag)
                break

    return list(tags)

def add_context_tags(tags, section_title):
    title = section_title.lower()

    if "definition" in title:
        tags.append("definition")

    if "scope" in title:
        tags.append("scope")

    if "responsibilit" in title:
        tags.append("responsibilities")

    if "objective" in title:
        tags.append("objectives")

    if "security" in title:
        tags.append("security")

    return list(set(tags))