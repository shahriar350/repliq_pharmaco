from django.urls import reverse
from rest_framework.test import APITestCase

from admin_app.models import Brand
from auth_app.models import Users
from client_app.models import Tenant


class BrandSearchProduct(APITestCase):
    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')

        Users.objects.create_merchant_owner(
            name='shiblu',
            phone_number='+8801772115060',
            password="123456"
        )

        login = {
            'phone_number': "+8801772115060",
            'password': "123456"
        }
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])


        brands = ["Square Pharmaceuticals", "Incepta Pharmaceutical Ltd.", "Beximco Pharmaceuticals LTD.",
                  "Opsonin Pharma Ltd."]


        for brand in brands:
            Brand.objects.create(
                name=brand
            )

    def test_brand_search(self):
        url = f"{reverse('search:brand')}?search=Square Pharmaceuticals"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Square Pharmaceuticals')
