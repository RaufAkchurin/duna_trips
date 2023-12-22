import os
from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from telegram.API import get_special_offers, get_post_list

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


def package_of_destinations(post_json):
    lst = post_json['destinations']
    count_of_directions_in_post = int(post_json['count_of_directions_in_post'])
    index = post_json['last_viewed_destination_index']

    if not lst:
        print("Список пуст.")
        return

    list_length = len(lst)
    iterations = 0  # Для отслеживания количества итераций

    while iterations < list_length:
        # Выбираем следующие 5 элементов из списка
        package_of_destinations = lst[index:index + count_of_directions_in_post]

        # Увеличиваем индекс и обрабатываем круговой переход
        index = (index + 5) % list_length

        # Увеличиваем количество итераций
        iterations += 1

    return package_of_destinations


async def special_offers(bot: Bot):
    posts = get_post_list()

    for post in posts:
        chat_id = post['chanel']["chanel_chat_id"]
        destinations = package_of_destinations(post)

        for destination in destinations:
            message = special_offers_message(destination['origin_code'], destination['destination_code'])
            if message:
                await bot.send_message(chat_id=chat_id,
                                       text=message,
                                       parse_mode=ParseMode.MARKDOWN,
                                       disable_web_page_preview=True,
                                       protect_content=False)
