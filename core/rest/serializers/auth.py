from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from core.models import User


# User = get_user_model()


class LogoutRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)


class PublicUserRegistrationSerializer(serializers.Serializer):
    slug = serializers.SlugField(read_only=True)
    name = serializers.CharField(label="Your full name")
    phone = PhoneNumberField()
    password = serializers.CharField(min_length=6)

    def phone_validate(self, value):
        if User.objects.filter(phone=value).exists():
            raise ValidationError("This phone number is already taken by another user", code=422)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(name=validated_data.get('name'), phone=validated_data.get('phone'),
                                        password=validated_data.get('password'))
        validated_data['slug'] = user.slug
        return validated_data
