from pyfzf import FzfPrompt
from pathlib import Path
import os

import graphview.chunker as chunker
import graphview.storage as storage


def search_file(file_path: Path, line_number: int | None = 0) -> str | None:
    line_number = line_number if line_number else 0
    chunk = __get_chunk_at_line(file_path, line_number)
    return search_text(f"{chunk.header}\n{chunk.content}")


def __get_chunk_at_line(file_path: Path, line_number: int) -> chunker.Chunk:
    if line_number < 0:
        raise ValueError(f"Line number must be nonnegative (given {line_number})")

    chunks = chunker.chapters_from_file(file_path)

    for chunk in reversed(chunks):
        if chunk.line_number >= line_number:
            return chunk
    # A valid chunk must exist since line_number >= 0 and a chunk starting at
    # line 0 always exists
    raise RuntimeError()


def search_text(query: str) -> str | None:
    db = storage.Storage()
    results = db.search(query)
    results.sort(key=lambda r: r.distance)

    dirs = [r.file_path for r in results]
    fzf = FzfPrompt()
    fzf_result = fzf.prompt(dirs)
    if len(fzf_result) == 1:
        return fzf_result[0]
    else:
        return None


def build_index(dir: Path) -> None:
    db = storage.Storage()
    db.clear()
    chunks = []
    for root, dirs, files in os.walk(dir):
        dirs[:] = [d for d in dirs if __is_valid_dir(d)]
        files[:] = [f for f in files if __is_valid_file(f)]
        for file in files:
            path = os.path.join(root, file)
            file_path = Path(path)
            entry_chunks = chunker.chapters_from_file(file_path)
            chunks.extend(entry_chunks)
    db.add(chunks)


def __is_valid_dir(dir: str) -> bool:
    return not dir.startswith(".")


def __is_valid_file(file: str) -> bool:
    return not file.startswith(".") and file.endswith(".md")
