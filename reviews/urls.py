from django.urls import path

from .views import (
    ReviewOnTenantCreateView, ReviewOnTenantListView, ReviewOnTenantDetailView,
    ReviewOnLandlordPropertyCreateView, ReviewOnLandlordPropertyListView, ReviewOnLandlordPropertyDetailView
)

app_name = 'reviews'

urlpatterns = [
    path('tenant/reviews', ReviewOnTenantListView.as_view(),
         name='list-tenant-review'),
    path('tenant/review/create', ReviewOnTenantCreateView.as_view(),
         name='create-tenant-review'),
    path('tenant/review/<int:pk>', ReviewOnTenantDetailView.as_view(),
         name='delete-update-retrieve-tenant-review'),

    path('landlord/reviews', ReviewOnLandlordPropertyListView.as_view(),
         name='list-landlord-review'),
    path('landlord/review/create', ReviewOnLandlordPropertyCreateView.as_view(),
         name='create-landlord-review'),
    path('landlord/review/<int:pk>', ReviewOnLandlordPropertyDetailView.as_view(),
         name='delete-update-retrieve-landlord-review'),
]
