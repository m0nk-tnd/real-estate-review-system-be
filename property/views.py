from .models import Property
from property.serializers import PropertySerializer
from rest_framework import generics


class PropertyList(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_fields = ['landlord', 'name', 'address', 'city']
    ordering_fields = ['address', 'city']
    search_fields = ['city__name', 'city__country__name']


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
