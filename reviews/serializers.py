from rest_framework import serializers
from .models import ReviewOnTenant, ReviewOnLandlordProperty


class ReviewOnTenantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewOnTenant
        fields = ['title', 'description', 'rating', 'reviewer', 'review_on']


class ReviewOnTenantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewOnTenant
        fields = '__all__'


class ReviewOnLandlordPropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewOnLandlordProperty
        fields = ['title', 'description', 'rating', 'reviewer', 'review_on']


class ReviewOnLandlordPropertyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewOnLandlordProperty
        fields = '__all__'
