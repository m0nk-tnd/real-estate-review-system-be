from .views import NotificationList
from django.urls import path

app_name = 'notifications'

urlpatterns = [
    path('<str:user_uuid>', NotificationList.as_view(), name='users_notification_list'),
]
