import os
from datetime import datetime
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot
from API import get_post_list, get_grouped_prices_by_month, create_log, get_post_details
from utils import data_formatted, price, link_generator_ticket, send_picture, weekday, \
    get_transfers_info, get_city_name, get_single_destination, get_package_of_destinations

load_dotenv()
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')


def sorting_tickets_by_price(tickets, post):
    # Здесь мы выдёргиваем все билеты на месяц, сортируем по цене и выдёргиваем нужное количество самых дешевых
    if tickets is not None:
        # Extract flight records from the data dictionary
        flights = list(tickets.values())
    else:
        return None

    # filer flights by maximum price of tickets
    flights = [x for x in flights if x['price'] <= post["max_price_of_tickets"]]

    # Sort flights by transfers and then by price
    sorted_flights = sorted(flights, key=lambda x: (x['transfers'], x['price']))

    # Keep the 5 cheapest options
    cheapest_flights = sorted_flights[:post['count_of_tickets_in_direction']]

    # Sort the 5 cheapest options by date
    sorted_cheapest_flights = sorted(cheapest_flights, key=lambda x: x['departure_at'])

    return sorted_cheapest_flights


def return_destinations_adding(destinations: list[dict]):
    new_destinations = []
    for ticket in destinations:
        new_destinations.append(ticket)

        reverse_destination = {
            'origin_code': ticket['destination_code'],
            'origin_name': ticket['destination_name'],
            'destination_code': ticket['origin_code'],
            'destination_name': ticket['origin_name']
        }

        new_destinations.append(reverse_destination)
    return new_destinations


def get_single_destination_with_return(post):
    destination = get_single_destination(post)
    if destination is not None:
        if bool(post['return_tickets']):
            destination = return_destinations_adding(destination)
        return destination
    else:
        return None


def get_tickets_cutted(destination, post):
    tickets_raw = get_grouped_prices_by_month(destination['origin_code'], destination['destination_code'])
    tickets_cutted = sorting_tickets_by_price(tickets_raw, post)
    return tickets_cutted, tickets_raw


def add_tickets_info_to_message(destination, message: str, tickets_cutted) -> str:
    message += f" \n <b>{get_city_name(destination['origin_name'])} - {get_city_name(destination['destination_name'])}</b> \n"

    for ticket in tickets_cutted:
        departure_time = datetime.fromisoformat(ticket['departure_at'][:-6])
        formatted_time = departure_time.strftime("%H:%M")

        message += (
            f"\n 🔥<b>{data_formatted(ticket['departure_at'])}</b> | {formatted_time} | {weekday(ticket['departure_at'])}"
            f"\n 💸 {price(ticket['price'])} с ручной кладью"
            f"\n {get_transfers_info(ticket['transfers'])}"
            f"\n • <a href='{link_generator_ticket(ticket['link'])}'>Купить билет</a>\n"
        )

    return message


def monthly_offers_message_processing(post_id, single_destination_with_return):
    post = get_post_details(post_id)
    message = ""
    if post['text_before']:
        message += f"✈️  {post['text_before']}  ✈️ \n"
    for destination in single_destination_with_return:
        tickets_cutted, tickets_raw = get_tickets_cutted(destination, post)

        if tickets_cutted:
            message = add_tickets_info_to_message(destination, message, tickets_cutted)
        else:
            title = "monthly_offers_message"
            body = f'''
                     \n Пост -  {post['id']}
                     \n Destanation -  {destination}
                     \n tickets_raw -  {tickets_raw}
                     \n Пост с билетами по данному направлению пропущен
                    '''
            create_log(title=title, body=body)
            return None

    message += "\n ⚠️ Цена и наличие билетов актуальны на момент публикации. \n"
    if post['text_after']:
        message += "—————————————————— \n"
        message += f"{post['text_after']}"

    return message


async def send_monthly_offers(bot: Bot):
    post_ids = [x["id"] for x in get_post_list()]
    try:
        for post_id in post_ids:
            post = get_post_details(post_id)
            if post is not None:
                destination = get_single_destination_with_return(post)
                if destination is not None:
                    message = monthly_offers_message_processing(post_id, destination)
                    if message and post.get('chanel').get('chanel_chat_id') == "-1002125473144":
                        await send_picture(bot, post_id, destination)

                        chat_id = post['chanel']["chanel_chat_id"]
                        await bot.send_message(chat_id=chat_id,
                                               text=message,
                                               parse_mode=ParseMode.HTML,
                                               disable_web_page_preview=True)

    except Exception as e:
        await bot.send_message(chat_id='5640395403',
                               text="ERROR TEXT for monthly_offers " + str(e),
                               parse_mode=ParseMode.MARKDOWN,
                               disable_web_page_preview=True,
                               protect_content=False)
