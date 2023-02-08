from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accountio.models import Organization, OrganizationUser
from core.models import User
from meio.rest.tests.preload_product_pre_data import create_product_preload


class TestSearch(APITestCase):
	def setUp(self) -> None:
		self.client = APIClient()

		reg_url = reverse('auth:register_login:user.registration')
		payload1 = {
			"name": 'Saifullah shahen',
			"phone": "+8801752495467",
			"password": "123456"
		}
		self.client.post(reg_url, payload1)

		token_url = reverse('auth:token:token_obtain_pair')
		payload2 = {
			'phone': "+8801752495467",
			"password": "123456"
		}
		res = self.client.post(token_url, payload2)
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

		user = User.objects.get(phone="+8801752495467")
		orga = Organization.objects.create(
			name="saif"
		)
		org1 = OrganizationUser.objects.create(
			organization=orga,
			user=user,
			role='owner',
			is_default=True
		)

		create_product_preload()

	def test_search_base_product(self):
		url = "%s?search=%s" % (reverse('we:search:base.product'), "nor")
		res = self.client.get(url)
		self.assertEqual(res.status_code, 200)
