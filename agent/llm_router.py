from openai import AsyncOpenAI
from config import settings


def get_llm() -> tuple[AsyncOpenAI, str]:
    backend = settings.llm_backend.lower()
    if backend == "groq":
        client = AsyncOpenAI(
            api_key=settings.groq_api_key, base_url="https://api.groq.com/openai/v1"
        )
        return client, settings.groq_model
    if backend == "nim":
        client = AsyncOpenAI(
            api_key=settings.nim_api_key, base_url=settings.nim_base_url
        )
        return client, settings.nim_model
    if backend == "zen":
        client = AsyncOpenAI(
            api_key=settings.zen_api_key, base_url=settings.zen_base_url
        )
        return client, settings.zen_model
    if backend == "openclaw":
        client = AsyncOpenAI(
            api_key=settings.openclaw_token,
            base_url="http://127.0.0.1:18789/v1",
        )
        return client, "openclaw"               # routes to your "main" agent
    client = AsyncOpenAI(
        api_key=settings.github_token, base_url=settings.github_models_base_url
    )
    return client, settings.llm_model