import datetime
import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from property.models import Property
from property.factories import CityFactory
from property.serializers import PropertySerializer
from property.views import PropertyList
from users.models import LandlordProfile

client = Client()


class PropertyListTest(APITestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.property1 = Property.objects.create(landlord=self.landlord, name='my property1', address='my address1',
                                                 city=self.city)
        self.property2 = Property.objects.create(landlord=self.landlord, name='my property2', address='my address2',
                                                 city=self.city)
        self.client.force_authenticate(self.user1)
        self.factory = RequestFactory()

    def test_get_all_properties(self):
        response = self.client.get(reverse('property:properties_list_create'))
        properties = Property.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(response.data['results'], serializer.data)


class PropertyCreateTest(APITestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('Pas$w0rd')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.valid_form = {
            'landlord': self.landlord.pk,
            'name': 'my prop',
            'address': 'spb',
            'city': self.city.pk,
            'building_type': 'house',
            'overall_floors': 14,
            'floor': 2,
            'decoration': False,
            'overall_square': 200.8,
            'living_square': 180.0,
            'kitchen_square': 20.0,
            'view': 'nice',
            'balcony': True
        }

        self.invalid_form = {
            'landlord': self.landlord.pk,
            'name': '',
            'address': 'spb',
            'city': self.city.pk,
            'building_type': 'house',
            'overall_floors': 14,
            'floor': 2,
            'decoration': False,
            'overall_square': 200.8,
            'living_square': 180.0,
            'kitchen_square': 20.0,
            'view': 'nice',
            'balcony': True
        }

        self.invalid_form2 = {
            'landlord': self.landlord.pk,
            'name': '',
            'address': 'spb',
            'city': self.city.pk,
            'building_type': 'house',
            'overall_floors': 14,
            'floor': 2,
            'decoration': False,
            'overall_square': 200.8,
            'living_square': 180.0,
            'kitchen_square': -20.0,
            'view': 'nice',
            'balcony': True
        }

    def test_create_valid_property(self):
        self.client.force_authenticate(self.user1)
        # self.assertTrue(self.client.login(username='anna123', password='Pas$w0rd'))
        response = self.client.post(
            reverse('property:properties_list_create'),
            data=json.dumps(self.valid_form),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_property(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            reverse('property:properties_list_create'),
            data=json.dumps(self.invalid_form),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_property_2(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            reverse('property:properties_list_create'),
            data=json.dumps(self.invalid_form2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSinglePropertyTest(APITestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.client.force_authenticate(self.user1)
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.property = Property.objects.create(landlord=self.landlord, name='my property1', address='my address1',
                                                city=self.city)

    def test_get_valid_property(self):
        response = self.client.get(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}))
        prop = Property.objects.get(id=self.property.id)
        serializer = PropertySerializer(prop)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_property(self):
        response = self.client.get(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PropertyUpdateTest(APITestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.property = Property.objects.create(landlord=self.landlord, name='my property1', address='my address1',
                                                city=self.city)
        self.valid_form = {
            'landlord': self.landlord.pk,
            'name': 'my prop',
            'address': 'spb',
            'city': self.city.pk,
            'building_type': 'house',
            'overall_floors': 14,
            'floor': 2,
            'decoration': False,
            'overall_square': 200.8,
            'living_square': 180.0,
            'kitchen_square': 20.0,
            'view': 'nice',
            'balcony': True
        }

        self.invalid_form = {
            'landlord': self.landlord.pk,
            'name': '',
            'address': 'spb',
            'city': self.city.pk,
            'building_type': 'house',
            'overall_floors': 14,
            'floor': 2,
            'decoration': False,
            'overall_square': 200.8,
            'living_square': 180.0,
            'kitchen_square': -20.0,
            'view': 'nice',
            'balcony': True
        }

    def test_valid_update_property(self):
        self.client.force_authenticate(self.user1)
        response = self.client.put(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}),
            data=json.dumps(self.valid_form),
            content_type='application/json'
        )
        prop = Property.objects.get(id=self.property.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(prop.name, 'my prop')

    def test_invalid_update_property(self):
        self.client.force_authenticate(self.user1)
        response = self.client.put(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}),
            data=json.dumps(self.invalid_form),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PropertyDeleteTest(APITestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.client.force_authenticate(self.user1)
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.property = Property.objects.create(landlord=self.landlord, name='my property1', address='my address1',
                                                city=self.city)

    def test_valid_delete_property(self):
        self.assertEqual(Property.objects.all().count(), 1)
        response = self.client.delete(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.all().count(), 0)

    def test_invalid_delete_property(self):
        response = self.client.delete(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
