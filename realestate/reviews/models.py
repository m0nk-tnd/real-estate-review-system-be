from django.db import models

from .testimonials import Review


class TenantReview(Review):
    pass


class LandlordReview(Review):
    pass
