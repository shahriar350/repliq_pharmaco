from datetime import timedelta

from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from merchant_app.documentation_serializers import MerchantLogin200Serializer
from merchant_app.serializers import MerchantLoginSerializer, MerchantRegisterSerializer, MerchantInfoSerializer, \
    MerchantProductCreateSerializer, CreateMerchantAdminSerializer, MerchantProductUpdateSerializer, \
    MerchantProductImageAddSerializer, MerchantProductSerializer, MerchantProductWithUUIDCreateSerializer
from otp_app.models import UserOTP
from pharmaco_backend.permissions import IsMerchant, IsMerchantOwnerOrAdmin, IsMerchantAdmin, IsMerchantOwner
from pharmaco_backend.utils import otpgen
from product_app.models import Product, BaseProduct


# Create your views here.
class MerchantLogin(CreateAPIView):
    serializer_class = MerchantLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')
        user = authenticate(username=phone_number, password=password)
        if user and user.is_merchant():
            UserOTP.objects.create(
                user=user,
                validate_time=timezone.now() + timedelta(minutes=15),
                otp=otpgen()
            )
            return Response({
                'message': "A otp has been send to your number."
            }, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Phone number or Password or Both are wrong.")


class MerchantRegister(CreateAPIView):
    serializer_class = MerchantRegisterSerializer


class MerchantInfoAddView(CreateAPIView):
    serializer_class = MerchantInfoSerializer
    permission_classes = (IsMerchant,)


class AddProductView(CreateAPIView):
    permission_classes = (IsMerchant,)
    serializer_class = MerchantProductWithUUIDCreateSerializer
    # serializer_class = MerchantProductCreateSerializer


@extend_schema(
    summary="Only Merchant who is owner can create admin only.",
)
class AuthCreateMerchantAdminView(CreateAPIView):
    permission_classes = (IsMerchantOwner,)
    serializer_class = CreateMerchantAdminSerializer


class UpdateDestroyProductInfoView(RetrieveUpdateDestroyAPIView):
    serializer_class = MerchantProductUpdateSerializer
    permission_classes = (IsMerchant,)
    http_method_names = ('put', 'delete',)

    def get_object(self):
        return Product.objects.get(slug=self.kwargs.get('product_slug'))

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# @extend_schema(
#     summary="Only merchant can remove product",
#     responses={
#         200: OpenApiResponse(description='Product is successfully removed'),
#         404: OpenApiResponse(description='Product cannot found.'),
#     },
# )
# class RemoveProductInfoView(DestroyAPIView):
#     def get_object(self):
#         try:
#             return Product.objects.get(pk=self.kwargs.get('product_id'))
#         except Product.DoesNotExist:
#             raise NotFound(detail="Product cannot found.")
#
#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()
#
#     def delete(self, request, *args, **kwargs):
#         super(RemoveProductInfoView, self).destroy(request, *args, **kwargs)
#         return Response(status=status.HTTP_200_OK)

class RestoreProductInfoView(DestroyAPIView):
    permission_classes = [IsMerchant]
    serializer_class = MerchantProductSerializer

    def get_object(self):
        return Product.objects.get(slug=self.kwargs.get('product_slug'))

    def perform_destroy(self, instance):
        instance.deleted_at = None
        instance.save()


class AddImageProductView(UpdateAPIView):
    permission_classes = [IsMerchant]
    serializer_class = MerchantProductImageAddSerializer
    parser_classes = (FormParser, MultiPartParser,)

    def get_object(self):
        try:
            return Product.objects.get(slug=self.kwargs.get('product_slug'))
        except Product.DoesNotExist:
            raise NotFound(detail="Product cannot found.")


class RemoveImageFromProductView(DestroyAPIView):
    permission_classes = [IsMerchant]
    serializer_class = MerchantProductImageAddSerializer

    def get_object(self):
        try:
            product = Product.objects.select_related('base_product').prefetch_related('get_product_images',
                                                                                      'get_base_product').get(
                uuid=self.kwargs.get('product_uuid'))
            if hasattr(product.get_base_product, 'uuid'):
                images = product.get_product_images.all()
                return images.filter(uuid=self.kwargs.get('image_uuid')).first()
            else:
                raise ValidationError("You cannot remove this image.")

        except Product.DoesNotExist:
            raise NotFound(detail="Product cannot found.")


class MerchantAuthCheckView(APIView):
    permission_classes = [IsMerchant]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
