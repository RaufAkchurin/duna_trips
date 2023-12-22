import os
from datetime import datetime

from aiogram import Bot
from dotenv import load_dotenv

from telegram.API import get_special_offers, get_chanel_list, get_post_list

load_dotenv()
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')


def link_generator(link):
    marker = "508478"  # айди профиля Travelpayouts чтобы учитывался проценто с каждой продажи
    res = f"https://aviasales.ru{link}"
    res += f"&marker={marker}"
    return res


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


def special_offers_message(origin, destination):
    trips = get_special_offers(origin, destination)
    message = "✈️Спецальные предложения с вылетом из Казани✈️ \n \n"  # из казаНИ прям с ендпоинта вытаскивать авиасейлс
    if trips:
        for trip in trips:
            message += (f"🔥{data_formatted(trip['departure_at'])} "
                        f"из {trip['origin_name_declined']} {trip['destination_name_declined']} "
                        f"за {trip['price']} р [ссылка]({link_generator(trip['link'])}) \n")
        message += "\n ⚠️ Цена и наличие билетов актуальны на момент публикации."
        return message
    else:
        return None


def get_destination_index_by_id(destinations: list, target_id):
    for index, destination in enumerate(destinations):
        if destination["id"] == target_id:
            return index
    return None  # Return None if the id is not found


def get_actual_destination(post):
    destinations = post['destinations']

    try:
        if post["last_viewed_destination_id"] == 0:
            actual_destination = destinations[0]

        else:
            last_index = get_destination_index_by_id(
                destinations=destinations,
                target_id=post["last_viewed_destination_id"]
            )
            if len(destinations) > last_index:
                actual_destination = destinations[last_index + 1]
            else:
                actual_destination = destinations[0]
    except:
        actual_destination = destinations[0]

    return actual_destination


async def special_offers(bot: Bot):
    posts = get_post_list()
    # message_text = special_offers_message()

    for post in posts:
        chat_id = post['chanel']["chanel_chat_id"]
        for _ in range(5):
            destination = get_actual_destination(post=post)
            text = special_offers_message(destination["origin_code"], destination["destination_code"])
            print(text)

    # await bot.send_message(chat_id=chanel["chanel_chat_id"], text=message_text, parse_mode=ParseMode.MARKDOWN,
    #                        disable_web_page_preview=True, protect_content=False)
    # else:
    #     for chanel in chanels:
    #         await bot.send_message(chat_id=chanel["chanel_chat_id"], text=f'Специальные предложения отсутствуют на данный момент')
