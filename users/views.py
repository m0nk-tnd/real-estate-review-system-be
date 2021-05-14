from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import TenantProfileSerializer, LandlordProfileSerializer
from .models import TenantProfile, LandlordProfile


class TenantProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = TenantProfileSerializer
    queryset = TenantProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_fields = ['firstname', 'birth_date']
    ordering_fields = ['firstname', 'birth_date']


class TenantProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantProfileSerializer
    queryset = TenantProfile.objects.all()
    permission_classes = (IsAuthenticated,)


class LandlordProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = LandlordProfileSerializer
    queryset = LandlordProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_fields = ['firstname', 'birth_date']
    ordering_fields = ['firstname', 'birth_date']


class LandlordProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandlordProfileSerializer
    queryset = LandlordProfile.objects.all()
    permission_classes = (IsAuthenticated,)
