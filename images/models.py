from django.db import models


class ImageAlbum(models.Model):
    name = models.CharField(max_length=255, default='UnknownAlbum')

    def __str__(self):
        return f"{self.name}"

    def get_images(self):
        return self.images.all()


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.album.name}"
