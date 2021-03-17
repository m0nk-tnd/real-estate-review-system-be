import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from ..models import NotificationType, Notification, NotificationContent
from reviews.models import LandlordReview, TenantReview
from users.models import LandlordProfile, TenantProfile
from property.models import Property
from property.factories import CityFactory


class NotificationModelTest(TestCase):
    def setUp(self):
        self.content = NotificationContent.objects.create(data={
            'landlord_id': 1,
            'landlord_first_name': 'Anna',
            'landlord_last_name': 'Grigoreva',
            'property_name': 'castle',
            'tenant_first_name': 'Bob',
            'tenant_last_name': 'Adams',
            'review_title': 'The perfect castle',
            'review_text': 'It is very cool but cold',
            'review_rating': 5
        })
        self.notification = Notification.objects.create(content=self.content, type=NotificationType.REVIEW)

    def test_content_label(self):
        notification = Notification.objects.get(id=self.notification.id)
        field_label = notification._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_type_label(self):
        notification = Notification.objects.get(id=self.notification.id)
        field_label = notification._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'type')

    def test_data_label(self):
        content = NotificationContent.objects.get(id=self.content.id)
        field_label = content._meta.get_field('data').verbose_name
        self.assertEquals(field_label, 'data')


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
        LandlordReview.objects.create(reviewer=self.tenant, review_on=self.property,
                                      title='my review', description='cool property',
                                      rating=5)
        self.assertEqual(Notification.objects.all().count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Property review')
        TenantReview.objects.create(reviewer=self.property, review_on=self.tenant,
                                    title='my rating', description='cool tenant',
                                    rating=5)
        self.assertEqual(Notification.objects.all().count(), 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'Rating')
