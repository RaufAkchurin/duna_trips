import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://api.travelpayouts.com/aviasales/'


def get_special_offers():
    url = f"{BASE_URL}v3/get_special_offers?origin=KZN&locale=ru&token={os.getenv('AVIASALES_TOKEN')}"
    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return None
