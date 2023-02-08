from django.urls import path
from ..views import orders

app_name = 'orders'

urlpatterns = [
    path('', orders.ListCreateOrder.as_view(), name='list.create'),
]
