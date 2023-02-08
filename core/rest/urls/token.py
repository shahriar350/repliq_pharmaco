from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ..views import otp

app_name = 'token'

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', otp.LogoutView.as_view(), name='logout'),
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair')
]
