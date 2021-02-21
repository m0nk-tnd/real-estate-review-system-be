from rest_framework import generics
from .serializers import (
    TenantReviewDetailSerializer, TenantReviewListSerializer,
    LandlordReviewListSerializer, LandlordReviewDetailSerializer,
)

from .models import TenantReview, LandlordReview


class TenantReviewCreateView(generics.CreateAPIView):
    serializer_class = TenantReviewDetailSerializer


class TenantReviewListView(generics.ListAPIView):
    serializer_class = TenantReviewListSerializer
    queryset = TenantReview.objects.all()


class TenantReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantReviewDetailSerializer
    queryset = TenantReview.objects.all()


class LandlordReviewCreateView(generics.CreateAPIView):
    serializer_class = LandlordReviewDetailSerializer


class LandlordReviewListView(generics.ListAPIView):
    serializer_class = LandlordReviewListSerializer
    queryset = LandlordReview.objects.all()


class LandlordReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandlordReviewDetailSerializer
    queryset = LandlordReview.objects.all()
