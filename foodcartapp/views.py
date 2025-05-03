from django.http import JsonResponse
from django.templatetags.static import static
import json
from django.views.decorators.csrf import csrf_exempt


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


@csrf_exempt
def register_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Только POST'}, status=405)

    data = json.loads(request.body)
    print('👉 Получен заказ:', data)

    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data.get('lastname', ''),
        phonenumber=data['phonenumber'],
        address=data['address']
    )

    for item in data['products']:
        product = Product.objects.get(pk=item['product'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=product.price
        )

    return JsonResponse({'status': 'ok'})
