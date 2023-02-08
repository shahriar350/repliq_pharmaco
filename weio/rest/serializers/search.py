from rest_framework import serializers

from catalogio.models import BaseProduct


class PrivateBaseProductSearchSerializers(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    active_ingredients = serializers.StringRelatedField(many=True)
    dosage_form = serializers.StringRelatedField()
    manufacturer = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    route_of_administration = serializers.StringRelatedField()
    medicine_physical_state = serializers.StringRelatedField()

    class Meta:
        model = BaseProduct
        fields = (
            'uid',
            'name',
            'description',
            'categories',
            'active_ingredients',
            'dosage_form',
            'manufacturer',
            'brand',
            'route_of_administration',
            'medicine_physical_state',
            'image',
        )
        read_only_fields = ("__all__",)
