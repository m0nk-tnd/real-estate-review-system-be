from property.models import Property, City
from property.serializers import PropertySerializer
from rest_framework import generics
from rest_framework import status, filters
from rest_framework.response import Response


class PropertyList(generics.ListCreateAPIView):
    search_fields = ['city__name', 'city__country']
    filter_backends = (filters.SearchFilter,)
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
