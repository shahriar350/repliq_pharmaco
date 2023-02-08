from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.rest.serializers.OTP import OTPLoginSerializer
from core.rest.serializers.auth import LogoutRefreshSerializer
from core.utils import create_token
from otpio.models import UserOTP


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

    @extend_schema(
        methods=['post'],
        request=OTPLoginSerializer,
        responses={200: OTPLoginSerializer, 400: None},
    )
    def post(self, request, *args, **kwargs):
        res = super(LoginOTPCheckRegister, self).create(request=request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data=res.data)


class LogoutView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutRefreshSerializer

    @extend_schema(
        responses={
            204: OpenApiResponse(description='Logout successfully.'),
            400: OpenApiResponse(description='Bad request'),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
