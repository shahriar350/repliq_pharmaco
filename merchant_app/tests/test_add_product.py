import random

from django.urls import reverse
from rest_framework.test import APITestCase

from admin_app.models import Ingredient, Brand, RouteOfAdministration, MedicinePhysicalState, Supplier, Manufacturer, \
    Category
from auth_app.models import Users, MerchantInformation
from client_app.models import Tenant
from product_app.models import BaseProduct


class TestAddProduct(APITestCase):
    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')

        merchant_owner = Users.objects.create_merchant_owner(
            name='saifullah',
            phone_number='+8801752495466',
            password="123456"
        )

        superadmin = Users.objects.create_superuser(
            name='saifullah',
            phone_number='+8801752495467',
            password="123456"
        )
        sub_domain = Tenant.objects.create(
            url="saif"
        )
        MerchantInformation.objects.create(
            user=merchant_owner,
            merchant_domain=sub_domain,
        )
        login = {
            'phone_number': "+8801752495466",
            'password': "123456"
        }
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

        categories = ["Analgesics", "ABC", "Antianxiety Drugs", "Antiarrhythmics"]
        ingredients = ["Clonazepam", "Minoxidil", "ingredient1", "ingredient2"]
        brands = ["Square Pharmaceuticals", "Incepta Pharmaceutical Ltd.", "Beximco Pharmaceuticals LTD.",
                  "Opsonin Pharma Ltd."]
        manufacturers = ["manufacturers1", "manufacturers2", "manufacturers3", "manufacturers4"]
        suppliers = ["suppliers1", "suppliers2", "suppliers3", "suppliers4", "suppliers5"]
        medicinePhysicalStates = ["medicinePhysicalStates", "medicinePhysicalStates1", "medicinePhysicalStates2",
                                  "medicinePhysicalStates3", "medicinePhysicalStates4"]
        routeOfAdministrations = ["routeOfAdministrations", "routeOfAdministrations1", "routeOfAdministrations3",
                                  "routeOfAdministrations2", "routeOfAdministrations4"]
        self.categories_uuid = []
        self.manufacturers_uuid = []
        self.suppliers_uuid = []
        self.medicinePhysicalStates_uuid = []
        self.routeOfAdministrations_uuid = []
        self.ingredients_uuid = []
        for category in categories:
            cat = Category.objects.create(
                name=category
            )
            self.categories_uuid.append(cat.uuid)
        for i in manufacturers:
            man = Manufacturer.objects.create(
                name=i
            )
            self.manufacturers_uuid.append(man.uuid)
        for i in suppliers:
            supplier = Supplier.objects.create(
                name=i
            )
            self.suppliers_uuid.append(supplier.uuid)
        for i in medicinePhysicalStates:
            physical = MedicinePhysicalState.objects.create(
                name=i
            )
            self.medicinePhysicalStates_uuid.append(physical.uuid)
        for i in routeOfAdministrations:
            route = RouteOfAdministration.objects.create(
                name=i
            )
            self.routeOfAdministrations_uuid.append(route.uuid)
        self.brands_uuid = []
        for brand in brands:
            brand = Brand.objects.create(
                name=brand
            )
            self.brands_uuid.append(brand.uuid)
        for ingredient in ingredients:
            ing = Ingredient.objects.create(
                name=ingredient
            )
            self.ingredients_uuid.append(ing.uuid)
        self.baseprod = BaseProduct.objects.create(
            superadmin=superadmin,
            name='demo',
            description='this is description',
            dosage_form='Oral',
            manufacturer_id=1,
            brand_id=1,
            route_of_administration_id=1,
            medicine_physical_state_id=1,
        )

    def test_merchant_add_product_if_baseproduct_not_available(self):
        url = reverse('merchant:product.create')
        payload = {
            "name": "string",
            "category": [self.categories_uuid[0], self.categories_uuid[1]],
            "active_ingredient": [self.ingredients_uuid[0], self.ingredients_uuid[1]],
            "dosage_form": "string",
            "manufacturer": self.manufacturers_uuid[0],
            "brand": self.brands_uuid[0],
            "route_of_administration": self.routeOfAdministrations_uuid[0],
            "medicine_physical_state": self.medicinePhysicalStates_uuid[0],
            "description": "string",
            "stock": 0,
            "buying_price": "0.00",
            "selling_price": "0.00"
        }
        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, 201)

    def test_merchant_add_product_if_baseproduct_available(self):
        url = reverse('merchant:product.create')
        payload = {
            "base_product": self.baseprod.uuid,
            "stock": 0,
            "buying_price": "0.00",
            "selling_price": "0.00"
        }
        res = self.client.post(url, payload, format='json')
        # response_data = {'base_product': 1, 'stock': 0, 'buying_price': '0.00', 'selling_price': '0.00'}
        self.assertEqual(res.status_code, 201)
        # self.assertEqual(res.data, response_data)
