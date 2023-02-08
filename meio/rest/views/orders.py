from rest_framework.generics import ListCreateAPIView, CreateAPIView

from meio.rest.serializers.orders import PublicOrderSerializer


class ListCreateOrder(CreateAPIView):
    serializer_class = PublicOrderSerializer