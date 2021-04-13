from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(receiver_user=self.kwargs['user_uuid'])
        return queryset
