from django.db import models
from versatileimagefield.fields import PPOIField, VersatileImageField

from core.utils import PreModel


# Create your models here.
class MediaImage(PreModel):
    image = VersatileImageField(
        width_field="width",
        height_field="height",
        ppoi_field="ppoi",
    )
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    ppoi = PPOIField()
    caption = models.CharField(max_length=100, blank=True, null=True)
    copyright = models.CharField(max_length=100, blank=True, null=True)
    priority = models.BigIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)
