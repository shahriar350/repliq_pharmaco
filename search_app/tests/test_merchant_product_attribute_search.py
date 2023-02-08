from django.urls import reverse
from rest_framework.test import APITestCase

from admin_app.models import Ingredient, Manufacturer, Supplier, MedicinePhysicalState, RouteOfAdministration
from auth_app.models import Users


class TestMerchantProductAttributeSearch(APITestCase):
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

        ingredients = ["Clonazepam", "Minoxidil", "ingredient1", "ingredient2"]
        manufacturers = ["manufacturers1", "manufacturers2", "manufacturers3", "manufacturers4"]
        suppliers = ["suppliers1", "suppliers2", "suppliers3", "suppliers4", "suppliers5"]
        medicinePhysicalStates = ["medicinePhysicalStates", "medicinePhysicalStates1", "medicinePhysicalStates2",
                                  "medicinePhysicalStates3", "medicinePhysicalStates4"]
        routeOfAdministrations = ["routeOfAdministrations", "routeOfAdministrations1", "routeOfAdministrations3",
                                  "routeOfAdministrations2", "routeOfAdministrations4"]

        for i in ingredients:
            Ingredient.objects.create(
                name=i
            )

        for i in manufacturers:
            Manufacturer.objects.create(
                name=i
            )

        for i in suppliers:
            Supplier.objects.create(
                name=i
            )

        for i in medicinePhysicalStates:
            MedicinePhysicalState.objects.create(
                name=i
            )

        for i in routeOfAdministrations:
            RouteOfAdministration.objects.create(
                name=i
            )

    def test_ingredient_search(self):
        url = f"{reverse('search:ingredient')}?search=Clonazepam"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Clonazepam')

    def test_manufacturer_search(self):
        url = f"{reverse('search:manufacturer')}?search=manufacturers1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'manufacturers1')

    def test_supplier_search(self):
        url = f"{reverse('search:supplier')}?search=suppliers1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'suppliers1')

    def test_medicinePhysicalStates_search(self):
        url = f"{reverse('search:medicinephysicalstate')}?search=medicinePhysicalStates"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'medicinePhysicalStates')

    def test_routeofadministration_search(self):
        url = f"{reverse('search:routeofadministration')}?search=routeOfAdministrations"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'routeOfAdministrations')
