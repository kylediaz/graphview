"""
Utility that turns breaks plaintext files apart into chapters and subchapters
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    path: Path
    header: str
    content: str = ""
    line_number: int = 0


def chapters_from_file(file_path: Path) -> list[Chunk]:
    lines = []
    try:
        file = open(file_path, "r")
        lines = file.readlines()
    except OSError:
        pass
    finally:
        file.close()

    return chapters_from_lines(lines, file_path)


def chapters_from_lines(lines: list[str], file_path: Path) -> list[Chunk]:
    chunks = []

    # Chroma handles chunking, so break documents up into chapters/
    # subchapters/etc so we can preserve chapter/subchapter title and line number,
    # and let Chroma handle the rest.
    current_chunk = Chunk(path=file_path, header=file_path.stem)
    current_chunk_content = []

    for line_number, line in enumerate(lines, start=1):
        header_level, header_content = __parse_heading(line)
        if header_level > 0:
            # finalize the chunk being created
            content = "\n".join(current_chunk_content)
            current_chunk.content = content
            chunks.append(current_chunk)

            # instantiate the new chunk to be created
            current_chunk_content.clear()
            current_chunk = Chunk(
                path=file_path, header=header_content, line_number=line_number
            )
        else:
            current_chunk_content.append(line)
        print(line_number, line, current_chunk)

    content = "\n".join(current_chunk_content)
    current_chunk.content = content
    chunks.append(current_chunk)

    return chunks


def __parse_heading(line: str) -> tuple[int, str]:
    """
    Args:
        line (str): Line that starts with <header_level> #s followed by its content
    Returns:
        tuple[int, str]: The header level and the header content.  Header level is 0 if not a header.
    """
    i = 0
    while i < len(line) and line[i] == "#":
        i += 1
    trimmed_line = line[i:].strip()
    return (i, trimmed_line)
