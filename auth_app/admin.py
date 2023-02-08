from django.contrib import admin
from django.contrib.auth import get_user_model

from auth_app.models import MerchantInformation, UserAddress

# Register your models here.
User = get_user_model()


class MerchantInformationInline(admin.StackedInline):
    model = MerchantInformation
    fk_name = "user"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = [
        'uuid',
        'name',
        'phone_number',
    ]
    list_filter = [
        'superuser',
        'admin',
        'active',
        'merchant',
        'staff',
    ]
    inlines = (MerchantInformationInline,)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    model = UserAddress
    list_display = [
        'uuid',
        'label',
        'district',
    ]
    list_filter = [
        'active',
    ]
