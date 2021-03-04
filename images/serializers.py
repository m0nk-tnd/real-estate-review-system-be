from rest_framework import serializers

from .models import TenantProfile, LandlordProfile


class TenantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = ['user', 'firstname', 'lastname', 'middlename', 'birth_date']


class LandlordProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = ['firstname', 'lastname']
