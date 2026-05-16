from openai import AsyncOpenAI
from config import settings

_client = AsyncOpenAI(
    api_key=settings.github_token, base_url=settings.github_models_base_url
)


async def embed_query(text: str) -> list[float]:
    response = await _client.embeddings.create(
        model="text-embedding-3-small", input=text
    )
    return response.data[0].embedding
