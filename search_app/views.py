from django.db.models import Q
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import MerchantProductSearchSerializer, CategorySearchSerializer, BrandSearchSerializer, \
    IngredientSearchSerializer, ManufacturerSearchSerializer, SupplierSearchSerializer, \
    MedicinePhysicalStateSearchSerializer, RouteOfAdministrationSearchSerializer
from pharmaco_backend.permissions import IsMerchant
from product_app.models import BaseProduct
from admin_app.models import Category, Brand, Ingredient, Manufacturer, Supplier, MedicinePhysicalState, \
    RouteOfAdministration


# Create your views here.
class BaseProductSearchView(ListAPIView):
    permission_classes = [IsMerchant]
    serializer_class = MerchantProductSearchSerializer
    queryset = BaseProduct.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class CategorySearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySearchSerializer
    queryset = Category.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class BrandSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BrandSearchSerializer
    queryset = Brand.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class IngredientSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSearchSerializer
    queryset = Ingredient.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class ManufacturerSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ManufacturerSearchSerializer
    queryset = Manufacturer.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class SupplierSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSearchSerializer
    queryset = Supplier.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class MedicinePhysicalStateSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicinePhysicalStateSearchSerializer
    queryset = MedicinePhysicalState.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class RouteOfAdministrationSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouteOfAdministrationSearchSerializer
    queryset = RouteOfAdministration.objects.filter(Q(active=True) & Q(deleted_at__isnull=True)).all()
    filter_backends = [SearchFilter]
    search_fields = ['name']
