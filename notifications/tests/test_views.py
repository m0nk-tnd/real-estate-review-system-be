import datetime
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import Notification
from ..serializers import NotificationSerializer
from property.factories import CityFactory
from property.models import Property
from reviews.models import ReviewOnLandlordProperty, ReviewOnTenant
from users.models import LandlordProfile, TenantProfile

client = Client()


class TestUsersNotificationList(TestCase):
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
        self.property = Property.objects.create(landlord=self.landlord, name='my property', address='my address',
                                                description='no description', city=self.city)

    def test_landlord_notification_list(self):
        ReviewOnLandlordProperty.objects.create(reviewer=self.tenant, review_on=self.property,
                                                title='my review', description='cool property',
                                                rating=5)
        response = client.get(
            reverse('notifications:users_notification_list', kwargs={'user_uuid': self.landlord.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification = Notification.objects.get(receiver_user=self.landlord.uuid)
        serializer = NotificationSerializer(notification)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], serializer.data)

    def test_tenant_notification_list(self):
        ReviewOnTenant.objects.create(reviewer=self.property, review_on=self.tenant,
                                      title='My review on tenant Bob', description='He was nice and polite',
                                      rating=5)
        response = client.get(
            reverse('notifications:users_notification_list', kwargs={'user_uuid': self.tenant.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification = Notification.objects.get(receiver_user=self.tenant.uuid)
        serializer = NotificationSerializer(notification)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], serializer.data)
