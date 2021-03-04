from rest_framework import serializers
from property.models import Property, City


class PropertySerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        allow_null=True
    )

    class Meta:
        model = Property
        fields = ['name', 'address', 'description', 'city']
