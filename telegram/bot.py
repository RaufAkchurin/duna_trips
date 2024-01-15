import logging
import random
import sys
import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import os
from dotenv import load_dotenv

from monthly_offers import send_monthly_offers

load_dotenv()

HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
"""

bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')
dp = Dispatcher()

scheduler = AsyncIOScheduler()  # Автоматическая отправка сообщений


async def scheduler_setup(scheduler):
    # Генерация двух случайных времен для отправки сообщений
    first_random_time = datetime.strptime("08:00:00", "%H:%M:%S") + timedelta(seconds=random.randint(0, 12 * 3600))  # До обеда
    second_random_time = datetime.strptime("12:00:00", "%H:%M:%S") + timedelta(seconds=random.randint(0, 8 * 3600))  # После обеда

    # Расписание для первого сообщения
    scheduler.add_job(send_monthly_offers, "cron", day_of_week="mon,wed,sat",
                      hour=first_random_time.hour, minute=first_random_time.minute, second=first_random_time.second, args=(bot,))

    # Расписание для второго сообщения
    scheduler.add_job(send_monthly_offers, "cron", day_of_week="mon,wed,sat",
                      hour=second_random_time.hour, minute=second_random_time.minute, second=second_random_time.second, args=(bot,))

    scheduler.start()


@dp.message(CommandStart())
async def start(message: Message):
    await bot.send_message(message.chat.id, text=
    f"Привет, бот запустился \n" \
    f"✈️ Желаем вам выгодных путешествий✈️ \n" \
    "Перезапустить бота - /start")


@dp.message(Command('month'))
async def handle_monthly_offers(message: types.Message):
    await send_monthly_offers(bot=bot)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # команды после включения не придут старые
    await scheduler_setup(scheduler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
