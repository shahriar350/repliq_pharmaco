from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from product_app.models import BaseProduct
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Category, Brand, Ingredient, Manufacturer, Supplier, MedicinePhysicalState, RouteOfAdministration
from rest_framework.exceptions import ValidationError
from auth_app.models import Users


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'uuid', 'name', 'parent')
        read_only_fields = ('id', 'uuid')


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'uuid', 'name')
        read_only_fields = ('id', 'uuid')


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'uuid', 'name')
        read_only_fields = ('id', 'uuid')


class ManufacturerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'uuid', 'name', 'deleted_at')
        read_only_fields = ('id', 'uuid')


class SupplierSerializers(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'uuid', 'name')
        read_only_fields = ('id', 'uuid')


class MedicinePhysicalStateSerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicinePhysicalState
        fields = ('id', 'uuid', 'name')
        read_only_fields = ('id', 'uuid')


class RouteOfAdministrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = RouteOfAdministration
        fields = ('id', 'uuid', 'name')
        read_only_fields = ('id', 'uuid')


class AdminLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)


class AdminBaseProductCreateUpdateSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    admin = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(max_length=255, required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(active=True).filter(deleted_at__isnull=True).all(), many=True,
        required=False)
    active_ingredient = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.filter(active=True).filter(deleted_at__isnull=True).all(), many=True,
        required=False)
    dosage_form = serializers.CharField(max_length=255, required=False)
    manufacturer = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.filter(active=True).filter(deleted_at__isnull=True).all(), required=False)
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.filter(active=True).filter(deleted_at__isnull=True).all(), required=False)
    route_of_administration = serializers.PrimaryKeyRelatedField(
        queryset=RouteOfAdministration.objects.filter(active=True).filter(deleted_at__isnull=True).all(),
        required=False)
    medicine_physical_state = serializers.PrimaryKeyRelatedField(
        queryset=MedicinePhysicalState.objects.filter(active=True).filter(deleted_at__isnull=True).all(),
        required=False)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        admin = validated_data.get('admin', None)
        name = validated_data.get('name', None)
        description = validated_data.get('description', None)
        categories = validated_data.get('category', None)
        active_ingredients = validated_data.get('active_ingredient', None)
        dosage_form = validated_data.get('dosage_form', None)
        manufacturer = validated_data.get('manufacturer', None)
        brand = validated_data.get('brand', None)
        route_of_administration = validated_data.get('route_of_administration', None)
        medicine_physical_state = validated_data.get('medicine_physical_state', None)
        # create product for merchant
        with transaction.atomic():
            base_product = BaseProduct.objects.create(
                name=name,
                description=description,
                dosage_form=dosage_form,
                manufacturer=manufacturer,
                brand=brand,
                route_of_administration=route_of_administration,
                medicine_physical_state=medicine_physical_state,
                superadmin=admin
            )
            validated_data['uuid'] = base_product.uuid
            for category in categories:
                base_product.category.add(category)
            for ingredient in active_ingredients:
                base_product.active_ingredient.add(ingredient)

        return validated_data

    def update(self, instance, validated_data):
        name = validated_data.get('name', None)
        description = validated_data.get('description', None)
        categories = validated_data.get('category', None)
        active_ingredients = validated_data.get('active_ingredient', None)
        dosage_form = validated_data.get('dosage_form', None)
        manufacturer = validated_data.get('manufacturer', None)
        brand = validated_data.get('brand', None)
        route_of_administration = validated_data.get('route_of_administration', None)
        medicine_physical_state = validated_data.get('medicine_physical_state', None)
        # create product for merchant
        with transaction.atomic():
            if name is not None:
                instance.name = name
            if description is not None:
                instance.description = description
            if dosage_form is not None:
                instance.dosage_form = dosage_form
            if manufacturer is not None:
                instance.manufacturer = manufacturer
            if brand is not None:
                instance.brand = brand
            if route_of_administration is not None:
                instance.route_of_administration = route_of_administration
            if medicine_physical_state is not None:
                instance.medicine_physical_state = medicine_physical_state
            instance.save()

            if categories is not None:
                instance.category.clear()
                for category in categories:
                    instance.category.add(category)
            if active_ingredients is not None:
                instance.active_ingredient.clear()
                for ingredient in active_ingredients:
                    instance.active_ingredient.add(ingredient)

        return validated_data


class BaseProductSerializer(serializers.ModelSerializer):
    superadmin = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BaseProduct
        fields = "__all__"
        read_only_fields = ['superadmin', 'merchant_product']


class BaseProductRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializers(many=True, read_only=True)
    active_ingredient = IngredientSerializers(many=True, read_only=True)
    manufacturer = ManufacturerSerializers(read_only=True)
    brand = BrandSerializers(read_only=True)
    route_of_administration = RouteOfAdministrationSerializers(read_only=True)
    medicine_physical_state = MedicinePhysicalStateSerializers(read_only=True)

    # superadmin = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BaseProduct
        fields = "__all__"
        # read_only_fields = ['superadmin', 'merchant_product']


class SuperUserRegisterSerializer(serializers.Serializer):
    TYPE_CHOICES = (
        ('staff', 'STAFF'),
        ('admin', 'ADMIN'),
    )

    phone_number = PhoneNumberField()
    full_name = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    role = serializers.CharField(read_only=True)
    password = serializers.CharField(max_length=255)
    repeat_password = serializers.CharField(max_length=255)

    def validate_phone_number(self, data):
        if Users.objects.filter(phone_number=data).exists():
            raise ValidationError("Phone number is already exists.")
        return data

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise ValidationError({'repeat_password': "Repeat password is not match to password."})
        return data

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        full_name = validated_data.get('full_name')
        password = validated_data.get('password')
        type = validated_data.get('type')
        if type == 'staff':
            user = Users(
                phone_number=phone_number,
                name=full_name,
                staff=True,
                active=True,
                is_verified=True
            )
            validated_data['role'] = 'staff'

        else:
            user = Users(
                phone_number=phone_number,
                name=full_name,
                admin=True,
                active=True,
                is_verified=True
            )
            validated_data['role'] = 'admin'
        user.set_password(password)
        user.save()
        return validated_data
