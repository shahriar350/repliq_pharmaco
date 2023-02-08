from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accountio.models import Domain


class CheckDomainAvailability(APIView):
    @extend_schema(
        responses={
            200: None,
            204: None
        },
    )
    def get(self, request, slug=None):
        try:
            Domain.objects.get(slug=slug)
        except Domain.DoesNotExist:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
