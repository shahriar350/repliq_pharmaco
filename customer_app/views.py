from django.db.models import Q
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from customer_app.models import Cart
from customer_app.serializers import CartProductSerializer, CartProductUpdateSerializer, \
    CartModelSerialiser, AddressCRUDSerializers, CheckoutSerializer
from rest_framework.permissions import IsAuthenticated
from auth_app.models import UserAddress


# Create your views here.
class AddToCartView(CreateAPIView):
    serializer_class = CartProductSerializer
    permission_classes = (IsAuthenticated,)


class RemoveUpdateToCartView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put', 'delete']
    serializer_class = CartProductUpdateSerializer

    def perform_destroy(self, instance):
        instance.delete()

    def get_object(self):
        cart = Cart.objects.prefetch_related('get_cart_products').filter(
            Q(active=True) & Q(deleted_at__isnull=True)).get(customer=self.request.user)
        return cart.get_cart_products.all().get(uuid=self.kwargs.get('cart_product_uuid'))


class CartListView(ListAPIView):
    serializer_class = CartModelSerialiser
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user).prefetch_related(
            "get_cart_products", 'get_cart_products__product').all()


class CartCurrentListView(APIView):
    serializer_class = CartModelSerialiser
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: OpenApiResponse(response=CartModelSerialiser),
            400: OpenApiResponse(description='Invalid data'),
        },
    )
    def get(self, request, format=None):
        cart = Cart.objects.prefetch_related("get_cart_products").get(customer=request.user)
        return Response(status=200, data=CartModelSerialiser(cart).data)


class AddressCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressCRUDSerializers


class AddressListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressCRUDSerializers

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).all()


class AddressRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressCRUDSerializers

    def get_object(self):
        return UserAddress.objects.filter(user=self.request.user).get(uuid=self.kwargs.get('uuid'))


class CheckoutView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CheckoutSerializer
