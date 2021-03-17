from django.contrib import admin
from .models import Notification, NotificationType, NotificationContent

admin.site.register(Notification)
admin.site.register(NotificationContent)
