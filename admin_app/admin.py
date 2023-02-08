from django.contrib import admin
from .models import Category, Brand, Supplier, Ingredient, Manufacturer, MedicinePhysicalState, RouteOfAdministration, \
    District, DeliveryCharge


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        'uuid',
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
        'uuid',
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
        'uuid',
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
        'uuid',
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
        'uuid',
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
        'uuid',
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
        'uuid',
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
        'uuid',
        'name'
    )


@admin.register(DeliveryCharge)
class DeliveryChargeAdmin(admin.ModelAdmin):
    model = DeliveryCharge
    list_display = (
        'uuid',
        'charge',
        'district'
    )

    def save_model(self, request, obj, form, change):
        obj.admin = request.user
        obj.save()

    # def get_form(self, request, obj=None, **kwargs):
    #     self.exclude = ("admin",)
    #     form = super(DeliveryChargeAdmin, self).get_form(request, obj, **kwargs)
    #     return form
