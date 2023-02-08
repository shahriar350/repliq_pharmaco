from django.contrib import admin
from .models import Product, BaseProduct, ProductImage


# Register your models here.

class BaseProductImageInline(admin.StackedInline):
    model = ProductImage
    fk_name = "base_product"


@admin.register(BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    model = BaseProduct
    list_display = (
        'uuid',
        'name'
    )
    list_filter = (
        'category',
        'active_ingredient',
        'manufacturer',
        'brand',
        'route_of_administration',
        'medicine_physical_state',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )
    inlines = (BaseProductImageInline,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        'uuid',
        'base_product',
        'stock'
    )
    list_filter = (
        'base_product',
        'merchant',
        'stock',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )
