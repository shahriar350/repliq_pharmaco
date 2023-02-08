from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accountio.models import Organization, OrganizationUser
from core.models import User


class TestOrganizationDefault(APITestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		reg_url = reverse('auth:register_login:user.registration')
		payload1 = {
			"name": 'Saifullah shahen',
			"phone": "+8801752495467",
			"password": "123456"
		}
		self.client.post(reg_url, payload1)
		user = User.objects.get(phone="+8801752495467")
		token_url = reverse('auth:token:token_obtain_pair')
		payload2 = {
			'phone': "+8801752495467",
			"password": "123456"
		}
		res = self.client.post(token_url, payload2)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])
		self.org1 = Organization.objects.create(
			name="saifullah"
		)
		self.org2 = Organization.objects.create(
			name="Sazzad"
		)
		OrganizationUser.objects.create(
			organization=self.org1,
			user=user,
			role='owner',
		)
		OrganizationUser.objects.create(
			organization=self.org2,
			user=user,
			role='staff',
			is_default=True
		)

	def test_set_organization_default(self):
		url = reverse('we:organizations:default')
		payload = {
			'organization': self.org1.uid
		}
		res = self.client.post(url, payload)
		self.assertEqual(res.status_code, 200)

	def test_owner_add_user(self):
		self.test_set_organization_default()
		url = reverse("we:organizations:create.user")
		payload = {
			'role': 'admin',
			'name': 'Saifullah shahen',
			'phone': '+8801752495463',
			'password': '123456',
		}
		res = self.client.post(url, payload)
		self.assertEqual(res.status_code, 201)
