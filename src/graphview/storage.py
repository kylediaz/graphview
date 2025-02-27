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

    def search(self, query: str) -> list[SearchResult]:
        result = self.collection.query(
            query_texts=[query], include=["metadatas", "distances"]
        )
        ids = result['ids'][0]
        metadatas = result['metadatas'][0]
        distances = result['distances'][0]

        output = []
        for _, metadata, distance in zip(ids, metadatas, distances):
            search_result = SearchResult(metadata['file_path'], metadata['line_number'], distance)
            output.append(search_result)
        return output

    def clear(self) -> None:
        # this is a hack. sorry :)
        self.collection.delete(where={"path": { "$nin": [""]}})

    def add(self, chunks: list[Chunk]) -> None:
        ids = [chunk.id() for chunk in chunks]
        metadatas = [
            {"file_path": str(chunk.path), "line_number": str(chunk.line_number)} for chunk in chunks
        ]
        documents = [chunk.content for chunk in chunks]
        
        self.collection.add(documents=documents, ids=ids, metadatas=metadatas)