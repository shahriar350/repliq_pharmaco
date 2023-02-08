from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from core.models import District


class TestAddress(APITestCase):
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
        self.district = District.objects.create(
            name='dhaka'
        )
        res = self.client.post(token_url, payload2)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

    def test_user_create_address(self):
        payload = {
            'label': 'hello',
            'house': 'house1',
            'street': 'street1',
            'post_office': 'post 11',
            'police_station': 'police',
            'district': self.district.slug,
            'country': 'bd',
            'state': '',
        }
        url = reverse('me:addresses:list.post')
        res = self.client.post(url, payload)
        self.address = res.data
        self.assertEqual(res.status_code, 201)

    def test_user_all_address(self):
        self.test_user_create_address()
        url = reverse('me:addresses:list.post')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_address_update(self):
        payload = {
            'label': 'hello',
            'house': 'house2',
            'street': 'street1',
            'post_office': 'post 11',
            'police_station': 'police',
            'district': self.district.slug,
            'country': 'bd',
            'state': '',
        }
        self.test_user_create_address()
        url = reverse('me:addresses:retrieve.update.delete', kwargs={'slug': self.address['slug']})
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['house'], 'house2')

    def test_address_get(self):
        payload = {
            'label': 'hello',
            'house': 'house2',
            'street': 'street1',
            'post_office': 'post 11',
            'police_station': 'police',
            'district': self.district.slug,
            'country': 'bd',
            'state': '',
        }
        self.test_user_create_address()
        url = reverse('me:addresses:retrieve.update.delete', kwargs={'slug': self.address['slug']})
        res = self.client.get(url, payload)
        self.assertEqual(res.status_code, 200)

    def test_address_delete(self):
        self.test_user_create_address()
        url = reverse('me:addresses:retrieve.update.delete', kwargs={'slug': self.address['slug']})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)
