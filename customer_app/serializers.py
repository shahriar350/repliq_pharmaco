from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import transaction, IntegrityError
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from admin_app.models import DeliveryCharge
from customer_app.models import Cart, CartProduct, Checkout, CheckoutProduct
from product_app.models import Product
from auth_app.models import UserAddress


class CartProductSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField(read_only=True)
    cart_product_id = serializers.IntegerField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all())
    quantity = serializers.IntegerField(validators=[MinValueValidator(1)])
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        customer = validated_data.get('customer', None)
        quantity = validated_data.get('quantity', None)
        product = validated_data.get('product', None)

        cart, created = Cart.objects.get_or_create(customer=customer, active=True, deleted_at__isnull=True)

        validated_data['cart_id'] = cart.id
        cart_product = CartProduct.objects.create(
            cart=cart, product=product, quantity=quantity
        )
        validated_data['cart_product_id'] = cart_product.id
        return validated_data


class CartDestroySerializer(serializers.Serializer):
    removed = serializers.BooleanField(default=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartProductModelSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = (
            'id',
            'cart',
            'product',
            'quantity',
        )


class CartModelSerialiser(serializers.ModelSerializer):
    get_cart_products = CartProductModelSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'customer',
            'slug',
            'get_cart_products',
        )


class CartProductUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity')
        instance.save()
        return validated_data


class AddressCRUDSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddress
        fields = [
            'uuid',
            'house',
            'user',
            'street',
            'post_office',
            'police_station',
            'district',
            'country',
            'state'
        ]


class CheckoutSerializer(serializers.Serializer):
    payment_choices = (
        (0, 'Cash On Delivery'),
    )
    slug = serializers.SlugField(read_only=True)
    cart = serializers.SlugField()
    address = serializers.SlugField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    payment = serializers.ChoiceField(choices=payment_choices)

    def validate(self, attrs):
        if not Cart.objects.filter(Q(customer=attrs.get('user')) & Q(slug=attrs.get('cart'))).exists():
            raise ValidationError({'cart': "Invalid cart"})
        if not UserAddress.objects.filter(Q(user=attrs.get('user')) & Q(slug=attrs.get('address'))).exists():
            raise ValidationError({'address': "Invalid address"})
        return attrs

    def create(self, validated_data):
        cart = Cart.objects.prefetch_related('get_cart_products__product').get(slug=validated_data.get('cart'))
        cart_products = cart.get_cart_products.all()
        with transaction.atomic():
            user_address = UserAddress.objects.get(slug=validated_data.get('address'))
            delivery_charge = DeliveryCharge.objects.filter(district=user_address.district)
            charge = 100
            if delivery_charge.exists():
                charge = delivery_charge.first().charge
            checkout = Checkout.objects.create(
                location_id=user_address.id,
                cart_id=cart.id,
                total_price=cart.total_price + charge,
                customer=validated_data.get('user'),
                payment_method=validated_data.get('payment'),
                delivery_charge=charge
            )
            validated_data['slug'] = checkout.slug
            for cart_product in cart_products:
                CheckoutProduct.objects.create(
                    checkout=checkout,
                    product=cart_product.product,
                    merchant=cart_product.product.merchant,
                    quantity=cart_product.quantity,
                    selling_price=cart_product.product.selling_price
                )
        return validated_data