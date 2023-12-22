import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL_AVIASALES = 'https://api.travelpayouts.com/aviasales/'


def get_special_offers(origin, destination):
    url = (f"{BASE_URL_AVIASALES}v3/get_special_offers?destination={destination}&origin={origin}"
           f"&locale=ru&token={os.getenv('AVIASALES_TOKEN')}")
    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None


# Admin panel django
load_dotenv()
BASE_URL_ADMIN = 'http://' + os.getenv('LOCALHOST_IP') + '/api/v1'


def get_chanel_list():
    url = f"{BASE_URL_ADMIN}/chanels"
    response = requests.get(url=url)
    return response.json()


def get_post_list():
    url = f"{BASE_URL_ADMIN}/posts"
    response = requests.get(url=url)
    return response.json()
