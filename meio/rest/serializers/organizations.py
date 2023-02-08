from rest_framework import serializers

from accountio.models import Organization, OrganizationUser


class PublicOrganization(serializers.Serializer):
	name = serializers.CharField(max_length=255, write_only=True)
	kind = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	tax_number = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	registration_no = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	website_url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	blog_url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	linkedin_url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	instagram_url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	facebook_url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	twitter_url = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	summary = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	description = serializers.CharField(max_length=255, allow_null=True, allow_blank=True, write_only=True)
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	def create(self, validated_data):
		user = validated_data.pop('user')
		organization = Organization.objects.create(**validated_data, active=False)
		a = OrganizationUser.objects.create(
			organization=organization,
			user=user,
			role='owner',
			active=False
		)
		return validated_data
