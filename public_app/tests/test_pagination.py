from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from auth_app.models import MerchantInformation, Users
from client_app.models import Tenant
from merchant_app.tests.test_crud_product import create_product_preload
from product_app.models import Product, BaseProduct


class TestPagination(APITestCase):
    def setUp(self) -> None:
        url = reverse('auth:token_obtain_pair')
        tenant = Tenant.objects.create(
            url="saif"
        )
        my_merchant_owner = Users.objects.create_merchant_owner(
            name="saifullah",
            phone_number="+8801752495466",
            password="123456"
        )
        MerchantInformation.objects.create(
            merchant_domain=tenant,
            user=my_merchant_owner,
            company_name="my_merchant_owner"
        )
        payload = {
            'phone_number': "+8801752495466",
            'password': "123456"
        }
        self.client = APIClient()
        res = self.client.post(url, payload, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])
        # base product pre requirements start
        create_product_preload()
        # base product pre requirements end

        baseproduct = BaseProduct.objects.create(
            name='saifullah shahen',
            description='hello',
            dosage_form='first',
            manufacturer_id=1,
            brand_id=1,
            route_of_administration_id=1,
            medicine_physical_state_id=1,
        )
        baseproduct.category.add(1)
        baseproduct.category.add(2)
        baseproduct.active_ingredient.add(1)

        self.prod = Product.objects.create(
            base_product=baseproduct,
            merchant=my_merchant_owner,
            merchant_domain=my_merchant_owner.get_user_information.merchant_domain,
            stock=100,
            selling_price=Decimal('100'),
            buying_price=Decimal('100')
        )
        baseproduct.merchant_product = self.prod
        baseproduct.save()

        url = reverse('merchant:product.create')
        payload = {
            "base_product": baseproduct.id,
            "stock": 0,
            "buying_price": "0.00",
            "selling_price": "0.00"
        }
        res = self.client.post(url, payload, format='json')
        # print(res.data)

    def test_paginator_data(self):
        url = reverse('global:products.list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
