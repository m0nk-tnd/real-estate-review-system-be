from django.db import models

from cities_light.abstract_models import (
    AbstractCity, AbstractRegion, AbstractCountry, AbstractSubRegion
)
from cities_light.receivers import connect_default_signals
from images.models import ImageAlbum


class EnabledObjectManager(models.Manager):
    def get_queryset(self):
        return super(EnabledObjectManager, self).get_queryset().filter(enabled=True)

from users.models import LandlordProfile


class Country(AbstractCountry):
    enabled = models.BooleanField(default=False)
    all_objects = models.Manager()
    objects = EnabledObjectManager()


connect_default_signals(Country)


class Region(AbstractRegion):
    enabled = models.BooleanField(default=False)
    all_objects = models.Manager()
    objects = EnabledObjectManager()


connect_default_signals(Region)


class SubRegion(AbstractSubRegion):
    enabled = models.BooleanField(default=False)
    all_objects = models.Manager()
    objects = EnabledObjectManager()


connect_default_signals(SubRegion)


class City(AbstractCity):
    enabled = models.BooleanField(default=False)
    timezone = models.CharField(max_length=40)
    all_objects = models.Manager()
    objects = EnabledObjectManager()


connect_default_signals(City)


class Property(models.Model):
    landlord = models.ForeignKey(LandlordProfile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    address = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(City, related_name='city', on_delete=models.CASCADE, blank=True, null=True)
    album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.city}"
