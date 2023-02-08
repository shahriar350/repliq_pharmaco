from django.contrib import admin

from addressio.models import Address


# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = [
        'uid',
        'district',
        'country',
    ]