from dirtyfields import DirtyFieldsMixin
from django.db import models

from pharmaco_backend.utils import PreModel


# Create your models here.
class Tenant(DirtyFieldsMixin, PreModel):
    url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.url
