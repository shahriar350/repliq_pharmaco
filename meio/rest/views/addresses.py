from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from addressio.models import Address, UserAddress
from meio.rest.serializers.addresses import PublicAddressSerializers
from django.utils import timezone


class ListPostAddress(ListCreateAPIView):
    serializer_class = PublicAddressSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(useraddress__user=self.request.user)


class UpdateDeleteAddress(RetrieveUpdateDestroyAPIView):
    serializer_class = PublicAddressSerializers
    permission_classes = [IsAuthenticated]
    http_method_names = ('put', "delete", "get")

    def get_object(self):
        return Address.objects.get(slug=self.kwargs.get('slug'))

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
