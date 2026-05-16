import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from bot.telegram_handler import build_app
from rag.qdrant_client import ensure_collection
from config import settings

ptb_app = build_app()
polling_task = None


async def run_polling():
    """Run polling in background, dropping any pending/old updates."""
    try:
        print("Starting Telegram polling...")
        await ptb_app.updater.start_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,   # ← skips accumulated old messages
        )
    except Exception as e:
        print(f"Polling error: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global polling_task

    try:
        await ensure_collection()
    except Exception as e:
        print(f"Warning: Failed to initialize Qdrant: {e}")

    # Correct PTB startup sequence: initialize → start → poll
    await ptb_app.initialize()
    await ptb_app.start()          # ← starts dispatcher queues; was missing

    if settings.webhook_url:
        # Production: use webhook
        await ptb_app.bot.set_webhook(
            f"{settings.webhook_url}/webhook",
            drop_pending_updates=True,
        )
    else:
        # Local development: polling as background task
        polling_task = asyncio.create_task(run_polling())

    yield

    # Correct PTB teardown sequence: stop polling → stop → shutdown
    if polling_task:
        await ptb_app.updater.stop()   # ← gracefully stops the updater first
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass

    await ptb_app.stop()           # ← drains dispatcher; was missing
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
