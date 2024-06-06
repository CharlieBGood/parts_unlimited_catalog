from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from parts.models import Part
from parts.tests.factories import PartsFactory

class PartsTests(APITestCase):
    """
    Test parts
    """
    def setUp(self):
        """
        Setting up required values
        """
        self.general_url = reverse('parts-list')
        self.most_common_words_url = reverse('parts-most-common-words')
        self.part_1 = PartsFactory()
        self.part_2 = PartsFactory()
        self.specific_part1_url = reverse('parts-detail', kwargs={"pk":self.part_1.id})

    def test_get_parts(self):
        """
        Test successfully getting all parts entries
        """
        response = self.client.get(self.general_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        part1 = response.data[0]

        self.assertEqual(part1['id'], self.part_1.id)
        self.assertEqual(part1['name'], self.part_1.name)
        self.assertEqual(part1['sku'], self.part_1.sku)
        self.assertEqual(part1['description'], self.part_1.description)
        self.assertEqual(part1['weight_ounces'], self.part_1.weight_ounces)
        self.assertEqual(part1['is_active'], self.part_1.is_active)

        part2 = response.data[1]

        self.assertEqual(part2['id'], self.part_2.id)
        self.assertEqual(part2['name'], self.part_2.name)
        self.assertEqual(part2['sku'], self.part_2.sku)
        self.assertEqual(part2['description'], self.part_2.description)
        self.assertEqual(part2['weight_ounces'], self.part_2.weight_ounces)
        self.assertEqual(part2['is_active'], self.part_2.is_active)

    def test_get_specific_part(self):
        """
        Test successfully retrieve a part based on its id
        """
        response = self.client.get(self.specific_part1_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data['id'], self.part_1.id)
        self.assertEqual(data['name'], self.part_1.name)
        self.assertEqual(data['sku'], self.part_1.sku)
        self.assertEqual(data['description'], self.part_1.description)
        self.assertEqual(data['weight_ounces'], self.part_1.weight_ounces)
        self.assertEqual(data['is_active'], self.part_1.is_active)

    def test_get_unexisting_part(self):
        """
        Test get a part that does not exist.
        """
        self.part_1.delete()

        response = self.client.get(self.specific_part1_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_part(self):
        """
        Test successfully create a part
        """
        payload = {
            "name": "test_part",
            "sku": "123456789",
            "description": "This is a test product",
            "weight_ounces": 23,
            "is_active": 1
        }

        response = self.client.post(self.general_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        part = response.data
        parts = Part.objects.all()

        self.assertEqual(parts.count(), 3)
        self.assertTrue(parts.filter(id=part['id']).exists())
        self.assertEqual(part["name"], payload["name"])
        self.assertEqual(part["sku"], payload["sku"])
        self.assertEqual(part["description"], payload["description"])
        self.assertEqual(part["weight_ounces"], payload["weight_ounces"])
        self.assertEqual(part["is_active"], payload["is_active"])

    def test_create_part_with_invalid_data(self):
        """
        Test create part with invalida data
        """
        payload = {
            "name": "test_part",
            "sku": "12345",
            "description": "This is a test product",
            "weight_ounces": True,
            "is_active": 3
        }

        response = self.client.post(self.general_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data

        self.assertEqual(str(data['weight_ounces'][0]), 'A valid integer is required.')
        self.assertEqual(str(data['is_active'][0]), '"3" is not a valid choice.')

    def test_update_part_data(self):
        """
        Test update part data
        """
        payload = {"name": "temp", "weight_ounces": 15}

        response = self.client.patch(self.specific_part1_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.part_1.refresh_from_db()

        self.assertAlmostEqual(self.part_1.name, payload["name"])
        self.assertAlmostEqual(self.part_1.weight_ounces, payload["weight_ounces"])


    def test_update_unexisting_part(self):
        """
        Test update a part that does not exist
        """
        self.part_1.delete()

        payload = {"name": "temp", "weight_ounces": 15}

        response = self.client.patch(self.specific_part1_url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_part_with_invalid_data(self):
        """
        Test update a part with invalid data
        """
        payload = {"weight_ounces": "hi", "is_active": 3, "sku": "a"*31}

        response = self.client.patch(self.specific_part1_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.data

        self.assertEqual(str(data['weight_ounces'][0]), 'A valid integer is required.')
        self.assertEqual(str(data['is_active'][0]), '"3" is not a valid choice.')
        self.assertEqual(str(data['sku'][0]), 'Ensure this field has no more than 30 characters.')

    
    def test_delete_part(self):
        """
        Test delete existing part
        """
        response = self.client.delete(self.specific_part1_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        parts = Part.objects.all()
        self.assertEqual(parts.count(), 1)
        self.assertFalse(parts.filter(id=self.part_1.id).exists())

    def test_delete_unexisting_part(self):
        """
        Test delete unexisting part
        """
        self.part_1.delete()

        response = self.client.delete(self.specific_part1_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_most_common_words(self):
        """
        Test get five most common words
        """
        Part.objects.filter(id=self.part_1.id).update(description="one two two three three three four four four four")
        Part.objects.filter(id=self.part_2.id).update(description="five five five five five six six six six six six")

        response = self.client.get(self.most_common_words_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        most_common_words = data['most_common_words']
        self.assertEqual(len(most_common_words), 5)
        self.assertEqual(most_common_words[0], 'six')
        self.assertEqual(most_common_words[1], 'five')
        self.assertEqual(most_common_words[2], 'four')
        self.assertEqual(most_common_words[3], 'three')
        self.assertEqual(most_common_words[4], 'two')

        