from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import Brand
from admin_app.serializers import BrandSerializers
from auth_app.models import Users
from merchant_app.tests.test_crud_product import create_product_preload


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
        token = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])
        create_product_preload()
        url = reverse('superadmin:product.base.create')
        payload = {
            "name": "string",
            "category": [
                1, 2
            ],
            "active_ingredient": [
                1, 2
            ],
            "dosage_form": "string",
            "manufacturer": 1,
            "brand": 1,
            "route_of_administration": 1,
            "medicine_physical_state": 1,
            "description": "string"
        }
        res = self.client.post(url, payload, format='json')
        self.product_uuid = res.data['uuid']

    def test_create_base_product(self):
        url = reverse('superadmin:product.base.create')
        payload = {
            "name": "string",
            "category": [
                1, 2
            ],
            "active_ingredient": [
                1, 2
            ],
            "dosage_form": "string",
            "manufacturer": 1,
            "brand": 1,
            "route_of_administration": 1,
            "medicine_physical_state": 1,
            "description": "string"
        }
        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, 201)

    def test_update_base_product(self):
        update_url = reverse('superadmin:product.base.retrieve.update.delete', kwargs={'uuid': self.product_uuid})
        payload1 = {
            "name": "string",
            "category": [
                1, 2, 3
            ],
            "active_ingredient": [
                1, 2
            ],
            "route_of_administration": 1,
            "description": "string"
        }
        res = self.client.put(update_url, payload1, format='json')
        self.assertEqual(res.status_code, 200)

    def test_remove_base_product(self):
        update_url = reverse('superadmin:product.base.retrieve.update.delete', kwargs={'uuid': self.product_uuid})
        res = self.client.delete(update_url)
        self.assertEqual(res.status_code, 204)
