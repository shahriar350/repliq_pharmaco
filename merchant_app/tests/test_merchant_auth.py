from django.urls import reverse
from rest_framework.test import APITestCase


class TestMerchant(APITestCase):
    def setUp(self) -> None:
        url = reverse('merchant:auth.register')
        payload = {
            'phone_number': "+8801752495466",
            'full_name': "Saifullah",
            'password': "123456",
            'repeat_password': "123456",
        }
        self.client.post(url, payload, format="json")

    def test_user_registration(self):
        url = reverse('merchant:auth.register')
        payload1 = {
            'phone_number': "+8801752495467",
            'full_name': "Saifullah",
            'password': "123456",
            'repeat_password': "123456",
        }
        res = self.client.post(url, payload1)
        self.assertEqual(res.status_code, 201)

    def test_merchant_owner_login(self):
        url = reverse('merchant:auth.login')
        payload1 = {
            'phone_number': "+8801752495467",
            'password': "123456",
        }
        res = self.client.post(url, payload1)
