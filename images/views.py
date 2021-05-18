from .models import Image
from .serializers import ImageSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ImageViewSet(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated,)
