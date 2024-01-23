import os
from datetime import datetime

from aiogram import types

from API import put_post_last_view_changer
from urllib.parse import quote

from pictures_generator import picture_generator


def link_generator_ticket(link):
    # см файл информация о ссылках чтобы понять какие данные откуда берутся in link_with_referal
    link_aviasales = f"https://www.aviasales.ru{link}"
    link_aviasales_unicode = quote(link_aviasales, safe="%")  # в юникоде должна быть линка для реферальной ссылки
    link_with_referal = f"https://tp.media/r?marker=508478&trs=287693&p=4114&u={link_aviasales_unicode}&campaign_id=100 "
    return link_with_referal


def data_formatted(timestamp_str):
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


def weekday(timestamp_str):
    week_days = {
        'Monday': 'понедельник',
        'Tuesday': 'вторник',
        'Wednesday': 'среда',
        'Thursday': 'четверг',
        'Friday': 'пятница',
        'Saturday': 'суббота',
        'Sunday': 'воскресенье',
    }

    day = datetime.fromisoformat(timestamp_str[:-6])
    weekday = day.strftime("%A")
    return f"{week_days.get(str(weekday))}"


def get_transfers_info(transfer_str):
    if int(transfer_str) == 0:
        return "✅ Прямой рейс"
    else:
        return "⚠️ Рейс с пересадкой"


def price(price):
    if price is None:
        return None
    else:
        price = f"{int(price): ,}".replace(',', ' ') + " ₽"
        return price


def package_of_destinations(post_json):
    path_list = post_json['destinations']
    last_index = int(post_json['last_viewed_destination_index'])
    paths_per_batch = 1  # int(post_json['count_of_directions_in_post'])  ЗАХАРДКОДИЛ ВРЕМЕННО(ПОКА НЕ ПОТРЕБУЕТСЯ ВОЗМОЖНОСТЬ МЕНЯТЬ)

    if not path_list or paths_per_batch <= 0:
        return None, None

    total_paths = len(path_list)
    processed_indices = set()  # Множество для отслеживания уже обработанных индексов
    processed_paths = []

    for i in range(last_index + 1, last_index + 1 + min(paths_per_batch, total_paths)):
        current_index = i % total_paths

        # Проверяем, был ли уже обработан этот индекс
        if current_index in processed_indices:
            continue

        # Добавляем индекс в множество обработанных
        processed_indices.add(current_index)

        # Обработка значения
        current_path = path_list[current_index]
        processed_paths.append(current_path)

    last_index = str((last_index + min(paths_per_batch, total_paths)) % total_paths)
    put_post_last_view_changer(post_id=post_json['id'],
                               new_last_view=last_index)  # Обновляем индекс последнего опубликованного направления
    # Возвращаем последний обработанный индекс и значения из списка путей (как список)
    return processed_paths


def get_photo_path_by_host_ip(filename):
    LOCALHOST_IP = os.getenv('LOCALHOST_IP')

    if LOCALHOST_IP in ['127.0.0.1:8000', '0.0.0.0:8000']:
        path = f"/home/rauf/PycharmProjects/duna_trips/trip_admin/media/post_pictures/{filename}"
    else:
        path = f"/root/duna_trips/trip_admin/media/post_pictures/{filename}"  # Смотри размещение у себя на сервере
    return path


def get_destination_name(post):
    destinations = post['destinations']
    index = post['last_viewed_destination_index'] + 1

    if index >= len(destinations):
        index = index % len(destinations)

    return destinations[index]['destination_name']


async def send_picture(bot, post, chat_id):
    path_from_ai = picture_generator(get_destination_name(post=post))
    if path_from_ai:
        await bot.send_photo(chat_id=chat_id,
                             photo=path_from_ai)

    else:
        file_name = os.path.basename(post['picture'])
        if file_name:
            path_from_db = get_photo_path_by_host_ip(file_name)
            await bot.send_photo(chat_id=chat_id,
                                 photo=types.FSInputFile(path=path_from_db))
