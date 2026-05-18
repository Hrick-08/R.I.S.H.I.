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


async def ingest_uploads_folder():
    """Ingest all files from the uploads folder into Qdrant."""
    uploads_path = Path("uploads")
    
    if not uploads_path.exists():
        print(f"Uploads folder not found at {uploads_path}")
        return
    
    await ensure_collection()
    
    # Find all supported file types
    supported_extensions = {".md", ".txt", ".pdf"}
    files = [f for f in uploads_path.rglob("*") if f.suffix in supported_extensions]
    
    if not files:
        print(f"No supported files found in {uploads_path}")
        return
    
    print(f"Found {len(files)} files to ingest from uploads folder")
    
    for f in files:
        try:
            await ingest_file(f, source="uploads")
        except Exception as e:
            print(f"Error ingesting {f.name}: {e}")
    
    print(f"Completed ingesting {len(files)} files from uploads folder")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("--source", default="document")
    parser.add_argument("--uploads", action="store_true", help="Ingest all files from uploads folder")
    args = parser.parse_args()
    
    await ensure_collection()
    
    if args.uploads:
        await ingest_uploads_folder()
    elif args.path:
        p = Path(args.path)
        files = list(p.rglob("*")) if p.is_dir() else [p]
        for f in files:
            if f.suffix in [".md", ".txt", ".pdf"]:
                try:
                    await ingest_file(f, args.source)
                except Exception as e:
                    print(f"Error ingesting {f.name}: {e}")
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
