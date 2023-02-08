import tempfile

from PIL import Image
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from decimal import Decimal

from admin_app.models import Category, Manufacturer, Supplier, MedicinePhysicalState, RouteOfAdministration, Brand, \
    Ingredient
from auth_app.models import Users, MerchantInformation
from client_app.models import Tenant
from product_app.models import BaseProduct, Product


def create_product_preload():
    categories = ["Analgesics", "Analgesics", "Antianxiety Drugs", "Antiarrhythmics"]
    ingredients = ["Clonazepam", "Minoxidil", "ingredient1", "ingredient2"]
    brands = ["Square Pharmaceuticals", "Incepta Pharmaceutical Ltd.", "Beximco Pharmaceuticals LTD.",
              "Opsonin Pharma Ltd."]
    manufacturers = ["manufacturers1", "manufacturers2", "manufacturers3", "manufacturers4"]
    suppliers = ["suppliers1", "suppliers2", "suppliers3", "suppliers4", "suppliers5"]
    medicinePhysicalStates = ["medicinePhysicalStates", "medicinePhysicalStates1", "medicinePhysicalStates2",
                              "medicinePhysicalStates3", "medicinePhysicalStates4"]
    routeOfAdministrations = ["routeOfAdministrations", "routeOfAdministrations1", "routeOfAdministrations3",
                              "routeOfAdministrations2", "routeOfAdministrations4"]
    for category in categories:
        Category.objects.create(
            name=category
        )
    for i in manufacturers:
        man = Manufacturer.objects.create(
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
    for brand in brands:
        Brand.objects.create(
            name=brand
        )
    for ingredient in ingredients:
        Ingredient.objects.create(
            name=ingredient
        )


class TestMerchant(APITestCase):
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

    def test_merchant_product_update(self):
        url = reverse('merchant:product.update.destroy', kwargs={'product_slug': self.prod.slug})
        payload = {
            "stock": 100,
            "selling_price": "90",
            "buying_price": "95",
        }
        res = self.client.put(url, payload, format="json")
        response_data = {'stock': 100, 'selling_price': '90.00', 'buying_price': '95.00', 'active': True}

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, response_data)

    def test_merchant_product_remove(self):
        url = reverse('merchant:product.update.destroy', kwargs={'product_slug': self.prod.slug})

        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)

    def test_merchant_product_restored(self):
        url = reverse('merchant:product.restore', kwargs={'product_slug': self.prod.slug})

        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)

    #
    def test_image_add(self):
        url = reverse('merchant:product.add.image', kwargs={'product_slug': self.prod.slug})
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'images': [image_file]
            }
            res = self.client.put(url, payload, type="json")
            self.assertEqual(res.status_code, 200)

            # remove that image

            produ = Product.objects.prefetch_related('get_product_images').get(slug=self.prod.slug)
            image = produ.get_product_images.first()

            url_delete = reverse('merchant:product.remove.image',
                                 kwargs={'product_uuid': self.prod.uuid, 'image_uuid': image.uuid})
            res = self.client.delete(url_delete)
            self.assertEqual(res.status_code, 204)
