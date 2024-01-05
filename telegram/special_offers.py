import os
from datetime import datetime
from aiogram import Bot, types
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from API import get_special_offers, get_post_list, put_post_last_view_changer

load_dotenv()
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')


def link_generator_ticket(link):
    # см файл информация о ссылках чтобы понять какие данные откуда берутся in link_with_referal

    link_aviasales = f"https://aviasales.ru{link}"
    link_with_referal = f"https://tp.media/r?marker=508478&trs=287693&p=4114&u={link_aviasales}&campaign_id=100 "
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


def price(price):
    if price is None:
        return None
    else:
        price = f"{int(price): ,}".replace(',', ' ') + " ₽"
        return price


def package_of_destinations(post_json):
    path_list = post_json['destinations']
    last_index = int(post_json['last_viewed_destination_index'])
    paths_per_batch = int(post_json['count_of_directions_in_post'])

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


def special_offers_message(post):
    message = f"✈️  {post['text']}  ✈️ \n \n"
    destinations = package_of_destinations(post)
    for destination in destinations:
        tickets = get_special_offers(destination['origin_code'], destination['destination_code'])
        if tickets:
            for ticket in tickets:
                departure_time = datetime.fromisoformat(ticket['departure_at'][:-6])
                formatted_time = departure_time.strftime("%H:%M")

                message += (
                    f"\n 🔥<b>{data_formatted(ticket['departure_at'])}</b> | {formatted_time} | {weekday(ticket['departure_at'])}"
                    f"\n <i>{ticket['origin_name']}({ticket['origin']}) - {ticket['destination_name']}({ticket['destination']})</i>"
                    f"\n 💸 {price(ticket['price'])}"
                    f"\n <a href='{link_generator_ticket(ticket['link'])}'>Купить билет</a>\n\n"
                )
        else:
            pass

    message += "\n ⚠️ Цена и наличие билетов актуальны на момент публикации."
    return message


async def get_photo_path_by_host_ip(filename):
    LOCALHOST_IP = os.getenv('LOCALHOST_IP')

    if LOCALHOST_IP in ['127.0.0.1:8000', '0.0.0.0:8000']:
        path = f"/home/rauf/PycharmProjects/duna_trips/trip_admin/media/post_pictures/{filename}"
    else:
        path = f"/root/duna_trips/trip_admin/media/post_pictures/{filename}"      # Смотри размещение у себя на сервере
    return path


async def send_special_offers(bot: Bot):
    posts = get_post_list()
    try:
        for post in posts:
            chat_id = post['chanel']["chanel_chat_id"]
            file_name = os.path.basename(post['picture'])
            if file_name:
                picture_path = await get_photo_path_by_host_ip(file_name)
            message = special_offers_message(post)
            if message:
                await bot.send_photo(chat_id=chat_id,
                                     photo=types.FSInputFile(path=picture_path))

                await bot.send_message(chat_id=chat_id,
                                     text=message,
                                     parse_mode=ParseMode.HTML)

    except Exception as e:
        await bot.send_message(chat_id='5640395403',
                               text="ERROR TEXT for special_offers - " + str(e),
                               parse_mode=ParseMode.MARKDOWN,
                               disable_web_page_preview=True,
                               protect_content=False)
