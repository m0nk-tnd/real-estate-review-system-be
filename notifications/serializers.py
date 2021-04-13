from rest_framework import serializers
from .models import Notification, NotificationType


class NotificationSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, notification):
        type_notification = notification.template.type
        return NotificationType(type_notification).label

    class Meta:
        model = Notification
        fields = ['sent', 'date_created', 'type']
