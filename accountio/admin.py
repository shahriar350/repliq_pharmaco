from django.contrib import admin

from addressio.models import OrganizationAddress
from core.forms import UserCreationForm
from mediaroomio.models import MediaImage
from accountio.models import Organization, Domain, OrganizationDomain


# Register your models here.
class OrganizationDomainInlineAdmin(admin.TabularInline):
    model = OrganizationDomain
    fk_name = 'organization'


class OrganizationAddressInlineAdmin(admin.TabularInline):
    model = OrganizationAddress
    fk_name = 'organization'


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = [
        'uid',
        'name',
    ]
    inlines = (
        OrganizationDomainInlineAdmin,
        OrganizationAddressInlineAdmin
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    model = Domain
    list_display = [
        'uid',
        'url',
    ]
