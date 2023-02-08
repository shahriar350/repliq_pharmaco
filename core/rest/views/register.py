from rest_framework.generics import CreateAPIView

from core.rest.serializers.auth import PublicUserRegistrationSerializer


class PostUserRegistration(CreateAPIView):
    serializer_class = PublicUserRegistrationSerializer
