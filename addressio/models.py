from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models

from addressio.utils import get_address_slug
from core.utils import PreModel

# Create your models here.
User = get_user_model()


class Address(PreModel):
    label = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from=get_address_slug, editable=False, unique=True)
    house = models.CharField(verbose_name="House number", max_length=255, null=True, blank=True)
    street = models.CharField(verbose_name="Street name", max_length=255, null=True, blank=True)
    post_office = models.CharField(verbose_name="Post office name", max_length=255)
    police_station = models.CharField(verbose_name="Police station name", max_length=255)
    district = models.ForeignKey('core.District', on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(verbose_name="Country name", max_length=255, default="BD")
    state = models.CharField(verbose_name="State name", max_length=255, null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.post_office, self.police_station, self.district.name)


class UserAddress(PreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)


class OrganizationAddress(PreModel):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
