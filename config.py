from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str = ""
    github_token: str = ""
    github_models_base_url: str = "https://models.inference.ai.azure.com"
    llm_backend: str = "github"
    llm_model: str = "gpt-4o-mini"
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    nim_api_key: str = ""
    nim_base_url: str = "https://integrate.api.nvidia.com/v1"
    nim_model: str = "meta/llama-3.1-70b-instruct"
    zen_api_key: str = ""
    zen_base_url: str = ""
    zen_model: str = ""
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "rishi_knowledge"
    webhook_url: str = ""
    openclaw_token: str = ""
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
