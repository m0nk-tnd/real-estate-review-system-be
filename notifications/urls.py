from .views import NotificationList, NotificationTemplateList
from django.urls import path

app_name = 'notifications'

urlpatterns = [
    path('', NotificationList.as_view(), name='users_notification_list'),
    path('templates/', NotificationTemplateList.as_view(), name='notification_template_list'),
]
