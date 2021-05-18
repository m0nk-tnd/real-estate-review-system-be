from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField


class ImageAlbum(models.Model):
    name = models.CharField(max_length=255, default='UnknownAlbum')

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField('Image', upload_to='images/', ppoi_field='image_ppoi', null=True, blank=True)
    image_ppoi = PPOIField()

    def __str__(self):
        return f"{self.name}"
