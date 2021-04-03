from django.urls import path

from users.views import (
    TenantProfileListCreateView, TenantProfileDetailView,
    LandlordProfileListCreateView, LandlordProfileDetailView,
)

app_name = 'users'

urlpatterns = [
    path('tenant', TenantProfileListCreateView.as_view(), name='list-create-tenant'),
    path('tenant/<int:pk>', TenantProfileDetailView.as_view(), name='retrieve-update-delete-tenant'),

    path('landlord', LandlordProfileListCreateView.as_view(), name='list-create-landlord'),
    path('landlord/<int:pk>', LandlordProfileDetailView.as_view(), name='retrieve-update-delete-landlord'),
]
