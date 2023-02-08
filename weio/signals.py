from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accountio.models import OrganizationUser


@receiver(pre_save, sender=OrganizationUser)
def organizationuser_update_all_isdefault_organization(sender, instance, *args, **kwargs):
    if instance.is_default:
        OrganizationUser.objects.filter(Q(user=instance.user) & Q(is_default=True)).update(is_default=False)
