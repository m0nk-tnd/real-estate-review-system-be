from .models import Image
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('thumbnail', 'thumbnail__500x500'),
        ]
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']
