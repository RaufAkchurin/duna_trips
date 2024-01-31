import os
from pprint import pprint

import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

BASE_URL_AVIASALES = 'https://api.travelpayouts.com/aviasales/'


def get_special_offers(origin, destination):
    depart_date, return_date = calculate_travel_dates()
    url = (f"{BASE_URL_AVIASALES}v3/get_special_offers?"
           f"destination={destination}&origin={origin}"
           f"&depart_date={depart_date}&return_date={return_date}"
           f"&locale=ru&token={os.getenv('AVIASALES_TOKEN')}")
    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None


def get_current_month():  # if to the end this month < 15 dsys - return with next month
    current_date = datetime.now()
    days_until_end_of_month = (
            datetime(current_date.year, current_date.month % 12 + 1, 1) - timedelta(days=1) - current_date).days

    if days_until_end_of_month < 15:
        next_month = current_date.replace(day=1, month=current_date.month % 12 + 1,
                                          year=current_date.year + current_date.month // 12)
        formatted_month = next_month.strftime('%Y-%m')
    else:
        formatted_month = current_date.strftime('%Y-%m')

    return formatted_month


def get_grouped_prices_by_month(origin, destination):  # month in format 2023-12
    url = (f"{BASE_URL_AVIASALES}v3/grouped_prices?origin={origin}"
           f"&destination={destination}&currency=rub&departure_at={get_current_month()}"
           f"&group_by=departure_at&token={os.getenv('AVIASALES_TOKEN')}")

    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None


def get_cheapest_offers(origin, destination):
    depart_date, return_date = calculate_travel_dates()
    url = (f"{BASE_URL_AVIASALES}v3/prices_for_dates"
           f"?origin={origin}&destination={destination}"
           f"&departure_at={depart_date}&return_at={return_date}"
           f"&unique=false&sorting=price&direct=false"
           f"&cy=rub&limit=5&page=1&one_way=false"
           f"&token={os.getenv('AVIASALES_TOKEN')}")

    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None


def calculate_travel_dates():  # for get_cheap_offers and return date in format YYYY-MM
    current_date = datetime.now()
    days_left_in_month = (current_date.replace(day=1, month=current_date.month + 1) - current_date).days

    if days_left_in_month > 7:
        depart_date = return_date = current_date.strftime('%Y-%m')
    else:
        next_month = current_date.replace(day=1) + timedelta(days=32)
        depart_date = current_date.strftime('%Y-%m')
        return_date = next_month.strftime('%Y-%m')

    return depart_date, return_date


BASE_URL_ADMIN = 'http://' + os.getenv('LOCALHOST_IP') + '/api/v1'


def get_chanel_list():
    url = f"{BASE_URL_ADMIN}/chanels"
    response = requests.get(url=url)
    return response.json()


def get_post_list():
    url = f"{BASE_URL_ADMIN}/posts"
    response = requests.get(url=url)
    return response.json()


def put_post_last_view_changer(post_id, new_last_view):
    url = f"{BASE_URL_ADMIN}/post_last_view_changer/{post_id}"
    response = requests.put(url=url, data={"last_viewed_destination_index": new_last_view})
    if response.status_code == 200:
        return response.json()
    else:
        return None
