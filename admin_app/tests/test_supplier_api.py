from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import Supplier
from admin_app.serializers import SupplierSerializers
from auth_app.models import Users

SUPPLIER_URL = reverse('superadmin:supplier.list.create')


def detail_supplier(uuid):
    """Create and return a detail URL."""
    return reverse('superadmin:supplier.retrieve.update.remove', args=[uuid])


# def delete_url(supplier_uuid):
#     """Create and return a delete URL."""
#     return reverse('superadmin:supplier.delete', args=[supplier_uuid])


# def remove_url(supplier_uuid):
#     """Create and return a remove URL."""
#     return reverse('superadmin:supplier.remove', args=[supplier_uuid])


def create_supplier(**params):
    """Create and return a supplier."""
    defaults = {
        'name': 'test string',
    }
    defaults.update(params)
    supplier = Supplier.objects.create(**defaults)
    return supplier


class SupplierTestcases(APITestCase):
    """Test for supplier API"""

    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')
        superadmin = Users.objects.create_superuser(
            name='saifullah',
            phone_number='+8801752495467',
            password="123456"
        )

        login = {
            'phone_number': "+8801752495467",
            'password': "123456"
        }
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

    def test_list_supplier(self):
        """Test listing supplier."""
        create_supplier()
        create_supplier()

        response = self.client.get(SUPPLIER_URL)
        supplier = Supplier.objects.all()
        serializer = SupplierSerializers(supplier, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_supplier(self):
        """Test creating a supplier."""
        payload = {
            'name': 'test string',
        }
        response = self.client.post(SUPPLIER_URL, payload, format='json')
        supplier = Supplier.objects.get(uuid=response.data['uuid'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], supplier.name)
       

    def test_retrieve_supplier(self):
        """Test retrieve a supplier."""
        supplier1 = create_supplier()
        supplier2 = create_supplier()
        url = detail_supplier(supplier1.uuid)
        response = self.client.get(url)
        supplier = Supplier.objects.get(uuid=supplier1.uuid)
        serializer = SupplierSerializers(supplier)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_supplier(self):
        """Test update a supplier."""
        supplier = create_supplier()

        payload = {
            'name': 'updated string',
        }
        url = detail_supplier(supplier.uuid)
        response = self.client.put(url, payload)
        supplier.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], supplier.name)

    def test_patch_supplier(self):
        """Test patch a supplier."""
        supplier = create_supplier()

        payload = {
            'name': 'partial update string',
        }
        url = detail_supplier(supplier.uuid)
        response = self.client.patch(url, payload)
        supplier.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], supplier.name)

    # def test_delete_supplier(self):
    #     """Test deleteing a supplier."""
    #     supplier = create_supplier()
    #     url = delete_url(supplier.uuid)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Supplier.objects.filter(uuid=supplier.uuid).exists())

    def test_remove_supplier(self):
        """Test remove a supplier."""
        supplier = create_supplier()
        url = detail_supplier(supplier.uuid)
        response = self.client.delete(url)
        supplier.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(supplier.deleted_at == None)
