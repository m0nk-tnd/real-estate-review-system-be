from rest_framework import generics
from .serializers import (
    TenantReviewDetailSerializer, TenantReviewListSerializer,
    LandlordReviewListSerializer, LandlordReviewDetailSerializer,
)

from .models import TenantReview, LandlordReview
from rest_framework.permissions import IsAuthenticated 

class TenantReviewCreateView(generics.CreateAPIView):
    serializer_class = TenantReviewDetailSerializer
    permission_classes = (IsAuthenticated, )

class TenantReviewListView(generics.ListAPIView):
    serializer_class = TenantReviewListSerializer
    queryset = TenantReview.objects.all()
    

class TenantReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantReviewDetailSerializer
    queryset = TenantReview.objects.all()
    permission_classes = (IsAuthenticated, )

class LandlordReviewCreateView(generics.CreateAPIView):
    serializer_class = LandlordReviewDetailSerializer
    permission_classes = (IsAuthenticated, )

class LandlordReviewListView(generics.ListAPIView):
    serializer_class = LandlordReviewListSerializer
    queryset = LandlordReview.objects.all()


class LandlordReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandlordReviewDetailSerializer
    queryset = LandlordReview.objects.all()
    permission_classes = (IsAuthenticated, )