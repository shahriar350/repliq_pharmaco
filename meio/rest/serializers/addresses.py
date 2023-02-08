from rest_framework import serializers

from addressio.models import Address, UserAddress
from core.models import District


class PublicAddressSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    slug = serializers.SlugField(read_only=True)
    district = serializers.SlugRelatedField(queryset=District.objects.filter(active=True, deleted_at__isnull=True),
                                            slug_field='slug')

    class Meta:
        model = Address
        fields = (
            'slug',
            'user',
            'label',
            'slug',
            'house',
            'street',
            'post_office',
            'police_station',
            'district',
            'country',
            'state',
        )

    def create(self, validated_data):
        user = validated_data.pop('user')
        address = Address.objects.create(**validated_data)
        UserAddress.objects.create(
            user=user,
            address=address
        )
        validated_data['slug'] = address.slug
        return validated_data
