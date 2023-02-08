from autoslug import AutoSlugField
from dirtyfields import DirtyFieldsMixin
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from versatileimagefield.fields import PPOIField, VersatileImageField

from admin_app.models import Category, Ingredient, Manufacturer, Brand, Supplier, RouteOfAdministration, \
    MedicinePhysicalState
from client_app.models import Tenant
from pharmaco_backend.utils import PreModel

User = get_user_model()


# Create your models here.

class BaseProduct(DirtyFieldsMixin, PreModel):
    '''
    the product which is created by superadmin is the main base product where merchant can inherit
    but if superadmin is null means that product is created by merchant which is not shown to merchant for suggestion,
     that product only for that merchant.

     we use merchant_product for track down the merchant product we can easily get the merchant product from here without making complex queries.
     merchant_slug: when a owner/admin of merchant want to see whole data for that merchant table, he can use easily from here to make a simple query.

    '''
    superadmin = models.ForeignKey(User, related_name='get_admin_products', on_delete=models.SET_NULL, null=True,
                                   blank=True, limit_choices_to=Q(admin=True) | Q(superuser=True))
    merchant_product = models.OneToOneField('product_app.Product', related_name='get_base_product',
                                            on_delete=models.SET_NULL, null=True,
                                            blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, related_name="get_category_baseproducts")
    active_ingredient = models.ManyToManyField(Ingredient, related_name='get_ingredient_baseproducts')
    dosage_form = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, related_name="get_manufacturer_baseproducts",
                                     on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name="get_brand_baseproducts",
                              on_delete=models.SET_NULL, null=True, blank=True)
    route_of_administration = models.ForeignKey(RouteOfAdministration,
                                                related_name='get_routeofadministration_products',
                                                null=True,
                                                blank=True, on_delete=models.SET_NULL)
    medicine_physical_state = models.ForeignKey(MedicinePhysicalState,
                                                related_name='get_medicinephysicalstate_products',
                                                null=True,
                                                blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Product(DirtyFieldsMixin, PreModel):
    base_product = models.ForeignKey(BaseProduct, related_name="get_baseproduct_products", on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, related_name='get_merchant_products', on_delete=models.CASCADE)
    merchant_domain = models.ForeignKey(Tenant, on_delete=models.CASCADE,
                                        related_name='get_tenant_products')
    slug = AutoSlugField(populate_from="get_product_name",
                         unique_with=['base_product__name'], editable=False, unique=True)
    stock = models.PositiveIntegerField(default=0)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def get_product_name(self):
        return self.base_product.name

    # class Inventory(DirtyFieldsMixin, PreModel):
    #     product = models.ForeignKey(Product, related_name='get_product_inventory', on_delete=models.CASCADE)
    #     supplier = models.ForeignKey(Supplier, related_name='get_supplier_inventories', on_delete=models.SET_NULL,
    #                                  null=True, blank=True)
    #     quantity = models.PositiveIntegerField()
    #     cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #     expired_date = models.DateField(null=True, blank=True)
    #     additional_information = models.CharField(max_length=255, null=True, blank=True)


class ProductImage(DirtyFieldsMixin, PreModel):
    product = models.ForeignKey(Product, related_name='get_product_images', on_delete=models.CASCADE, null=True,
                                blank=True)
    base_product = models.ForeignKey(BaseProduct, related_name='get_baseproduct_images', on_delete=models.CASCADE,
                                     null=True, blank=True)
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


# class ProductVariation(DirtyFieldsMixin, PreModel):
#     product = models.ForeignKey(Product, related_name='get_product_variation_prices', on_delete=models.CASCADE)
#     buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     variation_name = models.CharField(null=True, blank=True, max_length=255,
#                                       verbose_name='table could be used to store the labels "5mg Oral", "10mg Oral" etc.')
#     image = VersatileImageField(
#         'Image',
#         width_field='width',
#         height_field='height',
#         ppoi_field='ppoi'
#     )
#     height = models.PositiveIntegerField(
#         'Image Height',
#         blank=True,
#         null=True
#     )
#     width = models.PositiveIntegerField(
#         'Image Width',
#         blank=True,
#         null=True
#     )
#     ppoi = PPOIField(
#         'Image PPOI'
#     )
#
#
# class ProductVariationAttribute(DirtyFieldsMixin, PreModel):
#     product_variation = models.ForeignKey(ProductVariation,
#                                           related_name='get_productvariation_attributes',
#                                           on_delete=models.CASCADE)
#     attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL,
#                                   related_name="get_attribute_productvariationattribute",
#                                   null=True, blank=True)
#     attribute_value = models.CharField(max_length=255)
# class DeliveryMethod(DirtyFieldsMixin, PreModel):
#     police = models.OneToOneField(PoliceStation, on_delete=models.CASCADE, related_name='get_station_delivery_method',
#                                   null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=100)
