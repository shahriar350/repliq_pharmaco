from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import Brand
from admin_app.serializers import BrandSerializers
from auth_app.models import Users

BRAND_URL = reverse('superadmin:brand.list.create')


def detail_brand(uuid):
    """Create and return a detail URL."""
    return reverse('superadmin:brand.retrieve.update.remove', args=[uuid])


# def delete_url(brand_uuid):
#     """Create and return a delete URL."""
#     return reverse('superadmin:brand.delete', args=[brand_uuid])


# def remove_url(brand_uuid):
#     """Create and return a remove URL."""
#     return reverse('superadmin:brand.remove', args=[brand_uuid])


def create_brand(**params):
    """Create and return a brand."""
    defaults = {
        'name': 'test string',
    }
    defaults.update(params)
    brand = Brand.objects.create(**defaults)
    return brand


class BrandTestcases(APITestCase):
    """Test for Brand API"""

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

    def test_list_brand(self):
        """Test listing brand."""
        create_brand()
        create_brand()

        response = self.client.get(BRAND_URL)
        brand = Brand.objects.all()
        serializer = BrandSerializers(brand, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_brand(self):
        """Test creating a brand."""
        payload = {
            'name': 'parasitamol',
        }
        response = self.client.post(BRAND_URL, payload, format='json')
        brand = Brand.objects.get(uuid=response.data['uuid'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], brand.name)

    def test_retrieve_brand(self):
        """Test retrieve a brand."""
        brand1 = create_brand()
        brand2 = create_brand()
        url = detail_brand(brand1.uuid)
        response = self.client.get(url)
        brand = Brand.objects.get(uuid=brand1.uuid)
        serializer = BrandSerializers(brand)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_brand(self):
        """Test update a brand."""
        brand = create_brand()

        payload = {
            'name': 'updated string',
        }
        url = detail_brand(brand.uuid)
        response = self.client.put(url, payload)
        brand.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], brand.name)

    def test_patch_brand(self):
        """Test patch a brand."""
        brand = create_brand()

        payload = {
            'name': 'partial update string',
        }
        url = detail_brand(brand.uuid)
        response = self.client.patch(url, payload)
        brand.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], brand.name)

    # def test_delete_brand(self):
    #     """Test deleteing a brand."""
    #     brand = create_brand()
    #     url = delete_url(brand.uuid)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Brand.objects.filter(uuid=brand.uuid).exists())

    def test_remove_brand(self):
        """Test remove a brand."""
        brand = create_brand()
        url = detail_brand(brand.uuid)
        response = self.client.delete(url)
        brand.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(brand.deleted_at == None)
