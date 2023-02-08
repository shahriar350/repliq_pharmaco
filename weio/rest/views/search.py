from django.db.models import Q
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from catalogio.models import BaseProduct
from weio.rest.permissions import IsOrganizationStaff
from weio.rest.serializers.search import PrivateBaseProductSearchSerializers


class GetBaseProductSearch(ListAPIView):
    serializer_class = PrivateBaseProductSearchSerializers
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        return BaseProduct.objects.filter(Q(deleted_at__isnull=True) & Q(active=True) & Q(superadmin__isnull=False))
