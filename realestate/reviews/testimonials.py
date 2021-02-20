from django.db import models


class Review(models.Model):
    class Rating(models.IntegerChoices):
        rating1 = 1
        rating2 = 2
        rating3 = 3
        rating4 = 4
        rating5 = 5

    title = models.CharField('Название', max_length=50)
    description = models.CharField('Описание', max_length=200)
    rating = models.IntegerField(choices=Rating.choices)

    class Meta:
        abstract = True
