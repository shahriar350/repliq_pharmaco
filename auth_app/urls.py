from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenRefreshSlidingView

from . import views

app_name = 'auth'

urlpatterns = [
    path('login/otp/check/', views.LoginOTPCheckRegister.as_view(), name='login.otp.check'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/logout/', views.LogoutView.as_view(), name='logout'),
]
