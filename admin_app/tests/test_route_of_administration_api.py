from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import RouteOfAdministration
from admin_app.serializers import RouteOfAdministrationSerializers
from auth_app.models import Users

ROUTEOFADMINISTRATION_URL = reverse('superadmin:routeOfAdministration.list.create')


def detail_routeOfAdministration(uuid):
    """Create and return a detail URL."""
    return reverse('superadmin:routeOfAdministration.retrieve.update.remove', args=[uuid])


# def delete_url(routeOfAdministration_uuid):
#     """Create and return a delete URL."""
#     return reverse('superadmin:routeOfAdministration.delete', args=[routeOfAdministration_uuid])


# def remove_url(routeOfAdministration_uuid):
#     """Create and return a remove URL."""
#     return reverse('superadmin:routeOfAdministration.remove', args=[routeOfAdministration_uuid])


def create_routeOfAdministration(**params):
    """Create and return a routeOfAdministration."""
    defaults = {
        'name': 'test string',
    }
    defaults.update(params)
    routeOfAdministration = RouteOfAdministration.objects.create(**defaults)
    return routeOfAdministration


class RouteOfAdministrationTestcases(APITestCase):
    """Test for routeOfAdministration API"""

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

    def test_list_routeOfAdministration(self):
        """Test listing routeOfAdministration."""
        create_routeOfAdministration()
        create_routeOfAdministration()

        response = self.client.get(ROUTEOFADMINISTRATION_URL)
        routeOfAdministration = RouteOfAdministration.objects.all()
        serializer = RouteOfAdministrationSerializers(routeOfAdministration, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_routeOfAdministration(self):
        """Test creating a routeOfAdministration."""
        payload = {
            'name': 'test string',
        }
        response = self.client.post(ROUTEOFADMINISTRATION_URL, payload, format='json')
        routeOfAdministration = RouteOfAdministration.objects.get(uuid=response.data['uuid'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], routeOfAdministration.name)

    def test_retrieve_routeOfAdministration(self):
        """Test retrieve a routeOfAdministration."""
        routeOfAdministration1 = create_routeOfAdministration()
        routeOfAdministration2 = create_routeOfAdministration()
        url = detail_routeOfAdministration(routeOfAdministration1.uuid)
        response = self.client.get(url)
        routeOfAdministration = RouteOfAdministration.objects.get(uuid=routeOfAdministration1.uuid)
        serializer = RouteOfAdministrationSerializers(routeOfAdministration)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_routeOfAdministration(self):
        """Test update a routeOfAdministration."""
        routeOfAdministration = create_routeOfAdministration()

        payload = {
            'name': 'updated string',
        }
        url = detail_routeOfAdministration(routeOfAdministration.uuid)
        response = self.client.put(url, payload)
        routeOfAdministration.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], routeOfAdministration.name)

    def test_patch_routeOfAdministration(self):
        """Test patch a routeOfAdministration."""
        routeOfAdministration = create_routeOfAdministration()

        payload = {
            'name': 'partial update string',
        }
        url = detail_routeOfAdministration(routeOfAdministration.uuid)
        response = self.client.patch(url, payload)
        routeOfAdministration.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], routeOfAdministration.name)

    # def test_delete_routeOfAdministration(self):
    #     """Test deleteing a routeOfAdministration."""
    #     routeOfAdministration = create_routeOfAdministration()
    #     url = delete_url(routeOfAdministration.uuid)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(RouteOfAdministration.objects.filter(uuid=routeOfAdministration.uuid).exists())

    def test_remove_routeOfAdministration(self):
        """Test remove a routeOfAdministration."""
        routeOfAdministration = create_routeOfAdministration()
        url = detail_routeOfAdministration(routeOfAdministration.uuid)
        response = self.client.delete(url)
        routeOfAdministration.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(routeOfAdministration.deleted_at == None)
