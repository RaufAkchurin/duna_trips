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
        code_value = city_data['code']
        name_value = city_data['cases']['su'].lower()
        country_code_value = city_data['country_code']

        # Проверка существования страны с таким кодом
        country, created = Country.objects.get_or_create(code=country_code_value)

        # Проверка существования города с таким кодом
        city, created = City.objects.get_or_create(code=code_value, defaults={'name': name_value, 'country': country})

        # Если город уже существует, обновляем его название и страну
        if not created:
            city.name = name_value
            city.country = country
            city.save()


if __name__ == "__main__":
    json_file_path = '/home/rauf/PycharmProjects1/Trip/trip_admin/cities.json'  # Замените на актуальный путь к файлу
    update_cities_from_json(json_file_path)