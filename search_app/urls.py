from django.urls import path, include
from . import views

app_name = 'search'

urlpatterns = [
    path('base/products/', views.BaseProductSearchView.as_view(), name='base.products'),
    path('category/', views.CategorySearchView.as_view(), name='category'),
    path('brand/', views.BrandSearchView.as_view(), name='brand'),
    path('ingredient/', views.IngredientSearchView.as_view(), name='ingredient'),
    path('manufacturer/', views.ManufacturerSearchView.as_view(), name='manufacturer'),
    path('supplier/', views.SupplierSearchView.as_view(), name='supplier'),
    path('medicinephysicalstate/', views.MedicinePhysicalStateSearchView.as_view(), name='medicinephysicalstate'),
    path('routeofadministration/', views.RouteOfAdministrationSearchView.as_view(), name='routeofadministration'),

]
