import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from property.models import Property, City
from property.factories import CityFactory
from users.models import LandlordProfile


class PropertyModelTest(TestCase):

    def setUp(self):
        self.city = CityFactory()
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.property = Property.objects.create(landlord=self.landlord, name='my property', address='my address',
                                                description='no description', city=self.city)

    def test_landlord_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('landlord').verbose_name
        self.assertEquals(field_label, 'landlord')

    def test_name_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_address_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_description_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_city_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_name_max_length(self):
        prop = Property.objects.get(id=self.property.id)
        max_length = prop._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_str(self):
        prop = Property.objects.get(id=self.property.id)
        expected = f"{prop.name} | {prop.city}"
        self.assertEquals(expected, str(prop))
