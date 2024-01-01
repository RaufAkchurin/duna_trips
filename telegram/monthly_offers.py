import os
from datetime import datetime

from aiogram import Bot, types
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from API import get_post_list, get_grouped_prices_by_month
from special_offers import package_of_destinations, data_formatted, link_generator, price, weekday

load_dotenv()
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')


def monthly_offers_message(post):
    message = f"✈️  {post['text']}  ✈️ \n \n"
    destinations = package_of_destinations(post)
    for destination in destinations:
        message += f" <b>\n{destination['origin_name'].upper()} - {destination['destination_name'].upper()}</b> \n\n"
        tickets_raw = get_grouped_prices_by_month(destination['origin_code'], destination['destination_code'])
        tickets_cutted = dict(list(tickets_raw.items())[:5])
        if tickets_cutted:
            for ticket in tickets_cutted.values():
                departure_time = datetime.fromisoformat(ticket['departure_at'][:-6])
                formatted_time = departure_time.strftime("%H:%M")

                message += (
                    f"\n 🔥<b>{data_formatted(ticket['departure_at'])}</b> | {formatted_time} | {weekday(ticket['departure_at'])}"
                    f"\n <i>{destination['origin_name'].capitalize()} ({ticket['origin']}) - {destination['destination_name'].capitalize()} ({ticket['destination']})</i>"
                    f"\n 💸 {price(ticket['price'])}"
                    f"\n <a href='{link_generator(ticket['link'])}'>Купить билет</a>\n\n"
                )
        else:
            pass

    message += "\n ⚠️ Цена и наличие билетов актуальны на момент публикации."
    return message


async def monthly_offers(bot: Bot):
    posts = get_post_list()
    try:
        for post in posts:
            chat_id = post['chanel']["chanel_chat_id"]
            message = monthly_offers_message(post)
            if message:
                await bot.send_message(chat_id=chat_id,
                                       text=message,
                                       disable_web_page_preview=True,
                                       parse_mode=ParseMode.HTML)

    except Exception as e:
        await bot.send_message(chat_id='5640395403',
                               text="ERROR TEXT - " + str(e),
                               parse_mode=ParseMode.MARKDOWN,
                               disable_web_page_preview=True,
                               protect_content=False)
