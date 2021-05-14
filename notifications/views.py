from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification, NotificationTemplate
from .serializers import NotificationSerializer, NotificationTemplateSerializer


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(receiver_user=self.request.user)
        return queryset


class NotificationTemplateList(generics.ListAPIView):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = (IsAuthenticated,)
