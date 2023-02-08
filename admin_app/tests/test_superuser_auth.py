from rest_framework.test import APITestCase
from django.urls import reverse


class SuperUserCreateRoleTestcases(APITestCase):
    """Test for superuser Register API"""
    REGISTER_URL = reverse('superadmin:superuser.register')

    def test_register_staff(self):
        """Test Register staff."""
        payload = {
            "phone_number": "+8801772115063",
            "full_name": "shiblu",
            "type": "staff",
            "password": "123456789Aas",
            "repeat_password": "123456789Aas"
        }

        response = self.client.post(self.REGISTER_URL, payload)
        data = {'phone_number': '+8801772115063', 'full_name': 'shiblu', 
                            'type': 'staff', 'role': 'staff', 
                            'password': '123456789Aas', 
                            'repeat_password': '123456789Aas'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)