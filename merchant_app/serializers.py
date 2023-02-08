from django.db import transaction
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from admin_app.models import Category, Ingredient, Manufacturer, Brand, RouteOfAdministration, MedicinePhysicalState
from auth_app.models import Users, UserAddress, MerchantInformation
from client_app.models import Tenant
from product_app.models import BaseProduct, Product, ProductImage


class MerchantLoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField(max_length=255)


class MerchantRegisterSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    repeat_password = serializers.CharField(max_length=255, write_only=True)

    def validate_phone_number(self, data):
        if Users.objects.filter(phone_number=data).exists():
            raise ValidationError("Phone number is already exists.")
        return data

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise ValidationError({'repeat_password': "Repeat password is not match to password."})
        return super(MerchantRegisterSerializer, self).validate(data)

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        full_name = validated_data.get('full_name')
        password = validated_data.get('password')
        Users.objects.create_merchant_owner(
            phone_number=phone_number,
            name=full_name,
            password=password
        )
        return validated_data


class UserAddressBasicSerializer(serializers.Serializer):
    house = serializers.CharField()
    street = serializers.CharField()
    post_office = serializers.CharField(allow_null=True, allow_blank=True)
    police_station = serializers.CharField(allow_null=True, allow_blank=True)
    district = serializers.CharField(allow_null=True, allow_blank=True)
    country = serializers.CharField(allow_null=True, allow_blank=True)
    state = serializers.CharField()


class MerchantInfoSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    merchant_domain = serializers.CharField(max_length=255)
    company_name = serializers.CharField(max_length=255)

    def validate_merchant_domain(self, data):
        if Tenant.objects.filter(url=data).exists():
            raise ValidationError("This tenant is not available.")
        return data

    def create(self, validated_data):
        tenant = Tenant.objects.create(url=validated_data.get('merchant_domain'))
        with transaction.atomic():
            MerchantInformation.objects.create(
                merchant_domain=tenant,
                company_name=validated_data.get('company_name'),
                user=validated_data.get('user')
            )
        return validated_data


# product create serializers
class MerchantProductCreateSerializer(serializers.Serializer):
    merchant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(max_length=255, required=False)
    slug = serializers.SlugField(read_only=True)
    base_product = serializers.PrimaryKeyRelatedField(
        queryset=BaseProduct.objects.filter(active=True).filter(deleted_at__isnull=True).filter(
            superadmin__isnull=False).all(), required=False,
        help_text="If you donot have base product, so do not send the base_product to server because server search base_product, if server found base_product in your json data, server expect to get a id of base product."
    )
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
        queryset=Brand.objects.filter(active=True).filter(deleted_at__isnull=True).all(), required=False, )
    route_of_administration = serializers.PrimaryKeyRelatedField(
        queryset=RouteOfAdministration.objects.filter(active=True).filter(deleted_at__isnull=True).all(),
        required=False)
    medicine_physical_state = serializers.PrimaryKeyRelatedField(
        queryset=MedicinePhysicalState.objects.filter(active=True).filter(deleted_at__isnull=True).all(),
        required=False)
    description = serializers.CharField(required=False)
    stock = serializers.IntegerField()
    buying_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)
    selling_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)

    def validate(self, data):
        # if not self.context['request'].subdomain:
        #     raise ValidationError("Merchant must have a subdomain.")
        base_product = data.get('base_product') or None
        name = data.get('name') or None
        category = data.get('category') or None
        active_ingredient = data.get('active_ingredient') or None
        dosage_form = data.get('dosage_form') or None
        manufacturer = data.get('manufacturer') or None
        brand = data.get('brand') or None
        route_of_administration = data.get('route_of_administration') or None
        medicine_physical_state = data.get('medicine_physical_state') or None
        if base_product is None:
            if name is None or category is None or active_ingredient is None or dosage_form is None or manufacturer is None or brand is None or route_of_administration is None or medicine_physical_state is None:
                raise ValidationError("If you donot have base product, you have to provide rest of the data")
        # super(MerchantProductCreateSerializer, self).validate(data)
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
        selling_price = validated_data.get('selling_price', None)
        domain = merchant.get_user_information.merchant_domain
        if base_product is not None:
            Product.objects.create(
                base_product=base_product,
                stock=stock,
                buying_price=buying_price,
                selling_price=selling_price,
                merchant=merchant,
                merchant_domain=domain,
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
                for category in categories:
                    base_product.category.add(category)
                for ingredient in active_ingredients:
                    base_product.active_ingredient.add(ingredient)

                product = Product.objects.create(
                    base_product=base_product,
                    stock=stock,
                    buying_price=buying_price,
                    selling_price=selling_price,
                    merchant=merchant,
                    merchant_domain=domain,
                )
                base_product.merchant_product = product
                base_product.save()
        return validated_data


class CreateMerchantAdminSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    phone_number = PhoneNumberField()
    password = serializers.CharField(min_length=6)
    image = serializers.ImageField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        owner = validated_data['user']
        user_merchant_admin = Users.objects.create_merchant_admin(
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )
        MerchantInformation.objects.create(
            user=user_merchant_admin,
            merchant_domain=owner.get_user_information.merchant_domain,
            merchant_parent_who_created=owner,
            company_name=owner.get_user_information.company_name
        )


class MerchantProductUpdateSerializer(serializers.Serializer):
    stock = serializers.IntegerField(min_value=0, required=False)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, required=False)
    buying_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, required=False)
    active = serializers.BooleanField(default=True)

    def update(self, instance, validated_data):
        stock = validated_data.get('stock', None)
        buying_price = validated_data.get('buying_price', None)
        selling_price = validated_data.get('selling_price', None)
        active = validated_data.get('active', None)
        if stock is not None:
            instance.stock = stock
        if buying_price is not None:
            instance.buying_price = buying_price
        if selling_price is not None:
            instance.selling_price = selling_price
        if active is not None:
            instance.active = active
        instance.save()
        return validated_data


class MerchantProductImageAddSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = serializers.ListField(child=serializers.ImageField())

    def update(self, instance, validated_data):
        images = validated_data.get('images')
        for i in images:
            img = ProductImage.objects.create(
                image=i,
                product=instance
            )
        return validated_data


class MerchantProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class MerchantProductWithUUIDCreateSerializer(serializers.Serializer):
    merchant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(max_length=255, required=False)
    slug = serializers.SlugField(read_only=True)
    base_product = serializers.UUIDField(required=False)
    category = serializers.ListField(child=serializers.UUIDField(), required=False)
    active_ingredient = serializers.ListField(child=serializers.UUIDField(), required=False)
    dosage_form = serializers.CharField(max_length=255, required=False)
    manufacturer = serializers.UUIDField(required=False)
    brand = serializers.UUIDField(required=False)
    route_of_administration = serializers.UUIDField(required=False)
    medicine_physical_state = serializers.UUIDField(required=False)
    description = serializers.CharField(required=False)
    stock = serializers.IntegerField()
    buying_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)
    selling_price = serializers.DecimalField(decimal_places=2, max_digits=10, default=0)

    def create(self, validated_data):
        merchant = validated_data.get('merchant', None)
        base_product = validated_data.get('base_product', None)
        base_product_obj = None
        if base_product is not None:
            try:
                base_product_obj = BaseProduct.objects.get(uuid=base_product)
            except BaseProduct.DoesNotExist:
                raise ValidationError({'base_product': "Invalid uuid"})

        name = validated_data.get('name', None)
        description = validated_data.get('description', None)
        categories = validated_data.get('category', None)
        categories_arr = []
        if categories is not None:
            try:
                for uuid in categories:
                    data = Category.objects.get(uuid=uuid)
                    categories_arr.append(data.id)
            except Category.DoesNotExist:
                raise ValidationError({'categories': "Invalid uuid"})

        active_ingredients = validated_data.get('active_ingredient', None)
        active_ingredients_arr = []
        if active_ingredients is not None:
            try:
                for uuid in active_ingredients:
                    data = Ingredient.objects.get(uuid=uuid)
                    active_ingredients_arr.append(data.id)
            except Ingredient.DoesNotExist:
                raise ValidationError({'active_ingredients': "Invalid uuid"})

        dosage_form = validated_data.get('dosage_form', None)
        manufacturer = validated_data.get('manufacturer', None)
        manufacturer_obj = None
        if manufacturer is not None:
            try:
                manufacturer_obj = Manufacturer.objects.get(uuid=manufacturer)
            except Manufacturer.DoesNotExist:
                raise ValidationError({'manufacturer': "Invalid uuid"})

        brand = validated_data.get('brand', None)
        brand_obj = None
        if brand is not None:
            try:
                brand_obj = Brand.objects.get(uuid=brand)
            except Brand.DoesNotExist:
                raise ValidationError({'brand': "Invalid uuid"})

        route_of_administration = validated_data.get('route_of_administration', None)
        route_of_administration_obj = None
        if route_of_administration is not None:
            try:
                route_of_administration_obj = RouteOfAdministration.objects.get(uuid=route_of_administration)
            except RouteOfAdministration.DoesNotExist:
                raise ValidationError({'route_of_administration': "Invalid uuid"})

        medicine_physical_state = validated_data.get('medicine_physical_state', None)
        medicine_physical_state_obj = None
        if medicine_physical_state is not None:
            try:
                medicine_physical_state_obj = MedicinePhysicalState.objects.get(uuid=medicine_physical_state)
            except MedicinePhysicalState.DoesNotExist:
                raise ValidationError({'medicine_physical_state': "Invalid uuid"})

        stock = validated_data.get('stock', None)
        buying_price = validated_data.get('buying_price', None)
        selling_price = validated_data.get('selling_price', None)
        domain = merchant.get_user_information.merchant_domain
        if base_product is not None:
            Product.objects.create(
                base_product=base_product_obj,
                stock=stock,
                buying_price=buying_price,
                selling_price=selling_price,
                merchant=merchant,
                merchant_domain=domain,
            )
        else:
            # create product for merchant
            with transaction.atomic():
                base_product_obj = BaseProduct.objects.create(
                    name=name,
                    description=description,
                    dosage_form=dosage_form,
                    manufacturer=manufacturer_obj,
                    brand=brand_obj,
                    route_of_administration=route_of_administration_obj,
                    medicine_physical_state=medicine_physical_state_obj
                )
                if len(categories_arr) > 0:
                    for category in categories_arr:
                        base_product_obj.category.add(category)
                if len(active_ingredients_arr) > 0:
                    for ingredient in active_ingredients_arr:
                        base_product_obj.active_ingredient.add(ingredient)

                product = Product.objects.create(
                    base_product=base_product_obj,
                    stock=stock,
                    buying_price=buying_price,
                    selling_price=selling_price,
                    merchant=merchant,
                    merchant_domain=domain,
                )
                base_product_obj.merchant_product = product
                base_product_obj.save()
        return validated_data
