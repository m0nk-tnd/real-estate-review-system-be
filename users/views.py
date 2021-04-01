from rest_framework import generics

from url_filter.integrations.drf import DjangoFilterBackend

from users.serializers import TenantProfileSerializer, LandlordProfileSerializer
from .models import TenantProfile, LandlordProfile


class TenantProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = TenantProfileSerializer
    queryset = TenantProfile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['firstname', 'birth_date']


class TenantProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantProfileSerializer
    queryset = TenantProfile.objects.all()


class LandlordProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = LandlordProfileSerializer
    queryset = LandlordProfile.objects.all()


class LandlordProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandlordProfileSerializer
    queryset = LandlordProfile.objects.all()
