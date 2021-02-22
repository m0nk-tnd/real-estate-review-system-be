from django.test import TestCase
from property.models import Property, City


class CityModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Moscow', country='Russia')

    def test_name_label(self):
        city = City.objects.get(id=1)
        field_label = city._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_country_label(self):
        city = City.objects.get(id=1)
        field_label = city._meta.get_field('country').verbose_name
        self.assertEquals(field_label, 'country')

    def test_name_max_length(self):
        city = City.objects.get(id=1)
        max_length = city._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_country_max_length(self):
        city = City.objects.get(id=1)
        max_length = city._meta.get_field('country').max_length
        self.assertEquals(max_length, 255)

    def test_str(self):
        city = City.objects.get(id=1)
        expected = f"{city.name} | {city.country}"
        self.assertEquals(expected, str(city))


class PropertyModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Moscow', country='Russia')
        self.property = Property.objects.create(name='my property', address='my address',
                                                description='no description', city=self.city)

    def test_name_label(self):
        prop = Property.objects.get(id=1)
        field_label = prop._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_address_label(self):
        prop = Property.objects.get(id=1)
        field_label = prop._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_description_label(self):
        prop = Property.objects.get(id=1)
        field_label = prop._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_city_label(self):
        prop = Property.objects.get(id=1)
        field_label = prop._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_name_max_length(self):
        prop = Property.objects.get(id=1)
        max_length = prop._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_str(self):
        prop = Property.objects.get(id=1)
        expected = f"{prop.name} | {prop.city}"
        self.assertEquals(expected, str(prop))
