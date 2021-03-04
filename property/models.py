from django.db import models
from cities_light.abstract_models import (AbstractCity, AbstractRegion, AbstractCountry, AbstractSubRegion)
from cities_light.receivers import connect_default_signals
from images.models import ImageAlbum, Image


class Country(AbstractCountry):
    pass


connect_default_signals(Country)


class Region(AbstractRegion):
    pass


connect_default_signals(Region)


class SubRegion(AbstractSubRegion):
    pass


connect_default_signals(SubRegion)


class City(AbstractCity):
    timezone = models.CharField(max_length=40)


connect_default_signals(City)


class Property(models.Model):
    # landlord = models.ForeignKey(Landlord, related_name='landlord', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    address = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(City, related_name='city', on_delete=models.CASCADE, blank=True, null=True)
    album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.city}"
