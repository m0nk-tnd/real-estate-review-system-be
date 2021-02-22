from django.db import models


class City(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} | {self.country}"


class Property(models.Model):
    # landlord = models.ForeignKey(Landlord, related_name='landlord', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150)
    address = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(City, related_name='city', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.city}"
