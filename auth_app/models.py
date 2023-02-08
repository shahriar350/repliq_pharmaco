from dirtyfields import DirtyFieldsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models
from django.db.models import Q
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField, PPOIField
from autoslug import AutoSlugField

from client_app.models import Tenant
from pharmaco_backend.utils import PreModel
import uuid


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, name, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValidationError(_('Phone number is required'))
        if not password:
            raise ValidationError(_('Password is required'))
        extra_fields.setdefault("active", True)
        extra_fields.setdefault("is_verified", True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.name = name.title()
        user.save(using=self._db)
        return user

    def create_merchant_owner(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault('merchant', True)
        extra_fields.setdefault('active', True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        merchant, _ = Group.objects.get_or_create(name="merchant_owner")
        user.groups.add(merchant)
        return user

    def create_merchant_admin(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault('merchant', True)
        extra_fields.setdefault('active', True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        merchant, _ = Group.objects.get_or_create(name="merchant_admin")
        user.groups.add(merchant)
        return user

    def create_merchant_staff(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault('merchant', True)
        extra_fields.setdefault('active', True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        merchant, _ = Group.objects.get_or_create(name="merchant_staff")
        user.groups.add(merchant)
        return user

    def create_superuser(self, name, phone_number, password, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("admin", True)
        extra_fields.setdefault("active", True)
        user = self.create_user(name, phone_number, password, **extra_fields)
        return user


class Users(DirtyFieldsMixin, AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "users"

    name = models.CharField(_('Your name'), max_length=100)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4())
    phone_number = PhoneNumberField(blank=True, unique=True)
    superuser = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    merchant = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    merchant_accepted_by_superadmin = models.ForeignKey('self', related_name='get_user_merchants',
                                                        on_delete=models.SET_NULL,
                                                        null=True,
                                                        blank=True,
                                                        limit_choices_to=Q(superuser=True) | Q(admin=True))
    image = VersatileImageField(
        'Image',
        width_field='width',
        height_field='height',
        ppoi_field='ppoi'
    )
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    ppoi = PPOIField(
        'Image PPOI'
    )
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def is_merchant(self):
        return self.groups.filter(
            Q(name="merchant_owner") | Q(name="merchant_admin") | Q(name="merchant_staff")).exists() | False

    def __str__(self):
        return str(self.phone_number)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


class MerchantInformation(DirtyFieldsMixin, PreModel):
    user = models.OneToOneField(Users, related_name="get_user_information", on_delete=models.CASCADE,
                                limit_choices_to={'merchant': True})
    slug = AutoSlugField(unique_with='user__name', editable=False, unique=True)
    merchant_domain = models.ForeignKey(Tenant, related_name="get_tenant_users", on_delete=models.SET_NULL, null=True,
                                        blank=True)
    merchant_parent_who_created = models.ForeignKey(Users, related_name='get_merchant_children',
                                                    on_delete=models.SET_NULL,
                                                    verbose_name="only merchant id can be here because only merchant can create their children like admin or staff.",
                                                    null=True,
                                                    limit_choices_to={'merchant': True},
                                                    blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    tax_number = models.CharField(max_length=255, null=True, blank=True)
    tax_type = models.CharField(max_length=255, null=True, blank=True)


class UserAddress(DirtyFieldsMixin, PreModel):
    user = models.ForeignKey(Users, related_name="get_user_addresses", on_delete=models.SET_NULL, null=True,
                             blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='user_name', unique_with='user__name', editable=False, unique=True)
    house = models.CharField(verbose_name="House number", max_length=255, null=True, blank=True)
    street = models.CharField(verbose_name="Street name", max_length=255, null=True, blank=True)
    post_office = models.CharField(verbose_name="Post office name", max_length=255)
    police_station = models.CharField(verbose_name="Police station name", max_length=255)
    district = models.ForeignKey('admin_app.District', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='get_district_user_addresses')
    country = models.CharField(verbose_name="Country name", max_length=255)
    state = models.CharField(verbose_name="State name", max_length=255, null=True, blank=True)

    @property
    def user_name(self):
        return self.user.name
