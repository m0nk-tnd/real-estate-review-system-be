from django.contrib import admin

from .models import TenantProfile, LandlordProfile

admin.site.register(TenantProfile)
admin.site.register(LandlordProfile)
