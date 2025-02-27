from dataclasses import dataclass
import chromadb
from chromadb import Collection, ClientAPI
from pathlib import Path

from graphview.util import singleton
from graphview.chunker import Chunk

DATABASE_PATH = ".graphview/"

@dataclass
class SearchResult:
    file_path: Path
    line_number: int
    distance: float


@singleton
class Storage:

    def __init__(self):
        self.client: ClientAPI = chromadb.PersistentClient(path=DATABASE_PATH)
        self.collection: Collection = self.client.get_or_create_collection(
            name="chunks"
        )

    def search(self, query: str) -> list[Chunk]:
        pass

    def clear(self) -> None:
        # this is a hack. sorry :)
        self.collection.delete(where={"path": { "$nin": [""]}})

    def add(self, chunks: list[Chunk]) -> None:
        ids = [chunk.id() for chunk in chunks]
        metadatas = [
            {"path": str(chunk.path), "line_number": str(chunk.line_number)} for chunk in chunks
        ]
        documents = [chunk.content for chunk in chunks]
        
        self.collection.add(documents=documents, ids=ids, metadatas=metadatas)