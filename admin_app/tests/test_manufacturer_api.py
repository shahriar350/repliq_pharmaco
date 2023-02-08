from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import Manufacturer
from admin_app.serializers import ManufacturerSerializers
from auth_app.models import Users

MANUFACTURER_URL = reverse('superadmin:manufacturer.list.create')


def detail_manufacturer(uuid):
    """Create and return a detail URL."""
    return reverse('superadmin:manufacturer.retrieve.update.remove', args=[uuid])


# def delete_url(manufacturer_uuid):
#     """Create and return a delete URL."""
#     return reverse('superadmin:manufacturer.delete', args=[manufacturer_uuid])


# def remove_url(manufacturer_uuid):
#     """Create and return a remove URL."""
#     return reverse('superadmin:manufacturer.remove', args=[manufacturer_uuid])


def create_manufacturer(**params):
    """Create and return a manufacturer."""
    defaults = {
        'name': 'test string',
    }
    defaults.update(params)
    manufacturer = Manufacturer.objects.create(**defaults)
    return manufacturer


class ManufacturerTestcases(APITestCase):
    """Test for manufacturer API"""
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
    def test_list_manufacturer(self):
        """Test listing manufacturer."""
        create_manufacturer()
        create_manufacturer()

        response = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()
        serializer = ManufacturerSerializers(manufacturer, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_manufacturer(self):
        """Test creating a manufacturer."""
        payload = {
            'name': 'test string',
        }
        response = self.client.post(MANUFACTURER_URL, payload, format='json')
        manufacturer = Manufacturer.objects.get(uuid=response.data['uuid'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], manufacturer.name)

    def test_retrieve_manufacturer(self):
        """Test retrieve a manufacturer."""
        manufacturer1 = create_manufacturer()
        manufacturer2 = create_manufacturer()
        url = detail_manufacturer(manufacturer1.uuid)
        response = self.client.get(url)
        manufacturer = Manufacturer.objects.get(uuid=manufacturer1.uuid)
        serializer = ManufacturerSerializers(manufacturer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_manufacturer(self):
        """Test update a manufacturer."""
        manufacturer = create_manufacturer()

        payload = {
            'name': 'updated string',
        }
        url = detail_manufacturer(manufacturer.uuid)
        response = self.client.put(url, payload)
        manufacturer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], manufacturer.name)

    def test_patch_manufacturer(self):
        """Test patch a manufacturer."""
        manufacturer = create_manufacturer()

        payload = {
            'name': 'partial update string',
        }
        url = detail_manufacturer(manufacturer.uuid)
        response = self.client.patch(url, payload)
        manufacturer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], manufacturer.name)

    # def test_delete_manufacturer(self):
    #     """Test deleteing a manufacturer."""
    #     manufacturer = create_manufacturer()
    #     url = delete_url(manufacturer.uuid)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Manufacturer.objects.filter(uuid=manufacturer.uuid).exists())

    def test_remove_manufacturer(self):
        """Test remove a manufacturer."""
        manufacturer = create_manufacturer()
        url = detail_manufacturer(manufacturer.uuid)
        response = self.client.delete(url)
        manufacturer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(manufacturer.deleted_at == None)
