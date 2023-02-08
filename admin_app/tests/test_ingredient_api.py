from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import Ingredient
from admin_app.serializers import IngredientSerializers
from auth_app.models import Users

INGREDIENT_URL = reverse('superadmin:ingredient.list.create')


def detail_ingredient(uuid):
    """Create and return a detail URL."""
    return reverse('superadmin:ingredient.retrieve.update.remove', args=[uuid])


# def delete_url(ingredient_id):
#     """Create and return a delete URL."""
#     return reverse('superadmin:ingredient.delete', args=[ingredient_id])


# def remove_url(ingredient_id):
#     """Create and return a remove URL."""
#     return reverse('superadmin:ingredient.remove', args=[ingredient_uuid])


def create_ingredient(**params):
    """Create and return a ingredient."""
    defaults = {
        'name': 'test string',
    }
    defaults.update(params)
    ingredient = Ingredient.objects.create(**defaults)
    return ingredient


class IngredientTestcases(APITestCase):
    """Test for ingredient API"""

    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')
        superadmin = Users.objects.create_superuser(
            name='saifullah',
            phone_number='+8801752495467',
            password="123456"
        )

        login = {
            'phone_number': "+8801752495467",
            'password': "123456"
        }
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

    def test_list_ingredient(self):
        """Test listing ingredient."""
        create_ingredient()
        create_ingredient()

        response = self.client.get(INGREDIENT_URL)
        ingredient = Ingredient.objects.all()
        serializer = IngredientSerializers(ingredient, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_ingredient(self):
        """Test creating a ingredient."""
        payload = {
            'name': 'parasitamol',
        }
        response = self.client.post(INGREDIENT_URL, payload, format='json')
        ingredient = Ingredient.objects.get(uuid=response.data['uuid'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], ingredient.name)

    def test_retrieve_ingredient(self):
        """Test retrieve a ingredient."""
        ingredient1 = create_ingredient()
        ingredient2 = create_ingredient()
        url = detail_ingredient(ingredient1.uuid)
        response = self.client.get(url)
        ingredient = Ingredient.objects.get(uuid=ingredient1.uuid)
        serializer = IngredientSerializers(ingredient)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_ingredient(self):
        """Test update a ingredient."""
        ingredient = create_ingredient()

        payload = {
            'name': 'updated string',
        }
        url = detail_ingredient(ingredient.uuid)
        response = self.client.put(url, payload)
        ingredient.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], ingredient.name)

    def test_patch_ingredient(self):
        """Test patch a ingredient."""
        ingredient = create_ingredient()

        payload = {
            'name': 'partial update string',
        }
        url = detail_ingredient(ingredient.uuid)
        response = self.client.patch(url, payload)
        ingredient.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], ingredient.name)

    # def test_delete_ingredient(self):
    #     """Test deleteing a ingredient."""
    #     ingredient = create_ingredient()
    #     url = delete_url(ingredient.uuid)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Ingredient.objects.filter(uuid=ingredient.uuid).exists())

    def test_remove_ingredient(self):
        """Test remove a ingredient."""
        ingredient = create_ingredient()
        url = detail_ingredient(ingredient.uuid)
        response = self.client.delete(url)
        ingredient.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ingredient.deleted_at == None)
