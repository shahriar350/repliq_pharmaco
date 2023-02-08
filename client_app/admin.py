from django.contrib import admin

from client_app.models import Tenant


# Register your models here.
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    model = Tenant
    list_display = [
        'uuid',
        'url',
    ]
    list_filter = [
        'active',
        ("deleted_at", admin.EmptyFieldListFilter),
    ]
