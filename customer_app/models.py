import uuid

from dirtyfields import DirtyFieldsMixin
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F

from auth_app.models import UserAddress
from pharmaco_backend.utils import PreModel
from product_app.models import Product
from autoslug import AutoSlugField

User = get_user_model()


# Create your models here.
class Cart(DirtyFieldsMixin, PreModel):
    customer = models.ForeignKey(User, related_name="get_customer_carts", on_delete=models.CASCADE)
    slug = AutoSlugField(unique_with='customer__name', editable=False, unique=True)
    completed = models.BooleanField(default=False)

    @property
    def get_customer_name(self):
        return self.customer.name

    @property
    def total_price(self):
        return self.get_cart_products.all().aggregate(total=Sum(F('product__selling_price') * F('quantity')))['total']


class CartProduct(DirtyFieldsMixin, PreModel):
    cart = models.ForeignKey(Cart, related_name='get_cart_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="get_product_carts", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    merchant = models.ForeignKey(User, related_name='get_merchant_carts', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.product.base_product.name


class Checkout(DirtyFieldsMixin, PreModel):
    payment_choices = (
        (0, 'Cash On Delivery'),
    )
    slug = AutoSlugField(populate_from='user_name', unique_with='customer__name', editable=False, unique=True)
    customer = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='user_checkouts')
    cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, related_name='cart_checkout')
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    location = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name="user_address_checkouts")
    completed = models.BooleanField(default=False)
    delivery_charge = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    payment_method = models.SmallIntegerField(choices=payment_choices)

    @property
    def user_name(self):
        return self.customer.name


class CheckoutProduct(DirtyFieldsMixin, PreModel):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='get_checkout_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='get_product_checkouts')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(blank=True, validators=[MinValueValidator(1)])
    merchant = models.ForeignKey(User, related_name='get_merchant_checkoutproducts', on_delete=models.CASCADE,
                                 blank=True)


class CheckoutDeliveryStatus(DirtyFieldsMixin, PreModel):
    status_choices = (
        (0, 'Order placed'),
        (1, 'Processing'),
        (2, 'Packaging'),
        (3, 'On-way'),
        (4, 'Reached'),
        (5, 'Completed'),
    )
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='get_checkout_delivery_status',
                                 blank=True)
    checkout_product = models.ForeignKey(CheckoutProduct, on_delete=models.CASCADE,
                                         related_name='get_checkout_product_delivery_status')
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                                 related_name='get_merchant_delivery_status')
    status = models.PositiveSmallIntegerField(default=0, choices=status_choices)
