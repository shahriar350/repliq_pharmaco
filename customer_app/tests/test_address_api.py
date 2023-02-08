from django.urls import reverse
from rest_framework.test import APITestCase

from admin_app.models import District
from auth_app.models import Users
from auth_app.models import UserAddress
from customer_app.serializers import AddressCRUDSerializers


class TestAddressAPI(APITestCase):

    def setUp(self) -> None:
        loginurl = reverse('auth:token_obtain_pair')
        self.user = Users.objects.create_user(
            name="shiblu",
            phone_number="+8801752495466",
            password="123456"
        )
        login = {
            'phone_number': "+8801752495466",
            'password': "123456"
        }
        self.district = District.objects.create(name='dhaka')
        res = self.client.post(loginurl, login, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

        self.address = UserAddress.objects.create(
            user=self.user,
            house='string',
            street="string",
            post_office="string",
            police_station="string",
            district=self.district,
            country="string",
            state="string"
        )

        UserAddress.objects.create(
            user=self.user,
            house='string',
            street="string",
            post_office="string",
            police_station="string",
            district=self.district,
            country="string",
            state="string"
        )

    def test_list_address(self):
        url = reverse('customer:address.list')

        response = self.client.get(url)
        address = UserAddress.objects.all()
        serializer = AddressCRUDSerializers(address, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_address(self):
        """Test creating address."""

        url = reverse('customer:address.create')

        payload = {
            "house": "string",
            "street": "string",
            "post_office": "string",
            "police_station": "string",
            'district': self.district.id,
            "country": "string",
            "state": "string"
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 201)

    def test_retrieve_address(self):
        """Test retrieve a address."""

        url = reverse('customer:address.retrieve.update.destroy', kwargs={'uuid': self.address.uuid})
        response = self.client.get(url)
        address = UserAddress.objects.get(id=self.address.id)
        serializer = AddressCRUDSerializers(address)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update_address(self):
        """Test update a address."""

        payload = {
            "house": "string2",
            "street": "string2",
            "post_office": "string2",
            "police_station": "string2",
            "district": self.district.id,
            "country": "strin2g",
            "state": "stri2ng"
        }

        url = reverse('customer:address.retrieve.update.destroy', kwargs={'uuid': self.address.uuid})
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, 200)

    def test_patch_address(self):
        """Test patch address."""

        payload = {
            'country': 'BD',
        }
        url = reverse('customer:address.retrieve.update.destroy', kwargs={'uuid': self.address.uuid})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 200)

    def test_delete_address(self):
        """Test deleteing address."""

        url = reverse('customer:address.retrieve.update.destroy', kwargs={'uuid': self.address.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(UserAddress.objects.filter(id=self.address.id).exists())
