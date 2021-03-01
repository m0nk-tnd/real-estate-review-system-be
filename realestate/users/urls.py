from django.urls import path

from .views import (
    TenantProfileCreateView, TenantProfileListView, TenantProfileDetailView,
    LandlordProfileCreateView, LandlordProfileListView, LandlordProfileDetailView,
)

urlpatterns = [
    path('tenant', TenantProfileListView.as_view()),
    path('tenant/create', TenantProfileCreateView.as_view()),
    path('tenant/<int:pk>', TenantProfileDetailView.as_view()),

    path('landlord', LandlordProfileListView.as_view()),
    path('landlord/create', LandlordProfileCreateView.as_view()),
    path('landlord/<int:pk>', LandlordProfileDetailView.as_view()),
]
