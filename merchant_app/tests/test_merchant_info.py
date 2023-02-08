from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from auth_app.models import Users


class TestMerchant(APITestCase):
    def setUp(self) -> None:
        url = reverse('auth:token_obtain_pair')
        Users.objects.create_merchant_owner(
            name="saifullah",
            phone_number="+8801752495466",
            password="123456"
        )
        payload = {
            'phone_number': "+8801752495466",
            'password': "123456"
        }
        self.client = APIClient()
        res = self.client.post(url, payload, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

    def test_merchant_info_add(self):
        url = reverse('merchant:auth.info.add')
        payload = {
            "merchant_domain": "string",
            "company_name": "string",
            "address": {
                "house": "string",
                "street": "string",
                "post_office": "string",
                "police_station": "string",
                "city": "string",
                "country": "string",
                "state": "string"
            }
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, 201)
