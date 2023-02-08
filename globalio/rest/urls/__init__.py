from django.urls import path, include

app_name = 'global'

urlpatterns = [
    path('domains/', include('globalio.rest.urls.subdomains'))
]
