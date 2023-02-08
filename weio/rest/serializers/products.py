from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from accountio.models import Organization, OrganizationUser
from catalogio.models import BaseProduct, Product, Category, Ingredient, Manufacturer, Brand, RouteOfAdministration, \
    MedicinePhysicalState


class PrivateProductSerializers(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, allow_null=True)
    merchant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    slug = serializers.SlugField(read_only=True)
    organization = serializers.SlugRelatedField(queryset=Organization.objects.filter(), slug_field='uid')
    base_product = serializers.SlugRelatedField(
        queryset=BaseProduct.objects.filter(active=True).filter(deleted_at__isnull=True).filter(
            superadmin__isnull=False).all(), slug_field='uid', allow_null=True, allow_empty=True,
        help_text="If you donot have base product, so do not send the base_product to server."
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.filter(active=True).filter(deleted_at__isnull=True).all(), many=True,
        slug_field='uid',
        allow_empty=True, allow_null=True)
    active_ingredient = serializers.SlugRelatedField(
        queryset=Ingredient.objects.filter(active=True).filter(deleted_at__isnull=True).all(), many=True,
        slug_field='uid',
        allow_empty=True, allow_null=True)
    dosage_form = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    manufacturer = serializers.SlugRelatedField(
        queryset=Manufacturer.objects.filter(active=True).filter(deleted_at__isnull=True).all(), allow_empty=True,
        allow_null=True,
        slug_field='uid')
    brand = serializers.SlugRelatedField(
        queryset=Brand.objects.filter(active=True).filter(deleted_at__isnull=True).all(), slug_field='uid',
        allow_empty=True, allow_null=True, )
    route_of_administration = serializers.SlugRelatedField(
        queryset=RouteOfAdministration.objects.filter(active=True).filter(deleted_at__isnull=True).all(),
        slug_field='uid',
        allow_empty=True, allow_null=True)
    medicine_physical_state = serializers.SlugRelatedField(
        queryset=MedicinePhysicalState.objects.filter(active=True).filter(deleted_at__isnull=True).all(),
        slug_field='uid',
        allow_empty=True, allow_null=True)
    description = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    stock = serializers.IntegerField()
    buying_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)
    selling_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)

    def validate(self, data):
        base_product = data.get('base_product', None)
        name = data.get('name', None)
        category = data.get('category', [])
        active_ingredient = data.get('active_ingredient', [])
        dosage_form = data.get('dosage_form', None)
        manufacturer = data.get('manufacturer', None)
        brand = data.get('brand', None)
        route_of_administration = data.get('route_of_administration', None)
        medicine_physical_state = data.get('medicine_physical_state', None)
        organization = data.get('organization', None)
        merchant = data.get('merchant', None)
        if not OrganizationUser.objects.filter(organization=organization, user=merchant).exists():
            raise ValidationError({'organization': "Invalid organization."})

        if base_product is None:
            if name is None:
                raise ValidationError({'name': "Product name is required."})
            if len(category) < 1:
                raise ValidationError({'category': "Categories are required."})
            if len(active_ingredient) < 1:
                raise ValidationError({'active_ingredient': "Active ingredients are required."})
            if dosage_form is None:
                raise ValidationError({'dosage_form': "Dosage form is required."})
            if manufacturer is None:
                raise ValidationError({'manufacturer': "Manufacturer is required."})
            if brand is None:
                raise ValidationError({'brand': "Brand is required."})
            if route_of_administration is None:
                raise ValidationError({'route_of_administration': "Route of administration is required."})
            if medicine_physical_state is None:
                raise ValidationError({'medicine_physical_state': "Medicine physical state is required."})
        return data

    def create(self, validated_data):
        merchant = validated_data.get('merchant', None)
        base_product = validated_data.get('base_product', None)
        name = validated_data.get('name', None)
        description = validated_data.get('description', None)
        categories = validated_data.get('category', None)
        active_ingredients = validated_data.get('active_ingredient', None)
        dosage_form = validated_data.get('dosage_form', None)
        manufacturer = validated_data.get('manufacturer', None)
        brand = validated_data.get('brand', None)
        route_of_administration = validated_data.get('route_of_administration', None)
        medicine_physical_state = validated_data.get('medicine_physical_state', None)
        stock = validated_data.get('stock', None)
        buying_price = validated_data.get('buying_price', None)
        organization = validated_data.get('organization', None)
        selling_price = validated_data.get('selling_price', None)
        if base_product is not None:
            Product.objects.create(
                base_product=base_product,
                organization=organization,
                stock=stock,
                buying_price=buying_price,
                selling_price=selling_price,
                merchant=merchant
            )
        else:
            # create product for merchant
            with transaction.atomic():
                base_product = BaseProduct.objects.create(
                    name=name,
                    description=description,
                    dosage_form=dosage_form,
                    manufacturer=manufacturer,
                    brand=brand,
                    route_of_administration=route_of_administration,
                    medicine_physical_state=medicine_physical_state
                )
                if categories is not None:
                    for category in categories:
                        base_product.categories.add(category)

                if active_ingredients is not None:
                    for ingredient in active_ingredients:
                        base_product.active_ingredients.add(ingredient)

                product = Product.objects.create(
                    base_product=base_product,
                    organization=organization,
                    stock=stock,
                    buying_price=buying_price,
                    selling_price=selling_price,
                    merchant=merchant
                )
                base_product.merchant_product = product
                base_product.save()
            validated_data['uid'] = product.uid
        return validated_data
