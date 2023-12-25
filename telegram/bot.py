import logging
import sys
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import os
from dotenv import load_dotenv

from telegram import bot_kb
from telegram.monthly_offers import monthly_offers
from telegram.special_offers import special_offers


load_dotenv()

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')
dp = Dispatcher()

# Автоматическая отправка сообщений
scheduler = AsyncIOScheduler()


async def scheduler_setup(scheduler):
    # scheduler.add_job(special_offers, "cron", second="*/30", args=(bot,))
    scheduler.start()


@dp.message(CommandStart())
async def start(message: Message):
    await bot.send_message(message.chat.id, text=
    f"Привет, бот запустился \n" \
    f"✈️ Желаем вам выгодных путешествий✈️ \n" \
    "Перезапустить бота - /start"
    , reply_markup=bot_kb.main_kb)


dp.message.register(special_offers, F.text == 'Свежие билеты')


@dp.message(Command('special_offers'))
async def handle_special_offers(message: types.Message):
    await special_offers(bot=bot)


@dp.message(Command('monthly_offers'))
async def handle_monthly_offers(message: types.Message):
    await monthly_offers(bot=bot)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # команды после включения не придут старые
    await scheduler_setup(scheduler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
