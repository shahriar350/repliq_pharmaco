from decimal import Decimal

from accountio.models import Domain, Organization, OrganizationUser
from catalogio.models import Category, Manufacturer, Supplier, MedicinePhysicalState, RouteOfAdministration, Brand, \
    Ingredient, BaseProduct, Product
from core.models import User



# TODO cart tests

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
    for brand in brands:
        Brand.objects.create(
            name=brand
        )
    for ingredient in ingredients:
        Ingredient.objects.create(
            name=ingredient
        )
    owner = User.objects.create_user(
        name="saifullah",
        phone="+8801752495466",
        password="123456"
    )
    superadmin = User.objects.create_superuser(
        name="saifullah",
        phone="+8801752495423",
        password="123456"
    )

    org = Organization.objects.create(
        name='bac'
    )
    OrganizationUser.objects.create(
        organization=org,
        user=owner,
        role='owner'
    )

    base1 = BaseProduct.objects.create(
        name='Napa normal',
        description='hello',
        dosage_form='first',
        superadmin=superadmin,
        manufacturer_id=1,
        brand_id=1,
        route_of_administration_id=1,
        medicine_physical_state_id=1,
    )
    base2 = BaseProduct.objects.create(
        name='Para norpol',
        description='hello',
        dosage_form='first',
        superadmin=superadmin,
        manufacturer_id=1,
        brand_id=1,
        route_of_administration_id=1,
        medicine_physical_state_id=1,
    )
    base1.categories.add(1)
    base2.categories.add(1)
    base1.categories.add(2)
    base2.categories.add(2)
    base1.active_ingredients.add(1)
    base2.active_ingredients.add(1)

    baseproduct = BaseProduct.objects.create(
        name='saifullah shahen',
        description='hello',
        dosage_form='first',
        manufacturer_id=1,
        brand_id=1,
        route_of_administration_id=1,
        medicine_physical_state_id=1,
    )

    baseproduct.categories.add(1)
    baseproduct.categories.add(2)
    baseproduct.active_ingredients.add(1)
    prod = Product.objects.create(
        base_product=baseproduct,
        merchant=owner,
        organization=org,
        stock=100,
        selling_price=Decimal('100'),
        buying_price=Decimal('100')
    )
    baseproduct.merchant_product = prod
    baseproduct.save()
