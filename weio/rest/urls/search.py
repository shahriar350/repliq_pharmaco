from django.urls import path, include
from ..views import search

app_name = 'search'
urlpatterns = [
    path('product/', search.GetBaseProductSearch.as_view(), name='base.product'),

]
