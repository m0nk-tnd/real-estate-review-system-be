from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import TenantProfile, LandlordProfile
from property.models import Property


class Review(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        abstract = True


class TenantReview(Review):
    reviewer = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    review_on = models.ForeignKey(TenantProfile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Review on: {self.review_on} by {self.reviewer}'


class LandlordReview(Review):
    reviewer = models.ForeignKey(TenantProfile, on_delete=models.CASCADE, null=True)
    review_on = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Review on: Landlord - {self.review_on} by {self.reviewer}'
