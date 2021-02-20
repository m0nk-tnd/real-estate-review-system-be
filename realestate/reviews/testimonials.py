from django.db import models


class Review(models.Model):
    RATING_CHOICE = tuple((i, str(i)) for i in range(1, 6))

    title = models.CharField('Название', max_length=50)
    description = models.CharField('Описание', max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICE, default=RATING_CHOICE[0])

    class Meta:
        abstract = True
