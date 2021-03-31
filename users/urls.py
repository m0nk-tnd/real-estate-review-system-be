from django.urls import path

from users.views import (
    TenantProfileCreateView, TenantProfileListView, TenantProfileDetailView,
    LandlordProfileCreateView, LandlordProfileListView, LandlordProfileDetailView,
)

app_name = 'users'

urlpatterns = [
    path('tenants', TenantProfileListView.as_view(), name='list-tenant'),
    path('tenant', TenantProfileCreateView.as_view(), name='create-tenant'),
    path('tenant/<int:pk>', TenantProfileDetailView.as_view(), name='retrieve-update-delete-tenant'),

    path('landlords', LandlordProfileListView.as_view(), name='list-landlord'),
    path('landlord', LandlordProfileCreateView.as_view(), name='create-landlord'),
    path('landlord/<int:pk>', LandlordProfileDetailView.as_view(), name='retrieve-update-delete-landlord'),
]
