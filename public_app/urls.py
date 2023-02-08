from django.urls import path, include
from . import views

app_name = 'global'
urlpatterns = [
    path('tenant/<str:tenant_url>/availability/check/', views.TenantAvailabilityCheckView.as_view(),
         name='tenant.available.check'),
    path('products/', views.ProductListView.as_view(), name='products.list')
]
