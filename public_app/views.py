from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from client_app.models import Tenant
from pharmaco_backend.utils import PageNumberPaginationWithCount
from product_app.models import Product
from public_app.documentation_serializers import TenantAvailabilityResponseSerializer
from public_app.serializers import ProductListPublicSerializer


# Create your views here.

class TenantAvailabilityCheckView(APIView):
    @extend_schema(
        summary="Search tenant url if available or not.",
        responses={
            200: OpenApiResponse(response=TenantAvailabilityResponseSerializer,
                                 description='It response 200 because tenant is available.'),
            204: OpenApiResponse(response=TenantAvailabilityResponseSerializer,
                                 description='It response 204 because tenant not is available.'),

        }
    )
    def get(self, request, tenant_url):
        tenant_url = tenant_url.replace(' ', '')  # remove all space from string
        if not Tenant.objects.filter(url=tenant_url).exists():
            return Response({
                "available": True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "available": False
            }, status=status.HTTP_204_NO_CONTENT)


class ProductListView(ListAPIView):
    pagination_class = PageNumberPaginationWithCount
    serializer_class = ProductListPublicSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related('base_product__category').filter(
            Q(active=True) & Q(deleted_at__isnull=True)).order_by('slug')
