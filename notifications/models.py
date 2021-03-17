from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from reviews.models import LandlordReview, TenantReview
from .views import send_email


class NotificationType(models.IntegerChoices):
    EMPTY = 0, _('Empty')
    REVIEW = 1, _('ReviewNotification')
    RATING = 2, _('TenantRatingNotification')


notification_templates = {
    NotificationType.REVIEW: 'review_notification.html',
    NotificationType.RATING: 'rating_notification.html',
}


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
        notification = Notification.objects.create(content=content, type=NotificationType.REVIEW)
        send_email(content.data, notification.type)


@receiver(post_save, sender=TenantReview)
def create_notification_rating(sender, instance, created, **kwargs):
    if created:
        content = NotificationContent.objects.create(data={
            'rated_user': instance.review_on.id,
            'landlord': instance.reviewer.id,
            'rating': instance.rating
        })
        notification = Notification.objects.create(content=content, type=NotificationType.RATING)
        send_email(content.data, notification.type)
