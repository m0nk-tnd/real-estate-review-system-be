from django.db import models


class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    rating = models.IntegerField(max_length=1)

    class Meta:
        abstract = True
