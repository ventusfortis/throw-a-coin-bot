import logging
import os
import random
import uuid

from dotenv import load_dotenv
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.error import TelegramError
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


async def log_bot_capabilities(application: Application) -> None:
    me = await application.bot.get_me()
    inline = bool(me.supports_inline_queries)
    logger.info("Бот @%s (id=%s), inline=%s", me.username, me.id, inline)
    if not inline:
        logger.error(
            "Inline выключен. В @BotFather: /setinline → выберите бота → "
            "укажите placeholder (например: монетка)"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    me = await context.bot.get_me()
    inline_hint = (
        f"Наберите @{me.username} в поле ввода любого чата и выберите вариант."
        if me.supports_inline_queries
        else "Inline пока выключен — включите /setinline в @BotFather."
    )
    await update.message.reply_text(
        "Привет! Я подбрасываю монетку.\n\n"
        f"{inline_hint}\n\n"
        "В личке: /flip"
    )


async def flip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key, text = flip_coin()
    await update.message.reply_text(format_flip_message(key, text))


def build_inline_results() -> list[InlineQueryResultArticle]:
    key, text = flip_coin()
    message = format_flip_message(key, text)
    return [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Подбросить монетку",
            description=text,
            input_message_content=InputTextMessageContent(message),
        ),
    ]


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query
    if not query:
        return

    user = query.from_user
    logger.info(
        "inline_query id=%s user=%s query=%r",
        query.id,
        user.id if user else "?",
        query.query,
    )

    try:
        await query.answer(build_inline_results(), cache_time=0)
    except TelegramError:
        logger.exception("Не удалось ответить на inline_query id=%s", query.id)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("Задайте BOT_TOKEN в .env (см. .env.example)")

    app = (
        Application.builder()
        .token(token)
        .post_init(log_bot_capabilities)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("flip", flip_command))
    app.add_handler(InlineQueryHandler(inline_query))

    logger.info("Бот запущен (polling)")
    app.run_polling(
        allowed_updates=[
            Update.MESSAGE,
            Update.INLINE_QUERY,
            Update.CHOSEN_INLINE_RESULT,
        ],
    )


if __name__ == "__main__":
    main()
