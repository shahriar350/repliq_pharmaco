from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from admin_app.models import Category, Brand, Ingredient, Manufacturer, Supplier, MedicinePhysicalState, \
    RouteOfAdministration
from auth_app.models import Users

from faker import Faker
import random
from product_app.models import BaseProduct

fake = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
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
        with transaction.atomic():
            categories_id = []
            for category in categories:
                cat = Category.objects.create(
                    name=category
                )
                categories_id.append(cat.id)
            for i in manufacturers:
                Manufacturer_id = []
                manu = Manufacturer.objects.create(
                    name=i
                )
                Manufacturer_id.append(manu.id)
            for i in suppliers:
                suppliers_id = []
                supp = Supplier.objects.create(
                    name=i
                )
                suppliers_id.append(supp.id)
            for i in medicinePhysicalStates:
                medicinePhysicalStates_id = []
                mps = MedicinePhysicalState.objects.create(
                    name=i
                )
                medicinePhysicalStates_id.append(mps.id)
            for i in routeOfAdministrations:
                routeOfAdministrations_id = []
                roa = RouteOfAdministration.objects.create(
                    name=i
                )
                routeOfAdministrations_id.append(roa.id)
            for brand in brands:
                brands_id = []
                brands = Brand.objects.create(
                    name=brand
                )
                brands_id.append(brands.id)
            for ingredient in ingredients:
                ingredients_id = []
                ing = Ingredient.objects.create(
                    name=ingredient
                )
                ingredients_id.append(ing.id)

            super_admin = Users.objects.get(phone_number='+8801752495467')
            for i in range(20):
                base_product = BaseProduct.objects.create(
                    superadmin=super_admin,
                    name=fake.name(),
                    description=fake.name(),
                    dosage_form=fake.name(),
                    manufacturer_id=random.choice(Manufacturer_id),
                    brand_id=random.choice(brands_id),
                    route_of_administration_id=random.choice(routeOfAdministrations_id),
                    medicine_physical_state_id=random.choice(medicinePhysicalStates_id)
                )
                base_product.category.add(random.choice(categories_id))
                base_product.active_ingredient.add(random.choice(ingredients_id))
