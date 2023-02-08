# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls  import reverse
#
# from admin_app.models import Attribute
# from admin_app.serializers import AttributeSerializers
#
#
# ATTRIBUTE_URL = reverse('superadmin:attribute.list.create')
#
# def detail_attribute(attribute_id):
#     """Create and return a detail URL."""
#     return reverse('superadmin:attribute.retrieve.update', args=[attribute_id])
#
# def delete_url(attribute_id):
#     """Create and return a delete URL."""
#     return reverse('superadmin:attribute.delete', args=[attribute_id])
#
# def remove_url(attribute_id):
#     """Create and return a remove URL."""
#     return reverse('superadmin:attribute.remove', args=[attribute_id])
#
# def create_attribute(**params):
#     """Create and return a attribute."""
#     defaults = {
#         'name':'test string',
#     }
#     defaults.update(params)
#     attribute = Attribute.objects.create(**defaults)
#     return attribute
#
#
# class AttributeTestcases(APITestCase):
#     """Test for Attribute API"""
#
#     def test_list_attribute(self):
#         """Test listing attribute."""
#         create_attribute()
#         create_attribute()
#
#         response = self.client.get(ATTRIBUTE_URL)
#         attribute = Attribute.objects.all()
#         serializer = AttributeSerializers(attribute, many=True)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)
#
#     def test_create_attribute(self):
#         """Test creating a attribute."""
#         payload = {
#             'name':'parasitamol',
#         }
#         response = self.client.post(ATTRIBUTE_URL, payload, format='json')
#         attribute = Attribute.objects.get(id=response.data['id'])
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['name'], attribute.name)
#
#     def test_retrieve_attribute(self):
#         """Test retrieve a attribute."""
#         attribute1 = create_attribute()
#         attribute2 = create_attribute()
#         url = detail_attribute(attribute1.id)
#         response = self.client.get(url)
#         attribute = Attribute.objects.get(id=attribute1.id)
#         serializer = AttributeSerializers(attribute)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)
#
#     def test_update_attribute(self):
#         """Test update a attribute."""
#         attribute = create_attribute()
#
#         payload = {
#             'name':'updated string',
#         }
#         url = detail_attribute(attribute.id)
#         response = self.client.put(url, payload)
#         attribute.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], attribute.name )
#
#     def test_patch_attribute(self):
#         """Test patch a attribute."""
#         attribute = create_attribute()
#
#         payload = {
#             'name':'partial update string',
#         }
#         url = detail_attribute(attribute.id)
#         response = self.client.patch(url, payload)
#         attribute.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], attribute.name )
#
#     def test_delete_attribute(self):
#         """Test deleteing a attribute."""
#         attribute = create_attribute()
#         url = delete_url(attribute.id)
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Attribute.objects.filter(id=attribute.id).exists())
#
#     def test_remove_attribute(self):
#         """Test remove a attribute."""
#         attribute = create_attribute()
#         url = remove_url(attribute.id)
#         response = self.client.delete(url)
#         attribute.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(attribute.deleted_at == None)
