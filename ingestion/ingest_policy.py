from loaders.reader import load_document
from processors.cleaner import clean_text
from processors.sectioner import split_by_sections
from processors.chunker import chunk_text, semantic_chunk_section, chunk_definitions, is_table_noise
from processors.chunk_model import Chunk
from processors.chunk_quality import is_high_quality, score_chunk
from metadata.tagger import detect_tags, add_context_tags
from processors.ingest_mapper import process_chunks
from datetime import datetime, UTC
from pathlib import Path

import uuid
from halo import Halo

spinner = Halo(text='Processing chunks...', spinner='dots')
spinner.start()

file_path = "documents/information_security_policy.pdf"

text = load_document(file_path)

cleaned_text = clean_text(text)
""" print("\nCleaned text length:", len(cleaned_text))
print(cleaned_text[:500])
"""
print("\n" + "=" * 80 + "\n")

sections = split_by_sections(cleaned_text)
""" print(f"Sections detected: {len(sections)}")
for s in sections[:10]:
    print("SECTION:", s[0]) """
    

final_chunks = []

for title, section_text in sections:

    # Skip empty sections
    if not section_text.strip():
        continue

    # Use definition chunking if section is definitions
    if "DEFINITION" in title.upper():
        semantic_chunks = chunk_definitions(section_text, title)
    else:
        semantic_chunks = semantic_chunk_section(section_text, title)

    for item in semantic_chunks:
        chunk = item["text"].strip()

        if not chunk or is_table_noise(chunk):
            continue

        score = score_chunk(chunk)

        if not is_high_quality(chunk):
            continue

        tags = detect_tags(chunk)
        tags = add_context_tags(tags, item["section"])
        if "\n" in chunk:
            heading, body = chunk.split("\n", 1)
            chunk = f"{heading.strip()}: {body.strip()}"    

        chunk_obj = Chunk(
            id=str(uuid.uuid4()),
            text=chunk,
            section=item["section"],
            source=Path(file_path).name,
            created_at=datetime.now(UTC).isoformat(),
            score=score,
            tags=tags
            
        )

        final_chunks.append(chunk_obj)



print(f"\nChunks created: {len(final_chunks)}\n")

process_chunks(final_chunks, policy_id="ISO27001_2022")



""" print("Sample:\n")
if final_chunks:
    print(final_chunks[0].text[:300])
else:
    print("⚠️ No chunks created — check cleaner/sectioner")

for c in final_chunks:
    print(c.to_dict())
    print("\n" + "=" * 80 + "\n") 

print("\nTag distribution:\n")

from collections import Counter

all_tags = [tag for c in final_chunks for tag in c.tags]
print(Counter(all_tags)) """

spinner.succeed('Done!')
