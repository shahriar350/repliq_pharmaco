from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import Category
from admin_app.serializers import CategorySerializers
from auth_app.models import Users

CATEGORY_URL = reverse('superadmin:category.list.create')

def detail_category(uuid):
    """Create and return a detail URL."""
    return reverse('superadmin:category.retrieve.update.remove', args=[uuid])


# def delete_url(category_id):
#     """Create and return a delete URL."""
#     return reverse('superadmin:category.delete', args=[category_id])


# def remove_url(category_id):
#     """Create and return a remove URL."""
#     return reverse('superadmin:category.remove', args=[category_id])


def create_category(**params):
    """Create and return a category."""
    defaults = {
        'name': 'test string',
        'parent': None
    }
    defaults.update(params)
    category = Category.objects.create(**defaults)
    return category


class CategoryTestcases(APITestCase):
    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')
        superadmin = Users.objects.create_superuser(
            name='shiblu',
            phone_number='+8801752495467',
            password="123456"
        )

        login = {
            'phone_number': "+8801752495467",
            'password': "123456"
        }
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

    """Test for Category API"""

    def test_list_category(self):
        """Test listing category."""
        create_category()
        create_category()

        response = self.client.get(CATEGORY_URL)
        category = Category.objects.all()
        serializer = CategorySerializers(category, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_category(self):
        """Test creating a category."""
        payload = {
            'name': 'parasitamol',
            'parent': None
        }
        response = self.client.post(CATEGORY_URL, payload, format='json')
        category = Category.objects.get(uuid=response.data['uuid'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], category.name)

    def test_retrieve_category(self):
        """Test retrieve a category."""
        category1 = create_category()
        category2 = create_category()
        url = detail_category(category1.uuid)
        response = self.client.get(url)
        category = Category.objects.get(uuid=category1.uuid)
        serializer = CategorySerializers(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_category(self):
        """Test update a category."""
        category = create_category()

        payload = {
            'name': 'updated string',
        }
        url = detail_category(category.uuid)
        response = self.client.put(url, payload)
        category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], category.name)

    def test_patch_category(self):
        """Test patch a category."""
        category = create_category()

        payload = {
            'name': 'partial update string',
        }
        url = detail_category(category.uuid)
        response = self.client.patch(url, payload)
        category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], category.name)

    # def test_delete_category(self):
    #     """Test deleteing a category."""
    #     category = create_category()
    #     url = delete_url(category.id)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Category.objects.filter(id=category.id).exists())

    def test_remove_category(self):
        """Test remove a category."""
        category = create_category()
        url = detail_category(category.uuid)
        response = self.client.delete(url)
        category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(category.deleted_at == None)


