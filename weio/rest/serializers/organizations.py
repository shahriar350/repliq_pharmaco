from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers, renderers
from rest_framework.exceptions import ValidationError

from accountio.models import Organization, OrganizationUser
from core.models import User
from weio.rest.choices import MERCHANT_ROLE_CHOICES
from phonenumber_field.serializerfields import PhoneNumberField


# User = get_user_model()


class PrivateOrganizationSerializer(serializers.Serializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	role = serializers.ChoiceField(choices=MERCHANT_ROLE_CHOICES)
	name = serializers.CharField()
	phone = PhoneNumberField()
	password = serializers.CharField(max_length=255)

	def create(self, validated_data):
		with transaction.atomic():
			organization = validated_data.get('user').get_organization()
			phone = validated_data.get('phone')
			owner_user = validated_data.get('user')
			try:
				user = User.objects.get(phone=phone)
			except User.DoesNotExist:
				user = User.objects.create_user(name=validated_data.get('name'), phone=phone,
												password=validated_data.get('password'))
			role = validated_data.get('role')
			organization_set = OrganizationUser.objects.filter(
				organization=organization,
				user=user,
			)
			if organization_set.exists():
				raise ValidationError("This user is already added to your current organization.")
			else:
				OrganizationUser.objects.create(
					organization=organization,
					user=user,
					parent=owner_user,
					role=role,
				)

		return validated_data


class PrivateOrganizationDefaultSerializer(serializers.Serializer):
	organization = serializers.SlugRelatedField(
		queryset=Organization.objects.filter(active=True, deleted_at__isnull=True), slug_field='uid', write_only=True)
	merchant = serializers.HiddenField(default=serializers.CurrentUserDefault())
