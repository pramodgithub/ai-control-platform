from typing import List, Optional

class Chunk:
    def __init__(
        self,
        id: str,
        text: str,
        section: str,
        source: str,
        created_at: str,
        score: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ):
        self.id = id
        self.text = text
        self.section = section
        self.source = source
        self.created_at = created_at
        self.score = score
        self.tags = tags or []   # ensures always a list

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "section": self.section,
            "source": self.source,
            "created_at": self.created_at,
            "score": self.score,
            "tags": self.tags,
        }