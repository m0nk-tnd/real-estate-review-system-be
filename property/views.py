from .models import Property, City
from property.serializers import PropertySerializer
from rest_framework import generics


class PropertyList(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_fields = ['landlord', 'name', 'address', 'city']
    ordering_fields = ['address', 'city']
    search_fields = ['city__name', 'city__country__name']

    def perform_create(self, serializer):
        serializer.save(city=City.objects.get(name='Saint Petersburg'), landlord=self.request.user.landlordprofile)


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
