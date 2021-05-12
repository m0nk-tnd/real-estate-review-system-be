from rest_framework import serializers
from .models import Property, City
from users.models import LandlordProfile


class PropertySerializer(serializers.ModelSerializer):
    # city = serializers.PrimaryKeyRelatedField(
    #     queryset=City.objects.all(),
    #     allow_null=True
    # )
    city = serializers.StringRelatedField()

    # landlord = serializers.PrimaryKeyRelatedField(
    #     queryset=LandlordProfile.objects.all(),
    #     allow_null=False
    # )

    def validate(self, data):
        if data['overall_floors'] and data['floor']:
            if data['overall_floors'] < data['floor']:
                raise serializers.ValidationError("Overall floors must be bigger or equal to floors")
        if data['overall_square'] and data['living_square']:
            if data['overall_square'] < data['living_square']:
                raise serializers.ValidationError("Overall square must be bigger or equal to living square")
        if data['overall_square'] and data['kitchen_square']:
            if data['overall_square'] < data['kitchen_square']:
                raise serializers.ValidationError("Overall square must be bigger than kitchen square")
        if data['living_square'] and data['kitchen_square']:
            if data['living_square'] < data['kitchen_square']:
                raise serializers.ValidationError("Living square must be bigger or equal to kitchen square")
        return data

    class Meta:
        model = Property
        fields = ['name', 'address', 'city', 'building_type', 'overall_floors', 'floor', 'decoration',
                  'overall_square', 'living_square', 'kitchen_square', 'view', 'balcony']
