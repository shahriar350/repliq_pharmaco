from rest_framework.generics import CreateAPIView

from weio.rest.permissions import IsOrganization
from weio.rest.serializers.products import PrivateProductSerializers


class PostProductCreate(CreateAPIView):
    serializer_class = PrivateProductSerializers
    permission_classes = [IsOrganization]
