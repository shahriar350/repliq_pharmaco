from rest_framework import serializers

from product_app.models import BaseProduct
from admin_app.models import Category, Brand, Ingredient, Manufacturer, Supplier, MedicinePhysicalState, \
    RouteOfAdministration


class MerchantProductSearchSerializer(serializers.ModelSerializer):
    manufacturer = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    route_of_administration = serializers.StringRelatedField()
    medicine_physical_state = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)
    active_ingredient = serializers.StringRelatedField(many=True)

    class Meta:
        model = BaseProduct
        fields = (
            'uuid',
            'name',
            'category',
            'active_ingredient',
            'dosage_form',
            'manufacturer',
            'brand',
            'route_of_administration',
            'medicine_physical_state',
        )


class CategorySearchSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = (
            'uuid',
            'name',
            'parent',
        )


class BrandSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'uuid',
            'name',
        )


class IngredientSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'uuid',
            'name',
        )


class ManufacturerSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = (
            'uuid',
            'name',
        )


class SupplierSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            'uuid',
            'name',
        )


class MedicinePhysicalStateSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinePhysicalState
        fields = (
            'uuid',
            'name',
        )


class RouteOfAdministrationSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteOfAdministration
        fields = (
            'uuid',
            'name',
        )
