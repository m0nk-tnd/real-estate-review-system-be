from rest_framework import serializers
from .models import Property, City
from users.models import LandlordProfile


class PropertySerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        allow_null=True
    )

    landlord = serializers.PrimaryKeyRelatedField(
        queryset=LandlordProfile.objects.all(),
        allow_null=False
    )

    class Meta:
        model = Property
        fields = ['landlord', 'name', 'address', 'description', 'city']
