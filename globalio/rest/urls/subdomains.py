from django.urls import path, include
from ..views import domains

app_name = 'domains'

urlpatterns = [
    path('<slug:slug>/', domains.CheckDomainAvailability.as_view(), name='check.availability')
]
