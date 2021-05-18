from .views import ImageViewSet
from django.urls import path

app_name = 'images'

urlpatterns = [
    path('', ImageViewSet.as_view(), name='image-list-upload'),
]