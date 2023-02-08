from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    path('category/', views.CategoryListCreateView.as_view(), name='category.list.create'),
    path('category/<uuid:uuid>/', views.CategoryRetrieveUpdateRemoveView.as_view(),
         name='category.retrieve.update.remove'),
    # path('category/<int:id>/', views.CategoryRemove.as_view(), name='category.remove'),
    # path('category/delete/<int:id>/', views.CategoryDelete.as_view(), name='category.delete'),

    # path('attribute/',views.AttributeListCreateView.as_view(),name='attribute.list.create'),
    # path('attribute/<int:pk>/',views.AttributeRetrieveUpdateView.as_view(),name='attribute.retrieve.update'),
    # path('attribute/<int:id>/',views.AttributeRemove.as_view(),name='attribute.remove'),
    # path('attribute/delete/<int:id>/',views.AttributeDelete.as_view(),name='attribute.delete'),

    path('brand/', views.BrandListCreateView.as_view(), name='brand.list.create'),
    path('brand/<uuid:uuid>/', views.BrandRetrieveUpdateRemoveView.as_view(), name='brand.retrieve.update.remove'),
    # path('brand/<int:id>/', views.BrandRemove.as_view(), name='brand.remove'),
    # path('brand/delete/<int:id>/', views.BrandDelete.as_view(), name='brand.delete'),

    path('ingredient/', views.IngredientListCreateView.as_view(), name='ingredient.list.create'),
    path('ingredient/<uuid:uuid>/', views.IngredientRetrieveUpdateRemoveView.as_view(),
         name='ingredient.retrieve.update.remove'),
    # path('ingredient/<int:id>/', views.IngredientRemove.as_view(), name='ingredient.remove'),
    # path('ingredient/delete/<int:id>/', views.IngredientDelete.as_view(), name='ingredient.delete'),

    path('manufacturer/', views.ManufacturerListCreateView.as_view(), name='manufacturer.list.create'),
    path('manufacturer/<uuid:uuid>/', views.ManufacturerRetrieveUpdateRemoveView.as_view(),
         name='manufacturer.retrieve.update.remove'),
    # path('manufacturer/<int:id>/', views.ManufacturerRemove.as_view(), name='manufacturer.remove'),
    # path('manufacturer/delete/<int:id>/', views.ManufacturerDelete.as_view(), name='manufacturer.delete'),

    path('supplier/', views.SupplierListCreateView.as_view(), name='supplier.list.create'),
    path('supplier/<uuid:uuid>/', views.SupplierRetrieveUpdateRemoveView.as_view(),
         name='supplier.retrieve.update.remove'),
    # path('supplier/<int:id>/', views.SupplierRemove.as_view(), name='supplier.remove'),
    # path('supplier/delete/<int:id>/', views.SupplierDelete.as_view(), name='supplier.delete'),

    path('medicinePhysicalState/', views.MedicinePhysicalStateListCreateView.as_view(),
         name='medicinePhysicalState.list.create'),
    path('medicinePhysicalState/<uuid:uuid>/', views.MedicinePhysicalStateRetrieveUpdateRemoveView.as_view(),
         name='medicinePhysicalState.retrieve.update.remove'),
    # path('medicinePhysicalState/<int:id>/', views.MedicinePhysicalStateRemove.as_view(),
    #          name='medicinePhysicalState.remove'),
    # path('medicinePhysicalState/delete/<int:id>/', views.MedicinePhysicalStateDelete.as_view(), name='medicinePhysicalState.delete'),

    path('routeOfAdministration/', views.RouteOfAdministrationListCreateView.as_view(),
         name='routeOfAdministration.list.create'),
    path('routeOfAdministration/<uuid:uuid>/', views.RouteOfAdministrationRetrieveUpdateRemoveView.as_view(),
         name='routeOfAdministration.retrieve.update.remove'),
    # path('routeOfAdministration/<int:id>/', views.RouteOfAdministrationRemove.as_view(),
    #      name='routeOfAdministration.remove'),
    # path('routeOfAdministration/delete/<int:id>/', views.RouteOfAdministrationDelete.as_view(), name='routeOfAdministration.delete'),

    # product add start
    # path('product/create/',views.ProductCreateView.as_view(),name='product.create')
    # product add end
    # admin login
    path('auth/login/', views.AdminLoginView.as_view(), name='auth.login'),

    # product
    path('productbase/', views.BaseProductCreateView.as_view(), name='product.base.create'),
    path('baseproduct/<uuid:uuid>/', views.BaseProductRetrieveUpdateDeleteView.as_view(),
         name='product.base.retrieve.update.delete'),
    # Superuser registration
    path('superuser/register/', views.SuperUserRegisterCreateView.as_view(), name='superuser.register'),
]
