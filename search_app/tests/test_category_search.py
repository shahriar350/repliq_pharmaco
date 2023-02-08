from django.urls import reverse
from rest_framework.test import APITestCase

from admin_app.models import Category
from auth_app.models import Users


class CategorySearchProduct(APITestCase):
    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')

        Users.objects.create_merchant_owner(
            name='saifullah',
            phone_number='+8801752495466',
            password="123456"
        )


        login = {
            'phone_number': "+8801752495466",
            'password': "123456"
        }
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

        categories = ["Analgesics", "Analgesics", "Antianxiety Drugs", "Antiarrhythmics"]


        for category in categories:
            Category.objects.create(
                name=category
            )


    def test_category_search(self):
        url = f"{reverse('search:category')}?search=Analgesics"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)