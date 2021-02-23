from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        abstract = True


class TenantReview(Review):
    pass


class LandlordReview(Review):
    pass
