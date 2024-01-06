import os
from datetime import datetime
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot, types
from API import get_post_list, get_grouped_prices_by_month
from special_offers import package_of_destinations, data_formatted, link_generator_ticket, price, weekday, \
    get_photo_path_by_host_ip

load_dotenv()
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')


def sorting_tickets_by_price(tickets, count_of_tickets_in_direction):
    # Здесь мы выдёргиваем все билеты на месяц, сортируем по цене и выдёргиваем 5 самых дешевых

    # Extract flight records from the data dictionary
    flights = list(tickets.values())

    # Sort flights by price
    sorted_flights = sorted(flights, key=lambda x: x['price'])

    # Keep the 5 cheapest options
    cheapest_flights = sorted_flights[:count_of_tickets_in_direction]

    # Sort the 5 cheapest options by date
    sorted_cheapest_flights = sorted(cheapest_flights, key=lambda x: x['departure_at'])

    return sorted_cheapest_flights


def return_tickets_adding(destinations: list[dict]):
    new_tickets = []
    for ticket in destinations:
        new_tickets.append(ticket)

        # Создаем билет в обратном направлении
        reverse_ticket = {
            'origin_code': ticket['destination_code'],
            'origin_name': ticket['destination_name'],
            'destination_code': ticket['origin_code'],
            'destination_name': ticket['origin_name']
        }

        new_tickets.append(reverse_ticket)
    return new_tickets


def monthly_offers_message(post):
    message = ""
    if post['text_before']:
        message += f"✈️  {post['text_before']}  ✈️ \n"
    destinations = package_of_destinations(post)
    if bool(post['return_tickets']):
        destinations = return_tickets_adding(destinations)

    for destination in destinations:
        message += f" \n <b>{destination['origin_name'].capitalize()} - {destination['destination_name'].capitalize()}</b> \n"
        tickets_raw = get_grouped_prices_by_month(destination['origin_code'], destination['destination_code'])
        tickets_cutted = sorting_tickets_by_price(tickets_raw, post['count_of_tickets_in_direction'])

        if tickets_cutted:
            for ticket in tickets_cutted:
                departure_time = datetime.fromisoformat(ticket['departure_at'][:-6])
                formatted_time = departure_time.strftime("%H:%M")

                message += (
                    f"\n 🔥<b>{data_formatted(ticket['departure_at'])}</b> | {formatted_time} | {weekday(ticket['departure_at'])}"
                    f"\n 💸 {price(ticket['price'])}"
                    f"\n • <a href='{link_generator_ticket(ticket['link'])}'>Купить билет</a>\n"
                )
        else:
            message += "\n Билетов к сожалению нет в наличии =( \n"

    message += "\n ⚠️ Цена и наличие билетов актуальны на момент публикации. \n"
    if post['text_after']:
        message += "—————————————————— \n"
        message += f"{post['text_after']}"
    return message


async def send_monthly_offers(bot: Bot):
    posts = get_post_list()
    try:
        for post in posts:
            chat_id = post['chanel']["chanel_chat_id"]
            file_name = os.path.basename(post['picture'])
            if file_name:
                picture_path = await get_photo_path_by_host_ip(file_name)
            message = monthly_offers_message(post)
            if message:
                await bot.send_photo(chat_id=chat_id,
                                     photo=types.FSInputFile(path=picture_path))

                await bot.send_message(chat_id=chat_id,
                                       text=message,
                                       parse_mode=ParseMode.HTML,
                                       disable_web_page_preview=True)

    except Exception as e:
        await bot.send_message(chat_id='5640395403',
                               text="ERROR TEXT for monthly_offers - " + str(e),
                               parse_mode=ParseMode.MARKDOWN,
                               disable_web_page_preview=True,
                               protect_content=False)
