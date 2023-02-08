from dirtyfields import DirtyFieldsMixin
from django.contrib.auth import get_user_model
from django.db import models
from autoslug import AutoSlugField
from django.db.models import Q

from pharmaco_backend.utils import PreModel

User = get_user_model()


# Create your models here.
class Category(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=100, verbose_name='Category name')
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='subcategories')

    def __str__(self):
        return self.name


# class Attribute(DirtyFieldsMixin, PreModel):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name

class Brand(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class Ingredient(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class Manufacturer(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class Supplier(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class MedicinePhysicalState(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class RouteOfAdministration(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class District(DirtyFieldsMixin, PreModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DeliveryCharge(DirtyFieldsMixin, PreModel):
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    district = models.OneToOneField(District, on_delete=models.CASCADE, related_name='get_delivery_charge')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_admin_delivery_charge',
                              limit_choices_to=Q(superuser=True) | Q(admin=True) | Q(staff=True), blank=True)
