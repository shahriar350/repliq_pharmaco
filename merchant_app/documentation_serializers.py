from rest_framework import serializers


class MerchantRegisterResponse200Serializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class MerchantLogin200Serializer(serializers.Serializer):
    message = serializers.CharField()
