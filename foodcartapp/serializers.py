from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Order, OrderItem, Product


class OrderItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False)
    phonenumber = PhoneNumberField()

    class Meta:
        model = Order
        fields = [
            'firstname', 'lastname', 'phonenumber', 'address', 'products'
            ]

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)

        for item in products_data:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
        return order
