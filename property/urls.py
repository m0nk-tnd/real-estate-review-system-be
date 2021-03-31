from property.views import PropertyList, PropertyDetail
from django.urls import path

app_name = 'property'

urlpatterns = [
    path('landlord', PropertyList.as_view(), name='properties_list_create'),
    path('landlord/<int:pk>', PropertyDetail.as_view(), name='property_retrieve_update_delete'),
]
