import asyncio
import argparse
import uuid
from pathlib import Path
from qdrant_client.models import PointStruct
from rag.embedder import embed_query
from rag.qdrant_client import _client, ensure_collection
from config import settings

CHUNK_SIZE = 500


def chunk_text(text: str, size: int = CHUNK_SIZE) -> list[str]:
    words = text.split()
    chunks, current = [], []
    for word in words:
        current.append(word)
        if len(" ".join(current)) >= size:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks


async def ingest_file(path: Path, source: str):
    text = path.read_text(encoding="utf-8", errors="ignore")
    chunks = chunk_text(text)
    points = []
    for chunk in chunks:
        vector = await embed_query(chunk)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk, "source": source, "file": path.name},
            )
        )
    await _client.upsert(collection_name=settings.qdrant_collection, points=points)
    print(f"Ingested {len(points)} chunks from {path.name}")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--source", default="document")
    args = parser.parse_args()
    await ensure_collection()
    p = Path(args.path)
    files = list(p.rglob("*")) if p.is_dir() else [p]
    for f in files:
        if f.suffix in [".md", ".txt", ".pdf"]:
            await ingest_file(f, args.source)


if __name__ == "__main__":
    asyncio.run(main())
