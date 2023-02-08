from django.urls import path, include
from . import views

app_name = 'merchant'

urlpatterns = [
    path('auth/login/', views.MerchantLogin.as_view(), name='auth.login'),
    path('owner/auth/register/', views.MerchantRegister.as_view(), name='auth.register'),
    path('auth/info/add/', views.MerchantInfoAddView.as_view(), name='auth.info.add'),

    path('auth/create/staff/', views.AuthCreateMerchantAdminView.as_view(), name="auth.create.admin"),
    path('auth/check/', views.MerchantAuthCheckView.as_view(), name="auth.check"),

    # product for merchant
    path('product/', views.AddProductView.as_view(), name="product.create"),
    path('product/<slug:product_slug>/', views.UpdateDestroyProductInfoView.as_view(), name="product.update.destroy"),
    path('product/<slug:product_slug>/image/', views.AddImageProductView.as_view(), name="product.add.image"),
    path('product/<uuid:product_uuid>/image/<uuid:image_uuid>/', views.RemoveImageFromProductView.as_view(),
         name="product.remove.image"),
    # path('product/<slug:slug>/', views.RemoveProductInfoView.as_view(), name="product.remove"),
    path('product/<slug:product_slug>/restore/', views.RestoreProductInfoView.as_view(), name="product.restore"),

]
