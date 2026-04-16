import logging
import os
import sys

import telebot

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    # Local run: repository layout has `bot/services/...`
    from bot.services.user_service import get_users_count, save_or_update_user
except ModuleNotFoundError:
    # Dockerfile copies `bot/` contents into container root: `/app/services/...`
    from services.user_service import get_users_count, save_or_update_user
from shared.config import BOT_TOKEN
from shared.db import init_db, wait_for_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is empty. Set it in .env (BOT_TOKEN=...)")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    try:
        save_or_update_user(message.from_user)
        bot.reply_to(message, "Привет! Я сохранил ваши данные. Команда: /users_count")
    except Exception as e:
        logger.exception("Failed to save user: %s", e)
        bot.reply_to(message, "Ошибка при работе с базой данных. Попробуйте позже.")


@bot.message_handler(commands=["users_count"])
def handle_users_count(message):
    try:
        count = get_users_count()
        bot.reply_to(message, f"Всего пользователей в базе: {count}")
    except Exception as e:
        logger.exception("Failed to get users count: %s", e)
        bot.reply_to(message, "Не удалось получить количество пользователей.")


if __name__ == "__main__":
    logger.info("Waiting for database...")
    wait_for_db()
    init_db()
    logger.info("Starting Telegram bot polling...")
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
