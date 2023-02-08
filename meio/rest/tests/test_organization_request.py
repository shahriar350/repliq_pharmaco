from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestMerchantRequest(APITestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		# register user
		reg_url = reverse('auth:register_login:user.registration')
		payload1 = {
			"name": 'Saifullah shahen',
			"phone": "+8801752495467",
			"password": "123456"
		}
		self.client.post(reg_url, payload1)
		# authenticate user
		token_url = reverse('auth:token:token_obtain_pair')
		payload2 = {
			'phone': "+8801752495467",
			"password": "123456"
		}
		res = self.client.post(token_url, payload2)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

	def test_organization_user(self):
		url = reverse('me:organizations:request')
		payload = {
			"name": "string",
			"kind": "string",
			"tax_number": "string",
			"registration_no": "string",
			"website_url": "string",
			"blog_url": "string",
			"linkedin_url": "string",
			"instagram_url": "string",
			"facebook_url": "string",
			"twitter_url": "string",
			"summary": "string",
			"description": "string"
		}
		res = self.client.post(url, payload)
		self.assertEqual(res.status_code, 201)
