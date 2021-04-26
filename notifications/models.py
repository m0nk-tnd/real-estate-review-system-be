from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from reviews.models import ReviewOnLandlordProperty, ReviewOnTenant
from .tasks import send_email
from django.contrib.auth.models import User


class NotificationType(models.IntegerChoices):
    REVIEW = 1, _('ReviewNotification')
    RATING = 2, _('TenantRatingNotification')


class NotificationTemplate(models.Model):
    type = models.IntegerField(choices=NotificationType.choices, blank=True)
    subject = models.CharField(max_length=255)

    def _get_template(self):
        return NotificationType(self.type).label + '.html'

    email_template = property(_get_template)
    system_template = property(_get_template)


class Notification(models.Model):
    template = models.ForeignKey(NotificationTemplate, related_name='notifications', on_delete=models.CASCADE,
                                 null=True)
    data = models.JSONField(default=dict, null=True)
    sent = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    receiver_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE, null=True)


@receiver(post_save, sender=ReviewOnLandlordProperty)
def create_notification_review(sender, instance, created, **kwargs):
    if created:
        notification_type = NotificationType.REVIEW
        landlord = instance.review_on.landlord
        tenant = instance.reviewer
        property_instance = instance.review_on
        review = instance
        email_to = instance.review_on.landlord.user.email
        email_from = instance.reviewer.user.email
        data = {
            'receiver_id': landlord.id,
            'receiver_first_name': landlord.firstname,
            'receiver_last_name': landlord.lastname,
            'property_name': property_instance.name,
            'reviewer_id': tenant.id,
            'reviewer_first_name': tenant.firstname,
            'reviewer_last_name': tenant.lastname,
            'review_title': review.title,
            'review_text': review.description,
            'review_rating': review.rating,
            'email_to': email_to,
            'email_from': email_from,
        }
        create_notification(notification_type=notification_type, data=data, receiver_user=landlord.user)


@receiver(post_save, sender=ReviewOnTenant)
def create_notification_rating(sender, instance, created, **kwargs):
    if created:
        notification_type = NotificationType.RATING
        landlord = instance.reviewer.landlord
        tenant = instance.review_on
        property_instance = instance.reviewer
        review = instance
        email_to = instance.review_on.user.email
        email_from = instance.reviewer.landlord.user.email
        data = {
            'reviewer_id': landlord.id,
            'reviewer_first_name': landlord.firstname,
            'reviewer_last_name': landlord.lastname,
            'property_name': property_instance.name,
            'receiver_id': tenant.id,
            'receiver_first_name': tenant.firstname,
            'receiver_last_name': tenant.lastname,
            'review_title': review.title,
            'review_text': review.description,
            'review_rating': review.rating,
            'email_to': email_to,
            'email_from': email_from,
        }
        create_notification(notification_type=notification_type, data=data, receiver_user=tenant.user)


@receiver(post_save, sender=Notification)
def create_and_send_email(sender, instance, created, **kwargs):
    if created:
        send_email(instance)


def create_notification(notification_type, data, receiver_user):
    template = NotificationTemplate.objects.get(type=notification_type)
    Notification.objects.create(template=template, data=data, receiver_user=receiver_user)
