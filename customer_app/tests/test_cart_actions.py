from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from admin_app.models import District
from auth_app.models import Users, MerchantInformation, UserAddress
from client_app.models import Tenant
from customer_app.models import Cart, CartProduct
from merchant_app.tests.test_crud_product import create_product_preload
from product_app.models import BaseProduct, Product


class TestCartAction(APITestCase):
    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')
        self.user = Users.objects.create_user(
            name="saifullah",
            phone_number="+8801752495466",
            password="123456"
        )
        self.district = District.objects.create(name='dhaka')
        self.address = UserAddress.objects.create(
            user=self.user,
            house='hello',
            street='hello',
            post_office='hello',
            police_station='hello',
            district=self.district,
            country='hello',
            state='hello',

        )
        merchant_owner = Users.objects.create_merchant_owner(
            name="saifullah",
            phone_number="+8801752495469",
            password="123456"
        )
        tenant = Tenant.objects.create(
            url="first-tenant"
        )
        merchant_info = MerchantInformation.objects.create(
            user=merchant_owner,
            merchant_domain=tenant
        )

        superuser = Users.objects.create_superuser(
            name="saifullah",
            phone_number="+8801752495467",
            password="123456"
        )

        login = {
            'phone_number': "+8801752495466",
            'password': "123456"
        }
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])
        create_product_preload()
        baseprod = BaseProduct.objects.create(
            superadmin=superuser,
            name='demo',
            description='this is description',
            dosage_form='Oral',
            manufacturer_id=1,
            brand_id=1,
            route_of_administration_id=1,
            medicine_physical_state_id=1,
        )
        self.product = Product.objects.create(
            base_product=baseprod,
            merchant=merchant_owner,
            merchant_domain=merchant_info.merchant_domain,
            stock=100,
            buying_price=Decimal("100"),
            selling_price=Decimal("110"),

        )

    def test_product_to_cart(self):
        cart_url = reverse('customer:cart.add.product')
        payload = {
            'product': self.product.id,
            'quantity': 6,
        }
        res = self.client.post(cart_url, payload, format="json")
        self.product_cart = res.data['cart_product_id']
        self.assertEqual(res.status_code, 201)

    def test_product_remove_to_cart(self):
        cart = Cart.objects.create(
            customer=self.user
        )
        cart_prod = CartProduct.objects.create(
            cart=cart,
            product=self.product,
            quantity=6
        )
        cart_url = reverse('customer:cart.update.remove.product', kwargs={'cart_product_uuid': cart_prod.uuid})
        res = self.client.delete(cart_url)
        self.assertEqual(res.status_code, 204)

    def test_product_update_to_cart(self):
        cart = Cart.objects.create(
            customer=self.user
        )
        cart_prod = CartProduct.objects.create(
            cart=cart,
            product=self.product,
            quantity=6
        )
        payload = {
            'quantity': 7
        }
        cart_url = reverse('customer:cart.update.remove.product', kwargs={'cart_product_uuid': cart_prod.uuid})
        res = self.client.put(cart_url, payload, format="json")
        self.assertEqual(res.status_code, 200)

    def test_product_list(self):
        cart = Cart.objects.create(
            customer=self.user
        )
        cart_prod = CartProduct.objects.create(
            cart=cart,
            product=self.product,
            quantity=6
        )
        payload = {
            'quantity': 7
        }

        cart_url = reverse('customer:cart.list')
        res = self.client.get(cart_url)
        self.assertEqual(res.status_code, 200)

    def test_product_current_list(self):
        cart = Cart.objects.create(
            customer=self.user
        )
        self.cart_slug = cart.slug
        cart_prod = CartProduct.objects.create(
            cart=cart,
            product=self.product,
            quantity=6
        )

        payload = {
            'quantity': 7
        }

        cart_url = reverse('customer:cart.current.list')
        res = self.client.get(cart_url)
        self.assertEqual(res.status_code, 200)

    def test_checkout(self):
        self.test_product_current_list()
        url = reverse('customer:checkout')
        payload = {
            'cart': self.cart_slug,
            'address': self.address.slug,
            'payment': 0,
        }
        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, 201)
