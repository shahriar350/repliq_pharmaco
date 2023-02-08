from django.urls import path
from ..views import organizations

app_name = 'organizations'

urlpatterns = [
	path('', organizations.PostSendRequestForOrganization.as_view(), name='request')
]
