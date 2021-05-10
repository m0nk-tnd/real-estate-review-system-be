import datetime
import json

from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from property.models import Property
from property.factories import CityFactory
from property.serializers import PropertySerializer
from users.models import LandlordProfile

client = Client()


class PropertyListTest(TestCase):
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

    def test_get_all_properties(self):
        response = client.get(reverse('property:properties_list_create'))
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PropertyCreateTest(TestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.valid_form = {
            'landlord': self.landlord.pk,
            'name': 'my prop',
            'address': 'spb',
            'city': self.city.pk,
            'living_square': 40.6
        }

        self.invalid_form = {
            'landlord': self.landlord.pk,
            'name': '',
            'address': 'spb',
            'city': self.city.pk
        }

        self.invalid_form2 = {
            'landlord': self.landlord.pk,
            'name': '',
            'address': 'spb',
            'city': self.city.pk,
            'living_square': -0.5
        }

    def test_create_valid_property(self):
        response = client.post(
            reverse('property:properties_list_create'),
            data=json.dumps(self.valid_form),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_property(self):
        response = client.post(
            reverse('property:properties_list_create'),
            data=json.dumps(self.invalid_form),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_property_2(self):
        response = client.post(
            reverse('property:properties_list_create'),
            data=json.dumps(self.invalid_form2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSinglePropertyTest(TestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.property = Property.objects.create(landlord=self.landlord, name='my property1', address='my address1',
                                                city=self.city)

    def test_get_valid_property(self):
        response = client.get(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}))
        prop = Property.objects.get(id=self.property.id)
        serializer = PropertySerializer(prop)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_property(self):
        response = client.get(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PropertyUpdateTest(TestCase):
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
            'balcony': True,
            'overall_square': 0.0
        }

        self.invalid_form = {
            'landlord': self.landlord.pk,
            'name': '',
            'address': 'spb',
            'city': self.city.pk,
            'balcony': True,
            'overall_square': 0.0
        }

    def test_valid_update_property(self):
        response = client.put(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}),
            data=json.dumps(self.valid_form),
            content_type='application/json'
        )
        prop = Property.objects.get(id=self.property.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(prop.name, 'my prop')

    def test_invalid_update_property(self):
        response = client.put(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}),
            data=json.dumps(self.invalid_form),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PropertyDeleteTest(TestCase):
    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.property = Property.objects.create(landlord=self.landlord, name='my property1', address='my address1',
                                                city=self.city)

    def test_valid_delete_property(self):
        self.assertEqual(Property.objects.all().count(), 1)
        response = client.delete(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': self.property.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.all().count(), 0)

    def test_invalid_delete_property(self):
        response = client.delete(
            reverse('property:property_retrieve_update_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
