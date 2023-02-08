from rest_framework import serializers


class TenantAvailabilityResponseSerializer(serializers.Serializer):
    available = serializers.BooleanField()
