from rest_framework import serializers


# class MerchantRegisterResponse200Serializer(serializers.Serializer):
#     access_token = serializers.CharField()
#     refresh_token = serializers.CharField()
#
#
# class MerchantLogin200Serializer(serializers.Serializer):
#     message = serializers.CharField()

class LogoutRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)
