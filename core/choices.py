from django.db import models


class OrganizationUserRole(models.TextChoices):
    INITIATOR = "INITIATOR", "Initiator"
    STAFF = "STAFF", "Staff"
    ADMIN = "ADMIN", "Admin"
    OWNER = "OWNER", "Owner"
