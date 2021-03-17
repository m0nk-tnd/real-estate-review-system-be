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
            'landlord_id': instance.review_on.landlord.id,
            'landlord_first_name': instance.review_on.landlord.firstname,
            'landlord_last_name': instance.review_on.landlord.lastname,
            'property_name': instance.review_on.name,
            'tenant_first_name': instance.reviewer.firstname,
            'tenant_last_name': instance.reviewer.lastname,
            'review_title': instance.title,
            'review_text': instance.description,
            'review_rating': instance.rating
        })
        notification = Notification.objects.create(content=content, type=NotificationType.REVIEW)
        send_email(content.data, notification.type)


@receiver(post_save, sender=TenantReview)
def create_notification_rating(sender, instance, created, **kwargs):
    if created:
        content = NotificationContent.objects.create(data={
            'rated_user_id': instance.review_on.id,
            'first_name': instance.review_on.firstname,
            'last_name': instance.review_on.lastname,
            'landlord_id': instance.reviewer.id,
            'landlord_first_name': instance.reviewer.landlord.firstname,
            'landlord_last_name': instance.reviewer.landlord.lastname,
            'review_title': instance.title,
            'review_text': instance.description,
            'rating': instance.rating
        })
        notification = Notification.objects.create(content=content, type=NotificationType.RATING)
        send_email(content.data, notification.type)
