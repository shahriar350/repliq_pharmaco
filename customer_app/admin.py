from django.contrib import admin
from .models import Cart, CartProduct, Checkout, CheckoutProduct, CheckoutDeliveryStatus


# Register your models here.

class CartProductAdminInline(admin.StackedInline):
    model = CartProduct
    fk_name = "cart"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = (
        'uuid',
        'customer',
        'completed',
        'total_price',
        'updated_at',
    )

    list_filter = (
        'active',
        'completed',
        ('deleted_at', admin.EmptyFieldListFilter)
    )
    inlines = (CartProductAdminInline,)


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    model = CartProduct
    list_display = (
        'uuid',
        'cart',
        'product',
        'merchant',
        'quantity',
        'updated_at',
    )

    list_filter = (
        'product',
        'merchant',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    model = Checkout
    list_display = (
        'uuid',
        'cart',
        'customer',
        'total_price',
        'completed',
        'payment_method',
    )

    list_filter = (
        'customer',
        'cart',
        'location',
        'completed',
        'payment_method',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(CheckoutProduct)
class CheckoutProductAdmin(admin.ModelAdmin):
    model = CheckoutProduct
    list_display = (
        'uuid',
        'checkout',
        'product',
        'selling_price',
        'quantity',
    )

    list_filter = (
        'merchant',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(CheckoutDeliveryStatus)
class CheckoutDeliveryStatusAdmin(admin.ModelAdmin):
    model = CheckoutDeliveryStatus
    list_display = (
        'uuid',
        'checkout',
        'status',
    )

    list_filter = (
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )
