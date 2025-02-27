from pathlib import Path
import os

import graphview.chunker as chunker
import graphview.storage as storage


def search_file(file_path: Path, line_number: int | None = 0) -> None:
    pass

def search_text(query: str) -> None:
    raise NotImplementedError()

def build_index(dir: Path) -> None:
    db = storage.Storage()
    db.clear()
    chunks = []
    for entry in os.scandir(dir):
        if entry.name.endswith(".md"):
            file_path = Path(entry.path)
            entry_chunks = chunker.chapters_from_file(file_path)
            chunks.extend(entry_chunks)
    db.add(chunks)