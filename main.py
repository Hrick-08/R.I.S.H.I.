import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from bot.telegram_handler import build_app
from rag.qdrant_client import ensure_collection
from config import settings

ptb_app = build_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_collection()
    await ptb_app.initialize()
    if settings.webhook_url:
        await ptb_app.bot.set_webhook(f"{settings.webhook_url}/webhook")
    yield
    await ptb_app.shutdown()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, ptb_app.bot)
    await ptb_app.process_update(update)
    return {"ok": True}


@app.get("/health")
async def health():
    return {"status": "ok"}
