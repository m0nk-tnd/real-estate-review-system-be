from django.urls import path

from .views import (
    TenantReviewListView, TenantReviewCreateView, TenantReviewDetailView,
    LandlordReviewListView, LandlordReviewCreateView, LandlordReviewDetailView
)

urlpatterns = [
    path('tenant/reviews', TenantReviewListView.as_view()),
    path('tenant/review/create', TenantReviewCreateView.as_view()),
    path('tenant/review/<int:pk>', TenantReviewDetailView.as_view()),

    path('landlord/reviews', LandlordReviewListView.as_view()),
    path('landlord/review/create', LandlordReviewCreateView.as_view()),
    path('landlord/review/<int:pk>', LandlordReviewDetailView.as_view()),
]
