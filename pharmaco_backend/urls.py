from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('api/', include([
                      path('v1/', include([
                          path('auth/', include('auth_app.urls')),
                          path('superadmin/', include('admin_app.urls')),
                          path('public/', include('public_app.urls')),
                          path('customer/', include('customer_app.urls')),
                          path('otp/', include('otp_app.urls')),
                          path('merchant/', include('merchant_app.urls')),
                          path('search/', include('search_app.urls')),
                      ]))
                  ])),

                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
