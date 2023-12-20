import os
import django
import json

# Устанавливаем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trip_admin.settings")  # Замените "trip_admin" на имя вашего Django-проекта
django.setup()

from trip_admin_app.models import City, Country  # Замените 'trip_admin_app' на имя вашего Django-приложения


def update_cities_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for city_data in data:
        country_code = city_data['country_code']

        # Проверка существования города с таким кодом
        Country.objects.get_or_create(code=country_code)


if __name__ == "__main__":
    json_file_path = '/home/rauf/PycharmProjects1/Trip/trip_admin/cities.json'  # Замените на актуальный путь к файлу
    update_cities_from_json(json_file_path)
