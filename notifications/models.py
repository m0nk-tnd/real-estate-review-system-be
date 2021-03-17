from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from reviews.models import LandlordReview
from .views import send_email


class NotificationType(models.IntegerChoices):
    EMPTY = 0, _('Empty')
    REVIEW = 1, _('ReviewNotification')
    RATING = 2, _('TenantRatingNotification')


class NotificationContent(models.Model):
    data = models.JSONField()


class Notification(models.Model):
    type = models.IntegerField(choices=NotificationType.choices, default=NotificationType.EMPTY)
    content = models.OneToOneField(NotificationContent, related_name='notification', on_delete=models.CASCADE)


@receiver(post_save, sender=LandlordReview)
def create_notification_review(sender, instance, created, **kwargs):
    if created:
        content = NotificationContent.objects.create(data={
            'landlord': instance.review_on.landlord.id,
            'property': instance.review_on.name
        })
        Notification.objects.create(content=content, type=NotificationType.REVIEW)
        # send_email(content.data)
