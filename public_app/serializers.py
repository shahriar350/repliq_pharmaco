from rest_framework import serializers


class BaseProductUUIDNamePublicSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255,read_only=True)


class BaseProductPublicSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    category = BaseProductUUIDNamePublicSerializer(many=True, read_only=True)
    active_ingredient = BaseProductUUIDNamePublicSerializer(many=True, read_only=True)
    dosage_form = serializers.CharField(read_only=True)
    manufacturer = BaseProductUUIDNamePublicSerializer(read_only=True)
    brand = BaseProductUUIDNamePublicSerializer(read_only=True)
    route_of_administration = BaseProductUUIDNamePublicSerializer(read_only=True)
    medicine_physical_state = BaseProductUUIDNamePublicSerializer(read_only=True)


class ProductListPublicSerializer(serializers.Serializer):
    slug = serializers.SlugField(read_only=True)
    stock = serializers.IntegerField(read_only=True)
    selling_price = serializers.DecimalField(default=0, decimal_places=2, max_digits=10, read_only=True)
    base_product = BaseProductPublicSerializer()
