import factory
from .models import City, Country


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ('name',)

    name = 'Russia'


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = ('name',)

    name = 'Moscow'
    country = factory.SubFactory(CountryFactory)
