from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, status
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from auth_app.views import create_token
from pharmaco_backend.permissions import IsSuperAdminOrAdmin
from product_app.models import BaseProduct
from .serializers import (CategorySerializers,
                          BrandSerializers,
                          RouteOfAdministrationSerializers,
                          IngredientSerializers,
                          ManufacturerSerializers,
                          SupplierSerializers,
                          AdminBaseProductCreateUpdateSerializer,
                          BaseProductRetrieveSerializer,
                          MedicinePhysicalStateSerializers,
                          AdminLoginSerializer, SuperUserRegisterSerializer, BaseProductSerializer)

from .models import (Category, Brand, Ingredient,
                     Manufacturer, Supplier, MedicinePhysicalState,
                     RouteOfAdministration)

# Create your views here.


"""Views For Category Model"""


class CategoryListCreateView(generics.ListCreateAPIView):
    """List and Create Category"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class CategoryRetrieveUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve,Update and Patch Category"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# class CategoryRemove(generics.DestroyAPIView):
#     """Remove Category"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Category.objects.get(pk=self.kwargs.get('id'))

#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()


# class CategoryDelete(generics.DestroyAPIView):
#     """Delete Category"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Category.objects.get(pk=self.kwargs.get('id'))


"""Views For Brand Model"""


class BrandListCreateView(generics.ListCreateAPIView):
    """List and Create Brand"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers


class BrandRetrieveUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve,Update and Patch Brand"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# class BrandRemove(generics.DestroyAPIView):
#     """Remove Brand"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Brand.objects.get(id=self.kwargs.get(('id')))

#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()


# class BrandDelete(generics.DestroyAPIView):
#     """Delete Brand"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Brand.objects.get(id=self.kwargs.get('id'))


"""Views For Ingredient Model"""


class IngredientListCreateView(generics.ListCreateAPIView):
    """List and Create Ingredient"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers


class IngredientRetrieveUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve,Update and Patch Ingredient"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# class IngredientRemove(generics.DestroyAPIView):
#     """Remove Ingredient"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Ingredient.objects.get(pk=self.kwargs.get('id'))

#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()


# class IngredientDelete(generics.DestroyAPIView):
#     """Delete Ingredient"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Ingredient.objects.get(pk=self.kwargs.get('id'))


"""Views For Manufacturer Model"""


class ManufacturerListCreateView(generics.ListCreateAPIView):
    """List and Create Manufacturer"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializers


class ManufacturerRetrieveUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve,Update and Patch Manufacturer"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializers
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# class ManufacturerRemove(generics.DestroyAPIView):
#     """Remove Manufacturer"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Manufacturer.objects.get(pk=self.kwargs.get('id'))

#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()


# class ManufacturerDelete(generics.DestroyAPIView):
#     """Delete Manufacturer"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Manufacturer.objects.get(pk=self.kwargs.get('id'))


"""Views For Supplier Model"""


class SupplierListCreateView(generics.ListCreateAPIView):
    """List and Create Supplier"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers


class SupplierRetrieveUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve,Update and Patch Supplier"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializers
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# class SupplierRemove(generics.DestroyAPIView):
#     """Remove Supplier"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Supplier.objects.get(pk=self.kwargs.get('id'))

#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()


# class SupplierDelete(generics.DestroyAPIView):
#     """Delete Supplier"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return Supplier.objects.get(pk=self.kwargs.get('id'))


"""Views For MedicinePhysicalState Model"""


class MedicinePhysicalStateListCreateView(generics.ListCreateAPIView):
    """List and Create MedicinePhysicalState"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = MedicinePhysicalState.objects.all()
    serializer_class = MedicinePhysicalStateSerializers


class MedicinePhysicalStateRetrieveUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve,Update and Patch MedicinePhysicalState"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = MedicinePhysicalState.objects.all()
    serializer_class = MedicinePhysicalStateSerializers
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# class MedicinePhysicalStateRemove(generics.DestroyAPIView):
#     """Remove MedicinePhysicalState"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return MedicinePhysicalState.objects.get(pk=self.kwargs.get('id'))

