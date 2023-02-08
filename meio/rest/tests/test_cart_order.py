from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from accountio.models import Organization, OrganizationUser
from catalogio.models import Product
from core.models import District, PaymentMethod
from meio.rest.serializers.carts import PrivateCarts
from meio.rest.tests.preload_product_pre_data import create_product_preload
from orderio.models import CartProduct

User = get_user_model()


class TestCart(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        # creating merchant
        user = User.objects.create_user(
            name='saifullah',
            phone='+8801521475690',
            password="123456"
        )

        payload = {
            'phone': "+8801521475690",
            'password': "123456"
        }
        url = reverse('auth:token:token_obtain_pair')
        res = self.client.post(url, payload, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])
        create_product_preload()
        self.district = District.objects.create(
            name='dhaka'
        )
        self.pay_method = PaymentMethod.objects.create(
            name='cash on delivery'
        )
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
        res_address = self.client.post(url, payload)
        self.useraddress = res_address.data

    def test_add_product_to_cart(self):
        product = Product.objects.get(pk=1)
        payload = {
            'product': product.slug,
            'quantity': 10,
        }
        url = reverse('me:carts:list.post')
        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, 201)

    def test_update_quantity_of_cart(self):
        self.test_add_product_to_cart()
        product = Product.objects.get(pk=1)
        payload = {
            'product': product.slug,
            'quantity': 12,
        }
        url = reverse('me:carts:list.post')
        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data.get('quantity'), 12)

    def test_all_cart_products(self):
        self.test_add_product_to_cart()
        url = reverse('me:carts:list.post')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, 200)

    def test_order(self):
        self.test_add_product_to_cart()
        url = reverse('me:orders:list.create')
        payload = {
            "address": self.useraddress['slug'],
            "payment_method": self.pay_method.slug,
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, 201)
