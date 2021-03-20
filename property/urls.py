from property.views import PropertyList, PropertyDetail
from django.urls import path

app_name = 'property'

urlpatterns = [
    path('property-list/', PropertyList.as_view(), name='properties_list_create'),
    path('property-detail/<int:pk>', PropertyDetail.as_view(), name='property_retrieve_update_delete'),
]
