import re
from collections import Counter

def remove_repeated_columns(text: str) -> str:
    """
    Collapse repeated table column values.
    """
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        if "|" in line:
            cells = [c.strip() for c in line.split("|") if c.strip()]
            unique_cells = []

            for cell in cells:
                if cell not in unique_cells:
                    unique_cells.append(cell)

            if unique_cells:
                cleaned_lines.append(" | ".join(unique_cells))
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_toc_like_lines(text: str) -> str:
    """
    Remove TOC-like repeated section rows.
    """
    cleaned_lines = []
    for line in text.splitlines():
        if re.search(r'\b\d+\b$', line) and line.count("|") > 3:
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def remove_page_numbers(text: str) -> str:
    return re.sub(r'\b\d+\s*$', '', text, flags=re.MULTILINE)



def remove_toc_noise(text):
    """
    Remove table of contents artifacts and dotted leaders
    """

    # remove image placeholders
    text = re.sub(r'<!-- image -->', '', text)

    # remove dotted leader lines
    text = re.sub(r'\.{5,}', '', text)

    # remove TOC lines like:
    # 1. INTRODUCTION .....
    text = re.sub(r'^\s*\d+\.\s+[A-Z\s]+\s*$', '', text, flags=re.MULTILINE)

    return text


def remove_footer_blocks(text):
    text = re.sub(
        r'Date of approval\s*\|\s*Author\s*\|\s*Document\s*\|\s*Version\s*\|\s*Page',
        '',
        text,
        flags=re.IGNORECASE
    )
    return text


def remove_index_sections(text):
    """
    Remove section index pages listing headings only.
    """

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        # remove lines that look like index entries
        if re.match(r'^\s*\d+(\.\d+)*\s*\|?\s*[A-Z\s&]+\s*$', line):
            continue

        # remove lines with many pipes but no sentences
        if line.count("|") > 3 and len(line) < 120:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)



def remove_repeated_lines(text: str, min_repeats: int = 3) -> str:
    """
    Remove lines repeated frequently (e.g., headers/footers).
    Keeps meaningful repeated content intact.
    """

    lines = [line.strip() for line in text.split("\n")]

    # Count occurrences
    line_counts = Counter(lines)

    cleaned_lines = []

    for line in lines:
        if line_counts[line] >= min_repeats and len(line) < 120:
            # Skip repeated header/footer lines
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def normalize_whitespace(text: str) -> str:
    """
    Normalize spacing issues caused by PDF extraction.
    """

    # Convert Windows/Mac line endings → Unix
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing spaces
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Replace multiple spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines (more than 2 → 2)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix broken line joins inside sentences
    # Example:
    # Information
    # Security → Information Security
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    return text.strip()

def remove_toc_rows(text):
    """
    Remove table-of-contents rows like:
    | INTRODUCTION4 | 2. | DEFINITIONS
    """
    lines = text.split("\n")

    cleaned = []
    for line in lines:
        if "|" in line and any(char.isdigit() for char in line):
            if len(line) < 120:
                continue
        cleaned.append(line)

    return "\n".join(cleaned)

def clean_text(text: str) -> str:
        
        # --- Normalize structure ---
        text = remove_pipe_tables(text)
        text = remove_footer_dates(text)
        text = normalize_whitespace(text)

        # --- Remove repeated patterns ---
        text = remove_repeated_lines(text)
        text = remove_repeated_columns(text)
        text = remove_toc_rows(text)

        # --- Remove layout noise ---
        text = remove_page_numbers(text)
        text = remove_footer_blocks(text)

        # --- Remove TOC & index artifacts ---
        text = remove_toc_like_lines(text)
        text = remove_toc_noise(text)
        text = remove_index_sections(text)

        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()


def remove_pipe_tables(text):
    """
    Remove true table blocks while preserving content lines.
    """
    lines = text.split("\n")
    cleaned = []
    pipe_block = []

    for line in lines:
        # detect table-like row (multiple columns)
        if line.count("|") >= 3:
            pipe_block.append(line)
            continue
        else:
            # if block was short, keep it (likely real content)
            if 0 < len(pipe_block) <= 2:
                cleaned.extend(pipe_block)

            pipe_block = []

        cleaned.append(line)

    return "\n".join(cleaned)


def remove_footer_dates(text):
    """
    Remove repeating approval/footer metadata lines safely
    """
    lines = text.split("\n")

    cleaned = []
    for line in lines:
        if "out of" in line and len(line) < 40:
            continue
        cleaned.append(line)

    return "\n".join(cleaned)