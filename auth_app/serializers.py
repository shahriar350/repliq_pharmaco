from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

from auth_app.models import Users, UserAddress, MerchantInformation
from client_app.models import Tenant


class MerchantLoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)


class OTPLoginSerializer(serializers.Serializer):
    otp = serializers.IntegerField(write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
