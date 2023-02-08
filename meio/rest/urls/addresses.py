from django.urls import path
from ..views import addresses

app_name = 'addresses'

urlpatterns = [
    path('<slug:slug>/', addresses.UpdateDeleteAddress.as_view(), name='retrieve.update.delete'),
    path('', addresses.ListPostAddress.as_view(), name='list.post'),
]
