from property.views import PropertyList, PropertyDetail
from django.urls import path

app_name = 'property'
urlpatterns = [
    path('properties/', PropertyList.as_view(), name='properties_list_create'),
    path('properties/<int:pk>', PropertyDetail.as_view(), name='property'),
]
