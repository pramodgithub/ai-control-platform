import re

def is_heading(line):
    """
    Detect if a line is a section heading.
    """

    line = line.strip()

    if len(line) < 4:
        return False

    # ignore numeric markers
    if line.startswith("##"):
        line = line.replace("#", "").strip()

    # ignore lines that are only numbers
    if line.replace(".", "").isdigit():
        return False

    # heading characteristics
    return (
        line.isupper()
        and len(line.split()) <= 8
        and not "|" in line
    )


def split_by_sections(text):
    """
    Split text into sections using heading detection.
    """

    lines = text.split("\n")

    sections = []
    current_title = "GENERAL"
    current_content = []

    for line in lines:
        if is_heading(line):
            if current_content:
                sections.append((current_title, "\n".join(current_content).strip()))
                current_content = []

            current_title = re.sub(r'^\d+\.?\s*', '', line).strip("# ").strip()
        else:
            current_content.append(line)

    if current_content and "\n".join(current_content).strip():
        sections.append((current_title, "\n".join(current_content).strip()))

    return sections