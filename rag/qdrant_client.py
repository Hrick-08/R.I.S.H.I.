from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, Query
from config import settings

_client = AsyncQdrantClient(url=settings.qdrant_url)


async def ensure_collection():
    collections = await _client.get_collections()
    names = [c.name for c in collections.collections]
    if settings.qdrant_collection not in names:
        await _client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )


async def search_qdrant(vector: list[float], top_k: int = 4):
    response = await _client.query_points(
        collection_name=settings.qdrant_collection,
        query=vector,
        limit=top_k,
        with_payload=True,
    )
    return response.points  # list of ScoredPoint, same as .search() returned