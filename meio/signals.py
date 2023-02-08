from django.db.models.signals import pre_save
from django.dispatch import receiver

from orderio.models import CartProduct


@receiver(pre_save, sender=CartProduct)
def add_organization_to_cartproduct(sender, instance, **kwargs):
    instance.organization = instance.product.organization
