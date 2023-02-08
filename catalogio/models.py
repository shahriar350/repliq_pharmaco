from django.contrib.auth import get_user_model
from django.db import models
from autoslug import AutoSlugField
from django.db.models import Q

from catalogio.utils import get_product_slug
from core.models import District
from core.utils import PreModel

User = get_user_model()


# Create your models here.
class Category(PreModel):
    name = models.CharField(max_length=100, verbose_name='Category name')
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='subcategories')
    image = models.ForeignKey("mediaroomio.MediaImage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)
    image = models.ForeignKey("mediaroomio.MediaImage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Ingredient(PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class Manufacturer(PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class Supplier(PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class MedicinePhysicalState(PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class RouteOfAdministration(PreModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', editable=False, unique=True)

    def __str__(self):
        return self.name


class DeliveryCharge(PreModel):
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    district = models.OneToOneField(District, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE,
                              limit_choices_to=Q(is_superuser=True) | Q(is_staff=True), blank=True)

    def __str__(self):
        return f'{self.district.name}: {self.charge}'


# Product

class BaseProduct(PreModel):
    '''
    the product which is created by superadmin is the main base product where merchant can inherit
    but if superadmin is null means that product is created by merchant which is not shown to merchant for suggestion,
     that product only for that merchant.

     we use merchant_product for track down the merchant product we can easily get the merchant product from here without making complex queries.
     merchant_slug: when a owner/admin of merchant want to see whole data for that merchant table, he can use easily from here to make a simple query.

    '''
    superadmin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   blank=True,
                                   limit_choices_to=Q(is_superuser=True) | Q(is_staff=True))
    merchant_product = models.OneToOneField('catalogio.Product',
                                            on_delete=models.SET_NULL, null=True,
                                            blank=True)

    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    active_ingredients = models.ManyToManyField(Ingredient, blank=True)
    dosage_form = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer,
                                     on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand,
                              on_delete=models.SET_NULL, null=True, blank=True)
    route_of_administration = models.ForeignKey(RouteOfAdministration,
                                                null=True,
                                                blank=True, on_delete=models.SET_NULL)
    medicine_physical_state = models.ForeignKey(MedicinePhysicalState,
                                                null=True,
                                                blank=True, on_delete=models.SET_NULL)
    image = models.ForeignKey("mediaroomio.MediaImage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(PreModel):
    @property
    def product_name(self):
        return self.base_product.name

    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='get_products')
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=get_product_slug, editable=False, unique=True)
    stock = models.PositiveIntegerField(default=0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    merchant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 blank=True)  # only merchant who create this product
    image = models.ForeignKey("mediaroomio.MediaImage", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.base_product.name


class ProductImage(PreModel):
    base_product = models.ForeignKey(BaseProduct, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ForeignKey("mediaroomio.MediaImage", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.base_product.name or self.base_product.name
