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
                                                city=self.city, building_type='house', overall_floors=12, floor=4,
                                                decoration=True, overall_square=400.8, living_square=301.2,
                                                kitchen_square=30, view='nice', balcony=False)

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

    def test_city_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_building_type_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('building_type').verbose_name
        self.assertEquals(field_label, 'building type')

    def test_overall_floors_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('overall_floors').verbose_name
        self.assertEquals(field_label, 'overall floors')

    def test_floor_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('floor').verbose_name
        self.assertEquals(field_label, 'floor')

    def test_decoration_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('decoration').verbose_name
        self.assertEquals(field_label, 'decoration')

    def test_overall_square_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('overall_square').verbose_name
        self.assertEquals(field_label, 'overall square')

    def test_living_square_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('living_square').verbose_name
        self.assertEquals(field_label, 'living square')

    def test_kitchen_square_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('kitchen_square').verbose_name
        self.assertEquals(field_label, 'kitchen square')

    def test_view_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('view').verbose_name
        self.assertEquals(field_label, 'view')

    def test_balcony_label(self):
        prop = Property.objects.get(id=self.property.id)
        field_label = prop._meta.get_field('balcony').verbose_name
        self.assertEquals(field_label, 'balcony')

    def test_name_max_length(self):
        prop = Property.objects.get(id=self.property.id)
        max_length = prop._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_view_max_length(self):
        prop = Property.objects.get(id=self.property.id)
        max_length = prop._meta.get_field('view').max_length
        self.assertEquals(max_length, 255)

    def test_str(self):
        prop = Property.objects.get(id=self.property.id)
        expected = f"{prop.name} | {prop.city}"
        self.assertEquals(expected, str(prop))
