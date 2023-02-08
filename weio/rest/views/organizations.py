from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accountio.models import OrganizationUser
from core.models import User
from weio.rest.permissions import IsOrganization, IsOrganizationAdmin
from weio.rest.serializers.organizations import PrivateOrganizationSerializer, PrivateOrganizationDefaultSerializer


class PostUserOrganization(CreateAPIView):
	serializer_class = PrivateOrganizationSerializer
	permission_classes = [IsOrganizationAdmin]

	def perform_create(self, serializer):
		role = serializer.validated_data.get('role', None)
		if role and role == 'owner' and serializer.validated_data.get('user').get_my_organization_role() != 'owner':
			raise ValidationError("Unauthorized access", code=422)
		if role and (role == 'admin' or role == 'staff') and serializer.validated_data.get(
				'user').get_my_organization_role() == 'staff':
			raise ValidationError("Unauthorized access", code=422)
		serializer.save()
		return serializer


class PostOrganizationDefault(CreateAPIView):
	serializer_class = PrivateOrganizationDefaultSerializer
	permission_classes = (IsOrganization,)

	def perform_create(self, serializer):
		merchant = serializer.validated_data.get('merchant')
		organization = serializer.validated_data.get('organization')
		target_organization = get_object_or_404(merchant.organizationuser_set.filter(), organization=organization)
		target_organization.is_default = True
		target_organization.save()

	@extend_schema(
		responses={
			200: None,
		}
	)
	def post(self, request, *args, **kwargs):
		super().create(request, *args, **kwargs)
		return Response(status=200)
