from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ReviewOnTenantListSerializer, ReviewOnTenantDetailSerializer,
    ReviewOnLandlordPropertyListSerializer, ReviewOnLandlordPropertyDetailSerializer,
)

from .models import ReviewOnTenant, ReviewOnLandlordProperty


class ReviewOnTenantListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewOnTenantListSerializer
    queryset = ReviewOnTenant.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_fields = ['title', 'rating']
    ordering_fields = ['rating']
    

class ReviewOnTenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewOnTenantDetailSerializer
    queryset = ReviewOnTenant.objects.all()
    permission_classes = (IsAuthenticated, )


class ReviewOnLandlordPropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewOnLandlordPropertyListSerializer
    queryset = ReviewOnLandlordProperty.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_fields = ['title', 'rating']
    ordering_fields = ['rating']


class ReviewOnLandlordPropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewOnLandlordPropertyDetailSerializer
    queryset = ReviewOnLandlordProperty.objects.all()
    permission_classes = (IsAuthenticated, )
