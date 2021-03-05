from django.db import models
from cities_light.abstract_models import (AbstractCity, AbstractRegion, AbstractCountry, AbstractSubRegion)
from cities_light.receivers import connect_default_signals
from images.models import ImageAlbum


class IncludedManager(models.Manager):
    def get_queryset(self):
        return super(IncludedManager, self).get_queryset().filter(included=True)


class Country(AbstractCountry):
    included = models.BooleanField(default=False)
    objects = models.Manager()
    objects_included = IncludedManager()


connect_default_signals(Country)


class Region(AbstractRegion):
    included = models.BooleanField(default=False)
    objects = models.Manager()
    objects_included = IncludedManager()


connect_default_signals(Region)


class SubRegion(AbstractSubRegion):
    included = models.BooleanField(default=False)
    objects = models.Manager()
    objects_included = IncludedManager()


connect_default_signals(SubRegion)


class City(AbstractCity):
    included = models.BooleanField(default=False)
    timezone = models.CharField(max_length=40)
    objects = models.Manager()
    objects_included = IncludedManager()


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
