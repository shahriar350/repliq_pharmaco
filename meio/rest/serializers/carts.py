from django.core.validators import MinValueValidator
from django.db.models import Q
from rest_framework import serializers

from catalogio.models import Product
from orderio.models import Cart, CartProduct


class PrivateAddToCart(serializers.Serializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all(), slug_field='slug')
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)])
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)

    def create(self, validated_data):
        customer = validated_data.get('customer', None)
        quantity = validated_data.get('quantity', None)
        product = validated_data.get('product', None)

        cart, _ = Cart.objects.get_or_create(customer=customer)
        CartProduct.objects.update_or_create(
            cart=cart, product=product, defaults={'quantity': quantity}
        )
        return validated_data


class CartProductDetailSerializer(serializers.Serializer):
    slug = serializers.SlugField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    selling_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0, read_only=True)


class CartProductSerializers(serializers.Serializer):
    slug = serializers.SlugField(read_only=True)
    product = CartProductDetailSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=0, read_only=True)


class PrivateCarts(serializers.Serializer):
    slug = serializers.SlugField(read_only=True)
    cart_products = CartProductSerializers(many=True, read_only=True)
