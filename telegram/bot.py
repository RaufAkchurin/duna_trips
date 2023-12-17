import logging
import sys
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import os
from dotenv import load_dotenv

from telegram import bot_kb
from telegram.special_offers import special_offers

load_dotenv()

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await bot.send_message(GROUP_CHAT_ID, text=
                        f"Привет, бот запустился \n" \
                        f"✈️ Желаем вам выгодных путешествий✈️ \n" \
                         "Перезапустить бота - /start"
                         , reply_markup=bot_kb.main_kb)

dp.message.register(special_offers, F.text == 'Свежие билеты')


async def main() -> None:
    await bot.delete_webhook(
        drop_pending_updates=True)  # все команды при выключенном боте после включении его не будут обрабатываться
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
