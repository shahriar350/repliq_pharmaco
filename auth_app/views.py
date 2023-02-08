from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from auth_app.documentation_serializers import LogoutRefreshSerializer
from merchant_app.documentation_serializers import MerchantRegisterResponse200Serializer
from otp_app.models import UserOTP
from auth_app.serializers import OTPLoginSerializer
from django.utils import timezone

User = get_user_model()


# Create your views here.
def create_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh), str(refresh.access_token)  # first return refresh_token and second one is access_token


@extend_schema(
    summary="All user can check OTP here",
    responses={
        200: OpenApiResponse(response=MerchantRegisterResponse200Serializer,
                             description='A otp will sent to user phone if user is a user.'),
        400: OpenApiResponse(description='Bad request'),
    },
)
class LoginOTPCheckRegister(CreateAPIView):
    serializer_class = OTPLoginSerializer

    def perform_create(self, serializer):
        get_otp = serializer.validated_data.get('otp')

        otp = UserOTP.objects.filter(otp=get_otp)
        if otp.exists():
            otp = otp.first()
            valid_time = otp.validate_time
            if timezone.now() <= valid_time:
                serializer.validated_data['refresh_token'], serializer.validated_data['access_token'] = create_token(
                    otp.user)
                return serializer
            raise ValidationError("Invalid OTP.")

    def post(self, request, *args, **kwargs):
        res = super(LoginOTPCheckRegister, self).create(request=request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data=res.data)


class LogoutView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutRefreshSerializer

    @extend_schema(
        summary="All user can check OTP here",
        responses={
            205: OpenApiResponse(description='Logout successfully.'),
            400: OpenApiResponse(description='Bad request'),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
