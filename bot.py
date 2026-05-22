import logging
import os
import random
import uuid

from dotenv import load_dotenv
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

OUTCOMES = (
    ("орёл", "🦅 Орёл"),
    ("решка", "🪙 Решка"),
)


def flip_coin() -> tuple[str, str]:
    return random.choice(OUTCOMES)


def format_flip_message(outcome_key: str, outcome_text: str) -> str:
    return f"🎲 Подбросили монетку — {outcome_text}!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я подбрасываю монетку.\n\n"
        "В любом чате (даже без добавления меня): напишите "
        f"@{context.bot.username} и выберите результат.\n\n"
        "В личке: /flip"
    )


async def flip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key, text = flip_coin()
    await update.message.reply_text(format_flip_message(key, text))


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query
    if not query:
        return

    key, text = flip_coin()
    message = format_flip_message(key, text)

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Подбросить монетку",
            description=text,
            input_message_content=InputTextMessageContent(message),
        ),
    ]

    await query.answer(results, cache_time=0, is_personal=True)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("Задайте BOT_TOKEN в .env (см. .env.example)")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("flip", flip_command))
    app.add_handler(InlineQueryHandler(inline_query))

    logger.info("Бот запущен")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
