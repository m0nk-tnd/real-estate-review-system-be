from django.db import models
from django.urls import reverse


class Property(models.Model):
    # landlord = models.ForeignKey(Landlord, related_name='landlord', null=True, blank=True)
    name = models.CharField(max_length=150)
    address = models.TextField()
    description = models.TextField()
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} | {self.city}"
