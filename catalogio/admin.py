from django.contrib import admin
from .models import Category, Brand, Supplier, Ingredient, Manufacturer, MedicinePhysicalState, RouteOfAdministration, \
    District, DeliveryCharge, BaseProduct, ProductImage, Product


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        'uid',
        'name',
        'parent',
        'updated_at',
    )

    list_filter = (
        'name',
        'parent',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = (
        'uid',
        'name',
        'updated_at',
    )

    list_filter = (
        'name',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = (
        'uid',
        'name',
        'updated_at',
    )

    list_filter = (
        'name',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    list_display = (
        'uid',
        'name',
        'updated_at',
    )

    list_filter = (
        'name',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
    list_display = (
        'uid',
        'name',
        'updated_at',
    )

    list_filter = (
        'name',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(MedicinePhysicalState)
class MedicinePhysicalStateAdmin(admin.ModelAdmin):
    model = MedicinePhysicalState
    list_display = (
        'uid',
        'name',
        'updated_at',
    )

    list_filter = (
        'name',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(RouteOfAdministration)
class RouteOfAdministrationAdmin(admin.ModelAdmin):
    model = RouteOfAdministration
    list_display = (
        'uid',
        'name',
        'updated_at',
    )

    list_filter = (
        'name',
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    model = District
    list_display = (
        'uid',
        'name'
    )


@admin.register(DeliveryCharge)
class DeliveryChargeAdmin(admin.ModelAdmin):
    model = DeliveryCharge
    list_display = (
        'uid',
        'charge',
        'district'
    )

    def save_model(self, request, obj, form, change):
        obj.admin = request.user
        obj.save()


class BaseProductImageInline(admin.TabularInline):
    model = ProductImage
    fk_name = 'base_product'
    exclude = ('product',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fk_name = 'product'
    exclude = ('base_product',)


@admin.register(BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    model = BaseProduct
    list_display = (
        'uid',
        'name'
    )
    list_filter = (
        'active',
        ('deleted_at', admin.EmptyFieldListFilter)
    )
    exclude = ('product',)
    readonly_fields = ('superadmin',)
    inlines = (BaseProductImageInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.superadmin = request.user
        obj.save()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        'uid',
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
    inlines = (ProductImageInline,)
