from rest_framework import generics

from .serializers import TenantProfileSerializer, LandlordProfileSerializer
from .models import TenantProfile, LandlordProfile


class TenantProfileCreateView(generics.CreateAPIView):
    serializer_class = TenantProfileSerializer


class TenantProfileListView(generics.ListAPIView):
    serializer_class = TenantProfileSerializer
    queryset = TenantProfile.objects.all()


class TenantProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantProfileSerializer
    queryset = TenantProfile.objects.all()


class LandlordProfileCreateView(generics.CreateAPIView):
    serializer_class = LandlordProfileSerializer


class LandlordProfileListView(generics.ListAPIView):
    serializer_class = LandlordProfileSerializer
    queryset = LandlordProfile.objects.all()


class LandlordProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandlordProfileSerializer
    queryset = LandlordProfile.objects.all()
