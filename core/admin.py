from django.contrib import admin
from django.contrib.auth import get_user_model

from accountio.models import OrganizationUser
from core.forms import UserCreationForm

# Register your models here.
User = get_user_model()


class OrganizationUserInline(admin.TabularInline):
    model = OrganizationUser
    fk_name = 'user'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = [
        'uid',
        'name',
        'phone',
    ]
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ("Other", {'fields': ('name', 'image', 'is_active', 'is_verified')}),
        ("Only for Superuser", {'fields': ('is_superuser', 'is_staff')}),
        ("Groups and Permissions", {'fields': ('groups', 'user_permissions')}),
    )
    list_filter = [
        'is_superuser',
        'is_active',
        'is_staff',
    ]
    form = UserCreationForm
    inlines = (
        OrganizationUserInline,
    )
