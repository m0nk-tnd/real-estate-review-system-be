from rest_framework import serializers
from .models import Property, City
from users.models import LandlordProfile


class PropertySerializer(serializers.ModelSerializer):
    # city = serializers.PrimaryKeyRelatedField(
    #     queryset=City.objects.all(),
    #     allow_null=True
    # )
    city = serializers.StringRelatedField()

    landlord = serializers.PrimaryKeyRelatedField(
        queryset=LandlordProfile.objects.all(),
        allow_null=False
    )

    class Meta:
        model = Property
        fields = ['landlord', 'name', 'address', 'city', 'building_type', 'overall_floors', 'floor', 'decoration',
                  'overall_square', 'living_square', 'kitchen_square', 'view', 'balcony']
