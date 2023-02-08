from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from meio.rest.serializers.carts import PrivateAddToCart, PrivateCarts
from rest_framework.permissions import IsAuthenticated

from orderio.models import Cart


class GetPostCart(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return PrivateAddToCart
        else:
            return PrivateCarts

    def get_queryset(self):
        try:
            cart = Cart.objects.prefetch_related('cart_products__product').get(customer=self.request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.prefetch_related('cart_products__product').none()
        return cart

    def list(self, request, *args, **kwargs):
        serializer = super().get_serializer(self.get_queryset())
        return Response(serializer.data)
