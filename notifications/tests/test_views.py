import datetime
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Notification, NotificationTemplate
from ..serializers import NotificationSerializer, NotificationTemplateSerializer
from ..views import NotificationList
from property.factories import CityFactory
from property.models import Property
from reviews.models import ReviewOnLandlordProperty, ReviewOnTenant
from users.models import LandlordProfile, TenantProfile

client = Client()


class TestUsersNotificationList(APITestCase):
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
        self.factory = RequestFactory()
        self.client.force_authenticate(self.user1)
        self.client.force_authenticate(self.user2)

    def test_landlord_notification_list(self):
        ReviewOnLandlordProperty.objects.create(reviewer=self.tenant, review_on=self.property,
                                                title='my review', description='cool property',
                                                rating=5)
        request = self.factory.get(reverse('notifications:users_notification_list'))
        request.user = self.user1
        view = NotificationList()
        view.setup(request)
        content = view.get_queryset()
        notification = Notification.objects.filter(receiver_user=self.user1.id)
        self.assertQuerysetEqual(content, map(repr, notification))
        response = NotificationList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response = self.client.get(reverse('notifications:users_notification_list'))
        # serializer = NotificationSerializer(notification)
        # self.assertEqual(len(response.json()['results']), 1)
        # self.assertEqual(response.json()['results'][0], serializer.data)

    # TODO: add auth when it's available
    def test_tenant_notification_list(self):
        ReviewOnTenant.objects.create(reviewer=self.property, review_on=self.tenant,
                                      title='My review on tenant Bob', description='He was nice and polite',
                                      rating=5)
        request = self.factory.get(reverse('notifications:users_notification_list'))
        request.user = self.user2
        view = NotificationList()
        view.setup(request)
        content = view.get_queryset()
        notifications = Notification.objects.filter(receiver_user=self.tenant.user.id)
        self.assertQuerysetEqual(content, map(repr, notifications))
        response = NotificationList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response = client.get(
        #     reverse('notifications:users_notification_list'))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # notification = Notification.objects.get(receiver_user=self.tenant.user.id)
        # serializer = NotificationSerializer(notification)
        # self.assertEqual(len(response.json()['results']), 1)
        # self.assertEqual(response.json()['results'][0], serializer.data)


class TestNotificationTemplateList(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='anna123')
        self.user1.set_password('12345')
        self.client.force_authenticate(self.user1)

    def test_notification_template_list(self):
        response = self.client.get(reverse('notifications:notification_template_list'))
        content = response.json()
        print(content)
        print(content['results'][0])
        serializer_review = NotificationTemplateSerializer(NotificationTemplate.objects.get(subject='Review'))
        serializer_rating = NotificationTemplateSerializer(NotificationTemplate.objects.get(subject='Rating'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['results'][0], serializer_review.data)
        self.assertEqual(content['results'][1], serializer_rating.data)
