from django.urls import path
from ..views import organizations

app_name = 'organizations'

urlpatterns = [
    path('user/', organizations.PostUserOrganization.as_view(), name='create.user'),
    path('default/', organizations.PostOrganizationDefault.as_view(), name='default'),
]
