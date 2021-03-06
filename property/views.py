from property.models import Property, City
from property.serializers import PropertySerializer
from rest_framework import generics
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 


class PropertyList(generics.ListCreateAPIView):
    search_fields = ['city__name', 'city__country__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Property.objects.all()
    serializer_class = PropertySerializer



class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (IsAuthenticated,)