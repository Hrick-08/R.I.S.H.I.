from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from bot.session import get_session
from agent.openclaw_runner import run_agent
from config import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("R.I.S.H.I. online. What do you need?")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    session = get_session(user_id)
    session.add_message("user", text)
    response = await run_agent(session.messages)
    session.add_message("assistant", response)
    await update.message.reply_text(response)


def build_app():
    app = ApplicationBuilder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app
