from django.contrib import admin
from .models import TenantReview, LandlordReview

admin.site.register(TenantReview)
admin.site.register(LandlordReview)
