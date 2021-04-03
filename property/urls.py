from property.views import PropertyList, PropertyDetail
from django.urls import path

app_name = 'property'

urlpatterns = [
    path('', PropertyList.as_view(), name='properties_list_create'),
    path('<int:pk>', PropertyDetail.as_view(), name='property_retrieve_update_delete'),
]
