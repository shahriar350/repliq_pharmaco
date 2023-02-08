from django.urls import reverse
from rest_framework.test import APITestCase

from accountio.models import Domain, Organization, OrganizationUser, OrganizationDomain
from catalogio.models import Category, Manufacturer, Supplier, MedicinePhysicalState, RouteOfAdministration, Brand, \
	Ingredient, BaseProduct
from core.models import User
from weio.rest.serializers.products import PrivateProductSerializers


class TestAddProduct(APITestCase):
	def setUp(self) -> None:
		loginurl = reverse('auth:token:token_obtain_pair')

		merchant_owner = User.objects.create_user(
			name='saifullah',
			phone='+8801752495466',
			password="123456"
		)
		self.organization = Organization.objects.create(
			name="saif",
			kind="abc"
		)

		OrganizationUser.objects.create(
			organization=self.organization,
			user=merchant_owner,
			role='owner',
			is_default=True,
		)
		superadmin = User.objects.create_user(
			name='saifullah',
			phone='+8801752495467',
			password="123456"
		)

		domain = Domain.objects.create(
			url="saif"
		)
		OrganizationDomain.objects.create(
			domain=domain,
			organization=self.organization,
		)

		login = {
			'phone': "+8801752495466",
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
		self.categories_uid = []
		self.manufacturers_uid = []
		self.suppliers_uid = []
		self.medicinePhysicalStates_uid = []
		self.routeOfAdministrations_uid = []
		self.ingredients_uid = []
		for category in categories:
			cat = Category.objects.create(
				name=category
			)
			self.categories_uid.append(cat.uid)
		for i in manufacturers:
			man = Manufacturer.objects.create(
				name=i
			)
			self.manufacturers_uid.append(man.uid)
		for i in suppliers:
			supplier = Supplier.objects.create(
				name=i
			)
			self.suppliers_uid.append(supplier.uid)
		for i in medicinePhysicalStates:
			physical = MedicinePhysicalState.objects.create(
				name=i
			)
			self.medicinePhysicalStates_uid.append(physical.uid)
		for i in routeOfAdministrations:
			route = RouteOfAdministration.objects.create(
				name=i
			)
			self.routeOfAdministrations_uid.append(route.uid)
		self.brands_uid = []
		for brand in brands:
			brand = Brand.objects.create(
				name=brand
			)
			self.brands_uid.append(brand.uid)
		for ingredient in ingredients:
			ing = Ingredient.objects.create(
				name=ingredient
			)
			self.ingredients_uid.append(ing.uid)
		self.baseprod = BaseProduct.objects.create(
			superadmin=superadmin,
			name='demo',
			description='this is description',
			dosage_form='Oral',
			manufacturer=Manufacturer.objects.get(uid=self.manufacturers_uid[0]),
			brand=Brand.objects.get(uid=self.brands_uid[0]),
			route_of_administration=RouteOfAdministration.objects.get(uid=self.routeOfAdministrations_uid[0]),
			medicine_physical_state=MedicinePhysicalState.objects.get(uid=self.medicinePhysicalStates_uid[0]),
		)

	def test_merchant_add_product_if_baseproduct_not_available(self):
		url = reverse('we:products:create')
		payload = {
			"name": "This is product name",
			"base_product": "",
			"category": [self.categories_uid[0], self.categories_uid[1]],
			"active_ingredient": [self.ingredients_uid[0], self.ingredients_uid[1]],
			"dosage_form": "string",
			"manufacturer": self.manufacturers_uid[0],
			"brand": self.brands_uid[0],
			"route_of_administration": self.routeOfAdministrations_uid[0],
			"medicine_physical_state": self.medicinePhysicalStates_uid[0],
			"description": "string",
			"stock": 100,
			"buying_price": "0.00",
			"selling_price": "0.00",
			"organization": self.organization.uid,
		}

		res = self.client.post(url, payload, format='json')
		self.assertEqual(res.status_code, 201)

	def test_merchant_add_product_if_baseproduct_available(self):
		url = reverse('we:products:create')
		payload = {
			"name": "",
			"category": [],
			"active_ingredient": [],
			"dosage_form": "",
			"manufacturer": "",
			"brand": "",
			"route_of_administration": "",
			"medicine_physical_state": "",
			"description": "",
			"base_product": self.baseprod.uid,
			"stock": 0,
			"buying_price": "0.00",
			"selling_price": "0.00",
			"organization": self.organization.uid
		}
		res = self.client.post(url, payload, format='json')
		self.assertEqual(res.status_code, 201)

	def test_merchant_without_sending_value_available(self):
		url = reverse('we:products:create')
		payload = {
			"name": "This is product name",
			"base_product": "",
			"category": [],
			"active_ingredient": [],
			"dosage_form": "string",
			"manufacturer": self.manufacturers_uid[0],
			"brand": self.brands_uid[0],
			"route_of_administration": self.routeOfAdministrations_uid[0],
			"medicine_physical_state": self.medicinePhysicalStates_uid[0],
			"description": "string",
			"stock": 100,
			"buying_price": "0.00",
			"selling_price": "0.00",
			"organization": self.organization.uid,
		}
		res = self.client.post(url, payload, format='json')
		self.assertEqual(res.status_code, 400)