#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()


# class MedicinePhysicalStateDelete(generics.DestroyAPIView):
#     """Delete MedicinePhysicalState"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return MedicinePhysicalState.objects.get(pk=self.kwargs.get('id'))


"""Views For RouteOfAdministration Model"""


class RouteOfAdministrationListCreateView(generics.ListCreateAPIView):
    """List and Create RouteOfAdministration"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = RouteOfAdministration.objects.all()
    serializer_class = RouteOfAdministrationSerializers


class RouteOfAdministrationRetrieveUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve,Update and Patch RouteOfAdministration"""

    permission_classes = [IsSuperAdminOrAdmin]
    queryset = RouteOfAdministration.objects.all()
    serializer_class = RouteOfAdministrationSerializers
    lookup_field = 'uuid'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


# class RouteOfAdministrationRemove(generics.DestroyAPIView):
#     """Remove RouteOfAdministration"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return RouteOfAdministration.objects.get(pk=self.kwargs.get('id'))

#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()


# class RouteOfAdministrationDelete(generics.DestroyAPIView):
#     """Delete RouteOfAdministration"""

#     permission_classes = [IsSuperAdminOrAdmin]

#     def get_serializer(self, *args, **kwargs):
#         return None

#     def get_object(self):
#         return RouteOfAdministration.objects.get(pk=self.kwargs.get('id'))


# class ProductCreateView:
#     pass
class AdminLoginView(generics.CreateAPIView):
    serializer_class = AdminLoginSerializer

    def perform_create(self, serializer):
        user = authenticate(username=serializer.validated_data.get('phone_number'),
                            password=serializer.validated_data.get('password'))
        if user and (user.admin or user.superuser):
            serializer.validated_data['refresh_token'], serializer.validated_data['access_token'] = create_token(user)
            return serializer
        else:
            raise ValidationError("Phone number or password or both are wrong.")

    @extend_schema(
        summary="Only superadmin can login",
        responses={
            200: OpenApiResponse(description='Login Successful', response=AdminLoginSerializer),
            400: OpenApiResponse(description='Phone number or password or both are wrong.'),
        },
    )
    def post(self, request, *args, **kwargs):
        res = super(AdminLoginView, self).create(request=request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data=res.data)


class BaseProductCreateView(generics.CreateAPIView):
    permission_classes = [IsSuperAdminOrAdmin]
    serializer_class = AdminBaseProductCreateUpdateSerializer


class BaseProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrAdmin]
    http_method_names = ('get', 'put', 'delete',)

    def get_object(self):
        return BaseProduct.objects.get(uuid=self.kwargs.get('uuid'))

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return BaseProductRetrieveSerializer
        elif self.request.method == 'PUT':
            return AdminBaseProductCreateUpdateSerializer
        else:
            return BaseProductSerializer

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
        return instance


# class BaseProductUpdateView(generics.UpdateAPIView):
#     serializer_class = AdminBaseProductCreateUpdateSerializer
#     permission_classes = [IsSuperAdminOrAdmin]
#     http_method_names = ['put']
#
#     def get_object(self):
#         return BaseProduct.objects.get(pk=self.kwargs.get('product_id'))

# def update(self, request, *args, **kwargs):
#     partial = kwargs.pop('partial', False)
#     instance = self.get_object()
#     serializer = self.get_serializer(instance, data=request.data, partial=partial)
#     serializer.is_valid(raise_exception=True)
#     self.perform_update(serializer)
#     result = {
#         "message": "success",
#         "details": serializer.data,
#         "status": 200,
#
#     }
#     return Response(result)


# class BaseProductRemove(generics.DestroyAPIView):
#     permission_classes = [IsSuperAdminOrAdmin]
#
#     def get_serializer_class(self):
#         return BaseProductSerializer
#
#     def get_object(self):
#         return BaseProduct.objects.get(pk=self.kwargs.get('product_id'))
#
#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now()
#         instance.save()
#         return instance


class SuperUserRegisterCreateView(generics.CreateAPIView):
    """Superuser Registration"""

    serializer_class = SuperUserRegisterSerializer
