from django.http import JsonResponse
from django.templatetags.static import static
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    data = request.data
    print('!!!!! Заказ через DRF:', data)

    products = data.get('products', None)

    if products is None:
        return Response(
            {"products": "Обязательное поле."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not isinstance(products, list):
        return Response(
            {"products": "Ожидался list со значениями, но был получен другой тип."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(products) == 0:
        return Response(
            {"products": "Этот список не может быть пустым."},
            status=status.HTTP_400_BAD_REQUEST
        )

    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data.get('lastname', ''),
        phonenumber=data['phonenumber'],
        address=data['address']
    )

    for item in products:
        product = Product.objects.get(pk=item['product'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=product.price
        )

    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)