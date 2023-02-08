from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestUserRegistration(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('auth:register_login:user.registration')
        payload = {
            'phone': "+8801752495467",
            "name": 'saifullah',
            "password": "123456",
        }
        res = self.client.post(url, payload, format="json")
        self.assertEqual(res.status_code, 201)
