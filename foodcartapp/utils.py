from foodcartapp.models import RestaurantMenuItem


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
