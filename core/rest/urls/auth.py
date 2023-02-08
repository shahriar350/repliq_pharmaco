from django.urls import path, include

app_name = 'auth'

urlpatterns = [
    path('token/', include('core.rest.urls.token')),
    path('', include('core.rest.urls.register_login')),
]
