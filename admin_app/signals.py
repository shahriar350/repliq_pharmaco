from django.db.models.signals import pre_save
from django.dispatch import receiver

from admin_app.models import Category, Brand, Ingredient, Manufacturer, Supplier
from pharmaco_backend.utils import create_slug


# @receiver(pre_save, sender=Category)
# def category_admin(sender, instance, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance, instance.name)
#
#
# @receiver(pre_save, sender=Brand)
# def brand_admin(sender, instance, **kwargs):
#     if instance.pk is None:
#         instance.slug = create_slug(instance, instance.name)
#
# @receiver(pre_save, sender=Ingredient)
# def ingredient_admin(sender, instance, **kwargs):
#     if instance.pk is None:
#         instance.slug = create_slug(instance, instance.name)
#
#
# @receiver(pre_save, sender=Manufacturer)
# def manufacturer_admin(sender, instance, **kwargs):
#     if instance.pk is None:
#         instance.slug = create_slug(instance, instance.name)
#
#
# @receiver(pre_save, sender=Supplier)
# def supplier_admin(sender, instance, **kwargs):
#     if instance.pk is None:
#         instance.slug = create_slug(instance, instance.name)
