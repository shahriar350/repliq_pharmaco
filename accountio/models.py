from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models

from core.utils import PreModel
from weio.rest.choices import MERCHANT_ROLE_CHOICES

User = get_user_model()


class Domain(PreModel):
	url = models.CharField(max_length=255)
	slug = AutoSlugField(populate_from='url', editable=False, unique=True)

	def __str__(self):
		return f'{self.url}'


class Organization(PreModel):
	name = models.CharField(max_length=255)
	slug = AutoSlugField(populate_from='name', unique=True)
	kind = models.CharField(
		max_length=255, db_index=True
	)
	tax_number = models.CharField(max_length=255, null=True, blank=True)
	registration_no = models.CharField(max_length=50, blank=True, null=True)
	# Links to other external urls
	website_url = models.CharField(max_length=255, blank=True, null=True)
	blog_url = models.CharField(max_length=255, blank=True, null=True)
	linkedin_url = models.CharField(max_length=255, blank=True, null=True)
	instagram_url = models.CharField(max_length=255, blank=True, null=True)
	facebook_url = models.CharField(max_length=255, blank=True, null=True)
	twitter_url = models.CharField(max_length=255, blank=True, null=True)
	summary = models.TextField(blank=True, null=True, help_text="Short summary about company.")
	description = models.TextField(
		blank=True, null=True, help_text="Longer description about company."
	)

	@property
	def get_domains(self):
		return Domain.objects.filter(id__in=self.organizationdomain_set.values_list('domain_id'))


class OrganizationUser(PreModel):
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	# only merchant owner can create organization staff or admin and merchant owner id should be in here
	parent = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='get_descendant', null=True,
							   blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	role = models.CharField(choices=MERCHANT_ROLE_CHOICES, max_length=20)
	is_default = models.BooleanField(default=False)

	class Meta:
		unique_together = ('organization', 'user',)


class OrganizationDomain(PreModel):
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	domain = models.OneToOneField(Domain, on_delete=models.CASCADE)
