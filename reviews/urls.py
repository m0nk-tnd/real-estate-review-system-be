from django.urls import path

from .views import (
    TenantReviewListView, TenantReviewCreateView, TenantReviewDetailView,
    LandlordReviewListView, LandlordReviewCreateView, LandlordReviewDetailView
)

app_name = 'reviews'

urlpatterns = [
    path('tenant/reviews', TenantReviewListView.as_view(), name='list-tenant-review'),
    path('tenant/review/create', TenantReviewCreateView.as_view(), name='create-tenant-review'),
    path('tenant/review/<int:pk>', TenantReviewDetailView.as_view(), name='delete-update-retrieve-tenant-review'),

    path('landlord/reviews', LandlordReviewListView.as_view(), name='list-landlord-review'),
    path('landlord/review/create', LandlordReviewCreateView.as_view(), name='create-landlord-review'),
    path('landlord/review/<int:pk>', LandlordReviewDetailView.as_view(), name='delete-update-retrieve-landlord-review'),
]
