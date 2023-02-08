from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from meio.rest.serializers.organizations import PublicOrganization


class PostSendRequestForOrganization(CreateAPIView):
	serializer_class = PublicOrganization
	permission_classes = [IsAuthenticated]
