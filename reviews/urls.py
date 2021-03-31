from django.urls import path

from .views import (
    ReviewOnTenantListCreateView, ReviewOnTenantDetailView,
    ReviewOnLandlordPropertyListCreateView, ReviewOnLandlordPropertyDetailView
)

app_name = 'reviews'

urlpatterns = [
    path('tenant', ReviewOnTenantListCreateView.as_view(),
         name='list-create-tenant-review'),
    path('tenant/<int:pk>', ReviewOnTenantDetailView.as_view(),
         name='delete-update-retrieve-tenant-review'),

    path('landlord', ReviewOnLandlordPropertyListCreateView.as_view(),
         name='list-create-landlord-review'),
    path('landlord/<int:pk>', ReviewOnLandlordPropertyDetailView.as_view(),
         name='delete-update-retrieve-landlord-review'),
]
