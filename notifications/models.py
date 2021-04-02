from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from reviews.models import ReviewOnLandlordProperty, ReviewOnTenant
from .views import send_email


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


@receiver(post_save, sender=ReviewOnLandlordProperty)
def create_notification_review(sender, instance, created, **kwargs):
    if created:
        notification_type = NotificationType.REVIEW
        data, subject = create_notification(notification_type=notification_type, landlord=instance.review_on.landlord,
                                            tenant=instance.reviewer, property_instance=instance.review_on,
                                            review=instance, email_to=instance.review_on.landlord.user.email,
                                            email_from=instance.reviewer.user.email)
        send_email(data, notification_type, subject)


@receiver(post_save, sender=ReviewOnTenant)
def create_notification_rating(sender, instance, created, **kwargs):
    if created:
        notification_type = NotificationType.RATING
        data, subject = create_notification(notification_type=notification_type,
                                            landlord=instance.reviewer.landlord, tenant=instance.review_on,
                                            property_instance=instance.reviewer, review=instance,
                                            email_to=instance.review_on.user.email,
                                            email_from=instance.reviewer.landlord.user.email)
        send_email(data, notification_type, subject)


def create_notification(notification_type, landlord, tenant, property_instance, review, email_to, email_from):
    data = {
        'landlord.id': landlord.id,
        'landlord_first_name': landlord.firstname,
        'landlord_last_name': landlord.lastname,
        'property_name': property_instance.name,
        'tenant_id': tenant.id,
        'tenant_first_name': tenant.firstname,
        'tenant_last_name': tenant.lastname,
        'review_title': review.title,
        'review_text': review.description,
        'review_rating': review.rating,
        'email_to': email_to,
        'email_from': email_from,
    }
    template = NotificationTemplate.objects.get(type=notification_type)
    Notification.objects.create(template=template, data=data)
    return data, template.subject
