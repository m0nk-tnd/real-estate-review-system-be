from django.urls import path

from .views import (
    ReviewOnTenantCreateView, ReviewOnTenantListView, ReviewOnTenantDetailView,
    ReviewOnLandlordPropertyCreateView, ReviewOnLandlordPropertyListView, ReviewOnLandlordPropertyDetailView
)

app_name = 'reviews'

urlpatterns = [
    path('tenants', ReviewOnTenantListView.as_view(),
         name='list-tenant-review'),
    path('tenant', ReviewOnTenantCreateView.as_view(),
         name='create-tenant-review'),
    path('tenant/<int:pk>', ReviewOnTenantDetailView.as_view(),
         name='delete-update-retrieve-tenant-review'),

    path('landlords', ReviewOnLandlordPropertyListView.as_view(),
         name='list-landlord-review'),
    path('landlord', ReviewOnLandlordPropertyCreateView.as_view(),
         name='create-landlord-review'),
    path('landlord/<int:pk>', ReviewOnLandlordPropertyDetailView.as_view(),
         name='delete-update-retrieve-landlord-review'),
]
