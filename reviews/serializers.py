from rest_framework import serializers
from .models import TenantReview, LandlordReview


class TenantReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantReview
        fields = ['title', 'description', 'rating', 'reviewer', 'review_on']


class TenantReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantReview
        fields = '__all__'


class LandlordReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordReview
        fields = ['title', 'description', 'rating', 'reviewer', 'review_on']


class LandlordReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordReview
        fields = '__all__'
