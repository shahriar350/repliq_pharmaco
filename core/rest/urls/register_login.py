from django.urls import path, include
from ..views import register

app_name = 'register_login'

urlpatterns = [
    path('registration/', register.PostUserRegistration.as_view(), name='user.registration')
]
