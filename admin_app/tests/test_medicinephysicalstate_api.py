from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from admin_app.models import MedicinePhysicalState
from admin_app.serializers import MedicinePhysicalStateSerializers
from auth_app.models import Users

MEDICINEPHYSICALSTATE_URL = reverse('superadmin:medicinePhysicalState.list.create')


def detail_medicinePhysicalState(uuid):
    """Create and return a detail URL."""
    return reverse('superadmin:medicinePhysicalState.retrieve.update.remove', args=[uuid])


# def delete_url(medicinePhysicalState_uuid):
#     """Create and return a delete URL."""
#     return reverse('superadmin:medicinePhysicalState.delete', args=[medicinePhysicalState_uuid])


# def remove_url(medicinePhysicalState_uuid):
#     """Create and return a remove URL."""
#     return reverse('superadmin:medicinePhysicalState.remove', args=[medicinePhysicalState_uuid])


def create_medicinePhysicalState(**params):
    """Create and return a medicinePhysicalState."""
    defaults = {
        'name': 'test string',
    }
    defaults.update(params)
    medicinePhysicalState = MedicinePhysicalState.objects.create(**defaults)
    return medicinePhysicalState


class MedicinePhysicalStateTestcases(APITestCase):
    """Test for medicinePhysicalState API"""

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

    def test_list_medicinePhysicalState(self):
        """Test listing medicinePhysicalState."""
        create_medicinePhysicalState()
        create_medicinePhysicalState()

        response = self.client.get(MEDICINEPHYSICALSTATE_URL)
        medicinePhysicalState = MedicinePhysicalState.objects.all()
        serializer = MedicinePhysicalStateSerializers(medicinePhysicalState, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_medicinePhysicalState(self):
        """Test creating a medicinePhysicalState."""
        payload = {
            'name': 'test string',
        }
        response = self.client.post(MEDICINEPHYSICALSTATE_URL, payload, format='json')
        medicinePhysicalState = MedicinePhysicalState.objects.get(uuid=response.data['uuid'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], medicinePhysicalState.name)

    def test_retrieve_medicinePhysicalState(self):
        """Test retrieve a medicinePhysicalState."""
        medicinePhysicalState1 = create_medicinePhysicalState()
        medicinePhysicalState2 = create_medicinePhysicalState()
        url = detail_medicinePhysicalState(medicinePhysicalState1.uuid)
        response = self.client.get(url)
        medicinePhysicalState = MedicinePhysicalState.objects.get(uuid=medicinePhysicalState1.uuid)
        serializer = MedicinePhysicalStateSerializers(medicinePhysicalState)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_medicinePhysicalState(self):
        """Test update a medicinePhysicalState."""
        medicinePhysicalState = create_medicinePhysicalState()

        payload = {
            'name': 'updated string',
        }
        url = detail_medicinePhysicalState(medicinePhysicalState.uuid)
        response = self.client.put(url, payload)
        medicinePhysicalState.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], medicinePhysicalState.name)

    def test_patch_medicinePhysicalState(self):
        """Test patch a medicinePhysicalState."""
        medicinePhysicalState = create_medicinePhysicalState()

        payload = {
            'name': 'partial update string',
        }
        url = detail_medicinePhysicalState(medicinePhysicalState.uuid)
        response = self.client.patch(url, payload)
        medicinePhysicalState.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], medicinePhysicalState.name)

    # def test_delete_medicinePhysicalState(self):
    #     """Test deleteing a medicinePhysicalState."""
    #     medicinePhysicalState = create_medicinePhysicalState()
    #     url = delete_url(medicinePhysicalState.uuid)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(MedicinePhysicalState.objects.filter(uuid=medicinePhysicalState.uuid).exists())

    def test_remove_medicinePhysicalState(self):
        """Test remove a medicinePhysicalState."""
        medicinePhysicalState = create_medicinePhysicalState()
        url = detail_medicinePhysicalState(medicinePhysicalState.uuid)
        response = self.client.delete(url)
        medicinePhysicalState.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(medicinePhysicalState.deleted_at == None)
