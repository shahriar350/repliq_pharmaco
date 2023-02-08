from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, AbstractUser
from django.db import models
from django.db.models import Q
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.contrib import auth
from core.utils import PreModel


# Create your models here.

class CustomUserManager(BaseUserManager):
	def create_user(self, name, phone, password, **extra_fields):
		if not phone:
			raise ValidationError(_('Phone number is required'))
		if not password:
			raise ValidationError(_('Password is required'))
		extra_fields.setdefault("is_active", True)
		extra_fields.setdefault("is_verified", True)
		user = self.model(phone=phone, **extra_fields)
		user.set_password(password)
		user.name = name.title()
		user.save(using=self._db)
		return user

	def create_superuser(self, name, phone, password, **extra_fields):
		extra_fields.setdefault("is_superuser", True)
		extra_fields.setdefault("is_staff", True)
		user = self.create_user(name, phone, password, **extra_fields)
		return user

	def with_perm(
			self, perm, is_active=True, include_superusers=True, backend=None, obj=None
	):
		if backend is None:
			backends = auth._get_backends(return_tuples=True)
			if len(backends) == 1:
				backend, _ = backends[0]
			else:
				raise ValueError(
					"You have multiple authentication backends configured and "
					"therefore must provide the `backend` argument."
				)
		elif not isinstance(backend, str):
			raise TypeError(
				"backend must be a dotted import path string (got %r)." % backend
			)
		else:
			backend = auth.load_backend(backend)
		if hasattr(backend, "with_perm"):
			return backend.with_perm(
				perm,
				is_active=is_active,
				include_superusers=include_superusers,
				obj=obj,
			)
		return self.none()


class User(AbstractBaseUser, PermissionsMixin, PreModel):
	class Meta:
		verbose_name_plural = "users"

	slug = AutoSlugField(populate_from='name', editable=False, unique=True)
	name = models.CharField(max_length=255)
	phone = PhoneNumberField(blank=True, unique=True, db_index=True)
	image = models.ForeignKey("mediaroomio.MediaImage", on_delete=models.SET_NULL, null=True, blank=True)

	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_verified = models.BooleanField(default=True)

	USERNAME_FIELD = "phone"
	REQUIRED_FIELDS = ('name',)
	objects = CustomUserManager()

	def __str__(self):
		return str(self.phone)

	def is_merchant(self):
		return self.organizationuser_set.exists()

	def get_organization(self):
		return self.organizationuser_set.get(is_default=True).organization or None

	def get_my_organization_role(self):
		return self.organizationuser_set.get(is_default=True).role or None


class District(PreModel):
	name = models.CharField(max_length=255)
	slug = AutoSlugField(populate_from='name', unique=True, editable=False)

	def __str__(self):
		return self.name


class PaymentMethod(PreModel):
	name = models.CharField(max_length=255)
	slug = AutoSlugField(populate_from='name', unique=True, editable=False)
