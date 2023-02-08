from django.core.validators import MinValueValidator
from rest_framework import serializers

from addressio.models import Address
from catalogio.models import DeliveryCharge
from core.models import PaymentMethod
from orderio.models import Order, OrderProduct, OrderDeliveryStatus


class PublicProductSerializer(serializers.Serializer):
	slug = serializers.SlugField(read_only=True)
	name = serializers.Serializer(label='Product name', read_only=True)
	selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, read_only=True)


class PublicOrderSerializers(serializers.Serializer):
	product = PublicProductSerializer(read_only=True)
	quantity = serializers.IntegerField(validators=[MinValueValidator(1)])


class PublicOrderSerializer(serializers.Serializer):
	total_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, read_only=True)
	orders = PublicOrderSerializers(many=True, read_only=True)
	customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
	address = serializers.SlugRelatedField(queryset=Address.objects.filter(active=True, deleted_at__isnull=True),
										   slug_field='slug')
	payment_method = serializers.SlugRelatedField(
		queryset=PaymentMethod.objects.filter(active=True, deleted_at__isnull=True), slug_field='slug')

	def create(self, validated_data):
		customer = validated_data.get('customer')
		cart = customer.cart
		cartproducts = customer.cart.cart_products.all()

		delivery_charge_set = 100
		organization = cartproducts[0].product.organization
		delivery_charge = DeliveryCharge.objects.filter(
			district=validated_data.get('address').district
		)
		if delivery_charge.exists():
			delivery_charge_set = delivery_charge.first().charge

		order = Order.objects.create(
			customer=validated_data.get('customer'),
			total_price=cart.total_price + delivery_charge_set,
			address=validated_data.get('address'),
			payment_method=validated_data.get('payment_method'),
			delivery_charge=delivery_charge_set,
			organization=organization
		)
		for cartproduct in cartproducts:
			orderprod = OrderProduct.objects.create(
				order=order,
				product=cartproduct.product,
				selling_price=cartproduct.product.selling_price,
				quantity=cartproduct.quantity
			)
		OrderDeliveryStatus.objects.create(
			order=order,
		)
		customer.cart.delete()

		return validated_data
