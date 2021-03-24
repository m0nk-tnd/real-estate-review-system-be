from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ReviewOnTenantListSerializer, ReviewOnTenantDetailSerializer,
    ReviewOnLandlordPropertyListSerializer, ReviewOnLandlordPropertyDetailSerializer,
)

from .models import ReviewOnTenant, ReviewOnLandlordProperty


class ReviewOnTenantCreateView(generics.CreateAPIView):
    serializer_class = ReviewOnTenantDetailSerializer
    permission_classes = (IsAuthenticated, )


class ReviewOnTenantListView(generics.ListAPIView):
    serializer_class = ReviewOnTenantListSerializer
    queryset = ReviewOnTenant.objects.all()
    

class ReviewOnTenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewOnTenantDetailSerializer
    queryset = ReviewOnTenant.objects.all()
    # permission_classes = (IsAuthenticated, )


class ReviewOnLandlordPropertyCreateView(generics.CreateAPIView):
    serializer_class = ReviewOnLandlordPropertyDetailSerializer
    # permission_classes = (IsAuthenticated, )


class ReviewOnLandlordPropertyListView(generics.ListAPIView):
    serializer_class = ReviewOnLandlordPropertyListSerializer
    queryset = ReviewOnLandlordProperty.objects.all()


class ReviewOnLandlordPropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewOnLandlordPropertyDetailSerializer
    queryset = ReviewOnLandlordProperty.objects.all()
    # permission_classes = (IsAuthenticated, )
