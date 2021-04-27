import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from ..models import NotificationType, Notification, NotificationTemplate
from ..tasks import send_email
from reviews.models import ReviewOnLandlordProperty, ReviewOnTenant
from users.models import LandlordProfile, TenantProfile
from property.models import Property
from property.factories import CityFactory


class NotificationTemplateTest(TestCase):
    def setUp(self):
        self.template = NotificationTemplate.objects.get(type=NotificationType.REVIEW)

    def test_type_label(self):
        field_label = self.template._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'type')

    def test_subject_label(self):
        field_label = self.template._meta.get_field('subject').verbose_name
        self.assertEquals(field_label, 'subject')

    def test_subject_max_length(self):
        max_length = self.template._meta.get_field('subject').max_length
        self.assertEquals(max_length, 255)


class NotificationTemplateReviewTest(TestCase):
    def setUp(self):
        self.template_review = NotificationTemplate.objects.get(type=NotificationType.REVIEW)
        self.template_rating = NotificationTemplate.objects.get(type=NotificationType.RATING)

    def test_type_value(self):
        self.assertEqual(self.template_review.type, NotificationType.REVIEW)
        self.assertEqual(self.template_rating.type, NotificationType.RATING)

    def test_subject_value(self):
        self.assertEqual(self.template_review.subject, 'Review')
        self.assertEqual(self.template_rating.subject, 'Rating')

    def test_email_template_value(self):
        self.assertEqual(self.template_review.email_template, 'ReviewNotification.html')
        self.assertEqual(self.template_rating.email_template, 'TenantRatingNotification.html')

    def test_system_template_value(self):
        self.assertEqual(self.template_review.system_template, 'ReviewNotification.html')
        self.assertEqual(self.template_rating.system_template, 'TenantRatingNotification.html')


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='anna123')
        self.user.set_password('12345')
        self.data = {
            'receiver_id': 1,
            'receiver_first_name': 'Anna',
            'receiver_last_name': 'Grigoreva',
            'property_name': 'castle',
            'reviewer_id': 1,
            'reviewer_first_name': 'Bob',
            'reviewer_last_name': 'Adams',
            'review_title': 'The perfect castle',
            'review_text': 'It is very cool but cold',
            'review_rating': 5,
        }

        self.notification = Notification.objects.create(
            data=self.data,
            template=NotificationTemplate.objects.get(type=NotificationType.REVIEW), sent=False, receiver_user=self.user)

    def test_data_label(self):
        notification = Notification.objects.get(id=self.notification.id)
        field_label = notification._meta.get_field('data').verbose_name
        self.assertEquals(field_label, 'data')

    def test_template_label(self):
        notification = Notification.objects.get(id=self.notification.id)
        field_label = notification._meta.get_field('template').verbose_name
        self.assertEquals(field_label, 'template')

    def test_sent_label(self):
        notification = Notification.objects.get(id=self.notification.id)
        field_label = notification._meta.get_field('sent').verbose_name
        self.assertEquals(field_label, 'sent')

    def test_date_created_label(self):
        notification = Notification.objects.get(id=self.notification.id)
        field_label = notification._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, 'date created')

    def test_receiver_user_label(self):
        notification = Notification.objects.get(id=self.notification.id)
        field_label = notification._meta.get_field('receiver_user').verbose_name
        self.assertEquals(field_label, 'receiver user')


class NotificationCreationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.user2 = User.objects.create(username='bob123')
        self.user2.set_password('67890')
        self.landlord = LandlordProfile.objects.create(user=self.user1, firstname='Anna',
                                                       lastname='Grigoreva', middlename='no',
                                                       birth_date=datetime.date(1999, 1, 18))
        self.tenant = TenantProfile.objects.create(user=self.user2, firstname='Bob',
                                                   lastname='Adams', middlename='no',
                                                   birth_date=datetime.date(1990, 4, 23))
        self.city = CityFactory()
        self.property = Property.objects.create(landlord=self.landlord , name='my property', address='my address',
                                                description='no description', city=self.city)

    def test_notification_creation(self):
        mail.outbox = []
        self.assertEqual(Notification.objects.all().count(), 0)
        ReviewOnLandlordProperty.objects.create(reviewer=self.tenant, review_on=self.property,
                                                title='my review', description='cool property',
                                                rating=5)
        self.assertEqual(Notification.objects.all().count(), 1)
        send_email.apply()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Review')
        ReviewOnTenant.objects.create(reviewer=self.property, review_on=self.tenant,
                                      title='my rating', description='cool tenant',
                                      rating=5)
        self.assertEqual(Notification.objects.all().count(), 2)
        send_email.apply()
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'Rating')
