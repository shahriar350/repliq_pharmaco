from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F

from autoslug import AutoSlugField

from addressio.models import Address
from catalogio.models import Product
from core.utils import PreModel
from orderio.choices import order_status_choices
from orderio.utils import get_customer_name

User = get_user_model()


# Create your models here.
class Cart(PreModel):
	customer = models.OneToOneField(User, related_name="cart", on_delete=models.CASCADE)
	slug = AutoSlugField(populate_from=get_customer_name, editable=False, unique=True)

	@property
	def total_price(self):
		return self.cart_products.all().aggregate(total=Sum(F('product__selling_price') * F('quantity')))['total']


class CartProduct(PreModel):
	cart = models.ForeignKey(Cart, related_name='cart_products', on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, related_name="product_carts", on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.product.base_product.name


class Order(PreModel):
	customer = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='orders')
	organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE, blank=True)
	total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
	address = models.ForeignKey(Address, on_delete=models.CASCADE)
	completed = models.BooleanField(default=False)
	delivery_charge = models.DecimalField(default=0, decimal_places=2, max_digits=10)
	payment_method = models.ForeignKey("core.PaymentMethod", on_delete=models.CASCADE)

	@property
	def user_name(self):
		return self.customer.name


class OrderProduct(PreModel):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='checkout_products')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	selling_price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(blank=True, validators=[MinValueValidator(1)])


class OrderDeliveryStatus(PreModel):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='checkout_statuses', blank=True)
	status = models.CharField(max_length=100, default='order placed', choices=order_status_choices)
