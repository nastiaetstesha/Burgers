from foodcartapp.models import RestaurantMenuItem
import requests
from django.conf import settings
from geopy.distance import distance as geopy_distance
from .models import RestaurantMenuItem, Restaurant
from collections import defaultdict
import logging
from places.utils import get_or_create_place_with_coords


logger = logging.getLogger(__name__)


def get_available_restaurants(order):
    order_products = order.items.values_list('product', flat=True)
    menu_items = RestaurantMenuItem.objects.filter(
        availability=True,
        product_id__in=order_products
    ).select_related('restaurant')

    restaurants_per_product = {}
    for item in menu_items:
        restaurants_per_product.setdefault(item.product_id, set()).add(item.restaurant)

    common_restaurants = None
    for restaurants in restaurants_per_product.values():
        if common_restaurants is None:
            common_restaurants = restaurants
        else:
            common_restaurants &= restaurants

    return common_restaurants or set()


# def fetch_coordinates(apikey, address):
#     base_url = "https://geocode-maps.yandex.ru/1.x"
#     response = requests.get(base_url, params={
#         "geocode": address,
#         "apikey": apikey,
#         "format": "json",
#     })
#     response.raise_for_status()
#     found_places = response.json()['response']['GeoObjectCollection']['featureMember']

#     if not found_places:
#         return None

#     most_relevant = found_places[0]
#     lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
#     return float(lat), float(lon)


def get_restaurants_with_distances(order):
    order_place = get_or_create_place_with_coords(order.address)
    if order_place.lat is None or order_place.lon is None:
        logger.warning(f'Координаты не найдены для адреса: {order.address}')
        return None, 'Ошибка при получении координат доставки'

    suitable_restaurants = get_available_restaurants(order)
    restaurant_with_distances = []

    for restaurant in suitable_restaurants:
        restaurant_place = get_or_create_place_with_coords(restaurant.address)
        if restaurant_place.lat is None or restaurant_place.lon is None:
            continue

        dist = round(
            geopy_distance(
                (order_place.lat, order_place.lon),
                (restaurant_place.lat, restaurant_place.lon)
            ).km,
            2
        )
        restaurant_with_distances.append((restaurant, dist))

    restaurant_with_distances.sort(key=lambda item: item[1])
    return restaurant_with_distances, None

# def get_restaurants_with_distances(order):
#     try:
#         order_coords = fetch_coordinates(
#             settings.YANDEX_API_TOKEN,
#             order.address
#         )
#     except requests.exceptions.RequestException:
#         logger.error(f'Ошибка при запросе координат для адреса "{order.address}"')
#         return None, 'Ошибка при запросе координат доставки'

#     if not order_coords:
#         logger.warning(f'Координаты не найдены для адреса: {order.address}')
#         return None, 'Координаты доставки не найдены'

#     suitable_restaurants = get_available_restaurants(order)

#     restaurant_with_distances = []
#     for restaurant in suitable_restaurants:
#         try:
#             coords = fetch_coordinates(
#                 settings.YANDEX_API_TOKEN, restaurant.address
#                 )
#         except requests.exceptions.RequestException:
#             continue
#         if not coords:
#             continue

#         dist = round(geopy_distance(order_coords, coords).km, 2)
#         restaurant_with_distances.append((restaurant, dist))

#     restaurant_with_distances.sort(key=lambda item: item[1])
#     return restaurant_with_distances, None
