import requests
from django.conf import settings
from .models import Place
from django.utils.timezone import now
from requests.exceptions import RequestException
# from foodcartapp.utils import fetch_coordinates
import logging

logger = logging.getLogger(__name__)


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    try:
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        })
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return float(lat), float(lon)
    except RequestException:
        return None


def get_or_create_place_with_coords(address):
    # Пытаемся найти уже сохранённое место
    place = Place.objects.filter(address=address).first()
    if place and place.lat is not None and place.lon is not None:
        return place

    # Если объекта ещё нет или у него нет координат — получаем их
    coords = fetch_coordinates(settings.YANDEX_API_TOKEN, address)
    if coords is None:
        logger.warning(f'Координаты не найдены для адреса "{address}"')
        return place if place else None  # если объект уже есть, возвращаем его, иначе None

    lat, lon = coords

    if place:
        # обновляем координаты
        place.lat = lat
        place.lon = lon
        place.save()
    else:
        # создаём новый объект
        place = Place.objects.create(
            address=address,
            lat=lat,
            lon=lon
        )

    return place

