from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import Message

from telegram.API import get_special_offers


def data_formatted(timestamp_str):
    timestamp_str = timestamp_str

    months = {
        '1': 'января',
        '2': 'февраля',
        '3': 'марта',
        '4': 'апреля',
        '5': 'мая',
        '6': 'июня',
        '7': 'июля',
        '8': 'августа',
        '9': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря',
    }
    timestamp = datetime.fromisoformat(timestamp_str)

    day = timestamp.day
    month = timestamp.month
    return f"{day} {months.get(str(month))}"


def special_offers_message():
    trips = get_special_offers()
    message = "✈️Спецальные предложения с вылетом из Казани✈️ \n \n"
    if trips:
        for trip in trips:
            message += (f"🔥{data_formatted(trip['departure_at'])} {trip['destination_name_declined']} за {trip['price']} [ссылка](https://aviasales.ru{trip['link']}) \n")
        message += "\n ⚠️ Цена и наличие билетов актуальны на момент публикации."
        return message
    else:
        return None


async def special_offers(message: Message, bot: Bot):
    message_text = special_offers_message()
    if message_text:
        await bot.send_message(message.chat.id, text=message_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    else:
        await bot.send_message(message.from_user.id, text=f'Специальные предложения отсутствуют на данный момент')
